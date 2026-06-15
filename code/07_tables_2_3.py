# Tables 2-3 (rebuilt): covariate-adjusted estimates only (income removed from the
# adjustment set), contemporaneous AND cumulative (10-y average) rows, RD + RR
# columns, no significance stars. s1 style: bold tab-title ABOVE table, Table Grid, 9pt.
import csv, os
from docx import Document
from docx.shared import Pt

S2  = r"output"
OUT = S2
FONT="Arial"; MIN="−"

R={}
for r in csv.DictReader(open(os.path.join(OUT,"res_final_main.csv"), encoding="utf-8")):
    R[(r["dose"],r["outcome"],r["model"])]=r
def fmt(dose,outc,model):
    r=R.get((dose,outc,model))
    if r is None: return "—"
    b,lo,hi=float(r["b"]),float(r["lo"]),float(r["hi"])
    if model=="RR":
        import math
        return f"{math.exp(b):.3f} ({math.exp(lo):.3f}, {math.exp(hi):.3f})".replace("-",MIN)
    return f"{b:.4f} ({lo:.4f}, {hi:.4f})".replace("-",MIN)
def n_of(dose,outc):
    r=R.get((dose,outc,"RD")); return int(r["nobs"]) if r else None

ROWS=[("tax","Cigarette tax, current year (per $1.00)"),
      ("tax10","Cigarette tax, 10-year average (per $1.00)"),
      ("price","Cigarette price, current year (per $1.00)"),
      ("price10","Cigarette price, 10-year average (per $1.00)"),
      ("rest","Restaurant smoking ban (vs none)"),
      ("mall","Mall and grocery smoking ban (vs none)")]

def style(c,txt,bold=False):
    c.text=""
    rr=c.paragraphs[0].add_run(txt); rr.bold=bold; rr.font.size=Pt(9); rr.font.name=FONT

def build(fname,tno,caption,outcomes,note):
    doc=Document()
    nrm=doc.styles['Normal']; nrm.font.name=FONT; nrm.font.size=Pt(9)
    p=doc.add_paragraph()
    r1=p.add_run(f"Table {tno}"); r1.bold=True; r1.font.size=Pt(11); r1.font.name=FONT
    r2=p.add_run("\t"+caption); r2.bold=True; r2.font.size=Pt(11); r2.font.name=FONT
    t=doc.add_table(rows=2, cols=5); t.style="Table Grid"
    h=t.rows[0].cells
    style(h[0],"Policy exposure",bold=True)
    style(h[1],outcomes[0][0],bold=True); style(h[2],"",bold=True); h[1].merge(h[2])
    style(h[3],outcomes[1][0],bold=True); style(h[4],"",bold=True); h[3].merge(h[4])
    h2=t.rows[1].cells; style(h2[0],"",bold=True)
    style(h2[1],"RD (95% CI)",bold=True); style(h2[2],"RR (95% CI)",bold=True)
    style(h2[3],"RD (95% CI)",bold=True); style(h2[4],"RR (95% CI)",bold=True)
    for dose,lab in ROWS:
        c=t.add_row().cells; style(c[0],lab)
        style(c[1],fmt(dose,outcomes[0][1],"RD")); style(c[2],fmt(dose,outcomes[0][1],"RR"))
        style(c[3],fmt(dose,outcomes[1][1],"RD")); style(c[4],fmt(dose,outcomes[1][1],"RR"))
    np_=doc.add_paragraph(); rn=np_.add_run(note); rn.font.size=Pt(9); rn.font.name=FONT
    doc.save(os.path.join(S2,fname)); print("built",fname)

n2=n_of("tax","current_smoker"); n3=n_of("tax","all_removed")
build("Table2.docx","2",
  "Effects of state tobacco control policies on smoking behavior",
  [("Current smoking","current_smoker"),("Quitting (former smoking)","quitting")],
  f"Notes: Covariate-adjusted two-way (state and year) fixed-effects estimates; standard errors clustered by state "
  f"(N = {n2:,}). RD = risk difference (linear probability model); RR = risk ratio (Poisson). Models adjust for age, "
  "sex, race/ethnicity, education, diabetes, and dental visit within the past 12 months. The 10-year average is the "
  "mean dose over the 10 years up to and including the survey year (cumulative exposure). Estimates from "
  "heterogeneity-robust difference-in-differences estimators are reported in Supplementary Table 4.")
build("Table3.docx","3",
  "Effects of state tobacco control policies on tooth loss",
  [("Complete edentulism","all_removed"),("Loss of six or more teeth","t6_removed")],
  f"Notes: Covariate-adjusted two-way (state and year) fixed-effects estimates; standard errors clustered by state "
  f"(N = {n3:,}). RD = risk difference (linear probability model); RR = risk ratio (Poisson). Models adjust for age, "
  "sex, race/ethnicity, education, diabetes, and dental visit within the past 12 months. The 10-year average is the "
  "mean dose over the 10 years up to and including the survey year (cumulative exposure). Lag-stratified estimates "
  "are in Supplementary Table 3; heterogeneity-robust estimators in Supplementary Table 4; the identification "
  "diagnostic for the continuous two-stage estimator in Supplementary Table 5.")
