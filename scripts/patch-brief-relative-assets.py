#!/usr/bin/env python3
"""Use ../shared/ asset paths so briefs work via local server and file:// open."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"qa-briefs.html", "qa-briefs-wave2.html"}


def patch_html(text: str) -> str:
    return (
        text.replace('href="/shared/', 'href="../shared/')
        .replace("href='/shared/", "href='../shared/")
        .replace('src="/shared/', 'src="../shared/')
        .replace("src='/shared/", "src='../shared/")
    )


def main() -> None:
    n = 0
    for path in ROOT.glob("*/index.html"):
        if path.parent.name.startswith("."):
            continue
        raw = path.read_text(encoding="utf-8")
        patched = patch_html(raw)
        if patched != raw:
            path.write_text(patched, encoding="utf-8")
            n += 1
    print(f"Patched {n} brief index.html files")


if __name__ == "__main__":
    main()
