import pandas as pd
import glob
import os
import unicodedata
import re

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    text = unicodedata.normalize('NFKD', text)
    return text.lower().strip()

# Load sent emails and scraped data
sent_emails = set()
scraped_only = set()
email_to_file = {}

xlsx_files = glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/*.xlsx") + \
             glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/history/*.xlsx")

for file_path in xlsx_files:
    fname = os.path.basename(file_path).lower()
    if any(k in fname for k in ["ignored", "organized", "signups", "samples", "check", "verify"]):
        continue
    
    is_sent_file = "emails.xlsx" in fname
    try:
        df = pd.read_excel(file_path)
        for col in df.columns:
            if "email" in str(col).lower() or "contact" in str(col).lower():
                col_data = df[col].astype(str).apply(normalize_text)
                emails = set(col_data[col_data.str.contains("@", na=False)])
                for e in emails:
                    if e not in email_to_file:
                        email_to_file[e] = []
                    email_to_file[e].append(fname)
                    if is_sent_file:
                        sent_emails.add(e)
                    else:
                        scraped_only.add(e)
    except Exception as e:
        pass

# Map to store which name/username belongs to which file
name_to_file = {}

for file_path in xlsx_files:
    fname = os.path.basename(file_path).lower()
    if any(k in fname for k in ["ignored", "organized", "signups", "samples", "check", "verify"]):
        continue
    
    is_sent_file = "emails.xlsx" in fname
    try:
        df = pd.read_excel(file_path)
        name_cols = [col for col in df.columns if any(p in str(col).lower() for p in ["username", "name", "profile"])]
        for col in name_cols:
            names = set(df[col].dropna().astype(str).apply(normalize_text))
            for n in names:
                if len(n) < 3: continue
                if n not in name_to_file:
                    name_to_file[n] = []
                name_to_file[n].append(fname)
    except Exception as e:
        pass

def extract_date(fname):
    match = re.search(r'(\d+)(?:st|nd|rd|th)?\s*([a-zA-Z]+)', fname)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return fname

# April 1st signups with names and social data
signups_data = [
    {"email": "ethanw07@icloud.com", "name": "Ethan Warren", "socials": "-"},
    {"email": "vmelonz3@gmail.com", "name": "Quincy Smith", "socials": "-"},
    {"email": "quincybuisnesscontact@gmail.com", "name": "Quincy Smith", "socials": "-"},
    {"email": "tiktokemailjc@gmai.com", "name": "Joseph Crome", "socials": "-"},
    {"email": "innovd04@gmail.com", "name": "Innocent Vezi-Darby", "socials": "tiktok (4,345)"},
    {"email": "zarahfox19@gmail.com", "name": "Zarah fox", "socials": "tiktok (6,135)"},
    {"email": "mengsovandary20@gmail.com", "name": "meng sovandary", "socials": "tiktok (0), instagram (0)"},
    {"email": "caseyjoewilliams97@hotmail.com", "name": "Casey williams", "socials": "-"},
    {"email": "Kayenaatta@gmail.com", "name": "Kayenaat", "socials": "-"},
    {"email": "robertapellanda@hotmaul.it", "name": "Roberta Amadei", "socials": "-"},
    {"email": "voinicrenata@gmail.com", "name": "Renata Matkeviciene", "socials": "instagram (3,678)"},
    {"email": "jordandaleuk@outlook.com", "name": "Jordan Dale", "socials": "instagram (774), twitter (0), tiktok (2,979), youtube (47)"},
    {"email": "justusprice01@icloud.com", "name": "justus price", "socials": "-"},
]

sent_only = []
social_only = []
both = []
organic = []

for item in signups_data:
    email = item["email"]
    name = item["name"]
    socials = item["socials"]
    clean_email = normalize_text(email)
    clean_name = normalize_text(name)
    
    files = email_to_file.get(clean_email, [])
    # If no email match, try deep matching by name
    if not files:
        files = name_to_file.get(clean_name, [])
        if not files:
            # Try fuzzy match on email
            for db_email, db_files in email_to_file.items():
                if clean_email == db_email or clean_email in db_email or db_email in clean_email:
                    files = db_files
                    break
        if not files:
            # Try fuzzy match on name
            for db_name, db_files in name_to_file.items():
                if len(clean_name) > 5 and (clean_name in db_name or db_name in clean_name):
                    files = db_files
                    break
    
    if files:
        is_sent = any("emails.xlsx" in f for f in files)
        is_social = any("emails.xlsx" not in f for f in files)
        
        sent_dates = [extract_date(f) for f in files if "emails.xlsx" in f]
        social_files = [f for f in files if "emails.xlsx" not in f]
        
        if is_sent and is_social:
            both.append((email, name, sent_dates, social_files, socials))
        elif is_sent:
            sent_only.append((email, name, sent_dates, socials))
        else:
            social_only.append((email, name, social_files, socials))
    else:
        organic.append((email, name, socials))

print(f"\n=== APRIL 1ST SIGNUP VERIFICATION ===")
print(f"Total Signups: {len(signups_data)}")
print(f"From Our Emails (Sent): {len(sent_only)}")
print(f"From Socials Only (Scraped DB): {len(social_only)}")
print(f"From Both (Sent & Scraped): {len(both)}")
print(f"Organic/Direct (Unknown Source): {len(organic)}")

from_emails_total = len(sent_only) + len(both)
from_socials_total = len(social_only) + len(both)
print(f"\nTotal from our emails: {from_emails_total}")
print(f"Total in social scraping DB: {from_socials_total}")

print("\n--- Detailed Breakdown ---")

print("\n[FROM OUR EMAILS ONLY]")
for e, n, dates, s in sent_only: 
    print(f"- {e} ({n}) | Socials: {s}\n  Sent on: {', '.join(dates)}")

print("\n[FROM BOTH (Sent & Scraped)]")
for e, n, dates, s_files, s in both: 
    print(f"- {e} ({n}) | Socials: {s}\n  Sent on: {', '.join(dates)}\n  Scraped from: {', '.join(s_files)}")

print("\n[FROM SOCIALS ONLY (Scraped DB)]")
for e, n, s_files, s in social_only: 
    print(f"- {e} ({n}) | Socials: {s}\n  Scraped from: {', '.join(s_files)}")

print("\n[ORGANIC/DIRECT - Not in our DB]")
for e, n, s in organic: 
    print(f"- {e} ({n}) | Socials: {s}")

# === SOCIALS BREAKDOWN ===
print("\n\n=== SOCIAL MEDIA BREAKDOWN ===")
has_socials = [item for item in signups_data if item["socials"] != "-"]
no_socials = [item for item in signups_data if item["socials"] == "-"]
print(f"Signups WITH social profiles listed: {len(has_socials)}")
print(f"Signups WITHOUT social profiles: {len(no_socials)}")

# Check which socials are from our scraped DB
print("\nSocial profiles from our scraped DB:")
for item in has_socials:
    clean_email = normalize_text(item["email"])
    files = email_to_file.get(clean_email, [])
    social_files = [f for f in files if "emails.xlsx" not in f] if files else []
    if social_files:
        print(f"  ✓ {item['name']} ({item['socials']}) - Found in: {', '.join(social_files)}")
    else:
        print(f"  ✗ {item['name']} ({item['socials']}) - NOT in our scraped DB")
