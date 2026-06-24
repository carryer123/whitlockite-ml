# AI/ML Screening — Physics Score and XGBoost Extension

This note documents how the computational results in this repository form a predictive system for **rational materials design**, and how they rank **Ni** as the top divalent substituent for whitlockite (Rank #1 by the computational screen; the experimental confirmation of Ni's superior reinforcement is in the manuscript).

---

## 1. Methodology: a physics-based, data-driven screen

Molecular-dynamics simulations of 21 metal-substituted whitlockites provide the training data. A **physics-based scoring function** (Stage 1) converts MD- and theory-derived descriptors into a single **Physics Score** per metal, with weights fixed from physical reasoning — **not** fit to experimental data. An **XGBoost** regressor (Stage 2) then extends the Physics Score to the full candidate library.

### Descriptor groups feeding the Physics Score

1. **Dynamic stability** — MSD at 50 ns, MSD temporal stability, MSD trend
2. **Structural uniformity** — Lindemann CV, coordination-number CV
3. **Bond strength** — RDF peak height / width, score time-consistency
4. **Crystallinity** — calculated XRD peak count (fewer = more crystalline)
5. **Electronic / geometric** — CFSE, ionic-radius match to the site, Jahn-Teller penalty (d9)

---

## 2. Stage 1 — Physics Score (21 metals)

`src/physics_score_21metals.py` reproduces the authoritative Physics Score:

- **Ni = 282.1932 — Rank #1.**
- Validation against the four measured hardness values (Mg/Co/Ni/Cu, used **only** at this final step): **Pearson r = 0.855**.

These 21 values are the authoritative `outputs/physics_score_21metals.csv` and match the MD-data rows of manuscript Table S1.

## 3. Stage 2 — XGBoost extension

`src/predict_candidates_xgboost.py` trains XGBoost on the 21 Physics Scores using theoretical atomic descriptors, then predicts every candidate element (`outputs/physics_ranking_xgboost.csv`). **Ni stays Rank #1 (282.19); CFSE is the dominant feature** (importance ≈ 0.5).

**Model note.** The ranking uses XGBoost (Chen & Guestrin, 2016), the algorithm named in the manuscript. The 21 MD-data scores (including Ni = 282.19) are Stage-1 values and reproduce exactly.

## 4. Layer 2 — biocompatibility-weighted ranking (Table S2)

The Layer-1 Physics Score is a physical-property screen. Layer 2 (`src/physics_score_S2_21candidates.py`, reproducing SI Table S2) re-ranks the 21 Pareto-viable candidates by a weighted sum that adds **LD50/IC50 biocompatibility as an explicit 20% objective** (Hardness 40 / CFSE 30 / Biocompatibility 20 / Lindemann 5 / dUtopia 5), giving **Ni = 97.2881, Rank #1**. This is the quantitative form of the chemical reasoning below — physically-strong but unsafe candidates lose biocompatibility points and fall:

| candidate(s) | disposition |
|---|---|
| Ra | radioactive — excluded |
| Pb, Tl, Bi, Hg, Cd | toxic heavy metals — excluded |
| Eu, Gd, Tb, Dy, Ho, Y, Yb, La (rare earths) | +3 substitution introduces charge-compensating defects that weaken the divalent lattice |
| Pt, Pd, Au, Ag, Rh, Ir (noble) | redox / cost; favor M(0) over stable M2+ |

The viable, biocompatible, synthesizable survivors are 3d transition metals; **Ni is Rank #1** among them. The manuscript synthesizes and characterizes **Ni, Co, Cu, Mg**.

## 5. Conclusion

The Physics-Score ranking (Ni #1), the XGBoost extension (Ni #1), and the Stage-3 chemistry filter together make **Ni the top-ranked viable substituent** in this computational screen. The hardness model and DFT (Sections in the README) give the mechanistic, CFSE-based rationale. The experimental confirmation of Ni's superior reinforcement is reported in the manuscript and its Supporting Information.
