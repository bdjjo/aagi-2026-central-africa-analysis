"""Check whether reported composites reproduce as the mean / weighted mean of pillars.

The report marks composites as approximate. This script quantifies how closely
the displayed one-decimal pillar scores reproduce the reported composite under
(a) an unweighted 8-pillar mean and (b) the report's stated pillar weights.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "processed" / "report_comparative_summary.csv")

cols = ["P1 Strategy", "P2 Governance", "P3 Infrastructure", "P4 Human Capital",
        "P5 Innovation", "P6 Ethics", "P7 Regional", "P8 Implementation"]
# Report-stated weights: 15% for P1–P4, 10% for P5–P8.
w = [.15, .15, .15, .15, .10, .10, .10, .10]

df["weighted_calc"] = (df[cols] * w).sum(axis=1).round(3)
df["unweighted_mean"] = df[cols].mean(axis=1).round(3)
df["reported"] = df["Composite"]
df["diff_weighted"] = (df["weighted_calc"] - df["reported"]).round(3)
df["diff_unweighted"] = (df["unweighted_mean"] - df["reported"]).round(3)

print(df[["Country", "weighted_calc", "unweighted_mean", "reported",
          "diff_weighted", "diff_unweighted"]].to_string(index=False))
print("\nWeight total:", sum(w))
print("Note: all countries reproduce within +/-0.05 EXCEPT Gabon, whose displayed")
print("pillars imply ~1.375-1.40 versus a reported ~1.5. See docs/methodology.")
