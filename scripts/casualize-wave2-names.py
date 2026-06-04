#!/usr/bin/env python3
"""Propose and write CasualizedName for all Wave 2 Fit Pass rows."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from wave2_utils import (  # noqa: E402
    SERVICE_ACCOUNT_KEY,
    WAVE2_SHEET_ID,
    WAVE2_TAB,
    casualize_name,
    row_dict,
    slugify,
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CSV_OUT = ROOT / "data" / "wave2-casual-names.csv"
COL_HEADER = "CasualizedName"


def load_sheet():
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
    return svc, rows[0], rows[1:]


def build_proposals(headers: list[str], data_rows: list[list[str]]):
    proposals: list[dict[str, str]] = []
    for row in data_rows:
        r = row_dict(headers, row)
        legal = r.get("Name", "")
        domain = r.get("Domain", "")
        casual, needs_review = casualize_name(legal, domain=domain)
        slug = slugify(casual, domain, legal)
        proposals.append(
            {
                "Name": legal,
                "CasualizedName": casual,
                "Domain": domain,
                "Slug": slug,
                "NeedsReview": "yes" if needs_review else "",
                "Priority": r.get("Priority", ""),
            }
        )
    return proposals


def write_csv(proposals: list[dict[str, str]]) -> None:
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = ["Name", "CasualizedName", "Domain", "Slug", "NeedsReview", "Priority"]
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(proposals)
    print(f"wrote {CSV_OUT}")


def apply_to_sheet(svc, headers: list[str], proposals: list[dict[str, str]]) -> None:
    if COL_HEADER in headers:
        col_idx = headers.index(COL_HEADER)
    else:
        col_idx = len(headers)
        headers = headers + [COL_HEADER]
        svc.spreadsheets().values().update(
            spreadsheetId=WAVE2_SHEET_ID,
            range=f"'{WAVE2_TAB}'!A1",
            valueInputOption="RAW",
            body={"values": [headers]},
        ).execute()

    col_letter = _col_letter(col_idx)
    values = [[p["CasualizedName"]] for p in proposals]
    svc.spreadsheets().values().update(
        spreadsheetId=WAVE2_SHEET_ID,
        range=f"'{WAVE2_TAB}'!{col_letter}2:{col_letter}{len(values) + 1}",
        valueInputOption="RAW",
        body={"values": values},
    ).execute()
    print(f"wrote {COL_HEADER} to column {col_letter} ({len(values)} rows)")


def _col_letter(idx: int) -> str:
    n = idx + 1
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Pass --dry-run or --apply")

    svc, headers, data_rows = load_sheet()
    proposals = build_proposals(headers, data_rows)
    flagged = sum(1 for p in proposals if p["NeedsReview"])
    print(f"rows: {len(proposals)}  needs review: {flagged}")
    for p in proposals[:8]:
        flag = " [review]" if p["NeedsReview"] else ""
        print(f"  {p['Name']!r} → {p['CasualizedName']!r}{flag}")
    print("  ...")

    write_csv(proposals)
    if args.apply:
        apply_to_sheet(svc, headers, proposals)
        url = f"https://docs.google.com/spreadsheets/d/{WAVE2_SHEET_ID}/edit"
        print(url)


if __name__ == "__main__":
    main()
