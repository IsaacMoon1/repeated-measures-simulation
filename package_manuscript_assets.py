#!/usr/bin/env python3
"""
Title: Manuscript Figures and Tables Packager
Author: Isaac T. Adeyemi et al.
Description: Copies all 300 DPI figures and publication CSV tables into a dedicated 
             Downloads package, creates a formatted Word document containing all tables, 
             and bundles everything into a single ready-to-upload ZIP archive.
"""

import os
import shutil
import zipfile
import csv
import pandas as pd
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=50, bottom=50, left=60, right=60):
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

def build_all_tables_docx(output_path, tables_dir):
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(10)
    font.color.rgb = RGBColor(0x1F, 0x24, 0x21)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(4)

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Manuscript Tables: Complete Statistical Results and Decision Framework")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Adeyemi I. T., Bamidele D. E., Adisa Z. O., Ademola O. R. (2026)\n"
                          "Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Ordinary Least Squares, "
                          "Linear Mixed-Effects, and Cluster-Robust Estimators")
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    tables_meta = [
        ("table1_bias.csv", "Table 1: Empirical bias (MCSE) of the slope estimator β₁ across 2,000 replications (true β₁ = 0.500)",
         ["Covariate Type", "J", "ICC", "Naive OLS", "Cluster-Robust (CR2)", "Mixed Model (REML)"]),
        ("table2_se_accuracy.csv", "Table 2: Decomposed standard error accuracy across 2,000 replications (Empirical SD, Mean Model-Based SE, and Morris SE Ratio)",
         ["Covariate Type", "J", "ICC", "Empirical SD", "Naive OLS (SE | Ratio)", "CR2 (SE | Ratio)", "LMM REML (SE | Ratio)"]),
        ("table3_coverage.csv", "Table 3: Empirical 95% confidence interval coverage probabilities [MCSE] across 2,000 replications (nominal coverage = 0.950)",
         ["Covariate Type", "J", "ICC", "Naive OLS", "Cluster-Robust (CR2)", "Mixed Model (REML)"]),
        ("table4_type1_error.csv", "Table 4: Empirical Type I error rate under the null [MCSE] across 2,000 replications (nominal α = 0.050, true β₁ = 0.000)",
         ["Covariate Type", "J", "ICC", "Naive OLS", "Cluster-Robust (CR2)", "Mixed Model (REML)"]),
        ("table5_power.csv", "Table 5: Empirical statistical power [MCSE] across 2,000 replications (nominal α = 0.050, true β₁ = 0.500)",
         ["Covariate Type", "J", "ICC", "Naive OLS", "Cluster-Robust (CR2)", "Mixed Model (REML)"]),
        ("table_singular_fits.csv", "Table 5b: REML singular boundary fit diagnostics and conditional 95% CI coverage across 2,000 replications",
         ["Covariate Type", "J", "ICC", "Singular Fits (n/R)", "Rate (%)", "Overall Cov", "Singular Cov", "Non-Sing Cov"]),
        ("table6_sleepstudy.csv", "Table 6: Empirical comparison on the sleep deprivation benchmark dataset (N = 180, J = 18)",
         None),
        ("table7_decision_pathway.csv", "Table 7: Analytical decision pathway for repeated measures designs",
         None)
    ]

    for csv_name, caption, custom_headers in tables_meta:
        csv_path = os.path.join(tables_dir, csv_name)
        if not os.path.exists(csv_path):
            continue

        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(14)
        p_cap.paragraph_format.space_after = Pt(4)
        p_cap.paragraph_format.keep_with_next = True
        r = p_cap.add_run(caption)
        r.font.bold = True
        r.font.size = Pt(10.5)

        df = pd.read_csv(csv_path)

        if custom_headers:
            headers = custom_headers
            rows_data = []
            if csv_name == "table1_bias.csv":
                for _, row in df.iterrows():
                    rows_data.append([
                        row['Covariate_Type'], str(int(row['J'])), f"{row['ICC']:.2f}",
                        f"{row['Naive_OLS_Bias']:.4f} ({row['Naive_OLS_MCSE']:.4f})",
                        f"{row['CR2_Bias']:.4f} ({row['CR2_MCSE']:.4f})",
                        f"{row['LMM_Bias']:.4f} ({row['LMM_MCSE']:.4f})"
                    ])
            elif csv_name == "table2_se_accuracy.csv":
                for _, row in df.iterrows():
                    rows_data.append([
                        row['Covariate_Type'], str(int(row['J'])), f"{row['ICC']:.2f}",
                        f"{row['Empirical_SD']:.4f}",
                        f"{row['OLS_Mean_SE']:.4f} | {row['OLS_SE_Ratio']:.3f}",
                        f"{row['CR2_Mean_SE']:.4f} | {row['CR2_SE_Ratio']:.3f}",
                        f"{row['LMM_Mean_SE']:.4f} | {row['LMM_SE_Ratio']:.3f}"
                    ])
            elif csv_name == "table3_coverage.csv":
                for _, row in df.iterrows():
                    rows_data.append([
                        row['Covariate_Type'], str(int(row['J'])), f"{row['ICC']:.2f}",
                        f"{row['OLS_Coverage']:.3f} [{row['OLS_MCSE']:.3f}]",
                        f"{row['CR2_Coverage']:.3f} [{row['CR2_MCSE']:.3f}]",
                        f"{row['LMM_Coverage']:.3f} [{row['LMM_MCSE']:.3f}]"
                    ])
            elif csv_name == "table4_type1_error.csv":
                for _, row in df.iterrows():
                    rows_data.append([
                        row['Covariate_Type'], str(int(row['J'])), f"{row['ICC']:.2f}",
                        f"{row['OLS_Type1_Error']:.3f} [{row['OLS_MCSE']:.3f}]",
                        f"{row['CR2_Type1_Error']:.3f} [{row['CR2_MCSE']:.3f}]",
                        f"{row['LMM_Type1_Error']:.3f} [{row['LMM_MCSE']:.3f}]"
                    ])
            elif csv_name == "table5_power.csv":
                for _, row in df.iterrows():
                    rows_data.append([
                        row['Covariate_Type'], str(int(row['J'])), f"{row['ICC']:.2f}",
                        f"{row['OLS_Power']:.3f} [{row['OLS_MCSE']:.3f}]",
                        f"{row['CR2_Power']:.3f} [{row['CR2_MCSE']:.3f}]",
                        f"{row['LMM_Power']:.3f} [{row['LMM_MCSE']:.3f}]"
                    ])
            elif csv_name == "table_singular_fits.csv":
                for _, row in df.iterrows():
                    cov_sing_str = f"{float(row['LMM_Cov_Singular']):.3f}" if pd.notnull(row['LMM_Cov_Singular']) and str(row['LMM_Cov_Singular']) != 'NA' else "—"
                    rows_data.append([
                        row['Covariate_Type'], str(int(row['J'])), f"{float(row['ICC']):.2f}",
                        f"{int(row['Singular_Count'])} / 2,000",
                        f"{float(row['Singular_Rate_Pct']):.2f}%",
                        f"{float(row['LMM_Cov_Overall']):.3f}",
                        cov_sing_str,
                        f"{float(row['LMM_Cov_NonSingular']):.3f}"
                    ])
        else:
            headers = [c.replace('_', ' ') for c in df.columns]
            rows_data = df.values.tolist()

        tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl)

        # Header row
        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            set_cell_margins(cell, top=45, bottom=45, left=55, right=55)
            set_cell_background(cell, "0A2540")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(h_text))
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            run.font.size = Pt(9)

        # Data rows
        for r_idx, row in enumerate(rows_data):
            for c_idx, val in enumerate(row):
                cell = tbl.cell(r_idx + 1, c_idx)
                set_cell_margins(cell, top=45, bottom=45, left=55, right=55)
                set_cell_background(cell, "FFFFFF" if r_idx % 2 == 0 else "F8FAFC")
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(str(val))
                run.font.size = Pt(9)

        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.save(output_path)
    print(f"Created consolidated Word document: {output_path}")

