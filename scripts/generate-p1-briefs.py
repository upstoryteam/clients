#!/usr/bin/env python3
"""Generate Priority 1 growth brief HTML pages from outreach JSON."""

from __future__ import annotations

import json
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGOS = ROOT / "shared" / "logos"
OUTREACH = Path("/Users/stephendiedrich/Desktop/upstory/_all_contacts_for_personalization.json")

VB_W, STAGE_H, PAD_X, CX = 200, 48, 10, 100
CURVE_INSET = 0.94


def funnel_svg(rows: list[tuple[str, int, bool]]) -> tuple[str, str]:
    max_hw = CX - PAD_X
    n = len(rows)
    vb_h = n * STAGE_H
    paths = []
    dividers = []
    for i, (_, pct, key) in enumerate(rows):
        y0, y1 = i * STAGE_H, (i + 1) * STAGE_H
        w0 = max_hw * (pct / 100)
        w1 = max_hw * (rows[i + 1][1] / 100) if i < n - 1 else w0 * 0.92
        mid_y = (y0 + y1) / 2
        w_mid = ((w0 + w1) / 2) * CURVE_INSET
        cls = "vis-funnel-fill is-key" if key else "vis-funnel-fill"
        d = (
            f"M {CX - w0:.1f} {y0} L {CX + w0:.1f} {y0} "
            f"Q {CX + w_mid:.1f} {mid_y} {CX + w1:.1f} {y1} "
            f"L {CX - w1:.1f} {y1} Q {CX - w_mid:.1f} {mid_y} {CX - w0:.1f} {y0} Z"
        )
        paths.append(f'<path class="{cls}" d="{d}"/>')
        if i < n - 1:
            hw = max_hw * (rows[i + 1][1] / 100)
            y = (i + 1) * STAGE_H
            dividers.append(
                f'<line class="vis-funnel-divider" x1="{CX - hw:.1f}" y1="{y}" x2="{CX + hw:.1f}" y2="{y}"/>'
            )
    labels = "".join(
        f'<div class="vis-funnel-meta{" is-key" if k else ""}">{lab}</div>'
        for lab, _, k in rows
    )
    pcts = "".join(
        f'<div class="vis-funnel-meta{" is-key" if k else ""}">{p}</div>'
        for _, p, k in rows
    )
    inner = "\n                ".join(paths + dividers)
    block = f"""          <div class="vis-funnel">
            <div class="vis-funnel-layout" style="--funnel-stage-h: {STAGE_H}px">
              <div class="vis-funnel-aside vis-funnel-labels">{labels}</div>
              <svg class="vis-funnel-svg" viewBox="0 0 {VB_W} {vb_h}" role="img" aria-label="Conversion funnel">
                {inner}
              </svg>
              <div class="vis-funnel-aside vis-funnel-pcts">{pcts}</div>
            </div>
          </div>
          <p style="margin:14px 0 0;font-family:var(--sans);font-size:11px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:var(--ink-3)">Illustrative. Where we would look first.</p>"""
    return block, ""


def journey_svg(steps: list[tuple[str, bool]]) -> str:
    parts = []
    for i, (label, key) in enumerate(steps):
        if i:
            parts.append('<span class="arrow">→</span>')
        cls = "step is-key" if key else "step"
        parts.append(f'<span class="{cls}">{label}</span>')
    inner = "\n            ".join(parts)
    return f"""          <div class="vis-journey">
            {inner}
          </div>"""


INSIGHT_ICON = """        <svg class="insight-icon" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 1 7 7c0 2.5-1.5 4.5-3.5 5.5V17H8.5v-2.5C6.5 13.5 5 11.5 5 9a7 7 0 0 1 7-7z"/>
        </svg>"""

CLOSER = """    <section class="closer">
      <img class="logo" src="/shared/upstory-logo.png" alt="Upstory" />
      <div class="closer-copy">
        <p><strong>Upstory is a product design firm</strong>. We specialize in growth and retention for consumer products that ask for sensitive information. Our focus is in health, fintech, and identity, with client work featuring LifeMD, Firefox, and Wander.</p>
      </div>
      <div class="sig">
        <img src="/shared/rick-russie.avif" alt="Rick Russie" />
        <div>
          <p class="sig-name">Rick Russie</p>
          <p class="sig-title">Founder and Design Lead, Upstory</p>
        </div>
      </div>
      <a class="closer-link" href="https://www.upstory.co">upstory.co <span style="font-size:13px">↗</span></a>
    </section>

    <footer class="footer">
      <span>We design the moments where consumer products earn users.</span>
      <span class="footer-meta">&copy; Upstory 2026</span>
    </footer>"""


