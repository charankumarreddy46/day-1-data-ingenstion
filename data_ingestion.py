import glob
import os
import pandas as pd

def inspect_datasets():
    print("\n=== Phase 1: Scanning Local Files ===")
    csv_files = glob.glob("data/raw/*.csv")
    
    if not csv_files:
        print("⚠️ Notice: data/raw directory is currently empty.")
        return
    
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"\n--- Reading: {file_name} ---")
        try:
            df = pd.read_csv(file_path)
            print(f"Dimensions (Shape): {df.shape}")
            print("Structural Elements (Data Types):")
            print(df.dtypes)
            print("Preview (.head):")
            print(df.head(2))
            
            missing = df.isnull().sum().sum()
            dups = df.duplicated().sum()
            if missing > 0 or dups > 0:
                print(f"⚠️ Data Flag: {missing} missing cells, {dups} duplicate records identified.")
        except Exception as e:
            print(f"Could not open file {file_name}: {e}")

def explore_fund_master(fund_master_path):
    print("\n=== Phase 2: Analyzing Fund Master ===")
    if not os.path.exists(fund_master_path):
        print(f"Skipping lookup: missing reference master template at {fund_master_path}")
        return None
        
    df_master = pd.read_csv(fund_master_path)
    
    for col in ['fund_house', 'category', 'sub_category', 'risk_grade']:
        if col in df_master.columns:
            print(f"Unique keys inside {col}: {df_master[col].dropna().unique()[:5]}")
            
    return df_master

def validate_amfi_codes(df_master, nav_history_path):
    print("\n=== Phase 3: Structural Key Verification ===")
    if df_master is None or not os.path.exists(nav_history_path):
        print("Validation skipped due to missing composite history files.")
        return
        
    df_nav = pd.read_csv(nav_history_path)
    
    master_codes = set(df_master['scheme_code'].unique())
    nav_codes = set(df_nav['scheme_code'].unique())
    
    missing_in_nav = master_codes - nav_codes
    
    print("\n=== Data Quality Summary ===")
    print(f"Schemes listed inside Master File: {len(master_codes)}")
    print(f"Schemes tracked inside History File: {len(nav_codes)}")
    
    if not missing_in_nav:
        print("✅ Success: Every structural tracking code successfully validated.")
    else:
        print(f"❌ Key Inconsistencies Found: {len(missing_in_nav)} item references are missing historical pairs.")
        print(f"Truncated sample mismatch: {list(missing_in_nav)[:5]}")

if __name__ == "__main__":
    inspect_datasets()
    
    # Note: If your assignment provided you with 'fund_master.csv' and 'nav_history.csv' 
    # files, place them inside your data/raw/ folder to execute the validation phase below.
    master_file = "data/raw/fund_master.csv"
    history_file = "data/raw/nav_history.csv"
    
    df_m = explore_fund_master(master_file)
    if df_m is not None:
        validate_amfi_codes(df_m, history_file)
