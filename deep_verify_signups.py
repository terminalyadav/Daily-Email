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

# Missing signups with details
missing_data = [
    {"name": "Karmély", "email": "karmkmayard@gmail.com", "phone": "2148303301"},
    {"name": "Lilian Maxine Lasley", "email": "lily.lasley120906@gmail.com", "phone": "2607054275"},
    {"name": "diane suzanne", "email": "ms.deeee@icloud.com", "phone": "09496737752"},
    {"name": "Maddie", "email": "maddiehobbs2007@gmail.com", "phone": "07795468908"},
    {"name": "Mohamed mazhar", "email": "mohamedmazhar122006@gmail.com", "phone": "+201017322216"}
]

xlsx_files = glob.glob("/home/ashutosh-yadav/Desktop/Daily Email/**/*.xlsx", recursive=True)

found_results = {}

for file_path in xlsx_files:
    if ".~lock" in file_path:
        continue
    try:
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            for col in df.columns:
                col_data = df[col].astype(str).str.lower()
                for data in missing_data:
                    # Check Phone (strip non-numeric for comparison)
                    clean_phone = re.sub(r'\D', '', data['phone'])
                    if clean_phone:
                        mask_phone = col_data.apply(lambda x: clean_phone in re.sub(r'\D', '', str(x)))
                    else:
                        mask_phone = pd.Series([False]*len(df))
                    
                    # Check Name (partial)
                    first_name = unicodedata.normalize('NFKD', data['name'].split()[0]).encode('ascii', 'ignore').decode('ascii').lower()
                    mask_name = col_data.apply(lambda x: first_name in unicodedata.normalize('NFKD', str(x)).encode('ascii', 'ignore').decode('ascii').lower())
                    
                    # Check Email (exact and username)
                    username = data['email'].split("@")[0].lower()
                    mask_email = col_data.str.contains(username, na=False)
                    
                    combined_mask = mask_phone | mask_name | mask_email
                    
                    if combined_mask.any():
                        matches = df[combined_mask]
                        key = data['email']
                        if key not in found_results:
                            found_results[key] = []
                        found_results[key].append({
                            "file": os.path.relpath(file_path, "/home/ashutosh-yadav/Desktop/Daily Email"),
                            "sheet": sheet_name,
                            "column": col,
                            "matched_value": matches[col].iloc[0],
                            "row": matches.to_dict('records')[0]
                        })
    except Exception as e:
        pass

for data in missing_data:
    email = data['email']
    if email in found_results:
        print(f"\nPOSSIBLE MATCHES FOR {data['name']} ({email}):")
        for res in found_results[email]:
            print(f"  File: {res['file']}, Col: {res['column']}, Value: {res['matched_value']}")
            print(f"  Context: {res['row']}")
    else:
        print(f"\nNO MATCH FOUND FOR {data['name']} ({email})")
