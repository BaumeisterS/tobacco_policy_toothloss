# Build the Supplement FROM SCRATCH -> s2\TobaccoPolicies_ToothLoss_supplement_REVISED.docx
#  - no redundancy with the main text; no mention of the review/revision
#  - aligned mathematical notation set as real Word equations (OMML)
#  - titles ABOVE tables and figures; Arial 11, 1.5 line spacing; page-number footer
import csv, os, math
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = r"."
OUT  = os.path.join(ROOT, r"output")
MEDIA= os.path.join(ROOT, r"media")
DEST = os.path.join(ROOT, r"output\TobaccoPolicies_ToothLoss_supplement_REVISED.docx")
FONT="Arial"; MIN="−"

def rd_csv(f):
    p=os.path.join(OUT,f); return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []
main=rd_csv("res_final_main.csv"); lag=rd_csv("res_final_lag.csv"); neg=rd_csv("res_final_negctrl.csv")
regy=rd_csv("res_final_regyr.csv"); loo=rd_csv("res_final_loo.csv")
roll=rd_csv("rollout_by_year.csv"); dby=rd_csv("descriptives_by_year.csv")
robR=rd_csv("res_robust_R.csv")   # CS / SA / BJS overall ATTs re-estimated in R

def ci(b,lo,hi,dec=4): return f"{b:.{dec}f} ({lo:.{dec}f}, {hi:.{dec}f})".replace("-",MIN)
def get(rows,**kk):
    for r in rows:
        if all(r.get(k)==v for k,v in kk.items()): return r
    return None
def fmt(rows,dec=4,**kk):
    r=get(rows,**kk)
    if r is None or not r.get("b"): return "—"
    lo=r.get("lo") or r.get("cil"); hi=r.get("hi") or r.get("ciu")
    return ci(float(r["b"]),float(lo),float(hi),dec)
def fmt_se(rows,dec=4,**kk):  # rows with b,se only (diag csv)
    r=get(rows,**kk)
    if r is None: return "—"
    b,s=float(r["b"]),float(r["se"]); return ci(b,b-1.96*s,b+1.96*s,dec)
def fmtR(estimator,trt,outcome,dec=4):  # res_robust_R.csv uses 'att' (not 'b')
    r=get(robR, estimator=estimator, trt=trt, outcome=outcome)
    if r is None or not r.get("att"): return "—"
    return ci(float(r["att"]),float(r["lo"]),float(r["hi"]),dec)

doc=Document()
nrm=doc.styles['Normal']; nrm.font.name=FONT; nrm.font.size=Pt(11)
nrm.paragraph_format.line_spacing=1.5

def P(t,size=11,bold=False,italic=False,align=None,after=6):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(after)
    if align: p.alignment=align
    r=p.add_run(t); r.font.size=Pt(size); r.bold=bold; r.italic=italic; r.font.name=FONT
    return p
def H(t,lvl=1):
    # Match the original submission: plain (Normal-style) headings in black Arial -
    # main sections bold, subsections italic; no Word "Heading" style (no blue).
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(10 if lvl==1 else 6)
    p.paragraph_format.space_after=Pt(4)
    r=p.add_run(t); r.font.name=FONT
    if lvl==1: r.bold=True; r.font.size=Pt(12.5)
    else:      r.italic=True; r.bold=True; r.font.size=Pt(11)
    return p
def caption(t):  # table/figure title ABOVE the object
    return P(t, 11, bold=True, after=4)
def note(t):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(10)
    r=p.add_run(t); r.font.size=Pt(9); r.italic=True; r.font.name=FONT
def table(headers, rows, fs=9):
    t=doc.add_table(rows=1, cols=len(headers)); t.style="Table Grid"
    for c,h in zip(t.rows[0].cells, headers):
        c.text=""
        rr=c.paragraphs[0].add_run(h); rr.bold=True; rr.font.size=Pt(fs); rr.font.name=FONT
        c.paragraphs[0].paragraph_format.line_spacing=1.0
    for row in rows:
        cells=t.add_row().cells
        for c,v in zip(cells,row):
            c.text=""
            rr=c.paragraphs[0].add_run(str(v)); rr.font.size=Pt(fs); rr.font.name=FONT
            c.paragraphs[0].paragraph_format.line_spacing=1.0
    return t

