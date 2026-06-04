#!/usr/bin/env python3
"""Build send-ready contact list (max 3 per company) with Apollo emails + brief URLs → Google Sheet."""

from __future__ import annotations

import csv
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from repo_paths import ROOT, gcp_service_account_path

KEY = gcp_service_account_path()
APOLLO_SHEET_ID = "1fR-11ZbAJhR8wSkaatKKDq4G9iKsTWjZwUIY4mtfq-E"
APOLLO_TAB = "apollo-contacts-export (2)"
DEST_SHEET_ID = "1hbvYiOBm4gKPEIiO59x7II-52ZPcE19n2bp-u1iminM"
DEST_TAB = "Sheet1"
LIVE_BRIEF_BASE = "https://clients.upstory.co"
# Local audit preview — run: ./scripts/serve-local.sh
LOCAL_PREVIEW_BASE = "http://localhost:8765"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

CAP = 3

HEADER = [
    # Who (scan first)
    "First Name",
    "Last Name",
    "Full Name",
    "Job Title",
    "Company",
    "Domain",
    "Company Website URL",
    "Company LinkedIn URL",
    # Send + brief
    "Email",
    "Email Status",
    "LinkedIn URL",
    "Growth Brief URL (live)",
    "Growth Brief preview (local)",
    "Growth Brief preview (file)",
    "Headline",
    "Priority",
    "Rank at company",
    # Spot-check context (from growth brief review)
    "Inferred Goals",
    "Outreach Insight",
    "Top Opportunity",
    # Trailing metadata
    "Slug",
    "Location",
    "Seniority (Apollo)",
    "Contact source",
    "Title rank score",
    "Row #",
]

NEGATIVE_TITLE = re.compile(
    r"\b(recruiter|talent acquisition|human resources|\bhr\b|sourcer|"
    r"account executive|business development representative|\bbdr\b|\bsdr\b|"
    r"customer success|support specialist|intern\b|board member|board of|"
    r"advisor|advisory|investor relations)\b",
    re.I,
)

POSITIVE_RULES: list[tuple[int, re.Pattern]] = [
    (200, re.compile(r"\b(ceo|chief executive)\b", re.I)),
    (195, re.compile(r"\bco-?founder\b", re.I)),
    (190, re.compile(r"\bfounder\b", re.I)),
    (185, re.compile(r"\bowner\b", re.I)),
    (180, re.compile(r"\bpresident\b", re.I)),
    (175, re.compile(r"\bchief product\b|\bcpo\b", re.I)),
    (170, re.compile(r"\bchief technology\b|\bcto\b", re.I)),
    (168, re.compile(r"\bchief operating\b|\bcoo\b", re.I)),
    (165, re.compile(r"\bchief marketing\b|\bcmo\b", re.I)),
    (160, re.compile(r"\bchief growth\b", re.I)),
    (155, re.compile(r"\bvp\b.*\b(product|growth|marketing|engineering)\b", re.I)),
    (155, re.compile(r"\bvice president\b.*\b(product|growth|marketing|engineering)\b", re.I)),
    (150, re.compile(r"\bvp\b", re.I)),
    (145, re.compile(r"\bvice president\b", re.I)),
    (140, re.compile(r"\bhead of\b.*\b(product|growth|marketing|engineering)\b", re.I)),
    (130, re.compile(r"\bhead of\b", re.I)),
    (125, re.compile(r"\bgeneral manager\b|\bgm\b", re.I)),
    (120, re.compile(r"\bdirector\b.*\b(product|growth|marketing|engineering)\b", re.I)),
    (110, re.compile(r"\bdirector\b", re.I)),
    (100, re.compile(r"\bproduct manager\b", re.I)),
    (90, re.compile(r"\bmanager\b", re.I)),
]


def norm_domain(d: str) -> str:
    d = (d or "").strip().lower()
    d = re.sub(r"^https?://(www\.)?", "", d)
    return d.split("/")[0].split("?")[0]


