#!/usr/bin/env python3
"""Append a chunk of authored Wave 2 briefs to scripts/briefs_wave2.py.

Reads an authored chunk JSON (list of dicts) plus row data from
data/wave2-remaining-rows.json, validates copy against the Wave 2 banned-term
rules, formats each entry exactly like the existing BRIEFS_WAVE2 dicts, and
inserts them before the closing ``]`` of the list.

Authored chunk entry schema (per company)::

    {
      "slug": "acme",
      "qa_about": "Plain one-line description of what the product does.",
      "headline": "We believe we can help Acme ...",
      "insight": "Two sentences about the decisive moment.",
      "about": "optional override; defaults to the row's about (sanitized)",
      "opps": [
        {"n": "01", "title": "...", "body": "...",
         "journey": [["Step one", false], ["Step two", true], ["Step three", false]]},
        {"n": "02", "title": "...", "body": "..."},
        {"n": "03", "title": "...", "body": "..."}
      ],
      "measures": ["...", "...", "..."]
    }
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIEFS_PY = ROOT / "scripts" / "briefs_wave2.py"
ROWS_JSON = ROOT / "data" / "wave2-authoring-rows.json"

# Slugs whose brand name legitimately contains "trust"; the term is allowed
# there (it is a proper noun, not descriptive copy).
TRUST_BRAND_SLUGS = {
    "token-of-trust",
    "trustedid",
    "trust-swiftly",
}

BANNED_SUBSTRINGS = [
    "—",          # em dash
    "actually",
    "probably",
    "something real",
    "(yc",
    "cse:",
    "nyse:",
    "nasdaq:",
]


def sanitize_about(text: str) -> str:
    """Light cleanup of internal about copy: drop em dashes."""
    text = text.replace(" — ", ", ").replace("—", ", ")
    return text


def check_banned(slug: str, label: str, text: str, *, allow_trust: bool) -> list[str]:
    errs: list[str] = []
    low = text.lower()
    for term in BANNED_SUBSTRINGS:
        if term in low:
            errs.append(f"{slug}: banned '{term}' in {label}: ...{text[max(0, low.find(term) - 20):low.find(term) + 30]}...")
    if not allow_trust and "trust" in low:
        i = low.find("trust")
        errs.append(f"{slug}: banned 'trust' in {label}: ...{text[max(0, i - 20):i + 30]}...")
    return errs


def pystr(s: str) -> str:
    """Emit a double-quoted Python string literal (json.dumps is valid Python)."""
    return json.dumps(s, ensure_ascii=False)


def format_journey(journey) -> str:
    parts = []
    for label, active in journey:
        parts.append(f"({pystr(label)}, {'True' if active else 'False'})")
    return "[" + ", ".join(parts) + "]"


def format_opp(opp: dict) -> str:
    n = opp["n"]
    title = pystr(opp["title"])
    body = pystr(opp["body"])
    if opp.get("journey"):
        return f'            ({pystr(n)}, {title}, {body}, "journey", {format_journey(opp["journey"])}),'
    return f"            ({pystr(n)}, {title}, {body}, None, None),"


def format_entry(brief: dict, row: dict) -> str:
    about = brief.get("about") or sanitize_about(row["about"])
    lines = ["    {"]
    lines.append(f'        "slug": {pystr(brief["slug"])},')
    lines.append(f'        "name": {pystr(row["name"])},')
    lines.append('        "logo_ext": "png",')
    lines.append(f'        "logo_url": {pystr(row.get("logo_url", ""))},')
    lines.append(f'        "about": {pystr(about)},')
    lines.append(f'        "qa_about": {pystr(brief["qa_about"])},')
    lines.append(f'        "headline": {pystr(brief["headline"])},')
    lines.append(f'        "insight": {pystr(brief["insight"])},')
    lines.append('        "opps": [')
    for opp in brief["opps"]:
        lines.append(format_opp(opp))
    lines.append("        ],")
    lines.append('        "measures": [')
    for m in brief["measures"]:
        lines.append(f"            {pystr(m)},")
    lines.append("        ],")
    lines.append("    },")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: append_wave2_chunk.py <chunk.json>", file=sys.stderr)
        return 2
    chunk = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    rows = {r["slug"]: r for r in json.loads(ROWS_JSON.read_text(encoding="utf-8"))}

    # Existing slugs in the file.
    import importlib.util

    spec = importlib.util.spec_from_file_location("bw_check", BRIEFS_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    existing = {b["slug"] for b in mod.BRIEFS_WAVE2}

    errors: list[str] = []
    entries: list[str] = []
    seen: set[str] = set()
    for brief in chunk:
        slug = brief["slug"]
        if slug in existing:
            errors.append(f"{slug}: already present in BRIEFS_WAVE2")
            continue
        if slug in seen:
            errors.append(f"{slug}: duplicate within chunk")
            continue
        seen.add(slug)
        row = rows.get(slug)
        if not row:
            errors.append(f"{slug}: not found in remaining-rows.json")
            continue
        if len(brief["opps"]) != 3:
            errors.append(f"{slug}: expected 3 opps")
        if len(brief["measures"]) != 3:
            errors.append(f"{slug}: expected 3 measures")
        allow_trust = slug in TRUST_BRAND_SLUGS
        about = brief.get("about") or sanitize_about(row["about"])
        copy_fields = {
            "qa_about": brief["qa_about"],
            "headline": brief["headline"],
            "insight": brief["insight"],
            "about": about,
        }
        for opp in brief["opps"]:
            copy_fields[f"opp{opp['n']}-title"] = opp["title"]
            copy_fields[f"opp{opp['n']}-body"] = opp["body"]
        for i, m in enumerate(brief["measures"]):
            copy_fields[f"measure{i}"] = m
        for label, text in copy_fields.items():
            # about is allowed to keep brand trust too; only external-ish copy is strict
            field_allow_trust = allow_trust or label == "about" and allow_trust
            errors.extend(check_banned(slug, label, text, allow_trust=allow_trust))
        entries.append(format_entry(brief, row))

    if errors:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1

    text = BRIEFS_PY.read_text(encoding="utf-8")
    marker = "\n]\n"
    idx = text.rfind(marker)
    if idx == -1:
        print("could not find closing ]", file=sys.stderr)
        return 1
    new_text = text[:idx] + "\n" + "\n".join(entries) + "\n]\n"
    BRIEFS_PY.write_text(new_text, encoding="utf-8")
    print(f"appended {len(entries)} entries; file now has {len(existing) + len(entries)} slugs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
