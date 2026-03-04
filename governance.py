import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import json
import datetime

# ════════════════════════════════════════════════════════════════════
# PART 1: AI AGENT WORKFLOW DIAGRAM
# ════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(1, 1, figsize=(16, 20))
ax.set_xlim(0, 10)
ax.set_ylim(0, 22)
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

def draw_box(ax, x, y, w, h, text, subtext, color, text_color='white', style='round,pad=0.1'):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle=style,
                          facecolor=color, edgecolor='white',
                          linewidth=2, zorder=3)
    ax.add_patch(box)
    ax.text(x, y + 0.15, text, ha='center', va='center',
            fontsize=11, fontweight='bold', color=text_color, zorder=4)
    if subtext:
        ax.text(x, y - 0.35, subtext, ha='center', va='center',
                fontsize=8.5, color=text_color, alpha=0.9, zorder=4)

def draw_arrow(ax, x1, y1, x2, y2, color='#555555', label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=2.0, connectionstyle='arc3,rad=0.0'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.15, my, label, fontsize=8, color=color, style='italic')

def draw_diamond(ax, x, y, w, h, text, color):
    diamond = plt.Polygon(
        [[x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]],
        facecolor=color, edgecolor='white', linewidth=2, zorder=3
    )
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='white', zorder=4)

# ── Title ──
ax.text(5, 21.2, 'AI Bank Monitoring Agent — Governance Workflow',
        ha='center', va='center', fontsize=16, fontweight='bold', color='#1a1a2e')
ax.text(5, 20.7, 'How an automated early warning system operates inside a financial regulator',
        ha='center', va='center', fontsize=10, color='#555555', style='italic')

# ── Layer labels ──
for y_pos, label, col in [
    (19.5, 'DATA LAYER', '#dee2e6'),
    (16.8, 'PROCESSING LAYER', '#dee2e6'),
    (13.5, 'DECISION LAYER', '#dee2e6'),
    (9.5,  'GOVERNANCE LAYER', '#dee2e6'),
    (5.5,  'ACTION LAYER', '#dee2e6'),
    (2.0,  'AUDIT LAYER', '#dee2e6'),
]:
    ax.add_patch(FancyBboxPatch((0.1, y_pos - 0.3), 9.8, 0.6,
                                 boxstyle='round,pad=0.05',
                                 facecolor=col, edgecolor='none', alpha=0.5, zorder=1))
    ax.text(0.4, y_pos, label, fontsize=8, fontweight='bold',
            color='#555555', va='center', zorder=2)

# ── DATA LAYER ──
draw_box(ax, 2.5, 18.5, 3.2, 0.9, 'FDIC Call Reports', 'Quarterly financials — all banks', '#2c3e50')
draw_box(ax, 5.0, 18.5, 2.2, 0.9, 'Market Data', 'Rates, spreads', '#2c3e50')
draw_box(ax, 7.5, 18.5, 2.2, 0.9, 'CFPB Complaints', 'Consumer signals', '#2c3e50')

# ── arrows down to ingestion ──
for x in [2.5, 5.0, 7.5]:
    draw_arrow(ax, x, 18.05, x, 17.45)

draw_box(ax, 5.0, 17.0, 8.0, 0.9,
         'Data Ingestion & Validation Agent',
         'Checks completeness, flags missing fields, normalises formats', '#1a6b8a')

# ── PROCESSING LAYER ──
draw_arrow(ax, 5.0, 16.55, 5.0, 15.95)
draw_box(ax, 5.0, 15.5, 8.0, 0.9,
         'Feature Engineering Agent',
         'Computes ROA trend, NPA ratio, capital ratio, deposit concentration', '#1a6b8a')

draw_arrow(ax, 5.0, 15.05, 5.0, 14.45)
draw_box(ax, 5.0, 14.0, 8.0, 0.9,
         'Early Warning Scoring Agent',
         'Applies scorecard rules → outputs WATCH / ELEVATED / HIGH / CRITICAL', '#1a6b8a')

# ── DECISION LAYER ──
draw_arrow(ax, 5.0, 13.55, 5.0, 12.75)
draw_diamond(ax, 5.0, 12.2, 4.5, 1.0, 'Risk Level ≥ HIGH?', '#e67e22')

# Yes/No branches
draw_arrow(ax, 5.0, 11.7, 5.0, 11.1, color='#c0392b', label='  YES')
draw_arrow(ax, 7.25, 12.2, 8.5, 12.2, color='#27ae60', label=' NO')

draw_box(ax, 5.0, 10.6, 4.5, 0.9,
         'Escalation Triggered',
         'Alert generated for human review', '#c0392b')
draw_box(ax, 8.5, 12.2, 2.2, 0.9,
         'Continue\nMonitoring',
         'Next quarter', '#27ae60')

# ── GOVERNANCE LAYER ──
draw_arrow(ax, 5.0, 10.15, 5.0, 9.45)
draw_box(ax, 5.0, 9.0, 8.0, 0.9,
         'Human Review Gate  ★ KEY GOVERNANCE CONTROL',
         'Examiner reviews flag, model output, data quality score', '#6c3483')

