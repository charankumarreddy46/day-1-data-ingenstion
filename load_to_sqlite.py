import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

def load_database():
    engine = create_engine("sqlite:///bluestock_mf.db")
    
    # Fix: Added encoding="utf-8-sig" to strip out the hidden PowerShell BOM character
    with open("schema.sql", "r", encoding="utf-8-sig") as f:
        schema_ddl = f.read()
        
    with engine.connect() as conn:
        for statement in schema_ddl.split(";"):
            if statement.strip():
                conn.execute(text(statement))
    print("Database structures initialized successfully.")

    print("Generating Time Dimension...")
    nav_df = pd.read_csv("data/processed/02_nav_history_clean.csv")
    unique_dates = pd.to_datetime(nav_df['date'].unique())
    
    dim_date = pd.DataFrame({"date": unique_dates})
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['day'] = dim_date['date'].dt.day
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['is_weekend'] = dim_date['date'].dt.weekday.isin([5, 6]).astype(int)
    dim_date['date'] = dim_date['date'].dt.strftime('%Y-%m-%d')
    dim_date.to_sql("dim_date", engine, if_exists="append", index=False)

    mappings = {
        "data/processed/01_fund_master_clean.csv": "dim_fund",
        "data/processed/02_nav_history_clean.csv": "fact_nav",
        "data/processed/08_investor_transactions_clean.csv": "fact_transactions",
        "data/processed/07_scheme_performance_clean.csv": "fact_performance",
        "data/processed/03_aum_by_fund_house_clean.csv": "fact_aum"
    }

    for path, table in mappings.items():
        df = pd.read_csv(path)
        
        if table == "dim_fund":
            df = df[['amfi_code', 'fund_house', 'scheme_name', 'category', 'sub_category', 'plan', 'launch_date', 'benchmark', 'risk_category']]
        elif table == "fact_performance":
            df = df[['amfi_code', 'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'alpha', 'beta', 'sharpe_ratio', 'expense_ratio_pct', 'risk_grade']]
        elif table == "fact_aum":
            df = df[['date', 'fund_house', 'aum_crore', 'num_schemes']]

        df.to_sql(table, engine, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows into table: {table}")

if __name__ == "__main__":
    load_database()