def norm_linkedin(u: str) -> str:
    u = (u or "").strip().lower().rstrip("/")
    u = re.sub(r"\?.*", "", u)
    m = re.search(r"linkedin\.com/in/([^/#?]+)", u)
    return m.group(1) if m else ""


def title_rank(title: str, clay_score: int = 0) -> int:
    t = title or ""
    if NEGATIVE_TITLE.search(t):
        return min(clay_score, 40) if clay_score else 25
    score = 0
    for pts, pat in POSITIVE_RULES:
        if pat.search(t):
            score = max(score, pts)
    if score:
        return score + min(clay_score // 10, 5)
    return clay_score or 50


def load_apollo(svc) -> list[dict]:
    res = (
        svc.spreadsheets()
        .values()
        .get(spreadsheetId=APOLLO_SHEET_ID, range=f"'{APOLLO_TAB}'!A1:ZZ")
        .execute()
    )
    rows = res.get("values", [])
    if not rows:
        return []
    headers = rows[0]
    idx = {h: i for i, h in enumerate(headers)}

    def cell(row: list, name: str) -> str:
        i = idx.get(name)
        if i is None or i >= len(row):
            return ""
        return (row[i] or "").strip()

    out = []
    for row in rows[1:]:
        email = cell(row, "Email")
        if not email:
            continue
        out.append(
            {
                "first_name": cell(row, "First Name"),
                "last_name": cell(row, "Last Name"),
                "full_name": f"{cell(row, 'First Name')} {cell(row, 'Last Name')}".strip(),
                "job_title": cell(row, "Title"),
                "email": email,
                "email_status": cell(row, "Email Status"),
                "seniority": cell(row, "Seniority"),
                "location": ", ".join(
                    x
                    for x in [
                        cell(row, "City"),
                        cell(row, "State"),
                        cell(row, "Country"),
                    ]
                    if x
                ),
                "linkedin": cell(row, "Person Linkedin Url"),
                "domain": norm_domain(cell(row, "Website")),
                "company_website_url": cell(row, "Website"),
                "company_linkedin_url": cell(row, "Company Linkedin Url"),
                "company_name": cell(row, "Company Name"),
                "source": "apollo",
                "title_score": 0,
            }
        )
    return out


def load_brief_meta() -> dict[str, dict]:
    path = ROOT / "growth-brief-review.csv"
    meta: dict[str, dict] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slug = (r.get("Slug") or "").strip()
            if not slug:
                continue
            meta[slug] = {
                "brief_url": (r.get("Brief URL") or f"{LIVE_BRIEF_BASE}/{slug}").strip(),
                "headline": (r.get("Headline") or "").strip(),
                "company": (r.get("Company Name") or "").strip(),
                "inferred_goals": (r.get("About") or "").strip(),
                "outreach_insight": (r.get("Outreach Insight") or "").strip(),
                "top_opportunity": (r.get("Top Opportunity") or "").strip(),
            }
    return meta


def brief_urls(slug: str, meta: dict) -> tuple[str, str, str]:
    live = meta.get("brief_url") or f"{LIVE_BRIEF_BASE}/{slug}"
    preview = f"{LOCAL_PREVIEW_BASE.rstrip('/')}/{slug}/index.html"
    file_preview = (ROOT / slug / "index.html").resolve().as_uri()
    return live, preview, file_preview


PREVIEW_PORT = 8765


def preview_port_open(port: int = PREVIEW_PORT) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def ensure_preview_server(port: int = PREVIEW_PORT) -> str:
    """Start local http.server for brief previews if nothing is listening."""
    base = f"http://localhost:{port}"
    if preview_port_open(port):
        print(f"Preview server already running at {base}")
        return base
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            str(port),
            "--bind",
            "127.0.0.1",
        ],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(40):
        if preview_port_open(port):
            print(f"Started preview server at {base}")
            return base
        time.sleep(0.125)
    print(
        f"Warning: could not confirm preview server on port {port}. "
        f"Run: ./scripts/serve-local.sh",
        file=sys.stderr,
    )
    return base


