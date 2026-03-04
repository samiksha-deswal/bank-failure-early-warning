import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Load both datasets ────────────────────────────────────────────────────
financials = pd.read_csv('bank_financials.csv')
failures   = pd.read_csv('bank_failures.csv')

# ── Clean and prepare ─────────────────────────────────────────────────────
financials['REPDTE']  = pd.to_datetime(financials['REPDTE'], format='%Y%m%d', errors='coerce')
financials['CERT']    = financials['CERT'].astype(int)
failures['CERT']      = pd.to_numeric(failures['CERT'], errors='coerce').dropna().astype(int)
failures['FAILDATE']  = pd.to_datetime(failures['FAILDATE'], errors='coerce')

# Merge failure date onto financials
fin = financials.merge(failures[['CERT','FAILDATE','NAME']], on='CERT', how='left')

# ── Calculate quarters before failure ─────────────────────────────────────
fin['DAYS_TO_FAIL']     = (fin['FAILDATE'] - fin['REPDTE']).dt.days
fin['QTRS_TO_FAIL']     = (fin['DAYS_TO_FAIL'] / 91).round().astype('Int64')

# Keep only records up to 12 quarters (3 years) before failure
pre_failure = fin[(fin['QTRS_TO_FAIL'] >= 0) & (fin['QTRS_TO_FAIL'] <= 12)].copy()

print(f"Pre-failure records (within 3 years of failure): {len(pre_failure)}")
print(f"Banks covered: {pre_failure['CERT'].nunique()}")

# ── Chart 1: ROA deterioration before failure ─────────────────────────────
roa_trend = pre_failure.groupby('QTRS_TO_FAIL')['ROA'].mean().reset_index()
roa_trend = roa_trend.sort_values('QTRS_TO_FAIL', ascending=False)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(roa_trend['QTRS_TO_FAIL'], roa_trend['ROA'],
        color='steelblue', linewidth=2.5, marker='o', markersize=5)
