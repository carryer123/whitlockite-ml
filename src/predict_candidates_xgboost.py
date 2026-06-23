#!/usr/bin/env python3
"""
Stage 2 - XGBoost extension of the Physics Score to the full candidate library.
==============================================================================
Trains an XGBoost regressor on the 21 MD-derived Physics Scores (Stage 1) using
theoretical atomic descriptors as features, then predicts the Physics Score for
every candidate element. This reproduces the manuscript PAiCER ranking (Table S1):
Ni is Rank #1 with Physics Score 282.19.

Model: XGBoost (Chen & Guestrin, 2016), the algorithm named in the manuscript.
The 21 MD-data rows (including Ni = 282.19) are the Stage-1 Physics Scores and are
model-independent, so they reproduce exactly.

Run from the repository root:  python src/predict_candidates_xgboost.py
"""
import os
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "outputs"); os.makedirs(OUT, exist_ok=True)

XGB_PARAMS = dict(n_estimators=100, max_depth=4, learning_rate=0.1,
                  random_state=42, verbosity=0)

# ----------------------------------------------------------------------------
# 1. Stage-1 Physics Scores for the 21 MD-screened metals
# ----------------------------------------------------------------------------
df_physics = pd.read_csv(os.path.join(OUT, "physics_score_21metals.csv"))

