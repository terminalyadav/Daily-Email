import pandas as pd
import glob
import os
import unicodedata

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    # Normalize unicode characters to NFKD form
    text = unicodedata.normalize('NFKD', text)
    # Filter out non-ascii characters or keep them? Let's just normalize
    return text.lower().strip()

# Load all sent emails from historical files
sent_emails = set()
# Search in current directory and history directory
xlsx_files = glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/*.xlsx") + \
             glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/history/*.xlsx")

for file_path in xlsx_files:
    if "ignored" in file_path.lower() or "organized" in file_path.lower():
        continue # Skip these
    try:
        df = pd.read_excel(file_path)
        for col in df.columns:
            # Normalize and add to set
            col_data = df[col].astype(str).apply(normalize_text)
            emails = col_data[col_data.str.contains("@", na=False)]
            sent_emails.update(emails)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Add new_contacts.xlsx as well if it's considered part of our database
try:
    df = pd.read_excel("/home/ashutosh-yadav/Desktop/Daily Email/new_contacts.xlsx")
    if 'Email' in df.columns:
        sent_emails.update(df['Email'].astype(str).str.lower().str.strip())
except Exception as e:
    print(f"Error reading new_contacts.xlsx: {e}")

# Data extracted from image (Date: [Emails])
signups_by_date = {
    "28/03/2026": [
        "Ugcwithosayi@gmail.com", "akinmore96@gmail.com", "oonaghrocks@gmail.com", 
        "tracypaulpinto@gmail.com", "ibrahimmallam0305@gmail.com", "oliviainldn@gmail.com", 
        "liviainldn@gmail.com", "dylanfreeburn@googlemail.com", "luyisegarn@gmail.com", 
        "poorvisingh.ugc@gmail.com", "gatkulaniket36@gmail.com", "bradsonthemove@gmail.com", 
        "ayginparto@gmail.com", "hadiyah.collab@gmail.com"
    ],
    "27/03/2026": [
        "prochy24@hotmail.com", "prochy24@hotmail.con", "jennifercollabs10@gmail.com", 
        "Katelyn.kiser09@outlook.com", "appqueenworkman@gmail.com", "patmoraism1@hotmail.com", 
        "wellletmetellyou@hotmail.com", "jazziefonclara@gmail.com", "iamchris064@gmail.com", 
        "ugccreatordeena@gmail.com"
    ],
    "26/03/2026": [
        "creations_by_soph@outlook.com", "sachajaneugc@gmail.com", "lilianchiderah@gmail.com", 
        "faithlola.ugc@gmail.com", "rocks.oonagh@gmail.com", "s.m.r.pinto@hotmail.com"
    ],
    "25/03/2026": [
        "amellerosales@gmail.com", "sharmaashish21102000@gmail.com", "adreanalp@gmail.com", 
        "charlotte.brown14@icloud.com", "hannahugc.uk@gmail.com", "ugcyasmyn@gmail.com", 
        "rachelmcreynolds22@gmail.com"
    ],
    "24/03/2026": [
        "sophieatkinsonugc@gmail.com", "maddy-janea@hotmail.com", "fionaelizaugc@gmail.com", 
        "darlenegatall@gmail.com", "ugcmadi.uk@gmail.com", "matthewtucker18@hotmail.co.uk", 
        "ghennadiev@gmail.com", "ugcwithlily@yahoo.com"
    ],
    "23/03/2026": [
        "ugcwithsophie4@gmail.com", "annaleisepeacock20@gmail.com", "asifachaudhry@hotmail.co.uk", 
        "courtneycollabs@gmail.com", "collinssarah009@gmail.com", "faye.nortontaylor@gmail.com", 
        "hannahlaura.ugc@gmail.com", "monira_islam123@hotmail.com", "collandwithlibby@gmail.com"
    ],
    "21/03/2026": [
        "j_mabbott@hotmail.co.uk", "shai_ugc@outlook.com", "isabelleugc@outlook.com", 
        "sasha.ugc.x@gmail.com", "sophiehowardugc@gmail.com", "katia.pereira98@gmail.com"
    ],
    "20/03/2026": [
        "clionagerrity@outlook.com"
    ],
    "19/03/2026": [
        "nicshannon96@gmail.com", "ugclara9@gmail.com", "andru0611@gmail.com", 
        "beckywoodham97@gmail.com", "hannahshirley.ugc@gmail.com", "chardone.ugc@gmail.com", 
        "lillianadej@gmail.com"
    ],
    "18/03/2026": [
        "jennibark82@btinternet.com", "jennihoneyugc@gmail.com", "ashyugc@gmail.com", 
        "sasha.be.ugc@gmail.com", "charlottemurrayugc@outlook.com", "courtneycollabs@gmail.com", 
        "rachelmcreynolds22@gmail.com"
    ],
    "17/03/2026": [
        "ugcwithjess1@gmail.com", "katieelizabethugc@gmail.com", "beccarosecollabs@gmail.com", 
        "lulalilugc@gmail.com", "collandwithlibby@gmail.com", "ashiyugc@gmail.com", 
        "nicolepinto.ugc@gmail.com", "courtneycollabs@gmail.com", "rachelmcreynolds22@gmail.com"
    ]
}

results = []
for date, emails in signups_by_date.items():
    total = len(emails)
    matches = 0
    matched_list = []
    for email in emails:
        clean_email = normalize_text(email)
        # Check if clean_email is in normalized sent_emails
        if clean_email in sent_emails:
            matches += 1
            matched_list.append(clean_email)
        else:
            # Try a partial match or contain check as a fallback
            found_any = False
            for sent_e in sent_emails:
                if clean_email in sent_e or sent_e in clean_email:
                    matches += 1
                    matched_list.append(sent_e)
                    found_any = True
                    break
    
    results.append({
        "Date": date,
        "Total Signups": total,
        "Our Verified Emails": matches,
        "Percentage": f"{(matches/total)*100:.1f}%" if total > 0 else "0%"
    })

df_results = pd.DataFrame(results)
print(df_results)