# ---------------- OMML equation support ----------------
MNS='xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
def _esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def _mr(s):  return f'<m:r><m:t xml:space="preserve">{_esc(s)}</m:t></m:r>'
def _msub(b,s): return f'<m:sSub><m:e>{_mr(b)}</m:e><m:sub>{_mr(s)}</m:sub></m:sSub>'
def eq(tokens, number=None, display=True):
    """tokens: list of (text, sub) tuples; sub=None for plain runs."""
    inner="".join(_msub(b,s) if s else _mr(b) for b,s in tokens)
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(6)
    if display: p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p._p.append(parse_xml(f'<m:oMath {MNS}>{inner}</m:oMath>'))
    if number:
        r=p.add_run("    ("+number+")"); r.font.size=Pt(10); r.font.name=FONT
    return p

# ============================ TITLE PAGE ============================
tp=P("Tobacco Control Policies and Tooth Loss: A Difference-in-Differences Study",14,bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER,after=2)
P("Sebastian-Edgar Baumeister, Benjamin W Chaffee, Birte Holtfreter, Stefan Listl",11,
  align=WD_ALIGN_PARAGRAPH.CENTER,after=2)
P("Supplementary Material",12,bold=True,align=WD_ALIGN_PARAGRAPH.CENTER,after=10)
P("Contents: Supplementary Methods (covariates and negative controls; notation and estimating equations; "
  "identification of imputation-based estimators; graphical assessment of parallel trends; interpretation of "
  "event-study plots); Supplementary Tables 1–6; Supplementary Figures 1–3.",10,italic=True)

# ============================ METHODS ============================
H("Supplementary Methods")

H("Covariates and negative-control outcomes",2)
P("All estimates reported in the manuscript are covariate-adjusted. The adjustment set comprises pre-treatment "
  "individual characteristics measured in every BRFSS cycle: age (years), sex, race/ethnicity (white, Black, "
  "Hispanic, other), educational attainment (six categories), diagnosed diabetes, and a dental visit within the "
  "past 12 months. Household income was not included because it was missing for a substantial proportion of "
  "respondents, which would have markedly reduced the analytic sample.")
P("Two negative-control outcomes probe residual time-varying confounding: seat-belt use (always or almost always "
  "versus less often) and having a working smoke detector tested in the past year. Both respond to general "
  "state-level health climate, public-safety investment, and survey composition, but neither has a plausible "
  "causal pathway from cigarette excise taxes. A tobacco-specific effect should therefore leave them unaffected; "
  "an association would signal confounding by broader state health trends (Supplementary Table 5).")

H("Notation and estimating equations",2)
P("Throughout, i indexes respondents, s states (51 including DC), and t survey years (1995–2012). Y denotes a "
  "binary outcome, D the state-year policy exposure (combined federal and state excise tax or retail price in 2012 "
  "dollars per pack, or a 0/1 ban indicator), and X the covariate vector defined above. State effects are α, year "
  "effects λ. Standard errors are clustered by state in all models.")
P("Two-way fixed-effects (TWFE) linear probability model — the coefficient β is a risk difference per $1.00 of "
  "dose (continuous policies) or for ban versus no ban:")
eq([("Y","ist"),(" = ",None),("β",None),("D","st"),(" + ",None),("X","ist"),("′γ + ",None),
    ("α","s"),(" + ",None),("λ","t"),(" + ",None),("ε","ist")],"1")
P("TWFE Poisson model — exp(β) is a risk ratio:")
eq([("E",None),("[",None),("Y","ist"),(" ∣ ",None),("D","st"),(", ",None),("X","ist"),(", s, t] = exp(",None),
    ("β",None),("D","st"),(" + ",None),("X","ist"),("′γ + ",None),("α","s"),(" + ",None),("λ","t"),(")",None)],"2")
P("Extended TWFE (two-way Mundlak) regression — pooled OLS with unit and period means of the dose; Wooldridge "
  "(2025) shows it is numerically equivalent to (1) and, under heterogeneous effects, recovers a convex average of "
  "within-state dose responses:")
eq([("Y","ist"),(" = ",None),("β",None),("D","st"),(" + ",None),("X","ist"),("′γ + ",None),
    ("π","1"),("D̄","s"),(" + ",None),("π","2"),("D̄","t"),(" + κ + ",None),("u","ist")],"3")
P("Two-stage difference-in-differences (Gardner 2022) — stage 1 estimates state and year effects on cells whose "
  "treatment is off; stage 2 regresses the residualized outcome on the within-state dose change:")
eq([("Y","ist"),(" = ",None),("α","s"),(" + ",None),("λ","t"),(" + ",None),("X","ist"),("′γ + ",None),
    ("e","ist"),("   on untreated cells,",None)],"4a")
