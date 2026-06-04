"""Wave 2 outreach triage: ship or skip only."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALL_JSON = ROOT / "data" / "wave2-all-pass-rows.json"
GAPS_CSV = ROOT / "data" / "wave2-contacts-gaps.csv"
STATUS_CSV = ROOT / "data" / "wave2-ship-status.csv"

ENTITY = re.compile(
    r"entity verification|clay and apollo describe different organizations",
    re.I,
)
DEAD = re.compile(
    r"\b(was acquired by|been acquired by|recently acquired by|"
    r"shut down|closed down|defunct|merged into|"
    r"no longer operating|ceased operations|bankrupt|wind down|"
    r"discontinued operations)\b",
    re.I,
)
LOCAL_NAME = re.compile(
    r"chiropractic|pediatrics|dentist|dental\b|law firm|law office|"
    r"physical therapy|family medicine|primary care clinic|\.law\b",
    re.I,
)
REGISTRY = re.compile(r"top-level domain|\.law is a|registry trust|nic\.", re.I)

# Different companies — do not merge. Skip aviation row only (bad entity match).
FORCE_SKIP_SLUGS = {
    "blackbird",  # flyblackbird.com private aviation; not Blackbird Labs
}

from wave2_utils import DOMAIN_SLUG_OVERRIDES

DOMAIN_SLUG_MAP = DOMAIN_SLUG_OVERRIDES


def norm_domain(domain: str) -> str:
    d = (domain or "").strip().lower()
    d = re.sub(r"^https?://(www\.)?", "", d)
    return d.split("/")[0]


def slug_for_row(row: dict) -> str:
    dom = norm_domain(row.get("domain", ""))
    if dom in DOMAIN_SLUG_MAP:
        return DOMAIN_SLUG_MAP[dom]
    return row["slug"]


def load_gaps() -> dict[str, dict]:
    if not GAPS_CSV.is_file():
        return {}
    rows = json.loads(ALL_JSON.read_text(encoding="utf-8"))
    by_domain = {norm_domain(r["domain"]): slug_for_row(r) for r in rows}
    out: dict[str, dict] = {}
    for r in csv.DictReader(GAPS_CSV.open(encoding="utf-8")):
        slug = by_domain.get(norm_domain(r.get("domain", "")))
        if slug:
            out[slug] = r
    return out


def triage_row(row: dict, *, keepers: int = -1) -> tuple[str, str]:
    """Binary triage: ship unless clearly wrong, dead, or not ICP."""
    slug = slug_for_row(row)
    priority = str(row.get("priority", ""))
    text = " ".join(
        row.get(k, "") for k in ("about", "context_block", "name", "legal_name")
    )
    display_name = row.get("name", "") + " " + row.get("legal_name", "")

    if slug in FORCE_SKIP_SLUGS:
        return "skip", "entity mismatch / wrong company row"

    if REGISTRY.search(text) or LOCAL_NAME.search(display_name):
        return "skip", "local clinic or registry — not ICP"

    if DEAD.search(text):
        return "skip", "likely dead or acquired"

    if ENTITY.search(text) and priority == "4":
        return "skip", "entity verification — Clay/Apollo mismatch"

    return "ship", f"P{priority} — send when contact found"


def build_status_rows(
    all_rows: list[dict] | None = None,
    gaps: dict[str, dict] | None = None,
) -> list[dict]:
    rows = all_rows or json.loads(ALL_JSON.read_text(encoding="utf-8"))
    gaps = gaps if gaps is not None else load_gaps()
    out: list[dict] = []
    for row in rows:
        slug = slug_for_row(row)
        gap = gaps.get(slug) or gaps.get(row["slug"], {})
        keepers = int(gap.get("keepers") or 0)
        status, reason = triage_row(row, keepers=keepers)
        out.append(
            {
                "slug": slug,
                "casual_name": row.get("name", ""),
                "domain": row.get("domain", ""),
                "priority": row.get("priority", ""),
                "keepers": keepers,
                "ship_status": status,
                "reason": reason,
            }
        )
    return out


def write_status_csv(rows: list[dict] | None = None) -> Path:
    rows = rows or build_status_rows()
    fields = [
        "slug",
        "casual_name",
        "domain",
        "priority",
        "keepers",
        "ship_status",
        "reason",
    ]
    with STATUS_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["ship_status"], r["priority"], r["casual_name"])))
    return STATUS_CSV


def status_by_slug(rows: list[dict] | None = None) -> dict[str, dict]:
    return {r["slug"]: r for r in (rows or build_status_rows())}


def skip_slugs(rows: list[dict] | None = None) -> set[str]:
    return {r["slug"] for r in (rows or build_status_rows()) if r["ship_status"] == "skip"}


def fix_tulip_slugs_in_json(path: Path = ALL_JSON) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for row in data:
        dom = norm_domain(row.get("domain", ""))
        new_slug = DOMAIN_SLUG_MAP.get(dom)
        if new_slug and row.get("slug") != new_slug:
            row["slug"] = new_slug
            changed += 1
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return changed


def fix_tulip_casual_names_csv(path: Path = ROOT / "data" / "wave2-casual-names.csv") -> int:
    if not path.is_file():
        return 0
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    changed = 0
    for r in rows:
        dom = norm_domain(r.get("Domain", ""))
        new_slug = DOMAIN_SLUG_MAP.get(dom)
        if new_slug and r.get("Slug") != new_slug:
            r["Slug"] = new_slug
            changed += 1
        if dom == "tulipcremation.com":
            r["CasualizedName"] = "Tulip Cremation"
        elif dom == "tulipfertility.com":
            r["CasualizedName"] = "Tulip Fertility"
    if rows:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
    return changed


def fix_briefs_tulip_slug(briefs_path: Path = ROOT / "scripts" / "briefs_wave2.py") -> bool:
    text = briefs_path.read_text(encoding="utf-8")
    old = '"slug": "tulip",\n        "name": "Tulip",\n        "logo_ext": "png",\n        "logo_url": "https://zenprospect-production.s3.amazonaws.com/uploads/pictures/67303a97d2dcf10001bb55a7/picture",\n        "about": "Tulip (tulipfertility.com)'
    new = '"slug": "tulip-fertility",\n        "name": "Tulip Fertility",\n        "logo_ext": "png",\n        "logo_url": "https://zenprospect-production.s3.amazonaws.com/uploads/pictures/67303a97d2dcf10001bb55a7/picture",\n        "about": "Tulip (tulipfertility.com)'
    if old not in text:
        return False
    text = text.replace(old, new, 1)
    text = text.replace(
        '"slug": "tulip-cremation",\n        "name": "Tulip",',
        '"slug": "tulip-cremation",\n        "name": "Tulip Cremation",',
        1,
    )
    briefs_path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    n_json = fix_tulip_slugs_in_json()
    n_csv = fix_tulip_casual_names_csv()
    fixed = fix_briefs_tulip_slug()
    rows = build_status_rows()
    path = write_status_csv(rows)
    counts = {}
    for r in rows:
        counts[r["ship_status"]] = counts.get(r["ship_status"], 0) + 1
    print(f"fixed tulip slugs in JSON: {n_json}")
    print(f"fixed tulip rows in casual CSV: {n_csv}")
    print(f"fixed tulip-fertility in briefs_wave2.py: {fixed}")
    print(f"wrote {path}")
    print("status:", counts)


if __name__ == "__main__":
    main()
