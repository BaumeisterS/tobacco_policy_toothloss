# Reproducibility code

**Tobacco Control Policies and Tooth Loss: A Difference-in-Differences Study**

This repository contains the analysis code that reproduces the statistical results
and figures underlying the manuscript. No data are distributed: the analysis data
set is large and is derived from public sources (see `data/README.txt`). Running
the scripts on the assembled data set regenerates the estimates and figures.

---

## Software environment

| Component | Version | Packages used |
|-----------|---------|---------------|
| Stata     | 19.5    | `reghdfe`, `ftools`, `rangestat`, `did2s` |
| R         | 4.6.0   | `data.table`, `haven`, `fixest`, `did`, `didimputation`, `ggplot2`, `clubSandwich` |
| Python    | 3.11+   | `matplotlib` |
| LaTeX     | TeX Live / TinyTeX | `tikz` (causal DAG / Δ-SWIG figure) |

Standard errors are clustered by state throughout. All reported regression
estimates are covariate-adjusted (age, sex, race/ethnicity, education, diagnosed
diabetes, recent dental visit); household income is excluded because of a high rate
of item nonresponse.

---

## Directory layout

```
code/     analysis scripts, numbered in run order
data/     how to obtain and place the data (no data are included)
output/   destination for the estimates (.csv) and figures (.png) produced at run time
```

---

## Data

The individual-level analysis data set and the raw source files are not included
because of their size; all are publicly available:

- **BRFSS, 1995–2012** — Behavioral Risk Factor Surveillance System, CDC
  (<https://www.cdc.gov/brfss/>).
- **Cigarette taxes and prices** — *The Tax Burden on Tobacco*
  (<https://chronicdata.cdc.gov/>).
- **Clean indoor-air laws** — CDC STATE System
  (<https://www.cdc.gov/statesystem/>).

`code/01_build_analysis_dataset.do` documents how the raw files are merged into
`data/final_smoking_analysis_dataset.dta`. See `data/README.txt` for the expected
folder layout.

---

## How to run

Run all commands with the repository root as the working directory.

1. `01_build_analysis_dataset.do` (Stata) → `data/final_smoking_analysis_dataset.dta`
2. `02_descriptives_rollout_table1.do` (Stata) → descriptive and policy roll-out results
3. `03_primary_estimates.R` (R) → primary two-way fixed-effects estimates
4. `04_run_robust.R` (R) → heterogeneity-robust DiD estimators and event-study figures
   (this driver runs `04a_robust_prep.R`, then `04b_robust_cell.R` once per
   treatment × outcome, then `04c_event_study_figures.R`)
5. `05_causal_graph.py` (Python) → causal-diagram figure
6. `06_power_analysis.R` (R) → design-based minimum-detectable-effect table and Monte-Carlo power curves
7. `07_power_figure.R` (R) → statistical-power figure
8. `08_robust_ci_cr2.R` (R) → CR2 bias-reduced, Satterthwaite small-cluster confidence intervals
9. `09_causal_graph_swig.tex` (LaTeX/TikZ) → causal DAG and Δ-SWIG figure (compile with `pdflatex` or `tinytex::latexmk`)
10. `10_continuous_dose_robust.do` (Stata) → continuous-dose heterogeneity-robust estimators: extended two-way fixed-effects (Mundlak) and the Gardner two-stage estimator

All results (`.csv`) and figures (`.png`) are written to `output/`.

---

## Script → output map

| Script | Produces |
|--------|----------|
| `01_build_analysis_dataset.do` | `data/final_smoking_analysis_dataset.dta` |
| `02_descriptives_rollout_table1.do` | `table1_ever_*.csv`, `rollout_by_year.csv`, `descriptives_by_year.csv` |
| `03_primary_estimates.R` | `res_final_main.csv`, `res_final_lag.csv`, `res_final_negctrl.csv`, `res_final_regyr.csv`, `res_final_loo.csv` |
| `04a/04b/04c` (via `04_run_robust.R`) | `res_robust_R.csv`, `es_R.csv`, `figR_es_behavior.png`, `figR_es_toothloss.png` |
| `05_causal_graph.py` | `figS_causalgraph.png` |
| `06_power_analysis.R` / `07_power_figure.R` | `res_power_curve.csv`, `figR_power.png` |
| `08_robust_ci_cr2.R` | CR2 small-cluster confidence intervals |
| `09_causal_graph_swig.tex` | causal DAG / Δ-SWIG figure |
| `10_continuous_dose_robust.do` | `res_continuous_dose.csv` |

---

## Estimators

The analysis uses two-way (state × year) fixed-effects linear-probability and
Poisson models as the primary estimators, with the extended two-way fixed-effects
(Mundlak) estimator, the Gardner two-stage estimator, the Callaway–Sant'Anna
group-time estimator, the Sun–Abraham interaction-weighted estimator, and the
Borusyak–Jaravel–Spiess imputation estimator as heterogeneity-robust comparisons.