BRIEFS: list[dict] = [
    {
        "slug": "akko",
        "name": "AKKO",
        "logo_ext": "svg",
        "headline": "We believe we can help AKKO cut partner time-to-first-sale by 30 days after the Upsie integration.",
        "insight": "Channel Partners put partner launch speed on the table. The Upsie integration only pays off when embed and checkout feel turnkey. We would focus on the partner-facing activation path before scaling outbound.",
        "opps": [
            ("01", "Show coverage value before the partner commits engineering", "Partners decide on a demo, not a deck. We would lead with a live checkout snippet and claims story, then open the integration checklist.", "journey", [("Partner interest", False), ("Live embed demo", True), ("First policy sold", False)]),
            ("02", "Treat first end-customer purchase as the proof metric", "Partner revenue shows up when a real customer completes protection signup. We would map every step from partner launch to first paid policy.", "funnel", [("Partner live", 100, False), ("First quote", 55, False), ("Policy purchased", 32, True)]),
            ("03", "Instrument each partner cohort separately", "Upsie and legacy partners will behave differently. We would tag cohorts by launch week so you can read lift without blending channels.", None, None),
        ],
        "measures": [
            "Partner integrations reaching first sale within 45 days of go-live.",
            "Attach rate on partner checkout within 30 days of launch.",
            "Upsie cohort conversion versus pre-integration baseline by partner type.",
        ],
    },
    {
        "slug": "cloaked",
        "name": "Cloaked",
        "logo_ext": "svg",
        "headline": "We believe we can help Cloaked lift enterprise trial-to-paid conversion by 25% in the next two quarters.",
        "insight": "The Series B push is into enterprise, but the product still wins on consumer-grade polish. Identity creation is the wedge. If professional onboarding feels as fast as the consumer app, expansion keeps pace with the raise.",
        "opps": [
            ("01", "Lead with a usable alias before the enterprise contract ask", "Buyers need to feel Cloaked working in minute one. We would open with a generated identity and one protected action, then invite workspace setup.", "journey", [("Trial start", False), ("First alias live", True), ("Workspace invite", False)]),
            ("02", "Design the seat expansion moment around team invites", "Enterprise growth lives in invite acceptance, not top-of-funnel ads. We would map admin setup through first teammate protected.", "funnel", [("Admin signup", 100, False), ("Policy configured", 68, False), ("Teammate active", 41, True)]),
            ("03", "Keep consumer and enterprise flows visually aligned", "Two divergent UIs will slow sales engineering. We would reuse the same trust components across both surfaces.", None, None),
        ],
        "measures": [
            "Trial accounts creating a first alias within 24 hours.",
            "Second seat activated within 14 days of admin signup.",
            "Enterprise pilots reaching paid conversion within 60 days.",
        ],
    },
    {
        "slug": "eternal",
        "name": "Eternal",
        "logo_ext": "svg",
        "headline": "We believe we can help Eternal lift athlete enrollment completion to 65% within 60 days of first visit.",
        "insight": "The clinical story is strong on the inside. Public enrollment still asks athletes to commit before they have felt the performance model. The first session outcome should arrive before the long intake form.",
        "opps": [
            ("01", "Offer a performance snapshot before full intake", "Athletes arrive skeptical of another health portal. We would show a sample benchmark, then ask for labs and history.", "journey", [("Landing visit", False), ("Performance preview", True), ("Enrollment complete", False)]),
            ("02", "Shorten the path from interest to first scheduled visit", "Enrollment drop-off clusters between form submit and calendar hold. We would surface scheduling while motivation is high.", "funnel", [("Started enrollment", 100, False), ("Intake complete", 58, False), ("First visit booked", 38, True)]),
            ("03", "Make the first visit deliverable visible upfront", "Athletes need a tangible takeaway. We would preview the post-visit summary they receive after visit one.", None, None),
        ],
        "measures": [
            "Visitors starting enrollment who finish intake within seven days.",
            "First visit booked within 48 hours of intake complete.",
            "Seven-day return rate after first visit.",
        ],
    },
    {
        "slug": "dorsia",
        "name": "Dorsia",
        "logo_ext": "svg",
        "headline": "We believe we can help Dorsia convert 20% more membership applicants to paid members within 90 days.",
        "insight": "Membership is a pay-before-you-experience proposition. Culture Calendar and wallet features add complexity at the wrong moment if the first reservation still feels uncertain. We would tighten apply-to-first-booking.",
        "opps": [
            ("01", "Show a real reservation outcome before the membership fee", "Applicants need proof the network is alive. We would surface one credible experience preview, then ask for payment.", "journey", [("Application", False), ("Experience preview", True), ("Membership paid", False)]),
            ("02", "Map drop-off from approved member to first booking", "Paid members who never book churn quietly. We would instrument the first reservation funnel end to end.", "funnel", [("Member approved", 100, False), ("Wallet connected", 72, False), ("First reservation", 44, True)]),
            ("03", "Keep crypto and card paths feeling like one product", "Split payment flows read as experiments. We would unify confirmation and receipts across methods.", None, None),
        ],
        "measures": [
            "Applicants reaching paid membership within 14 days of approval.",
            "New members completing a first reservation within 21 days.",
            "Second booking within 60 days of the first.",
        ],
    },
    {
        "slug": "caramel",
        "name": "Caramel",
        "logo_ext": "png",
        "headline": "We believe we can help Caramel lift eBay checkout completion by 15% on private-party listings.",
        "insight": "Checkout inside eBay is not your UI, but it is your conversion problem. Buyers did not choose Caramel. They need trust signals and clarity before they fund a high-ticket vehicle or collectible purchase.",
        "opps": [
            ("01", "Front-load buyer protection before payment details", "Marketplace buyers fear scams. We would lead with escrow and title clarity, then collect payment.", "journey", [("Listing click", False), ("Protection explained", True), ("Payment submitted", False)]),
            ("02", "Reduce steps from checkout start to funds committed", "Every extra screen costs GMV on mobile. We would map abandonment between start and confirm.", "funnel", [("Checkout started", 100, False), ("Buyer verified", 71, False), ("Purchase complete", 48, True)]),
            ("03", "Align seller and buyer status in one timeline", "Split statuses create support load. We would show both parties the same milestone view.", None, None),
        ],
        "measures": [
            "Checkout starts completing within five minutes on mobile.",
            "Buyer verification pass rate on first attempt.",
            "eBay cohort completion versus standalone Caramel baseline.",
        ],
    },
    {
        "slug": "brave",
        "name": "Brave",
        "logo_ext": "svg",
        "headline": "We believe we can help Brave move 30% more developers from API key signup to first paid query within 30 days.",
        "insight": "Brave Search as a platform is a different promise than the browser. Developers commit billing before they have seen index quality on their own queries. The first successful API call should land before the card form.",
        "opps": [
            ("01", "Let developers run a live query before billing setup", "Docs alone do not prove the index. We would ship a sandbox key with visible results, then ask for billing.", "journey", [("Docs visit", False), ("First query works", True), ("Billing added", False)]),
            ("02", "Funnel API adoption from key created to production traffic", "Keys without traffic do not expand revenue. We would track activation through sustained query volume.", "funnel", [("API key issued", 100, False), ("First production query", 54, False), ("Paid tier active", 36, True)]),
            ("03", "Tie Brave Rewards opt-in to the same trust pattern", "Browser users face a parallel commitment moment. We would reuse proof-before-ask components where it fits.", None, None),
        ],
        "measures": [
            "New keys running a successful query within one hour.",
            "Developers crossing 1,000 queries within 14 days of signup.",
            "Paid conversion among keys with sustained weekly traffic.",
        ],
    },
    {
        "slug": "whisker-labs",
        "name": "Whisker Labs",
        "logo_ext": "svg",
        "headline": "We believe we can help Whisker Labs reach 80% Ting device activation within 14 days of ship.",
        "insight": "Insurer partnerships scale when homeowners actually install Ting. The hardware is only valuable after setup finishes and alerts feel trustworthy. That onboarding window is the product moment partners measure.",
        "opps": [
            ("01", "Make install success visible before the insurer report", "Homeowners need confidence the sensor works. We would confirm live readings in app before asking them to ignore the box.", "journey", [("Kit arrives", False), ("Sensor online", True), ("Alert test passed", False)]),
            ("02", "Map insurer-led enrollment through first active day", "Ship-to-silent devices hurt renewal. We would track ship, install, and first alert sent.", "funnel", [("Device shipped", 100, False), ("App paired", 67, False), ("Active monitoring", 52, True)]),
            ("03", "Give partners a cohort dashboard they can show", "Insurers sell outcomes. We would package activation rate per campaign for their account teams.", None, None),
        ],
        "measures": [
            "Devices reporting data within 48 hours of delivery.",
            "First homeowner alert successfully delivered within seven days.",
            "Partner cohorts beating prior activation baseline by launch month.",
        ],
    },
    {
        "slug": "vinovest",
        "name": "Vinovest",
        "logo_ext": "png",
        "headline": "We believe we can help Vinovest fund 25% more new accounts within 45 days on StartEngine.",
        "insight": "The StartEngine network brings volume, but wine investing still asks for money before portfolio proof. Funding and first allocation are the trust handoff inside a bigger audience.",
        "opps": [
            ("01", "Show a sample portfolio outcome before the minimum transfer", "New investors need to see how capital maps to bottles. We would preview holdings, then ask for funding.", "journey", [("Account opened", False), ("Portfolio preview", True), ("First transfer", False)]),
            ("02", "Tighten KYC-to-first-allocation completion", "Drop-off between verification and first buy is expensive on paid traffic. We would shorten that bridge.", "funnel", [("Signup", 100, False), ("KYC cleared", 63, False), ("First allocation", 39, True)]),
            ("03", "Onboard StartEngine users with a distinct cohort view", "Blended metrics will hide channel quality. We would tag users by acquisition source from day one.", None, None),
        ],
        "measures": [
            "Verified accounts funding within seven days of KYC approval.",
            "Median time from signup to first allocation under 72 hours.",
            "StartEngine cohort funding rate versus organic baseline.",
        ],
    },
    {
        "slug": "goldin",
        "name": "Goldin",
        "logo_ext": "svg",
        "headline": "We believe we can help Goldin lift winning-bid payment completion to 92% on high-value lots.",
        "insight": "eBay scale raises the stakes on checkout trust. Bidders commit large sums after adrenaline fades. Consignors need the same clarity on payouts. Both sides need proof before the wire.",
        "opps": [
            ("01", "Confirm buyer funds and fees before the hammer drop", "Last-second surprises kill completion. We would show all-in cost during bidding, not after win.", "journey", [("Bid placed", False), ("All-in price shown", True), ("Payment cleared", False)]),
            ("02", "Map win-to-paid for bidders and consignors separately", "Two-sided marketplaces fail in the handoff. We would funnel each side with its own proof moment.", "funnel", [("Auction won", 100, False), ("Payment started", 78, False), ("Funds settled", 71, True)]),
            ("03", "Reuse eBay trust cues without duplicating flows", "Buyers know eBay. We would align status language with what they already expect.", None, None),
        ],
        "measures": [
            "Winning bids completing payment within 24 hours.",
            "Consignor payout initiated within 48 hours of settlement.",
            "Support tickets per 100 closed lots trending down quarter over quarter.",
        ],
    },
    {
        "slug": "poparide",
        "name": "Poparide",
        "logo_ext": "png",
        "headline": "We believe we can help Poparide book a first trip for 40% of new members within 21 days.",
        "insight": "One million members is proof the model works. The next million will expose verification and first-trip friction. Carpooling is a real-world commitment. Riders need trust before they sit in a stranger's car.",
        "opps": [
            ("01", "Earn trust before the first message to a driver", "Profiles matter more than search filters. We would verify identity and show trip history cues up front.", "journey", [("Profile created", False), ("ID verified", True), ("First message", False)]),
            ("02", "Funnel new members to a booked trip", "Many members never leave browse. We would map signup through confirmed seat.", "funnel", [("Member joined", 100, False), ("Search to contact", 61, False), ("Trip booked", 37, True)]),
            ("03", "Localize onboarding for each new route launch", "Expansion repeats enrollment problems. We would template the first-trip path per region.", None, None),
        ],
        "measures": [
            "New members verifying identity within 48 hours.",
            "First trip booked within 21 days of signup.",
            "Second trip within 60 days of the first completed ride.",
        ],
    },
]


