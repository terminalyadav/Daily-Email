"""
Universal Email Processor
Replaces all date-specific calculate_*.py scripts.
Fetches from Google Sheets, deduplicates, and saves daily JSON to data/ folder.
"""
import os
import re
import json
import gspread
import pandas as pd
from datetime import date, datetime
from google.oauth2.service_account import Credentials

# ─── Config ──────────────────────────────────────────────────────────────────
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "1Q8Pw_a88RRZZ9dpaREMAgf5b0RqRqSkQdaJsLGWivMw")
SHEET_NAMES    = ["TikTok", "Instagram", "Instagram(Ash)", "Tik-Tok(Ash)"]
KEY_FILE       = os.path.join(os.path.dirname(__file__), "..", "service-account-key.json")
DATA_DIR       = os.path.join(os.path.dirname(__file__), "data")

# When running in GitHub Actions / Render, credentials come from env var
CREDS_JSON_ENV = "GOOGLE_CREDENTIALS_JSON"

# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_credentials():
    creds_json = os.getenv(CREDS_JSON_ENV)
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    if creds_json:
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(creds_json)
            tmp_path = f.name
        creds = Credentials.from_service_account_file(tmp_path, scopes=scopes)
        os.unlink(tmp_path)
        return creds
    elif os.path.exists(KEY_FILE):
        return Credentials.from_service_account_file(KEY_FILE, scopes=scopes)
    else:
        raise FileNotFoundError("No Google credentials found. Set GOOGLE_CREDENTIALS_JSON env var or place service-account-key.json.")


def is_junk_email(email: str) -> bool:
    if not email:
        return True
    email = str(email).lower().strip()
    if "@" not in email or "." not in email or "?" in email:
        return True
    if any(email.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"]):
        return True
    if any(k in email for k in ["sentry", "wixpress", "@2x", "placeholder", "example.com"]):
        return True
    generic = ["sales", "info", "support", "admin", "contact", "enquiries", "jobs",
               "press", "hello", "marketing", "business", "help", "enquiry"]
    local = email.split("@")[0]
    if any(local == p or local.startswith(p + ".") or local.startswith(p + "@") for p in generic):
        return True
    if len(local) > 20:
        if local.count("-") >= 3:
            return True
        hex_chars = re.findall(r"[0-9a-f]", local)
        if len(hex_chars) / len(local) > 0.7 and len(local) > 15:
            return True
    return False


def is_junk_username(username: str) -> bool:
    if not username:
        return True
    username = str(username).strip()
    if re.search(r"\s\d+$", username):
        return True
    if len(username) > 30 and re.search(r"[0-9a-f]{10,}", username.lower()):
        return True
    return False


def clean_email(raw) -> str | None:
    if pd.isna(raw):
        return None
    for part in re.split(r"[,\s;]+", str(raw)):
        part = part.strip()
        if not is_junk_email(part):
            return part
    return None


def find_column(columns, patterns):
    for pattern in patterns:
        for col in columns:
            if str(pattern).lower() == str(col).lower():
                return col
    for pattern in patterns:
        for col in columns:
            if str(pattern).lower() in str(col).lower():
                return col
    return None


def load_data_dir_emails_usernames() -> tuple[set, set]:
    """Load all previously saved JSON records to deduplicate."""
    emails, usernames = set(), set()
    os.makedirs(DATA_DIR, exist_ok=True)
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(DATA_DIR, fname)) as f:
                    data = json.load(f)
                for r in data.get("records", []):
                    if r.get("email"):
                        emails.add(r["email"].lower().strip())
                    if r.get("username"):
                        usernames.add(r["username"].strip())
            except Exception:
                pass
    return emails, usernames


def fetch_from_sheets(credentials) -> list[dict]:
    """Fetch all rows from Google Sheets."""
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SPREADSHEET_ID)
    all_rows = []
    for sheet_name in SHEET_NAMES:
        try:
            ws = sh.worksheet(sheet_name)
            data = ws.get_all_records()
            if not data:
                continue
            df = pd.DataFrame(data)
            user_col  = find_column(df.columns, ["Username", "Profile Name", "Name", "Full Name"])
            email_col = find_column(df.columns, ["Email", "E-mail", "Contact"])
            if not email_col or not user_col:
                continue
            platform = "Instagram" if "Instagram" in sheet_name else "TikTok"
            for _, row in df.iterrows():
                email    = str(row[email_col]).strip() if pd.notna(row[email_col]) else ""
                username = str(row[user_col]).strip()  if pd.notna(row[user_col])  else ""
                all_rows.append({"platform": platform, "username": username, "email": email})
        except Exception as e:
            print(f"  Warning: sheet '{sheet_name}' failed: {e}")
    return all_rows


def process_for_date(target_date: date | None = None) -> dict:
    """
    Main pipeline: fetch → deduplicate → filter → save JSON.
    Returns the day's result dict.
    """
    if target_date is None:
        target_date = date.today()
    date_str = target_date.strftime("%Y-%m-%d")
    out_path  = os.path.join(DATA_DIR, f"{date_str}.json")

    print(f"=== Processing for {date_str} ===")
    print("Loading historical records from data/ ...")
    hist_emails, hist_usernames = load_data_dir_emails_usernames()

    print("Connecting to Google Sheets ...")
    creds = get_credentials()
    raw_rows = fetch_from_sheets(creds)
    print(f"  Fetched {len(raw_rows)} raw rows from sheets.")

    fresh, seen_emails, seen_usernames = [], set(), set()
    for row in raw_rows:
        email    = clean_email(row["email"])
        username = row["username"]
        if is_junk_username(username):
            continue
        if not email:
            continue
        e_low = email.lower()
        if e_low in hist_emails or e_low in seen_emails:
            continue
        if username in hist_usernames or username in seen_usernames:
            continue
        fresh.append({"platform": row["platform"], "username": username, "email": email})
        seen_emails.add(e_low)
        seen_usernames.add(username)

    result = {
        "date":  date_str,
        "total": len(fresh),
        "tiktok_count":    sum(1 for r in fresh if r["platform"] == "TikTok"),
        "instagram_count": sum(1 for r in fresh if r["platform"] == "Instagram"),
        "records": fresh,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"  Saved {len(fresh)} fresh records → {out_path}")
    return result


if __name__ == "__main__":
    process_for_date()
