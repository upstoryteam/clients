"""Shared helpers for Wave 2 Fit Pass sheet → growth brief pipeline."""

from __future__ import annotations

import re
from pathlib import Path

WAVE2_SHEET_ID = "1_uESfrg8Ozu4vP_tpxtfXxPBuZGFidVVuCNAKEMNDNQ"
WAVE2_TAB = "Wave 2 - Fit Pass"
from repo_paths import gcp_service_account_path

SERVICE_ACCOUNT_KEY = gcp_service_account_path()

PILOT_SLUGS = [
    "yendo",
    "mobicip",
    "vitaltrax",
    "zevo",
    "tailor-brands",
    "10adventures",
    "chapter",
    "assort-health",
    "based",
    "floorplans-by-tripleseat",
]

# Legal Name → canonical casual display name
CASUAL_OVERRIDES: dict[str, str] = {
    "Floorplans by Tripleseat": "Merri",
    "Citizen": "Citizen Health",
    "Ciitizen": "Citizen Health",
    "Granted Health": "Granted Health",
    "Medbill AI": "Granted Health",
    "Lasting (acquired by Talkspace)": "Lasting",
    "Marble (Acquired by The Zebra)": "Marble",
    "CatchCorner by Sports Illustrated": "CatchCorner",
    "Diem App": "Diem",
    "OtoZen: Driving and Family Safety App": "OtoZen",
    "Super Unlimited Inc.": "Super Unlimited",
    "Vinovest (Acquired by StartEngine)": "Vinovest",
    "Ivideon. Cloud Video Surveillance": "Ivideon",
    "Carpooll.com": "Carpooll",
    "Faireez inc.": "Faireez",
    "HOMMA Group, Inc": "Homma",
    "Gride Technology": "Gride",
    "1502.app LLC": "1502",
    "Avion  (YC W20)": "Avion",
    "Novoflow (YC X25)": "Novoflow",
    "Pie (pie.org)": "Pie",
    "Riva (sold to Teal HQ)": "Riva",
    "Privacy Labs (now Helm)": "Helm",
    "Credissential Inc. (CSE: WHIP)": "Credissential",
    "FIT:MATCH.ai": "Fit Match",
    "CO:CREATE": "Co:Create",
    "Ahara Med | Ahara Nutrition": "Ahara Med",
    "Sweeten | Sweeten Enterprise": "Sweeten",
    "Houser | Find a Real Home Pro": "Houser",
    "MyAdvocate | Online Estate Planning": "MyAdvocate",
    "BOOMITY|health": "Boomity",
    "ClarityHLTH | Telehealth Comparison |Decision Layer": "Clarity Health",
    "PlacePay powered by Payroc": "PlacePay",
    "Verified ID by Verity": "Verified ID",
    "IvyMedia Corp. GotoBus.com / TakeTours.com": "GotoBus",
    "Freshin'Up App - In-Home Hairstylist Services": "Freshin Up",
    "Safr: Ridesharing As An Extension of Lifestyle": "Safr",
    "The Financial Superapp for the Global Diaspora": "Eversend",
    "Kinside (now part of UrbanSitter)": "Kinside",
    "Olivia AI, Inc. (acquired by Nubank)": "Olivia AI",
    "PetCoach (acquired by Petco)": "PetCoach",
    "Pillar (acquired by Acorns)": "Pillar",
    "docTrackr (acquired by NYSE:IL)": "DocTrackr",
    "TrustedID, Inc. (Acquired by Equifax)": "TrustedID",
    "The Dyrt": "The Dyrt",
    "The Forever AppTM": "Forever",
    "The Realest": "The Realest",
    "The GoodCoin": "GoodCoin",
    "Future Proof Property Intelligence": "Future Proof",
    "Rent FYV- Car Sharing Marketplace": "FYV",
    "#1 AI Virtual Family Office Platform": "WealthCloud360",
    "YAY - New Rider and Driver App": "Yay",
    "Pivit from Olfactive Biosolutions": "Pivit",
    "Expatfile - US Expat Taxes made Simple": "Expatfile",
    "SoyMomo - AI Products for Family Safety": "SoyMomo",
    "Anonabox | Tor Hardware Router | Access Deep Web": "Anonabox",
    "PayByCar": "PayByCar",
    "XP": "XP",
}

# domain → URL slug when casual name collides
DOMAIN_SLUG_OVERRIDES: dict[str, str] = {
    "tulipcremation.com": "tulip-cremation",
    "tulipfertility.com": "tulip-fertility",
}