eq([("Y","ist"),(" − ",None),("α̂","s"),(" − ",None),("λ̂","t"),(" = ",None),("β",None),
    ("ΔD","st"),(" + ",None),("v","ist"),(",   ",None),("ΔD","st"),(" = ",None),("D","st"),(" − ",None),
    ("D","s,1995")],"4b")
P("Group-time average treatment effects (Callaway and Sant'Anna 2021) for adoption cohort g at time t, with "
  "never-treated comparison C = 1, aggregated over (g, t):")
eq([("ATT",None),("(g, t) = E[",None),("Y","t"),(" − ",None),("Y","g−1"),(" ∣ ",None),("G","s"),
    (" = g] − E[",None),("Y","t"),(" − ",None),("Y","g−1"),(" ∣ ",None),("C","s"),(" = 1]",None)],"5")
P("Interaction-weighted estimator (Sun and Abraham 2021) — a saturated event-study regression interacts adoption-"
  "cohort indicators with relative-time (l = t − g) indicators, omitting l = −1; the cohort-specific coefficients "
  "δ are then averaged with weights equal to each cohort's share among the treated, giving the effect at relative "
  "time l:")
eq([("Y","ist"),(" = ",None),("α","s"),(" + ",None),("λ","t"),(" + ",None),("Σ","g"),("Σ","l≠−1"),
    ("δ","g,l"),(" · 1{",None),("G","s"),(" = g} · 1{t − g = l} + ",None),("ε","ist")],"6a")
eq([("β","l"),(" = ",None),("Σ","g"),(" ",None),("δ̂","g,l"),(" · Pr(",None),("G","s"),(" = g ∣ G",None),
    (" ∈ treated)",None)],"6b")
P("Imputation estimator (Borusyak, Jaravel and Spiess 2024) — α and λ are fit on untreated cells, counterfactuals "
  "are imputed for treated cells, and cell-level effects are averaged with weights w:")
eq([("τ̂","st"),(" = ",None),("Y","st"),(" − ",None),("α̂","s"),(" − ",None),("λ̂","t"),
    (",   ATT = ",None),("Σ","st"),(" ",None),("w","st"),("τ̂","st")],"7")
P("In plain terms, every difference-in-differences estimator attributes to the policy only the change in treated "
  "states' outcomes that exceeds the contemporaneous change in comparison states; the estimators differ in which "
  "comparison cells and baseline periods form that counterfactual and in how effects are aggregated across "
  "cohorts and time. Readers seeking an introduction to these methods are referred to Roth et al. (2023) and "
  "Baker et al. (2026).")

H("Identification of imputation-based estimators",2)
P("The imputation-based estimators (4) and (7) require untreated or not-yet-treated cells in every calendar period "
  "to identify the year effects λ. For the continuous tax this requirement fails when treatment is defined as any "
  "deviation of the combined tax from its 1995 baseline: because the federal component rises for all states, every "
  "state's combined tax moved off baseline by 1996, leaving untreated cells only in 1995 (50 of 51 states) and "
  "1996 (one state) and none thereafter. The year effects for 1997–2012 are then unidentified, and the estimator "
  "absorbs the national secular decline in tooth loss into the dose coefficient, producing a spurious protective "
  "association: the baseline-deviation specification implies a smoking effect of about −3.1 percentage points per "
  "$1.00 — roughly seven times the adequately identified estimate — together with protective tooth-loss effects "
  "that disappear once the comparison group is defined as a valid not-yet-treated cohort or the extended TWFE "
  "estimator (3) is used. The same sparse-comparison problem affects the indoor-ban estimates, since roughly 70% "
  "of person-time was exposed to bans. The de Chaisemartin–D'Haultfœuille continuous estimator is not applicable "
  "because the federally driven tax has no staggered timing of first dose change, and dose-response estimators in "
  "the spirit of Callaway et al., Hettinger et al., and Zhang presuppose a zero-dose comparison group, which does "
  "not exist when every state is taxed in every year. We therefore adopt the extended two-way fixed-effects "
  "estimator (3) as the primary specification and report the continuous two-stage estimates only as a sensitivity "
  "analysis. All results were cross-validated in Stata and R.")

