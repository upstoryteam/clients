"""Merge Wave 2 brief content with CasualizedName + sheet metadata."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALL_JSON = ROOT / "data" / "wave2-all-pass-rows.json"
P1_JSON = ROOT / "data" / "wave2-p1-rows.json"
REMAINING_JSON = ROOT / "data" / "wave2-p1-remaining.json"
ALL_REMAINING_JSON = ROOT / "data" / "wave2-remaining-rows.json"


def refresh_p1_rows() -> list[dict]:
    """Reload P1 rows from Google Sheet into wave2-p1-rows.json."""
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "load-wave2-sheet.py"),
            "--priority",
            "1",
            "-o",
            str(P1_JSON),
        ],
        check=True,
    )
    return load_p1_rows()


def refresh_all_rows() -> list[dict]:
    """Reload all Wave 2 pass rows from Google Sheet."""
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "load-wave2-sheet.py"),
            "-o",
            str(ALL_JSON),
        ],
        check=True,
    )
    return load_all_rows()


def load_p1_rows(*, refresh: bool = False) -> list[dict]:
    if refresh or not P1_JSON.is_file():
        return refresh_p1_rows()
    return json.loads(P1_JSON.read_text(encoding="utf-8"))


def load_all_rows(*, refresh: bool = False) -> list[dict]:
    if refresh or not ALL_JSON.is_file():
        return refresh_all_rows()
    return json.loads(ALL_JSON.read_text(encoding="utf-8"))


def apply_sheet_names(briefs: list[dict], rows: list[dict] | None = None) -> list[dict]:
    """Overlay CasualizedName (and logo URL when present) from sheet rows."""
    by_slug = {r["slug"]: r for r in (rows or load_p1_rows())}
    out: list[dict] = []
    for b in briefs:
        nb = dict(b)
        row = by_slug.get(b["slug"])
        if row:
            nb["name"] = row["name"]
            if row.get("logo_url"):
                nb["logo_url"] = row["logo_url"]
                nb.setdefault("logo_ext", "png")
        out.append(nb)
    return out


def get_wave2_briefs(*, refresh_sheet: bool = False) -> list[dict]:
    from briefs_wave2 import BRIEFS_WAVE2

    rows = load_all_rows(refresh=refresh_sheet)
    return apply_sheet_names(BRIEFS_WAVE2, rows)


def get_remaining_rows(
    *, priority: str | None = None, refresh_sheet: bool = False
) -> list[dict]:
    from briefs_wave2 import BRIEFS_WAVE2

    done = {b["slug"] for b in BRIEFS_WAVE2}
    rows = [r for r in load_all_rows(refresh=refresh_sheet) if r["slug"] not in done]
    if priority:
        rows = [r for r in rows if r.get("priority") == priority]
    return rows


def get_remaining_p1_rows(*, refresh_sheet: bool = False) -> list[dict]:
    return get_remaining_rows(priority="1", refresh_sheet=refresh_sheet)


def write_remaining_queue(*, refresh_sheet: bool = False) -> Path:
    rows = get_remaining_p1_rows(refresh_sheet=refresh_sheet)
    REMAINING_JSON.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return REMAINING_JSON


def write_remaining_queues(*, refresh_sheet: bool = False) -> dict[str, Path]:
    rows = get_remaining_rows(refresh_sheet=refresh_sheet)
    ALL_REMAINING_JSON.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    paths = {"all": ALL_REMAINING_JSON}
    for priority in ("1", "2", "3", "4"):
        priority_rows = [r for r in rows if r.get("priority") == priority]
        path = ROOT / "data" / f"wave2-p{priority}-remaining.json"
        path.write_text(json.dumps(priority_rows, indent=2) + "\n", encoding="utf-8")
        paths[priority] = path
    return paths


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Reload all rows from sheet")
    parser.add_argument("--queue", action="store_true", help="Write wave2-p1-remaining.json")
    parser.add_argument(
        "--queues",
        action="store_true",
        help="Write all remaining queues, including p2/p3/p4 files",
    )
    args = parser.parse_args()

    if args.refresh:
        rows = refresh_all_rows()
        print(f"refreshed {len(rows)} rows → {ALL_JSON}")
        p1 = [r for r in rows if r.get("priority") == "1"]
        P1_JSON.write_text(json.dumps(p1, indent=2) + "\n", encoding="utf-8")
        print(f"refreshed {len(p1)} P1 rows → {P1_JSON}")
    if args.queue:
        path = write_remaining_queue(refresh_sheet=False)
        remaining = json.loads(path.read_text(encoding="utf-8"))
        print(f"wrote {len(remaining)} remaining → {path}")
    if args.queues:
        paths = write_remaining_queues(refresh_sheet=False)
        for label, path in paths.items():
            remaining = json.loads(path.read_text(encoding="utf-8"))
            print(f"wrote {len(remaining)} remaining ({label}) → {path}")
