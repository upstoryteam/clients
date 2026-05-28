#!/usr/bin/env python3
"""Add Audit Link column to Contacts_Combined for Instantly / outreach export."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
KEY = Path("/Users/stephendiedrich/Desktop/upstory/upstory-494617-fe9165a30344.json")
SHEET_ID = "1Gs_FA3fvry3q7i79JYhriDpGCEwyLP24Xer67WMXH0o"
GID = 1698358620
TAB = "Contacts_Combined"
BASE_URL = "https://clients.upstory.co"
COL_HEADER = "Audit Link"
EXCLUDE_COMPANIES = {"Brave"}

_spec = importlib.util.spec_from_file_location(
    "qa", ROOT / "scripts" / "generate-qa-index.py"
)
_qa = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_qa)

_spec2 = importlib.util.spec_from_file_location(
    "cov", ROOT / "scripts" / "check-brief-coverage.py"
)
_cov = importlib.util.module_from_spec(_spec2)
assert _spec2.loader is not None
_spec2.loader.exec_module(_cov)


def company_to_slug() -> dict[str, str]:
    out = dict(_cov.CO_TO_SLUG)
    out.update(_qa.CO_SLUG)
    return out


def col_letter(idx: int) -> str:
    idx += 1
    result = ""
    while idx:
        idx, rem = divmod(idx - 1, 26)
        result = chr(65 + rem) + result
    return result


def main() -> int:
    if not KEY.is_file():
        print("Missing service account key", file=sys.stderr)
        return 1

    mapping = company_to_slug()
    creds = service_account.Credentials.from_service_account_file(
        str(KEY), scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    ss = svc.spreadsheets()

    header = ss.values().get(
        spreadsheetId=SHEET_ID, range=f"'{TAB}'!1:1"
    ).execute().get("values", [[]])[0]

    if COL_HEADER in header:
        col_idx = header.index(COL_HEADER)
    else:
        col_idx = len(header)
        letter = col_letter(col_idx)
        ss.values().update(
            spreadsheetId=SHEET_ID,
            range=f"'{TAB}'!{letter}1",
            valueInputOption="RAW",
            body={"values": [[COL_HEADER]]},
        ).execute()

    rows = ss.values().get(
        spreadsheetId=SHEET_ID, range=f"'{TAB}'!A2:I200"
    ).execute().get("values", [])
    co_col = 8  # Company Name

    links: list[list[str]] = []
    missing: list[str] = []
    for row in rows:
        co = row[co_col].strip() if len(row) > co_col else ""
        if not co or co in EXCLUDE_COMPANIES:
            links.append([""])
            continue
        slug = mapping.get(co)
        if not slug:
            links.append([""])
            missing.append(co)
            continue
        brief_path = ROOT / slug / "index.html"
        if not brief_path.is_file():
            links.append([""])
            missing.append(f"{co} (no {slug}/index.html)")
            continue
        links.append([f"{BASE_URL}/{slug}"])

    letter = col_letter(col_idx)
    end = len(rows) + 1
    ss.values().update(
        spreadsheetId=SHEET_ID,
        range=f"'{TAB}'!{letter}2:{letter}{end}",
        valueInputOption="RAW",
        body={"values": links},
    ).execute()

    meta = ss.get(spreadsheetId=SHEET_ID).execute()
    gid = next(
        s["properties"]["sheetId"]
        for s in meta["sheets"]
        if s["properties"]["title"] == TAB
    )
    ss.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={
            "requests": [{
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": gid,
                        "dimension": "COLUMNS",
                        "startIndex": col_idx,
                        "endIndex": col_idx + 1,
                    }
                }
            }]
        },
    ).execute()

    filled = sum(1 for x in links if x[0])
    print(f"Wrote {filled}/{len(links)} audit links to column {letter} ({COL_HEADER})")
    if missing:
        print(f"warning: {len(missing)} rows without link:", file=sys.stderr)
        for m in sorted(set(missing))[:20]:
            print(f"  - {m}", file=sys.stderr)
    print(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid={gid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
