#!/usr/bin/env python3
"""Generate qa-briefs.html — internal index of all growth brief previews."""

from __future__ import annotations

import html
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTREACH = Path("/Users/stephendiedrich/Desktop/upstory/_all_contacts_for_personalization.json")

_spec = importlib.util.spec_from_file_location(
    "gen_p1", Path(__file__).with_name("generate-p1-briefs.py")
)
_gen = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_gen)

_p2_spec = importlib.util.spec_from_file_location(
    "briefs_p2_p4", Path(__file__).with_name("briefs_p2_p4.py")
)
_p2 = importlib.util.module_from_spec(_p2_spec)
assert _p2_spec.loader is not None
_p2_spec.loader.exec_module(_p2)

_sheet_spec = importlib.util.spec_from_file_location(
    "briefs_sheet_wave1", Path(__file__).with_name("briefs_sheet_wave1.py")
)
_sheet = importlib.util.module_from_spec(_sheet_spec)
assert _sheet_spec.loader is not None
_sheet_spec.loader.exec_module(_sheet)

EXCLUDE_SLUGS = _p2.EXCLUDE_SLUGS

# Slug overrides for outreach `co` names
CO_SLUG = {
    "Stake": "stake",
    "Abby Care": "abby-care",
    "AKKO": "akko",
    "Cloaked": "cloaked",
    "Eternal": "eternal",
    "Dorsia": "dorsia",
    "Caramel": "caramel",
    "Whisker Labs": "whisker-labs",
    "Vinovest (Acquired by StartEngine)": "vinovest",
    "Goldin": "goldin",
    "Poparide": "poparide",
    "Portola": "portola",
    "LegitApp Authentication": "legit-app",
    "WinIt": "winit",
    "Lolli": "lolli",
    "Getmyboat": "getmyboat",
    "Swifto": "swifto",
    "The Arena": "the-arena",
    "Citizen": "citizen-health/brief",
    "CatchCorner by Sports Illustrated": "catchcorner",
    "Diem App": "diem-app",
    "Gride Technology": "gride-technology",
    "HOMMA Group, Inc": "homma",
    "Lasting (acquired by Talkspace)": "lasting",
    "Marble (Acquired by The Zebra)": "marble",
    "OtoZen: Driving and Family Safety App": "otozen",
    "Super Unlimited Inc.": "super-unlimited",
    "TiiCKER": "tiicker",
}

MANUAL = [
    {
        "slug": "stake",
        "name": "Stake",
        "about": "Renter cash-back product scaling after UMoveFree integration and new financing.",
        "opportunity": "Prove the Cash Back payoff in the first session after handoff so more UMoveFree renters schedule first rent payment.",
    },
    {
        "slug": "abby-care",
        "name": "Abby Care",
        "about": "Home care platform helping families hire Medicaid-paid caregivers across expanding states.",
        "opportunity": "Unify training and Medicaid paperwork into one guided path to cut days-to-certification in each new state.",
    },
    {
        "slug": "citizen-health/brief",
        "name": "Citizen Health",
        "about": "Consumer health app for records, visit summaries, and care navigation.",
        "opportunity": "Earn public App Store proof right after in-product wins instead of leading with email signup alone.",
    },
]

ABOUT_OVERRIDE = {
    "stake": "Renter cash-back product scaling after UMoveFree integration and new financing.",
    "abby-care": "Home care platform helping families hire Medicaid-paid caregivers across expanding states.",
    "citizen-health/brief": "Consumer health app for records, visit summaries, and care navigation.",
    "akko": "Device protection sold through partner embeds and checkout, now integrating Upsie.",
    "caramel": "Vehicle marketplace checkout and escrow for private-party sales, including eBay listings.",
    "cloaked": "Identity privacy app moving from consumer aliases into enterprise workspace sales.",
    "dorsia": "Paid membership club for hard-to-book restaurants and global dining experiences.",
    "eternal": "Performance health program for lifelong athletes combining labs, coaching, and visits.",
    "getmyboat": "Boat rental marketplace merging two large inventories into one booking experience.",
    "goldin": "Collectibles auction house integrating tightly with eBay for high-value lots.",
    "legit-app": "Authentication service for luxury goods sold on marketplaces and social commerce.",
    "lolli": "Bitcoin and cash-back rewards on everyday spend, now via card-linked offers with Kard.",
    "poparide": "Long-distance rideshare community with a million members across Canada.",
    "portola": "Voice-first AI companion Tolan focused on character, memory, and conversation.",
    "swifto": "On-demand dog walking and pet care, expanding through acquisition in new markets.",
    "the-arena": "SocialFi app on Avalanche with launchpad and DEX, integrating Arcade2Earn gaming rewards.",
    "vinovest": "Fine wine and whiskey investing platform, recently acquired by StartEngine.",
    "whisker-labs": "Ting home electrical fire sensor distributed through insurer partnerships.",
    "winit": "Legal-tech tools that guide consumers through disputes, tickets, and claims.",
}


