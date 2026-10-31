#!/usr/bin/env python3
"""
Title: Publication Paper Document Rebuilder (DOCX Generator)
Author: Isaac T. Adeyemi
Institution: Ladoke Akintola University of Technology (LAUTECH)
Description: Generates the formal, publication-ready Microsoft Word (.docx) document
             incorporating unified R=2,000 Monte Carlo simulation results, decomposed Table 2,
             singular fit diagnostic subtable, high-resolution figures, and peer-reviewed citations.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import pandas as pd

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="D0D5DD", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_paper_docx(filename, figures_dir, tables_dir):
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x1F, 0x24, 0x21)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)

    # Header / Meta
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run("ORIGINAL RESEARCH ARTICLE | METHODOLOGICAL SIMULATION & EMPIRICAL BENCHMARK")
    r_meta.font.size = Pt(8.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Ordinary Least Squares, Linear Mixed-Effects, and Cluster-Robust Estimators")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0A, 0x25, 0x40) # Midnight Navy

    # Author
    p_author = doc.add_paragraph()
    p_author.paragraph_format.space_after = Pt(2)
    r_author = p_author.add_run("Isaac T. Adeyemi")
    r_author.font.bold = True
    r_author.font.size = Pt(12)

    p_aff = doc.add_paragraph()
    p_aff.paragraph_format.space_after = Pt(2)
    r_aff = p_aff.add_run("Department of Pure and Applied Mathematics / Statistics\nLadoke Akintola University of Technology (LAUTECH), P.M.B. 4000, Ogbomoso, Oyo State, Nigeria")
    r_aff.font.size = Pt(10)
    r_aff.font.italic = True
    r_aff.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    p_email = doc.add_paragraph()
    p_email.paragraph_format.space_after = Pt(14)
    r_email = p_email.add_run("Corresponding Author: isaacadeyemi245@gmail.com")
    r_email.font.size = Pt(9.5)
    r_email.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)

    # Abstract Box - Strictly 220 words (within 200-250 limit)
    tbl_abs = doc.add_table(rows=1, cols=1)
    tbl_abs.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_abs = tbl_abs.cell(0, 0)
    c_abs.width = Inches(6.5)
    set_cell_background(c_abs, "F7F9FC")
    set_cell_margins(c_abs, top=140, bottom=140, left=180, right=180)
    
    tcPr = c_abs._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="0A2540"/>'
        f'<w:top w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p_absh = c_abs.paragraphs[0]
    p_absh.paragraph_format.space_after = Pt(4)
    r_absh = p_absh.add_run("Abstract")
    r_absh.font.bold = True
    r_absh.font.size = Pt(11)
    r_absh.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)

    p_abst = c_abs.add_paragraph()
    p_abst.paragraph_format.space_after = Pt(8)
    p_abst.paragraph_format.line_spacing = 1.15
    r_abst = p_abst.add_run(
        "Repeated measures designs are widely utilized across biomedical and psychological research, yet the inferential consequences "
        "of ignoring clustering remain pervasive. Following the ADEMP protocol, this Monte Carlo simulation evaluates three analytical "
        "strategies: Naive Ordinary Least Squares (OLS), Linear Mixed-Effects Models (LMM) with Satterthwaite degrees of freedom, and "
        "Cluster-Robust Variance Estimation using the small-sample bias-reduced CR2 adjustment. We evaluated 24 factorial scenarios "
        "crossing cluster counts (J ∈ {10, 30, 100}), intraclass correlation coefficients (ICC ∈ {0.10, 0.50}), covariate structures "
        "(between- vs. within-subject), and effect sizes across 2,000 replications each (48,000 datasets), alongside an empirical "
        "re-analysis of the classic sleep deprivation benchmark. While all estimators yield unbiased point estimates, Naive OLS exhibits "
        "severe inferential failure: for between-subject covariates at ICC = 0.50, standard errors are deflated by over 40% (SE Ratio ≈ "
        "0.55–0.58), reducing 95% confidence interval coverage to 71.8%–74.2% and inflating Type I error rates to 26.0%–28.0% (nominal "
        "α = 0.05). Conversely, for within-subject covariates, Naive OLS overestimates standard errors (SE Ratio ≈ 1.39–1.47), yielding "
        "conservative coverage (99.2%–99.4%) and deflated Type I error rates (0.6%–1.2%). Both LMM and CR2 estimators preserve nominal "
        "coverage (94.4%–96.0%) and controlled Type I error rates (4.3%–5.8%) even at J = 10. In the empirical application, CR2 matched "
        "the standard error of a maximal random-slope model (SE = 1.546) without requiring parametric random-effects specification, "
        "illustrating design-based robustness."
    )
    r_abst.font.size = Pt(10)

    p_kw = c_abs.add_paragraph()
    p_kw.paragraph_format.space_after = Pt(0)
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.font.bold = True
    r_kwh.font.size = Pt(9.5)
    r_kwh.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    r_kwt = p_kw.add_run("Repeated measures; Linear mixed-effects models; Cluster-robust standard errors; CR2 estimator; ADEMP framework; Monte Carlo simulation; Moulton factor.")
    r_kwt.font.size = Pt(9.5)
    r_kwt.font.italic = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Heading helpers
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1F, 0x24, 0x21)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    def render_table(t_data, caption, col_widths=None):
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(8)
        p_cap.paragraph_format.space_after = Pt(2)
        p_cap.paragraph_format.keep_with_next = True
        r = p_cap.add_run(caption)
        r.font.bold = True
        r.font.size = Pt(10)

        tbl = doc.add_table(rows=len(t_data), cols=len(t_data[0]))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl)
        for r_idx, row in enumerate(t_data):
            for c_idx, val in enumerate(row):
                cell = tbl.cell(r_idx, c_idx)
                if col_widths and c_idx < len(col_widths):
                    cell.width = col_widths[c_idx]
                set_cell_margins(cell, top=45, bottom=45, left=55, right=55)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                if r_idx == 0:
                    set_cell_background(cell, "0A2540")
                    run = p.add_run(str(val))
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    run.font.size = Pt(9)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    set_cell_background(cell, "FFFFFF" if r_idx % 2 == 1 else "F8FAFC")
                    run = p.add_run(str(val))
                    run.font.size = Pt(9)
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 1. Introduction
    add_h1("1. Introduction")
    doc.add_paragraph(
        "Repeated measures and longitudinal data architectures—where multiple quantitative observations are sampled serially "
        "from the same experimental subjects, clinical patients, or sampling units—are ubiquitous across quantitative science "
        "(Bates et al., 2015; Diggle et al., 2002; Laird & Ware, 1982). The defining structural property of repeated measurements "
        "is the violation of statistical independence: observations nested within the same individual are inevitably more correlated "
        "than observations originating from different individuals due to unobserved subject-specific biological, environmental, or "
        "psychological traits (Kahan et al., 2016)."
    )
    doc.add_paragraph(
        "Despite extensive pedagogical warnings in contemporary statistics (Cameron & Miller, 2015; Huang, 2022), applied investigators "
        "frequently employ standard Ordinary Least Squares (OLS) regression that assumes independent and identically distributed errors. "
        "While Gauss-Markov principles establish that OLS point estimates remain unbiased in linear settings, its default covariance "
        "matrix is fundamentally compromised under clustering. In clustered data theory, this distortion is governed by the design "
        "effect or variance inflation factor (VIF; Moulton, 1990):"
    )
    p_eq1 = doc.add_paragraph()
    p_eq1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq1 = p_eq1.add_run("VIF_OLS = 1 + (K - 1) ρ_x ρ_y           (1)")
    r_eq1.font.name = 'Consolas'
    r_eq1.font.size = Pt(10)

    doc.add_paragraph(
        "where K represents the cluster size (number of observations per subject), ρ_y is the intraclass correlation coefficient (ICC) "
        "of the outcome, and ρ_x is the intraclass correlation of the covariate (Huang, 2022; Moulton, 1990)."
    )
    doc.add_paragraph(
        "When an experimental covariate varies exclusively between subjects (e.g., treatment arm assigned at the subject level, where "
        "ρ_x = 1), VIF_OLS > 1. Here, naive OLS treats repeated measures as independent observations, resulting in an artificially "
        "deflated standard error, spuriously narrow confidence intervals, and high false-positive Type I error rates (Kahan et al., 2016). "
        "Conversely, when a covariate varies within subjects (such as centered observation time or repeated task conditions, where "
        "ρ_x ≤ 0), VIF_OLS < 1. In this case, naive OLS improperly pools between-subject variance into residual error, overestimating "
        "standard errors, producing excessively conservative confidence intervals, and sacrificing inferential precision (Huang, 2022)."
    )
    doc.add_paragraph("To account for intra-cluster correlation, modern applied methodology utilizes two main frameworks:")
    doc.add_paragraph(
        "1. Model-Based Estimation (Linear Mixed-Effects Models - LMM): LMMs partition total variance into between-subject random effects "
        "(u_i) and within-subject residual variation (ε_ij) using Restricted Maximum Likelihood (REML) (Bates et al., 2015; Laird & Ware, 1982). "
        "While optimal under correct specification, LMM inference in small samples (J < 30) requires small-sample degrees-of-freedom approximations, "
        "such as Satterthwaite or Kenward-Roger adjustments, to control Type I error rates (Kenward & Roger, 1997; Kuznetsova et al., 2017; "
        "Satterthwaite, 1946). Additionally, random-effects models can encounter singular covariance boundary solutions when cluster sizes "
        "are small or clustering is weak (Bates et al., 2015)."
    )
    doc.add_paragraph(
        "2. Design-Based Estimation (Cluster-Robust Variance Estimation - CRVE): CRVE retains standard OLS point estimates while substituting "
        "the naive covariance with an empirical sandwich estimator that is asymptotically robust to arbitrary correlation structures (Liang & "
        "Zeger, 1986; Zeileis et al., 2020). However, traditional sandwich estimators (CR0/CR1) suffer downward bias when the number of clusters "
        "J is small (J < 30), resulting in inflated Type I error rates (Cameron & Miller, 2015). Methodological work has emphasized the CR2 "
        "bias-reduced linearization estimator paired with Satterthwaite degrees of freedom, which provides unbiased variance estimation under "
        "the target model even with few clusters (Bell & McCaffrey, 2002; Pustejovsky, 2023; Pustejovsky & Tipton, 2018, 2022)."
    )
    doc.add_paragraph(
        "While these analytical properties have been examined individually (Huang, 2022; McNeish & Harring, 2017), applied researchers need "
        "direct, comparative benchmarks contrasting Naive OLS, REML-estimated LMMs with Satterthwaite corrections, and CR2 cluster-robust "
        "estimators across varying cluster sizes, ICC levels, and covariate structures. This study conducts an extensive Monte Carlo simulation "
        "adhering to the ADEMP simulation reporting guidelines (Morris et al., 2019). We evaluate parameter bias, standard error accuracy, "
        "95% confidence interval coverage, Type I error control, statistical power, and the incidence of singular fits across 24 factorial "
        "scenarios. Furthermore, we illustrate these findings through an empirical re-analysis of the benchmark psychomotor vigilance sleep "
        "deprivation dataset (Belenky et al., 2003)."
    )

    # 2. Methods
    add_h1("2. Materials and Methods (The ADEMP Protocol)")
    add_h2("2.1. Aims")
    doc.add_paragraph(
        "The primary objective of this simulation study is to quantify the empirical operating characteristics of Naive OLS, Linear Mixed-Effects "
        "Models (LMM), and Small-Sample Cluster-Robust Estimators (CR2) in repeated measures data. Specifically, we investigate:\n"
        "1. The magnitude of standard error deflation/inflation across between- and within-subject covariates.\n"
        "2. The empirical validity of Satterthwaite small-sample degrees of freedom under small (J = 10), moderate (J = 30), and large (J = 100) cluster numbers.\n"
        "3. The empirical incidence and inferential impact of singular boundary fits (σ_u² = 0) in REML estimation."
    )

    add_h2("2.2. Data-Generating Mechanism (DGM)")
    doc.add_paragraph("The data-generating process simulates a two-level hierarchical linear model:")
    p_eq2 = doc.add_paragraph()
    p_eq2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq2 = p_eq2.add_run("y_ik = β_0 + β_1 x_ik + u_i + ε_ik,   i = 1, ..., J;  k = 1, ..., K     (2)")
    r_eq2.font.name = 'Consolas'
    r_eq2.font.size = Pt(10)
    doc.add_paragraph(
        "where y_ik is the continuous outcome for subject i at occasion k, β_0 = 10.0 is the grand intercept, and β_1 is the target slope parameter. "
        "Total residual variance was held constant at σ² = σ_u² + σ_ε² = 1.0.\n\n"
        "The simulation manipulated four design factors in a full-factorial architecture (3 × 2 × 2 × 2 = 24 scenarios):\n"
        "1. Number of Clusters (J): J ∈ {10, 30, 100}, representing small, moderate, and large sample sizes.\n"
        "2. Cluster Size (K): Balanced at K = 5 occasions per subject.\n"
        "3. Intraclass Correlation Coefficient (ICC): ICC = σ_u² / (σ_u² + σ_ε²) ∈ {0.10, 0.50}, corresponding to weak (σ_u = √0.10, σ_ε = √0.90) and strong (σ_u = √0.50, σ_ε = √0.50) clustering.\n"
        "4. Covariate Structure (x_ik):\n"
        "   • Between-Subject: A cluster-level balanced binary indicator x_ik = z_i ∈ {0, 1}, where J/2 subjects receive z_i = 0 and J/2 receive z_i = 1 (ρ_x = 1.0).\n"
        "   • Within-Subject: An occasion-level linear time metric x_ik = t_k ∈ {-2, -1, 0, 1, 2}, centered within each subject (∑ t_k = 0, ∑ t_k² = 10, ρ_x = -0.25).\n"
        "5. Effect Size (β_1): Evaluated under the sharp null hypothesis H_0: β_1 = 0.0 (for Type I error calibration) and under the alternative hypothesis H_1: β_1 = 0.50 (for bias, standard error accuracy, confidence interval coverage, and statistical power).\n\n"
        "Each of the 24 factorial conditions was simulated across R = 2,000 independent Monte Carlo replications (totaling 48,000 generated datasets), using a fixed master pseudorandom seed integer of 20261031."
    )

    add_h2("2.3. Estimand")
    doc.add_paragraph("The estimand of primary scientific interest is the fixed-effect slope parameter β_1.")

    add_h2("2.4. Competing Analytical Methods")
    add_h3("Method 1: Naive Ordinary Least Squares (OLS)")
    doc.add_paragraph("Computed via standard OLS pooling across all observations:")
    p_eq3 = doc.add_paragraph()
    p_eq3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq3 = p_eq3.add_run("β_hat_OLS = (X^T X)^(-1) X^T y           (3)\nVar_hat_OLS(β_hat) = s² (X^T X)^(-1),   s² = (e^T e) / (N - 2)     (4)")
    r_eq3.font.name = 'Consolas'
    r_eq3.font.size = Pt(9.5)
    doc.add_paragraph("where N = J × K. Inferential tests and 95% confidence intervals used the Student's t-distribution with N - 2 degrees of freedom.")

    add_h3("Method 2: Linear Mixed-Effects Model (LMM - REML)")
    doc.add_paragraph("Specified with a subject-level random intercept:")
    p_eq4 = doc.add_paragraph()
    p_eq4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq4 = p_eq4.add_run("y_i = X_i β + 1_K u_i + ε_i           (5)")
    r_eq4.font.name = 'Consolas'
    r_eq4.font.size = Pt(9.5)
    doc.add_paragraph(
        "Estimated via Restricted Maximum Likelihood (REML) using lme4 (Bates et al., 2015). Statistical inference for β_1 was conducted "
        "using Satterthwaite degrees-of-freedom approximations via lmerTest (Kuznetsova et al., 2017). Singular fits (σ_u² < 10^(-4)) and optimizer "
        "convergence warnings were systematically audited (Bates et al., 2015; Lüdecke et al., 2021)."
    )

    add_h3("Method 3: Cluster-Robust OLS (CR2 Linearization)")
    doc.add_paragraph("Retains the OLS point estimate β_hat_OLS but replaces the naive covariance matrix with the bias-reduced linearization estimator CR2 (Bell & McCaffrey, 2002; Pustejovsky, 2023; Pustejovsky & Tipton, 2018, 2022):")
    p_eq5 = doc.add_paragraph()
    p_eq5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq5 = p_eq5.add_run("V_CR2 = (X^T X)^(-1) [ ∑_{i=1}^J X_i^T e_tilde_i e_tilde_i^T X_i ] (X^T X)^(-1)      (6)")
    r_eq5.font.name = 'Consolas'
    r_eq5.font.size = Pt(9.5)
    doc.add_paragraph(
        "where e_tilde_i = (I_K - H_ii)^(-1/2) e_i represents cluster-level residuals adjusted by the symmetric inverse square root of I_K - H_ii, "
        "with H_ii = X_i (X^T X)^(-1) X_i^T. Hypothesis tests and 95% confidence intervals were evaluated against the Satterthwaite-approximated "
        "Student's t-distribution via clubSandwich (Pustejovsky, 2023). Under the balanced designs utilized here, the Satterthwaite degrees of "
        "freedom equal J - 2 for the between-subject binary covariate and J - 1 for the orthogonal within-subject covariate."
    )

    add_h2("2.5. Performance Measures")
    doc.add_paragraph(
        "In accordance with modern simulation reporting standards (Morris et al., 2019), seven primary metrics were evaluated:\n"
        "1. Empirical Bias: Bias_hat = (1/R) ∑ (β_hat_1,r - β_1).\n"
        "2. Monte Carlo Standard Error of Bias: MCSE = S_β / √R, where S_β = √[ (1/(R-1)) ∑ (β_hat_1,r - β_bar_1)² ].\n"
        "3. Empirical Standard Deviation (Empirical SD): S_β, representing the true sampling dispersion across replications.\n"
        "4. Mean Model-Based Standard Error (Mean SE): SE_bar = (1/R) ∑ SE_hat(β_hat_1,r).\n"
        "5. Standard Error Accuracy Ratio (Morris SE Ratio): Computed following Morris et al. (2019) as SE Ratio = √[ (1/R) ∑ Var_hat(β_hat_1,r) ] / S_β, "
        "taking the root mean variance to eliminate Jensen's inequality bias. Values ≈ 1.00 indicate accurate standard error estimation; values < 1.00 "
        "indicate anti-conservative standard errors; values > 1.00 indicate conservative standard errors.\n"
        "6. 95% Confidence Interval Coverage: Empirical proportion capturing true β_1, with MCSE = √[ p_hat (1 - p_hat) / R ].\n"
        "7. Empirical Rejection Rate (α = 0.05): Rejection rate under H_0: β_1 = 0 (Type I error rate) and under H_1: β_1 = 0.50 (Statistical power), "
        "assessed against Bradley's (1978) liberal robustness boundaries [0.025, 0.075].\n\n"
        "Additionally, the incidence of singular boundary fits (σ_u_hat² < 10^(-4)) in REML was systematically audited across all scenarios, "
        "with coverage evaluated separately for singular and non-singular solutions."
    )

    # 3. Results
    add_h1("3. Monte Carlo Simulation Results")
    add_h2("3.1. Parameter Bias and Estimator Equivalence")
    doc.add_paragraph(
        "Table 1 displays the empirical bias of β_hat_1 across all 12 scenarios evaluated under β_1 = 0.50 at R = 2,000. In accordance with "
        "Gauss-Markov theory, all three estimators remained strictly unbiased across all conditions. Absolute bias never exceeded 0.009, and all "
        "confidence intervals for bias included zero (±1.96 × MCSE). Clustered data do not bias point estimation; the fundamental vulnerability "
        "lies in standard error calibration and inferential tests."
    )
    doc.add_paragraph(
        "The three estimators return identical point estimates because, in these balanced designs, the REML estimate of the fixed effect coincides "
        "with the OLS estimate; they differ solely in their standard errors and reference distributions. For the same reason, the CR2 and mixed-model "
        "results are identical or nearly identical in several cells (particularly for the between-subject covariate at ICC = 0.50), reflecting theoretical equivalence under balanced orthogonal structures."
    )

    # Load CSV data for tables
    df_t1 = pd.read_csv(os.path.join(tables_dir, "table1_bias.csv"))
    t1_rows = [["Covariate Type", "J", "ICC", "Naive OLS", "Cluster-Robust (CR2)", "Mixed Model (REML)"]]
    for _, r in df_t1.iterrows():
        t1_rows.append([
            r['Covariate_Type'], str(int(r['J'])), f"{r['ICC']:.2f}",
            f"{r['Naive_OLS_Bias']:.4f} ({r['Naive_OLS_MCSE']:.4f})",
            f"{r['CR2_Bias']:.4f} ({r['CR2_MCSE']:.4f})",
            f"{r['LMM_Bias']:.4f} ({r['LMM_MCSE']:.4f})"
        ])
    render_table(t1_rows, "Table 1: Empirical bias (MCSE) of the slope estimator β₁ across 2,000 replications (true β₁ = 0.500)")

    add_h2("3.2. Standard Error Accuracy and the Moulton Factor")
    doc.add_paragraph(
        "Table 2 decomposes the empirical sampling standard deviation (S_β), mean model-based standard error (SE_bar), and the root-mean-square "
        "variance ratio (SE Ratio = √[ (1/R) ∑ Var_hat ] / S_β, Morris et al., 2019) across all 12 conditions at R = 2,000. The results demonstrate "
        "the exact bidirectional distortion predicted by Moulton design-effect theory:\n"
        "• Between-Subject Covariates: When ICC = 0.50, naive OLS standard errors underestimate empirical dispersion by over 40%, producing SE ratios "
        "between 0.548 and 0.579. At ICC = 0.10, naive OLS ratios remain deflated (0.825 to 0.856). Both Cluster-Robust CR2 (Ratio = 0.989–1.018) "
        "and Mixed Models (Ratio = 0.989–1.018) accurately track empirical sampling dispersion across all sample sizes.\n"
        "• Within-Subject Covariates: When ICC = 0.50, naive OLS substantially overestimates standard errors, producing ratios between 1.394 and 1.469. "
        "Because OLS fails to subtract subject-level variance from within-subject contrasts, it misattributes between-subject heterogeneity to residual error. "
        "Both LMM and CR2 isolate intra-subject residual variation, maintaining calibrated ratios (0.982–1.042)."
    )
    doc.add_paragraph(
        "These empirical ratios agree closely with analytical design-effect derivations. For between-subject predictors, the theoretical ratio is "
        "1 / √(1 + (K - 1) ICC), which yields 0.845 at ICC = 0.10 and 0.577 at ICC = 0.50. For centered within-subject predictors, where ρ_x = -1 / (K - 1) = -0.25, "
        "the theoretical ratio is 1 / √(1 - ICC), which equals 1.054 at ICC = 0.10 and 1.414 at ICC = 0.50. The observed empirical ratios (0.825–0.856 and "
        "0.548–0.579 for between-subject; 1.037–1.063 and 1.394–1.469 for within-subject) align precisely with these analytical benchmarks across all J. "
        "Notably, at J = 30, ICC = 0.10 within-subject, the empirical SD (0.0548) is within 0.1% of the analytical theoretical SD (0.0548), eliminating Monte Carlo sampling anomalies."
    )

    df_t2 = pd.read_csv(os.path.join(tables_dir, "table2_se_accuracy.csv"))
    t2_rows = [["Covariate Type", "J", "ICC", "Empirical SD", "Naive OLS (SE | Ratio)", "CR2 (SE | Ratio)", "LMM REML (SE | Ratio)"]]
    for _, r in df_t2.iterrows():
        t2_rows.append([
            r['Covariate_Type'], str(int(r['J'])), f"{r['ICC']:.2f}",
            f"{r['Empirical_SD']:.4f}",
            f"{r['OLS_Mean_SE']:.4f} | {r['OLS_SE_Ratio']:.3f}",
            f"{r['CR2_Mean_SE']:.4f} | {r['CR2_SE_Ratio']:.3f}",
            f"{r['LMM_Mean_SE']:.4f} | {r['LMM_SE_Ratio']:.3f}"
        ])
    render_table(t2_rows, "Table 2: Decomposed standard error accuracy across 2,000 replications (Empirical SD, Mean Model-Based SE, and Morris SE Ratio)")

    add_h2("3.3. 95% Confidence Interval Coverage and Monte Carlo Resolution")
    doc.add_paragraph(
        "Table 3 presents empirical coverage probabilities for nominal 95% confidence intervals across all 12 simulation cells under β_1 = 0.50 (R = 2,000). "
        "With R = 2,000, the Monte Carlo standard error near nominal coverage is MCSE = √(0.95 × 0.05 / 2000) ≈ 0.00487, defining a narrow 95% simulation "
        "margin of error of ±1.96 × MCSE ≈ ±0.0095 ([0.9405, 0.9595]).\n"
        "• Naive OLS Under-Coverage (Between-Subject): Due to standard error deflation, naive OLS 95% confidence intervals provide severe under-coverage "
        "for between-subject predictors, capturing the true parameter in only 71.8% to 74.2% of replications when ICC = 0.50, and 89.4% to 91.3% when ICC = 0.10.\n"
        "• Naive OLS Over-Coverage (Within-Subject): Conversely, for within-subject predictors at ICC = 0.50, standard error inflation causes naive OLS "
        "confidence intervals to be unnecessarily wide, capturing the true parameter in 99.2% to 99.4% of replications.\n"
        "• Robust Calibration (LMM & CR2): Both LMM with Satterthwaite degrees of freedom and CR2 with Satterthwaite reference distributions maintain "
        "exemplary nominal coverage across all 12 conditions. CR2 coverage ranges between 94.5% and 95.8% (mean: 95.2%), with every single cell falling "
        "within the 95% Monte Carlo simulation limits [0.9405, 0.9595]. LMM coverage ranges between 94.4% and 96.0% (mean: 95.2%)."
    )

    df_t3 = pd.read_csv(os.path.join(tables_dir, "table3_coverage.csv"))
    t3_rows = [["Covariate Type", "J", "ICC", "Naive OLS", "Cluster-Robust (CR2)", "Mixed Model (REML)"]]
    for _, r in df_t3.iterrows():
        t3_rows.append([
            r['Covariate_Type'], str(int(r['J'])), f"{r['ICC']:.2f}",
            f"{r['OLS_Coverage']:.3f} [{r['OLS_MCSE']:.3f}]",
            f"{r['CR2_Coverage']:.3f} [{r['CR2_MCSE']:.3f}]",
            f"{r['LMM_Coverage']:.3f} [{r['LMM_MCSE']:.3f}]"
        ])
    render_table(t3_rows, "Table 3: Empirical 95% confidence interval coverage probabilities [MCSE] across 2,000 replications (nominal coverage = 0.950)")

    # Embed Figure 1
    fig1_file = os.path.join(figures_dir, "figure1_coverage.png")
    if os.path.exists(fig1_file):
        p_fig1 = doc.add_paragraph()
        p_fig1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig1.paragraph_format.space_before = Pt(6)
        p_fig1.paragraph_format.space_after = Pt(2)
        doc.add_picture(fig1_file, width=Inches(6.2))
        
        p_cap1 = doc.add_paragraph()
        p_cap1.paragraph_format.space_before = Pt(2)
        p_cap1.paragraph_format.space_after = Pt(10)
        r_c1 = p_cap1.add_run("Figure 1: Empirical 95% Confidence Interval Coverage Probability across sample sizes (J), faceted by intraclass correlation (columns) and covariate structure (rows). Dashed horizontal reference lines represent nominal 95% coverage; error bars reflect ±1.96 Monte Carlo standard errors.")
        r_c1.font.size = Pt(9.5)
        r_c1.font.italic = True
        r_c1.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    add_h2("3.4. False-Positive Type I Error Rates")
    doc.add_paragraph(
        "Table 4 summarizes empirical rejection rates under the sharp null hypothesis (H_0: β_1 = 0) at nominal α = 0.05. Figure 2 illustrates these "
        "trajectories relative to Bradley's (1978) liberal robustness boundaries [0.025, 0.075]:\n"
        "• Between-Subject Predictors: For naive OLS at ICC = 0.50, Type I error rates explode to 28.0% at J = 10, 26.65% at J = 30, and 26.0% at J = 100. "
        "This constitutes an over 5-fold surge above nominal α = 0.05 (5.33-fold at J = 30 and 5.60-fold at J = 10). Even under weak clustering (ICC = 0.10), "
        "naive OLS error rates reach 10.0% to 10.15%, severely breaching Bradley's (1978) liberal bound of 0.075.\n"
        "• Within-Subject Predictors: For within-subject time predictors at ICC = 0.50, naive OLS produced overly conservative Type I error rates (0.65% to 1.20%), "
        "reflecting standard error overestimation and loss of statistical sensitivity.\n"
        "• Controlled Inference (LMM & CR2): Both Linear Mixed Models (REML) and CR2 preserved excellent Type I error control across all 12 null scenarios, "
        "with empirical error rates bounded strictly between 4.30% and 5.80%, fully inside Bradley's (1978) liberal robustness interval [0.025, 0.075] and tightly centered on nominal 5.0%."
    )

    df_t4 = pd.read_csv(os.path.join(tables_dir, "table4_type1_error.csv"))
    t4_rows = [["Covariate Type", "J", "ICC", "Naive OLS", "Cluster-Robust (CR2)", "Mixed Model (REML)"]]
    for _, r in df_t4.iterrows():
        t4_rows.append([
            r['Covariate_Type'], str(int(r['J'])), f"{r['ICC']:.2f}",
            f"{r['OLS_Type1_Error']:.3f} [{r['OLS_MCSE']:.3f}]",
            f"{r['CR2_Type1_Error']:.3f} [{r['CR2_MCSE']:.3f}]",
            f"{r['LMM_Type1_Error']:.3f} [{r['LMM_MCSE']:.3f}]"
        ])
    render_table(t4_rows, "Table 4: Empirical Type I error rate under the null [MCSE] across 2,000 replications (nominal α = 0.050, true β₁ = 0.000)")

    # Embed Figure 2
    fig2_file = os.path.join(figures_dir, "figure2_type1_error.png")
    if os.path.exists(fig2_file):
        p_fig2 = doc.add_paragraph()
        p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig2.paragraph_format.space_before = Pt(6)
        p_fig2.paragraph_format.space_after = Pt(2)
        doc.add_picture(fig2_file, width=Inches(6.2))
        
        p_cap2 = doc.add_paragraph()
        p_cap2.paragraph_format.space_before = Pt(2)
        p_cap2.paragraph_format.space_after = Pt(10)
        r_c2 = p_cap2.add_run("Figure 2: Empirical Type I Error Rate under the sharp null hypothesis (β₁ = 0) at nominal α = 0.05. Shaded bands represent Bradley's (1978) liberal robustness limits [0.025, 0.075]; dashed horizontal line indicates nominal α = 0.05.")
        r_c2.font.size = Pt(9.5)
        r_c2.font.italic = True
        r_c2.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    add_h2("3.5. Statistical Power and Singular Fit Audit")
    doc.add_paragraph(
        "Table 5 summarizes statistical power under the alternative hypothesis β_1 = 0.50. For within-subject time predictors, all three methods achieved "
        "saturated 100% empirical power across all sample sizes (99.6%–100.0% at J = 10, and 100.0% at J ≥ 30). Because each scenario provided N = 5J "
        "observations with ∑ t_k² = 10 (yielding a denominator sum of squares ∑ ∑ t_k² = 10J), an effect size of β_1 = 0.50 saturated the power function, "
        "masking the asymptotic efficiency penalty of naive OLS. Demonstrating empirical power loss for naive OLS on within-subject factors requires smaller "
        "effect sizes (e.g., β_1 ≤ 0.15), where the wider OLS confidence intervals directly diminish detection sensitivity.\n\n"
        "For between-subject covariates, naive OLS appeared to exhibit higher power (e.g., 49.55% at J = 10, ICC = 0.50), but this is an uninterpretable "
        "artifact of its 28.0% false-positive rate. Properly calibrated power (achieved by LMM and CR2) under strong clustering (ICC = 0.50) was 15.30% "
        "at J = 10, increasing to 40.20% at J = 30, and reaching 89.65% at J = 100. Under weak clustering (ICC = 0.10), properly calibrated power was "
        "substantially higher: 25.30%–26.25% at J = 10, 71.50%–71.65% at J = 30, and 99.75% at J = 100."
    )

    df_t5 = pd.read_csv(os.path.join(tables_dir, "table5_power.csv"))
    t5_rows = [["Covariate Type", "J", "ICC", "Naive OLS", "Cluster-Robust (CR2)", "Mixed Model (REML)"]]
    for _, r in df_t5.iterrows():
        t5_rows.append([
            r['Covariate_Type'], str(int(r['J'])), f"{r['ICC']:.2f}",
            f"{r['OLS_Power']:.3f} [{r['OLS_MCSE']:.3f}]",
            f"{r['CR2_Power']:.3f} [{r['CR2_MCSE']:.3f}]",
            f"{r['LMM_Power']:.3f} [{r['LMM_MCSE']:.3f}]"
        ])
    render_table(t5_rows, "Table 5: Empirical statistical power [MCSE] across 2,000 replications (nominal α = 0.050, true β₁ = 0.500)")

    doc.add_paragraph(
        "Singular Boundary Fits in REML: Table 5b audits boundary convergence solutions (estimated random intercept variance σ_u_hat² < 10^(-4)) across "
        "all 48,000 simulated datasets. Boundary fits occurred primarily under weak clustering (ICC = 0.10) combined with small cluster counts (J = 10), "
        "reaching 24.50% for between-subject and 23.35% for within-subject designs. As J increased to 30, singular fit rates dropped to 8.95% (between) "
        "and 7.70% (within); at J = 100, singular fits were rare (0.75% and 0.35%). Under strong clustering (ICC = 0.50), boundary fits were virtually "
        "absent, occurring in only 0.65% (between) and 0.20% (within) of replications at J = 10, and 0.00% across all scenarios with J ≥ 30.\n\n"
        "Conditioning coverage on singular status reveals a fundamental structural contrast:\n"
        "• For between-subject predictors, when REML encounters a singular boundary fit, the estimated random-intercept variance collapses to zero, "
        "and the model mistakenly relies on residual within-subject variance. Consequently, LMM coverage among singular fits drops to 91.6% at J = 10, ICC = 0.10 and "
        "87.7% at J = 30, ICC = 0.10 (compared to 97.4% and 95.3% for non-singular fits). At J = 10, ICC = 0.50, singular fits were exceptionally rare "
        "(13 out of 2,000 replications, or 0.65%); coverage among these 13 singular cases was 69.2% (9/13), which illustrates severe variance collapse but carries "
        "substantial Monte Carlo imprecision due to the small count (n = 13). Because singular solutions occurred in less than 1% of replications in this cell, "
        "overall coverage remained well-calibrated at 95.2%.\n"
        "• For within-subject predictors, because the within-subject contrast is mathematically orthogonal to the random intercept, singular fits have "
        "no adverse effect on fixed-effect coverage: LMM coverage remained 96.1% at J = 10 and 96.8% at J = 30 among singular fits."
    )

    df_sing = pd.read_csv(os.path.join(tables_dir, "table_singular_fits.csv"))
    tsing_rows = [["Covariate Type", "J", "ICC", "Singular Fits (n/R)", "Rate (%)", "Overall Cov", "Singular Cov", "Non-Sing Cov"]]
    for _, r in df_sing.iterrows():
        cov_sing_str = f"{float(r['LMM_Cov_Singular']):.3f}" if pd.notnull(r['LMM_Cov_Singular']) and str(r['LMM_Cov_Singular']) != 'NA' else "—"
        tsing_rows.append([
            r['Covariate_Type'], str(int(r['J'])), f"{float(r['ICC']):.2f}",
            f"{int(r['Singular_Count'])} / 2,000",
            f"{float(r['Singular_Rate_Pct']):.2f}%",
            f"{float(r['LMM_Cov_Overall']):.3f}",
            cov_sing_str,
            f"{float(r['LMM_Cov_NonSingular']):.3f}"
        ])
    render_table(tsing_rows, "Table 5b: REML singular boundary fit diagnostics and conditional 95% CI coverage across 2,000 replications")

    # 4. Empirical Benchmark
    add_h1("4. Empirical Benchmark: The Sleep Deprivation Case Study")
    doc.add_paragraph(
        "To examine how these theoretical and simulation dynamics function in real-world biomedical data, we re-analyzed the canonical sleep deprivation "
        "experiment conducted by Belenky et al. (2003) and benchmarked by Bates et al. (2015). The dataset tracks average reaction times (ms) on a "
        "psychomotor vigilance task across N = 180 measurements obtained from J = 18 subjects across 10 consecutive observation days (Days 0 to 9, where K = 10). "
        "In the standard lme4 benchmarking protocol (Bates et al., 2015; Belenky et al., 2003), Day 0 represents baseline performance under normal sleep, "
        "with sleep restriction (restricted to 3 hours time-in-bed per night) commencing that night and continuing through Day 9.\n\n"
        "We fitted four competing specifications modeling reaction time as a linear function of sleep restriction days:\n"
        "1. Naive OLS Pooling: Regressing reaction time on days without clustering adjustments (df = 178).\n"
        "2. Cluster-Robust CR2: OLS point estimation with small-sample bias-reduced standard errors clustered by subject (df = 17).\n"
        "3. Random-Intercept LMM: LMM with subject-specific random intercepts, assuming uniform deterioration across subjects (df = 161).\n"
        "4. Random-Slope & Intercept LMM: Maximal LMM allowing both baseline reaction times and degradation rates to vary across subjects (df = 17)."
    )

    t6_data = [
        ["Model Specification", "Estimate (β₁)", "Std. Error", "df", "p-value", "95% Confidence Interval"],
        ["1. Naive OLS (complete pooling)", "10.467", "1.238", "178", "< 0.001", "[8.024, 12.911]"],
        ["2. Cluster-Robust OLS (CR2)", "10.467", "1.546", "17", "< 0.001", "[7.206, 13.729]"],
        ["3. LMM (random intercept only)", "10.467", "0.804", "161", "< 0.001", "[8.879, 12.055]"],
        ["4. LMM (random slope & intercept)", "10.467", "1.546", "17", "< 0.001", "[7.206, 13.729]"]
    ]
    render_table(t6_data, "Table 6: Empirical comparison on the sleep deprivation benchmark dataset (N = 180, J = 18)")

    add_h2("4.1. Empirical Insights")
    doc.add_paragraph(
        "Table 6 delivers three critical methodological insights:\n\n"
        "1. The Danger of Random-Intercept-Only Models: When fitting a Random-Intercept LMM, the standard error for Days collapses to 0.804 "
        "(df = 161, 95% CI: [8.879, 12.055]). The model assumes that every individual deteriorates at the exact same rate (10.467 ms/day). By restricting "
        "individual slope variability to zero, the model mistakenly pools subject-by-treatment interactions into residual precision, yielding dangerously "
        "overconfident inferences (Barr et al., 2013).\n\n"
        "2. Subject Slope Heterogeneity: Allowing random slopes across individuals (Model 4) increases the estimated standard error from 0.804 to 1.546 "
        "(df = 17, 95% CI: [7.206, 13.729]), reflecting substantial subject-level variance in neurobehavioral vulnerability to sleep restriction (Belenky et al., 2003).\n\n"
        "3. Analytical Mechanism of the CR2 Estimator: Without requiring explicit specification or optimization of a random-slope covariance matrix, the "
        "Cluster-Robust CR2 estimator yielded an identical standard error of 1.546 (df = 17, 95% CI: [7.206, 13.729]). This exact agreement is expected in a "
        "balanced design with a single within-subject covariate, because both approaches effectively base the standard error on the between-subject dispersion "
        "of the individual OLS slope estimates. This demonstrates that CR2 reproduces the maximal random-slope standard error without requiring random-slope "
        "specification. However, as noted in Section 5.3, a single empirical dataset does not constitute universal proof of robustness to arbitrary covariance "
        "misspecification; evaluating general robustness requires Monte Carlo simulations with random slopes explicitly embedded in the data-generating mechanism (Pustejovsky & Tipton, 2018)."
    )

    # 5. Discussion
    add_h1("5. Discussion")
    add_h2("5.1. Methodological Implications")
    doc.add_paragraph(
        "This study demonstrates the inferential hazards of applying naive OLS regression to repeated measures data. The direction and magnitude of inferential "
        "distortion align precisely with modern design-effect formulations (Huang, 2022; Moulton, 1990):\n"
        "• For between-subject predictors (e.g., parallel randomized trials), naive OLS standard errors underestimate true sampling variance by over 40%, "
        "causing 95% confidence interval coverage to collapse to 71.8%–74.2% and false-positive rates to surge to 26.0%–28.0%.\n"
        "• For within-subject predictors (e.g., longitudinal trajectories), naive OLS standard errors are overly conservative (SE Ratio ≈ 1.39–1.47), producing "
        "excessively wide intervals (99.2%–99.4% coverage) and sacrificing estimation precision.\n\n"
        "Both Linear Mixed Models (REML) with Satterthwaite corrections and Cluster-Robust CR2 estimators fully resolve these inferential breakdowns, "
        "maintaining nominal coverage (94.4%–96.0%) and controlled Type I error rates (4.3%–5.8%) down to small cluster counts (J = 10) (Bradley, 1978; "
        "Pustejovsky & Tipton, 2018, 2022)."
    )

    add_h2("5.2. Practical Decision Framework")
    doc.add_paragraph("Based on our empirical and simulation findings, we recommend the following analytical decision pathway for repeated measures designs:")

    t7_data = [
        ["Cluster Count", "Analytical Goal", "Recommended Approach", "Requirements and Cautions"],
        ["J < 30 (Small)", "Subject trajectories / variance components", "Linear mixed model (REML)", "Satterthwaite degrees of freedom is mandatory (Kuznetsova et al., 2017); audit singular boundary fits (Bates et al., 2015)"],
        ["J < 30 (Small)", "Population-averaged effects / robustness", "Cluster-robust OLS (CR2)", "Satterthwaite t reference distribution is mandatory (Pustejovsky, 2023); protected against random-slope misspecification in balanced designs (Pustejovsky & Tipton, 2018)"],
        ["J ≥ 30 (Moderate to Large)", "Subject trajectories", "Linear mixed model (REML / ML)", "Asymptotically robust inference is valid (Verbeke & Molenberghs, 2000)"],
        ["J ≥ 30 (Moderate to Large)", "Population-averaged effects", "GEE / CR0 / CR1", "Standard sandwich errors are valid; recommendation drawn from established literature (Cameron & Miller, 2015; Zeileis et al., 2020)"]
    ]
    render_table(t7_data, "Table 7: Analytical decision pathway for repeated measures designs")

    doc.add_paragraph(
        "Note: Recommendations for GEE, CR0, and CR1 at J ≥ 30 stem from established methodological literature (Cameron & Miller, 2015; Zeileis et al., 2020), "
        "as the present simulation focused specifically on contrasting Naive OLS, CR2, and LMM."
    )

    add_h2("5.3. Limitations and Future Directions")
    doc.add_paragraph(
        "Several methodological boundaries of the present study warrant consideration:\n"
        "1. Design Regularity: The Monte Carlo simulation evaluated strictly balanced designs (K = 5 occasions per cluster) without missing data. "
        "In observational cohorts with variable cluster sizes (K_i) and informative attrition, CR2 degrees of freedom can decrease substantially, occasionally leading to reduced power.\n"
        "2. Random-Slope Misspecification: Our simulation data-generating mechanism specified a pure random-intercept architecture. Consequently, the empirical "
        "equivalence observed between CR2 and maximal LMM in Section 4 rests on the balanced structure of the sleepstudy dataset and literature demonstrations "
        "(Pustejovsky & Tipton, 2018), rather than a simulated random-slope DGM. Future simulation work should formally manipulate random-slope variance (σ_u1²) "
        "to quantify the exact point at which random-intercept LMMs fail under controlled conditions.\n"
        "3. Distributional Assumptions: All random effects and residuals were generated from Gaussian distributions. While LMM fixed-effect inference is moderately "
        "robust to non-normal random effects (Schielzeth et al., 2020), extreme heavy-tailed skewness may alter small-sample performance."
    )

    # 6. Conclusion
    add_h1("6. Conclusion")
    doc.add_paragraph(
        "Ignoring clustering in repeated measures data creates severe inferential distortions whose direction depends strictly on covariate architecture. "
        "For between-subject factors, naive OLS generates deflated standard errors, artificially narrow confidence intervals, and catastrophic Type I error "
        "inflation (exceeding 26%), and must never be applied. For within-subject factors, naive OLS does not inflate Type I error rates, but overestimates "
        "standard errors by 39% to 47%, resulting in unnecessarily wide confidence intervals and loss of inferential efficiency.\n\n"
        "When cluster counts are small (J < 30), applied researchers must adopt either Linear Mixed Models with Satterthwaite degrees of freedom or Cluster-Robust "
        "Variance Estimation using the CR2 bias-reduced linearization. For population-averaged questions, CR2 provides a transparent, assumption-lean framework "
        "that avoids the computational complexities and boundary convergence pitfalls of random-effects modeling."
    )

    # Declarations
    add_h1("Declarations")
    doc.add_paragraph(
        "• Funding: This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.\n"
        "• Conflicts of Interest / Competing Interests: The author declares no conflicts of interest.\n"
        "• Data and Code Availability: Complete reproducible R and Python code pipelines, simulation routines, and benchmark dataset analysis scripts are "
        "openly accessible on GitHub: https://github.com/IsaacMoon1/repeated-measures-simulation.\n"
        "• Author Contributions: I.T.A. conceived the study, developed the methodology, executed the Monte Carlo simulations, analyzed the empirical benchmark data, and authored the manuscript."
    )

    # References
    add_h1("References")
    refs = [
        "Barr, D. J., Levy, R., Scheepers, C., & Tily, H. J. (2013). Random effects structure for confirmatory hypothesis testing: Keep it maximal. Journal of Memory and Language, 68(3), 255–278. https://doi.org/10.1016/j.jml.2012.11.001",
        "Bates, D., Mächler, M., Bolker, B., & Walker, S. (2015). Fitting linear mixed-effects models using lme4. Journal of Statistical Software, 67(1), 1–48. https://doi.org/10.18637/jss.v067.i01",
        "Belenky, G., Wesensten, N. J., Thorne, D. R., Thomas, M. L., Sing, H. C., Redmond, D. P., Russo, M. B., & Balkin, T. J. (2003). Patterns of performance degradation and restoration during sleep restriction and subsequent recovery: A sleep dose-response study. Journal of Sleep Research, 12(1), 1–12. https://doi.org/10.1046/j.1365-2869.2003.00337.x",
        "Bell, R. M., & McCaffrey, D. F. (2002). Bias reduction in standard errors for linear regression with multi-stage samples. Survey Methodology, 28(2), 169–181. https://www150.statcan.gc.ca/n1/pub/12-001-x/2002002/article/9058-eng.pdf",
        "Bradley, J. V. (1978). Robustness? British Journal of Mathematical and Statistical Psychology, 31(2), 144–152. https://doi.org/10.1111/j.2044-8317.1978.tb00581.x",
        "Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. Journal of Human Resources, 50(2), 317–372. https://doi.org/10.3368/jhr.50.2.317",
        "Diggle, P. J., Heagerty, P., Liang, K.-Y., & Zeger, S. L. (2002). Analysis of Longitudinal Data (2nd ed.). Oxford University Press. https://doi.org/10.1093/oso/9780198524847.001.0001",
        "Huang, F. L. (2022). Using cluster-robust standard errors when analyzing group-randomized trials with few clusters. Behavior Research Methods, 54(1), 282–298. https://doi.org/10.3758/s13428-021-01627-0",
        "Kahan, B. C., Forbes, G., Ali, Y., Jairath, V., Bremner, S., Harhay, M. O., Hooper, R., Wright, N., Eldridge, S. M., & Leyrat, C. (2016). Increased risk of type I errors in cluster randomised trials with small or medium numbers of clusters: A review, reanalysis, and simulation study. Trials, 17(1), 438. https://doi.org/10.1186/s13063-016-1571-2",
        "Kenward, M. G., & Roger, J. H. (1997). Small sample inference for fixed effects from restricted maximum likelihood. Biometrics, 53(3), 983–997. https://doi.org/10.2307/2533558",
        "Kuznetsova, A., Brockhoff, P. B., & Christensen, R. H. B. (2017). lmerTest package: Tests in linear mixed effects models. Journal of Statistical Software, 82(13), 1–26. https://doi.org/10.18637/jss.v082.i13",
        "Laird, N. M., & Ware, J. H. (1982). Random-effects models for longitudinal data. Biometrics, 38(4), 963–974. https://doi.org/10.2307/2529876",
        "Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using generalized linear models. Biometrics, 42(1), 121–130. https://doi.org/10.2307/2531248",
        "Lüdecke, D., Ben-Shachar, M. S., Patil, I., Waggoner, P., & Makowski, D. (2021). performance: An R package for assessment, comparison and testing of statistical models. Journal of Open Source Software, 6(60), 3139. https://doi.org/10.21105/joss.03139",
        "McNeish, D., & Harring, J. R. (2017). Clustered data with small sample sizes: Comparing the performance of model-based and design-based approaches. Communications in Statistics - Simulation and Computation, 46(2), 859–869. https://doi.org/10.1080/03610918.2014.983648",
        "Morris, T. P., White, I. R., & Crowther, M. J. (2019). Using simulation studies to evaluate statistical methods. Statistics in Medicine, 38(11), 2074–2102. https://doi.org/10.1002/sim.8086",
        "Moulton, B. R. (1990). An illustration of a pitfall in estimating the effects of aggregate variables on micro units. The Review of Economics and Statistics, 72(2), 334–338. https://doi.org/10.2307/2109724",
        "Pustejovsky, J. E. (2023). clubSandwich: Cluster-robust (sandwich) variance estimators with small-sample corrections (R package version 0.5.10). Comprehensive R Archive Network. https://CRAN.R-project.org/package=clubSandwich",
        "Pustejovsky, J. E., & Tipton, E. (2018). Small-sample methods for cluster-robust variance estimation and hypothesis testing in fixed effects models. Journal of Business & Economic Statistics, 36(4), 672–683. https://doi.org/10.1080/07350015.2016.1247004",
        "Pustejovsky, J. E., & Tipton, E. (2022). Meta-analysis with robust variance estimation: Expanding the range of working models. Prevention Science, 23(3), 425–438. https://doi.org/10.1007/s11121-021-01246-3",
        "Satterthwaite, F. E. (1946). An approximate distribution of estimates of variance components. Biometrics Bulletin, 2(6), 110–114. https://doi.org/10.2307/3002019",
        "Schielzeth, H., Dingemanse, N. J., Nakagawa, S., Westneat, D. F., Allegue, H., Teplitsky, C., Réale, D., Dochtermann, N. A., Garamszegi, L. Z., & Araya-Ajoy, Y. G. (2020). Robustness of linear mixed-effects models to violations of distributional assumptions. Methods in Ecology and Evolution, 11(9), 1141–1152. https://doi.org/10.1111/2041-210X.13434",
        "Verbeke, G., & Molenberghs, G. (2000). Linear Mixed Models for Longitudinal Data. Springer. https://doi.org/10.1007/978-1-4419-0300-6",
        "Zeileis, A., Köll, S., & Graham, N. (2020). Various versatile variances: An object-oriented implementation of clustered covariances in R. Journal of Statistical Software, 95(1), 1–36. https://doi.org/10.18637/jss.v095.i01"
    ]
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.space_after = Pt(4)
        r_ref = p_ref.add_run(ref)
        r_ref.font.size = Pt(9.5)

    doc.save(filename)
    print(f"Successfully generated DOCX paper: {filename}")

if __name__ == '__main__':
    base_dir = r"C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review"
    figures_dir = os.path.join(base_dir, "figures")
    tables_dir = os.path.join(base_dir, "tables")
    out_docx = os.path.join(base_dir, "Adeyemi_Repeated_Measures_Simulation_Paper.docx")
    build_paper_docx(out_docx, figures_dir, tables_dir)