H("Graphical assessment of parallel trends",2)
P("Parallel pre-trends are neither necessary nor sufficient for parallel trends (Roth 2022; Renson et al. 2026). "
  "Supplementary Figure 3 therefore gives an a-priori, structural assessment: a causal diagram and a transformed "
  "single-world intervention graph (Δ-SWIG) for the two-period design, with U denoting time-invariant unmeasured "
  "state factors (oral-health infrastructure, dental workforce, fluoridation history), A the policy, M smoking, "
  "X the measured covariates, and Y₀, Y₁ pre- and post-period tooth loss.")
P("Renson et al. (2026) show that, under linear faithfulness, parallel trends can be rejected if any of three "
  "graphical features is present: an effect of the pre-treatment outcome on treatment (Y₀ → A), confounding "
  "specific to one period, or an effect of the pre- on the post-treatment outcome (Y₀ → Y₁). None is plausible "
  "here: tobacco policy is set by fiscal and political processes, not by states' tooth-loss levels; the unmeasured "
  "drivers of tooth loss are slowly varying state characteristics that confound both periods alike; and because "
  "BRFSS samples different individuals each cycle, the only Y₀ → Y₁ channel is a state-level disease stock, which "
  "the state effects absorb. With these features absent, parallel trends holds if and only if confounding is "
  "additively homogeneous — exactly the additive separability that makes U cancel in the differenced node ΔY(0) of "
  "the Δ-SWIG, so that ΔY(0) ⫫ A ∣ X (conditional parallel trends; Knaus and Pfleiderer 2026). Because parallel "
  "trends is scale-dependent while the graph is not, risk ratios from the Poisson model (2) accompany every risk "
  "difference in Tables 2–3.")

H("Interpreting the event-study plots and assessing parallel trends",2)
P("Parallel trends for the robust estimators is assessed from their event-study coefficients (Supplementary "
  "Figures 1–2): pre-treatment coefficients (left of the dashed line) should lie near zero without trend, and "
  "post-treatment coefficients trace dynamic effects. Roth (2026) shows that recent estimators differ in how they "
  "construct these coefficients — in particular, the reference period and whether pre-treatment coefficients are "
  "built relative to a varying or a universal base period — so event studies from different estimators are not "
  "directly comparable unless this convention is fixed. Following Roth (2026), we estimate the Callaway–Sant'Anna "
  "event studies with a universal base period (the period before adoption), which yields pre-treatment "
  "coefficients that are interpretable as ordinary pre-trends; the Sun–Abraham interaction-weighted estimator uses "
  "the same common-baseline construction. Two further cautions apply. First, with millions of observations, formal "
  "pre-trend tests reject even negligible deviations (Roth 2022), so magnitudes matter more than significance; "
  "Rambachan and Roth (2023) relative-magnitude sensitivity analysis of the high-tax event study for loss of six "
  "or more teeth widened the 95% robust interval from [−0.002, 0.015] to [−0.090, 0.111] at M̄ = 2. Second, the "
  "high-dose financial cohorts are small and late, so their tooth-loss event studies are imprecise. Across "
  "estimators the pre-treatment coefficients are small and unsystematic, supporting the parallel-trends "
  "assumption, while the post-treatment coefficients show no consistent protective pattern for tooth loss.")

# ============================ FIGURES (placed before the tables) ============================
doc.add_page_break()
H("Supplementary Figures")

caption("Supplementary Figure 1. Callaway–Sant'Anna event studies for smoking outcomes, by policy")
doc.add_picture(os.path.join(OUT,"figR_es_behavior.png"), width=Inches(6.5))
note("Group-time effects aggregated by relative time, universal base period (Roth 2026); not-yet-treated states "
     "form the comparison; weighted state-year panel. Pre-treatment coefficients (green) are small and without "
     "trend, supporting parallel trends; post-treatment coefficients (orange) show the reduction in current "
     "smoking for the financial cohorts and the absence of a consistent ban effect.")

caption("Supplementary Figure 2. Callaway–Sant'Anna event studies for tooth loss, high-tax (≥$3.00) cohort")
doc.add_picture(os.path.join(OUT,"figR_es_toothloss.png"), width=Inches(6.5))
note("Constructed as in Supplementary Figure 1. Pre-treatment coefficients are flat; post-treatment coefficients "
     "are non-negative, i.e. no protective dynamic effect on tooth loss. The high-dose financial cohorts emerge "
     "only after 2008 and the oral-health module is biennial, so these dynamic estimates are imprecise; the "
     "high-price and ban cohorts were too sparse for stable group-time tooth-loss event studies (Supplementary "
     "Table 4).")