# casual or legal name → URL slug
SLUG_OVERRIDES: dict[str, str] = {
    "Merri": "floorplans-by-tripleseat",
    "Floorplans by Tripleseat": "floorplans-by-tripleseat",
    "Assort Health": "assort-health",
    "Tailor Brands": "tailor-brands",
    "Book An Artist": "book-an-artist",
    "Bookend AI": "bookend-ai",
    "Blackbird Labs": "blackbird-labs",
    "10Adventures": "10adventures",
    "Citizen Health": "citizen-health",
    "Granted Health": "medbill-ai",
    "CatchCorner": "catchcorner",
    "Super Unlimited": "super-unlimited",
    "OurFamilyWizard": "ourfamilywizard",
}

LEGAL_SUFFIX_RE = re.compile(
    r"\s*,?\s*(LLC|L\.L\.C\.|Inc\.?|Incorporated|Corp\.?|Corporation|Ltd\.?|Limited|"
    r"Co\.?|Company|PLC|P\.L\.C\.|LP|L\.P\.|LLP|L\.L\.P\.|PLLC|P\.L\.L\.C\.|"
    r"Group,?\s+Inc\.?|Holdings|Holdings,?\s+Inc\.?|Adventure,?\s+Inc\.?)\.?\s*$",
    re.IGNORECASE,
)
PAREN_RE = re.compile(r"\s*\([^)]*\)")
NOW_BRAND_RE = re.compile(r"\(now\s+(?:part of\s+)?([^)]+)\)", re.IGNORECASE)
BY_RE = re.compile(r"\s+by\s+.+$", re.IGNORECASE)
FROM_RE = re.compile(r"\s+from\s+.+$", re.IGNORECASE)
POWERED_BY_RE = re.compile(r"\s+powered by\s+.+$", re.IGNORECASE)
DASH_SUFFIX_RE = re.compile(r"\s*[-–—]\s*.+$")
MARK_RE = re.compile(r"[™®]|\bTM\b", re.IGNORECASE)
SLASH_RE = re.compile(r"\s*/\s*")
SMALL_WORDS = {"a", "an", "the", "and", "or", "for", "of", "by", "at", "to", "in", "on"}
UPPER_TOKENS = {"ai", "otc", "ev", "id", "tv", "api", "hr", "md", "llc", "usa", "uk", "vr"}


def _domain_brand(domain: str) -> str:
    stem = domain.split(".", 1)[0].strip()
    stem = stem.replace("-", " ").replace("_", " ")
    return smart_title(stem) if stem else ""


def _looks_like_tagline(name: str) -> bool:
    words = name.split()
    lower = name.lower()
    if name.strip().startswith("#"):
        return True
    if len(words) > 6:
        return True
    if len(words) >= 5 and any(
        token in lower
        for token in (
            "platform",
            "marketplace",
            "intelligence",
            "superapp",
            "virtual",
            "comparison",
            "planning",
            "surveillance",
            "services",
            "extension",
            "diaspora",
        )
    ):
        return True
    if re.search(r"\b(made simple|for the global|for family safety)\b", lower):
        return True
    return False


def smart_title(name: str) -> str:
    name = re.sub(r"\s+", " ", name.strip())
    if not name:
        return name
    if re.search(r"[a-z]", name) and re.search(r"[A-Z]", name) and not name.isupper():
        return name

    words = name.split()
    out: list[str] = []
    for i, word in enumerate(words):
        core = word.strip(".,'\"")
        lower = core.lower()
        if re.fullmatch(r"\d+[a-zA-Z]+", core):
            num = re.match(r"^(\d+)", core).group(1)
            rest = core[len(num) :]
            out.append(num + (rest[:1].upper() + rest[1:].lower() if rest else ""))
            continue
        if lower in UPPER_TOKENS:
            out.append(lower.upper())
        elif lower in SMALL_WORDS and i > 0:
            out.append(lower)
        elif core.isupper() and len(core) <= 4:
            out.append(core)
        else:
            out.append(core[:1].upper() + core[1:].lower() if core else core)
    return " ".join(out)


def strip_parentheticals(name: str) -> str:
    prev = None
    working = name
    while prev != working:
        prev = working
        now = NOW_BRAND_RE.search(working)
        if now:
            return smart_title(now.group(1).strip())
        working = PAREN_RE.sub("", working).strip()
    return re.sub(r"\s+", " ", working).strip()


