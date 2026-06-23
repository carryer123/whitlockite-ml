# Scientific Validation of the AI-Driven Screen: Why Ni?

This note explains why the conclusion **"Ni is the optimal substituent for whitlockite reinforcement (Rank #1)"** follows from a physics-based score, an XGBoost extension, and science-based elimination — without using experimental hardness in the scoring.

---

## The pipeline: 21 metals → full library → Ni

### Step 1 — Physics Score (21 MD-screened metals)

`src/physics_score_21metals.py` combines MD descriptors (MSD, Lindemann CV, CN CV, RDF peak height/width, calculated XRD peaks) with theoretical atomic properties (CFSE, ionic-radius match, Jahn-Teller penalty) into a single **Physics Score**, using physically-fixed weights. No experimental hardness enters the scoring.

- **Ni = 282.1932 — Rank #1.**
- Read back at the end for validation only: **Pearson r = 0.855** vs the four measured hardness values.

### Step 2 — XGBoost extension to the candidate library

`src/predict_45elements_xgboost.py` trains XGBoost on the 21 Physics Scores (theoretical atomic descriptors as features) and predicts every candidate element. **Ni remains Rank #1; CFSE dominates feature importance.** Authoritative output: `outputs/physics_ranking_45elements_xgboost.csv`.

The ranking uses XGBoost (the algorithm named in the manuscript); the 21 MD-data scores (including Ni = 282.19) are model-independent and reproduce exactly.

### Step 3 — chemistry / biocompatibility / synthesis elimination

| candidate(s) | disposition |
|---|---|
| Ra | radioactive — excluded |
| Pb, Tl, Bi, Hg, Cd | toxic heavy metals — excluded |
| Eu, Gd, Tb, Dy, Ho, Y, Yb, La | rare-earth +3; charge-compensating defects weaken the lattice |
| Pt, Pd, Au, Ag, Rh, Ir | noble-metal redox / cost; favor M(0) over stable M2+ |

### Step 4 — the winner

Ni is Rank #1 by Physics Score and remains a viable, biocompatible, divalent, synthesizable candidate after the Stage-3 filters. The manuscript synthesizes **Ni, Co, Cu, Mg** for experimental comparison.

---

## Supporting computational evidence

- **Geometric compatibility:** the conflict between the distorted M5 site and Ni's preference for a regular octahedron is the proposed reinforcement mechanism (Ni ionic radius 0.69 Å, closest match to the site).
- **Thermodynamic stability (MD):** Ni has low MSD and high structural uniformity among divalent transition-metal candidates.
- **Hardness model (n = 4):** full-fit XGBoost on the four measured metals gives **CFSE-dominant importance** and predicted ranking **Ni > Co > Mg > Cu** (matching experiment). These claims come from `outputs/hardness_fullfit_importance_xgboost.csv`, **not** from the statistically limited leave-one-out point predictions in `outputs/loocv_hardness_xgboost.csv`.
- **Electronic origin (DFT):** Ni's near-degenerate high/low-spin states reflect electronic/structural flexibility; see `DFT_convergence_criteria.md`.

The full experimental validation (XRD / XPS / FTIR / nanoindentation) is reported in the manuscript.
