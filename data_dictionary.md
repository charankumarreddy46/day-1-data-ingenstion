# Mutual Fund Analytics Data Dictionary

## 1. dim_fund (Fund Dimension)
| Column Name | Data Type | Key Type | Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PK | Unique AMFI verification code identifier | `01_fund_master.csv` |
| `fund_house` | TEXT | | Registered Asset Management Company name | `01_fund_master.csv` |
| `scheme_name` | TEXT | | Complete official fund scheme name | `01_fund_master.csv` |
| `category` | TEXT | | Asset class allocation (e.g. Equity, Debt) | `01_fund_master.csv` |
| `sub_category` | TEXT | | Strategic style classification group | `01_fund_master.csv` |
| `plan` | TEXT | | Investment layout variant (Regular / Direct) | `01_fund_master.csv` |
| `launch_date` | TEXT | | Public inception release date | `01_fund_master.csv` |
| `benchmark` | TEXT | | Evaluated baseline target index portfolio | `01_fund_master.csv` |
| `risk_category` | TEXT | | Structural portfolio risk labeling | `01_fund_master.csv` |

## 2. dim_date (Date/Time Dimension)
| Column Name | Data Type | Key Type | Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `date` | TEXT | PK | Formatted timestamp index (`YYYY-MM-DD`) | Dynamic Generation |
| `year` | INTEGER | | Calendar numerical year index | Dynamic Generation |
| `month` | INTEGER | | Calendar numerical month index | Dynamic Generation |
| `day` | INTEGER | | Numerical day of the month | Dynamic Generation |
| `quarter` | INTEGER | | Financial business tracking quarter (1 - 4) | Dynamic Generation |
| `is_weekend` | INTEGER | | Flag identifier for holiday/weekend tracking | Dynamic Generation |

## 3. fact_nav (Net Asset Value Time-Series Fact)
| Column Name | Data Type | Key Type | Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PK/FK | Target scheme identifier link | `02_nav_history.csv` |
| `date` | TEXT | PK/FK | Transaction processing tracking date | `02_nav_history.csv` |
| `nav` | REAL | | Calculated net asset valuation price | `02_nav_history.csv` |

## 4. fact_transactions (Investor Transaction Metrics Fact)
| Column Name | Data Type | Key Type | Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id`| INTEGER | PK | Auto-incrementing transaction sequence index| Dynamic Generation |
| `investor_id` | TEXT | | Anonymized investor profile tracking code | `08_investor_transactions.csv` |
| `transaction_date`| TEXT | FK | Settlement date linking token | `08_investor_transactions.csv` |
| `amfi_code` | INTEGER | FK | Associated transactional fund link key | `08_investor_transactions.csv` |
| `transaction_type`| TEXT | | Capital action classification enum | `08_investor_transactions.csv` |
| `amount_inr` | REAL | | Gross processed ledger value volume | `08_investor_transactions.csv` |
| `state` | TEXT | | Demographics geography indicator state | `08_investor_transactions.csv` |
| `city` | TEXT | | Local metropolitan market origin city | `08_investor_transactions.csv` |
| `city_tier` | TEXT | | Urbanization grouping code classification | `08_investor_transactions.csv` |
| `age_group` | TEXT | | Generational market segment indexing | `08_investor_transactions.csv` |
| `gender` | TEXT | | Demographics gender processing class | `08_investor_transactions.csv` |
| `annual_income_lakh`| REAL| | Explicit household annual tier income | `08_investor_transactions.csv` |
| `payment_mode` | TEXT | | Digital gateway asset acquisition routing | `08_investor_transactions.csv` |
| `kyc_status` | TEXT | | Compliance validation states enum | `08_investor_transactions.csv` |

## 5. fact_performance (Historical Scheme Performance Fact)
| Column Name | Data Type | Key Type | Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PK/FK | Target schema performance validation link | `07_scheme_performance.csv` |
| `return_1yr_pct` | REAL | | Trailing 12-month net growth metric return | `07_scheme_performance.csv` |
| `return_3yr_pct` | REAL | | Trailing 3-year annualized return profile | `07_scheme_performance.csv` |
| `return_5yr_pct` | REAL | | Trailing 5-year annualized return profile | `07_scheme_performance.csv` |
| `alpha` | REAL | | Risk-adjusted structural outperformance score | `07_scheme_performance.csv` |
| `beta` | REAL | | Volatility benchmark sensitivity ranking | `07_scheme_performance.csv` |
| `sharpe_ratio` | REAL | | Risk-adjusted allocation return profile | `07_scheme_performance.csv` |
| `expense_ratio_pct`| REAL | | Year asset operational tracking costs fee | `07_scheme_performance.csv` |
| `risk_grade` | TEXT | | Qualitative asset assessment risk grade | `07_scheme_performance.csv` |

## 6. fact_aum (Asset Under Management Fact)
| Column Name | Data Type | Key Type | Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `date` | TEXT | PK/FK | Asset declaration reporting date | `03_aum_by_fund_house.csv` |
| `fund_house` | TEXT | PK | Asset Management Company holding entity | `03_aum_by_fund_house.csv` |
| `aum_crore` | REAL | | Consolidated absolute capitalization scaling | `03_aum_by_fund_house.csv` |
| `num_schemes` | INTEGER | | Total active scheme options operated | `03_aum_by_fund_house.csv` |
