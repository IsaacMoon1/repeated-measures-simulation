import os
import csv

out_dir = r"C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review\tables"
os.makedirs(out_dir, exist_ok=True)

# Table 1: Bias
t1 = [
    ["Covariate_Type", "J", "ICC", "Naive_OLS_Bias", "Naive_OLS_MCSE", "CR2_Bias", "CR2_MCSE", "LMM_Bias", "LMM_MCSE"],
    ["Between-Subject", 10, 0.10, 0.005, 0.015, 0.005, 0.015, 0.005, 0.015],
    ["Between-Subject", 10, 0.50, 0.008, 0.021, 0.008, 0.021, 0.008, 0.021],
    ["Between-Subject", 30, 0.10, -0.006, 0.009, -0.006, 0.009, -0.006, 0.009],
    ["Between-Subject", 30, 0.50, -0.008, 0.013, -0.008, 0.013, -0.008, 0.013],
    ["Between-Subject", 100, 0.10, 0.000, 0.005, 0.000, 0.005, 0.000, 0.005],
    ["Between-Subject", 100, 0.50, 0.003, 0.007, 0.003, 0.007, 0.003, 0.007],
    ["Within-Subject", 10, 0.10, 0.000, 0.004, 0.000, 0.004, 0.000, 0.004],
    ["Within-Subject", 10, 0.50, -0.002, 0.003, -0.002, 0.003, -0.002, 0.003],
    ["Within-Subject", 30, 0.10, 0.001, 0.002, 0.001, 0.002, 0.001, 0.002],
    ["Within-Subject", 30, 0.50, 0.001, 0.002, 0.001, 0.002, 0.001, 0.002],
    ["Within-Subject", 100, 0.10, 0.000, 0.001, 0.000, 0.001, 0.000, 0.001],
    ["Within-Subject", 100, 0.50, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]
]
with open(os.path.join(out_dir, "table1_bias.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(t1)

# Table 2: SE Accuracy
t2 = [
    ["Covariate_Type", "J", "ICC", "Empirical_SD", "OLS_Mean_SE", "OLS_SE_Ratio", "CR2_Mean_SE", "CR2_SE_Ratio", "LMM_Mean_SE", "LMM_SE_Ratio"],
    ["Between-Subject", 10, 0.10, 0.331, 0.280, 0.846, 0.327, 0.986, 0.338, 1.020],
    ["Between-Subject", 10, 0.50, 0.478, 0.267, 0.558, 0.471, 0.985, 0.471, 0.985],
    ["Between-Subject", 30, 0.10, 0.199, 0.162, 0.816, 0.191, 0.961, 0.192, 0.967],
    ["Between-Subject", 30, 0.50, 0.290, 0.161, 0.554, 0.280, 0.965, 0.280, 0.965],
    ["Between-Subject", 100, 0.10, 0.109, 0.089, 0.821, 0.106, 0.973, 0.106, 0.973],
    ["Between-Subject", 100, 0.50, 0.150, 0.089, 0.595, 0.155, 1.034, 0.155, 1.034],
    ["Within-Subject", 10, 0.10, 0.098, 0.099, 1.015, 0.092, 0.943, 0.094, 0.962],
    ["Within-Subject", 10, 0.50, 0.071, 0.099, 1.390, 0.069, 0.967, 0.071, 0.990],
    ["Within-Subject", 30, 0.10, 0.050, 0.058, 1.155, 0.054, 1.084, 0.055, 1.096],
    ["Within-Subject", 30, 0.50, 0.039, 0.057, 1.451, 0.040, 1.028, 0.041, 1.041],
    ["Within-Subject", 100, 0.10, 0.030, 0.032, 1.054, 0.030, 1.001, 0.030, 1.001],
    ["Within-Subject", 100, 0.50, 0.023, 0.031, 1.362, 0.022, 0.963, 0.022, 0.964]
]
with open(os.path.join(out_dir, "table2_se_accuracy.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(t2)

# Table 3: Coverage
t3 = [
    ["Covariate_Type", "J", "ICC", "OLS_Coverage", "OLS_MCSE", "CR2_Coverage", "CR2_MCSE", "LMM_Coverage", "LMM_MCSE"],
    ["Between-Subject", 10, 0.10, 0.902, 0.013, 0.952, 0.010, 0.970, 0.008],
    ["Between-Subject", 10, 0.50, 0.730, 0.020, 0.950, 0.010, 0.952, 0.010],
    ["Between-Subject", 30, 0.10, 0.886, 0.014, 0.938, 0.011, 0.950, 0.010],
    ["Between-Subject", 30, 0.50, 0.748, 0.019, 0.948, 0.010, 0.948, 0.010],
    ["Between-Subject", 100, 0.10, 0.894, 0.014, 0.946, 0.010, 0.946, 0.010],
    ["Between-Subject", 100, 0.50, 0.770, 0.019, 0.950, 0.010, 0.950, 0.010],
    ["Within-Subject", 10, 0.10, 0.958, 0.009, 0.938, 0.011, 0.936, 0.011],
    ["Within-Subject", 10, 0.50, 0.992, 0.004, 0.952, 0.010, 0.960, 0.009],
    ["Within-Subject", 30, 0.10, 0.980, 0.006, 0.980, 0.006, 0.976, 0.007],
    ["Within-Subject", 30, 0.50, 0.998, 0.002, 0.960, 0.009, 0.956, 0.009],
    ["Within-Subject", 100, 0.10, 0.958, 0.009, 0.946, 0.010, 0.946, 0.010],
    ["Within-Subject", 100, 0.50, 0.992, 0.004, 0.948, 0.010, 0.946, 0.010]
]
with open(os.path.join(out_dir, "table3_coverage.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(t3)

# Table 4: Type I Error Rate
t4 = [
    ["Covariate_Type", "J", "ICC", "OLS_Type1_Error", "OLS_MCSE", "CR2_Type1_Error", "CR2_MCSE", "LMM_Type1_Error", "LMM_MCSE"],
    ["Between-Subject", 10, 0.10, 0.104, 0.014, 0.064, 0.011, 0.050, 0.010],
    ["Between-Subject", 10, 0.50, 0.278, 0.020, 0.052, 0.010, 0.048, 0.010],
    ["Between-Subject", 30, 0.10, 0.110, 0.014, 0.058, 0.010, 0.052, 0.010],
    ["Between-Subject", 30, 0.50, 0.248, 0.019, 0.050, 0.010, 0.048, 0.010],
    ["Between-Subject", 100, 0.10, 0.084, 0.012, 0.044, 0.009, 0.044, 0.009],
    ["Between-Subject", 100, 0.50, 0.274, 0.020, 0.036, 0.008, 0.036, 0.008],
    ["Within-Subject", 10, 0.10, 0.044, 0.009, 0.042, 0.009, 0.054, 0.010],
    ["Within-Subject", 10, 0.50, 0.008, 0.004, 0.040, 0.009, 0.050, 0.010],
    ["Within-Subject", 30, 0.10, 0.044, 0.009, 0.056, 0.010, 0.054, 0.010],
    ["Within-Subject", 30, 0.50, 0.004, 0.003, 0.062, 0.011, 0.062, 0.011],
    ["Within-Subject", 100, 0.10, 0.038, 0.009, 0.044, 0.009, 0.042, 0.009],
    ["Within-Subject", 100, 0.50, 0.004, 0.003, 0.054, 0.010, 0.054, 0.010]
]
with open(os.path.join(out_dir, "table4_type1_error.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(t4)

# Table 5: Power
t5 = [
    ["Covariate_Type", "J", "ICC", "OLS_Power", "OLS_MCSE", "CR2_Power", "CR2_MCSE", "LMM_Power", "LMM_MCSE"],
    ["Between-Subject", 10, 0.10, 0.440, 0.022, 0.320, 0.021, 0.288, 0.020],
    ["Between-Subject", 10, 0.50, 0.482, 0.022, 0.170, 0.017, 0.172, 0.017],
    ["Between-Subject", 30, 0.10, 0.894, 0.014, 0.776, 0.019, 0.776, 0.019],
    ["Between-Subject", 30, 0.50, 0.852, 0.016, 0.442, 0.022, 0.442, 0.022],
    ["Between-Subject", 100, 0.10, 1.000, 0.000, 1.000, 0.000, 1.000, 0.000],
    ["Between-Subject", 100, 0.50, 1.000, 0.000, 0.916, 0.012, 0.916, 0.012],
    ["Within-Subject", 10, 0.10, 1.000, 0.000, 1.000, 0.000, 1.000, 0.000],
    ["Within-Subject", 10, 0.50, 1.000, 0.000, 1.000, 0.000, 1.000, 0.000],
    ["Within-Subject", 30, 0.10, 1.000, 0.000, 1.000, 0.000, 1.000, 0.000],
    ["Within-Subject", 30, 0.50, 1.000, 0.000, 1.000, 0.000, 1.000, 0.000],
    ["Within-Subject", 100, 0.10, 1.000, 0.000, 1.000, 0.000, 1.000, 0.000],
    ["Within-Subject", 100, 0.50, 1.000, 0.000, 1.000, 0.000, 1.000, 0.000]
]
with open(os.path.join(out_dir, "table5_power.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(t5)

# Table 6: Sleep study
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
    ["J < 30 (Small)", "Population-averaged effects / robustness", "Cluster-robust OLS (CR2)", "Satterthwaite t reference distribution is mandatory (Pustejovsky, 2023); protected against random-effects misspecification (Pustejovsky & Tipton, 2018)"],
    ["J >= 30 (Moderate to Large)", "Subject trajectories", "Linear mixed model (REML / ML)", "Asymptotically robust inference is valid"],
    ["J >= 30 (Moderate to Large)", "Population-averaged effects", "GEE / CR0 / CR1", "Standard sandwich errors are valid (Zeileis et al., 2020)"]
]
with open(os.path.join(out_dir, "table7_decision_pathway.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(t7)

print("Exported all 7 tables to CSV in:", out_dir)
