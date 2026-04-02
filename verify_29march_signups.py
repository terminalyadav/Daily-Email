import pandas as pd
import os

# Emails provided by the user
signup_emails = [
    "maebelilss@gmail.com",
    "rose@hansenaudio.co.uk",
    "Busolacreates@gmail.com",
    "ooluwabusola2@gmail.com",
    "asiapaintsart@gmail.com",
    "saavanvaram@gmail.com",
    "chaoscoffeeandcuddles@gmail.com",
    "risingfromzero1@gmail.com",
    "Tanyabailey86@outlook.com",
    "jaydah.tauarua3@gmail.com",
    "ahmedmiah5303@gmail.com",
    "tiwatemi16@gmail.com",
    "noestraa@icloud.com",
    "vab92.ugc@outlook.com",
    "satpheang68@gmail.com",
    "tayjarnn@outlook.com",
    "ivaklocked@gmail.com"
]

# Clean signup emails
signup_emails = [e.lower().strip() for e in signup_emails]

# Daily email files to check against
daily_files = [
    "29March emails.xlsx",
    "28March emails.xlsx",
    "27March emails.xlsx",
    "26March emails.xlsx",
    "25March emails.xlsx",
    "24March emails.xlsx",
    "22March emails.xlsx",
    "21March emails.xlsx",
    "20March emails.xlsx",
    "19March emails.xlsx",
    "18March emails.xlsx",
    "17March emails.xlsx",
    "16th March emails.xlsx"
]

matches = []

print("--- Verifying Signup Origination ---")
for f in daily_files:
    if os.path.exists(f):
        try:
            df = pd.read_excel(f)
            email_col = None
            for col in df.columns:
                if "email" in str(col).lower():
                    email_col = col
                    break
            
            if email_col:
                found_emails = df[email_col].dropna().astype(str).str.lower().str.strip().tolist()
                for se in signup_emails:
                    if se in found_emails:
                        matches.append({"email": se, "file": f})
                        # Remove from list to avoid duplicate counting if in multiple files (though unlikely given deduplication)
                        # signup_emails.remove(se) 
        except Exception as e:
            print(f"Error reading {f}: {e}")

# Deduplicate matches (in case an email is in multiple files, which shouldn't happen but good to be safe)
seen = set()
unique_matches = []
for m in matches:
    if m["email"] not in seen:
        unique_matches.append(m)
        seen.add(m["email"])

print(f"\nTotal Signups Checked: {len(signup_emails)}")
print(f"Total Matches Found: {len(unique_matches)}")

if unique_matches:
    print("\nMatches Breakdown:")
    for m in unique_matches:
        print(f" - {m['email']} (Found in: {m['file']})")
else:
    print("\nNo matches found in our email lists.")