caption("Supplementary Figure 3. Causal diagram (A) and transformed single-world intervention graph (Δ-SWIG) (B) "
        "for the parallel-trends assessment")
doc.add_picture(os.path.join(OUT,"figS_causalgraph.png"), width=Inches(6.5))
note("Green edges: the hypothesised causal pathway (policy A → smoking M → post-period tooth loss Y₁). Red dashed "
     "edges: time-invariant confounding by U, absorbed by the difference-in-differences design. Crossed edges mark "
     "the three conditions under which parallel trends would be refutable (Renson et al. 2026): (1) an effect of "
     "pre-period tooth loss on policy adoption (Y₀→A); (2) period-specific confounding (no common cause shared by "
     "Y₀ and Y₁); and (3) an effect of pre- on post-period tooth loss (Y₀→Y₁). In panel (B), splitting A and "
     "differencing the untreated potential outcomes removes U because it enters Y₀ and Y₁ additively and cancels in "
     "ΔY(0); conditioning on the measured covariates X then blocks every remaining path between A and ΔY(0), giving "
     "ΔY(0) ⫫ A ∣ X — conditional parallel trends (Knaus and Pfleiderer 2026; Richardson and Robins 2013).")

# ============================ TABLES ============================
doc.add_page_break()
H("Supplementary Tables")

caption("Supplementary Table 1. Number of states (of 51, including DC) with each tobacco control policy in force, "
        "by survey year")
if roll:
    table(["Year","Restaurant ban","Mall/grocery ban","Tax ≥ $3","Price ≥ $6","States reporting"],
          [[r['year'],r['n_rest'],r['n_mall'],r['n_hightax'],r['n_highprice'],r['n_states']] for r in roll])
note("Restaurant and mall restrictions were already common in 1995 (≈29 of 51 states); the high-tax (≥$3.00/pack) "
     "cohort emerges only after 2008 (≤15 states). Monetary thresholds in constant 2012 dollars.")

caption("Supplementary Table 2. Sample characteristics by survey year (weighted means)")
if dby:
    rows=[[r['year'], f"{int(round(float(r['n']))):,}", f"{float(r['age']):.1f}", f"{100*float(r['female']):.1f}",
           f"{100*float(r['current_smoker']):.1f}", f"{100*float(r['quitting']):.1f}",
           f"{100*float(r['all_removed']):.1f}", f"{100*float(r['t6_removed']):.1f}",
           f"{float(r['tax_fed_state']):.2f}", f"{float(r['price_state']):.2f}"] for r in dby]
    table(["Year","N","Age, y","Female, %","Smoker, %","Quit, %","Edentulism, %","≥6 teeth lost, %","Tax, $","Price, $"], rows)
note("The sample ages (46 to 55 years on average) and smoking declines (22.6% to 16.5%) over the study period; "
     "year fixed effects absorb these national secular trends and the covariates absorb compositional shifts.")

caption("Supplementary Table 3. Tooth loss and the timing of exposure: covariate-adjusted two-way fixed-effects "
        "risk differences per $1.00, by exposure window")
WIN=[("Current year", {"tax":("main","tax"),"price":("main","price")}),
     ("1-year lag",   {"tax":("lag","tax_fed_state_lag1"),"price":("lag","price_lag1")}),
     ("5-year lag",   {"tax":("lag","tax_fed_state_lag5"),"price":("lag","price_lag5")}),
     ("10-year average",{"tax":("main","tax10"),"price":("main","price10")})]
rows=[]
for wlab,src in WIN:
    for pol,plab in [("tax","Cigarette tax"),("price","Cigarette price")]:
        kind,key=src[pol]
        if kind=="main":
            e1=fmt(main,dose=key,outcome="all_removed",model="RD"); e2=fmt(main,dose=key,outcome="t6_removed",model="RD")
        else:
            e1=fmt(lag,dose=key,outcome="all_removed",model="RD");  e2=fmt(lag,dose=key,outcome="t6_removed",model="RD")
        rows.append([plab,wlab,e1,e2])
table(["Policy","Exposure window","Edentulism, RD (95% CI)","Loss of ≥6 teeth, RD (95% CI)"],rows)
note("Models as in Table 3 (state and year fixed effects; covariate-adjusted; SE clustered by state). The "
     "protective association with loss of ≥6 teeth strengthens with longer exposure windows but remains "
     "statistically non-significant.")

caption("Supplementary Table 4. Heterogeneity-robust difference-in-differences estimators for the high-dose "
        "cohorts and indoor bans (re-estimated in R)")
