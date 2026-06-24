# Scientific Validation of the AI-Driven Screen: Why Ni?

This note explains why **Ni is the top-ranked substituent for whitlockite reinforcement (Rank #1)** in this computational screen — from a physics-based score, an XGBoost extension, and science-based elimination, without using experimental hardness in the scoring. (The experimental confirmation of Ni's superior performance is reported in the manuscript.)

---

## The pipeline: 21 metals → full library → Ni

### Step 1 — Physics Score (21 MD-screened metals)

`src/physics_score_21metals.py` combines MD descriptors (MSD, Lindemann CV, CN CV, RDF peak height/width, calculated XRD peaks) with theoretical atomic properties (CFSE, ionic-radius match, Jahn-Teller penalty) into a single **Physics Score**, using physically-fixed weights. No experimental hardness enters the scoring.

- **Ni = 282.1932 — Rank #1.**

### Step 2 — XGBoost extension to the candidate library

`src/predict_candidates_xgboost.py` trains XGBoost on the 21 Physics Scores (theoretical atomic descriptors as features) and predicts every candidate element. **Ni remains Rank #1; CFSE dominates feature importance.** Authoritative output: `outputs/physics_ranking_xgboost.csv`.

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
- **Stability / structure (MD):** Ni's Physics Score is dominated by strong structural-uniformity (Lindemann/CN) and electronic (CFSE) contributions; see the per-descriptor weights in `src/physics_score_21metals.py`.
- **Experimental validation (manuscript):** the ranking predicts **Ni as Rank #1 by a wide margin**, independently confirmed by nanoindentation showing the Ni system (PAiCER-hc) is by far the hardest. Measured hardness is **not** an input to the ML ranking; it is used only as external validation in the manuscript.
- **Electronic origin (DFT):** Ni's near-degenerate high/low-spin states reflect electronic/structural flexibility; see `DFT_convergence_criteria.md`.

The full experimental validation (XRD / XPS / FTIR / nanoindentation) is reported in the manuscript.
