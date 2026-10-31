# ==============================================================================
# Title: Statistical Analysis of Repeated Measures Data: A Simulation Study
# Authors: Adeyemi I. T., Bamidele D. E., Adisa Z. O., Ademola O. R.
# Institution: Ladoke Akintola University of Technology (LAUTECH)
# Description: Reproducible R simulation script adhering to the ADEMP protocol
#              and re-analysis of the Belenky et al. (2003) sleepstudy benchmark.
# ==============================================================================

# Required Libraries
suppressPackageStartupMessages({
  if (!requireNamespace("lme4", quietly = TRUE)) install.packages("lme4")
  if (!requireNamespace("lmerTest", quietly = TRUE)) install.packages("lmerTest")
  if (!requireNamespace("clubSandwich", quietly = TRUE)) install.packages("clubSandwich")
  
  library(lme4)
  library(lmerTest)
  library(clubSandwich)
})

set.seed(20261031)

# ------------------------------------------------------------------------------
# 1. Empirical Benchmark: Sleep Deprivation Case Study (Belenky et al., 2003)
# ------------------------------------------------------------------------------
cat("\n=======================================================\n")
cat("1. RE-ANALYSIS OF SLEEP DEPRIVATION BENCHMARK (N=180, J=18)\n")
cat("=======================================================\n")

data("sleepstudy", package = "lme4")

# Model 1: Naive OLS (complete pooling)
m1_ols <- lm(Reaction ~ Days, data = sleepstudy)
s1 <- summary(m1_ols)
ci1 <- confint(m1_ols)["Days", ]

# Model 2: Cluster-robust OLS (CR2)
m2_cr2 <- coef_test(m1_ols, vcov = "CR2", cluster = sleepstudy$Subject, test = "Satterthwaite")
ci2 <- conf_int(m1_ols, vcov = "CR2", cluster = sleepstudy$Subject, test = "Satterthwaite")
ci2_days <- ci2[ci2$Coef == "Days", c("CI_L", "CI_U")]

# Model 3: LMM (random intercept only)
m3_ri <- lmer(Reaction ~ Days + (1 | Subject), data = sleepstudy, REML = TRUE)
s3 <- summary(m3_ri)
ci3_est <- fixef(m3_ri)["Days"]
ci3_se <- coef(s3)["Days", "Std. Error"]
ci3_df <- coef(s3)["Days", "df"]
ci3 <- ci3_est + c(-1, 1) * qt(0.975, df = ci3_df) * ci3_se

# Model 4: Maximal LMM (random slope & intercept)
m4_rs <- lmer(Reaction ~ Days + (Days | Subject), data = sleepstudy, REML = TRUE)
s4 <- summary(m4_rs)
ci4_est <- fixef(m4_rs)["Days"]
ci4_se <- coef(s4)["Days", "Std. Error"]
ci4_df <- coef(s4)["Days", "df"]
ci4 <- ci4_est + c(-1, 1) * qt(0.975, df = ci4_df) * ci4_se

results_sleep <- data.frame(
  Model = c("1. Naive OLS", "2. Cluster-Robust CR2", "3. LMM Random Intercept", "4. LMM Random Slope & Intercept"),
  Estimate = c(coef(m1_ols)["Days"], coef(m1_ols)["Days"], ci3_est, ci4_est),
  Std_Error = c(coef(s1)["Days", "Std. Error"], m2_cr2["Days", "SE"], ci3_se, ci4_se),
  df = c(m1_ols$df.residual, m2_cr2["Days", "df"], ci3_df, ci4_df),
  p_val = c(coef(s1)["Days", "Pr(>|t|)"], m2_cr2["Days", "p_Satt"], coef(s3)["Days", "Pr(>|t|)"], coef(s4)["Days", "Pr(>|t|)"]),
  CI_Lower = c(ci1[1], ci2_days$CI_L, ci3[1], ci4[1]),
  CI_Upper = c(ci1[2], ci2_days$CI_U, ci3[2], ci4[2])
)
print(results_sleep, digits = 4)

# ------------------------------------------------------------------------------
# 2. Monte Carlo Simulation Engine (ADEMP Protocol)
# ------------------------------------------------------------------------------
cat("\n=======================================================\n")
cat("2. RUNNING ADEMP MONTE CARLO SIMULATION PIPELINE\n")
cat("=======================================================\n")

