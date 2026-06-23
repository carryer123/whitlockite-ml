#!/usr/bin/env python3
"""
5D Pareto screening for metal-substituted whitlockite (XGBoost version).
=======================================================================
Reproduces the AI screening of the manuscript using XGBoost (gradient-boosted
trees; Chen & Guestrin, 2016), matching the method described in the paper.

Pipeline:
  1. From in-house MD (21 metals): targets MSD_50ns, lindemann_mean, PMF_depth.
  2. Features = atomic/ionic descriptors [Z, ionic_radius, mass, electronegativity,
     polarizability, OSSE].
  3. Train 3 XGBoost regressors to predict MSD / Lindemann / PMF.
  4. Extrapolate to all candidate elements; add Radius_Mismatch and OSSE.
  5. 5D Pareto optimization (minimize MSD/Lindemann/PMF/Radius, maximize OSSE).

Run from the repository root:  python src/run_5d_pareto_xgboost.py
"""
import os
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.preprocessing import MinMaxScaler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs"); os.makedirs(OUT, exist_ok=True)

XGB_PARAMS = dict(n_estimators=200, max_depth=3, learning_rate=0.1,
                  random_state=42, verbosity=0)

# ----------------------------------------------------------------------------
# 1. Load in-house MD descriptors (targets) for the 21 simulated metals
# ----------------------------------------------------------------------------
df_time = pd.read_csv(os.path.join(DATA, "md_timepoint_scores_21metals.csv"))
df_spat = pd.read_csv(os.path.join(DATA, "spatial_heterogeneity_21metals.csv"))
df_pmf = pd.read_csv(os.path.join(DATA, "pmf_results.csv"))

df_train = pd.merge(df_time[["Metal", "MSD_50ns"]],
                    df_spat[["metal", "lindemann_mean"]],
                    left_on="Metal", right_on="metal").drop(columns=["metal"])
df_train = pd.merge(df_train, df_pmf[["metal", "PMF_depth"]],
                    left_on="Metal", right_on="metal", how="left")
df_train = df_train.rename(columns={"PMF_depth": "PMF"}).dropna()
print(f"Training metals (MD): {len(df_train)}")

# ----------------------------------------------------------------------------
# 2. Atomic features [Z, ionic_radius(A), mass, electronegativity, polarizability]
#    + OSSE (octahedral site stabilization energy proxy, theoretical)
# ----------------------------------------------------------------------------
atomic_data = {
    'Mg':[12,0.72,24.31,1.31,15.0],'Ca':[20,1.00,40.08,1.00,11.9],'Sr':[38,1.18,87.62,0.95,11.0],
    'Ba':[56,1.35,137.3,0.89,10.0],'Ra':[88,1.48,226.0,0.90,10.1],'Be':[4,0.45,9.01,1.57,18.2],
    'V':[23,0.79,50.94,1.63,14.2],'Cr':[24,0.80,52.00,1.66,16.5],'Mn':[25,0.83,54.94,1.55,15.6],
    'Fe':[26,0.78,55.85,1.83,16.2],'Co':[27,0.75,58.93,1.88,17.1],'Ni':[28,0.69,58.69,1.91,18.2],
    'Cu':[29,0.73,63.55,1.90,20.3],'Zn':[30,0.74,65.38,1.65,18.0],'Pd':[46,0.86,106.4,2.20,19.4],
    'Cd':[48,0.95,112.4,1.69,16.9],'Pt':[78,0.63,195.1,2.28,18.6],'Au':[79,0.85,197.0,2.54,20.5],
    'Hg':[80,1.02,200.6,2.00,18.8],'Sc':[21,0.75,44.96,1.36,12.8],'Ti':[22,0.67,47.87,1.54,13.6],
    'Y':[39,0.90,88.91,1.22,12.2],'Zr':[40,0.72,91.22,1.33,13.1],'Nb':[41,0.72,92.91,1.60,14.3],
    'Mo':[42,0.69,95.95,2.16,16.2],'Tc':[43,0.65,98.00,1.90,15.3],'Ru':[44,0.68,101.1,2.20,16.8],
    'Rh':[45,0.67,102.9,2.28,18.1],'Ag':[47,1.15,107.9,1.93,21.5],'Hf':[72,0.71,178.5,1.30,14.9],
    'Ta':[73,0.72,181.0,1.50,16.2],'W':[74,0.66,183.8,2.36,17.7],'Re':[75,0.63,186.2,1.90,16.6],
    'Os':[76,0.63,190.2,2.20,17.0],'Ir':[77,0.68,192.2,2.20,17.0],'Sn':[50,0.69,118.7,1.96,14.6],
    'Pb':[82,1.19,207.2,2.33,15.0],'Sm':[62,0.96,150.4,1.17,11.1],'Eu':[63,0.95,152.0,1.20,11.2],
    'Er':[68,0.89,167.3,1.24,11.9],'Yb':[70,0.87,173.1,1.10,12.2],'La':[57,1.03,138.9,1.10,11.1],
    'Ce':[58,1.01,140.1,1.12,10.9],'Pr':[59,0.99,140.9,1.13,10.6],'Nd':[60,0.98,144.2,1.14,10.7],
    'Pm':[61,0.97,145.0,1.13,10.9],'Gd':[64,0.94,157.3,1.20,12.1],'Tb':[65,0.92,158.9,1.20,11.5],
    'Dy':[66,0.91,162.5,1.22,11.7],'Ho':[67,0.90,164.9,1.23,11.8],'Tm':[69,0.88,168.9,1.25,12.1],
    'Lu':[71,0.86,175.0,1.27,13.9]
}
osse_map = {'Ni':12.0,'Co':8.0,'Fe':4.0,'Mn':0.0,'Cr':12.0,'V':8.0,'Cu':6.0,'Zn':0.0,
            'Mg':0.0,'Ca':0.0,'Sr':0.0,'Ba':0.0,'Pd':0.0,'Pt':0.0,'Au':0.0,'W':0.0,'Mo':0.0}
