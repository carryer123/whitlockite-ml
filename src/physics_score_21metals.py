#!/usr/bin/env python3
"""
Stage 1 - Physics-based score for the 21 MD-screened metals.
============================================================
Computes the manuscript "Physics Score" for each of the 21 metal-substituted
whitlockite systems from MD- and theory-derived descriptors ONLY. No experimental
data enters the model; experimental nanoindentation is reported in the manuscript
as independent validation, not as an input here.

The score is a weighted, additive combination of:
  - MSD (50 ns, temporal stability, trend)        -> dynamic stability
  - Lindemann CV, coordination-number CV          -> structural uniformity
  - RDF peak height / width, time consistency     -> bond strength
  - calculated XRD peak count                      -> crystallinity
  - CFSE, ionic-radius match, Jahn-Teller penalty  -> electronic / geometric
All weights are fixed from physical reasoning (NOT fit to the experimental data).

Run from the repository root:  python src/physics_score_21metals.py
Reproduces Ni Physics Score = 282.1932 (manuscript Table S1, MD-data rows).
"""
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs"); os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------------
# 1. Load MD / calculated-XRD descriptors (21 metals)
# ----------------------------------------------------------------------------
df_time = pd.read_csv(os.path.join(DATA, "md_timepoint_scores_21metals.csv"))
df_spatial = pd.read_csv(os.path.join(DATA, "spatial_heterogeneity_21metals.csv"))
df_timedep = pd.read_csv(os.path.join(DATA, "time_dependent_scores_21metals.csv"))
df_xrd = pd.read_csv(os.path.join(DATA, "xrd_calc_peaks_21metals.csv"))

# ----------------------------------------------------------------------------
# 2. Theoretical atomic properties
# ----------------------------------------------------------------------------
cfse_data = {  # crystal-field stabilization energy (Dq units), ligand-field theory
    'V': 0.6, 'Cr': 1.2, 'Mn': 0.0, 'Fe': 0.4, 'Co': 0.8, 'Ni': 1.2, 'Cu': 0.6,
    'Zn': 0.0, 'Pd': 1.2, 'Cd': 0.0, 'Mg': 0.0, 'Ca': 0.0, 'Sr': 0.0, 'Ba': 0.0,
    'Ra': 0.0, 'Sn': 0.0, 'Pb': 0.0, 'Sm': 0.0, 'Eu': 0.0, 'Er': 0.0, 'Yb': 0.0}
ionic_radius = {  # Shannon radii (A), 6-coordination
    'V': 0.79, 'Cr': 0.80, 'Mn': 0.83, 'Fe': 0.78, 'Co': 0.75, 'Ni': 0.69, 'Cu': 0.73,
    'Zn': 0.74, 'Pd': 0.86, 'Cd': 0.95, 'Mg': 0.72, 'Ca': 1.00, 'Sr': 1.18, 'Ba': 1.35,
    'Ra': 1.48, 'Sn': 0.69, 'Pb': 1.19, 'Sm': 0.96, 'Eu': 0.95, 'Er': 0.89, 'Yb': 0.87}
d_electrons = {
    'V': 3, 'Cr': 4, 'Mn': 5, 'Fe': 6, 'Co': 7, 'Ni': 8, 'Cu': 9, 'Zn': 10, 'Pd': 8,
    'Cd': 10, 'Mg': 0, 'Ca': 0, 'Sr': 0, 'Ba': 0, 'Ra': 0, 'Sn': 0, 'Pb': 0, 'Sm': 0,
    'Eu': 0, 'Er': 0, 'Yb': 0}

# ----------------------------------------------------------------------------
# 3. Physics-based weights (theoretical, not optimized)
# ----------------------------------------------------------------------------
WEIGHTS = {
    'msd_final': 1.0, 'msd_temporal': 0.5, 'msd_trend': 0.3,
    'lindemann_cv': 0.4, 'cn_cv': 0.3,
    'rdf_peak_height': 0.3, 'rdf_peak_width': 0.2,
    'xrd_peaks': 0.4,
    'cfse': 0.8, 'ionic_radius': 0.5, 'jahn_teller': 0.6,
    'time_consistency': 0.4,
}

# ----------------------------------------------------------------------------
# 4. Score one metal
# ----------------------------------------------------------------------------
def physics_score(metal):
    t = df_time[df_time['Metal'] == metal]
    s = df_spatial[df_spatial['metal'] == metal]
    td = df_timedep[df_timedep['metal'] == metal]
    x = df_xrd[df_xrd['Metal'] == metal]
    if len(t) == 0:
        return np.nan
    score = 0.0
    # MSD
    score += max(0, 100 - t['MSD_50ns'].values[0]) * WEIGHTS['msd_final']
    score += t['MSD_Temporal_Stability'].values[0] * WEIGHTS['msd_temporal']
    score += t['MSD_Trend_Score'].values[0] * WEIGHTS['msd_trend']
    # structural uniformity
    if len(s):
        score += (100 - s['lindemann_cv'].values[0] if s['lindemann_cv'].values[0] < 100 else 0) * WEIGHTS['lindemann_cv']
        score += (100 - s['cn_cv'].values[0] if s['cn_cv'].values[0] < 100 else 0) * WEIGHTS['cn_cv']
    # RDF bond strength + time consistency
    if len(td):
        score += min(td['rdf_peak_height'].values[0] / 10, 50) * WEIGHTS['rdf_peak_height']
        w = td['rdf_peak_width'].values[0]
        score += (min(50 / w, 50) if w > 0 else 50) * WEIGHTS['rdf_peak_width']
        scores = [td[f'score_{k}ns'].values[0] for k in (10, 20, 30, 40, 50)]
        score += max(0, 50 - np.std(scores)) * WEIGHTS['time_consistency']
    # crystallinity (fewer calculated peaks = better)
    if len(x):
        score += max(0, (465 - x['Calc_Peaks'].values[0]) / 4.5) * WEIGHTS['xrd_peaks']
    # electronic / geometric
    score += (cfse_data.get(metal, 0) / 1.2) * 100 * WEIGHTS['cfse']
    score += max(0, 50 - abs(ionic_radius.get(metal, 1.0) - 0.70) * 100) * WEIGHTS['ionic_radius']
    if d_electrons.get(metal, 0) == 9:  # Jahn-Teller penalty (d9, e.g. Cu)
        score -= 100 * WEIGHTS['jahn_teller']
    return score

rows = [{'Metal': m, 'Physics_Score': physics_score(m)}
        for m in df_time['Metal'].unique()]
df = pd.DataFrame(rows).dropna(subset=['Physics_Score']).sort_values('Physics_Score', ascending=False)
df.to_csv(os.path.join(OUT, "physics_score_21metals.csv"), index=False)

# ----------------------------------------------------------------------------
# 5. Report
# ----------------------------------------------------------------------------
print(df.to_string(index=False))
ni = float(df[df.Metal == 'Ni'].Physics_Score.values[0])
ni_rank = list(df.Metal).index('Ni') + 1
print(f"\nNi Physics Score = {ni:.4f}  (expected 282.1932)   |   Ni rank = #{ni_rank}")
print(f"Saved: outputs/physics_score_21metals.csv")
