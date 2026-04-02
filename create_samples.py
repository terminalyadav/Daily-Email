import pandas as pd
import os

def create_sample_files():
    # TikTok Sample
    df_tiktok = pd.DataFrame({
        "Username": ["tk_user1", "tk_user2", "tk_user3"],
        "Name": ["John Doe 🚀", "Jane Smith", "Duplicate User"],
        "Email": ["john@example.com", "jane@example.com", "dup@example.com"],
        "Followers": [1000, 2000, 500]
    })
    
    # Instagram Sample
    df_insta = pd.DataFrame({
        "Username": ["ig_user1", "ig_user2"],
        "Name": ["Alice Wonderland", "jane smith"], # lowercase name for testing
        "Email": ["alice@example.com", "jane@example.com"], # Duplicate email
        "Bio": ["Hello", "World"]
    })
    
    # Instagram2 Sample
    df_insta2 = pd.DataFrame({
        "Username": ["ig_user3", "ig_user4"],
        "Name": ["🚀 Emoji Name", ""], # Name empty or emoji only
        "Email": ["emoji@example.com", ""], # Empty email
        "Profile URL": ["url1", "url2"]
    })
    
    df_tiktok.to_excel("TikTok.xlsx", index=False)
    df_insta.to_excel("Instagram.xlsx", index=False)
    df_insta2.to_excel("Instagram2.xlsx", index=False)
    print("Sample files created.")

if __name__ == "__main__":
    create_sample_files()
