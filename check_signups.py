import pandas as pd
import glob
import os

emails_to_check = [
    "prochy24@hotmail.com",
    "prochy24@hotmail.con",
    "jennifercollabs10@gmail.com",
    "Katelyn.kiser09@outlook.com",
    "appqueenworkman@gmail.com",
    "patmoraism1@hotmail.com",
    "wellletmetellyou@hotmail.com",
    "jazziefonclara@gmail.com",
    "iamchris064@gmail.com",
]

# Socials status for these emails (to match the order above)
socials = [
    "tiktok (1,364)", # prochy24@hotmail.com
    "-",             # prochy24@hotmail.con
    "tiktok (8,011)", # jennifercollabs10@gmail.com
    "-",             # Katelyn.kiser09@outlook.com
    "tiktok (1,330)", # appqueenworkman@gmail.com
    "tiktok (16,782)", # patmoraism1@hotmail.com
    "-",             # wellletmetellyou@hotmail.com
    "-",             # jazziefonclara@gmail.com
    "instagram (198)", # iamchris064@gmail.com
]

# normalize testing emails
emails_to_check = [e.lower().strip() for e in emails_to_check]

found_emails = {}

# Check all excel files
excel_files = glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/*.xlsx")
for file_path in excel_files:
    file_name = os.path.basename(file_path)
    try:
        # Load all sheets or just the first one? Let's load the whole file
        df = pd.read_excel(file_path)
        # Find all columns that might contain emails
        for col in df.columns:
            # Convert column to string and lower case
            col_data = df[col].astype(str).str.lower().str.strip()
            # Check overlap
            for email in emails_to_check:
                if (col_data == email).any() or col_data.str.contains(email, na=False).any():
                    if email not in found_emails:
                        found_emails[email] = []
                    if file_name not in found_emails[email]:
                        found_emails[email].append(file_name)
    except Exception as e:
        print(f"Error reading {file_name}: {e}")

print("Results:")
for email in emails_to_check:
    if email in found_emails:
        print(f"{email}: Found in {', '.join(found_emails[email])}")
    else:
        print(f"{email}: Not found in any sent email list")

# results will be printed by the script

print("\n--- Summary ---")
# Only count the ones that were found in the sent emails
emails_found_count = len([e for e in emails_to_check if e in found_emails])
emails_not_found_count = len([e for e in emails_to_check if e not in found_emails])

# Also let's check the socials matching those found
found_with_socials = 0
found_without_socials = 0

for i, email in enumerate(emails_to_check):
    if email in found_emails:
        if socials[i] != "-":
            found_with_socials += 1
        else:
            found_without_socials += 1

print(f"Total signups from provided list: {len(emails_to_check)}")
print(f"Signups matching sent emails: {emails_found_count}")
print(f"Signups matching sent emails WITH socials: {found_with_socials}")
print(f"Signups matching sent emails WITHOUT socials: {found_without_socials}")
