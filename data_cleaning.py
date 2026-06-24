import os
import glob
import pandas as pd
import numpy as np

# Ensure target directory exists
os.makedirs("data/processed", exist_ok=True)

def clean_nav_history():
    print("Cleaning 02_nav_history.csv...")
    if not os.path.exists("02_nav_history.csv"):
        print("❌ Error: 02_nav_history.csv not found in the current directory!")
        return
        
    df = pd.read_csv("02_nav_history.csv")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['amfi_code', 'date'])
    df = df.drop_duplicates(subset=['amfi_code', 'date'])
    df = df[df['nav'] > 0]
    
    filled_dfs = []
    for amfi, group in df.groupby('amfi_code'):
        group = group.set_index('date')
        full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
        group = group.reindex(full_range)
        group['amfi_code'] = amfi
        group['nav'] = group['nav'].ffill()
        group = group.reset_index().rename(columns={'index': 'date'})
        filled_dfs.append(group)
        
    df_clean = pd.concat(filled_dfs, ignore_index=True)
    df_clean.to_csv("data/processed/02_nav_history_clean.csv", index=False)
    print(f"-> Saved nav_history_clean.csv. Shape: {df_clean.shape}")

def clean_investor_transactions():
    print("Cleaning 08_investor_transactions.csv...")
    if not os.path.exists("08_investor_transactions.csv"):
        print("❌ Error: 08_investor_transactions.csv not found!")
        return
        
    df = pd.read_csv("08_investor_transactions.csv")
    df['transaction_type'] = df['transaction_type'].str.strip().str.capitalize()
    df = df[df['amount_inr'] > 0]
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    valid_kyc = ['Verified', 'Pending', 'Rejected']
    df['kyc_status'] = df['kyc_status'].str.strip().str.capitalize()
    df.loc[~df['kyc_status'].isin(valid_kyc), 'kyc_status'] = 'Pending'
    
    df.to_csv("data/processed/08_investor_transactions_clean.csv", index=False)
    print(f"-> Saved investor_transactions_clean.csv. Shape: {df.shape}")

def clean_scheme_performance():
    print("Cleaning 07_scheme_performance.csv...")
    if not os.path.exists("07_scheme_performance.csv"):
        print("❌ Error: 07_scheme_performance.csv not found!")
        return
        
    df = pd.read_csv("07_scheme_performance.csv")
    numeric_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct', 'alpha', 'beta', 'sharpe_ratio', 'expense_ratio_pct']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    df = df[(df['expense_ratio_pct'] >= 0.1) & (df['expense_ratio_pct'] <= 2.5)]
    df.to_csv("data/processed/07_scheme_performance_clean.csv", index=False)
    print(f"-> Saved scheme_performance_clean.csv. Shape: {df.shape}")

def process_remaining_datasets():
    print("Processing remaining datasets...")
    remaining = {
        "01_fund_master.csv": "01_fund_master_clean.csv",
        "03_aum_by_fund_house.csv": "03_aum_by_fund_house_clean.csv",
        "04_monthly_sip_inflows.csv": "04_monthly_sip_inflows_clean.csv",
        "05_category_inflows.csv": "05_category_inflows_clean.csv",
        "06_industry_folio_count.csv": "06_industry_folio_count_clean.csv",
        "09_portfolio_holdings.csv": "09_portfolio_holdings_clean.csv",
        "10_benchmark_indices.csv": "10_benchmark_indices_clean.csv"
    }
    for source, target in remaining.items():
        if os.path.exists(source):
            df = pd.read_csv(source)
            df.columns = df.columns.str.strip()
            df.to_csv(f"data/processed/{target}", index=False)
            print(f"-> Staged {target}")
        else:
            print(f"⚠️ Warning: {source} not found in current folder, skipping.")

if __name__ == "__main__":
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    process_remaining_datasets()
