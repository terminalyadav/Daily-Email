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

# Load sent emails from files ending in 'emails.xlsx'
sent_emails = set()
scraped_only = set()

xlsx_files = glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/*.xlsx") + \
             glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/history/*.xlsx")

for file_path in xlsx_files:
    fname = os.path.basename(file_path).lower()
    if "ignored" in fname or "organized" in fname or "signups" in fname:
        continue
    
    is_sent_file = "emails.xlsx" in fname
    try:
        df = pd.read_excel(file_path)
        for col in df.columns:
            col_data = df[col].astype(str).apply(normalize_text)
            emails = set(col_data[col_data.str.contains("@", na=False)])
            if is_sent_file:
                sent_emails.update(emails)
            else:
                scraped_only.update(emails)
    except Exception as e:
        pass

# Signups provided by the user for March 30th
signups = [
    "karmkmayard@gmail.com",
    "albertjamescorral@gmail.com",
    "kaleneg10@gmail.com",
    "lily.lasley120906@gmail.com",
    "laurenjoycebush@gmail.com",
    "becaaelizabeth@aol.com",
    "hairhealing2025@gmail.com",
    "raine.ugc.creative@gmail.com",
    "june.sadler65@gmail.com",
    "milliemacfamily@gmail.com",
    "ms.deeee@icloud.com",
    "maddiehobbs2007@gmail.com",
    "nicollewhiteugc@outlook.com",
    "leanne.green21@yahoo.com",
    "richieruyy@gmail.com",
    "fyzanzzz@gmail.com",
    "brookevintage0@gmail.com",
    "d1dotnayah@gmail.com",
    "annaosborneugc@gmail.com",
    "mohamedmazhar122006@gmail.com"
]

results = []
sent_matches = {} # email -> filename
social_matches = {}
others = []

# Map to store which email belongs to which file
email_to_file = {}

for file_path in xlsx_files:
    fname = os.path.basename(file_path).lower()
    if "ignored" in fname or "organized" in fname or "signups" in fname:
        continue
    
    is_sent_file = "emails.xlsx" in fname
    try:
        df = pd.read_excel(file_path)
        for col in df.columns:
            col_data = df[col].astype(str).apply(normalize_text)
            emails = set(col_data[col_data.str.contains("@", na=False)])
            for e in emails:
                if e not in email_to_file:
                    email_to_file[e] = []
                email_to_file[e].append(fname)
    except Exception as e:
        pass

for email in signups:
    clean_email = normalize_text(email)
    found = False
    if clean_email in email_to_file:
        files = email_to_file[clean_email]
        is_sent = any("emails.xlsx" in f for f in files)
        if is_sent:
            sent_matches[email] = files
        else:
            social_matches[email] = files
        found = True
    else:
        # Fallback partial match
        for db_email, files in email_to_file.items():
            if clean_email in db_email or db_email in clean_email:
                is_sent = any("emails.xlsx" in f for f in files)
                if is_sent:
                    sent_matches[email] = files
                else:
                    social_matches[email] = files
                found = True
                break
    
    if not found:
        others.append(email)

print(f"Total Signups: {len(signups)}")
print(f"From Emails (Sent): {len(sent_matches)}")
print(f"From Socials (Scraped but not Sent): {len(social_matches)}")
print(f"Others (Organic/Direct): {len(others)}")

print("\nFrom Emails (with Source Files):")
for e, files in sent_matches.items():
    print(f"- {e} (Source: {', '.join(files)})")

print("\nFrom Socials (with Source Files):")
for e, files in social_matches.items():
    print(f"- {e} (Source: {', '.join(files)})")

print("\nOthers:")
for e in others:
    print(f"- {e}")