def casualize_name(name: str, domain: str = "") -> tuple[str, bool]:
    """Return (casual_name, needs_review)."""
    raw = name.strip()
    if not raw:
        return raw, True
    if raw in CASUAL_OVERRIDES:
        return CASUAL_OVERRIDES[raw], False

    needs_review = False
    working = MARK_RE.sub("", raw).strip()

    if _looks_like_tagline(working) and domain:
        brand = _domain_brand(domain)
        if brand:
            return brand, True

    working = strip_parentheticals(working)

    if "|" in working:
        working = working.split("|", 1)[0].strip()
        needs_review = True

    if "/" in working:
        parts = [p.strip() for p in SLASH_RE.split(working) if p.strip()]
        if parts:
            working = parts[0]
            if len(parts) > 1:
                needs_review = True

    working = POWERED_BY_RE.sub("", working).strip()
    working = FROM_RE.sub("", working).strip()
    working = BY_RE.sub("", working).strip()
    working = DASH_SUFFIX_RE.sub("", working).strip()

    if ":" in working and not re.fullmatch(r"[A-Za-z]+:[A-Za-z]+", working.replace(" ", "")):
        left, right = working.split(":", 1)
        if len(left.strip()) <= 24:
            working = left.strip()
        else:
            working = right.strip() or left.strip()
        needs_review = True

    stripped = LEGAL_SUFFIX_RE.sub("", working).strip(" ,.")
    if stripped:
        working = stripped

    working = re.sub(r"\.(com|org|net|io|ai|co)\b", "", working, flags=re.IGNORECASE).strip()
    working = re.sub(r"\s+", " ", working).strip(" ,.")

    if not working:
        if domain:
            return _domain_brand(domain), True
        return smart_title(raw), True

    casual = smart_title(working)

    if len(casual) > 32:
        needs_review = True
    if casual.lower() in {"co", "fit", "app", "inc", "llc"}:
        needs_review = True
    if "(" in raw or "YC" in raw.upper():
        needs_review = needs_review or casual == smart_title(raw)

    return casual, needs_review


def slugify(casual_name: str, domain: str = "", legal_name: str = "") -> str:
    dom = domain.strip().lower()
    dom = re.sub(r"^https?://(www\.)?", "", dom).split("/")[0]
    if dom in DOMAIN_SLUG_OVERRIDES:
        return DOMAIN_SLUG_OVERRIDES[dom]
    for key in (legal_name, casual_name):
        if key and key in SLUG_OVERRIDES:
            return SLUG_OVERRIDES[key]
    base = casual_name or legal_name or domain.split(".", 1)[0]
    s = base.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def row_dict(headers: list[str], row: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for i, h in enumerate(headers):
        out[h] = str(row[i]).strip() if i < len(row) else ""
    return out


def compose_context(row: dict[str, str]) -> str:
    parts: list[str] = []
    clay = row.get("Description (Clay)", "")
    apollo = row.get("Description (Apollo)", "")
    desc = clay if len(clay) >= len(apollo) else apollo
    if desc:
        parts.append(f"Product: {desc}")

    goals = row.get("Inferred Company Goals", "")
    if goals:
        parts.append(f"Direction: {goals}")

    signals: list[str] = []
    for label, key in (
        ("Annual revenue", "Annual Revenue"),
        ("Total funding", "Total Funding"),
        ("Latest funding", "Latest Funding Round Date"),
        ("Headcount T6", "Headcount Growth - T6"),
        ("Headcount T12", "Headcount Growth - T12"),
        ("Engineering", "Engineering"),
        ("Product management", "Product Management"),
    ):
        val = row.get(key, "")
        if val:
            signals.append(f"{label}: {val}")
    if signals:
        parts.append("Signals: " + "; ".join(signals))

    return "\n\n".join(parts)


def compose_recent_news(row: dict[str, str]) -> str:
    goals = row.get("Inferred Company Goals", "")
    if goals:
        return goals
    clay = row.get("Description (Clay)", "")
    apollo = row.get("Description (Apollo)", "")
    return clay if len(clay) >= len(apollo) else apollo


def download_logo_from_url(
    slug: str, url: str, logos_dir: Path, *, force: bool = False
) -> str | None:
    """Download logo to shared/logos/<slug>.<ext>. Returns extension or None."""
    import urllib.request

    if not url:
        return None
    ext = Path(url.split("?", 1)[0]).suffix.lower()
    if ext not in {".png", ".svg", ".jpg", ".jpeg", ".webp"}:
        ext = ".png"
    dest = logos_dir / f"{slug}{ext}"
    if dest.exists() and not force:
        return ext.lstrip(".")
    logos_dir.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "UpstoryBriefBot/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())
        print("logo", dest)
        return ext.lstrip(".")
    except Exception as exc:
        print("logo failed", slug, exc)
        return None
