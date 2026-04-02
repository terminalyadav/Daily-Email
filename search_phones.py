import pandas as pd
import glob
import os
import re

phones = ['3301', '4275', '7752', '8908', '2216']
xlsx_files = glob.glob('/home/ashutosh-yadav/Desktop/Daily Email/**/*.xlsx', recursive=True)

for f in xlsx_files:
    if ".~lock" in f: continue
    try:
        xls = pd.ExcelFile(f)
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            # Search all columns for any of the 4-digit phone suffixes
            mask = df.astype(str).apply(lambda row: row.str.contains('|'.join(phones), na=False).any(), axis=1)
            if mask.any():
                print(f"\nMATCH in {os.path.relpath(f, '/home/ashutosh-yadav/Desktop/Daily Email')} (Sheet: {sheet}):")
                print(df[mask])
    except Exception as e:
        pass
