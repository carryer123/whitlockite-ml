# Ni-Whitlockite: Computational Screening (MD → Physics Score → XGBoost)

[![Method](https://img.shields.io/badge/method-MD%20%E2%86%92%20PhysicsScore%20%E2%86%92%20XGBoost-blue?style=flat-square)](#pipeline)
[![Model](https://img.shields.io/badge/ML-XGBoost-success?style=flat-square)](#3-xgboost-extension-to-the-candidate-library)
[![MD](https://img.shields.io/badge/MD-GROMACS%2021%20metals-blue?style=flat-square)](#2-physics-score-21-metals)
[![DFT](https://img.shields.io/badge/DFT-Quantum%20ESPRESSO%20%2B%20LOBSTER-blue?style=flat-square)](#5-dft-verification)
[![Paper](https://img.shields.io/badge/manuscript-Advanced%20Materials-orange?style=flat-square)](#citation)

The **computational pipeline** behind the PAiCER manuscript ranks **nickel (Ni)** as the **top divalent substituent** for metal-substituted **whitlockite** (a calcium-phosphate bone-graft biomaterial) — Rank #1 by this computational screen after the stated chemical filters. (The experimental confirmation that Ni is optimal is reported in the manuscript, not in this repository.) The screen runs molecular dynamics → a physics-based scoring function → an XGBoost extension over the full candidate library, and ranks **Ni at #1 with a Physics Score of 282.19**.

> **Scientific question.** Which substituent M gives the best reinforcement profile in metal-substituted whitlockite?
> **Hypothesis.** A d8 transition metal (Ni) maximizes strength through crystal-field stabilization (CFSE) and a regular octahedral preference in a distorted lattice.

*This repository contains the computational/ML pipeline, its input data, and reproduced result tables only. Experimental characterization (XRD / XPS / FTIR / nanoindentation) is reported in the manuscript and its Supporting Information.*

---

## Pipeline

```text
Stage 1  Physics-based score (21 metals, MD + theory)   -> Physics Score; Ni = 282.19 (Rank #1)
Stage 2  XGBoost extension (full candidate library)     -> Physics Score predicted for every element
Stage 3  Chemistry / biocompatibility / synthesis filter-> remove unviable candidates
Stage 4  Hardness model (n = 4) + DFT verification      -> Ni > Co > Mg > Cu; CFSE / electronic origin
```

## 2. Physics Score (21 metals)

`src/physics_score_21metals.py` computes the manuscript **Physics Score** for the 21 MD-screened metal-substituted whitlockites from MD- and theory-derived descriptors **only** (the four measured hardness values are read back at the very end solely to report a validation correlation; they are never used in scoring).

The score is a weighted additive combination of:

| group | descriptors | weight basis |
|---|---|---|
| dynamic stability | MSD (50 ns, temporal stability, trend) | physical, fixed |
| structural uniformity | Lindemann CV, coordination-number CV | physical, fixed |
| bond strength | RDF peak height / width, time consistency | physical, fixed |
| crystallinity | calculated XRD peak count | physical, fixed |
| electronic / geometric | CFSE, ionic-radius match, Jahn-Teller penalty | ligand-field theory |

Running it reproduces **Ni Physics Score = 282.1932 (Rank #1)** and a validation Pearson r = 0.855 against the four measured hardness values — matching the manuscript Table S1 (MD-data rows).

## 3. XGBoost extension to the candidate library

`src/predict_candidates_xgboost.py` trains an **XGBoost** regressor (Chen & Guestrin, 2016) on the 21 Stage-1 Physics Scores using theoretical atomic descriptors as features, then predicts the Physics Score for every candidate element. **Ni remains Rank #1 (282.19);** CFSE is the dominant feature. (The candidate library spans **62 elements** across the periodic table; the manuscript Table S1 reports the **45 divalent-relevant** candidates — Ni is Rank #1 in both.)

The authoritative reproduced ranking is `outputs/physics_ranking_xgboost.csv` (manuscript Table S1).

> **Note.** The ranking uses XGBoost (Chen & Guestrin, 2016), the algorithm named in the manuscript. The Stage-1 Physics Scores for the 21 MD-screened metals — including **Ni = 282.19 (Rank #1)** — are model-independent and reproduce exactly.

## 4. Stage-3 chemistry / biocompatibility / synthesis filter

The Physics-Score ranking is a physical-property screen; it does not encode chemical viability. Candidates ranked near the top but unsuitable for a divalent biomaterial substitution are removed on independent chemical grounds (this is the manuscript's Stage 3, not a column in the scoring code):

| removed | reason |
|---|---|
| Ra, (radioactive) | not viable for a biomaterial |
| Pb, Tl, Bi, Hg, Cd | toxic heavy metals |
| Eu, Gd, Tb, Dy, Ho, Y, Yb, La… | rare-earth +3; charge-compensating defects weaken the divalent lattice |
| Pt, Pd, Au, Ag, Rh, Ir… | noble-metal redox / cost; favor M(0) over stable M2+ |

What survives as divalent, biocompatible, synthesizable candidates are 3d transition metals; among them **Ni is Rank #1**, and the manuscript synthesizes and characterizes **Ni, Co, Cu, Mg**.

## 5. Hardness model and DFT verification

- `src/run_loocv_hardness_xgboost.py` — an **exploratory n = 4** hardness model (Mg/Co/Ni/Cu). The full-fit XGBoost model (`outputs/hardness_fullfit_importance_xgboost.csv`) shows **CFSE as the dominant descriptor** and reproduces the experimental order **Ni > Co > Mg > Cu** *in-sample*. With only n = 4 this is a diagnostic, **not** a validated predictor: the leave-one-out file (`outputs/loocv_hardness_xgboost.csv`) is retained transparently and its per-fold point predictions should **not** be cited as evidence for ranking or feature importance.
- DFT: Quantum ESPRESSO (PBE+U) + LOBSTER address the electronic origin (CFSE / COHP). Ni's near-degenerate high/low-spin states are handled with a 42-atom primitive cell and a two-step protocol (`nspin=1` relaxation → `nspin=2` energy). See `docs/DFT_convergence_criteria.md`.

---

## Reproduce

```bash
pip install -r requirements.txt
python src/physics_score_21metals.py        # Stage 1 -> outputs/physics_score_21metals.csv  (Ni = 282.1932)
python src/predict_candidates_xgboost.py     # Stage 2 -> outputs/physics_ranking_xgboost.csv (Ni #1)
python src/run_loocv_hardness_xgboost.py     # hardness model (full-fit + LOO diagnostic)
```

## Repository structure

```text
src/        physics-score pipeline (Stage 1), XGBoost extension (Stage 2), hardness model
data/       MD descriptors (21 metals), calculated XRD peak counts, hardness (n=4)
docs/       analysis & validation notes, DFT convergence, data dictionary, ranking dump
outputs/    reproduced result tables
```

## Authors & Contributors

- **Jung Heon Lee** — [@juhelee7](https://github.com/juhelee7) — supervision, corresponding author
- **Jina Bae** — [@jinjin-del](https://github.com/jinjin-del) — experiments (synthesis & characterization)
- **Byoungsang Lee** — [@carryer123](https://github.com/carryer123) — MD / DFT / ML computation (this repo)

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

## Software

GROMACS (MD); Quantum ESPRESSO 7.3.1 + LOBSTER 5.1.0 (DFT); XGBoost, NumPy, pandas (ML).

## Citation

Manuscript: PAiCER (Bae *et al.*), submitted to **Advanced Materials**.
ML method: Chen, T. & Guestrin, C. *XGBoost: A Scalable Tree Boosting System.* KDD 2016.