def first_sentence(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    for sep in (". ", "? ", "! "):
        if sep in text:
            return text.split(sep, 1)[0] + sep.strip()
    return text if text.endswith(".") else text + "."


def load_about_from_json() -> dict[str, str]:
    out: dict[str, str] = {}
    if not OUTREACH.exists():
        return out
    data = json.loads(OUTREACH.read_text(encoding="utf-8"))
    for row in data:
        if str(row.get("priority")) != "1":
            continue
        co = (row.get("co") or "").strip()
        slug = CO_SLUG.get(co)
        if not slug or slug in out:
            continue
        news = row.get("news") or ""
        out[slug] = first_sentence(news)
    return out


def entries() -> list[dict]:
    about_json = load_about_from_json()
    by_slug: dict[str, dict] = {}

    for item in MANUAL:
        by_slug[item["slug"]] = item

    def add_brief(b: dict, about_key: str | None = None) -> None:
        slug = b["slug"]
        if slug in EXCLUDE_SLUGS:
            return
        opp_title = b["opps"][0][1] if b.get("opps") else ""
        opportunity = opp_title or b["headline"]
        if opportunity and opportunity[0].islower():
            opportunity = opportunity[0].upper() + opportunity[1:]
        if opportunity and not opportunity.endswith("."):
            opportunity += "."
        about = b.get("about") or ABOUT_OVERRIDE.get(slug) or about_json.get(slug or "")
        if not about:
            about = first_sentence(b.get("insight", ""))
        by_slug[slug] = {
            "slug": slug,
            "name": b["name"],
            "about": about,
            "opportunity": opportunity,
        }

    for b in _gen.BRIEFS:
        add_brief(b)
    for b in _p2.BRIEFS_P2_P4:
        add_brief(b)
    for b in _sheet.BRIEFS_SHEET_WAVE1:
        add_brief(b)

    return sorted(by_slug.values(), key=lambda x: x["name"].lower())


def render_card(e: dict) -> str:
    href = f"/{e['slug']}"
    return f"""      <article class="qa-card">
        <h2 class="qa-name">{html.escape(e['name'])}</h2>
        <p class="qa-about">{html.escape(e['about'])}</p>
        <p class="qa-opp"><span class="qa-label">Opportunity</span> {html.escape(e['opportunity'])}</p>
        <p class="qa-link"><a href="{html.escape(href)}">View brief</a></p>
      </article>"""


def render_page(items: list[dict]) -> str:
    cards = "\n".join(render_card(e) for e in items)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Growth briefs — Upstory QA</title>
  <link rel="icon" href="/shared/favicon-light.svg" type="image/svg+xml" media="(prefers-color-scheme: light)">
  <link rel="icon" href="/shared/favicon-dark.svg" type="image/svg+xml" media="(prefers-color-scheme: dark)">
  <link rel="stylesheet" href="/shared/brief.css">
  <link rel="stylesheet" href="/shared/qa-briefs.css">
</head>
<body class="brief qa-index">
  <main class="page qa-page">
    <header class="qa-header">
      <img class="qa-logo" src="/shared/upstory-logo.png" alt="Upstory" width="140" height="40" />
      <h1 class="qa-title">Growth brief previews</h1>
      <p class="qa-meta">For internal review only</p>
    </header>
    <section class="qa-list">
{cards}
    </section>
    <footer class="footer">
      <span>Internal only — not for client distribution as a list page.</span>
      <span class="footer-meta">&copy; Upstory 2026</span>
    </footer>
  </main>
</body>
</html>
"""


def main():
    items = entries()
    out = ROOT / "qa-briefs.html"
    out.write_text(render_page(items), encoding="utf-8")
    print(f"wrote {out} ({len(items)} briefs)")


if __name__ == "__main__":
    main()
