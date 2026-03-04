# bank-failure-early-warning
AI-assisted early warning system for U.S. bank failures using FDIC data - scorecard, governance framework, and audit trail

U.S. Bank Failure Early Warning System
An AI-assisted analysis of 4,114 FDIC bank failures (1934–2024), an early warning scorecard built on quarterly financial data, and a governance framework for AI monitoring in regulated financial institutions.
By Samiksha Deswal | Economics • Finance • AI Governance

Project Overview
This project demonstrates how public regulatory data can be used to build and govern an AI-assisted early warning system for bank failures. It is structured in three layers mirroring a real production system: descriptive analysis, predictive scoring, and governance framework.
Repository Structure
analysis.py — Descriptive analysis of 90 years of FDIC failure data (Charts 1–4)
scorecard.py — Early warning scorecard using pre-failure financial indicators (Charts 5–8)
governance.py — AI agent workflow diagram and audit trail system (Charts 9–10)
get_financial_data.py — FDIC API data pipeline for quarterly call report data
bank_failures.csv — Source data from FDIC failures database
bank_financials.csv — Quarterly financial data for 100 failed banks
audit_trail.csv — Full audit log: 417 scored records with flags and risk levels
audit_sample.json — Sample audit output in JSON format

Key Findings
4,114 bank failures since 1934, costing $294 billion in FDIC resolution costs
Three distinct crisis clusters: S&L Crisis (volume), GFC (cost), 2023 Regional (asset size)
ROA crosses zero at exactly 6 quarters before failure on average — a detectable early warning signal
Non-performing assets accelerate exponentially in the final 4 quarters before failure
Average risk score rises 4x: from 1.15 at 8 quarters before failure to 4.70 in the final quarter
69 of 417 pre-failure quarterly records flagged as requiring human review

Data Sources
FDIC Bank Failures Database: banks.data.fdic.gov/api/failures
FDIC Financials API: banks.data.fdic.gov/api/financials
Both datasets are public, free, and updated regularly by the FDIC

How to Run
Requirements
Python 3.9+ with: pandas, matplotlib, seaborn, requests
pip3 install pandas matplotlib seaborn requests
Steps
Download bank_failures.csv from the FDIC link above
Run get_financial_data.py to pull quarterly financials via API
Run analysis.py for descriptive charts (Charts 1–4)
Run scorecard.py for early warning analysis (Charts 5–8)
Run governance.py for workflow diagram and audit trail (Charts 9–10)

Governance Framework
The governance workflow (Chart 9) implements a six-layer architecture: Data → Ingestion & Validation → Feature Engineering → Scoring → Human Review Gate → Action → Audit Log. The design is informed by the Federal Reserve's SR 11-7 model risk management guidance.
Key governance principles implemented: full explainability of every flag, human review gate before any action, immutable audit trail for every decision, and no black-box scoring.
Limitations
Retrospective analysis only — not tested on out-of-sample data
Capital ratio data quality issues limit HIGH/CRITICAL flag generation for older records
No healthy bank comparator group — false positive rate not yet measured
Four indicators only — production system would require additional features




This project was built as part of a portfolio demonstrating AI-assisted financial analysis and governance. All data is public. All code is original. Feedback welcome.
