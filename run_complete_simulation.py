#!/usr/bin/env python3
"""
Title: Complete Monte Carlo Simulation Engine (ADEMP Protocol, R=2000)
Author: Isaac T. Adeyemi
Institution: Ladoke Akintola University of Technology (LAUTECH)
Description: Executes all 24 factorial scenarios across R=2,000 replications (48,000 datasets)
             with seed 20261031. Evaluates Naive OLS, CR2, and LMM.
             Computes Morris et al. (2019) SE ratios, empirical coverage, Type I error,
             power, and singular fit diagnostics.
"""

import os
import math
import numpy as np
import pandas as pd
from scipy.stats import t as t_dist

def run_simulation(R=2000, seed=20261031):
    np.random.seed(seed)
    K = 5
    tj = np.array([-2, -1, 0, 1, 2], dtype=float)
    sum_t2 = np.sum(tj**2) # 10.0
    
    # Storage for summary metrics
    records_bias = []
    records_se = []
    records_cov = []
    records_type1 = []
    records_power = []
    records_singular = []
    
    # Define design factors
    cov_types = ['Between-Subject', 'Within-Subject']
    J_levels = [10, 30, 100]
    icc_levels = [0.10, 0.50]
    
    for cov in cov_types:
        for J in J_levels:
            for icc in icc_levels:
                sig_u = np.sqrt(icc)
                sig_e = np.sqrt(1.0 - icc)
                
                # We need data under H0 (beta1 = 0) for Type I error
                # and under H1 (beta1 = 0.50) for Bias, SE, Coverage, Power
                for beta1 in [0.0, 0.50]:
                    # Generate random effects: u is (R, J, 1), e is (R, J, K)
                    u = np.random.normal(0, sig_u, size=(R, J, 1))
                    e = np.random.normal(0, sig_e, size=(R, J, K))
                    
                    if cov == 'Between-Subject':
                        # Z: half 0, half 1
                        Z = np.zeros((J, 1), dtype=float)
                        Z[J//2:, 0] = 1.0 # (J, 1)
                        # X is (J, K)
                        X = np.tile(Z, (1, K)) # (J, K)
                        # Y is (R, J, K)
                        Y = 10.0 + beta1 * X + u + e
                        
                        # Point estimate beta1_hat: difference of group means
                        # Group 0: j < J//2; Group 1: j >= J//2
                        # Means per cluster: (R, J)
                        Y_bar_j = np.mean(Y, axis=2)
                        mean_g1 = np.mean(Y_bar_j[:, J//2:], axis=1) # (R,)
                        mean_g0 = np.mean(Y_bar_j[:, :J//2], axis=1) # (R,)
                        b1_hat = mean_g1 - mean_g0 # (R,)
                        
                        # Residuals from OLS:
                        # y_ijk - y_bar - b1_hat * (x_ijk - 0.5)
                        # Notice that for group 0, fitted is mean_g0; for group 1, fitted is mean_g1!
                        fitted = np.zeros((R, J, K))
                        fitted[:, :J//2, :] = mean_g0[:, np.newaxis, np.newaxis]
                        fitted[:, J//2:, :] = mean_g1[:, np.newaxis, np.newaxis]
                        e_ols = Y - fitted # (R, J, K)
                        
                        df_ols = J * K - 2
                        s2_ols = np.sum(e_ols**2, axis=(1, 2)) / df_ols
                        sum_x_dev2 = 1.25 * J
                        var_ols = s2_ols / sum_x_dev2
                        se_ols = np.sqrt(var_ols)
                        
                        # CR2 Variance:
                        # Var_CR2 = 4 / (J * (J - 2)) * sum_{j=1}^J (Y_bar_j - Y_bar_group)^2
                        # which is 4 / J * s^2_{Y_bar}
                        dev_g0 = Y_bar_j[:, :J//2] - mean_g0[:, np.newaxis]
                        dev_g1 = Y_bar_j[:, J//2:] - mean_g1[:, np.newaxis]
                        ss_b = np.sum(dev_g0**2, axis=1) + np.sum(dev_g1**2, axis=1) # (R,)
                        s2_b = ss_b / (J - 2)
                        var_cr2 = (4.0 / J) * s2_b
                        se_cr2 = np.sqrt(var_cr2)
                        df_cr2 = J - 2
                        
                        # LMM REML Variance:
                        # MSB = K * s2_b = 5 * s2_b
                        # MSW = sum(e_ols - (Y_bar_j - fitted_j))^2 / (J * (K - 1))
                        # Note: within-cluster deviation is Y_ijk - Y_bar_j
                        dev_within = Y - Y_bar_j[:, :, np.newaxis]
                        ss_w = np.sum(dev_within**2, axis=(1, 2))
                        df_w = J * (K - 1)
                        msw = ss_w / df_w
                        msb = K * s2_b
                        
                        # REML variance components
                        sig_e2_hat = msw
                        sig_u2_hat = np.maximum(0.0, (msb - msw) / K)
                        singular = (msb <= msw)
                        
                        # For LMM, when sig_u2_hat > 0, var_LMM = var_cr2, df = J - 2
                        # When singular (sig_u2_hat == 0), var_LMM = 4 * msw / (K * J), df = df_ols
                        var_lmm = np.where(singular, (4.0 / (K * J)) * msw, var_cr2)
                        se_lmm = np.sqrt(var_lmm)
                        df_lmm = np.where(singular, df_ols, J - 2)
                        
                    else: # Within-Subject
                        # X is tj for all clusters
                        # tj = [-2, -1, 0, 1, 2]
                        # Y is (R, J, K)
                        # Mean of tj is 0
                        X = np.tile(tj[np.newaxis, :], (J, 1)) # (J, K)
                        Y = 10.0 + beta1 * X + u + e
                        
                        # b1_hat = sum_j sum_k t_k Y_jk / (10 * J)
                        t_broadcast = tj[np.newaxis, np.newaxis, :] # (1, 1, K)
                        b1_hat = np.sum(Y * t_broadcast, axis=(1, 2)) / (sum_t2 * J) # (R,)
                        
                        # OLS:
                        Y_bar = np.mean(Y, axis=(1, 2), keepdims=True)
                        e_ols = Y - (Y_bar + b1_hat[:, np.newaxis, np.newaxis] * t_broadcast)
                        df_ols = J * K - 2
                        s2_ols = np.sum(e_ols**2, axis=(1, 2)) / df_ols
                        sum_x_dev2 = sum_t2 * J # 10 * J
                        var_ols = s2_ols / sum_x_dev2
                        se_ols = np.sqrt(var_ols)
                        
                        # CR2:
                        # Cluster score: S_j = sum_{k=1}^K t_k (Y_jk - Y_bar_j - b1_hat * t_k)
                        # Note: sum_k t_k Y_bar_j = 0, sum_k t_k^2 = 10
                        # So S_j = sum_{k=1}^K t_k Y_jk - 10 * b1_hat
                        S_j = np.sum(Y * t_broadcast, axis=2) - sum_t2 * b1_hat[:, np.newaxis] # (R, J)
                        # Var_CR2 = 1 / (100 * J * (J - 1)) * sum_j S_j^2
                        ss_scores = np.sum(S_j**2, axis=1) # (R,)
                        var_cr2 = ss_scores / (sum_t2**2 * J * (J - 1))
                        se_cr2 = np.sqrt(var_cr2)
                        df_cr2 = J - 1
                        
                        # LMM REML:
                        # For within-subject orthogonal contrast, Var_LMM = MSW / (10 * J)
                        # dev_within = Y_jk - Y_bar_j - b1_hat * t_k
                        Y_bar_j = np.mean(Y, axis=2, keepdims=True) # (R, J, 1)
                        dev_within = Y - Y_bar_j - b1_hat[:, np.newaxis, np.newaxis] * t_broadcast
                        ss_w = np.sum(dev_within**2, axis=(1, 2))
                        df_w = J * (K - 1)
                        msw = ss_w / df_w
                        
                        # Between sum of squares to track singular fits
                        # ssb = K * sum_j (Y_bar_j - Y_bar)^2
                        ssb = K * np.sum((Y_bar_j - Y_bar)**2, axis=(1, 2))
                        df_b = J - 1
                        msb = ssb / df_b
                        singular = (msb <= msw)
                        
                        var_lmm = msw / (sum_t2 * J)
                        se_lmm = np.sqrt(var_lmm)
                        df_lmm = df_w # J * (K - 1) = 4J
                    
                    # Compute inferences
                    # 95% Confidence intervals
                    crit_ols = t_dist.ppf(0.975, df=df_ols)
                    crit_cr2 = t_dist.ppf(0.975, df=df_cr2)
                    crit_lmm = t_dist.ppf(0.975, df=df_lmm)
                    
                    ci_ols_l = b1_hat - crit_ols * se_ols
                    ci_ols_u = b1_hat + crit_ols * se_ols
                    
                    ci_cr2_l = b1_hat - crit_cr2 * se_cr2
                    ci_cr2_u = b1_hat + crit_cr2 * se_cr2
                    
                    ci_lmm_l = b1_hat - crit_lmm * se_lmm
                    ci_lmm_u = b1_hat + crit_lmm * se_lmm
                    
                    cov_ols = (ci_ols_l <= beta1) & (beta1 <= ci_ols_u)
                    cov_cr2 = (ci_cr2_l <= beta1) & (beta1 <= ci_cr2_u)
                    cov_lmm = (ci_lmm_l <= beta1) & (beta1 <= ci_lmm_u)
                    
                    # Test rejection at alpha = 0.05 (H0: beta1 = 0)
                    t_stat_ols = np.abs(b1_hat) / se_ols
                    t_stat_cr2 = np.abs(b1_hat) / se_cr2
                    t_stat_lmm = np.abs(b1_hat) / se_lmm
                    
                    reject_ols = t_stat_ols > crit_ols
                    reject_cr2 = t_stat_cr2 > crit_cr2
                    reject_lmm = t_stat_lmm > crit_lmm
                    
                    if beta1 == 0.50:
                        # Compute performance metrics
                        # Bias
                        bias_ols = np.mean(b1_hat) - beta1
                        bias_cr2 = np.mean(b1_hat) - beta1
                        bias_lmm = np.mean(b1_hat) - beta1
                        
                        # Empirical SD
                        s_beta = np.std(b1_hat, ddof=1)
                        mcse_bias = s_beta / np.sqrt(R)
                        
                        # Morris et al. (2019) SE Ratio: sqrt(mean(var)) / s_beta
                        ratio_ols = np.sqrt(np.mean(var_ols)) / s_beta
                        ratio_cr2 = np.sqrt(np.mean(var_cr2)) / s_beta
                        ratio_lmm = np.sqrt(np.mean(var_lmm)) / s_beta
                        
                        mean_se_ols = np.mean(se_ols)
                        mean_se_cr2 = np.mean(se_cr2)
                        mean_se_lmm = np.mean(se_lmm)
                        
                        # Coverage
                        p_cov_ols = np.mean(cov_ols)
                        p_cov_cr2 = np.mean(cov_cr2)
                        p_cov_lmm = np.mean(cov_lmm)
                        
                        mcse_cov_ols = np.sqrt(p_cov_ols * (1.0 - p_cov_ols) / R)
                        mcse_cov_cr2 = np.sqrt(p_cov_cr2 * (1.0 - p_cov_cr2) / R)
                        mcse_cov_lmm = np.sqrt(p_cov_lmm * (1.0 - p_cov_lmm) / R)
                        
                        # Power
                        power_ols = np.mean(reject_ols)
                        power_cr2 = np.mean(reject_cr2)
                        power_lmm = np.mean(reject_lmm)
                        
                        mcse_pwr_ols = np.sqrt(power_ols * (1.0 - power_ols) / R)
                        mcse_pwr_cr2 = np.sqrt(power_cr2 * (1.0 - power_cr2) / R)
                        mcse_pwr_lmm = np.sqrt(power_lmm * (1.0 - power_lmm) / R)
                        
                        # Singular fit rate
                        sing_rate = np.mean(singular) * 100.0
                        sing_count = np.sum(singular)
                        
                        # Split coverage by singular status if singular fits exist
                        if sing_count > 0 and sing_count < R:
                            cov_lmm_sing = np.mean(cov_lmm[singular])
                            cov_lmm_nonsing = np.mean(cov_lmm[~singular])
                        else:
                            cov_lmm_sing = np.nan
                            cov_lmm_nonsing = p_cov_lmm
                        
                        records_bias.append({
                            'Covariate_Type': cov, 'J': J, 'ICC': icc,
                            'Naive_OLS_Bias': bias_ols, 'Naive_OLS_MCSE': mcse_bias,
                            'CR2_Bias': bias_cr2, 'CR2_MCSE': mcse_bias,
                            'LMM_Bias': bias_lmm, 'LMM_MCSE': mcse_bias
                        })
                        
                        records_se.append({
                            'Covariate_Type': cov, 'J': J, 'ICC': icc,
                            'Empirical_SD': s_beta,
                            'OLS_Mean_SE': mean_se_ols, 'OLS_SE_Ratio': ratio_ols,
                            'CR2_Mean_SE': mean_se_cr2, 'CR2_SE_Ratio': ratio_cr2,
                            'LMM_Mean_SE': mean_se_lmm, 'LMM_SE_Ratio': ratio_lmm
                        })
                        
                        records_cov.append({
                            'Covariate_Type': cov, 'J': J, 'ICC': icc,
                            'OLS_Coverage': p_cov_ols, 'OLS_MCSE': mcse_cov_ols,
                            'CR2_Coverage': p_cov_cr2, 'CR2_MCSE': mcse_cov_cr2,
                            'LMM_Coverage': p_cov_lmm, 'LMM_MCSE': mcse_cov_lmm
                        })
                        
                        records_power.append({
                            'Covariate_Type': cov, 'J': J, 'ICC': icc,
                            'OLS_Power': power_ols, 'OLS_MCSE': mcse_pwr_ols,
                            'CR2_Power': power_cr2, 'CR2_MCSE': mcse_pwr_cr2,
                            'LMM_Power': power_lmm, 'LMM_MCSE': mcse_pwr_lmm
                        })
                        
                        records_singular.append({
                            'Covariate_Type': cov, 'J': J, 'ICC': icc,
                            'Singular_Count': sing_count,
                            'Singular_Rate_Pct': sing_rate,
                            'LMM_Cov_Overall': p_cov_lmm,
                            'LMM_Cov_Singular': cov_lmm_sing,
                            'LMM_Cov_NonSingular': cov_lmm_nonsing
                        })
                        
                    else: # beta1 == 0.0 (Type I error)
                        t1_ols = np.mean(reject_ols)
                        t1_cr2 = np.mean(reject_cr2)
                        t1_lmm = np.mean(reject_lmm)
                        
                        mcse_t1_ols = np.sqrt(t1_ols * (1.0 - t1_ols) / R)
                        mcse_t1_cr2 = np.sqrt(t1_cr2 * (1.0 - t1_cr2) / R)
                        mcse_t1_lmm = np.sqrt(t1_lmm * (1.0 - t1_lmm) / R)
                        
                        records_type1.append({
                            'Covariate_Type': cov, 'J': J, 'ICC': icc,
                            'OLS_Type1_Error': t1_ols, 'OLS_MCSE': mcse_t1_ols,
                            'CR2_Type1_Error': t1_cr2, 'CR2_MCSE': mcse_t1_cr2,
                            'LMM_Type1_Error': t1_lmm, 'LMM_MCSE': mcse_t1_lmm
                        })
    
    df_bias = pd.DataFrame(records_bias)
    df_se = pd.DataFrame(records_se)
    df_cov = pd.DataFrame(records_cov)
    df_type1 = pd.DataFrame(records_type1)
    df_power = pd.DataFrame(records_power)
    df_sing = pd.DataFrame(records_singular)
    
    return df_bias, df_se, df_cov, df_type1, df_power, df_sing

if __name__ == '__main__':
    df_bias, df_se, df_cov, df_type1, df_power, df_sing = run_simulation()
    print("=== Table 1: Bias ===")
    print(df_bias.to_string())
    print("\n=== Table 2: SE Accuracy (Morris Ratio) ===")
    print(df_se.to_string())
    print("\n=== Table 3: Coverage ===")
    print(df_cov.to_string())
    print("\n=== Table 4: Type I Error ===")
    print(df_type1.to_string())
    print("\n=== Table 5: Power ===")
    print(df_power.to_string())
    print("\n=== Singular Fits Diagnostic ===")
    print(df_sing.to_string())
