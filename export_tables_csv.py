#!/usr/bin/env python3
"""
Title: Export Simulation Tables to CSV (ADEMP Protocol, R=2000)
Author: Isaac T. Adeyemi
Institution: Ladoke Akintola University of Technology (LAUTECH)
Description: Generates clean publication CSV tables from the complete R=2,000 simulation run.
"""

import os
import csv
from run_complete_simulation import run_simulation

out_dir = r"C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review\tables"
os.makedirs(out_dir, exist_ok=True)

df_bias, df_se, df_cov, df_type1, df_power, df_sing = run_simulation(R=2000, seed=20261031)

# Format numerical columns for clean presentation
def fmt(df, precision_dict):
    df_out = df.copy()
    for col, prec in precision_dict.items():
        if col in df_out.columns:
            df_out[col] = df_out[col].apply(lambda x: f"{x:.{prec}f}" if pd.notnull(x) else "NA")
    return df_out

import pandas as pd

# Table 1: Bias
df_bias_fmt = fmt(df_bias, {
    'Naive_OLS_Bias': 4, 'Naive_OLS_MCSE': 4,
    'CR2_Bias': 4, 'CR2_MCSE': 4,
    'LMM_Bias': 4, 'LMM_MCSE': 4
})
df_bias_fmt.to_csv(os.path.join(out_dir, "table1_bias.csv"), index=False)

# Table 2: SE Accuracy
df_se_fmt = fmt(df_se, {
    'Empirical_SD': 4,
    'OLS_Mean_SE': 4, 'OLS_SE_Ratio': 3,
    'CR2_Mean_SE': 4, 'CR2_SE_Ratio': 3,
    'LMM_Mean_SE': 4, 'LMM_SE_Ratio': 3
})
df_se_fmt.to_csv(os.path.join(out_dir, "table2_se_accuracy.csv"), index=False)

# Table 3: Coverage
df_cov_fmt = fmt(df_cov, {
    'OLS_Coverage': 3, 'OLS_MCSE': 3,
    'CR2_Coverage': 3, 'CR2_MCSE': 3,
    'LMM_Coverage': 3, 'LMM_MCSE': 3
})
df_cov_fmt.to_csv(os.path.join(out_dir, "table3_coverage.csv"), index=False)

# Table 4: Type I Error
df_type1_fmt = fmt(df_type1, {
    'OLS_Type1_Error': 3, 'OLS_MCSE': 3,
    'CR2_Type1_Error': 3, 'CR2_MCSE': 3,
    'LMM_Type1_Error': 3, 'LMM_MCSE': 3
})
df_type1_fmt.to_csv(os.path.join(out_dir, "table4_type1_error.csv"), index=False)

# Table 5: Power
df_power_fmt = fmt(df_power, {
    'OLS_Power': 3, 'OLS_MCSE': 3,
    'CR2_Power': 3, 'CR2_MCSE': 3,
    'LMM_Power': 3, 'LMM_MCSE': 3
})
df_power_fmt.to_csv(os.path.join(out_dir, "table5_power.csv"), index=False)

# Table 5b / Diagnostic: Singular Fits
df_sing_fmt = fmt(df_sing, {
    'Singular_Rate_Pct': 2,
    'LMM_Cov_Overall': 3,
    'LMM_Cov_Singular': 3,
    'LMM_Cov_NonSingular': 3
})
df_sing_fmt.to_csv(os.path.join(out_dir, "table_singular_fits.csv"), index=False)

# Table 6: Sleep study benchmark
t6 = [
    ["Model_Specification", "Estimate_beta1", "Std_Error", "df", "p_value", "CI_95_Lower", "CI_95_Upper"],
    ["1. Naive OLS (complete pooling)", 10.467, 1.238, 178, "< 0.001", 8.024, 12.911],
    ["2. Cluster-robust OLS (CR2)", 10.467, 1.546, 17, "< 0.001", 7.206, 13.729],
    ["3. LMM (random intercept only)", 10.467, 0.804, 161, "< 0.001", 8.879, 12.055],
    ["4. LMM (random slope & intercept)", 10.467, 1.546, 17, "< 0.001", 7.206, 13.729]
]
with open(os.path.join(out_dir, "table6_sleepstudy.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(t6)

# Table 7: Decision Pathway
t7 = [
    ["Cluster_Count", "Analytical_Goal", "Recommended_Approach", "Requirements_and_Cautions"],
    ["J < 30 (Small)", "Subject trajectories / variance components", "Linear mixed model (REML)", "Satterthwaite degrees of freedom is mandatory (Kuznetsova et al., 2017); audit singular boundary fits (Bates et al., 2015)"],
    ["J < 30 (Small)", "Population-averaged effects / robustness", "Cluster-robust OLS (CR2)", "Satterthwaite t reference distribution is mandatory (Pustejovsky, 2023); protected against random-slope misspecification in empirical balanced designs (Pustejovsky & Tipton, 2018)"],
    ["J >= 30 (Moderate to Large)", "Subject trajectories", "Linear mixed model (REML / ML)", "Asymptotically robust inference is valid (Verbeke & Molenberghs, 2000)"],
    ["J >= 30 (Moderate to Large)", "Population-averaged effects", "GEE / CR0 / CR1", "Standard sandwich errors are valid; recommendation drawn from literature (Cameron & Miller, 2015; Zeileis et al., 2020)"]
]
with open(os.path.join(out_dir, "table7_decision_pathway.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(t7)

print("Exported all CSV tables successfully to:", out_dir)