def render_opp(num: str, title: str, body: str, artifact: str | None, data) -> str:
    visual = ""
    if artifact == "journey":
        visual = f"""        <div class="visual is-inline">
          {journey_svg(data)}
        </div>"""
    elif artifact == "funnel":
        funnel, _ = funnel_svg(data)
        visual = f"""        <div class="visual">
          {funnel}
        </div>"""
    return f"""      <article class="solution">
        <div class="solution-head">
          <span class="solution-num">{num}</span>
          <h2 class="solution-title">{title}</h2>
        </div>
        <div class="solution-body">
          <p>{body}</p>
        </div>
{visual}
      </article>"""


def render_page(b: dict) -> str:
    ext = b["logo_ext"]
    logo = f"/shared/logos/{b['slug']}.{ext}"
    opps_html = "\n".join(
        render_opp(n, t, p, a, d) for n, t, p, a, d in b["opps"]
    )
    measures = "\n".join(
        f'      <li><span class="bullet">&middot;</span><span>{m}</span></li>' for m in b["measures"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Upstory for {b['name']}</title>
  <link rel="stylesheet" href="/shared/brief.css">
</head>
<body class="brief">
  <main class="page">
    <header class="brief-header">
      <div class="brief-header-brands">
        <img class="brief-header-upstory" src="/shared/upstory-logo.png" alt="Upstory" />
        <span class="brief-header-for">for</span>
        <img class="brief-header-logo" src="{logo}" alt="{b['name']}" />
      </div>
    </header>

    <h1 class="outcome">{b['headline']}</h1>

    <div class="insight-callout">
      <div class="insight-callout-head">
{INSIGHT_ICON}
        <p class="insight-eyebrow">Our read</p>
      </div>
      <p class="insight-body">{b['insight']} The opportunities below are where we would start.</p>
    </div>

    <div class="opportunities-intro">
      <h2 class="opportunities-heading">Opportunities</h2>
      <p class="opportunities-lead">Three places we would start in the product.</p>
    </div>

    <section class="solutions">
{opps_html}
    </section>

    <div class="section-intro">
      <h2 class="section-heading">Ways to measure success</h2>
      <p class="section-lead">A few ideas for leading indicators we could track with you.</p>
    </div>
    <ul class="measure-list">
{measures}
    </ul>

{CLOSER}
  </main>
</body>
</html>
"""


LOGO_URLS = {
    "akko": "https://cdn.prod.website-files.com/653ebce5eaad971b32d955f3/653ebce5eaad971b32d95895_Group%20(12).svg",
    "cloaked": "https://cdn.prod.website-files.com/63ec0f977f0357126ec38bcd/696691327b6ddbf53f5163a6_Cloaked-icon-logo.svg",
}


def download_logos():
    LOGOS.mkdir(parents=True, exist_ok=True)
    for slug, url in LOGO_URLS.items():
        dest = LOGOS / f"{slug}.svg"
        if not dest.exists():
            urllib.request.urlretrieve(url, dest)
            print("downloaded", dest)

    # Additional logos via curl in shell for sites that block urllib


def main():
    download_logos()
    for b in BRIEFS:
        slug_dir = ROOT / b["slug"]
        slug_dir.mkdir(parents=True, exist_ok=True)
        html = render_page(b)
        (slug_dir / "index.html").write_text(html, encoding="utf-8")
        meta = {
            "tone": "dark",
            "headerVariant": "plain",
            "source": "company marketing site",
        }
        (LOGOS / f"{b['slug']}.meta.json").write_text(
            json.dumps(meta, indent=2) + "\n", encoding="utf-8"
        )
        readme = f"""# {b['name']} growth brief

Priority 1 outreach preview. Live at `/ {b['slug']}/` after deploy.

Status: draft for internal audit.
"""
        (slug_dir / "README.md").write_text(readme, encoding="utf-8")
        print("wrote", slug_dir / "index.html")


if __name__ == "__main__":
    main()
