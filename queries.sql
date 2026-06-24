-- Query 1: Top 5 Funds by AUM
SELECT fund_house, MAX(aum_crore) as max_aum 
FROM fact_aum 
GROUP BY fund_house 
ORDER BY max_aum DESC LIMIT 5;

-- Query 2: Average NAV per month for SBI Bluechip (AMFI: 119551)
SELECT strftime('%Y-%m', date) as month, AVG(nav) as avg_nav 
FROM fact_nav 
WHERE amfi_code = 119551 
GROUP BY month;

-- Query 3: Cumulative Investment Value by State
SELECT state, SUM(amount_inr) as total_invested 
FROM fact_transactions 
GROUP BY state 
ORDER BY total_invested DESC;

-- Query 4: Funds with highly cost-effective allocations (Expense Ratio < 1%)
SELECT f.scheme_name, p.expense_ratio_pct 
FROM fact_performance p 
JOIN dim_fund f ON p.amfi_code = f.amfi_code 
WHERE p.expense_ratio_pct < 1.0;

-- Query 5: Transaction volume segmented by payment options
SELECT payment_mode, COUNT(*) as txn_count, SUM(amount_inr) as absolute_volume 
FROM fact_transactions 
GROUP BY payment_mode;

-- Query 6: Risk Grade distribution across Active Portfolios
SELECT risk_grade, COUNT(*) as category_count 
FROM fact_performance 
GROUP BY risk_grade;

-- Query 7: Top Performing Schemes based on highest Alpha return thresholds
SELECT f.scheme_name, p.alpha 
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.alpha DESC LIMIT 5;

-- Query 8: Outperforming schemes ranked by Sharpe Ratio
SELECT f.scheme_name, p.sharpe_ratio 
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.sharpe_ratio DESC LIMIT 5;

-- Query 9: Average Ticket size for SIP vs Lumpsum transactions
SELECT transaction_type, AVG(amount_inr) as average_ticket_size 
FROM fact_transactions 
GROUP BY transaction_type;

-- Query 10: KYC Validation Rates grouped across demographics age metrics
SELECT age_group, kyc_status, COUNT(*) as volume 
FROM fact_transactions 
GROUP BY age_group, kyc_status;
