#!/usr/bin/env python3
"""Generate qa-briefs.html — internal index of all growth brief previews."""

from __future__ import annotations

import html
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from repo_paths import outreach_contacts_json

OUTREACH = outreach_contacts_json()

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

_wave2_spec = importlib.util.spec_from_file_location(
    "briefs_wave2", Path(__file__).with_name("briefs_wave2.py")
)
_wave2 = importlib.util.module_from_spec(_wave2_spec)
assert _wave2_spec.loader is not None
_wave2_spec.loader.exec_module(_wave2)

_w2_loader_spec = importlib.util.spec_from_file_location(
    "wave2_brief_loader", Path(__file__).with_name("wave2_brief_loader.py")
)
_w2_loader = importlib.util.module_from_spec(_w2_loader_spec)
assert _w2_loader_spec.loader is not None
_w2_loader_spec.loader.exec_module(_w2_loader)

EXCLUDE_SLUGS = _p2.EXCLUDE_SLUGS

# QA batch groupings (newest first on index page)
QA_BATCHES: list[dict] = [
    {
        "id": "wave2",
        "label": "Wave 2",
        "date": "June 2026",
        "note": "Full Wave 2 Fit Pass batch (P1–P4)",
    },
    {
        "id": "sheet-wave1",
        "label": "ICP Wave 1",
        "date": "Prior batch",
        "note": "Sheet-sourced companies not in outreach JSON",
    },
    {
        "id": "outreach-p1",
        "label": "Outreach P1",
        "date": "Prior batch",
        "note": "Priority 1 from outreach personalization JSON",
    },
    {
        "id": "outreach-p2-p4",
        "label": "Outreach P2–P4",
        "date": "Prior batch",
        "note": "Lower-priority outreach companies",
    },
    {
        "id": "handcrafted",
        "label": "Hand-crafted",
        "date": "Original",
        "note": "Stake, Abby Care, Citizen Health",
    },
]

BATCH_ORDER = [b["id"] for b in QA_BATCHES]

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
    "Citizen": "citizen-health",
    "Citizen Health": "citizen-health",
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
        "slug": "citizen-health",
        "name": "Citizen Health",
        "about": "Consumer health app for records, visit summaries, and care navigation.",
        "opportunity": "Earn public App Store proof right after in-product wins instead of leading with email signup alone.",
    },
]

