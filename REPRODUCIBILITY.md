# Reproducibility

Environment used to generate the committed `outputs/`:

- Python 3.12.6
- xgboost 3.3.0, numpy 2.1.1, pandas 2.3.0 (see `requirements.txt`)

```bash
pip install -r requirements.txt
python src/physics_score_21metals.py
python src/predict_candidates_xgboost.py
python src/physics_score_S2_21candidates.py
```

> On Windows, use the `py` launcher if `python` resolves to the Microsoft Store stub
> (e.g. `py src/physics_score_21metals.py`).

## Expected console output (key lines)

`python src/physics_score_21metals.py`
```
Ni Physics Score = 282.1932  (expected 282.1932)   |   Ni rank = #1
Saved: outputs/physics_score_21metals.csv
```

`python src/predict_candidates_xgboost.py`
```
XGBoost feature importance (top 4): [('CFSE', 0.507), ('Z', 0.139), ('EN', 0.137), ('polar', 0.075)]
Candidates ranked: 62
Ni Rank #1  |  Physics Score 282.1932  (Table S1: #1, 282.1932)
Saved: outputs/physics_ranking_xgboost.csv
```

`python src/physics_score_S2_21candidates.py`
```
Ni: Rank #1  Weighted sum 97.2881  (Table S2 target: #1, 97.2881)
Max |reproduced - published| Weighted sum over 21 candidates: 0.0001  -> PASS
Saved: outputs/physics_score_S2_21candidates.csv
```

## Notes

- The Layer-1 Physics Score for the 21 MD-screened metals (including **Ni = 282.1932**) is
  computed by a fixed weighted function and is independent of any ML model, so it reproduces
  exactly.
- `src/predict_candidates_xgboost.py` evaluates a broad candidate library of 62 elements spanning
  the periodic table. The manuscript Table S1 reports the 45 divalent-relevant candidates; Ni is
  Rank #1 in both.
- `src/physics_score_S2_21candidates.py` reproduces SI Table S2 (Ni = 97.2881) from the published
  per-element objective values to < 1e-3.
- The ML ranking takes **no measured hardness as input**; experimental nanoindentation is reported
  in the manuscript as independent validation only.
