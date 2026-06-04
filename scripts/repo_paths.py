"""Repo-root paths. Works after you move the audits folder under ~/Desktop/upstory/."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Parent folder when audits lives at e.g. ~/Desktop/upstory/audits
UPSTORY_HOME = ROOT.parent


def gcp_service_account_path() -> Path:
    """Google service account JSON for Sheets (not committed)."""
    env = os.environ.get("USTORY_GCP_SERVICE_ACCOUNT_JSON", "").strip()
    if env:
        p = Path(env).expanduser()
        if p.is_file():
            return p
        raise FileNotFoundError(f"USTORY_GCP_SERVICE_ACCOUNT_JSON not found: {p}")

    for candidate in (
        UPSTORY_HOME / "credentials" / "upstory-494617-fe9165a30344.json",
        UPSTORY_HOME / "upstory-494617-fe9165a30344.json",
        Path.home() / ".config" / "upstory" / "gcp-service-account.json",
    ):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "GCP service account JSON not found. Set USTORY_GCP_SERVICE_ACCOUNT_JSON "
        "or place the file in <upstory>/credentials/"
    )


def outreach_contacts_json() -> Path:
    env = os.environ.get("USTORY_OUTREACH_JSON", "").strip()
    if env:
        return Path(env).expanduser()
    for candidate in (
        UPSTORY_HOME / "_all_contacts_for_personalization.json",
        ROOT / "data" / "all-contacts-for-personalization.json",
    ):
        if candidate.is_file():
            return candidate
    return UPSTORY_HOME / "_all_contacts_for_personalization.json"


def wave2_news_csv() -> Path:
    """Clay/news export copied into data/ (gitignored)."""
    env = os.environ.get("USTORY_WAVE2_NEWS_CSV", "").strip()
    if env:
        return Path(env).expanduser()
    preferred = ROOT / "data" / "wave2-company-news-export.csv"
    if preferred.is_file():
        return preferred
    legacy = Path.home() / "Downloads" / (
        "wave-2-unique-companies-unique-companies-Default-view-export-1780587945616.csv"
    )
    return preferred if preferred.exists() else legacy