run_cell <- function(J = 10, K = 5, icc = 0.50, cov_type = "Between", beta1 = 0.50, R = 500) {
  sigma_u <- sqrt(icc)
  sigma_eps <- sqrt(1 - icc)
  
  tj <- c(-2, -1, 0, 1, 2)
  sum_t2 <- sum(tj^2)
  
  ols_res <- matrix(NA, nrow = R, ncol = 3) # est, se, cover
  cr2_res <- matrix(NA, nrow = R, ncol = 3)
  lmm_res <- matrix(NA, nrow = R, ncol = 3)
  singular_count <- 0
  
  for (r in 1:R) {
    u_i <- rnorm(J, mean = 0, sd = sigma_u)
    
    if (cov_type == "Between") {
      Z_i <- rep(c(0, 1), each = J / 2)
      x_mat <- matrix(rep(Z_i, each = K), nrow = J, byrow = TRUE)
    } else {
      x_mat <- matrix(rep(tj, J), nrow = J, byrow = TRUE)
    }
    
    eps_mat <- matrix(rnorm(J * K, mean = 0, sd = sigma_eps), nrow = J, ncol = K)
    y_mat <- beta1 * x_mat + matrix(rep(u_i, K), nrow = J, ncol = K) + eps_mat
    
    # Flatten
    df_sim <- data.frame(
      Subject = factor(rep(1:J, each = K)),
      x = as.vector(t(x_mat)),
      y = as.vector(t(y_mat))
    )
    
    # 1. Naive OLS
    m_ols <- lm(y ~ x, data = df_sim)
    b_ols <- coef(m_ols)["x"]
    se_ols <- summary(m_ols)$coefficients["x", "Std. Error"]
    df_ols <- m_ols$df.residual
    ci_ols <- b_ols + c(-1, 1) * qt(0.975, df = df_ols) * se_ols
    ols_res[r, ] <- c(b_ols, se_ols, as.numeric(ci_ols[1] <= beta1 && beta1 <= ci_ols[2]))
    
    # 2. CR2
    t_cr2 <- coef_test(m_ols, vcov = "CR2", cluster = df_sim$Subject, test = "Satterthwaite")
    se_cr2 <- t_cr2["x", "SE"]
    df_cr2 <- t_cr2["x", "df"]
    ci_cr2 <- b_ols + c(-1, 1) * qt(0.975, df = df_cr2) * se_cr2
    cr2_res[r, ] <- c(b_ols, se_cr2, as.numeric(ci_cr2[1] <= beta1 && beta1 <= ci_cr2[2]))
    
    # 3. LMM REML
    m_lmm <- lmer(y ~ x + (1 | Subject), data = df_sim, REML = TRUE)
    b_lmm <- fixef(m_lmm)["x"]
    s_lmm <- summary(m_lmm)
    se_lmm <- coef(s_lmm)["x", "Std. Error"]
    df_lmm <- coef(s_lmm)["x", "df"]
    ci_lmm <- b_lmm + c(-1, 1) * qt(0.975, df = df_lmm) * se_lmm
    lmm_res[r, ] <- c(b_lmm, se_lmm, as.numeric(ci_lmm[1] <= beta1 && beta1 <= ci_lmm[2]))
    
    # Track singular
    vc <- as.data.frame(VarCorr(m_lmm))
    sig_u2 <- vc[vc$grp == "Subject", "vcov"]
    if (sig_u2 < 1e-4) singular_count <- singular_count + 1
  }
  
  cat(sprintf("[%s | J=%d | ICC=%.2f] Singular Fits: %d/%d (%.1f%%) | OLS Cov: %.3f | CR2 Cov: %.3f | LMM Cov: %.3f\n",
              cov_type, J, icc, singular_count, R, (singular_count / R) * 100,
              mean(ols_res[, 3]), mean(cr2_res[, 3]), mean(lmm_res[, 3])))
}

# Run sample test scenarios
run_cell(J = 10, K = 5, icc = 0.50, cov_type = "Between", beta1 = 0.50, R = 100)
run_cell(J = 10, K = 5, icc = 0.10, cov_type = "Between", beta1 = 0.50, R = 100)
run_cell(J = 10, K = 5, icc = 0.50, cov_type = "Within", beta1 = 0.50, R = 100)

cat("\nSimulation test complete. For production R=500 runs, execute with parallel clusters.\n")