# ----------------------------------------------------------------------------
# 2. Theoretical atomic descriptors for the candidate library
#    [Z, electron_affinity, ionization_E, ionic_radius, electronegativity,
#     CFSE, polarizability, valence_e, d_electrons, Jahn-Teller flag]
# ----------------------------------------------------------------------------
atomic_data = {
    'Sc':{'Z':21,'EA':18.1,'IE':633,'radius':0.75,'EN':1.36,'CFSE':0.0,'polar':17.8,'val_e':3,'d_elec':1,'JT':0},
    'Ti':{'Z':22,'EA':7.6,'IE':658,'radius':0.67,'EN':1.54,'CFSE':0.4,'polar':14.6,'val_e':4,'d_elec':2,'JT':0},
    'V':{'Z':23,'EA':50.9,'IE':650,'radius':0.79,'EN':1.63,'CFSE':0.6,'polar':12.4,'val_e':5,'d_elec':3,'JT':0},
    'Cr':{'Z':24,'EA':64.3,'IE':653,'radius':0.80,'EN':1.66,'CFSE':1.2,'polar':11.6,'val_e':6,'d_elec':4,'JT':0},
    'Mn':{'Z':25,'EA':0,'IE':717,'radius':0.83,'EN':1.55,'CFSE':0.0,'polar':9.4,'val_e':7,'d_elec':5,'JT':0},
    'Fe':{'Z':26,'EA':15.7,'IE':762,'radius':0.78,'EN':1.83,'CFSE':0.4,'polar':8.4,'val_e':8,'d_elec':6,'JT':0},
    'Co':{'Z':27,'EA':63.7,'IE':760,'radius':0.75,'EN':1.88,'CFSE':0.8,'polar':7.5,'val_e':9,'d_elec':7,'JT':0},
    'Ni':{'Z':28,'EA':112.0,'IE':737,'radius':0.69,'EN':1.91,'CFSE':1.2,'polar':6.8,'val_e':10,'d_elec':8,'JT':0},
    'Cu':{'Z':29,'EA':118.4,'IE':746,'radius':0.73,'EN':1.90,'CFSE':0.6,'polar':6.2,'val_e':11,'d_elec':9,'JT':1},
    'Zn':{'Z':30,'EA':0,'IE':906,'radius':0.74,'EN':1.65,'CFSE':0.0,'polar':5.7,'val_e':12,'d_elec':10,'JT':0},
    'Y':{'Z':39,'EA':29.6,'IE':600,'radius':0.90,'EN':1.22,'CFSE':0.0,'polar':22.7,'val_e':3,'d_elec':1,'JT':0},
    'Zr':{'Z':40,'EA':41.1,'IE':640,'radius':0.72,'EN':1.33,'CFSE':0.4,'polar':17.9,'val_e':4,'d_elec':2,'JT':0},
    'Nb':{'Z':41,'EA':86.1,'IE':652,'radius':0.72,'EN':1.6,'CFSE':0.6,'polar':15.7,'val_e':5,'d_elec':4,'JT':0},
    'Mo':{'Z':42,'EA':71.9,'IE':684,'radius':0.69,'EN':2.16,'CFSE':1.2,'polar':12.8,'val_e':6,'d_elec':5,'JT':0},
    'Tc':{'Z':43,'EA':53.0,'IE':702,'radius':0.65,'EN':1.9,'CFSE':0.0,'polar':11.4,'val_e':7,'d_elec':5,'JT':0},
    'Ru':{'Z':44,'EA':101.3,'IE':710,'radius':0.68,'EN':2.2,'CFSE':0.4,'polar':9.6,'val_e':8,'d_elec':7,'JT':0},
    'Rh':{'Z':45,'EA':109.7,'IE':720,'radius':0.67,'EN':2.28,'CFSE':0.8,'polar':8.6,'val_e':9,'d_elec':8,'JT':0},
    'Pd':{'Z':46,'EA':54.2,'IE':804,'radius':0.86,'EN':2.20,'CFSE':1.2,'polar':4.8,'val_e':10,'d_elec':10,'JT':0},
    'Ag':{'Z':47,'EA':125.6,'IE':731,'radius':0.75,'EN':1.93,'CFSE':0.0,'polar':7.2,'val_e':11,'d_elec':10,'JT':0},
    'Cd':{'Z':48,'EA':0,'IE':868,'radius':0.95,'EN':1.69,'CFSE':0.0,'polar':7.4,'val_e':12,'d_elec':10,'JT':0},
    'Hf':{'Z':72,'EA':17.2,'IE':658,'radius':0.71,'EN':1.3,'CFSE':0.4,'polar':16.2,'val_e':4,'d_elec':2,'JT':0},
    'Ta':{'Z':73,'EA':31.0,'IE':761,'radius':0.72,'EN':1.5,'CFSE':0.6,'polar':13.1,'val_e':5,'d_elec':3,'JT':0},
    'W':{'Z':74,'EA':78.6,'IE':770,'radius':0.66,'EN':2.36,'CFSE':1.2,'polar':11.1,'val_e':6,'d_elec':4,'JT':0},
    'Re':{'Z':75,'EA':14.5,'IE':760,'radius':0.63,'EN':1.9,'CFSE':0.0,'polar':9.7,'val_e':7,'d_elec':5,'JT':0},
    'Os':{'Z':76,'EA':106.1,'IE':840,'radius':0.63,'EN':2.2,'CFSE':0.4,'polar':8.5,'val_e':8,'d_elec':6,'JT':0},
    'Ir':{'Z':77,'EA':151.0,'IE':880,'radius':0.68,'EN':2.20,'CFSE':0.8,'polar':7.6,'val_e':9,'d_elec':7,'JT':0},
    'Pt':{'Z':78,'EA':205.3,'IE':870,'radius':0.63,'EN':2.28,'CFSE':1.2,'polar':6.5,'val_e':10,'d_elec':8,'JT':0},
    'Au':{'Z':79,'EA':222.8,'IE':890,'radius':0.85,'EN':2.54,'CFSE':0.0,'polar':5.8,'val_e':11,'d_elec':10,'JT':0},
    'Hg':{'Z':80,'EA':0,'IE':1007,'radius':1.02,'EN':2.00,'CFSE':0.0,'polar':5.0,'val_e':12,'d_elec':10,'JT':0},
    'Be':{'Z':4,'EA':0,'IE':900,'radius':0.45,'EN':1.57,'CFSE':0.0,'polar':5.6,'val_e':2,'d_elec':0,'JT':0},
    'Mg':{'Z':12,'EA':0,'IE':738,'radius':0.72,'EN':1.31,'CFSE':0.0,'polar':10.6,'val_e':2,'d_elec':0,'JT':0},
    'Ca':{'Z':20,'EA':2.4,'IE':590,'radius':1.00,'EN':1.00,'CFSE':0.0,'polar':22.8,'val_e':2,'d_elec':0,'JT':0},
    'Sr':{'Z':38,'EA':5.0,'IE':549,'radius':1.18,'EN':0.95,'CFSE':0.0,'polar':27.6,'val_e':2,'d_elec':0,'JT':0},
    'Ba':{'Z':56,'EA':13.9,'IE':503,'radius':1.35,'EN':0.89,'CFSE':0.0,'polar':39.7,'val_e':2,'d_elec':0,'JT':0},
    'Ra':{'Z':88,'EA':9.6,'IE':509,'radius':1.48,'EN':0.90,'CFSE':0.0,'polar':38.3,'val_e':2,'d_elec':0,'JT':0},
    'Al':{'Z':13,'EA':42.5,'IE':578,'radius':0.54,'EN':1.61,'CFSE':0.0,'polar':6.8,'val_e':3,'d_elec':0,'JT':0},
    'Ga':{'Z':31,'EA':28.9,'IE':579,'radius':0.62,'EN':1.81,'CFSE':0.0,'polar':8.1,'val_e':3,'d_elec':10,'JT':0},
    'In':{'Z':49,'EA':28.9,'IE':558,'radius':0.80,'EN':1.78,'CFSE':0.0,'polar':10.2,'val_e':3,'d_elec':10,'JT':0},
    'Tl':{'Z':81,'EA':19.2,'IE':589,'radius':0.89,'EN':1.62,'CFSE':0.0,'polar':7.6,'val_e':3,'d_elec':10,'JT':0},
    'Sn':{'Z':50,'EA':107.3,'IE':709,'radius':0.69,'EN':1.96,'CFSE':0.0,'polar':7.7,'val_e':4,'d_elec':10,'JT':0},
    'Pb':{'Z':82,'EA':35.1,'IE':716,'radius':1.19,'EN':2.33,'CFSE':0.0,'polar':6.8,'val_e':4,'d_elec':10,'JT':0},
    'Bi':{'Z':83,'EA':91.2,'IE':703,'radius':1.03,'EN':2.02,'CFSE':0.0,'polar':7.4,'val_e':5,'d_elec':10,'JT':0},
    'La':{'Z':57,'EA':48.0,'IE':538,'radius':1.03,'EN':1.10,'CFSE':0.0,'polar':31.1,'val_e':3,'d_elec':1,'JT':0},
    'Ce':{'Z':58,'EA':50.0,'IE':534,'radius':1.01,'EN':1.12,'CFSE':0.0,'polar':29.6,'val_e':4,'d_elec':1,'JT':0},
    'Pr':{'Z':59,'EA':50.0,'IE':527,'radius':0.99,'EN':1.13,'CFSE':0.0,'polar':28.2,'val_e':3,'d_elec':0,'JT':0},
    'Nd':{'Z':60,'EA':50.0,'IE':533,'radius':0.98,'EN':1.14,'CFSE':0.0,'polar':31.4,'val_e':3,'d_elec':0,'JT':0},
    'Pm':{'Z':61,'EA':50.0,'IE':540,'radius':0.97,'EN':1.13,'CFSE':0.0,'polar':30.0,'val_e':3,'d_elec':0,'JT':0},
    'Sm':{'Z':62,'EA':50.0,'IE':545,'radius':0.96,'EN':1.17,'CFSE':0.0,'polar':28.8,'val_e':3,'d_elec':0,'JT':0},
    'Eu':{'Z':63,'EA':50.0,'IE':547,'radius':0.95,'EN':1.20,'CFSE':0.0,'polar':27.7,'val_e':3,'d_elec':0,'JT':0},
    'Gd':{'Z':64,'EA':50.0,'IE':593,'radius':0.94,'EN':1.20,'CFSE':0.0,'polar':23.5,'val_e':3,'d_elec':1,'JT':0},
    'Tb':{'Z':65,'EA':50.0,'IE':566,'radius':0.92,'EN':1.20,'CFSE':0.0,'polar':25.5,'val_e':3,'d_elec':0,'JT':0},
    'Dy':{'Z':66,'EA':50.0,'IE':573,'radius':0.91,'EN':1.22,'CFSE':0.0,'polar':24.5,'val_e':3,'d_elec':0,'JT':0},
    'Ho':{'Z':67,'EA':50.0,'IE':581,'radius':0.90,'EN':1.23,'CFSE':0.0,'polar':23.6,'val_e':3,'d_elec':0,'JT':0},
    'Er':{'Z':68,'EA':50.0,'IE':589,'radius':0.89,'EN':1.24,'CFSE':0.0,'polar':22.7,'val_e':3,'d_elec':0,'JT':0},
    'Tm':{'Z':69,'EA':50.0,'IE':597,'radius':0.88,'EN':1.25,'CFSE':0.0,'polar':21.8,'val_e':3,'d_elec':0,'JT':0},
    'Yb':{'Z':70,'EA':50.0,'IE':603,'radius':0.87,'EN':1.10,'CFSE':0.0,'polar':21.0,'val_e':3,'d_elec':0,'JT':0},
    'Lu':{'Z':71,'EA':50.0,'IE':524,'radius':0.86,'EN':1.27,'CFSE':0.0,'polar':21.9,'val_e':3,'d_elec':1,'JT':0},
    'Li':{'Z':3,'EA':59.6,'IE':520,'radius':0.76,'EN':0.98,'CFSE':0.0,'polar':24.3,'val_e':1,'d_elec':0,'JT':0},
    'Na':{'Z':11,'EA':52.8,'IE':496,'radius':1.02,'EN':0.93,'CFSE':0.0,'polar':24.1,'val_e':1,'d_elec':0,'JT':0},
    'K':{'Z':19,'EA':48.4,'IE':419,'radius':1.38,'EN':0.82,'CFSE':0.0,'polar':43.4,'val_e':1,'d_elec':0,'JT':0},
    'Rb':{'Z':37,'EA':46.9,'IE':403,'radius':1.52,'EN':0.82,'CFSE':0.0,'polar':47.3,'val_e':1,'d_elec':0,'JT':0},
    'Cs':{'Z':55,'EA':45.5,'IE':376,'radius':1.67,'EN':0.79,'CFSE':0.0,'polar':59.6,'val_e':1,'d_elec':0,'JT':0},
}
exp_hardness = {'Ni': 467.5, 'Co': 380.0, 'Mg': 320.0, 'Cu': 280.0}  # validation ONLY
FEAT = ['Z', 'EA', 'IE', 'radius', 'EN', 'CFSE', 'polar', 'val_e', 'd_elec', 'JT']

