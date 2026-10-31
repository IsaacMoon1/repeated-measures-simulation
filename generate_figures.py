import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set publication style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

base_dir = r"C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review"
tables_dir = os.path.join(base_dir, "tables")
figures_dir = os.path.join(base_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

df_cov = pd.read_csv(os.path.join(tables_dir, "table3_coverage.csv"))
df_t1 = pd.read_csv(os.path.join(tables_dir, "table4_type1_error.csv"))

colors = {'OLS': '#D95F02', 'CR2': '#1B9E77', 'LMM': '#1F78B4'}
markers = {'OLS': 'o', 'CR2': 's', 'LMM': '^'}
labels = {'OLS': 'Naive OLS', 'CR2': 'Cluster-Robust (CR2)', 'LMM': 'Mixed Model (REML)'}

# -------------------------------------------------------------
# Figure 1: 95% Confidence Interval Coverage
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True, dpi=300)

for row_idx, cov_type in enumerate(['Between-Subject', 'Within-Subject']):
    for col_idx, icc in enumerate([0.10, 0.50]):
        ax = axes[row_idx, col_idx]
        sub = df_cov[(df_cov['Covariate_Type'] == cov_type) & (np.isclose(df_cov['ICC'], icc))]
        
        # Nominal line & 1.96 * MCSE region for R=2000
        # mcse = sqrt(0.95 * 0.05 / 2000) approx 0.00487
        mcse_nom = np.sqrt(0.95 * 0.05 / 2000)
        ax.axhline(0.95, color='#444444', linestyle='--', linewidth=1.2, zorder=1)
        ax.axhspan(0.95 - 1.96 * mcse_nom, 0.95 + 1.96 * mcse_nom, color='#EAEAEA', alpha=0.6, zorder=0)
        
        jitters = {'OLS': -1.5, 'CR2': 0.0, 'LMM': 1.5}
        for m_name in ['OLS', 'CR2', 'LMM']:
            x_vals = sub['J'].values + jitters[m_name]
            y_vals = sub[f'{m_name}_Coverage'].values
            mcse_vals = sub[f'{m_name}_MCSE'].values
            
            ax.errorbar(x_vals, y_vals, yerr=1.96 * mcse_vals, fmt=f'-{markers[m_name]}',
                        color=colors[m_name], label=labels[m_name] if (row_idx == 0 and col_idx == 0) else "",
                        capsize=3.5, capthick=1.0, elinewidth=1.2, markersize=6, zorder=3)
        
        short_cov = "Between" if "Between" in cov_type else "Within"
        ax.set_title(f"{short_cov}-Subject | ICC = {icc:.2f}", fontsize=11, fontweight='bold', pad=8)
        ax.set_xticks([10, 30, 100])
        ax.set_xticklabels(['10', '30', '100'], fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.5, color='#CCCCCC')
        ax.set_ylim(0.68, 1.02)

for i in range(2):
    axes[1, i].set_xlabel("Number of Clusters (J)", fontsize=11, fontweight='bold', labelpad=8)
    axes[i, 0].set_ylabel("95% CI Coverage Probability", fontsize=11, fontweight='bold', labelpad=8)

fig.legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.01), fontsize=10.5, frameon=True, edgecolor='#CCCCCC')
plt.tight_layout()
fig.subplots_adjust(bottom=0.10)
fig1_path = os.path.join(figures_dir, "figure1_coverage.png")
plt.savefig(fig1_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated Figure 1: {fig1_path}")

# -------------------------------------------------------------
# Figure 2: Empirical Type I Error Rate
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True, dpi=300)

for row_idx, cov_type in enumerate(['Between-Subject', 'Within-Subject']):
    for col_idx, icc in enumerate([0.10, 0.50]):
        ax = axes[row_idx, col_idx]
        sub = df_t1[(df_t1['Covariate_Type'] == cov_type) & (np.isclose(df_t1['ICC'], icc))]
        
        # Nominal line & Bradley's (1978) liberal robustness band [0.025, 0.075]
        ax.axhline(0.05, color='#444444', linestyle='--', linewidth=1.2, zorder=1)
        ax.axhspan(0.025, 0.075, color='#E2E8F0', alpha=0.8, zorder=0, 
                   label="Bradley's (1978) Robustness Band [0.025, 0.075]" if (row_idx == 0 and col_idx == 0) else "")
        
        jitters = {'OLS': -1.5, 'CR2': 0.0, 'LMM': 1.5}
        for m_name in ['OLS', 'CR2', 'LMM']:
            x_vals = sub['J'].values + jitters[m_name]
            y_vals = sub[f'{m_name}_Type1_Error'].values
            mcse_vals = sub[f'{m_name}_MCSE'].values
            
            ax.errorbar(x_vals, y_vals, yerr=1.96 * mcse_vals, fmt=f'-{markers[m_name]}',
                        color=colors[m_name], label=labels[m_name] if (row_idx == 0 and col_idx == 0) else "",
                        capsize=3.5, capthick=1.0, elinewidth=1.2, markersize=6, zorder=3)
        
        short_cov = "Between" if "Between" in cov_type else "Within"
        ax.set_title(f"{short_cov}-Subject | ICC = {icc:.2f}", fontsize=11, fontweight='bold', pad=8)
        ax.set_xticks([10, 30, 100])
        ax.set_xticklabels(['10', '30', '100'], fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.5, color='#CCCCCC')
        ax.set_ylim(-0.01, 0.33)

for i in range(2):
    axes[1, i].set_xlabel("Number of Clusters (J)", fontsize=11, fontweight='bold', labelpad=8)
    axes[i, 0].set_ylabel("Empirical Type I Error Rate", fontsize=11, fontweight='bold', labelpad=8)

fig.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.01), fontsize=9.5, frameon=True, edgecolor='#CCCCCC')
plt.tight_layout()
fig.subplots_adjust(bottom=0.10)
fig2_path = os.path.join(figures_dir, "figure2_type1_error.png")
plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated Figure 2: {fig2_path}")
