# Reproducibility materials

**Tobacco Control Policies and Tooth Loss: A Difference-in-Differences Study**

This repository contains the code that reproduces every table and figure in the
manuscript and its supplement, together with the small intermediate result files
needed to regenerate the tables and figures directly.

---

## Software environment

| Component | Version | Packages used |
|-----------|---------|---------------|
| Stata     | 19.5    | `reghdfe`, `ftools`, `rangestat` |
| R         | 4.6.0   | `data.table`, `haven`, `fixest`, `did`, `didimputation`, `ggplot2` |
| Python    | 3.11+   | `python-docx`, `matplotlib` |

Standard errors are clustered by state throughout. All reported regression
estimates are covariate-adjusted (age, sex, race/ethnicity, education, diagnosed
diabetes, recent dental visit); household income is excluded because of a high
rate of item nonresponse.

---

## Directory layout

```
reproduce/
  README.md                this file
  code/                    analysis and table/figure scripts (run order numbered)
  data/                    place the analysis data set here (see data/README.txt)
  output/                  intermediate result files (.csv) and figures (.png);
                           generated tables/supplement (.docx) are written here
```

---

## Data

The individual-level analysis data set (~480 MB) and the raw source files are not
included because of their size; all are publicly available:

- **BRFSS, 1995–2012** — Behavioral Risk Factor Surveillance System, CDC
  (<https://www.cdc.gov/brfss/>).
- **Cigarette taxes and prices** — *The Tax Burden on Tobacco*
  (<https://chronicdata.cdc.gov/>).
- **Clean indoor-air laws** — CDC STATE System
  (<https://www.cdc.gov/statesystem/>).

Script `01_build_analysis_dataset.do` documents how the raw files are merged into
`data/final_smoking_analysis_dataset.dta`. See `data/README.txt` for the expected
folder layout. The small intermediate result files in `output/` are provided so
that the tables and figures can be regenerated without rebuilding the data set.

---

## How to reproduce

Run all commands with the `reproduce/` folder as the working directory.

### Path A — full pipeline (from raw data)

1. `01_build_analysis_dataset.do` (Stata) → `data/final_smoking_analysis_dataset.dta`
2. `02_descriptives_rollout_table1.do` (Stata) → descriptive/roll-out result files
3. `03_primary_estimates.R` (R) → primary fixed-effects estimates
4. `04_run_robust.R` (R) → robust DiD estimators and event-study figures
   (this driver runs `04a_robust_prep.R`, then `04b_robust_cell.R` once per
   treatment × outcome, then `04c_event_study_figures.R`)
5. `05_causal_graph.py` (Python) → causal-diagram figure
6. `06_table1.py`, `07_tables_2_3.py`, `08_supplement.py` (Python) → tables and supplement

### Path B — tables and figures only (from the provided result files)

The intermediate `.csv` and `.png` files in `output/` are already included, so the
final tables and figures can be built directly:

```
Rscript code/04c_event_study_figures.R     # Supplementary Figures 1–2
python  code/05_causal_graph.py            # Supplementary Figure 3
python  code/06_table1.py                  # Table 1
python  code/07_tables_2_3.py              # Tables 2–3
python  code/08_supplement.py              # Supplement (Suppl. Tables 1–6, Figures 1–3)
```

---

## Script → output map

| Script | Produces | Used in |
|--------|----------|---------|
| `01_build_analysis_dataset.do` | `data/final_smoking_analysis_dataset.dta` | all analyses |
| `02_descriptives_rollout_table1.do` | `table1_ever_*.csv`, `rollout_by_year.csv`, `descriptives_by_year.csv` | Table 1; Suppl. Tables 1–2 |
| `03_primary_estimates.R` | `res_final_main.csv`, `res_final_lag.csv`, `res_final_negctrl.csv`, `res_final_regyr.csv`, `res_final_loo.csv` | Tables 2–3; Suppl. Tables 3, 5, 6 |
| `04a/04b/04c` (via `04_run_robust.R`) | `res_robust_R.csv`, `es_R.csv`, `figR_es_behavior.png`, `figR_es_toothloss.png` | Suppl. Table 4; Suppl. Figures 1–2 |
| `05_causal_graph.py` | `figS_causalgraph.png` | Suppl. Figure 3 |
| `06_table1.py` | `Table1.docx` | Table 1 |
| `07_tables_2_3.py` | `Table2.docx`, `Table3.docx` | Tables 2–3 |
| `08_supplement.py` | `*_supplement_REVISED.docx` | Supplement |

---

## Estimators

The analysis uses two-way (state × year) fixed-effects linear-probability and
Poisson models as the primary estimators, with the extended two-way fixed-effects
(Mundlak) estimator, the Gardner two-stage estimator, the Callaway–Sant'Anna
group-time estimator, the Sun–Abraham interaction-weighted estimator, and the
Borusyak–Jaravel–Spiess imputation estimator as heterogeneity-robust comparisons.
Estimating equations and identification details are given in the manuscript's
supplement.
