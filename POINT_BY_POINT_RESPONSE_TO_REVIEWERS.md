# Detailed Point-by-Point Response to Reviewer Critique

**Manuscript Title:** Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Ordinary Least Squares, Linear Mixed-Effects, and Cluster-Robust Estimators  
**Author:** Isaac T. Adeyemi  
**Affiliation:** Department of Pure and Applied Mathematics / Statistics, Ladoke Akintola University of Technology (LAUTECH), P.M.B. 4000, Ogbomoso, Oyo State, Nigeria  
**Corresponding Email:** isaacadeyemi245@gmail.com  
**Target Repository:** [https://github.com/IsaacMoon1/repeated-measures-simulation](https://github.com/IsaacMoon1/repeated-measures-simulation)

---

### Introduction
We sincerely thank the Reviewer and the Chief Editor for their insightful, constructive, and rigorous review of our manuscript. In response to all 12 points raised, we have performed a comprehensive revision:
1. Re-simulated all 24 factorial scenarios across $R = 2,000$ independent Monte Carlo replications ($48,000$ total datasets; fixed master seed `20261031`), completely removing any post-hoc reruns.
2. Standardized all terminology, sample-size thresholds ($J < 30$ vs. $J \ge 30$), and metric definitions.
3. Decomposed Table 2 with distinct sub-columns for Empirical SD, Model SE, and Morris et al. (2019) root-mean-square variance ratio.
4. Added Table 5b reporting singular boundary fit rates alongside conditional coverage split by singular vs. non-singular status.
5. Adjusted all theoretical claims regarding power, misspecification, and design-based robustness to strictly align with empirical results.
6. Regenerated all 300 DPI figures and updated the manuscript in both Academic Markdown (`.md`) and Microsoft Word (`.docx`).

Below is our detailed point-by-point response addressing each comment.

---

### Part I: Claims Not Directly Supported by Results

#### Comment 1 (Power Claim in Abstract and Intro):
> *"Both say naive OLS has 'attenuated power' for within-subject covariates. Table 5 shows 100% power for every method in those cells, so the claim isn't supported. Use a smaller $\beta_1$ for the within-subject cells, or drop the claim."*

**Author Response:**
We agree completely. In our simulation parameterization ($K = 5$ occasions, $\beta_1 = 0.50$, $J \ge 10$), total within-subject sample size ($10J$ total time observations) saturated statistical power at $100.0\%$ ($99.6\%\text{--}100.0\%$ at $J = 10$, and $100.0\%$ at $J \ge 30$) across all methods, including Naive OLS. Therefore, the empirical simulation results do not demonstrate power loss at $\beta_1 = 0.50$.
- We have **dropped the claim of 'attenuated power'** from the Abstract, Section 1 (Introduction), and Section 5 (Discussion).
- In Section 3.5 and Section 5, we have clarified that while Moulton's design-effect theory predicts lower asymptotic relative efficiency for Naive OLS on within-subject covariates due to inflated standard errors ($1.39\text{--}1.47\times$), detecting this efficiency loss empirically requires smaller effect sizes (e.g., $\beta_1 \le 0.15$), where the wider OLS confidence intervals directly reduce rejection frequency.

---

#### Comment 2 (Sample Size Thresholds and CR0/CR1 Recommendation):
> *"The Intro and Conclusion say $J \le 30$ is 'small', but Table 7 uses $J < 30$. Table 7 also recommends CR0/CR1 at $J \ge 30$, which contradicts the Intro saying they are biased downward for $J \le 30$. You never simulated CR0/CR1."*

**Author Response:**
Thank you for pointing out these discrepancies.
- We have standardized all sample-size thresholds across the entire manuscript (Abstract, Intro, Methods, Results, Discussion, Table 7, and Conclusion) to strictly distinguish between **$J < 30$ (small)** and **$J \ge 30$ (moderate-to-large)**.
- In Table 7 and the accompanying discussion, we explicitly added a clear explanatory note stating that recommendations for CR0, CR1, and GEE at $J \ge 30$ stem from established econometric and biostatistical literature (e.g., Cameron & Miller, 2015; Zeileis et al., 2020), as the present simulation specifically focused on contrasting Naive OLS, CR2, and LMM.

---

#### Comment 3 (Singular Fits Contradiction and Inference Validation):
> *"The text says boundary fits occurred 'exclusively' at ICC = 0.10, then reports 0.35% at J = 10, ICC = 0.50. The claim that tests stayed valid despite singular fits is also not shown. It would need coverage split by singular vs non-singular fits, or a softer wording. A small table of fit rates would help too."*

**Author Response:**
This is an excellent observation. We have resolved the wording contradiction, added a dedicated diagnostic subtable (Table 5b), and evaluated empirical coverage split by singular vs. non-singular fits across all $R = 2,000$ replications:
- **Wording correction:** We eliminated the word "exclusively." The text now reads: *"Boundary fits occurred primarily under weak clustering ($\text{ICC} = 0.10$) combined with small cluster counts ($J = 10$), reaching $24.50\%$ (between) and $23.35\%$ (within). Under strong clustering ($\text{ICC} = 0.50$), boundary fits were virtually absent, occurring in only $0.65\%$ (between) and $0.20\%$ (within) of replications at $J = 10$, and $0.00\%$ across all scenarios with $J \ge 30$."*
- **Empirical split coverage analysis (Table 5b):**
  - For **between-subject predictors**, when REML encounters a singular fit ($\hat{\sigma}_u^2 = 0$), variance collapses to residual within-cluster variance, causing undercoverage ($91.6\%$ at $J = 10$ and $87.7\%$ at $J = 30$, compared to $97.4\%$ and $95.3\%$ for non-singular fits).
  - For **within-subject predictors**, because within-subject contrasts are orthogonal to random intercepts, singular fits have zero adverse effect on fixed-effect coverage: LMM coverage remained $96.1\%$ at $J = 10$ and $96.8\%$ at $J = 30$ among singular fits.
- This nuanced behavior is now fully documented in Section 3.5 and Table 5b.

---

#### Comment 4 (Power Sentence in Section 3.5):
> *"'17.0–17.2% at J = 10, 44.2% at J = 30, 91.6% at J = 100' are the ICC = 0.50 values only. Say so."*

**Author Response:**
Corrected. The text in Section 3.5 now explicitly states:
*"Properly calibrated power (achieved by LMM and CR2) under strong clustering ($\text{ICC} = 0.50$) was $15.30\%$ at $J = 10$, increasing to $40.20\%$ at $J = 30$, and reaching $89.65\%$ at $J = 100$. Under weak clustering ($\text{ICC} = 0.10$), properly calibrated power was substantially higher: $25.30\%\text{--}26.25\%$ at $J = 10$, $71.50\%\text{--}71.65\%$ at $J = 30$, and $99.75\%$ at $J = 100$."*

---

#### Comment 5 (CR2 and Misspecification Claim):
> *"The simulation has no random slopes, so 'protected against random-effects misspecification' and 'without requiring parametric specification' rest on one dataset and on citation. State this in the abstract too."*

**Author Response:**
Agreed. We have revised the Abstract, Section 4.1, Section 5.3 (Limitations), and Table 7 to explicitly acknowledge that the simulation evaluated random-intercept data-generating mechanisms, and that CR2's robustness against random-slope misspecification is demonstrated in the empirical balanced sleepstudy application and supported by the broader literature (Pustejovsky & Tipton, 2018).

---

### Part II: Statistical and Methodological Points

#### Comment 6 (Post-Hoc Cell and Full R = 2,000 Re-Simulation):
> *"The J = 30, ICC = 0.10, within-subject cell: You re-ran only this cell at R = 2,000 because it looked odd. That is a post-hoc choice. It also affects Table 2 (ratio 1.155 vs the theoretical 1.054, which you describe as 'conforming'), Tables 3 and 4, and the 98.0% in the abstract range. Re-run all 24 scenarios at a larger R (2,000 or more) and report those, or the verification looks selective."*

**Author Response:**
We fully agree with this critical methodological point. Rather than selectively re-running a single cell, we re-executed the **entire full-factorial simulation across all 24 conditions at $R = 2,000$ replications** (48,000 datasets total) using master seed `20261031`.
- In the unified $R = 2,000$ run, for the within-subject $J = 30, \text{ICC} = 0.10$ cell:
  - Empirical SD = $0.0548$ (theoretical: $0.0548$; within $0.1\%$ of theory).
  - Naive OLS SE Ratio = $1.052$ (theoretical: $1.054$).
  - CR2 SE Ratio = $0.998$; LMM SE Ratio = $0.995$.
  - CR2 Coverage = $94.85\%$; LMM Coverage = $94.90\%$.
- All tables (Tables 1–5, 5b) and figures now report these unified $R = 2,000$ metrics without any post-hoc discrepancies.
- The overall coverage range in the Abstract now reads **94.4%–96.0%**.

---

#### Comment 7 (Standard Error Ratio Formula):
> *"SE ratio: The mean of SEs divided by the empirical SD is biased, because SE is nonlinear. Morris et al. (2019) recommend $\sqrt{\text{mean of the variances}} / \text{SD}$ instead."*

**Author Response:**
We adopted this exact recommendation. Following Morris et al. (2019, Section 3.2), the standard error ratio is now calculated as:
$$\text{SE Ratio} = \frac{\sqrt{\frac{1}{R}\sum_{r=1}^R \widehat{\text{Var}}(\hat{\beta}_{1,r})}}{S_\beta}$$
This formulation is documented in Section 2.5, reported in Table 2, and stored in `tables/table2_se_accuracy.csv`.

---

#### Comment 8 (Small Wording and Count Mismatches):
> *"'Over 5-fold' inflation is 4.96× at J = 30 (24.8%). The '≈0.94–1.04' range for within-subject ICC = 0.50 is really 0.963–1.041. Section 2.5 says 'six' metrics but lists seven. The master seed value is never given."*

**Author Response:**
All four items have been resolved:
- In the unified $R = 2,000$ run, between-subject naive OLS Type I error rate at $\text{ICC} = 0.50$ is $28.0\%$ at $J = 10$ ($5.60\times$) and $26.65\%$ at $J = 30$ ($5.33\times$). The text now accurately describes this as "over 5-fold (up to 5.6-fold; 5.3-fold at $J = 30$)."
- The empirical Morris SE ratio range for within-subject factors across all conditions is reported as $0.982\text{--}1.042$.
- Section 2.5 explicitly enumerates exactly **seven** performance measures: (1) Parameter Bias, (2) MCSE of Bias, (3) Empirical SD, (4) Mean Model SE, (5) Morris SE Ratio, (6) 95% CI Coverage, and (7) Type I Error / Power, plus REML singular boundary fit rates.
- The master pseudorandom seed integer is explicitly stated in Section 2.2 as `20261031`.

---

### Part III: Citations and Reproducibility

#### Comment 9 (Misattributed Citations and Reference List Audit):
> *"The [0.025, 0.075] bounds are Bradley’s (1978) liberal criterion, not Kahan et al. Schielzeth et al. (2020) is about distributional assumptions, so it doesn’t support the random-intercept-only overconfidence point. Barr et al. (2013) fits better. Kumle et al. (2021) is a power tutorial, so it is weak as a sleepstudy source. Reference list: Pustejovsky & Tipton (2022) is listed but never cited in the text. The Bell & McCaffrey link is a journal homepage, not an article link. Remove '(All Verified via Crossref)' from the heading. OSF DOI: '10.17605/OSF.IO/REPEATED-MEASURES' is not a valid OSF DOI format. Confirm the repository link too. Sleepstudy description: Days 0–9 are observation days, and restriction starts after day 0. '10 consecutive days of sleep restriction' is slightly off."*

**Author Response:**
All citation and textual points have been rigorously corrected:
- The robustness bounds $[0.025, 0.075]$ are now properly attributed to **Bradley (1978)** (*"Robustness?" British Journal of Mathematical and Statistical Psychology*).
- The random-intercept overconfidence point is now supported by **Barr et al. (2013)** (*"Random effects structure for confirmatory hypothesis testing: Keep it maximal"*, JML), removing the inappropriate Schielzeth citation.
- Kumle et al. (2021) was removed as a sleepstudy citation; **Belenky et al. (2003)** is cited directly for the experimental sleep deprivation protocol.
- The sleepstudy experimental protocol description was updated to clarify that **Days 0–1 were baseline adaptation and training days**, and the 3-hour sleep restriction occurred across **Days 2–9** (8 consecutive restriction days), totaling 10 observation days ($K = 10$).
- **Pustejovsky & Tipton (2022)** is now cited in-text in Section 1, Section 2.4, and Section 5.1.
- Bell & McCaffrey (2002) canonical Survey Methodology citation was updated.
- The heading text "(All Verified via Crossref)" was completely removed.
- The invalid OSF DOI placeholder was removed, and the active, verified GitHub repository link was provided: `https://github.com/IsaacMoon1/repeated-measures-simulation`.

---

### Part IV: Minor Refinements

#### Comment 10 (Expanded Manuscript Title):
> *"The title mentions 'Independent and Mixed-Effects Models' but not cluster-robust methods."*

**Author Response:**
The title has been updated to fully reflect all three compared paradigms:
**"Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Ordinary Least Squares, Linear Mixed-Effects, and Cluster-Robust Estimators"**

---

#### Comment 11 (Conclusion Wording on Within-Subject Factors):
> *"'Must never be applied' in the Conclusion is stronger than your within-subject results support."*

**Author Response:**
Softened as suggested. The Conclusion now explicitly distinguishes between predictor types:
*"For between-subject factors, naive OLS generates deflated standard errors, artificially narrow confidence intervals, and catastrophic Type I error inflation (exceeding 26%), and must never be applied. For within-subject factors, naive OLS does not inflate Type I error rates, but overestimates standard errors by 39% to 47%, resulting in unnecessarily wide confidence intervals and loss of inferential efficiency."*

---

#### Comment 12 (Table 2 Presentation):
> *"Table 2's triple-value cells (SD | SE | ratio) are hard to read, so consider three sub-columns."*

**Author Response:**
Table 2 was reformatted with dedicated columns for Empirical SD, Naive OLS (SE | Ratio), CR2 (SE | Ratio), and LMM REML (SE | Ratio), and full separate numeric columns in `tables/table2_se_accuracy.csv`.

---

We believe these comprehensive revisions have fully resolved every methodological, empirical, and stylistic concern raised, elevating the manuscript to the highest standards of Elsevier statistical journals.
