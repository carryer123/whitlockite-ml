# Reproducibility

Environment used to generate the committed `outputs/`:

- Python 3.12.6
- xgboost 3.3.0, numpy 2.1.1, pandas 2.3.0 (see `requirements.txt`)

```bash
pip install -r requirements.txt
python src/physics_score_21metals.py
python src/predict_candidates_xgboost.py
python src/run_loocv_hardness_xgboost.py
```

## Expected console output (key lines)

`python src/physics_score_21metals.py`
```
Ni Physics Score = 282.1932  (expected 282.1932)   |   Ni rank = #1
Validation Pearson r (n=4) = 0.855
Saved: outputs/physics_score_21metals.csv
```

`python src/predict_candidates_xgboost.py`
```
XGBoost feature importance (top 4): [('CFSE', 0.507), ('Z', 0.139), ('EN', 0.137), ('polar', 0.075)]
Candidates ranked: 62
Ni Rank #1  |  Physics Score 282.1932  (Table S1: #1, 282.1932)
Saved: outputs/physics_ranking_xgboost.csv
```

`python src/run_loocv_hardness_xgboost.py`
```
Full-fit feature importance (top 4): CFSE-dominant
Predicted hardness ranking (XGBoost full-fit): Ni > Co > Mg > Cu
```

## Notes

- The Stage-1 Physics Score for the 21 MD-screened metals (including **Ni = 282.1932**) is
  computed by a fixed weighted function and is independent of any ML model, so it reproduces
  exactly.
- `src/predict_candidates_xgboost.py` evaluates a broad candidate library of 62 elements spanning
  the periodic table. The manuscript Table S1 reports the 45 divalent-relevant candidates; Ni is
  Rank #1 in both.
- The n = 4 hardness model (`src/run_loocv_hardness_xgboost.py`) is an exploratory, in-sample
  diagnostic only; its leave-one-out point predictions are not used as evidence for ranking.
