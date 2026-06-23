# Scientific Validation of the AI-Driven Screen: Why Ni?

This note explains why the conclusion **"Ni is the optimal substituent for whitlockite reinforcement (Rank #1)"** follows from systematic **multi-objective optimization** followed by **science-based elimination**.

---

## The screening pipeline: 52 -> Top-12 -> 1

We performed an unbiased screen over **52 candidate elements**, without relying on intuition.

### Step 1 - AI prediction (52 candidate elements)

Using the 21-metal MD results as training data, an XGBoost model predicts the properties (MSD, Lindemann, PMF) of all 52 candidate elements across the periodic table.

### Step 2 - 5D Pareto optimization and Utopia-distance selection

Five orthogonal metrics are considered simultaneously: stability (MSD), structure (Lindemann), binding (PMF), size fit (radius mismatch), and geometry (OSSE).

The raw 5D Pareto frontier is large. In the XGBoost output `outputs/pareto_5d_xgboost.csv`, **38 metals are non-dominated**; the `Dist` and `Rank` columns then provide Utopia-distance ordering. The manuscript-facing **Top-12 is the Utopia-distance Tier-1 selection**, not the full raw Pareto set.

The authoritative ranking is `data/final_ranking_5d.csv`, which matches the XGBoost script output `outputs/pareto_5d_xgboost.csv`. Its Top-12 is:

`Ni, Cr, V, Co, Cu, W, Eu, Ho, Dy, Tb, Tc, Au`

Ni is **Rank #1**, and the leading 3d-metal Top-5 is **Ni, Cr, V, Co, Cu**. The XGBoost script `src/run_5d_pareto_xgboost.py` reproduces this ranking exactly.

The Top-12 period distribution is period 4 (3d) = Ni, Cr, V, Co, Cu (5); period 5 (4d) = Tc (1); period 6 (5d/4f) = W, Eu, Ho, Dy, Tb, Au (6).

### Step 3 - scientific elimination on the authoritative Top-12

The elimination logic is applied only to the authoritative Top-12:

| candidate(s) | disposition |
|---|---|
| Cr, V, Co, Cu | Viable 3d M2+ candidates, but rank below Ni by Utopia distance. |
| W | High-valence W(+6) chemistry creates charge imbalance in the divalent substitution site. |
| Eu, Tb, Ho, Dy | Rare-earth +3 substitution weakens the lattice through charge-compensating defects. |
| Tc | Radioactive; not viable for a biomaterial. |
| Au | Noble-metal redox favors reduction to Au(0) rather than stable M2+ substitution. |

### Step 4 - the winner

Ni is the only candidate that is Rank #1 by Utopia distance and remains chemically viable after the Top-12 filters.

---

## Supporting computational evidence

- **Geometric compatibility:** the conflict between the distorted M5 site and Ni's preference for a regular octahedron is the proposed reinforcement mechanism.
- **Thermodynamic stability (MD):** Ni has the lowest potential energy among screened divalent transition-metal candidates and a deep PMF well (-14.25 kJ/mol).
- **Hardness model:** full-fit XGBoost on the n = 4 hardness data gives CFSE-dominant importance (0.96) and predicted ranking Ni > Co > Mg > Cu. These claims come from `outputs/hardness_fullfit_importance_xgboost.csv`, not from the statistically limited leave-one-out point predictions in `outputs/loocv_hardness_xgboost.csv`.
- **Electronic origin (DFT):** Ni's near-degenerate high/low-spin states reflect electronic/structural flexibility; see `DFT_convergence_criteria.md`.

The full experimental validation (XRD / XPS / FTIR / nanoindentation) is reported in the manuscript.
