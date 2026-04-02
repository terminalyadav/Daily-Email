import pandas as pd
import glob
import os
import unicodedata

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    # Normalize unicode characters to NFKD form
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
            # Check for email columns
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
        # print(f"Error reading {fname}: {e}")
        pass

# Signups provided by the user for March 31st
signups = [
    "davidoniyindeugc@gmail.com",
    "david.oniyinde@gmail.com",
    "dhlifestylezinfo@gmail.com",
    "emma.twinmumcontent@gmail.com",
    "scarlettdaisy96x@gmail.com",
    "nextupdon@hotmail.com",
    "juliusadekola1@gmail.com",
    "nom98408@gmail.com",
    "wokilisuccess@gmail.com",
    "eve04white@gmail.com",
    "zainabbakarebusiness@gmail.com",
    "crafternoons.design@outlook.com",
    "haileyhiggins.ugc@gmail.com",
    "undraak0602@gmail.com",
    "kamilajankowsks2006@gmail.com",
    "ngonyotracy586@gmail.com",
    "nelz.z@yahoo.com",
    "Annaaikins@icloud.com",
    "viviane.salvador.2024@gmail.com",
    "pratimagulia26@gmail.com",
    "jiliany.haydee@gmail.com",
    "addiemarkham6@yahoo.com",
    "thatjennzhang@gmail.com",
    "Atinukeolushola24@gmail.com"
]

import re

def extract_date(fname):
    # Extract date patterns like "16th March", "17March", "31March"
    match = re.search(r'(\d+)(?:st|nd|rd|th)?\s*([a-zA-Z]+)', fname)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return fname

# Map to store which name/username belongs to which file
name_to_file = {}

for file_path in xlsx_files:
    fname = os.path.basename(file_path).lower()
    if any(k in fname for k in ["ignored", "organized", "signups", "samples", "check", "verify"]):
        continue
    
    is_sent_file = "emails.xlsx" in fname
    try:
        df = pd.read_excel(file_path)
        # Find username/name columns
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

# Signups data with names
signups_data = [
    {"email": "davidoniyindeugc@gmail.com", "name": "David Oniyinde"},
    {"email": "david.oniyinde@gmail.com", "name": "David"},
    {"email": "dhlifestylezinfo@gmail.com", "name": "DHlifestylez C"},
    {"email": "emma.twinmumcontent@gmail.com", "name": "emma bakes"},
    {"email": "scarlettdaisy96x@gmail.com", "name": "Scarlett Daisy"},
    {"email": "nextupdon@hotmail.com", "name": "Don"},
    {"email": "juliusadekola1@gmail.com", "name": "Julius Phil"},
    {"email": "nom98408@gmail.com", "name": "Rania"},
    {"email": "wokilisuccess@gmail.com", "name": "SUCCESS WOKILI"},
    {"email": "eve04white@gmail.com", "name": "eve white"},
    {"email": "zainabbakarebusiness@gmail.com", "name": "Zainab Bakare"},
    {"email": "crafternoons.design@outlook.com", "name": "Phoebe Fergusson"},
    {"email": "haileyhiggins.ugc@gmail.com", "name": "Hailey Higgins"},
    {"email": "undraak0602@gmail.com", "name": "Undraak"},
    {"email": "kamilajankowsks2006@gmail.com", "name": "Kamila"},
    {"email": "ngonyotracy586@gmail.com", "name": "Tracy Ngonyo"},
    {"email": "nelz.z@yahoo.com", "name": "Nella mahieu"},
    {"email": "Annaaikins@icloud.com", "name": "Annalise Aikins-Andoh"},
    {"email": "viviane.salvador.2024@gmail.com", "name": "viviane"},
    {"email": "pratimagulia26@gmail.com", "name": "PRATIMA GILL"},
    {"email": "jiliany.haydee@gmail.com", "name": "Jiliany Haydee"},
    {"email": "addiemarkham6@yahoo.com", "name": "Addie Markham"},
    {"email": "thatjennzhang@gmail.com", "name": "Jennifer"},
    {"email": "Atinukeolushola24@gmail.com", "name": "ATINUKE OWOEYE"}
]

sent_only = []
social_only = []
both = []
organic = []

for item in signups_data:
    email = item["email"]
    name = item["name"]
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
            both.append((email, name, sent_dates, social_files))
        elif is_sent:
            sent_only.append((email, name, sent_dates))
        else:
            social_only.append((email, name, social_files))
    else:
        organic.append((email, name))

print(f"Total Signups: {len(signups_data)}")
print(f"From Emails Only (Sent): {len(sent_only)}")
print(f"From Socials Only (Scraped): {len(social_only)}")
print(f"From Both (Sent & Scraped): {len(both)}")
print(f"Organic/Direct: {len(organic)}")

print("\n--- Detailed Breakdown ---")

print("\n[Emails Only]")
for e, n, dates in sent_only: 
    print(f"- {e} ({n})\n  Sent on: {', '.join(dates)}")

print("\n[Both Sent & Scraped]")
for e, n, dates, s_files in both: 
    print(f"- {e} ({n})\n  Sent on: {', '.join(dates)}\n  Scraped from: {', '.join(s_files)}")

print("\n[Socials Only (Scraped)]")
for e, n, s_files in social_only: 
    print(f"- {e} ({n})\n  Scraped from: {', '.join(s_files)}")

print("\n[Organic/Direct]")
for e, n in organic: 
    print(f"- {e} ({n})")
