#!/usr/bin/env python3
"""Export growth brief QA list to a Google Sheet tab for manual review."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
KEY = Path("/Users/stephendiedrich/Desktop/upstory/upstory-494617-fe9165a30344.json")
SHEET_ID = "1HnA1Auy2BTy-IszZbBBOod8YcrBUJUqG6v94JDD2weA"
TAB_NAME = "Growth Brief Review"
BASE_URL = "https://clients.upstory.co"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CSV_OUT = ROOT / "growth-brief-review.csv"

# Manual / non-generator briefs (not in BRIEFS catalogs)
EXTRA_HEADLINES: dict[str, str] = {
    "stake": (
        "We believe we can help Stake move 40% of UMoveFree renters to first rent payment."
    ),
    "abby-care": (
        "We believe we can help Abby Care cut median days-to-certification to 45 in each new state."
    ),
    "citizen-health": (
        "We believe we can help Citizen Health add 90 five-star App Store ratings."
    ),
}

ICP_SHEET_GID = 724991299
ICP_NAME_COL = 0
ICP_INSIGHT_COL = 28

# Slug → ICP "Name" when it differs from CO_SLUG / QA display name
SLUG_ICP_NAME: dict[str, str] = {
    "carpooll": "Carpooll.com",
    "faireez": "Faireez inc.",
    "medbill-ai": "Medbill AI",
    "ivideon": "Ivideon. Cloud Video Surveillance",
    "lasting": "Lasting (acquired by Talkspace)",
    "marble": "Marble (Acquired by The Zebra)",
    "catchcorner": "CatchCorner by Sports Illustrated",
    "diem-app": "Diem App",
    "gride-technology": "Gride Technology",
    "homma": "HOMMA Group, Inc",
    "otozen": "OtoZen: Driving and Family Safety App",
    "super-unlimited": "Super Unlimited Inc.",
    "tiicker": "TiiCKER",
    "citizen-health": "Citizen",
}

HEADER = [
    "#",
    "Company Name",
    "About",
    "Outreach Insight",
    "Headline",
    "Top Opportunity",
    "Brief URL",
    "Slug",
    "Review Status",
    "Notes",
    "OK to send?",
]


def load_modules():
    spec_qa = importlib.util.spec_from_file_location(
        "qa", ROOT / "scripts" / "generate-qa-index.py"
    )
    qa = importlib.util.module_from_spec(spec_qa)
    assert spec_qa.loader is not None
    spec_qa.loader.exec_module(qa)

    spec_p1 = importlib.util.spec_from_file_location(
        "p1", ROOT / "scripts" / "generate-p1-briefs.py"
    )
    p1 = importlib.util.module_from_spec(spec_p1)
    assert spec_p1.loader is not None
    spec_p1.loader.exec_module(p1)

    spec_p2 = importlib.util.spec_from_file_location(
        "p2", ROOT / "scripts" / "briefs_p2_p4.py"
    )
    p2 = importlib.util.module_from_spec(spec_p2)
    assert spec_p2.loader is not None
    spec_p2.loader.exec_module(p2)

    spec_sheet = importlib.util.spec_from_file_location(
        "sheet", ROOT / "scripts" / "briefs_sheet_wave1.py"
    )
    sheet = importlib.util.module_from_spec(spec_sheet)
    assert spec_sheet.loader is not None
    spec_sheet.loader.exec_module(sheet)

    headlines: dict[str, str] = dict(EXTRA_HEADLINES)
    for b in list(p1.BRIEFS) + list(p2.BRIEFS_P2_P4) + list(sheet.BRIEFS_SHEET_WAVE1):
        headlines[b["slug"]] = b.get("headline", "")

    return qa, headlines


def load_icp_outreach_insights() -> dict[str, str]:
    """Company Name (ICP tab) → Insight for Outreach."""
    if not KEY.is_file():
        return {}
    creds = service_account.Credentials.from_service_account_file(
        str(KEY), scopes=SCOPES
    )
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    meta = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    title = next(
        s["properties"]["title"]
        for s in meta["sheets"]
        if s["properties"]["sheetId"] == ICP_SHEET_GID
    )
    res = (
        svc.spreadsheets()
        .values()
        .get(spreadsheetId=SHEET_ID, range=f"'{title}'!A1:ZZ")
        .execute()
    )
    out: dict[str, str] = {}
    for row in res.get("values", [])[1:]:
        if len(row) <= ICP_NAME_COL:
            continue
        name = str(row[ICP_NAME_COL]).strip()
        insight = (
            str(row[ICP_INSIGHT_COL]).strip()
            if len(row) > ICP_INSIGHT_COL
            else ""
        )
        if name and insight:
            out[name] = insight
    return out


def outreach_insight_for_slug(
    slug: str,
    display_name: str,
    icp_insights: dict[str, str],
    slug_to_co: dict[str, str],
) -> str:
    for key in (
        SLUG_ICP_NAME.get(slug),
        slug_to_co.get(slug),
        display_name,
    ):
        if key and key in icp_insights:
            return icp_insights[key]
    return ""


def build_rows(
    qa,
    headlines: dict[str, str],
    icp_insights: dict[str, str],
) -> list[list[str]]:
    slug_to_co = {v: k for k, v in qa.CO_SLUG.items()}
    items = qa.entries()
    rows: list[list[str]] = [HEADER]
    for i, e in enumerate(items, start=1):
        slug = e["slug"]
        url = f"{BASE_URL}/{slug}"
        insight = outreach_insight_for_slug(
            slug, e["name"], icp_insights, slug_to_co
        )
        rows.append(
            [
                str(i),
                e["name"],
                e["about"],
                insight,
                headlines.get(slug, ""),
                e["opportunity"],
                url,
                slug,
                "Pending",
                "",
                "",
            ]
        )
    return rows


def write_csv(rows: list[list[str]]) -> None:
    import csv

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"wrote {CSV_OUT}")


def get_or_create_tab(svc, title: str) -> int:
    meta = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    for s in meta.get("sheets", []):
        if s["properties"]["title"] == title:
            return s["properties"]["sheetId"]

    resp = (
        svc.spreadsheets()
        .batchUpdate(
            spreadsheetId=SHEET_ID,
            body={"requests": [{"addSheet": {"properties": {"title": title}}}]},
        )
        .execute()
    )
    return resp["replies"][0]["addSheet"]["properties"]["sheetId"]


def clear_and_write(svc, gid: int, rows: list[list[str]]) -> None:
    svc.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID,
        range=f"'{TAB_NAME}'!A:Z",
    ).execute()
    svc.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f"'{TAB_NAME}'!A1",
        valueInputOption="RAW",
        body={"values": rows},
    ).execute()

    # Freeze header row
    svc.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={
            "requests": [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": gid,
                            "gridProperties": {"frozenRowCount": 1},
                        },
                        "fields": "gridProperties.frozenRowCount",
                    }
                },
                {
                    "autoResizeDimensions": {
                        "dimensions": {
                            "sheetId": gid,
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": len(HEADER),
                        }
                    }
                },
            ]
        },
    ).execute()


def main() -> int:
    qa, headlines = load_modules()
    icp_insights = load_icp_outreach_insights()
    rows = build_rows(qa, headlines, icp_insights)
    write_csv(rows)
    missing = sum(1 for r in rows[1:] if not r[3])
    if missing:
        print(f"warning: {missing} rows missing Outreach Insight", file=sys.stderr)

    if not KEY.is_file():
        print("Service account key missing; CSV only.", file=sys.stderr)
        return 1

    creds = service_account.Credentials.from_service_account_file(
        str(KEY), scopes=SCOPES
    )
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    gid = get_or_create_tab(svc, TAB_NAME)
    clear_and_write(svc, gid, rows)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid={gid}"
    print(f"wrote {len(rows) - 1} companies to tab '{TAB_NAME}'")
    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
