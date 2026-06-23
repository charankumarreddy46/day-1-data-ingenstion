import os
import pandas as pd
import requests

os.makedirs("data/raw", exist_ok=True)

def fetch_and_save_nav(scheme_code, filename):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching data for scheme code: {scheme_code}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        meta = data.get("meta", {})
        print(f"Successfully connected to: {meta.get('scheme_name', 'Unknown Scheme')}")
        
        nav_list = data.get("data", [])
        df = pd.DataFrame(nav_list)
        
        if not df.empty:
            df['scheme_code'] = scheme_code
            df['scheme_name'] = meta.get('scheme_name')
            
            output_path = f"data/raw/{filename}.csv"
            df.to_csv(output_path, index=False)
            print(f"Saved into -> {output_path} ({len(df)} rows found)\n")
        else:
            print(f"⚠️ No dataset records inside scheme {scheme_code}\n")
            
    except Exception as e:
        print(f"❌ Connection error for scheme {scheme_code}: {e}\n")

if __name__ == "__main__":
    # Fetch HDFC Target
    fetch_and_save_nav(125497, "hdfc_top_100_raw")
    
    # Fetch 5 Core Bluechip Targets
    bluechip_schemes = {
        119551: "sbi_bluechip",
        120503: "icici_bluechip",
        118632: "nippon_large_cap",
        119092: "axis_bluechip",
        120841: "kotak_bluechip"
    }
    
    for code, file_label in bluechip_schemes.items():
        fetch_and_save_nav(code, f"{file_label}_raw")