def package_assets():
    base_dir = r"C:\Users\HP\.gemini\antigravity\scratch\repeated_measures_review"
    figures_src = os.path.join(base_dir, "figures")
    tables_src = os.path.join(base_dir, "tables")
    
    downloads_pkg = r"C:\Users\HP\Downloads\Repeated_Measures_Manuscript_Assets"
    pkg_figures = os.path.join(downloads_pkg, "figures")
    pkg_tables = os.path.join(downloads_pkg, "tables")

    os.makedirs(pkg_figures, exist_ok=True)
    os.makedirs(pkg_tables, exist_ok=True)

    # 1. Copy Figures
    fig_map = {
        "figure1_coverage.png": "Figure1_95CI_Coverage.png",
        "figure2_type1_error.png": "Figure2_Type1_Error_Rate.png"
    }
    for orig, dest_name in fig_map.items():
        src_f = os.path.join(figures_src, orig)
        dest_f = os.path.join(pkg_figures, dest_name)
        if os.path.exists(src_f):
            shutil.copy2(src_f, dest_f)
            # also copy original name for compatibility
            shutil.copy2(src_f, os.path.join(pkg_figures, orig))
            print(f"Copied figure: {dest_name}")

    # 2. Copy Tables (both canonical names and publication descriptive names)
    tbl_map = {
        "table1_bias.csv": "Table1_Empirical_Bias.csv",
        "table2_se_accuracy.csv": "Table2_Standard_Error_Accuracy.csv",
        "table3_coverage.csv": "Table3_95CI_Coverage.csv",
        "table4_type1_error.csv": "Table4_Type1_Error_Rate.csv",
        "table5_power.csv": "Table5_Statistical_Power.csv",
        "table_singular_fits.csv": "Table5b_Singular_Boundary_Fits.csv",
        "table6_sleepstudy.csv": "Table6_Sleepstudy_Benchmark.csv",
        "table7_decision_pathway.csv": "Table7_Analytical_Decision_Pathway.csv"
    }
    for orig, dest_name in tbl_map.items():
        src_t = os.path.join(tables_src, orig)
        dest_t = os.path.join(pkg_tables, dest_name)
        if os.path.exists(src_t):
            shutil.copy2(src_t, dest_t)
            shutil.copy2(src_t, os.path.join(pkg_tables, orig))
            print(f"Copied table: {dest_name}")

    # 3. Build Word Document with All Tables
    docx_tables_out = os.path.join(pkg_tables, "All_Tables_Publication_Format.docx")
    build_all_tables_docx(docx_tables_out, tables_src)

    # 4. Copy Readme into package
    readme_path = os.path.join(downloads_pkg, "ASSETS_INDEX.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Manuscript Figures and Tables Package\n\n"
                "**Title:** Statistical Analysis of Repeated Measures Data: A Simulation Study Comparing Ordinary Least Squares, Linear Mixed-Effects, and Cluster-Robust Estimators\n\n"
                "**Authors:** Adeyemi I. T., Bamidele D. E., Adisa Z. O., Ademola O. R. (2026)\n\n"
                "**Institution:** Ladoke Akintola University of Technology (LAUTECH), Ogbomoso, Nigeria\n\n"
                "**GitHub Repository:** https://github.com/IsaacMoon1/repeated-measures-simulation\n\n"
                "## Contents\n"
                "### Figures (300 DPI High-Resolution PNG)\n"
                "- `figures/Figure1_95CI_Coverage.png`: 95% Confidence Interval Coverage probability across J, ICC, and Covariate structures.\n"
                "- `figures/Figure2_Type1_Error_Rate.png`: Empirical Type I error rate under the sharp null hypothesis with Bradley's (1978) bounds.\n\n"
                "### Tables (Publication CSV & Formatted Word Document)\n"
                "- `tables/All_Tables_Publication_Format.docx`: Formatted Microsoft Word document containing all 8 tables ready for journal submission.\n"
                "- `tables/Table1_Empirical_Bias.csv`: Parameter bias & MCSE across all 12 alternative scenarios.\n"
                "- `tables/Table2_Standard_Error_Accuracy.csv`: Decomposed Empirical SD, Mean SE, and Morris et al. (2019) SE ratios.\n"
                "- `tables/Table3_95CI_Coverage.csv`: 95% Confidence interval coverage probabilities & MCSE.\n"
                "- `tables/Table4_Type1_Error_Rate.csv`: Empirical Type I error rates under sharp null (beta1 = 0).\n"
                "- `tables/Table5_Statistical_Power.csv`: Empirical statistical power under beta1 = 0.50.\n"
                "- `tables/Table5b_Singular_Boundary_Fits.csv`: REML singular boundary fit rates & conditional coverage.\n"
                "- `tables/Table6_Sleepstudy_Benchmark.csv`: Empirical estimates, SEs, and CIs for sleep deprivation models.\n"
                "- `tables/Table7_Analytical_Decision_Pathway.csv`: Practical analytical decision framework.\n")

    # 5. Create ZIP Archive
    zip_out = r"C:\Users\HP\Downloads\Repeated_Measures_Tables_and_Figures.zip"
    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(downloads_pkg):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, downloads_pkg)
                zf.write(full_path, rel_path)
    print(f"Created ZIP archive: {zip_out}")

if __name__ == '__main__':
    package_assets()
