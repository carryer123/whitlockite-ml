#!/usr/bin/env python3
"""
Table S2 - Layer-2 weighted multi-objective ranking (PAiCER "Physics Score", 0-100).
====================================================================================
The 21 Pareto-viable candidates are ranked by a weighted sum of five normalized
objectives (the manuscript's biomaterial-facing final ranking, Fig. 1):

    Hardness 40 | CFSE 30 | Biocompatibility 20 | Lindemann CV 5 | dUtopia 5

Each objective is min-max normalized to its per-objective weight; higher-is-better
objectives map high values to high score, lower-is-better objectives are inverted:
    Hardness        (higher better)  -> 40 * (H - Hmin)/(Hmax - Hmin)
    CFSE            (higher better)  -> 30 * CFSE / CFSEmax
    Biocompatibility(lower  better)  -> 20 * (Bmax - B)/(Bmax - Bmin)   [B = LD50/IC50 toxicity index]
    Lindemann CV    (lower  better)  ->  5 * (Lmax - L)/(Lmax - Lmin)
    dUtopia         (pre-normalized) ->  5 * dUtopia/100
    Weighted sum    = sum of the five contributions

Inputs are the published per-element objective values (PAiCER SI, Table S2);
the LD50/IC50-derived Biocompatibility values are taken from that table.
Reproduces Ni = 97.2881 (Rank #1) and matches all 21 published Weighted sums.

Run from the repository root:  python src/physics_score_S2_21candidates.py
"""
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs"); os.makedirs(OUT, exist_ok=True)
EXP = os.path.join(ROOT, "expected")

WEIGHTS = {"Hardness_MPa": 40, "CFSE_Dq": 30, "Biocompatibility": 20,
           "Lindemann_CV": 5, "dUtopia_norm": 5}

df = pd.read_csv(os.path.join(DATA, "objectives_21candidates.csv"))
H, C, B, L, U = (df[c].values.astype(float) for c in
                 ["Hardness_MPa", "CFSE_Dq", "Biocompatibility", "Lindemann_CV", "dUtopia_norm"])

contrib = pd.DataFrame({"Metal": df["Metal"]})
contrib["Hardness_w40"]      = 40 * (H - H.min()) / (H.max() - H.min())
contrib["CFSE_w30"]          = 30 * C / C.max()
contrib["Biocompat_w20"]     = 20 * (B.max() - B) / (B.max() - B.min())
contrib["Lindemann_w5"]      =  5 * (L.max() - L) / (L.max() - L.min())
contrib["dUtopia_w5"]        =  5 * U / 100.0
contrib["Weighted_sum"]      = contrib[["Hardness_w40", "CFSE_w30", "Biocompat_w20",
                                        "Lindemann_w5", "dUtopia_w5"]].sum(axis=1)
contrib = contrib.sort_values("Weighted_sum", ascending=False).reset_index(drop=True)
contrib["Rank"] = np.arange(1, len(contrib) + 1)
contrib.to_csv(os.path.join(OUT, "physics_score_S2_21candidates.csv"), index=False)

print(contrib[["Rank", "Metal", "Hardness_w40", "CFSE_w30", "Biocompat_w20",
               "Lindemann_w5", "dUtopia_w5", "Weighted_sum"]].round(4).to_string(index=False))
ni = contrib[contrib.Metal == "Ni"].iloc[0]
print(f"\nNi: Rank #{int(ni.Rank)}  Weighted sum {ni.Weighted_sum:.4f}  (Table S2 target: #1, 97.2881)")

# --- verify against published Table S2 ---
exp = pd.read_csv(os.path.join(EXP, "TableS2_21.csv"))
m = contrib.merge(exp, on="Metal", suffixes=("", "_pub"))
maxdiff = (m["Weighted_sum"] - m["Weighted_sum_pub"]).abs().max()
print(f"Max |reproduced - published| Weighted sum over 21 candidates: {maxdiff:.4f}  "
      f"-> {'PASS' if maxdiff < 0.01 else 'FAIL'}")
print("Saved: outputs/physics_score_S2_21candidates.csv")
