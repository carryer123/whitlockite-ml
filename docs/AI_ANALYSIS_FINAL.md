# AI/ML Screening — Physics Score and XGBoost Extension

This note documents how the computational results in this repository form a predictive system for **rational materials design**, and how they identify **Ni** as the optimal divalent substituent for whitlockite.

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

`src/predict_45elements_xgboost.py` trains XGBoost on the 21 Physics Scores using theoretical atomic descriptors, then predicts every candidate element (`outputs/physics_ranking_45elements_xgboost.csv`). **Ni stays Rank #1 (282.19); CFSE is the dominant feature** (importance ≈ 0.5).

**Model note.** The ranking uses XGBoost (Chen & Guestrin, 2016), the algorithm named in the manuscript. The 21 MD-data scores (including Ni = 282.19) are Stage-1 values and reproduce exactly.

## 4. Stage 3 — chemistry / biocompatibility / synthesis filter

The Physics Score is a physical-property screen and does not encode chemical viability. Top-ranked but unviable candidates are removed on independent grounds:

| candidate(s) | disposition |
|---|---|
| Ra | radioactive — excluded |
| Pb, Tl, Bi, Hg, Cd | toxic heavy metals — excluded |
| Eu, Gd, Tb, Dy, Ho, Y, Yb, La (rare earths) | +3 substitution introduces charge-compensating defects that weaken the divalent lattice |
| Pt, Pd, Au, Ag, Rh, Ir (noble) | redox / cost; favor M(0) over stable M2+ |

The viable, biocompatible, synthesizable survivors are 3d transition metals; **Ni is Rank #1** among them. The manuscript synthesizes and characterizes **Ni, Co, Cu, Mg**.

## 5. Conclusion

The Physics-Score ranking (Ni #1), the XGBoost extension (Ni #1), and the Stage-3 chemistry filter together identify **Ni as the optimal substituent**. The hardness model and DFT (Sections in the README) give the mechanistic, CFSE-based explanation. Experimental validation is reported in the manuscript and its Supporting Information.
