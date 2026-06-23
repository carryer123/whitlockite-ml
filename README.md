# Ni-Whitlockite ML Screening (XGBoost)

Reproducible machine-learning pipeline for the manuscript
**"Unveiling the Superiority of Ni-Whitlockite"** (metal-substituted whitlockite,
Ca10M(PO4)7, for high-hardness biomaterials).

The model is an **XGBoost** gradient-boosted-tree regressor (Chen & Guestrin, 2016).

## Pipeline
1. **MD screening (21 metals, in-house GROMACS):** descriptors MSD, Lindemann index,
   PMF depth, coordination number (CN_mean/CN_std).
2. **AI extrapolation (XGBoost):** atomic/ionic descriptors → predict MD descriptors
   for candidate elements.
3. **5D Pareto optimization:** MSD, Lindemann, PMF, radius mismatch, OSSE → Ni is the
   optimal (Pareto-frontier, rank-1) substituent.
4. **Hardness model + LOO-CV (n=4: Mg/Co/Ni/Cu):** CFSE dominates the feature
   importance; predicted hardness rank Ni > Co > Mg > Cu matches experiment.

## Reproduce
```bash
pip install -r requirements.txt
python src/run_5d_pareto_xgboost.py        # -> outputs/pareto_5d_xgboost.csv (Ni on Pareto frontier)
python src/run_loocv_hardness_xgboost.py   # -> outputs/loocv_hardness_xgboost.csv (CFSE importance, ranking)
```

## Data (`data/`)
| file | content |
|---|---|
| `md_timepoint_scores_21metals.csv` | MD RDF/MSD time-resolved scores (21 metals) |
| `spatial_heterogeneity_21metals.csv` | CN_mean, CN_std, Lindemann index (21 metals) |
| `pmf_results.csv` | PMF binding depth (per metal) |
| `hardness_4metals.csv` | experimental nanoindentation hardness + atomic features (n=4) |
| `final_ranking_5d_ORIGINAL.csv` | reference 5D Pareto ranking from the original analysis |

## Notes
- With n=4 experimentally validated metals, individual LOO point predictions are
  statistically limited; the robust, reproducible conclusions are the **CFSE-dominant
  feature importance** and the **Ni > Co > Mg > Cu hardness ranking** / **Ni Pareto-optimality**.
- Primary MD/DFT raw trajectories and inputs are archived separately (large files);
  available on request.

## Authors & Contributors
- **Jung Heon Lee** (이정헌) — [@juhelee7](https://github.com/juhelee7) — supervision, corresponding author
- **Jina Bae** (배진아) — [@jinjin-del](https://github.com/jinjin-del) — experiments (synthesis, XRD/XPS/FTIR, nanoindentation)
- **Byeongsang** — [@carryer123](https://github.com/carryer123) — MD / DFT / ML computation (this repo)

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

## Citation
Chen, T. & Guestrin, C. *XGBoost: A Scalable Tree Boosting System.* KDD 2016.