draw_arrow(ax, 5.0, 8.55, 5.0, 7.95)
draw_diamond(ax, 5.0, 7.4, 4.5, 1.0, 'Examiner Confirms?', '#8e44ad')

draw_arrow(ax, 5.0, 6.9, 5.0, 6.3, color='#c0392b', label='  CONFIRMED')
draw_arrow(ax, 7.25, 7.4, 8.5, 7.4, color='#27ae60', label=' DISMISSED')

draw_box(ax, 8.5, 7.4, 2.2, 0.9, 'Dismissed\n+ Logged', '', '#27ae60')

# ── ACTION LAYER ──
draw_box(ax, 3.2, 5.8, 2.8, 0.9,
         'Supervisory Letter',
         'Formal notice to bank', '#c0392b')
draw_box(ax, 5.0, 5.8, 1.8, 0.9,
         'On-site\nExam', '', '#c0392b')
draw_box(ax, 6.8, 5.8, 2.8, 0.9,
         'Enforcement\nAction', 'If warranted', '#c0392b')

draw_arrow(ax, 5.0, 6.3, 3.2, 6.25)
draw_arrow(ax, 5.0, 6.3, 5.0, 6.25)
draw_arrow(ax, 5.0, 6.3, 6.8, 6.25)

# ── AUDIT LAYER ──
for x in [3.2, 5.0, 6.8]:
    draw_arrow(ax, x, 5.35, 5.0, 2.75)

draw_box(ax, 5.0, 2.3, 8.5, 0.9,
         'Immutable Audit Log',
         'Every decision, score, override, and action time-stamped and stored', '#2c3e50')

ax.text(5.0, 1.5,
        '★  SR 11-7 Compliant  |  Full explainability  |  Human override at every stage  |  No black-box decisions',
        ha='center', fontsize=9, color='#6c3483', fontweight='bold')

plt.tight_layout()
plt.savefig('chart9_governance_workflow.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 9: Governance workflow saved.")


# ════════════════════════════════════════════════════════════════════
# PART 2: AUDIT TRAIL SYSTEM
# ════════════════════════════════════════════════════════════════════

financials = pd.read_csv('bank_financials.csv')
failures   = pd.read_csv('bank_failures.csv')

financials['REPDTE'] = pd.to_datetime(financials['REPDTE'], format='%Y%m%d', errors='coerce')
financials['CERT']   = financials['CERT'].astype(int)
failures['CERT']     = pd.to_numeric(failures['CERT'], errors='coerce').dropna().astype(int)
failures['FAILDATE'] = pd.to_datetime(failures['FAILDATE'], errors='coerce')

fin = financials.merge(failures[['CERT','FAILDATE','NAME']], on='CERT', how='left')
fin['DAYS_TO_FAIL'] = (fin['FAILDATE'] - fin['REPDTE']).dt.days
fin['QTRS_TO_FAIL'] = (fin['DAYS_TO_FAIL'] / 91).round().astype('Int64')

pre_failure = fin[(fin['QTRS_TO_FAIL'] >= 0) & (fin['QTRS_TO_FAIL'] <= 12)].copy()

def score_bank(row):
    score = 0
    flags = []
    if row['ROA'] < -1.0:
        score += 3; flags.append('ROA critically negative (<-1.0)')
    elif row['ROA'] < 0:
        score += 2; flags.append('ROA negative')
    elif row['ROA'] < 0.5:
        score += 1; flags.append('ROA very low (<0.5)')
    if pd.notna(row['RBCRWAJ']) and row['RBCRWAJ'] > 0 and row['RBCRWAJ'] < 20:
        if row['RBCRWAJ'] < 6:
            score += 3; flags.append('Capital ratio critical (<6%)')
        elif row['RBCRWAJ'] < 8:
            score += 2; flags.append('Capital ratio low (<8%)')
        elif row['RBCRWAJ'] < 10:
            score += 1; flags.append('Capital ratio below well-capitalised')
    if pd.notna(row['NPERFV']) and row['ASSET'] > 0:
        npa = row['NPERFV'] / row['ASSET'] * 100
        if npa > 10:
            score += 3; flags.append(f'NPA ratio critical ({npa:.1f}%)')
        elif npa > 5:
            score += 2; flags.append(f'NPA ratio elevated ({npa:.1f}%)')
        elif npa > 2:
            score += 1; flags.append(f'NPA ratio rising ({npa:.1f}%)')
    if row['NETINC'] < 0:
        score += 1; flags.append('Net income negative')
    if score >= 7:   risk = 'CRITICAL'
    elif score >= 5: risk = 'HIGH'
    elif score >= 3: risk = 'ELEVATED'
    else:            risk = 'WATCH'
    return score, risk, flags

# Build audit trail
audit_records = []
run_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for _, row in pre_failure.iterrows():
    score, risk, flags = score_bank(row)
    audit_records.append({
        'run_timestamp'   : run_timestamp,
        'cert'            : int(row['CERT']),
        'bank_name'       : row.get('NAME', 'Unknown'),
        'report_date'     : str(row['REPDTE'].date()) if pd.notna(row['REPDTE']) else 'N/A',
        'qtrs_to_failure' : int(row['QTRS_TO_FAIL']) if pd.notna(row['QTRS_TO_FAIL']) else -1,
        'roa'             : round(float(row['ROA']), 4) if pd.notna(row['ROA']) else None,
        'capital_ratio'   : round(float(row['RBCRWAJ']), 4) if pd.notna(row['RBCRWAJ']) else None,
        'npa_value'       : round(float(row['NPERFV']), 0) if pd.notna(row['NPERFV']) else None,
        'total_assets'    : round(float(row['ASSET']), 0) if pd.notna(row['ASSET']) else None,
        'risk_score'      : score,
        'risk_level'      : risk,
        'flags_triggered' : flags,
        'flag_count'      : len(flags),
        'model_version'   : 'v1.0-rules-based',
        'requires_review' : risk in ['HIGH', 'CRITICAL'],
        'human_reviewed'  : False,
        'examiner_note'   : '',
    })

# Save full audit trail
audit_df = pd.DataFrame(audit_records)
audit_df.to_csv('audit_trail.csv', index=False)
print(f"Audit trail saved: {len(audit_df)} records")

# Save JSON sample (first 5 HIGH/CRITICAL or top scorers)
top_records = audit_df.nlargest(5, 'risk_score')[audit_df.columns.tolist()]
with open('audit_sample.json', 'w') as f:
    json.dump(top_records.to_dict(orient='records'), f, indent=2, default=str)
print("Audit sample JSON saved.")

# ── Chart 10: Audit trail — score distribution over time ─────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Audit Trail Analysis — Scorecard Behaviour Over Time',
             fontsize=14, fontweight='bold', y=1.01)

