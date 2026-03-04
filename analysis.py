import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Load ──────────────────────────────────────────────────────────────────
df = pd.read_csv('bank_failures.csv')

# ── Clean ─────────────────────────────────────────────────────────────────
df['FAILDATE'] = pd.to_datetime(df['FAILDATE'], errors='coerce')
df['FAILYR']   = pd.to_numeric(df['FAILYR'],   errors='coerce')
df['QBFASSET'] = pd.to_numeric(df['QBFASSET'], errors='coerce')
df['QBFDEP']   = pd.to_numeric(df['QBFDEP'],   errors='coerce')
df['COST']     = pd.to_numeric(df['COST'],     errors='coerce')

# ── Summary ───────────────────────────────────────────────────────────────
print("=== DATASET OVERVIEW ===")
print(f"Total bank failures: {len(df)}")
print(f"Year range: {int(df['FAILYR'].min())} – {int(df['FAILYR'].max())}")
print(f"Total FDIC cost ($ thousands): ${df['COST'].sum():,.0f}")

# ── Chart 1: Failures per year ────────────────────────────────────────────
failures_by_year = df.groupby('FAILYR').size().reset_index(name='count')

plt.figure(figsize=(14, 5))
plt.bar(failures_by_year['FAILYR'], failures_by_year['count'], color='steelblue')
plt.axvspan(1986, 1995, alpha=0.15, color='red',    label='S&L Crisis')
plt.axvspan(2008, 2013, alpha=0.15, color='orange', label='GFC')
plt.axvspan(2022, 2024, alpha=0.15, color='purple', label='2023 Regional Crisis')
plt.title('U.S. Bank Failures by Year (1934–2024)', fontsize=14, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Number of Failures')
plt.legend()
plt.tight_layout()
plt.savefig('chart1_failures_by_year.png', dpi=150)
plt.show()
print("Chart 1 saved.")

# ── Chart 2: Top 15 states by failures ───────────────────────────────────
top_states = df['PSTALP'].value_counts().head(15)

plt.figure(figsize=(12, 5))
top_states.plot(kind='bar', color='steelblue')
plt.title('Top 15 States by Bank Failures', fontsize=14, fontweight='bold')
plt.xlabel('State')
plt.ylabel('Number of Failures')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('chart2_top_states.png', dpi=150)
plt.show()
print("Chart 2 saved.")

# ── Chart 3: FDIC resolution cost over time ───────────────────────────────
cost_by_year = df.groupby('FAILYR')['COST'].sum().reset_index()

plt.figure(figsize=(14, 5))
plt.fill_between(cost_by_year['FAILYR'], cost_by_year['COST'],
                 color='tomato', alpha=0.6)
plt.title('Total FDIC Resolution Cost by Year ($ Thousands)',
          fontsize=14, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Cost ($ Thousands)')
plt.tight_layout()
plt.savefig('chart3_fdic_cost.png', dpi=150)
plt.show()
print("Chart 3 saved.")

# ── Chart 4: Asset size of failed banks ───────────────────────────────────
era_map = {
    'S&L Crisis (1986–1995)' : (1986, 1995),
    'GFC (2008–2013)'        : (2008, 2013),
    'Post-GFC (2014–2021)'   : (2014, 2021),
    '2023 Regional (2022+)'  : (2022, 2026),
}

era_data = []
for era, (start, end) in era_map.items():
    assets = df[(df['FAILYR'] >= start) & (df['FAILYR'] <= end)]['QBFASSET'].dropna()
    for val in assets:
        era_data.append({'Era': era, 'Assets': val})

era_df = pd.DataFrame(era_data)

plt.figure(figsize=(12, 6))
sns.boxplot(data=era_df, x='Era', y='Assets', palette='Set2')
plt.yscale('log')
plt.title('Asset Size of Failed Banks by Era (Log Scale)',
          fontsize=14, fontweight='bold')
plt.xlabel('Crisis Era')
plt.ylabel('Total Assets ($ Thousands, log scale)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('chart4_asset_size_by_era.png', dpi=150)
plt.show()
print("Chart 4 saved.")

print("\n=== DONE — 4 charts saved to your folder ===")