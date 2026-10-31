import os
import matplotlib.pyplot as plt
import numpy as np

# Set publication style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

out_dir = r"C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review"
os.makedirs(os.path.join(out_dir, "figures"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "tables"), exist_ok=True)

# Data for Figure 1: Coverage
# J = [10, 30, 100]
# Panels: (Row 1: Between, Row 2: Within) x (Col 1: ICC=0.10, Col 2: ICC=0.50)
data_cov = {
    ('Between', 0.10): {
        'OLS': ([10, 30, 100], [0.902, 0.886, 0.894], [0.013, 0.014, 0.014]),
        'CR2': ([10, 30, 100], [0.952, 0.938, 0.946], [0.010, 0.011, 0.010]),
        'LMM': ([10, 30, 100], [0.970, 0.950, 0.946], [0.008, 0.010, 0.010])
    },
    ('Between', 0.50): {
        'OLS': ([10, 30, 100], [0.730, 0.748, 0.770], [0.020, 0.019, 0.019]),
        'CR2': ([10, 30, 100], [0.950, 0.948, 0.950], [0.010, 0.010, 0.010]),
        'LMM': ([10, 30, 100], [0.952, 0.948, 0.950], [0.010, 0.010, 0.010])
    },
    ('Within', 0.10): {
        'OLS': ([10, 30, 100], [0.958, 0.980, 0.958], [0.009, 0.006, 0.009]),
        'CR2': ([10, 30, 100], [0.938, 0.980, 0.946], [0.011, 0.006, 0.010]),
        'LMM': ([10, 30, 100], [0.936, 0.976, 0.946], [0.011, 0.007, 0.010])
    },
    ('Within', 0.50): {
        'OLS': ([10, 30, 100], [0.992, 0.998, 0.992], [0.004, 0.002, 0.004]),
        'CR2': ([10, 30, 100], [0.952, 0.960, 0.948], [0.010, 0.009, 0.010]),
        'LMM': ([10, 30, 100], [0.960, 0.956, 0.946], [0.009, 0.009, 0.010])
    }
}

colors = {'OLS': '#D95F02', 'CR2': '#1B9E77', 'LMM': '#1F78B4'}
markers = {'OLS': 'o', 'CR2': 's', 'LMM': '^'}
labels = {'OLS': 'Naive OLS', 'CR2': 'Cluster-Robust (CR2)', 'LMM': 'Mixed Model (REML)'}

# Plot Figure 1
fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True, dpi=300)

for row_idx, cov_type in enumerate(['Between', 'Within']):
    for col_idx, icc in enumerate([0.10, 0.50]):
        ax = axes[row_idx, col_idx]
        cell_data = data_cov[(cov_type, icc)]
        
        # Nominal line
        ax.axhline(0.95, color='#444444', linestyle='--', linewidth=1.2, zorder=1)
        ax.axhspan(0.95 - 1.96*0.01, 0.95 + 1.96*0.01, color='#EAEAEA', alpha=0.6, zorder=0)
        
        # J positions with slight jitter
        jitters = {'OLS': -1.5, 'CR2': 0.0, 'LMM': 1.5}
        for m_name in ['OLS', 'CR2', 'LMM']:
            x_raw, y, se = cell_data[m_name]
            x = [val + jitters[m_name] for val in x_raw]
            ax.errorbar(x, y, yerr=[1.96*s for s in se], fmt=f'-{markers[m_name]}', 
                        color=colors[m_name], label=labels[m_name] if (row_idx==0 and col_idx==0) else "",
                        capsize=3.5, capthick=1.0, elinewidth=1.2, markersize=6, zorder=3)
        
        ax.set_title(f"{cov_type}-Subject | ICC = {icc:.2f}", fontsize=11, fontweight='bold', pad=8)
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
fig1_path = os.path.join(out_dir, "figures", "figure1_coverage.png")
plt.savefig(fig1_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated Figure 1: {fig1_path}")

# Data for Figure 2: Type I Error Rate
data_t1 = {
    ('Between', 0.10): {
        'OLS': ([10, 30, 100], [0.104, 0.110, 0.084], [0.014, 0.014, 0.012]),
        'CR2': ([10, 30, 100], [0.064, 0.058, 0.044], [0.011, 0.010, 0.009]),
        'LMM': ([10, 30, 100], [0.050, 0.052, 0.044], [0.010, 0.010, 0.009])
    },
    ('Between', 0.50): {
        'OLS': ([10, 30, 100], [0.278, 0.248, 0.274], [0.020, 0.019, 0.020]),
        'CR2': ([10, 30, 100], [0.052, 0.050, 0.036], [0.010, 0.010, 0.008]),
        'LMM': ([10, 30, 100], [0.048, 0.048, 0.036], [0.010, 0.010, 0.008])
    },
    ('Within', 0.10): {
        'OLS': ([10, 30, 100], [0.044, 0.044, 0.038], [0.009, 0.009, 0.009]),
        'CR2': ([10, 30, 100], [0.042, 0.056, 0.044], [0.009, 0.010, 0.009]),
        'LMM': ([10, 30, 100], [0.054, 0.054, 0.042], [0.010, 0.010, 0.009])
    },
    ('Within', 0.50): {
        'OLS': ([10, 30, 100], [0.008, 0.004, 0.004], [0.004, 0.003, 0.003]),
        'CR2': ([10, 30, 100], [0.040, 0.062, 0.054], [0.009, 0.011, 0.010]),
        'LMM': ([10, 30, 100], [0.050, 0.062, 0.054], [0.010, 0.011, 0.010])
    }
}

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True, dpi=300)

for row_idx, cov_type in enumerate(['Between', 'Within']):
    for col_idx, icc in enumerate([0.10, 0.50]):
        ax = axes[row_idx, col_idx]
        cell_data = data_t1[(cov_type, icc)]
        
        # Nominal line & robustness band [0.025, 0.075]
        ax.axhline(0.05, color='#444444', linestyle='--', linewidth=1.2, zorder=1)
        ax.axhspan(0.025, 0.075, color='#E2E8F0', alpha=0.8, zorder=0, label='Robustness Band [0.025, 0.075]' if (row_idx==0 and col_idx==0) else "")
        
        jitters = {'OLS': -1.5, 'CR2': 0.0, 'LMM': 1.5}
        for m_name in ['OLS', 'CR2', 'LMM']:
            x_raw, y, se = cell_data[m_name]
            x = [val + jitters[m_name] for val in x_raw]
            ax.errorbar(x, y, yerr=[1.96*s for s in se], fmt=f'-{markers[m_name]}', 
                        color=colors[m_name], label=labels[m_name] if (row_idx==0 and col_idx==0) else "",
                        capsize=3.5, capthick=1.0, elinewidth=1.2, markersize=6, zorder=3)
        
        ax.set_title(f"{cov_type}-Subject | ICC = {icc:.2f}", fontsize=11, fontweight='bold', pad=8)
        ax.set_xticks([10, 30, 100])
        ax.set_xticklabels(['10', '30', '100'], fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.5, color='#CCCCCC')
        ax.set_ylim(-0.01, 0.33)

for i in range(2):
    axes[1, i].set_xlabel("Number of Clusters (J)", fontsize=11, fontweight='bold', labelpad=8)
    axes[i, 0].set_ylabel("Empirical Type I Error Rate", fontsize=11, fontweight='bold', labelpad=8)

fig.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.01), fontsize=10, frameon=True, edgecolor='#CCCCCC')
plt.tight_layout()
fig.subplots_adjust(bottom=0.10)
fig2_path = os.path.join(out_dir, "figures", "figure2_type1_error.png")
plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated Figure 2: {fig2_path}")
