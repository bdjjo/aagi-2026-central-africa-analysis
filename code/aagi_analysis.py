"""
AAGI Central Africa 2026 — reproducible audit and analysis.

Regenerates the processed CSV exports and the figure set from the two supplied
source files under ``data/raw/``:

  * AAGI_2026_CentralAfrica_Bainamndi.docx  (the regional report; comparative
    scores are transcribed from its page-2 summary table)
  * CopyofAAGI_Data_Collection_centralafricarepublic.xlsx  (the supplied,
    partially completed data-collection workbook)

The script uses only the two supplied files. Comparative figures use the
report's page-2 summary; workbook figures audit completeness only. See
``docs/methodology_and_limitations.md`` for the evidence rules and known
reproducibility caveats.

Run from anywhere:

    python3 code/aagi_analysis.py

Paths are resolved relative to the repository root, so the script is portable
across machines once the source files are placed in ``data/raw/``.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt
from openpyxl import load_workbook

# --- Portable paths -------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
FIG_PNG = ROOT / "figures" / "png"
FIG_SVG = ROOT / "figures" / "svg"
for _p in (PROC, FIG_PNG, FIG_SVG):
    _p.mkdir(parents=True, exist_ok=True)

WB_PATH = RAW / "CopyofAAGI_Data_Collection_centralafricarepublic.xlsx"
REPORT_PATH = RAW / "AAGI_2026_CentralAfrica_Bainamndi.docx"  # provenance only

PILLARS = [
    "P1 Strategy", "P2 Governance", "P3 Infrastructure", "P4 Human Capital",
    "P5 Innovation", "P6 Ethics", "P7 Regional", "P8 Implementation",
]

# --- 1. Comparative summary (transcribed from report p.2) -----------------
# The report presents composites as approximate (~). Values are one-decimal.
summary = pd.DataFrame({
    "Country": ["Cameroon", "Gabon", "DRC", "Republic of Congo", "Chad", "CAR"],
    "P1 Strategy":       [2.1, 1.7, 2.1, 1.8, 1.4, 0.1],
    "P2 Governance":     [1.3, 1.8, 1.5, 2.0, 1.7, 0.6],
    "P3 Infrastructure": [1.3, 1.6, 1.5, 0.9, 0.4, 0.2],
    "P4 Human Capital":  [1.3, 0.9, 1.3, 1.6, 0.4, 0.0],
    "P5 Innovation":     [1.1, 0.9, 1.5, 1.2, 0.3, 0.0],
    "P6 Ethics":         [1.5, 1.6, 1.4, 1.5, 0.6, 0.3],
    "P7 Regional":       [1.2, 1.8, 1.4, 2.1, 1.3, 0.2],
    "P8 Implementation": [0.8, 0.7, 1.0, 0.8, 0.1, 0.0],
    "Composite":         [1.3, 1.5, 1.5, 1.5, 0.8, 0.2],
})
summary.to_csv(PROC / "report_comparative_summary.csv", index=False)

long = summary.melt(id_vars=["Country", "Composite"], var_name="Pillar", value_name="Score")
long.to_csv(PROC / "report_pillar_scores_long.csv", index=False)

# --- 2. Workbook completeness and populated records -----------------------
wb = load_workbook(WB_PATH, data_only=False, read_only=True)
pillar_sheets: list[dict] = []
records: list[dict] = []
support: list[dict] = []

for ws in wb.worksheets:
    if ws.title.startswith("P") and ws.title[1:2].isdigit() and ws.title not in ("Public Perception",):
        for r in range(5, 15):
            row = [ws.cell(r, c).value for c in range(1, 9)]
            if row[0] and str(row[0]).strip() and str(row[0]).strip() not in ("ID",):
                records.append({
                    "sheet": ws.title, "row": r, "id": row[0], "indicator": row[1],
                    "score": row[4], "evidence": row[5], "source": row[6], "notes": row[7],
                })
        filled = [
            x for x in records
            if x["sheet"] == ws.title
            and any(x[k] not in (None, "") for k in ("score", "evidence", "source", "notes"))
        ]
        pillar_sheets.append({
            "sheet": ws.title, "indicator_rows": 10, "filled_indicator_rows": len(filled),
            "country": ws["D2"].value, "fellow": ws["B2"].value, "date": ws["F2"].value,
        })
    elif ws.title in ("Country Profile", "Economy & Investment", "Public Perception", "AI Incidents Tracker"):
        nonempty = []
        for row in ws.iter_rows(values_only=True):
            if any(v not in (None, "") for v in row):
                nonempty.append(list(row))
        uservals = []
        for row in nonempty:
            for v in row:
                if v not in (None, "", "[Enter]") and not (
                    isinstance(v, str) and (
                        v.startswith("CHAPTER") or v.startswith("AAGI")
                        or v in ("Country:", "Metric", "Value", "Year", "Source", "Notes")
                    )
                ):
                    uservals.append(v)
        support.append({
            "sheet": ws.title, "nonempty_rows": len(nonempty), "non_placeholder_values": len(uservals),
        })

pd.DataFrame(records).to_csv(PROC / "workbook_pillar_records.csv", index=False)
pd.DataFrame(pillar_sheets).to_csv(PROC / "workbook_pillar_completeness.csv", index=False)
pd.DataFrame(support).to_csv(PROC / "workbook_supporting_sheet_audit.csv", index=False)

# --- 3. Descriptive statistics, ranking, correlations, tiers --------------
stats = []
for p in PILLARS:
    s = summary[p]
    stats.append({
        "Pillar": p, "Mean": s.mean(), "Median": s.median(), "Min": s.min(),
        "Max": s.max(), "Range": s.max() - s.min(), "SD_population": s.std(ddof=0),
    })
pd.DataFrame(stats).to_csv(PROC / "pillar_descriptive_stats.csv", index=False)

rank = summary[["Country", "Composite"]].sort_values(["Composite", "Country"], ascending=[False, True])
rank.to_csv(PROC / "country_composite_ranking.csv", index=False)

# n=6 only: descriptive, NOT inferential.
corr = summary[PILLARS].corr(method="spearman")
corr.to_csv(PROC / "pillar_spearman_correlation.csv")

summary["Tier"] = pd.cut(
    summary["Composite"], bins=[-np.inf, 0.5, 1.0, 2.0, np.inf],
    labels=["Pre-Governance", "Nascent", "Developing", "Established+"],
)
summary.to_csv(PROC / "report_summary_with_tiers.csv", index=False)

# --- 4. Figures -----------------------------------------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans", "axes.titlesize": 14, "axes.labelsize": 10, "figure.dpi": 120,
})
SRC_REPORT = "Source: AAGI 2026 Central Africa report, p. 2."


def savefig(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG_PNG / f"{name}.png", dpi=150)
    plt.savefig(FIG_SVG / f"{name}.svg")
    plt.close()


# 1 composite ranking
x = summary.sort_values("Composite", ascending=True)
plt.figure(figsize=(12, 6.75))
plt.barh(x.Country, x.Composite,
         color=["#8c8c8c" if v <= 0.5 else "#E69F00" if v <= 1 else "#0072B2" for v in x.Composite])
plt.xlim(0, 4)
plt.xlabel("Composite score (0–4)")
plt.title("Central Africa AI governance scores cluster below the established threshold")
plt.axvline(3, color="black", ls="--", lw=1, label="Established threshold (3.0)")
plt.grid(axis="x", alpha=.25)
plt.legend()
plt.text(0.01, -0.13, f"{SRC_REPORT} Composite scores are shown as approximate in the report.",
         transform=plt.gca().transAxes, fontsize=8)
savefig("01_composite_ranking")

# 2 heatmap
plt.figure(figsize=(12, 6.75))
mat = summary.set_index("Country")[PILLARS]
im = plt.imshow(mat, cmap="YlGnBu", vmin=0, vmax=4, aspect="auto")
plt.colorbar(im, label="Score (0–4)")
plt.xticks(range(8), PILLARS, rotation=30, ha="right")
plt.yticks(range(6), mat.index)
plt.title("Governance maturity varies more by pillar than by a single regional average")
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        plt.text(j, i, f"{mat.iloc[i, j]:.1f}", ha="center", va="center", fontsize=9, color="black")
plt.text(0.01, -0.17, SRC_REPORT, transform=plt.gca().transAxes, fontsize=8)
savefig("02_pillar_heatmap")

# 3 mean pillar
means = summary[PILLARS].mean().sort_values()
plt.figure(figsize=(12, 6.75))
plt.barh(means.index, means.values, color="#009E73")
plt.xlim(0, 2.2)
plt.xlabel("Mean score across six countries (0–4)")
plt.title("Regional averages are highest in strategy and regional integration, lowest in implementation")
plt.grid(axis="x", alpha=.25)
plt.text(0.01, -0.13, f"{SRC_REPORT} n=6 countries; descriptive only.",
         transform=plt.gca().transAxes, fontsize=8)
savefig("03_mean_pillars")

# 4 spread range
ranges = (summary[PILLARS].max() - summary[PILLARS].min()).sort_values()
plt.figure(figsize=(12, 6.75))
plt.barh(ranges.index, ranges.values, color="#D55E00")
plt.xlim(0, 3)
plt.xlabel("Max–min score range (0–4)")
plt.title("Strategy and governance show the widest cross-country spread")
plt.grid(axis="x", alpha=.25)
plt.text(0.01, -0.13, f"{SRC_REPORT} Range is a descriptive spread, not an uncertainty interval.",
         transform=plt.gca().transAxes, fontsize=8)
savefig("04_pillar_spread")

# 5 top vs bottom composite
plt.figure(figsize=(12, 6.75))
top = summary.set_index("Country")[PILLARS].loc[["Gabon", "Republic of Congo"]].mean()
bottom = summary.set_index("Country")[PILLARS].loc[["Chad", "CAR"]].mean()
width = .35
idx = np.arange(8)
plt.bar(idx - width / 2, top.values, width, label="Gabon + Republic of Congo", color="#0072B2")
plt.bar(idx + width / 2, bottom.values, width, label="Chad + CAR", color="#E69F00")
plt.xticks(idx, [p.split(" ", 1)[1] for p in PILLARS], rotation=30, ha="right")
plt.ylim(0, 2.5)
plt.ylabel("Mean score (0–4)")
plt.title("The lower tier falls furthest behind on infrastructure, innovation, and implementation")
plt.legend()
plt.grid(axis="y", alpha=.25)
plt.text(0.01, -0.17, f"{SRC_REPORT} Group means are descriptive.",
         transform=plt.gca().transAxes, fontsize=8)
savefig("05_tier_pillar_comparison")

# 6 score distribution
vals = summary[PILLARS].to_numpy().ravel()
plt.figure(figsize=(12, 6.75))
bins = np.arange(-.05, 4.06, .2)
plt.hist(vals, bins=bins, color="#56B4E9", edgecolor="white")
plt.xlabel("Pillar score (0–4)")
plt.ylabel("Country–pillar cells")
plt.title("Most country–pillar scores lie between 0 and 2")
plt.xticks(np.arange(0, 4.1, .5))
plt.grid(axis="y", alpha=.25)
plt.text(0.01, -0.13, f"{SRC_REPORT} 48 country–pillar observations.",
         transform=plt.gca().transAxes, fontsize=8)
savefig("06_score_distribution")

# 7 workbook completion
comp = pd.DataFrame(pillar_sheets)
plt.figure(figsize=(12, 6.75))
plt.barh(comp["sheet"].str.replace("P[1-8] ", "", regex=True), comp["filled_indicator_rows"], color="#CC79A7")
plt.xlim(0, 10)
plt.xlabel("Indicator rows with at least one populated field")
plt.title("The workbook contains only eight populated indicator rows")
plt.xticks(range(0, 11, 2))
plt.grid(axis="x", alpha=.25)
plt.text(0.01, -0.13, "Source: AAGI data-collection workbook, P1–P8 sheets; audit of rows 5–14.",
         transform=plt.gca().transAxes, fontsize=8)
savefig("07_workbook_completion")

# 8 strategy vs implementation
plt.figure(figsize=(12, 6.75))
plt.scatter(summary["P1 Strategy"], summary["P8 Implementation"], s=110,
            c=summary["Composite"], cmap="viridis", vmin=0, vmax=2)
for _, r in summary.iterrows():
    plt.annotate(r["Country"], (r["P1 Strategy"], r["P8 Implementation"]),
                 xytext=(5, 5), textcoords="offset points", fontsize=9)
plt.xlim(0, 2.5)
plt.ylim(0, 1.2)
plt.xlabel("Strategy & vision score")
plt.ylabel("Implementation & impact score")
plt.title("Strategy scores do not translate directly into implementation scores")
plt.grid(alpha=.25)
plt.text(0.01, -0.13, f"{SRC_REPORT} n=6; descriptive association only.",
         transform=plt.gca().transAxes, fontsize=8)
savefig("08_strategy_vs_implementation")

# 9 six-country grouped pillar comparison
labels = ["Strategy", "Governance", "Infrastructure", "Human capital",
          "Innovation", "Ethics", "Regional integration", "Implementation"]
colors6 = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]
fig, ax = plt.subplots(figsize=(14, 8))
w = 0.13
xpos = list(range(len(PILLARS)))
for i, (_, r) in enumerate(summary.iterrows()):
    offs = [v + (i - 2.5) * w for v in xpos]
    ax.bar(offs, r[PILLARS].tolist(), width=w, label=r["Country"], color=colors6[i])
ax.set_xticks(xpos)
ax.set_xticklabels(labels, rotation=25, ha="right")
ax.set_ylim(0, 4)
ax.set_ylabel("Score (0–4)")
ax.set_title("AAGI 2026 Central Africa: pillar scores across six countries")
ax.axhline(3.0, color="black", linestyle="--", linewidth=1, label="Established threshold (3.0)")
ax.grid(axis="y", alpha=.25)
ax.legend(ncol=3, frameon=False, loc="upper left")
fig.text(0.01, 0.01, f"{SRC_REPORT} Scores are report summary values; composites are approximate.", fontsize=9)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(FIG_PNG / "09_six_country_pillar_comparison.png", dpi=150)
fig.savefig(FIG_SVG / "09_six_country_pillar_comparison.svg")
plt.close(fig)

# --- 5. JSON audit summary ------------------------------------------------
out = {
    "report_summary_rows": 6,
    "report_pillar_cells": 48,
    "workbook_sheets": len(wb.sheetnames),
    "pillar_sheets": pillar_sheets,
    "supporting_sheets": support,
    "workbook_populated_indicator_rows": int(sum(x["filled_indicator_rows"] for x in pillar_sheets)),
    "report_page": 2,
    "caveats": [
        "Report composites are approximate (~) in the report.",
        "Workbook is a country template with only Cameroon P1 rows S1.1–S1.4 and P2 rows G2.1–G2.4 populated.",
        "Comparisons and correlations use n=6 countries and are descriptive, not inferential.",
    ],
}
(PROC / "audit_summary.json").write_text(json.dumps(out, indent=2, default=str))

print("Wrote processed data to", PROC)
print("Wrote figures to", FIG_PNG, "and", FIG_SVG)
print("Populated pillar rows:", out["workbook_populated_indicator_rows"])
print(summary.to_string(index=False))