radius_map = {k: v[1] for k, v in atomic_data.items()}

# ----------------------------------------------------------------------------
# 3. Train XGBoost regressors for the 3 MD descriptors
# ----------------------------------------------------------------------------
X_train, y_msd, y_lind, y_pmf = [], [], [], []
for _, row in df_train.iterrows():
    m = row["Metal"]
    if m in atomic_data:
        X_train.append(atomic_data[m] + [osse_map.get(m, 0.0)])
        y_msd.append(row["MSD_50ns"]); y_lind.append(row["lindemann_mean"]); y_pmf.append(row["PMF"])

model_msd = XGBRegressor(**XGB_PARAMS).fit(np.array(X_train), np.array(y_msd))
model_lind = XGBRegressor(**XGB_PARAMS).fit(np.array(X_train), np.array(y_lind))
model_pmf = XGBRegressor(**XGB_PARAMS).fit(np.array(X_train), np.array(y_pmf))

# ----------------------------------------------------------------------------
# 4. Predict for all candidate elements
# ----------------------------------------------------------------------------
rows = []
for m, props in atomic_data.items():
    f = np.array([props + [osse_map.get(m, 0.0)]])
    rows.append({"Metal": m,
                 "MSD": float(model_msd.predict(f)[0]),
                 "Lindemann": float(model_lind.predict(f)[0]),
                 "PMF": float(model_pmf.predict(f)[0]),
                 "Radius_Mismatch": abs(radius_map[m] - 0.72),
                 "OSSE": osse_map.get(m, 0.0)})
df_res = pd.DataFrame(rows)

# ----------------------------------------------------------------------------
# 5. 5D Pareto optimization
# ----------------------------------------------------------------------------
sc = MinMaxScaler(); dn = df_res.copy()
dn["S_MSD"] = 1 - sc.fit_transform(df_res[["MSD"]])
dn["S_Lind"] = 1 - sc.fit_transform(df_res[["Lindemann"]])
dn["S_PMF"] = 1 - sc.fit_transform(df_res[["PMF"]])
dn["S_Rad"] = 1 - sc.fit_transform(df_res[["Radius_Mismatch"]])
dn["S_OSSE"] = sc.fit_transform(df_res[["OSSE"]])
costs = dn[["S_MSD", "S_Lind", "S_PMF", "S_Rad", "S_OSSE"]].values

pareto = []
for i in range(len(costs)):
    if not any((np.all(costs[j] >= costs[i]) and np.any(costs[j] > costs[i]))
               for j in range(len(costs)) if j != i):
        pareto.append(i)
df_res["Is_Pareto"] = False
df_res.loc[df_res.index[pareto], "Is_Pareto"] = True

pareto_metals = df_res[df_res["Is_Pareto"]]["Metal"].tolist()
df_res.to_csv(os.path.join(OUT, "pareto_5d_xgboost.csv"), index=False)

print("\nXGBoost feature importance (MSD model):",
      dict(zip(["Z","r_ion","mass","EN","polar","OSSE"],
               np.round(model_msd.feature_importances_, 3))))
print(f"5D Pareto frontier (XGBoost): {pareto_metals}")
print(f"Ni on Pareto frontier? {'YES' if 'Ni' in pareto_metals else 'NO'}")
print(f"Saved: {os.path.join(OUT, 'pareto_5d_xgboost.csv')}")
