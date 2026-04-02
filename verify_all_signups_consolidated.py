import pandas as pd
import glob
import os
import unicodedata

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    text = unicodedata.normalize('NFKD', text)
    return text.lower().strip()

# Load all sent emails from historical files
sent_emails = set()
# Search in current directory and history directory
xlsx_files = glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/*.xlsx") + \
             glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/history/*.xlsx")

for file_path in xlsx_files:
    # Skip files that aren't daily reports
    fname = os.path.basename(file_path).lower()
    if any(k in fname for k in ["ignored", "organized", "new_contacts", "instagram", "tiktok", "sample", "final_creator"]):
        continue
    
    try:
        df = pd.read_excel(file_path)
        for col in df.columns:
            if "email" in str(col).lower():
                emails = df[col].dropna().astype(str).apply(normalize_text)
                sent_emails.update(emails)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Data (Date: [Emails]) - Updated to include 29th March
signups_by_date = {
    "29/03/2026": [
        "maebelilss@gmail.com", "rose@hansenaudio.co.uk", "Busolacreates@gmail.com",
        "ooluwabusola2@gmail.com", "asiapaintsart@gmail.com", "saavanvaram@gmail.com",
        "chaoscoffeeandcuddles@gmail.com", "risingfromzero1@gmail.com", "Tanyabailey86@outlook.com",
        "jaydah.tauarua3@gmail.com", "ahmedmiah5303@gmail.com", "tiwatemi16@gmail.com",
        "noestraa@icloud.com", "vab92.ugc@outlook.com", "satpheang68@gmail.com",
        "tayjarnn@outlook.com", "ivaklocked@gmail.com"
    ],
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
for date in sorted(signups_by_date.keys(), reverse=True):
    emails = signups_by_date[date]
    total = len(emails)
    matches = 0
    for email in emails:
        if normalize_text(email) in sent_emails:
            matches += 1
    
    results.append({
        "Date": date,
        "Total Signups": total,
        "Our Emails": matches,
        "Origination %": f"{(matches/total)*100:.1f}%" if total > 0 else "0.0%"
    })

df_results = pd.DataFrame(results)
print("\n--- Consolidated Signup Verification ---")
print(df_results.to_string(index=False))

total_all_signups = sum(r['Total Signups'] for r in results)
total_all_matches = sum(r['Our Emails'] for r in results)
print(f"\nOVERALL SUMMARY:")
print(f"Total Signups Across All Dates: {total_all_signups}")
print(f"Total Identified as Our Emails: {total_all_matches}")
print(f"Overall Origination Rate: {(total_all_matches/total_all_signups)*100:.1f}%")
