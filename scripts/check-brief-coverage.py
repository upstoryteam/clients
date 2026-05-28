#!/usr/bin/env python3
"""Report growth brief coverage vs outreach JSON (unique companies)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTREACH = Path("/Users/stephendiedrich/Desktop/upstory/_all_contacts_for_personalization.json")
EXCLUDE = {"Brave"}

CO_TO_SLUG = {
    "Stake": "stake",
    "Abby Care": "abby-care",
    "AKKO": "akko",
    "Cloaked": "cloaked",
    "Eternal": "eternal",
    "Dorsia": "dorsia",
    "Caramel": "caramel",
    "Whisker Labs": "whisker-labs",
    "Vinovest (Acquired by StartEngine)": "vinovest",
    "Goldin": "goldin",
    "Poparide": "poparide",
    "Portola": "portola",
    "LegitApp Authentication": "legit-app",
    "WinIt": "winit",
    "Lolli": "lolli",
    "Getmyboat": "getmyboat",
    "Swifto": "swifto",
    "The Arena": "the-arena",
    "Everplans": "everplans",
    "Faireez inc.": "faireez",
    "Foodini": "foodini",
    "Home Alliance": "home-alliance",
    "Ivideon. Cloud Video Surveillance": "ivideon",
    "MealPal": "mealpal",
    "Medbill AI": "medbill-ai",
    "MoboKey": "mobokey",
    "OurFamilyWizard": "ourfamilywizard",
    "Push Health": "push-health",
    "Tandym": "tandym",
    "Tlon": "tlon",
    "Upwards": "upwards",
    "AutosToday": "autostoday",
    "Bambino Sitters": "bambino-sitters",
    "CareClinic": "careclinic",
    "Carpooll.com": "carpooll",
    "Cirtru": "cirtru",
    "CoPilot": "copilot",
    "Modak": "modak",
    "Trustworthy": "trustworthy",
    "HOOPT": "hoopt",
    "Citizen": "citizen-health",
    "Citizen Health": "citizen-health",
}

# ICP sheet Wave 1 (no JSON contacts yet); Leafwell and Citizen excluded from generation
SHEET_WAVE1_SLUGS = [
    "windscribe", "spetz", "super-unlimited", "intrivo", "homma", "lasting",
    "tenantpay", "marble", "tiicker", "catchcorner", "incogni", "diem-app",
    "otozen", "quicktutor", "gofree", "gride-technology", "jiffy", "kaly",
]


def main():
    data = json.loads(OUTREACH.read_text(encoding="utf-8"))
    companies = sorted({r["co"] for r in data if r.get("co")})
    rows = len(data)

    missing = []
    for co in companies:
        if co in EXCLUDE:
            continue
        slug = CO_TO_SLUG.get(co)
        if not slug or not (ROOT / slug / "index.html").is_file():
            missing.append(co)

    print(f"Outreach rows (contacts): {rows}")
    print(f"Unique companies in JSON: {len(companies)}")
    print(f"Excluded (existing client): {', '.join(sorted(EXCLUDE))}")
    print(f"Target briefs from JSON: {len(companies) - len(EXCLUDE)}")
    print(f"Missing briefs: {len(missing)}")
    if missing:
        for co in missing:
            print(f"  - {co}")
    sheet_missing = [s for s in SHEET_WAVE1_SLUGS if not (ROOT / s / "index.html").is_file()]
    print(f"Sheet wave 1 briefs: {len(SHEET_WAVE1_SLUGS) - len(sheet_missing)}/{len(SHEET_WAVE1_SLUGS)}")
    if sheet_missing:
        for s in sheet_missing:
            print(f"  - missing sheet brief: {s}")
    print(f"QA index: run generate-qa-index.py (expect 59 cards)")


if __name__ == "__main__":
    main()
