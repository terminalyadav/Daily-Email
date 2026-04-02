import pandas as pd
import json
import os

files = ["final_creator_contacts.xlsx", "ignored_contacts.xlsx"]
records = []
seen_emails = set()
seen_usernames = set()

for f in files:
    if os.path.exists(f):
        df = pd.read_excel(f)
        email_col = None
        user_col = None
        for col in df.columns:
            col_lower = str(col).lower()
            if "email" in col_lower: email_col = col
            if any(p in col_lower for p in ["username", "name", "profile"]): user_col = col
        
        for _, row in df.iterrows():
            email = str(row[email_col]).strip() if pd.notna(row[email_col]) else ""
            username = str(row[user_col]).strip() if pd.notna(row[user_col]) else ""
            
            if email and email not in seen_emails:
                records.append({"email": email, "username": username, "platform": "Blocklist"})
                seen_emails.add(email)
                seen_usernames.add(username)

print(f"Extracted {len(records)} records from master files.")

out_path = "backend/data/master_blocklist.json"
result = {
    "date": "2000-01-01",
    "total": len(records),
    "records": records
}

with open(out_path, "w") as out:
    json.dump(result, out, indent=2)

print(f"Saved master blocklist to {out_path}!")
