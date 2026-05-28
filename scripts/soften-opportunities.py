#!/usr/bin/env python3
"""Soften opportunities section copy across growth brief HTML pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP = {ROOT / "citizen-health" / "legacy-audit" / "index.html"}

GERUND = {
    "lead": "leading",
    "open": "opening",
    "show": "showing",
    "map": "mapping",
    "track": "tracking",
    "surface": "surfacing",
    "instrument": "instrumenting",
    "ask": "asking",
    "preview": "previewing",
    "shorten": "shortening",
    "tag": "tagging",
    "package": "packaging",
    "ship": "shipping",
    "unify": "unifying",
    "template": "templating",
    "funnel": "funneling",
    "align": "aligning",
    "confirm": "confirming",
    "reuse": "reusing",
    "tighten": "tightening",
}


def soften_body(text: str) -> str:
    for verb, gerund in GERUND.items():
        text = text.replace(f"We would {verb} ", f"We'd start by {gerund} ")
    text = text.replace("We would ", "We'd ")
    return text


def patch_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '<h2 class="opportunities-heading">Opportunities</h2>',
        '<h2 class="opportunities-heading">Opportunities to explore</h2>',
    )
    text = text.replace(
        "Three places we would start in the product.",
        "Three places we'd start in the product.",
    )
    text = text.replace(
        "Illustrative. Where we would look first.",
        "Illustrative. Where we'd look first.",
    )

    def repl_body(match: re.Match[str]) -> str:
        inner = match.group(1)
        return f'<div class="solution-body">\n          <p>{soften_body(inner)}</p>'

    text = re.sub(
        r'<div class="solution-body">\s*<p>(.*?)</p>',
        repl_body,
        text,
        flags=re.DOTALL,
    )

    path.write_text(text, encoding="utf-8")
    print("softened", path.relative_to(ROOT))


def main():
    for path in sorted(ROOT.glob("**/index.html")):
        if path in SKIP:
            continue
        if not (path.parent / "index.html") == path:
            continue
        # growth brief folders only: has brief.css link
        if "/shared/brief.css" not in path.read_text(encoding="utf-8"):
            continue
        patch_html(path)


if __name__ == "__main__":
    main()
