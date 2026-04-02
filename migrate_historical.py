"""
migrate_historical.py
Converts all existing daily Excel files (16th March → 2 April) into
JSON files in the data/ folder so the dashboard shows historical data too.
Run once: python migrate_historical.py
"""
import os
import re
import json
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Map filename → ISO date
EXCEL_DATE_MAP = {
    "16th March emails.xlsx":  "2026-03-16",
    "17March emails.xlsx":     "2026-03-17",
    "18March emails.xlsx":     "2026-03-18",
    "18March_fresh_data.xlsx": None,          # skip (duplicate of 18th)
    "19March emails.xlsx":     "2026-03-19",
    "20March emails.xlsx":     "2026-03-20",
    "21March emails.xlsx":     "2026-03-21",
    "22March emails.xlsx":     "2026-03-22",
    "24March emails.xlsx":     "2026-03-24",
    "25March emails.xlsx":     "2026-03-25",
    "26March emails.xlsx":     "2026-03-26",
    "27March emails.xlsx":     "2026-03-27",
    "28March emails.xlsx":     "2026-03-28",
    "29March emails.xlsx":     "2026-03-29",
    "30March emails.xlsx":     "2026-03-30",
    "31March emails.xlsx":     "2026-03-31",
    "1April emails.xlsx":      "2026-04-01",
    "2April emails.xlsx":      "2026-04-02",
}


def detect_platform(df, fname):
    """Guess platform from columns or filename."""
    cols_lower = [c.lower() for c in df.columns]
    if "platform" in cols_lower:
        return None  # will read per row
    if "tiktok" in fname.lower():
        return "TikTok"
    if "instagram" in fname.lower():
        return "Instagram"
    return "Unknown"


def is_junk_email(email):
    if not email:
        return True
    email = str(email).lower().strip()
    if "@" not in email or "." not in email or "?" in email:
        return True
    if any(email.endswith(e) for e in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"]):
        return True
    if any(k in email for k in ["sentry", "wixpress", "@2x", "placeholder", "example.com"]):
        return True
    generic = ["sales", "info", "support", "admin", "contact", "enquiries", "jobs",
               "press", "hello", "marketing", "business", "help", "enquiry"]
    local = email.split("@")[0]
    if any(local == p for p in generic):
        return True
    return False


def convert_file(fname, date_str):
    fpath = os.path.join(BASE_DIR, fname)
    if not os.path.exists(fpath):
        print(f"  SKIP (not found): {fname}")
        return

    df = pd.read_excel(fpath)
    cols_lower = {c.lower(): c for c in df.columns}

    email_col    = next((cols_lower[k] for k in cols_lower if "email" in k), None)
    username_col = next((cols_lower[k] for k in cols_lower if any(p in k for p in ["username", "name", "profile"])), None)
    platform_col = cols_lower.get("platform")

    records = []
    for _, row in df.iterrows():
        email    = str(row[email_col]).strip()    if email_col    and pd.notna(row[email_col])    else ""
        username = str(row[username_col]).strip() if username_col and pd.notna(row[username_col]) else ""
        platform = str(row[platform_col]).strip() if platform_col and pd.notna(row[platform_col]) else "Unknown"

        if is_junk_email(email):
            continue
        records.append({"platform": platform, "username": username, "email": email})

    tiktok_c    = sum(1 for r in records if r["platform"] == "TikTok")
    instagram_c = sum(1 for r in records if r["platform"] == "Instagram")

    result = {
        "date":             date_str,
        "total":            len(records),
        "tiktok_count":     tiktok_c,
        "instagram_count":  instagram_c,
        "records":          records,
        "generated_at":     datetime.utcnow().isoformat() + "Z",
    }
    out_path = os.path.join(DATA_DIR, f"{date_str}.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"  ✓ {fname} → {date_str}.json  ({len(records)} records)")


if __name__ == "__main__":
    print("=== Historical Data Migration ===")
    for fname, date_str in EXCEL_DATE_MAP.items():
        if date_str is None:
            print(f"  SKIP (manual exclusion): {fname}")
            continue
        convert_file(fname, date_str)
    print("\nDone! Check the data/ folder.")
