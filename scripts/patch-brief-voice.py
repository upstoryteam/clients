#!/usr/bin/env python3
"""One-off patch: headlines without deadlines, What we see + client-facing insights."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATCHES: dict[str, tuple[str, str, str]] = {
    # slug -> (headline, insight_body, optional calc label in citizen only)
    "stake/index.html": (
        "We believe we can help Stake move 40% of UMoveFree renters to first rent payment.",
        "Right after the UMoveFree handoff, renters still have the apartment math in their head. That is when Cash Back needs to feel real, in the same session, not later in onboarding.",
        "",
    ),
    "abby-care/index.html": (
        "We believe we can help Abby Care cut median days-to-certification to 45 in each new state.",
        "Your new states are sending you applicants who already plan to care at home. The friction we see is training modules and Medicaid paperwork feeling like two different products. One guided queue would speed certification.",
        "",
    ),
    "citizen-health/index.html": (
        "We believe we can help Citizen Health add 90 five-star App Store ratings.",
        "When someone lands on your homepage, they are already leaning in on the problem. The signup flow still asks for email before the Advocate runs. Closing that gap is the fastest path to more accounts and more public proof.",
        "Projected five-star ratings",
    ),
    "akko/index.html": (
        "We believe we can help AKKO shorten partner time-to-first policy sale after the Upsie integration.",
        "You are scaling partner distribution after Upsie, and partners only win when embed and checkout feel turnkey. The gap we keep seeing is the path from signed partner to first policy sold.",
        "",
    ),
    "cloaked/index.html": (
        "We believe we can help Cloaked lift enterprise trial-to-paid conversion by 25%.",
        "You are pushing into enterprise while the product still wins on consumer polish. People need to feel a live identity in the first minute, the same way they do on the consumer app.",
        "",
    ),
    "eternal/index.html": (
        "We believe we can help Eternal lift athlete enrollment completion to 65%.",
        "Your clinical model is strong. On the public site, athletes are still asked to commit before they have felt what performance care looks like from you. The long intake form comes before the first win.",
        "",
    ),
    "dorsia/index.html": (
        "We believe we can help Dorsia convert 20% more membership applicants to paid members.",
        "Members pay before they have experienced the network. If the first reservation still feels uncertain, Culture Calendar and wallet work do not get a chance to matter. The break is apply through first booking.",
        "",
    ),
    "caramel/index.html": (
        "We believe we can help Caramel lift eBay checkout completion by 15% on private-party listings.",
        "Checkout inside eBay is not your UI, but it is your conversion problem. Buyers did not choose Caramel. They need trust and clarity before they fund a high-ticket purchase.",
        "",
    ),
    "brave/index.html": (
        "We believe we can help Brave move 30% more developers from API key signup to first paid query.",
        "Brave Search is a different product than the browser. Developers are being asked for billing before they have run a query that proves the index on their use case.",
        "",
    ),
    "whisker-labs/index.html": (
        "We believe we can help Whisker Labs lift Ting device activation to 80% after devices ship.",
        "Ting only matters once it is installed and alerting. Your insurer partners are measured on activation, and homeowners still drop off between the box arriving and a live sensor.",
        "",
    ),
    "vinovest/index.html": (
        "We believe we can help Vinovest fund 25% more new accounts on StartEngine.",
        "The StartEngine audience is bigger, but the same moment still decides trust: money moves only after someone believes the portfolio is real.",
        "",
    ),
    "goldin/index.html": (
        "We believe we can help Goldin lift winning-bid payment completion to 92% on high-value lots.",
        "eBay scale raises the stakes on checkout trust. Bidders commit large sums after the adrenaline fades. Consignors need the same clarity on payouts before anyone wires funds.",
        "",
    ),
    "poparide/index.html": (
        "We believe we can help Poparide book a first trip for 40% of new members.",
        "You have proof the model works at a million members. The next wave will surface verification and first-trip friction. Riders need trust before they get in a stranger's car.",
        "",
    ),
}


def patch_file(rel: str, headline: str, insight: str, calc_label: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = text.replace("Our read", "What we see")
    import re

    text = re.sub(
        r'<h1 class="outcome">.*?</h1>',
        f'<h1 class="outcome">{headline}</h1>',
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = re.sub(
        r'<p class="insight-body">.*?</p>',
        f'<p class="insight-body">{insight}</p>',
        text,
        count=1,
        flags=re.DOTALL,
    )
    if calc_label:
        text = text.replace("New ratings in 90 days", calc_label)
    path.write_text(text, encoding="utf-8")
    print("patched", rel)


def main():
    for rel, (h, i, c) in PATCHES.items():
        patch_file(rel, h, i, c)


if __name__ == "__main__":
    main()
