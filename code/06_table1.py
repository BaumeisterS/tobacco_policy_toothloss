# Build main Table 1 (baseline characteristics, stratified by treatment status).
import csv, math, os
from docx import Document
from docx.shared import Pt
OUT="output"; FONT="Arial"
def load(f):
    d={}
    for r in csv.DictReader(open(os.path.join(OUT,f), encoding="utf-8")): d[int(float(r["grp"]))]=r
    return d
tax=load("table1_ever_high_tax.csv"); rest=load("table1_ever_rest.csv")
def sd_bin(p1,p0):
    den=math.sqrt((p1*(1-p1)+p0*(1-p0))/2); return (p1-p0)/den if den>0 else float("nan")
def sd_age(m1,s1,m0,s0):
    den=math.sqrt((s1**2+s0**2)/2); return (m1-m0)/den if den>0 else float("nan")
VARS=[("n","N (person-records)","count"),("female","Female, %","pct"),("age","Age, mean (SD), y","age"),
      ("current_smoker","Current smoker, %","pct"),("quitting","Former smoker, %","pct"),
      ("diabetes","Diabetes, %","pct"),("dentist12","Dental visit <12 mo, %","pct"),
      ("all_removed","Edentulism, %","pct"),("t6_removed","Loss of \u22656 teeth, %","pct")]
doc=Document(); nrm=doc.styles["Normal"]; nrm.font.name=FONT; nrm.font.size=Pt(9)
p=doc.add_paragraph()
r1=p.add_run("Table 1"); r1.bold=True; r1.font.size=Pt(11); r1.font.name=FONT
r2=p.add_run("\tBaseline characteristics of the analytical sample, stratified by treatment status")
r2.bold=True; r2.font.size=Pt(11); r2.font.name=FONT
t=doc.add_table(rows=1, cols=7); t.style="Table Grid"
heads=["Characteristic","Never high-tax","Ever high-tax","Std. diff.","Never rest-ban","Ever rest-ban","Std. diff."]
for c,h in zip(t.rows[0].cells,heads):
    rr=c.paragraphs[0].add_run(h); rr.bold=True; rr.font.size=Pt(9); rr.font.name=FONT
def pct(x): return f"{100*float(x):.1f}"
def nfmt(x): return f"{int(round(float(x))):,}"
for key,label,kind in VARS:
    cells=t.add_row().cells; cells[0].text=label
    for gi,dset in enumerate([tax,rest]):
        g0,g1=dset[0],dset[1]; base=1+gi*3
        if kind=="count":
            cells[base].text=nfmt(g0["n"]); cells[base+1].text=nfmt(g1["n"]); cells[base+2].text=""
        elif kind=="pct":
            p0,p1=float(g0[key]),float(g1[key])
            cells[base].text=pct(p0); cells[base+1].text=pct(p1); cells[base+2].text=f"{sd_bin(p1,p0):+.2f}"
        else:
            m0,s0,m1,s1=float(g0["age"]),float(g0["age_sd"]),float(g1["age"]),float(g1["age_sd"])
            cells[base].text=f"{m0:.1f} ({s0:.1f})"; cells[base+1].text=f"{m1:.1f} ({s1:.1f})"; cells[base+2].text=f"{sd_age(m1,s1,m0,s0):+.2f}"
    for c in cells:
        for pp in c.paragraphs:
            for rr in pp.runs: rr.font.size=Pt(9); rr.font.name=FONT
note=doc.add_paragraph()
rn=note.add_run("Notes: Entries are % unless stated. Ever high-tax = states whose combined federal+state cigarette "
    "excise tax ever reached \u2265$3.00/pack during 1995-2012; ever rest-ban = states ever enacting a restaurant "
    "smoking restriction. Std. diff. = standardized difference; |value| > 0.10 indicates potentially meaningful imbalance.")
rn.font.size=Pt(9); rn.font.name=FONT
doc.save(os.path.join(OUT,"Table1.docx")); print("Table1.docx")