def build_output_row(
    row_num: int,
    ship: dict,
    meta: dict,
    slug: str,
    company: str,
    rank_at_co: int,
    c: dict,
) -> list[str]:
    priority = c.get("priority") or ship.get("priority", "")
    live_url, preview_url, file_preview_url = brief_urls(slug, meta)
    return [
        c.get("first_name", ""),
        c.get("last_name", ""),
        c.get("full_name", ""),
        c.get("job_title", ""),
        company,
        c.get("domain") or norm_domain(ship.get("domain", "")),
        c.get("company_website_url") or f"https://{c.get('domain') or norm_domain(ship.get('domain', ''))}",
        c.get("company_linkedin_url", ""),
        c.get("email", ""),
        c.get("email_status", ""),
        c.get("linkedin", ""),
        live_url,
        preview_url,
        file_preview_url,
        meta.get("headline", ""),
        f"P{priority}" if priority else "",
        str(rank_at_co),
        meta.get("inferred_goals", ""),
        meta.get("outreach_insight", ""),
        meta.get("top_opportunity", ""),
        c.get("slug") or ship.get("slug", ""),
        c.get("location", ""),
        c.get("seniority", ""),
        c.get("source", ""),
        str(c.get("rank_score", "")),
        str(row_num),
    ]


def main() -> None:
    if not KEY.is_file():
        raise SystemExit(f"Missing service account key: {KEY}")

    ship_by_slug = {}
    with (ROOT / "data/wave2-ship-status.csv").open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("ship_status") != "ship":
                continue
            ship_by_slug[r["slug"]] = r

    brief_meta = load_brief_meta()

    capped = []
    with (ROOT / "data/wave2-contacts-capped.csv").open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slug = r.get("slug", "")
            if slug not in ship_by_slug:
                continue
            capped.append(
                {
                    "slug": slug,
                    "priority": r.get("priority", ship_by_slug[slug].get("priority", "")),
                    "casual_name": r.get("casual_name", ""),
                    "domain": norm_domain(r.get("domain", "")),
                    "first_name": r.get("first_name", ""),
                    "last_name": r.get("last_name", ""),
                    "full_name": r.get("full_name", ""),
                    "job_title": r.get("job_title", ""),
                    "location": r.get("location", ""),
                    "linkedin": r.get("linkedin", ""),
                    "company_website_url": f"https://{norm_domain(r.get('domain', ''))}",
                    "company_linkedin_url": "",
                    "source": "clay",
                    "title_score": int(r.get("title_score") or 0),
                    "email": "",
                    "email_status": "",
                    "seniority": "",
                }
            )

    creds = service_account.Credentials.from_service_account_file(str(KEY), scopes=SCOPES)
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    apollo = load_apollo(svc)

    # Index Apollo by linkedin slug and domain
    apollo_by_li: dict[str, list[dict]] = {}
    apollo_by_domain: dict[str, list[dict]] = {}
    for a in apollo:
        li = norm_linkedin(a["linkedin"])
        if li:
            apollo_by_li.setdefault(li, []).append(a)
        if a["domain"]:
            apollo_by_domain.setdefault(a["domain"], []).append(a)

    def enrich_email(c: dict) -> dict:
        if c.get("email"):
            return c
        li = norm_linkedin(c.get("linkedin", ""))
        matches = []
        if li and li in apollo_by_li:
            matches = apollo_by_li[li]
        elif c.get("domain") in apollo_by_domain:
            dom_matches = apollo_by_domain[c["domain"]]
            fn = (c.get("first_name") or "").lower()
            ln = (c.get("last_name") or "").lower()
            for a in dom_matches:
                if fn and fn in a["first_name"].lower() and (not ln or ln in a["last_name"].lower()):
                    matches.append(a)
            if not matches:
                matches = dom_matches
        if matches:
            best = sorted(
                matches,
                key=lambda x: (
                    0 if x["email_status"] == "Verified" else 1,
                    -title_rank(x["job_title"]),
                ),
            )[0]
            c = {**c, **best, "source": c["source"] + "+apollo"}
        return c

    # Candidates per slug
    by_slug: dict[str, list[dict]] = {}

    for c in capped:
        slug = c["slug"]
        row = enrich_email(c)
        by_slug.setdefault(slug, []).append(row)

    ship_domains = {norm_domain(v["domain"]) for v in ship_by_slug.values()}
    for a in apollo:
        if a["domain"] not in ship_domains:
            continue
        slug = None
        for s, info in ship_by_slug.items():
            if norm_domain(info["domain"]) == a["domain"]:
                slug = s
                break
        if not slug:
            continue
        a = {
            **a,
            "slug": slug,
            "priority": ship_by_slug[slug].get("priority", ""),
            "casual_name": ship_by_slug[slug].get("casual_name", a["company_name"]),
        }
        by_slug.setdefault(slug, []).append(a)

    def dedupe_key(c: dict) -> str:
        if c.get("email"):
            return f"email:{c['email'].lower()}"
        li = norm_linkedin(c.get("linkedin", ""))
        if li:
            return f"li:{li}"
        return f"name:{c.get('full_name','').lower()}|{c.get('domain','')}"

    final_rows: list[list[str]] = []
    row_num = 0
    companies_with_contacts = 0

    for slug in sorted(
        by_slug.keys(),
        key=lambda s: (
            int(ship_by_slug[s].get("priority") or 99),
            ship_by_slug[s].get("casual_name", "").lower(),
        ),
    ):
        ship = ship_by_slug[slug]
        meta = brief_meta.get(slug, {})
        company = meta.get("company") or ship.get("casual_name", "")

        seen = set()
        candidates = []
        for c in by_slug[slug]:
            k = dedupe_key(c)
            if k in seen:
                continue
            seen.add(k)
            if not c.get("email"):
                continue
            rank = title_rank(c.get("job_title", ""), int(c.get("title_score") or 0))
            email_bonus = 0 if c.get("email_status") == "Verified" else -5
            candidates.append({**c, "rank_score": rank + email_bonus})

        candidates.sort(key=lambda x: (-x["rank_score"], x.get("full_name", "")))
        picks = candidates[:CAP]
        if not picks:
            continue
        companies_with_contacts += 1

        for i, c in enumerate(picks, start=1):
            row_num += 1
            c["slug"] = slug
            final_rows.append(
                build_output_row(row_num, ship, meta, slug, company, i, c)
            )

    out_csv = ROOT / "data/wave2-campaign-contacts-ready.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(final_rows)

    # Plain full URLs in sheet (no HYPERLINK labels) so slugs are visible for mapping.
    body = [HEADER] + final_rows
    svc.spreadsheets().values().clear(
        spreadsheetId=DEST_SHEET_ID, range=f"'{DEST_TAB}'!A:ZZ"
    ).execute()
    svc.spreadsheets().values().update(
        spreadsheetId=DEST_SHEET_ID,
        range=f"'{DEST_TAB}'!A1",
        valueInputOption="USER_ENTERED",
        body={"values": body},
    ).execute()

    ensure_preview_server()

    print(f"Companies with send-ready contacts: {companies_with_contacts}")
    print(f"Total contact rows (max {CAP}/co): {len(final_rows)}")
    print(f"Wrote {out_csv}")
    print(f"Uploaded to https://docs.google.com/spreadsheets/d/{DEST_SHEET_ID}/edit")
    print(f"Preview URLs: {LOCAL_PREVIEW_BASE}/<slug>/index.html")
    print("Share the destination sheet with the service account email if the tab looks empty.")


if __name__ == "__main__":
    main()
