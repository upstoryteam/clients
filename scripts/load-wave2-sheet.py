#!/usr/bin/env python3
"""Load Wave 2 Fit Pass rows into normalized JSON for brief generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from wave2_utils import (  # noqa: E402
    PILOT_SLUGS,
    SERVICE_ACCOUNT_KEY,
    WAVE2_SHEET_ID,
    WAVE2_TAB,
    compose_context,
    compose_recent_news,
    row_dict,
    slugify,
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
OUT_DIR = ROOT / "data"


def load_rows() -> tuple[list[str], list[list[str]]]:
    if not SERVICE_ACCOUNT_KEY.is_file():
        raise SystemExit(f"Missing service account key: {SERVICE_ACCOUNT_KEY}")
    creds = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_KEY), scopes=SCOPES
    )
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    res = (
        svc.spreadsheets()
        .values()
        .get(spreadsheetId=WAVE2_SHEET_ID, range=f"'{WAVE2_TAB}'!A1:ZZ")
        .execute()
    )
    rows = res.get("values", [])
    if not rows:
        raise SystemExit("Empty sheet")
    headers = rows[0]
    if "CasualizedName" not in headers:
        raise SystemExit(
            "CasualizedName column missing. Run: python3 scripts/casualize-wave2-names.py --apply"
        )
    return headers, rows[1:]


def normalize_row(headers: list[str], row: list[str]) -> dict | None:
    r = row_dict(headers, row)
    if r.get("Fit Verdict", "").strip() != "Pass":
        return None
    legal = r.get("Name", "")
    casual = r.get("CasualizedName", "").strip() or legal
    domain = r.get("Domain", "")
    slug = slugify(casual, domain, legal)
    return {
        "slug": slug,
        "name": casual,
        "legal_name": legal,
        "domain": domain,
        "trust_type": r.get("Trust Type", ""),
        "priority": r.get("Priority", ""),
        "about": r.get("Inferred Company Goals", ""),
        "outreach_insight": r.get("Insight for Outreach", ""),
        "context_block": compose_context(r),
        "recent_news": compose_recent_news(r),
        "logo_url": r.get("Logo URL (Apollo)", ""),
        "hiring_focus": r.get("Inferred Company Goals", ""),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", action="store_true", help="Export pilot slugs only")
    parser.add_argument("--priority", type=str, help="Filter by Priority value")
    parser.add_argument(
        "-o",
        type=Path,
        default=OUT_DIR / "wave2-pilot-rows.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    headers, data_rows = load_rows()
    out: list[dict] = []
    for row in data_rows:
        norm = normalize_row(headers, row)
        if norm is None:
            continue
        if args.priority and norm.get("priority") != args.priority:
            continue
        if args.pilot and norm["slug"] not in PILOT_SLUGS:
            continue
        out.append(norm)

    args.o.parent.mkdir(parents=True, exist_ok=True)
    args.o.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(out)} rows → {args.o}")


if __name__ == "__main__":
    main()