ABOUT_OVERRIDE = {
    "stake": "Renter cash-back product scaling after UMoveFree integration and new financing.",
    "abby-care": "Home care platform helping families hire Medicaid-paid caregivers across expanding states.",
    "citizen-health": "Consumer health app for records, visit summaries, and care navigation.",
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


def entries_grouped() -> list[dict]:
    about_json = load_about_from_json()
    by_slug: dict[str, dict] = {}
    batch_by_slug: dict[str, str] = {}

    def add_brief(b: dict, batch_id: str) -> None:
        slug = b["slug"]
        if slug in EXCLUDE_SLUGS:
            return
        opp_title = b["opps"][0][1] if b.get("opps") else ""
        opportunity = opp_title or b["headline"]
        if opportunity and opportunity[0].islower():
            opportunity = opportunity[0].upper() + opportunity[1:]
        if opportunity and not opportunity.endswith("."):
            opportunity += "."
        about = b.get("qa_about") or b.get("about") or ABOUT_OVERRIDE.get(slug) or about_json.get(slug or "")
        if not about:
            about = first_sentence(b.get("insight", ""))
        by_slug[slug] = {
            "slug": slug,
            "name": b["name"],
            "about": about,
            "opportunity": opportunity,
            "batch": batch_id,
        }
        batch_by_slug[slug] = batch_id

    for item in MANUAL:
        by_slug[item["slug"]] = {
            **item,
            "batch": "handcrafted",
        }
        batch_by_slug[item["slug"]] = "handcrafted"

    for b in _gen.BRIEFS:
        add_brief(b, "outreach-p1")
    for b in _p2.BRIEFS_P2_P4:
        add_brief(b, "outreach-p2-p4")
    for b in _sheet.BRIEFS_SHEET_WAVE1:
        add_brief(b, "sheet-wave1")
    for b in _w2_loader.get_wave2_briefs():
        add_brief(b, "wave2")

    ship_status: dict[str, str] = {}
    try:
        _ship_spec = importlib.util.spec_from_file_location(
            "wave2_ship", Path(__file__).with_name("wave2_ship.py")
        )
        _ship = importlib.util.module_from_spec(_ship_spec)
        assert _ship_spec.loader is not None
        _ship_spec.loader.exec_module(_ship)
        ship_status = {r["slug"]: r["ship_status"] for r in _ship.build_status_rows()}
    except Exception:
        pass

    for slug, item in by_slug.items():
        if batch_by_slug.get(slug) == "wave2" and slug in ship_status:
            item["ship_status"] = ship_status[slug]

    grouped: dict[str, list[dict]] = {bid: [] for bid in BATCH_ORDER}
    for slug in sorted(by_slug.keys(), key=lambda s: by_slug[s]["name"].lower()):
        item = by_slug[slug]
        batch_id = item.get("batch") or batch_by_slug.get(slug, "outreach-p1")
        grouped.setdefault(batch_id, []).append(item)

    out: list[dict] = []
    meta = {b["id"]: b for b in QA_BATCHES}
    for batch_id in BATCH_ORDER:
        items = grouped.get(batch_id, [])
        if not items:
            continue
        info = meta[batch_id]
        out.append(
            {
                "id": batch_id,
                "label": info["label"],
                "date": info["date"],
                "note": info["note"],
                "items": items,
            }
        )
    return out


def entries() -> list[dict]:
    flat: list[dict] = []
    for section in entries_grouped():
        flat.extend(section["items"])
    return flat


def render_card(e: dict) -> str:
    href = f"/{e['slug']}"
    name = html.escape(e["name"])
    about = html.escape(e["about"])
    opp = html.escape(e["opportunity"])
    batch = html.escape(e.get("batch", ""))
    batch_attr = f' data-batch="{batch}"' if batch else ""
    ship = e.get("ship_status", "")
    ship_attr = f' data-ship="{html.escape(ship)}"' if ship else ""
    ship_badge = ""
    if ship == "skip":
        ship_badge = ' <span class="qa-ship-flag is-skip">Skip</span>'
    elif ship == "ship":
        ship_badge = ' <span class="qa-ship-flag is-ship">Ship</span>'
    return f"""      <article class="qa-card"{batch_attr}{ship_attr}>
        <header class="qa-card-head">
          <h2 class="qa-name"><a href="{html.escape(href)}">{name}</a>{ship_badge}</h2>
        </header>
        <div class="qa-card-body">
          <div class="qa-detail">
            <span class="qa-label">About</span>
            <p class="qa-about">{about}</p>
          </div>
          <div class="qa-detail">
            <span class="qa-label">Opportunity</span>
            <p class="qa-opp">{opp}</p>
          </div>
        </div>
        <footer class="qa-card-foot">
          <a class="qa-cta" href="{html.escape(href)}">View brief →</a>
        </footer>
      </article>"""


def render_batch_nav(sections: list[dict]) -> str:
    links = ['      <a class="qa-nav-link is-active" href="#">All batches</a>']
    for s in sections:
        sid = html.escape(s["id"])
        count = len(s["items"])
        label = html.escape(s["label"])
        links.append(
            f'      <a class="qa-nav-link" href="#{sid}">{label} ({count})</a>'
        )
    return "\n".join(links)


def render_batch_section(section: dict) -> str:
    sid = html.escape(section["id"])
    label = html.escape(section["label"])
    date = html.escape(section["date"])
    note = html.escape(section["note"])
    count = len(section["items"])
    cards = "\n".join(render_card(e) for e in section["items"])
    is_new = section["id"] == "wave2"
    ship_counts = {}
    for item in section["items"]:
        s = item.get("ship_status", "")
        if s:
            ship_counts[s] = ship_counts.get(s, 0) + 1
    ship_note = ""
    if ship_counts:
        parts = [f"{ship_counts.get('ship', 0)} ship", f"{ship_counts.get('skip', 0)} skip"]
        ship_note = " · " + " · ".join(parts)
    flag = '\n        <span class="qa-batch-flag">Ready to ship</span>' if is_new else ""
    return f"""    <section class="qa-batch" id="{sid}">
      <header class="qa-batch-head">
        <div class="qa-batch-titles">
          <h2 class="qa-batch-title">{label}{flag}</h2>
          <p class="qa-batch-meta">{date} · {count} briefs · {note}{ship_note}</p>
        </div>
      </header>
      <div class="qa-list">
{cards}
      </div>
    </section>"""


def render_page(sections: list[dict], *, title: str, subtitle: str) -> str:
    nav = render_batch_nav(sections)
    body = "\n".join(render_batch_section(s) for s in sections)
    total = sum(len(s["items"]) for s in sections)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>{html.escape(title)}</title>
  <link rel="icon" href="/shared/favicon-light.svg" type="image/svg+xml" media="(prefers-color-scheme: light)">
  <link rel="icon" href="/shared/favicon-dark.svg" type="image/svg+xml" media="(prefers-color-scheme: dark)">
  <link rel="stylesheet" href="/shared/brief.css">
  <link rel="stylesheet" href="/shared/qa-briefs.css">
</head>
<body class="brief qa-index">
  <main class="page qa-page">
    <header class="qa-header">
      <img class="qa-logo" src="/shared/upstory-logo.png" alt="Upstory" width="140" height="40" />
      <h1 class="qa-title">{html.escape(title)}</h1>
      <p class="qa-meta">{html.escape(subtitle)} · {total} briefs</p>
      <nav class="qa-nav" aria-label="Brief batches">
{nav}
      </nav>
    </header>
{body}
    <footer class="footer">
      <span>Internal only — not for client distribution as a list page.</span>
      <span class="footer-meta">&copy; Upstory 2026</span>
    </footer>
  </main>
</body>
</html>
"""


def main():
    sections = entries_grouped()
    total = sum(len(s["items"]) for s in sections)

    all_out = ROOT / "qa-briefs.html"
    all_out.write_text(
        render_page(
            sections,
            title="Growth brief previews",
            subtitle="For internal review only",
        ),
        encoding="utf-8",
    )
    print(f"wrote {all_out} ({total} briefs, {len(sections)} batches)")

    wave2 = [s for s in sections if s["id"] == "wave2"]
    if wave2:
        w2_out = ROOT / "qa-briefs-wave2.html"
        w2_out.write_text(
            render_page(
                wave2,
                title="Wave 2 — QA",
                subtitle="June 2026 full Wave 2 batch",
            ),
            encoding="utf-8",
        )
        print(f"wrote {w2_out} ({len(wave2[0]['items'])} briefs)")


if __name__ == "__main__":
    main()
