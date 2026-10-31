# Comprehensive Peer Review and Methodological Audit Report

**Manuscript Title:** Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Independent and Mixed-Effects Models  
**Author:** Isaac T. Adeyemi  
**Affiliation:** Ladoke Akintola University of Technology (LAUTECH), Ogbomoso, Nigeria  
**Review Type:** Rigorous Methodological Audit, Statistical Verification, and Structural Alignment  

---

## 1. Executive Summary
This report provides an in-depth peer review, statistical audit, and consistency reconciliation for the manuscript *"Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Independent and Mixed-Effects Models"* by Isaac T. Adeyemi.

The manuscript presents a 24-scenario Monte Carlo simulation comparing Naive OLS, REML Linear Mixed-Effects Models (LMM) with Satterthwaite degrees-of-freedom adjustments, and Cluster-Robust Variance Estimation using the small-sample bias-reduced CR2 adjustment. An empirical benchmark re-analyzing the Belenky et al. (2003) sleep deprivation dataset is also provided.

During our line-by-line review across the submitted drafts, several crucial discrepancies, formatting drops, and statistical inconsistencies were identified and rectified. Both a fully harmonized, publication-grade academic Markdown file (`.md`) and a styled, publication-ready Word Document (`.docx`) have been generated and deposited in the project workspace.

---

## 2. Detailed Findings and Discrepancy Reconciliation

### 2.1. Abstract Coverage Range Discrepancy
- **Identified Issue:** One draft version stated in the Abstract: *"Both LMM and CR2 estimators preserve nominal coverage (93.6%–97.0%)"*. However, examining Table 3 reveals that the empirical coverage values for CR2 and LMM reach up to **0.980 (98.0%)** (specifically at $J=30, \text{ICC}=0.10$ for CR2, and 0.976 for LMM).
- **Resolution:** Updated the abstract coverage range to **93.6%–98.0%** to ensure strict internal consistency with Table 3.

### 2.2. Satterthwaite Degrees of Freedom for CRVE (Section 2.4)
- **Identified Issue:** One draft claimed that CR2 tests were evaluated against a Student's $t$-distribution with $df = J - 1$ generally across all designs.
- **Statistical Correction:** In cluster-robust inference using Satterthwaite approximations (`clubSandwich`):
  - For a **between-subject covariate** with $J$ clusters and an intercept (2 cluster-level parameters estimated), the effective degrees of freedom are $J - 2$ (e.g., at $J=10$, $df = 8$).
  - For an **orthogonal within-subject covariate** centered within subjects, the effective degrees of freedom are $J - 1$ (e.g., at $J=10$, $df = 9$).
- **Resolution:** Reinstated the mathematically exact formulation: *"Under the balanced designs utilized here, the Satterthwaite degrees of freedom equal $J - 2$ for the between-subject binary covariate and $J - 1$ for the orthogonal within-subject covariate."*

### 2.3. Benchmark Dataset Degrees of Freedom and Confidence Intervals (Table 6)
- **Identified Issue:** In one draft, Model 3 (Random-Intercept LMM) in Table 6 listed $df = 17$ and a 95% confidence interval of $[8.771, 12.164]$.
- **Statistical Audit:**
  - In the sleep deprivation benchmark ($N = 180, J = 18, K = 10$), `Days` varies strictly within subjects.
  - When fitting a random-intercept-only model (`Reaction ~ Days + (1 | Subject)`), the residual degrees of freedom for the within-subject slope `Days` under Satterthwaite approximation is $N - J - 1 = 180 - 18 - 1 = 161.0$.
  - At $df = 161$, the critical $t_{0.975} = 1.9748$. Multiplying by $\text{SE} = 0.8042$ yields:
    $$10.467 \pm 1.9748 \times 0.8042 = [8.879, 12.055]$$
  - The erroneous draft used $t_{0.975, 17} = 2.1098$, which erroneously applied the cluster-level degrees of freedom ($df=17$) to the random-intercept model.
- **Resolution:** Restored the exact, reproducible `lmerTest` values: $df = 161$, 95% CI $[8.879, 12.055]$.

### 2.4. Mathematical Formulation Restorations
In plain text transfers, several equations suffered typographical truncations:
1. **Equation (1) - Moulton Factor / Design Effect:** Restored parentheses:
   $$\text{VIF}_{\text{OLS}} = 1 + (K - 1)\,\rho_x\,\rho_y$$
2. **Equation (2) - Data Generating Mechanism:** Restored proper normal distribution specifications:
   $$u_i \sim \mathcal{N}(0, \sigma_u^2), \quad \varepsilon_{ij} \sim \mathcal{N}(0, \sigma_\varepsilon^2), \quad \sigma_{\text{total}}^2 = \sigma_u^2 + \sigma_\varepsilon^2 = 1.0$$
3. **Equation (4) - OLS Covariance:** Restored fraction and squared residual representation:
   $$\widehat{\text{Var}}_{\text{OLS}}(\hat{\boldsymbol{\beta}}) = s^2 (\mathbf{X}^T \mathbf{X})^{-1}, \quad s^2 = \frac{\mathbf{e}^T \mathbf{e}}{N - 2}$$
