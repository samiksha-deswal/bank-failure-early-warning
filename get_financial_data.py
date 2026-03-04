import requests
import pandas as pd
import time

print("Loading failed bank certificates...")

# ── Load failures data ────────────────────────────────────────────────────
failures = pd.read_csv('bank_failures.csv')
recent_failures = failures[failures['FAILYR'] >= 2000].copy()
failed_certs = recent_failures['CERT'].dropna().astype(int).tolist()
print(f"Found {len(failed_certs)} failures from 2000-2023")

# ── Pull financial data from FDIC API ─────────────────────────────────────
# These are the key early warning indicators
fields = "CERT,REPDTE,ASSET,DEP,LNLSNET,RBCRWAJ,ROA,NETINC,NPERFV"

all_data = []
sample_certs = failed_certs[:100]  # Start with 100 banks

print(f"Fetching financial data for {len(sample_certs)} failed banks...")

for i, cert in enumerate(sample_certs):
    url = (
        f"https://banks.data.fdic.gov/api/financials"
        f"?filters=CERT%3A{cert}"
        f"&fields={fields}"
        f"&limit=50"
        f"&sort_by=REPDTE"
        f"&sort_order=ASC"
        f"&output=json"
    )

    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            for item in data['data']:
                row = item['data']
                row['FAILED'] = 1
                all_data.append(row)
        
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{len(sample_certs)} banks fetched...")
    
    except Exception as e:
        print(f"  Error on cert {cert}: {e}")
    
    time.sleep(0.3)

# ── Save ──────────────────────────────────────────────────────────────────
if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv('bank_financials.csv', index=False)
    print(f"\nSuccess! Saved {len(df)} quarterly records")
    print(f"Covering {df['CERT'].nunique()} unique banks")
    print(f"\nColumns available: {df.columns.tolist()}")
    print(f"\nSample data:")
    print(df[['CERT','REPDTE','ASSET','DEP','ROA','RBCRWAJ']].head(10))
else:
    print("No data retrieved — check connection")