# Repeated Measures Simulation Study: Naive OLS, Linear Mixed Models, and CR2 Cluster-Robust Variance Estimation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![R: >=4.0.0](https://img.shields.io/badge/R-%3E%3D4.0.0-blue.svg)](https://www.r-project.org/)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![ADEMP: Morris et al. (2019)](https://img.shields.io/badge/Simulation-ADEMP%20Standard-success.svg)](https://doi.org/10.1002/sim.8086)

**Author:** Isaac T. Adeyemi  
**Affiliation:** Department of Pure and Applied Mathematics / Statistics, Ladoke Akintola University of Technology (LAUTECH), Ogbomoso, Nigeria  
**Corresponding Email:** [isaacadeyemi245@gmail.com](mailto:isaacadeyemi245@gmail.com)

---

## Overview
This repository houses the reproducible code, simulation engine, figure generators, and dataset archives for the research paper:

> **Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Independent and Mixed-Effects Models**

The study investigates the inferential consequences of ignoring nested longitudinal correlation structures. Using a 24-scenario factorial Monte Carlo simulation adhering strictly to the **ADEMP** protocol (Morris et al., 2019), we contrast:
1. **Naive Ordinary Least Squares (OLS)** (complete pooling, assuming i.i.d. errors)
2. **Linear Mixed-Effects Models (LMM)** estimated via Restricted Maximum Likelihood (REML) with Satterthwaite degrees-of-freedom approximations (`lme4` / `lmerTest`)
3. **Cluster-Robust Variance Estimation (CR2)** using bias-reduced linearization and Satterthwaite reference distributions (`clubSandwich`)

The study also includes an empirical benchmark re-analyzing the classic psychomotor vigilance sleep deprivation trial (*Belenky et al., 2003*).

---

## Key Methodological Findings
- **Unbiased Point Estimation:** All three estimators return mathematically identical and unbiased point estimates ($\text{Bias} < 0.008$) under balanced orthogonal designs.
- **Between-Subject Failure of OLS:** For subject-level covariates at $\text{ICC} = 0.50$, naive OLS underestimates sampling variability by $>40\%$ ($\text{SE Ratio} \approx 0.55$), causing 95% confidence interval coverage to collapse to **73.0%** and false-positive Type I error rates to surge to **27.8%** (nominal $\alpha = 0.05$).
- **Within-Subject Conservatism of OLS:** For centered within-subject time predictors, naive OLS overestimates standard errors ($\text{SE Ratio} \approx 1.45$), yielding overly conservative coverage (**99.8%**) and attenuated statistical power.
- **Equivalence of LMM and CR2:** Both REML-estimated LMMs and small-sample adjusted CR2 estimators maintain close-to-nominal coverage (**93.6%–98.0%**) and controlled Type I error rates (**3.6%–6.4%**) down to $J = 10$ clusters.
- **Sleep Study Benchmark:** In the Belenky et al. dataset ($N = 180, J = 18$), CR2 reproduced the standard error of a maximal random-slope model ($\text{SE} = 1.546, \text{df} = 17$) without requiring explicit parameterization of the random-effects covariance matrix.

---

## Repository Structure

```text
├── figures/
│   ├── figure1_coverage.png           # 300 DPI 95% CI Coverage Plot across factorial grid
│   └── figure2_type1_error.png        # 300 DPI Empirical Type I error rate plot with robustness bands
├── tables/
│   ├── table1_bias.csv                # Empirical bias & MCSE across all 12 alternative scenarios
│   ├── table2_se_accuracy.csv         # Empirical SD, Mean SE, and Moulton SE ratios
│   ├── table3_coverage.csv            # 95% Confidence interval coverage probabilities
│   ├── table4_type1_error.csv         # Empirical Type I error rates under sharp null (beta1 = 0)
│   ├── table5_power.csv               # Statistical power under beta1 = 0.50
│   ├── table6_sleepstudy.csv          # Empirical estimates and CIs for sleep deprivation models
│   └── table7_decision_pathway.csv    # Practical analytical decision framework
├── simulation_study_repeated_measures.R  # Primary reproducible R simulation script
├── run_simulation_ademp.py           # Primary Python simulation pipeline & singular fit audit
├── generate_figures.py                # Publication figure generation script (300 DPI)
├── requirements.txt                   # Python environment dependencies
├── Adeyemi_Repeated_Measures_Simulation_Paper.md   # Publication manuscript (Academic Markdown)
├── Adeyemi_Repeated_Measures_Simulation_Paper.docx # Formatted manuscript (Microsoft Word)
└── README.md                          # Repository documentation
```

---

## Replication Instructions

### Option A: Running the R Simulation Pipeline
Ensure R (version $\ge 4.0.0$) is installed.
```r
# Install required packages
install.packages(c("lme4", "lmerTest", "clubSandwich"))

# Run the simulation & empirical re-analysis
source("simulation_study_repeated_measures.R")
```

### Option B: Running the Python Pipeline & Figure Generator
```bash
# Clone the repository
git clone https://github.com/isaacadeyemi/repeated-measures-simulation.git
cd repeated-measures-simulation

# Install Python dependencies
pip install -r requirements.txt

# Run simulation & export table CSVs
python run_simulation_ademp.py

# Re-generate 300 DPI publication figures
python generate_figures.py
```

---

## Citation
If you utilize this simulation architecture or findings in your methodological research, please cite:

```bibtex
@article{adeyemi2026repeated,
  author    = {Adeyemi, Isaac T.},
  title     = {Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Independent and Mixed-Effects Models},
  journal   = {Methodological Preprint},
  year      = {2026},
  institution = {Ladoke Akintola University of Technology (LAUTECH)}
}
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