OUTL={"current_smoker":"Current smoking","quitting":"Quitting","all_removed":"Edentulism","t6_removed":"Loss of ≥6 teeth"}
OUTS4=("current_smoker","quitting","all_removed","t6_removed")
EST=[("CS","Callaway–Sant'Anna"),("SA","Sun–Abraham"),("BJS","BJS imputation")]
TRTL=[("hightax","High tax (≥$3.00)"),("highprice","High price (≥$6.00)"),
      ("rest","Restaurant ban"),("mall","Mall/grocery ban")]
rows=[]
for tn,tlab in TRTL:
    for ec,elab in EST:
        rows.append([f"{tlab} — {elab}"]+[fmtR(ec, tn, o) for o in OUTS4])
table(["Cohort — estimator","Current smoking","Quitting","Edentulism","Loss of ≥6 teeth"],rows,fs=8)
note("Overall ATT (simple aggregation) with 95% CIs; SE clustered by state; weighted state-year panel; estimated "
     "in R (did, fixest::sunab, didimputation). Callaway–Sant'Anna uses a universal base period (Roth 2026) and "
     "not-yet-treated comparison states. These estimators are unadjusted (the covariate-adjusted primary estimates "
     "are in Tables 2–3) and confirm the absence of a protective tooth-loss effect. Dashes denote cells not "
     "estimable from the small, late, biennially observed high-dose tooth-loss cohorts (the Sun–Abraham variance is "
     "undefined and the group-time estimator does not converge); the imputation estimator, which is more stable, "
     "is null throughout. The de Chaisemartin–D'Haultfœuille continuous estimator and zero-dose dose-response "
     "estimators are not applicable to these data (Supplementary Methods).")

caption("Supplementary Table 5. Negative-control outcomes: covariate-adjusted two-way fixed-effects risk differences")
POLL=[("tax","Cigarette tax (per $1.00)"),("price","Cigarette price (per $1.00)"),
      ("rest","Restaurant ban"),("mall","Mall/grocery ban")]
rows=[[plab, fmt(neg,dose=pol,outcome="seatbelt"), fmt(neg,dose=pol,outcome="smkdetec")] for pol,plab in POLL]
table(["Policy","Seat-belt use, RD (95% CI)","Smoke-detector test, RD (95% CI)"],rows)
note("Cigarette taxes and prices are unrelated to both negative-control outcomes, supporting a tobacco-specific "
     "interpretation of the smoking effects. An association of the bans with the negative controls would indicate "
     "confounding of the ban estimates by broader state health trends. The smoke-detector item was administered in "
     "a subset of survey years; within that subsample the restaurant-ban indicator is collinear with the fixed "
     "effects and not estimable (—).")

caption("Supplementary Table 6. Region-by-year fixed effects: covariate-adjusted risk differences")
rows=[[plab]+[fmt(regy,dose=pol,outcome=o) for o in ("current_smoker","quitting","all_removed","t6_removed")]
      for pol,plab in POLL]
table(["Policy","Current smoking","Quitting","Edentulism","Loss of ≥6 teeth"],rows,fs=8.5)
def loorange(outc):
    sub=[float(r["b"]) for r in loo if r["model"]=="LOO" and r["outcome"]==outc]
    full=[float(r["b"]) for r in loo if r["model"]=="LOO_full" and r["outcome"]==outc]
    if not sub or not full: return "—"
    return f"full {full[0]:.4f}; range [{min(sub):.4f}, {max(sub):.4f}]".replace("-",MIN)
note("Region-by-year fixed effects replace the year effects with census-region × year effects, absorbing any "
     "state-level time-varying confounder shared by states within a region in a given year. Leave-one-state-out "
     f"re-estimation of the current-year tax effect (51 fits): edentulism {loorange('all_removed')}; loss of ≥6 "
     f"teeth {loorange('t6_removed')} — no result is driven by a single state.")

# ============================ footer ============================
def add_page_footer(section):
    f=section.footer; f.is_linked_to_previous=False
    p=f.paragraphs[0] if f.paragraphs else f.add_paragraph()
    p.text=""
    run=p.add_run("Supplement — Tobacco Control Policies and Tooth Loss      Page ")
    run.font.size=Pt(8); run.font.name=FONT
    fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE')
    p._p.append(fld)
for s in doc.sections:
    try: add_page_footer(s)
    except Exception as e: print("footer warn", e)

doc.save(DEST)
print("saved", DEST)