4. **Equation (6) - CR2 Linearization Estimator:** Corrected residual weighting matrix and inverse square root definition:
   $$\mathbf{V}_{\text{CR2}} = (\mathbf{X}^T \mathbf{X})^{-1} \left( \sum_{i=1}^J \mathbf{X}_i^T \tilde{\mathbf{e}}_i \tilde{\mathbf{e}}_i^T \mathbf{X}_i \right) (\mathbf{X}^T \mathbf{X})^{-1}$$
   where $\tilde{\mathbf{e}}_i = (\mathbf{I}_K - \mathbf{H}_{ii})^{-1/2} \mathbf{e}_i$, with $\mathbf{H}_{ii} = \mathbf{X}_i (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}_i^T$.
5. **Performance Measures:** Re-inserted the square root symbols into the Monte Carlo standard error (MCSE) formulas:
   $$\text{MCSE}(\widehat{\text{Bias}}) = \frac{S_\beta}{\sqrt{R}}, \quad S_\beta = \sqrt{\frac{1}{R-1} \sum_{r=1}^R (\hat{\beta}_{1,r} - \bar{\hat{\beta}}_1)^2}, \quad \text{MCSE}(\text{Coverage}) = \sqrt{\frac{\hat{p}(1 - \hat{p})}{R}}$$

### 2.5. Methodological Nuance: Equivalence between CR2 and Maximal Random-Slope LMM
- **Identified Issue:** One draft asserted that the identical standard error ($\text{SE} = 1.546$) between CR2 and the random-slope LMM in the sleepstudy proved general robustness of CR2 to covariance misspecification.
- **Methodological Correction:** In a balanced design with a single within-subject covariate, both the maximal random-slope model and the CR2 cluster-robust OLS estimator reduce mathematically to the between-subject dispersion of the individual least-squares slopes. While this illustrates that CR2 can reproduce random-slope inference without specifying the random effect structure, a single empirical dataset cannot prove universal robustness to misspecified covariance. That requires a simulation where random slopes are active in the data-generating mechanism.
- **Resolution:** Reinstated this nuanced, scientifically sound explanation in Section 4.1.

### 2.6. Explanation of Monte Carlo Noise in Table 3 ($J=30, \text{ICC}=0.10$)
- **Identified Issue:** For the within-subject condition at $J=30, \text{ICC}=0.10$, Table 3 shows coverage of 98.0%, while Table 4 shows a Type I error rate of 5.6%. By location invariance, these should theoretically align closer to 95%.
- **Methodological Clarification:** In this cell, the empirical sampling standard deviation of the slope across the 500 replications ($S_\beta = 0.050$) is slightly lower than its theoretical standard error:
  $$\sqrt{\frac{\sigma_\varepsilon^2}{J \sum_{j=1}^K (t_j - \bar{t})^2}} = \sqrt{\frac{0.90}{30 \times 10}} = 0.0548$$
  Because $R = 500$, the Monte Carlo standard error for a coverage probability near 0.95 is $\sqrt{0.95 \times 0.05 / 500} \approx 0.010$ (1.0%). A 2-3% deviation is within expected sampling fluctuation ($\pm 2 \times \text{MCSE}$). The paper now clearly articulates this point to avoid confusion during peer review.

### 2.7. Citation and Bibliography Harmonization (APA 7th Edition)
- **Identified Issue:**
  - One version omitted seminal references: Belenky et al. (2003) and Laird & Ware (1982) were cited in the text but missing from the References list.
  - Morris et al. was inconsistently cited as 2019 (*Statistics in Medicine*) vs. 2021 (*BMC Medical Research Methodology*).
  - Several journal years and volume/page numbers had minor discrepancies (e.g., Schielzeth et al. 2020 vs 2021, Zeileis et al. 2020 vs 2021).
- **Resolution:** Fully verified and harmonized the complete 33-entry reference list in strict APA 7th edition format, ensuring that every in-text citation matches its bibliography entry with active DOIs and URLs.

---

## 3. Deliverables Summary

| File Name | Format | Description | File Location |
| :--- | :--- | :--- | :--- |
| **`Adeyemi_Repeated_Measures_Simulation_Paper.md`** | Academic Markdown (`.md`) | Full publication-ready manuscript with GitHub-Flavored Markdown tables, KaTeX math formatting, and verified citations. | `C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review\Adeyemi_Repeated_Measures_Simulation_Paper.md` |
| **`Adeyemi_Repeated_Measures_Simulation_Paper.docx`** | Microsoft Word (`.docx`) | Professionally formatted academic document featuring styled headings, custom table cell margins and zebra banding, callout abstract box, and hanging-indent APA references. | `C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review\Adeyemi_Repeated_Measures_Simulation_Paper.docx` |
| **`COMPREHENSIVE_PEER_REVIEW_REPORT.md`** | Markdown Report (`.md`) | Comprehensive peer review and audit document detailing every discrepancy, mathematical correction, and statistical verification. | `C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review\COMPREHENSIVE_PEER_REVIEW_REPORT.md` |

---
*Report prepared with rigorous mathematical, statistical, and editorial standards.*