def vec(p):
    return [p['Z'], p['EA'], p['IE'], p['radius'], p['EN'], p['CFSE'], p['polar'], p['val_e'], p['d_elec'], p['JT']]

# ----------------------------------------------------------------------------
# 3. Train XGBoost on the 21 Physics Scores; target is NOT experimental data
# ----------------------------------------------------------------------------
train = df_physics[df_physics.Metal.isin(atomic_data)]
X = np.array([vec(atomic_data[m]) for m in train.Metal])
y = train.Physics_Score.values
model = XGBRegressor(**XGB_PARAMS).fit(X, y)

# ----------------------------------------------------------------------------
# 4. Predict for every candidate element (MD-data rows keep their Stage-1 score)
# ----------------------------------------------------------------------------
known = dict(zip(df_physics.Metal, df_physics.Physics_Score))
rows = []
for m, p in atomic_data.items():
    if m in known:
        rows.append({'Metal': m, 'Score': known[m], 'Type': 'MD Data', 'Experimental': exp_hardness.get(m, np.nan)})
    else:
        rows.append({'Metal': m, 'Score': float(model.predict(np.array([vec(p)]))[0]), 'Type': 'ML Prediction', 'Experimental': np.nan})
df = pd.DataFrame(rows).sort_values('Score', ascending=False).reset_index(drop=True)
df['Rank'] = np.arange(1, len(df) + 1)
df.to_csv(os.path.join(OUT, "physics_ranking_xgboost.csv"), index=False)

# ----------------------------------------------------------------------------
# 5. Report
# ----------------------------------------------------------------------------
imp = sorted(zip(FEAT, model.feature_importances_), key=lambda z: -z[1])
print("XGBoost feature importance (top 4):", [(f, round(float(v), 3)) for f, v in imp[:4]])
print(f"\nCandidates ranked: {len(df)}")
print(df.head(12).to_string(index=False))
ni = df[df.Metal == 'Ni'].iloc[0]
print(f"\nNi Rank #{int(ni.Rank)}  |  Physics Score {ni.Score:.4f}  (Table S1: #1, 282.1932)")
print("Saved: outputs/physics_ranking_xgboost.csv")
