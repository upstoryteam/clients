#!/usr/bin/env python3
"""Generate Priority 1 growth brief HTML pages from outreach JSON."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import urllib.request
from pathlib import Path

_soften_spec = importlib.util.spec_from_file_location(
    "soften_opportunities",
    Path(__file__).with_name("soften-opportunities.py"),
)
_soften_mod = importlib.util.module_from_spec(_soften_spec)
assert _soften_spec.loader is not None
_soften_spec.loader.exec_module(_soften_mod)
soften_body = _soften_mod.soften_body

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
          <p style="margin:14px 0 0;font-family:var(--sans);font-size:11px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:var(--ink-3)">Illustrative. Where we'd look first.</p>"""
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
        "headline": "We believe we can help AKKO shorten partner time-to-first policy sale after the Upsie integration.",
        "insight": "You are scaling partner distribution after Upsie, and partners only win when embed and checkout feel turnkey. The break is the path from signed partner to first policy sold.",
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
        "headline": "We believe we can help Cloaked lift enterprise trial-to-paid conversion by 25%.",
        "insight": "You are pushing into enterprise while the product still wins on consumer polish. People need to feel a live identity in the first minute, the same way they do on the consumer app.",
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
        "headline": "We believe we can help Eternal lift athlete enrollment completion to 65%.",
        "insight": "Your clinical model is strong. On the public site, athletes are still asked to commit before they have felt what performance care looks like from you. The long intake form comes before the first win.",
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
        "headline": "We believe we can help Dorsia convert 20% more membership applicants to paid members.",
        "insight": "Members pay before they have experienced the network. If the first reservation still feels uncertain, Culture Calendar and wallet work do not get a chance to matter. The break is apply through first booking.",
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
        "insight": "Checkout inside eBay is not your UI, but it is your conversion problem. Buyers did not choose Caramel. They need trust and clarity before they fund a high-ticket purchase.",
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
        "headline": "We believe we can help Brave move 30% more developers from API key signup to first paid query.",
        "insight": "Brave Search is a different product than the browser. Developers are being asked for billing before they have run a query that proves the index on their use case.",
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
        "headline": "We believe we can help Whisker Labs lift Ting device activation to 80% after devices ship.",
        "insight": "Ting only matters once it is installed and alerting. Your insurer partners are measured on activation, and homeowners still drop off between the box arriving and a live sensor.",
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
        "headline": "We believe we can help Vinovest fund 25% more new accounts on StartEngine.",
        "insight": "The StartEngine audience is bigger, but the same moment still decides trust: money moves only after someone believes the portfolio is real.",
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
        "logo_ext": "png",
        "headline": "We believe we can help Goldin lift winning-bid payment completion to 92% on high-value lots.",
        "insight": "eBay scale raises the stakes on checkout trust. Bidders commit large sums after the adrenaline fades. Consignors need the same clarity on payouts before anyone wires funds.",
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
        "headline": "We believe we can help Poparide book a first trip for 40% of new members.",
        "insight": "You have proof the model works at a million members. The next wave will surface verification and first-trip friction. Riders need trust before they get in a stranger's car.",
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
    {
        "slug": "portola",
        "name": "Portola",
        "logo_ext": "svg",
        "headline": "We believe we can help Portola lift week-one return rate for new Tolan users by 20%.",
        "insight": "Tolan wins on voice and character, and you are investing in the first minutes of that relationship. If the opening conversation and visual presence feel polished before feature depth, retention has room to move.",
        "opps": [
            ("01", "Make the first voice exchange feel complete before signup depth", "New users decide whether Tolan is real in the first session. We'd start by giving them a satisfying voice moment, then invite account creation.", "journey", [("App open", False), ("Voice moment", True), ("Account created", False)]),
            ("02", "Map drop-off from first chat to day-three return", "Voice companions live on habit. We'd start by mapping where first-week users stall after the initial conversation.", "funnel", [("First session", 100, False), ("Day 2 return", 48, False), ("Day 7 active", 29, True)]),
            ("03", "Keep visual and voice quality consistent across surfaces", "Design hiring signals polish matters in public moments. We'd start by aligning the same trust cues on web, mobile, and character render.", None, None),
        ],
        "measures": [
            "First session ending with a completed voice exchange.",
            "Day-three return rate among users who finish session one.",
            "Week-one retention versus users who bounce after first chat.",
        ],
    },
    {
        "slug": "legit-app",
        "name": "LegitApp",
        "logo_ext": "svg",
        "headline": "We believe we can help LegitApp lift first-submit authentication pass rate to 95%.",
        "insight": "You are scaling trust with marketplaces and publishing accuracy numbers that set a high bar. Sellers and buyers still hesitate at the moment they hand over an item or a photo. That submit flow is where credibility becomes tangible.",
        "opps": [
            ("01", "Show what happens during authentication before the user commits", "Users fear a black box. We'd start by previewing steps, timing, and what pass or fail means for them.", "journey", [("Item photos", False), ("Auth preview", True), ("Result + cert", False)]),
            ("02", "Tighten the path from upload to certificate issued", "Marketplace deadlines are tight. We'd start by mapping friction between upload, payment, and result.", "funnel", [("Submit started", 100, False), ("Photos accepted", 74, False), ("Certificate issued", 58, True)]),
            ("03", "Align TikTok Shop and marketplace flows to one trust pattern", "Partners multiply surfaces. We'd start by reusing the same proof components everywhere you authenticate.", None, None),
        ],
        "measures": [
            "First-submit pass rate without reshoot requests.",
            "Median time from upload complete to certificate issued.",
            "Partner cohort completion versus direct traffic.",
        ],
    },
    {
        "slug": "winit",
        "name": "WinIt",
        "logo_ext": "svg",
        "headline": "We believe we can help WinIt lift dispute submission completion to 70%.",
        "insight": "You are expanding the legal product suite while users still face high-stress moments when they upload evidence or authorize payment. Those screens need to feel guided, not bureaucratic.",
        "opps": [
            ("01", "Walk users through evidence before they commit to filing", "Disputes spike anxiety. We'd start by showing what strong evidence looks like, then ask for uploads.", "journey", [("Dispute opened", False), ("Evidence guide", True), ("Submitted", False)]),
            ("02", "Reduce abandonment on multi-step dispute flows", "New product lines add steps. We'd start by mapping where users exit before submission.", "funnel", [("Flow started", 100, False), ("Evidence complete", 55, False), ("Dispute filed", 38, True)]),
            ("03", "Separate onboarding for each new product without reinventing trust", "Growth hires signal new surfaces. We'd start by reusing the same reassurance pattern across offerings.", None, None),
        ],
        "measures": [
            "Dispute flows started that reach submission.",
            "Evidence upload completed on first attempt.",
            "Support contacts per 100 submitted disputes.",
        ],
    },
    {
        "slug": "lolli",
        "name": "Lolli",
        "logo_ext": "svg",
        "headline": "We believe we can help Lolli lift card-linked reward activation to 45% of eligible users.",
        "insight": "The Kard partnership moves rewards into everyday card spend. Users still have to link a card and believe Bitcoin cashback is real before they swipe. That first-link experience is the new wedge.",
        "opps": [
            ("01", "Prove the reward before asking for card link", "Card linking is a big ask. We'd start by showing estimated earn on a typical purchase, then request link.", "journey", [("Offer seen", False), ("Reward preview", True), ("Card linked", False)]),
            ("02", "Map first swipe to first credited reward", "Activation is not link alone. We'd start by tracking link through first merchant reward posted.", "funnel", [("Card linked", 100, False), ("First purchase", 62, False), ("Reward credited", 41, True)]),
            ("03", "Keep browser and card rewards feeling like one brand", "Two surfaces can confuse. We'd start by aligning status and payout language across both.", None, None),
        ],
        "measures": [
            "Eligible users completing card link.",
            "First purchase with posted reward within 14 days of link.",
            "Repeat swipe rate among activated card users.",
        ],
    },
    {
        "slug": "getmyboat",
        "name": "Getmyboat",
        "logo_ext": "svg",
        "headline": "We believe we can help Getmyboat lift booking completion across integrated inventory by 18%.",
        "insight": "You are merging two large marketplaces into one discovery experience. Renters still need confidence on price, captain, and cancellation before they commit. The unified booking path is where that trust is won or lost.",
        "opps": [
            ("01", "Show total trip clarity before payment", "Boat rentals have hidden complexity. We'd start by surfacing fees, captain, and cancellation in one summary before checkout.", "journey", [("Listing view", False), ("Trip summary", True), ("Booking paid", False)]),
            ("02", "Map drop-off across the merged checkout", "Integration adds steps. We'd start by instrumenting search through confirmation on blended inventory.", "funnel", [("Checkout started", 100, False), ("Details confirmed", 68, False), ("Booking complete", 44, True)]),
            ("03", "Give owners and renters the same milestone language", "Two-sided confusion drives support. We'd start by aligning status updates on both apps.", None, None),
        ],
        "measures": [
            "Checkout starts reaching paid booking.",
            "Time from listing click to confirmed booking.",
            "Cancellation rate in the first 48 hours after book.",
        ],
    },
    {
        "slug": "swifto",
        "name": "Swifto",
        "logo_ext": "png",
        "headline": "We believe we can help Swifto lift Meet & Greet to first paid walk conversion to 55%.",
        "insight": "The North Carolina expansion follows an acquisition, and your model depends on a high-trust first meeting between owner, walker, and dog. The scheduling and Meet & Greet flow is where that trust is built.",
        "opps": [
            ("01", "Set expectations before the Meet & Greet is booked", "Owners worry about fit. We'd start by showing walker credentials and visit structure, then open scheduling.", "journey", [("Owner signup", False), ("Walker match preview", True), ("Meet & Greet booked", False)]),
            ("02", "Map Meet & Greet through first recurring walk", "The handoff from trial visit to paid schedule is the revenue moment. We'd start by mapping that funnel in the new market.", "funnel", [("Meet & Greet done", 100, False), ("First walk scheduled", 61, False), ("Recurring plan active", 38, True)]),
            ("03", "Localize the NC onboarding without cloning NYC blindly", "Markets differ. We'd start by testing copy and steps tuned to acquired customers in North Carolina.", None, None),
        ],
        "measures": [
            "Meet & Greet bookings per new owner signup.",
            "First paid walk within 14 days of Meet & Greet.",
            "Recurring plan adoption in new markets versus NYC baseline.",
        ],
    },
    {
        "slug": "the-arena",
        "name": "The Arena",
        "logo_ext": "svg",
        "headline": "We believe we can help The Arena lift Arcade mission activation to 35% of existing SocialFi users.",
        "insight": "The Arcade2Earn acquisition folds gaming rewards into a SocialFi stack that already moves real volume. Creators and players meet new Mission Pool flows before they understand the payoff. The integration window is when first-session clarity matters most.",
        "opps": [
            ("01", "Preview mission rewards before wallet connect depth", "Gamers bail when crypto steps stack early. We'd start by showing a sample mission payout, then ask for wallet link.", "journey", [("Feed visit", False), ("Mission preview", True), ("Wallet linked", False)]),
            ("02", "Map SocialFi users through first completed Arcade mission", "Acquisition adds a second activation curve. We'd start by instrumenting existing users from discovery through first mission complete.", "funnel", [("Mission started", 100, False), ("Onchain step done", 58, False), ("Reward claimed", 34, True)]),
            ("03", "Keep launchpad, DEX, and feed feeling like one Arena", "Three surfaces can read as three products. We'd start by aligning status and reward language across the stack.", None, None),
        ],
        "measures": [
            "Existing users starting an Arcade mission within seven days of announcement.",
            "First mission completion rate among starters.",
            "Repeat mission participation within 30 days of first claim.",
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
          <p>{soften_body(body)}</p>
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
  <link rel="icon" href="/shared/favicon-light.svg" type="image/svg+xml" media="(prefers-color-scheme: light)">
  <link rel="icon" href="/shared/favicon-dark.svg" type="image/svg+xml" media="(prefers-color-scheme: dark)">
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
        <p class="insight-eyebrow">What we see</p>
      </div>
      <p class="insight-body">{b['insight']}</p>
    </div>

    <div class="opportunities-intro">
      <h2 class="opportunities-heading">Opportunities to explore</h2>
      <p class="opportunities-lead">Three places we'd start in the product.</p>
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
    "portola": "https://cdn.prod.website-files.com/668499ce7cef6042b2f1a2bc/668499ce7cef6042b2f1a2c6_tolan.svg",
    "legit-app": "https://www.legitapp.com/logo-app-full.svg",
    "winit": "https://winitnow.com/assets/images/logos/winit-logo-blue.svg",
    "lolli": "https://lolli.com/images/logo.svg",
    "getmyboat": "https://www.getmyboat.com/static-images/gmb-logo-color.svg",
    "swifto": "https://swifto.com/sites/all/themes/custom/dogwalk/logo.png",
    "whisker-labs": "https://www.whiskerlabs.com/wp-content/uploads/2023/08/whisker-labs-logo.svg",
    "goldin": "https://d2tt46f3mh26nl.cloudfront.net/assets/images/logo/GoldinIcon.png",
    "eternal": "https://www.eternal.com/_astro/eternal_footer_logo.DyKavH3T.svg",
    "the-arena": "https://arena.social/icons/logo.svg",
}


def download_logos(only_slugs: set[str] | None = None):
    LOGOS.mkdir(parents=True, exist_ok=True)
    for slug, url in LOGO_URLS.items():
        if only_slugs is not None and slug not in only_slugs:
            continue
        ext = Path(url.split("?", 1)[0]).suffix.lower() or ".svg"
        dest = LOGOS / f"{slug}{ext}"
        if dest.exists():
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            dest.write_bytes(resp.read())
        print("downloaded", dest)


def main(only_slugs: set[str] | None = None):
    download_logos(only_slugs)
    for b in BRIEFS:
        if only_slugs is not None and b["slug"] not in only_slugs:
            continue
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

Priority 1 outreach preview. Live at `/{b['slug']}` after deploy.

Status: draft for internal audit.
"""
        (slug_dir / "README.md").write_text(readme, encoding="utf-8")
        print("wrote", slug_dir / "index.html")


if __name__ == "__main__":
    import sys

    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    main(only)
