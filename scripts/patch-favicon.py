#!/usr/bin/env python3
"""Add Upstory favicon links to growth brief HTML pages."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAVICON = """  <link rel="icon" href="/shared/favicon-light.svg" type="image/svg+xml" media="(prefers-color-scheme: light)">
  <link rel="icon" href="/shared/favicon-dark.svg" type="image/svg+xml" media="(prefers-color-scheme: dark)">
"""


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "favicon-light.svg" in text:
        return False
    if "/shared/brief.css" not in text and path.name != "qa-briefs.html":
        return False
    marker = "  <title>"
    idx = text.find(marker)
    if idx == -1:
        return False
    end = text.find("</title>", idx)
    if end == -1:
        return False
    insert_at = end + len("</title>\n")
    text = text[:insert_at] + FAVICON + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    return True


def main():
    targets = list(ROOT.glob("**/index.html")) + [ROOT / "qa-briefs.html"]
    for path in sorted(targets):
        if path == ROOT / "citizen-health" / "index.html":
            continue
        if patch(path):
            print("patched", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
