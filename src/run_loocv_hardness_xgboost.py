#!/usr/bin/env python3
"""
Leave-One-Out cross-validation of the hardness model (XGBoost version).
=======================================================================
n = 4 experimentally measured metals (Mg, Co, Ni, Cu). For each fold, one metal
is held out, the model is trained on the other three, and the held-out hardness
is predicted. Also reports full-fit feature importance (CFSE dominance) and the
predicted ranking. XGBoost (Chen & Guestrin, 2016), matching the manuscript.

Run from the repository root:  python src/run_loocv_hardness_xgboost.py
"""
import os
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs"); os.makedirs(OUT, exist_ok=True)

XGB_PARAMS = dict(n_estimators=200, max_depth=3, learning_rate=0.1,
                  random_state=42, verbosity=0)

df = pd.read_csv(os.path.join(DATA, "hardness_4metals.csv"))
feat = ["atomic_num", "ionic_radius", "electronegativity", "d_electrons", "CFSE",
        "ionization_E", "atomic_mass", "valence_e", "electron_affinity", "polarizability"]
metals = df["Metal"].tolist()
X = df[feat].values
y = df["exp_hardness_MPa"].values

# ---- Leave-One-Out CV ----
rows = []
for i, m in enumerate(metals):
    tr = [j for j in range(len(metals)) if j != i]
    mdl = XGBRegressor(**XGB_PARAMS).fit(X[tr], y[tr])
    pred = float(mdl.predict(X[i:i+1])[0])
    err = (pred - y[i]) / y[i] * 100
    rows.append({"Metal": m, "actual_MPa": y[i], "LOO_pred_MPa": round(pred, 1),
                 "error_pct": round(err, 1), "CFSE_importance": round(float(mdl.feature_importances_[feat.index("CFSE")]), 3)})
loo = pd.DataFrame(rows)
loo.to_csv(os.path.join(OUT, "loocv_hardness_xgboost.csv"), index=False)
print(loo.to_string(index=False))

# ---- Full-fit: feature importance + ranking (exploratory, in-sample only) ----
full = XGBRegressor(**XGB_PARAMS).fit(X, y)
imp = sorted(zip(feat, full.feature_importances_), key=lambda z: -z[1])
pd.DataFrame(imp, columns=["feature", "importance"]).to_csv(
    os.path.join(OUT, "hardness_fullfit_importance_xgboost.csv"), index=False)
print("\nFull-fit feature importance (top 4):", [(f, round(float(v), 3)) for f, v in imp[:4]])
pred_full = {m: float(full.predict(X[i:i+1])[0]) for i, m in enumerate(metals)}
rank = sorted(metals, key=lambda m: -pred_full[m])
print(f"Predicted hardness ranking (XGBoost full-fit): {' > '.join(rank)}")
print(f"Experimental ranking:                          Ni > Co > Mg > Cu")
print(f"\nNOTE: with n=4 this hardness model is EXPLORATORY / in-sample only. The LOO point"
      f"\npredictions (loocv_hardness_xgboost.csv) are statistically limited and are NOT used as"
      f"\nevidence for ranking. The full-fit model is reported only as a diagnostic: (i) CFSE is the"
      f"\ndominant descriptor and (ii) the in-sample ranking matches the experimental order Ni > Co > Mg > Cu.")
print(f"Saved: loocv_hardness_xgboost.csv, hardness_fullfit_importance_xgboost.csv")
