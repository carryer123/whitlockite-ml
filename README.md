# Ni-Whitlockite: Computational Screening (MD → AI → DFT)

[![Method](https://img.shields.io/badge/method-MD%20%E2%86%92%20AI%20%E2%86%92%20DFT-blue?style=flat-square)](#pipeline)
[![Model](https://img.shields.io/badge/ML-XGBoost%205D%20Pareto-success?style=flat-square)](#3-aiml-45-element-screening)
[![MD](https://img.shields.io/badge/MD-GROMACS%2021%20metals-blue?style=flat-square)](#2-md-screening-21-metals)
[![DFT](https://img.shields.io/badge/DFT-Quantum%20ESPRESSO%20%2B%20LOBSTER-blue?style=flat-square)](#4-dft-verification)
[![Paper](https://img.shields.io/badge/manuscript-Advanced%20Materials-orange?style=flat-square)](#citation)

The **computational pipeline** behind the manuscript *"Unveiling the Superiority of Ni-Whitlockite"* —
a multi-scale screening (molecular dynamics → machine learning → DFT) that identifies **nickel (Ni)**
as the optimal metal substituent for high-hardness metal-substituted **whitlockite** (Ca₁₀M(PO₄)₇),
a bone-graft biomaterial.

> **Scientific question.** In Ca₁₀M(PO₄)₇, which substituent M maximizes hardness, and why?
> **Hypothesis.** A *d⁸* transition metal (Ni) maximizes strength via crystal-field stabilization
> energy (CFSE) and a structurally distorted lattice.

*This repository contains the computational/ML pipeline, data, and result figures only.
Experimental characterization (XRD / XPS / FTIR / nanoindentation) is reported in the manuscript
and its Supporting Information.*

---

## Pipeline

```
Stage 1  MD screening (21 metals, GROMACS)             → MSD, RDF, PMF, Lindemann, CN
Stage 2  AI prediction (45 elements, XGBoost)          → 5D Pareto: 45 → 12 → 1 (Ni)
Stage 3  DFT verification (Quantum ESPRESSO + LOBSTER) → CFSE / electronic origin
```

## 2. MD screening (21 metals)

Large-scale GROMACS MD of 21 candidate M²⁺ substituents (single substitution at the M5 Wyckoff
6b site). Per-metal descriptors: **MSD** (dynamic stability), **RDF**, **PMF depth** (M–O binding),
**Lindemann index**, **CN_mean / CN_std** (local structural rigidity).
- Ni shows the **lowest potential energy** among 2+ metals and the **deepest PMF well (−14.25 kJ/mol)**.
- Data: `data/md_potential_energy_21metals.csv`, `data/spatial_heterogeneity_21metals.csv`,
  `data/md_timepoint_scores_21metals.csv`, `data/pmf_results.csv`.

## 3. AI/ML 45-element screening

**XGBoost** gradient-boosted-tree regressors (Chen & Guestrin, 2016) trained on the 21-metal MD
data predict MSD / Lindemann / PMF for **45 elements**, followed by **5D Pareto optimization**:

| axis | descriptor | objective |
|---|---|---|
| Stability | MSD | min |
| Structure | Lindemann | min |
| Binding | PMF | min (deeper) |
| Size fit | radius mismatch | min |
| Geometry | OSSE (octahedral site stabilization) | max |

**45 → 12 → 1.** The Pareto frontier yields **12 non-dominated survivors**
(`Ni, Co, Pt, Pd, W, Mo, Rh, Ir, Ru, Os, Pb, Eu`); a scree-plot elbow defines Tier-1; a
materials-science elimination (W/Mo +6 and rare-earth +3 → charge-imbalance defects;
Pt/Pd/Au d⁸ low-spin square-planar → structural collapse) leaves **Ni as Rank #1**
(5D Utopia-distance). A separate hardness model (n = 4: Mg/Co/Ni/Cu) shows **CFSE dominates**
the feature importance and reproduces the ranking **Ni > Co > Mg > Cu**.

| ![5D Pareto](figures/final_5d_pareto.png) | ![Radar](figures/nature_radar_5d.png) |
|:--:|:--:|
| 5D Pareto frontier (Ni highlighted) | 5D radar: why Ni |

## 4. DFT verification

Quantum ESPRESSO (PBE+U) + LOBSTER for the electronic origin (CFSE / COHP). Ni's near-degenerate
high/low-spin states cause charge sloshing & spin frustration, resolved with a 42-atom primitive
cell and a 2-step protocol (nspin=1 relax → nspin=2 energy). See `docs/DFT_convergence_criteria.md`.

---

## Reproduce the ML
```bash
pip install -r requirements.txt
python src/run_5d_pareto_xgboost.py        # -> outputs/pareto_5d_xgboost.csv  (Ni on Pareto frontier)
python src/run_loocv_hardness_xgboost.py   # -> outputs/loocv_hardness_xgboost.csv (CFSE-dominant, Ni>Co>Mg>Cu)
```

## Repository structure
```
src/        XGBoost ML pipeline (5D Pareto, LOOCV hardness)  — reproducible
data/       MD descriptors (21 metals), 45-element predictions, rankings, hardness (n=4)
figures/    5D Pareto / radar / scree-plot result figures
docs/        AI analysis & validation, DFT convergence, Pareto survivor analysis
outputs/    reproduced result CSVs
```

## Authors & Contributors
- **Jung Heon Lee** — [@juhelee7](https://github.com/juhelee7) — supervision, corresponding author
- **Jina Bae** — [@jinjin-del](https://github.com/jinjin-del) — experiments (synthesis & characterization)
- **Byoungsang Lee** — [@carryer123](https://github.com/carryer123) — MD / DFT / ML computation (this repo)

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

## Software
GROMACS 2023.3 · Quantum ESPRESSO 7.3.1 · LOBSTER 5.1.0 · XGBoost · scikit-learn · NumPy · pandas · matplotlib.

## Citation
Manuscript: *"Unveiling the Superiority of Ni-Whitlockite"* (submitted to **Advanced Materials**).
ML method: Chen, T. & Guestrin, C. *XGBoost: A Scalable Tree Boosting System.* KDD 2016.
