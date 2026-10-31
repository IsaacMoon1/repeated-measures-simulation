# Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Ordinary Least Squares, Linear Mixed-Effects, and Cluster-Robust Estimators

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![R: >=4.0.0](https://img.shields.io/badge/R-%3E%3D4.0.0-blue.svg)](https://www.r-project.org/)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![ADEMP: Morris et al. (2019)](https://img.shields.io/badge/Simulation-ADEMP%20Standard-success.svg)](https://doi.org/10.1002/sim.8086)

**Authors:** Adeyemi I. T.$^1$, Bamidele D. E.$^2$, Adisa Z. O.$^3$, Ademola O. R.$^4$  
**Affiliations:**  
- $^1,^2$ Department of Pure and Applied Mathematics, Ladoke Akintola University of Technology, P.M.B. 4000, Ogbomoso, Oyo State, Nigeria  
- $^3,^4$ Department of Science Laboratory Technology, Ladoke Akintola University of Technology, P.M.B. 4000, Ogbomoso, Oyo State, Nigeria  
**Corresponding Author Email:** [isaacadeyemi245@gmail.com](mailto:isaacadeyemi245@gmail.com)

---

## Overview
This repository contains the complete reproducible simulation routines, publication figures, CSV result tables, and manuscript source files for the methodological paper:

> **Adeyemi, I. T., Bamidele, D. E., Adisa, Z. O., & Ademola, O. R. (2026). Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Ordinary Least Squares, Linear Mixed-Effects, and Cluster-Robust Estimators.**

The study examines the inferential consequences of ignoring repeated measures clustering across varying sample sizes and correlation strengths. Following the **ADEMP** protocol (Morris et al., 2019), we conduct a full-factorial Monte Carlo simulation crossing:
- Cluster counts ($J \in \{10, 30, 100\}$)
- Intraclass correlation coefficients ($\text{ICC} \in \{0.10, 0.50\}$)
- Covariate structures (Between-subject binary vs. Within-subject centered linear time)
- Effect sizes ($H_0: \beta_1 = 0$ for Type I error; $H_1: \beta_1 = 0.50$ for bias, SE accuracy, coverage, and power)
- Replications: $R = 2,000$ per condition ($48,000$ simulated datasets total; master seed `20261031`).

We contrast three primary estimators:
1. **Naive Ordinary Least Squares (OLS)** (complete pooling, assuming i.i.d. errors)
2. **Linear Mixed-Effects Models (LMM)** via Restricted Maximum Likelihood (REML) with Satterthwaite degrees of freedom (`lme4` / `lmerTest`)
3. **Cluster-Robust Variance Estimation (CR2)** using bias-reduced linearization and Satterthwaite reference distributions (`clubSandwich`)

Additionally, we re-analyze the benchmark psychomotor vigilance sleep deprivation trial (*Belenky et al., 2003*; $N = 180, J = 18$).

---

## Key Methodological Findings
- **Unbiased Point Estimation:** All three estimators return strictly unbiased and numerically identical point estimates under balanced orthogonal designs ($\text{Bias} < 0.009$; $95\%$ CI includes 0).
- **Between-Subject Failure of OLS:** For subject-level covariates at $\text{ICC} = 0.50$, naive OLS underestimates true standard errors by over 40% ($\text{SE Ratio} \approx 0.55\text{--}0.58$), collapsing 95% confidence interval coverage to **71.8%–74.2%** and inflating Type I error rates to **26.0%–28.0%** (nominal $\alpha = 0.05$).
- **Within-Subject Conservatism of OLS:** For centered within-subject predictors, naive OLS overestimates standard errors ($\text{SE Ratio} \approx 1.39\text{--}1.47$), resulting in excessively wide confidence intervals (**99.2%–99.4%** coverage) and deflated Type I error rates (**0.6%–1.2%**).
- **Equivalence of LMM and CR2:** Both REML-estimated LMMs and small-sample adjusted CR2 estimators maintain close-to-nominal coverage (**94.4%–96.0%**) and controlled Type I error rates (**4.3%–5.8%**) down to $J = 10$ clusters, strictly within Bradley's (1978) liberal robustness bounds $[0.025, 0.075]$.
- **Singular Boundary Fits in REML:** Boundary solutions ($\hat{\sigma}_u^2 < 10^{-4}$) occurred primarily under weak clustering ($\text{ICC} = 0.10$) and small cluster counts ($24.5\%$ at $J = 10$). Conditioning coverage on singular status reveals that singular fits cause modest undercoverage for between-subject factors ($87.7\%\text{--}91.6\%$), but leave within-subject inference fully robust ($96.1\%\text{--}96.8\%$) due to parameter orthogonality.
- **Sleep Study Benchmark:** In the Belenky et al. (2003) dataset ($N = 180, J = 18$), CR2 reproduced the standard error of a maximal random-slope model ($\text{SE} = 1.546, \text{df} = 17$) without requiring explicit parametric specification of the random-effects covariance structure.

---

## Repository Structure

```text
repeated-measures-simulation/
├── figures/
│   ├── figure1_coverage.png           # 300 DPI 95% CI Coverage Plot across factorial grid
│   └── figure2_type1_error.png        # 300 DPI Empirical Type I error rate plot with Bradley's bounds
├── tables/
│   ├── table1_bias.csv                # Empirical bias & MCSE across all 12 alternative scenarios
│   ├── table2_se_accuracy.csv         # Decomposed Empirical SD, Mean SE, and Morris SE ratios
│   ├── table3_coverage.csv            # 95% Confidence interval coverage probabilities & MCSE
│   ├── table4_type1_error.csv         # Empirical Type I error rates under sharp null (beta1 = 0)
│   ├── table5_power.csv               # Empirical statistical power under beta1 = 0.50
│   ├── table_singular_fits.csv        # REML singular boundary fit rates & conditional coverage
│   ├── table6_sleepstudy.csv          # Empirical estimates and CIs for sleep deprivation models
│   └── table7_decision_pathway.csv    # Practical analytical decision framework
├── simulation_study_repeated_measures.R  # Primary reproducible R simulation script
├── run_complete_simulation.py         # Complete Python simulation engine (R=2,000, 48,000 datasets)
├── export_tables_csv.py               # Script exporting publication CSV tables
├── generate_figures.py                # Publication figure generation script (300 DPI)
├── rebuild_paper.py                   # Automated Microsoft Word (.docx) publication builder
├── requirements.txt                   # Python environment dependencies
├── Adeyemi_Repeated_Measures_Simulation_Paper.md   # Publication manuscript (Academic Markdown)
├── Adeyemi_Repeated_Measures_Simulation_Paper.docx # Formatted manuscript (Microsoft Word)
├── LICENSE                            # MIT License
└── README.md                          # Repository documentation
```

---

## Replication Instructions

### Option A: Running the Python Pipeline (R = 2,000 Replications)
```bash
# Clone the repository
git clone https://github.com/IsaacMoon1/repeated-measures-simulation.git
cd repeated-measures-simulation

# Install Python dependencies
pip install -r requirements.txt

# Run complete Monte Carlo simulation and export CSV tables
python export_tables_csv.py

# Re-generate 300 DPI publication figures
python generate_figures.py

# Rebuild publication Microsoft Word document
python rebuild_paper.py
```

### Option B: Running the R Simulation Pipeline
Ensure R (version $\ge 4.0.0$) is installed with `lme4`, `lmerTest`, and `clubSandwich`.
```r
source("simulation_study_repeated_measures.R")
```

---

## Citation
If you utilize this simulation architecture or findings in your methodological research, please cite:

```bibtex
@article{adeyemi2026repeated,
  author    = {Adeyemi, Isaac T. and Bamidele, D. E. and Adisa, Z. O. and Ademola, O. R.},
  title     = {Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Ordinary Least Squares, Linear Mixed-Effects, and Cluster-Robust Estimators},
  journal   = {Methodological Preprint},
  year      = {2026},
  institution = {Ladoke Akintola University of Technology (LAUTECH)},
  url       = {https://github.com/IsaacMoon1/repeated-measures-simulation}
}
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
