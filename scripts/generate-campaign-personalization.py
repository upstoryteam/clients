#!/usr/bin/env python3
"""Merge company news into campaign contacts and generate personalization lines."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from repo_paths import ROOT, gcp_service_account_path, wave2_news_csv

KEY = gcp_service_account_path()
DEST_SHEET_ID = "1hbvYiOBm4gKPEIiO59x7II-52ZPcE19n2bp-u1iminM"
DEST_TAB = "Sheet1"
NEWS_CSV = wave2_news_csv()
CONTACTS_CSV = ROOT / "data" / "wave2-campaign-contacts-ready.csv"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

BANNED = re.compile(
    r"(thought i'd get on your radar|i noticed|i came across|"
    r"recent funding round|activation moment we've spent|"
    r"where it gets real|it's not .+ it's |ecosystem|leverage|front and center|—)",
    re.I,
)

# Map Top Opportunity to a theme one level up (human segue, not brief copy)
THEME_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"tap-in|device setup|check-in|onboard|first routine|first week|active profile", re.I), "onboarding"),
    (re.compile(r"discovery|booking|search lead|schedule|reservation|itinerary|trip", re.I), "booking"),
    (re.compile(r"wire|payment|transaction|commission|closing|incorporation", re.I), "money_moment"),
    (re.compile(r"therapy|care path|symptom|clinical|care-plan|prescreen|study fit", re.I), "care_intake"),
    (re.compile(r"claim|document|auth|formation|legal|eligibility|paperwork", re.I), "paperwork"),
    (re.compile(r"scenario|planning|assessment|readiness", re.I), "early_planning"),
    (re.compile(r"useful view|bank|account|budget|financial", re.I), "financial_setup"),
    (re.compile(r"driver|both sides|contractor|marketplace|coverage|referral", re.I), "two_sided"),
    (re.compile(r"class|teacher|school|student|family", re.I), "household"),
]

THEME_SEGUES: dict[str, list[str]] = {
    "onboarding": [
        "onboarding moments that create value early is where we spend our time",
        "the early product experience before someone is fully in is most of what we work on",
        "getting the first session to feel worth it is where we spend our time",
    ],
    "booking": [
        "discovery-to-commitment in consumer products is the kind of thing we tend to look at",
        "moving people from interest to action early is adjacent to what we work on",
    ],
    "money_moment": [
        "we're not fintech operators, but early conversion in consumer products is the overlap we tend to look at",
        "products where money shows up early are adjacent to what we work on, mostly on the onboarding side",
        "the early experience before things get serious is the lane we spend time in",
    ],
    "care_intake": [
        "consumer health with a heavy early experience is adjacent to what we work on",
        "early decisions before the paperwork pile is the kind of thing we tend to look at",
    ],
    "paperwork": [
        "guided flows through paperwork-heavy steps is where we spend our time",
        "moments before a long form or document dump is most of what we work on",
    ],
    "early_planning": [
        "early planning before a big data ask is where we spend our time",
        "first-planning experiences that do not feel like homework is most of what we work on",
    ],
    "financial_setup": [
        "first-week consumer app experiences are what we work on, and money apps have that same early-experience problem",
        "linking and setup before the product proves itself is adjacent to what we tend to look at",
        "consumer onboarding in apps like this is the kind of thing we spend time on",
    ],
    "two_sided": [
        "two-sided consumer flows with an early handoff are the kind of thing we tend to look at",
        "marketplace products before either side commits are adjacent to what we work on",
    ],
    "household": [
        "household and classroom onboarding that sticks is where we spend our time",
        "first-use moments in shared settings is most of what we work on",
    ],
    "default": [
        "early conversion in consumer products is where we spend our time",
        "the first stretch of the product experience is most of what we work on",
    ],
}


def pick(seed: str, options: list[str]) -> str:
    if not options:
        return ""
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return options[h % len(options)]


def theme_key(top_opportunity: str) -> str:
    top = top_opportunity or ""
    for pat, key in THEME_RULES:
        if pat.search(top):
            return key
    return "default"


def theme_segue(top_opportunity: str, seed: str) -> str:
    key = theme_key(top_opportunity)
    return pick(f"{seed}:theme:{key}", THEME_SEGUES[key])


def cap_sentence(s: str) -> str:
    s = s.strip()
    return s[0].upper() + s[1:] if s else s


def news_hook(company: str, slug: str, summary: str, strength: str) -> str | None:
    s = (summary or "").strip()
    if not s or "no notable recent news" in s.lower():
        return None
    if strength not in {"Strong", "Moderate", "Weak"}:
        return None
    low = s.lower()
    co = company.strip()

    # Specific, human hooks (prefer these over generic parsers)
    if slug == "blackbird-labs":
        return "congrats on the Blackbird Club updates"
    if slug == "boldin":
        return pick(slug, ["saw the AI Planner Assistant launch", "nice Boldin product push lately"])
    if slug == "bookend-ai":
        return pick(slug, ["nice to see Bookend close the round", "congrats on getting the round done"])
    if slug == "certifid":
        return pick(slug, ["congrats on the Series C", "big CertifID news with the Series C"])
    if slug == "doctronic":
        return pick(slug, ["congrats on the Series B", "nice raise at Doctronic"])
    if slug == "doola":
        return "congrats on the Lovable partnership"
    if slug == "empathy":
        return "congrats on launching Empathy Connect"
    if slug == "empower":
        return "congrats on crossing 500,000 rides"
    if slug == "ezpag":
        return pick(slug, ["saw EzPag close the debt round", "nice financing news at EzPag"])
    if slug == "firstbase":
        return "congrats on the AppDirect deal"
    if slug == "medmo":
        return "congrats on the Covera merger"
    if slug == "merri":
        return "saw Tripleseat launch the new event management tools"
    if slug == "sparrow-bioacoustics":
        return "congrats on the award recognition"
    if slug == "the-realest":
        return "congrats on the PGA Championship partnership"
    if slug == "wheel-the-world":
        return "congrats on launching the AI accessibility travel agent"
    if slug == "zevo":
        return pick(slug, ["nice momentum at Zevo lately", "congrats on the recent press"])

    if re.search(r"series ([a-z])\b", low):
        letter = re.search(r"series ([a-z])\b", low).group(1).upper()
        return pick(
            slug,
            [
                f"congrats on the Series {letter}",
                f"nice to see the Series {letter} come together",
            ],
        )

    if "merged with" in low or "merger" in low:
        return pick(slug, [f"congrats on the merger", f"big news with the merger at {co}"])

    if "partnership" in low:
        partner = ""
        m = re.search(r"partnership with ([A-Za-z0-9]+)", summary, re.I)
        if m:
            partner = m.group(1)
        if partner:
            return f"congrats on the {partner} partnership"
        return f"congrats on the new partnership"

    if "acquired" in low or "acquisition" in low:
        return pick(
            slug,
            [
                f"congrats on the acquisition news",
                f"interesting acquisition news at {co}",
            ],
        )

    if "launched" in low or "launching" in low:
        return pick(
            slug,
            [
                f"congrats on the recent launch",
                f"nice launch momentum at {co}",
            ],
        )

    if "funding" in low or "raised" in low:
        return pick(
            slug,
            [
                f"congrats on the raise",
                f"nice to see {co} close the round",
                f"looks like {co} just raised",
            ],
        )

    if "award" in low or "finalist" in low:
        return "congrats on the recognition"

    return None


def segue_with_news(name: str, company: str, hook: str, top: str, seed: str) -> str:
    hook_s = hook[0].lower() + hook[1:] if hook else hook
    segue = cap_sentence(theme_segue(top, seed))
    templates = [
        f"Hi {name}, {hook_s}. {segue}, wanted to drop a line.",
        f"Hi {name}, {hook_s}. {segue}, figured I'd reach out.",
    ]
    return pick(seed, templates)


def cold_read_rank1(name: str, company: str, title: str, top: str, seed: str) -> str:
    segue = cap_sentence(theme_segue(top, seed))
    title_low = (title or "").lower()
    if any(x in title_low for x in ("founder", "ceo", "co-founder", "president", "owner")):
        options = [
            f"Hi {name}, love what you're doing with {company}. {segue}, wanted to drop a line.",
            f"Hi {name}, {company} stuck out. {segue}, figured I'd reach out.",
            f"Hi {name}, {company} is one of those products where people commit before the payoff is obvious. Quick hello.",
        ]
    elif any(x in title_low for x in ("product", "cpo", "cto")):
        options = [
            f"Hi {name}, most of my work is the early product experience in consumer apps. {company} fit that pattern, wanted to drop a line.",
            f"Hi {name}, {company} felt worth a note on the onboarding side. {segue}, figured I'd reach out.",
        ]
    elif any(x in title_low for x in ("growth", "marketing", "gtm")):
        options = [
            f"Hi {name}, growth at {company} seems tied to the early experience. Figured the growth desk was the right hello.",
            f"Hi {name}, {company} caught my eye on early conversion. {segue}, wanted to drop a line.",
        ]
    else:
        options = [
            f"Hi {name}, {company} caught my eye on the consumer onboarding side. {segue}, figured I'd reach out.",
            f"Hi {name}, {company} stuck out. {segue}, wanted to drop a line.",
        ]
    return pick(seed, options)


def rank2_line(name: str, company: str, title: str, hook: str | None, seed: str) -> str:
    title_low = (title or "").lower()
    if hook:
        hook_s = hook[0].lower() + hook[1:]
        if "product" in title_low or "cpo" in title_low:
            return f"Hi {name}, {hook_s}. Figured the product desk at {company} was the right hello."
        if "growth" in title_low or "marketing" in title_low:
            return f"Hi {name}, {hook_s}. Figured the growth side of {company} was worth a quick note."
        return f"Hi {name}, {hook_s}. Figured your lane at {company} was the right place for a note."

    if "product" in title_low or "cpo" in title_low:
        return f"Hi {name}, figured the product desk at {company} was the right hello."
    if "growth" in title_low or "marketing" in title_low:
        return f"Hi {name}, figured the growth side of {company} was the right place to send a note."
    if "cto" in title_low or "engineering" in title_low:
        return f"Hi {name}, the systems side at {company} seemed like the right hello."
    if "operations" in title_low or "strategy" in title_low:
        return f"Hi {name}, ops at {company} usually owns more of the user flow than people expect. Quick hello."
    return f"Hi {name}, figured I'd reach out with a short note on {company}."


def rank3_line(name: str, company: str, title: str, seed: str) -> str:
    title_low = (title or "").lower()
    if "operations" in title_low or "strategy" in title_low:
        return f"Hi {name}, figured your lane at {company} was the right place for a short note."
    if "engineering" in title_low or "data" in title_low:
        return f"Hi {name}, quick hello from the outside on the {company} product experience."
    return pick(
        seed,
        [
            f"Hi {name}, figured I'd reach out with a short note on {company}.",
            f"Hi {name}, quick hello on the {company} side.",
        ],
    )


def generate_personalization(row: dict, company_state: dict[str, dict]) -> str:
    name = (row.get("First Name") or "there").strip() or "there"
    company = (row.get("Company") or "").strip()
    title = (row.get("Job Title") or "").strip()
    slug = (row.get("Slug") or "").strip()
    rank = int(row.get("Rank at company") or 1)
    top = (row.get("Top Opportunity") or "").strip()
    summary = (row.get("company_news") or "").strip()
    strength = (row.get("company_news_signal") or "").strip()
    seed = f"{slug}:{rank}:{name}"

    state = company_state.setdefault(
        slug, {"used_news": False, "hook": news_hook(company, slug, summary, strength)}
    )
    hook = state["hook"]

    if rank == 1:
        if hook and not state["used_news"]:
            line = segue_with_news(name, company, hook, top, seed)
            state["used_news"] = True
        else:
            line = cold_read_rank1(name, company, title, top, seed)
    elif rank == 2:
        alt_hook = None if state["used_news"] else hook
        line = rank2_line(name, company, title, alt_hook, seed)
        if alt_hook:
            state["used_news"] = True
    else:
        line = rank3_line(name, company, title, seed)

    line = re.sub(r"\s+", " ", line).strip()
    if BANNED.search(line):
        line = cold_read_rank1(name, company, title, top, seed + ":fallback")
    return line


def load_news() -> dict[str, dict]:
    by_slug: dict[str, dict] = {}
    with NEWS_CSV.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            slug = (r.get("Slug") or "").strip()
            if not slug:
                continue
            by_slug[slug] = {
                "company_news": (r.get("Recent News Summary") or "").strip(),
                "company_news_signal": (r.get("News Signal Strength") or "").strip(),
            }
    return by_slug


def main() -> None:
    if not NEWS_CSV.is_file():
        raise SystemExit(f"Missing news export: {NEWS_CSV}")
    news_by_slug = load_news()
    rows = list(csv.DictReader(CONTACTS_CSV.open(newline="", encoding="utf-8")))

    base_header = [
        k
        for k in rows[0].keys()
        if k not in {"company_news", "company_news_signal", "personalization"}
    ]
    insert_at = base_header.index("Top Opportunity") + 1
    header = (
        base_header[:insert_at]
        + ["company_news", "company_news_signal", "personalization"]
        + base_header[insert_at:]
    )

    company_state: dict[str, dict] = {}
    out_rows: list[dict] = []
    for r in rows:
        slug = r.get("Slug", "")
        extra = news_by_slug.get(slug, {})
        merged = {**r, **extra}
        merged["personalization"] = generate_personalization(merged, company_state)
        out_rows.append(merged)

    with CONTACTS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(out_rows)

    body = [header] + [[r.get(h, "") for h in header] for r in out_rows]
    creds = service_account.Credentials.from_service_account_file(str(KEY), scopes=SCOPES)
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    svc.spreadsheets().values().clear(
        spreadsheetId=DEST_SHEET_ID, range=f"'{DEST_TAB}'!A:ZZ"
    ).execute()
    svc.spreadsheets().values().update(
        spreadsheetId=DEST_SHEET_ID,
        range=f"'{DEST_TAB}'!A1",
        valueInputOption="USER_ENTERED",
        body={"values": body},
    ).execute()

    print(f"Updated {len(out_rows)} contacts")
    print(f"Sheet: https://docs.google.com/spreadsheets/d/{DEST_SHEET_ID}/edit")
    print(f"CSV: {CONTACTS_CSV}")


if __name__ == "__main__":
    main()