ax.axhline(0, color='red', linestyle='--', linewidth=1.2, label='Zero ROA line')
ax.axvspan(0, 2,  alpha=0.15, color='red',    label='Critical zone (0–2 qtrs)')
ax.axvspan(2, 6,  alpha=0.10, color='orange', label='Warning zone (2–6 qtrs)')
ax.invert_xaxis()
ax.set_title('Average ROA of Failed Banks — Quarters Before Failure',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Quarters Before Failure (right = closer to failure)')
ax.set_ylabel('Return on Assets (ROA %)')
ax.legend()
plt.tight_layout()
plt.savefig('chart5_roa_deterioration.png', dpi=150)
plt.close()
print("Chart 5 saved.")

# ── Chart 2: Asset size trend before failure ──────────────────────────────
asset_trend = pre_failure.groupby('QTRS_TO_FAIL')['ASSET'].mean().reset_index()
asset_trend = asset_trend.sort_values('QTRS_TO_FAIL', ascending=False)

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(asset_trend['QTRS_TO_FAIL'], asset_trend['ASSET'],
                color='steelblue', alpha=0.5)
ax.plot(asset_trend['QTRS_TO_FAIL'], asset_trend['ASSET'],
        color='steelblue', linewidth=2)
ax.invert_xaxis()
ax.set_title('Average Total Assets of Failed Banks — Quarters Before Failure',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Quarters Before Failure')
ax.set_ylabel('Average Total Assets ($ Thousands)')
plt.tight_layout()
plt.savefig('chart6_asset_trend.png', dpi=150)
plt.close()
print("Chart 6 saved.")

# ── Chart 3: Non-performing assets trend ─────────────────────────────────
nperfv_trend = pre_failure.groupby('QTRS_TO_FAIL')['NPERFV'].mean().reset_index()
nperfv_trend = nperfv_trend.sort_values('QTRS_TO_FAIL', ascending=False)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(nperfv_trend['QTRS_TO_FAIL'], nperfv_trend['NPERFV'],
        color='tomato', linewidth=2.5, marker='o', markersize=5)
ax.invert_xaxis()
ax.set_title('Average Non-Performing Assets — Quarters Before Failure',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Quarters Before Failure')
ax.set_ylabel('Non-Performing Assets ($ Thousands)')
plt.tight_layout()
plt.savefig('chart7_nonperforming.png', dpi=150)
plt.close()
print("Chart 7 saved.")

# ── Build the Early Warning Scorecard ────────────────────────────────────
print("\n=== BUILDING EARLY WARNING SCORECARD ===")

# Use last available quarter before failure for each bank
last_qtrs = pre_failure.sort_values('QTRS_TO_FAIL', ascending=True)
last_qtrs = last_qtrs.drop_duplicates(subset='CERT', keep='last')

def early_warning_score(row):
    score = 0
    flags = []

    # ROA scoring
    if row['ROA'] < -1.0:
        score += 3
        flags.append('ROA critically negative')
    elif row['ROA'] < 0:
        score += 2
        flags.append('ROA negative')
    elif row['ROA'] < 0.5:
        score += 1
        flags.append('ROA very low')

    # Capital ratio scoring
    if pd.notna(row['RBCRWAJ']):
        if row['RBCRWAJ'] < 6:
            score += 3
            flags.append('Capital ratio critically low (<6%)')
        elif row['RBCRWAJ'] < 8:
            score += 2
            flags.append('Capital ratio low (<8%)')
        elif row['RBCRWAJ'] < 10:
            score += 1
            flags.append('Capital ratio below well-capitalised threshold')

    # Non-performing assets
    if pd.notna(row['NPERFV']) and row['ASSET'] > 0:
        npa_ratio = row['NPERFV'] / row['ASSET'] * 100
        if npa_ratio > 10:
            score += 3
            flags.append(f'NPA ratio very high ({npa_ratio:.1f}%)')
        elif npa_ratio > 5:
            score += 2
            flags.append(f'NPA ratio elevated ({npa_ratio:.1f}%)')
        elif npa_ratio > 2:
            score += 1
            flags.append(f'NPA ratio rising ({npa_ratio:.1f}%)')

    # Net income
    if row['NETINC'] < 0:
        score += 1
        flags.append('Net income negative')

    return score, "; ".join(flags)

last_qtrs[['SCORE','FLAGS']] = last_qtrs.apply(
    lambda r: pd.Series(early_warning_score(r)), axis=1
)

def risk_label(score):
    if score >= 7:  return 'CRITICAL'
    elif score >= 5: return 'HIGH'
    elif score >= 3: return 'ELEVATED'
    else:            return 'WATCH'

last_qtrs['RISK_LEVEL'] = last_qtrs['SCORE'].apply(risk_label)

# ── Chart 4: Scorecard distribution ──────────────────────────────────────
risk_counts = last_qtrs['RISK_LEVEL'].value_counts()
colors = {'CRITICAL':'#d32f2f','HIGH':'#f57c00','ELEVATED':'#fbc02d','WATCH':'#388e3c'}
bar_colors = [colors.get(r, 'gray') for r in risk_counts.index]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(risk_counts.index, risk_counts.values, color=bar_colors, edgecolor='white', linewidth=1.5)
for bar, val in zip(bars, risk_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            str(val), ha='center', fontweight='bold', fontsize=12)
ax.set_title('Early Warning Scorecard — Risk Distribution of Failed Banks\n(Last Quarter Before Failure)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Risk Level')
ax.set_ylabel('Number of Banks')
plt.tight_layout()
plt.savefig('chart8_scorecard_distribution.png', dpi=150)
plt.close()
print("Chart 8 saved.")

# ── Print summary scorecard ───────────────────────────────────────────────
print("\n=== RISK LEVEL SUMMARY ===")
print(risk_counts.to_string())

print("\n=== TOP 10 HIGHEST RISK BANKS (pre-failure) ===")
top10 = last_qtrs.nlargest(10, 'SCORE')[['CERT','NAME','REPDTE','ROA','RBCRWAJ','SCORE','RISK_LEVEL','FLAGS']]
print(top10.to_string(index=False))

print("\n=== SCORECARD LEGEND ===")
print("Score 0–2  : WATCH     — Monitor closely")
print("Score 3–4  : ELEVATED  — Increased supervision warranted")
print("Score 5–6  : HIGH      — Intervention likely needed")
print("Score 7+   : CRITICAL  — Failure imminent")

print("\n=== ALL CHARTS SAVED ===")