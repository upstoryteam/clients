#!/usr/bin/env python3
"""Generate all growth brief HTML pages (P1 + P2–P4). Excludes existing clients."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGOS = ROOT / "shared" / "logos"

_spec = importlib.util.spec_from_file_location(
    "gen_p1", Path(__file__).with_name("generate-p1-briefs.py"),
)
_gen = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_gen)

_p2_spec = importlib.util.spec_from_file_location(
    "briefs_p2_p4", Path(__file__).with_name("briefs_p2_p4.py"),
)
_p2 = importlib.util.module_from_spec(_p2_spec)
assert _p2_spec.loader is not None
_p2_spec.loader.exec_module(_p2)

EXCLUDE = _p2.EXCLUDE_SLUGS


def wordmark_svg(name: str) -> str:
    label = name.replace("&", "&amp;")
    return (
        f'<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 200 36"><text x="0" y="26" font-family="Manrope,system-ui,sans-serif" '
        f'font-size="22" font-weight="700" fill="#151D1F">{label}</text></svg>'
    )


def ensure_logo(b: dict) -> None:
    ext = b.get("logo_ext", "svg")
    dest = LOGOS / f"{b['slug']}.{ext}"
    if dest.exists():
        return
    if ext == "svg":
        dest.write_text(wordmark_svg(b["name"]), encoding="utf-8")
        print("wordmark", dest)


def all_briefs() -> list[dict]:
    out = [b for b in _gen.BRIEFS if b["slug"] not in EXCLUDE]
    out.extend(_p2.BRIEFS_P2_P4)
    return out


def write_brief(b: dict) -> None:
    ensure_logo(b)
    slug_dir = ROOT / b["slug"]
    slug_dir.mkdir(parents=True, exist_ok=True)
    html = _gen.render_page(b)
    (slug_dir / "index.html").write_text(html, encoding="utf-8")
    meta = {
        "tone": "dark",
        "headerVariant": "plain",
        "source": "growth brief generator",
    }
    (LOGOS / f"{b['slug']}.meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    readme = f"""# {b['name']} growth brief

Outreach preview. Live at `/{b['slug']}` after deploy.

Status: draft for internal audit.
"""
    (slug_dir / "README.md").write_text(readme, encoding="utf-8")
    print("wrote", slug_dir / "index.html")


def main():
    only = None
    import sys

    if len(sys.argv) > 1:
        only = set(sys.argv[1:])
    if only:
        _gen.download_logos(only)
    for b in all_briefs():
        if only is not None and b["slug"] not in only:
            continue
        write_brief(b)
    print("total", len(all_briefs()), "briefs in catalog")


if __name__ == "__main__":
    main()