# Left: score distribution
score_counts = audit_df['risk_score'].value_counts().sort_index()
color_map = {0:'#388e3c', 1:'#66bb6a', 2:'#fbc02d',
             3:'#fbc02d', 4:'#f57c00', 5:'#e64a19',
             6:'#d32f2f', 7:'#b71c1c', 8:'#880e4f'}
bar_colors = [color_map.get(s, '#888888') for s in score_counts.index]
axes[0].bar(score_counts.index, score_counts.values, color=bar_colors, edgecolor='white')
axes[0].set_title('Distribution of Risk Scores\n(All Pre-Failure Records)', fontweight='bold')
axes[0].set_xlabel('Risk Score')
axes[0].set_ylabel('Number of Quarterly Records')
axes[0].set_xticks(range(0, 9))

legend_items = [
    mpatches.Patch(color='#388e3c', label='WATCH (0–2)'),
    mpatches.Patch(color='#fbc02d', label='ELEVATED (3–4)'),
    mpatches.Patch(color='#e64a19', label='HIGH (5–6)'),
    mpatches.Patch(color='#b71c1c', label='CRITICAL (7+)'),
]
axes[0].legend(handles=legend_items, fontsize=9)

# Right: average score by quarters to failure
avg_score = audit_df.groupby('qtrs_to_failure')['risk_score'].mean().reset_index()
avg_score = avg_score[avg_score['qtrs_to_failure'] >= 0].sort_values('qtrs_to_failure', ascending=False)

axes[1].plot(avg_score['qtrs_to_failure'], avg_score['risk_score'],
             color='#e67e22', linewidth=2.5, marker='o', markersize=6)
axes[1].axhline(3, color='#fbc02d', linestyle='--', linewidth=1.2, label='ELEVATED threshold')
axes[1].axhline(5, color='#e64a19', linestyle='--', linewidth=1.2, label='HIGH threshold')
axes[1].axhline(7, color='#b71c1c', linestyle='--', linewidth=1.2, label='CRITICAL threshold')
axes[1].invert_xaxis()
axes[1].set_title('Average Risk Score vs Quarters Before Failure\n(Early Warning Trajectory)', fontweight='bold')
axes[1].set_xlabel('Quarters Before Failure (right = closer to failure)')
axes[1].set_ylabel('Average Risk Score')
axes[1].legend(fontsize=9)

plt.tight_layout()
plt.savefig('chart10_audit_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 10: Audit analysis saved.")

# ── Final summary ─────────────────────────────────────────────────────────
print("\n=== GOVERNANCE FRAMEWORK SUMMARY ===")
print(f"Total records audited       : {len(audit_df)}")
print(f"Records requiring review    : {audit_df['requires_review'].sum()}")
print(f"Unique banks covered        : {audit_df['cert'].nunique()}")
print(f"Most common flag            : {audit_df['flags_triggered'].explode().value_counts().index[0]}")
print(f"Avg score at 1 qtr to fail  : {audit_df[audit_df['qtrs_to_failure']==1]['risk_score'].mean():.2f}")
print(f"Avg score at 8 qtrs to fail : {audit_df[audit_df['qtrs_to_failure']==8]['risk_score'].mean():.2f}")
print("\nFiles saved:")
print("  chart9_governance_workflow.png")
print("  chart10_audit_analysis.png")
print("  audit_trail.csv")
print("  audit_sample.json")
print("\n=== DONE ===")