#!/usr/bin/env python3
"""
Final AI 5D Pareto Analysis
===========================

Objective:
Identify optimal candidates using 5 independent metrics.
No artificial weighting or scoring. Just raw (or predicted) data.

Metrics:
1. MSD (MD) - Min
2. Lindemann (MD) - Min
3. PMF (MD) - Min (More Negative)
4. Radius Mismatch (Chem) - Min
5. OSSE (Chem) - Max

Method:
1. Train AI to predict MSD, Lindemann, PMF.
2. Use theoretical values for Radius and OSSE.
3. Perform 5D Pareto Optimization.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler

# Set style
plt.style.use('seaborn-v0_8-whitegrid')

print("=" * 70)
print("AI 5D Pareto Analysis")
print("Metrics: MSD, Lindemann, PMF, Radius, OSSE")
print("=" * 70)

# =============================================================================
# 1. DATA PREPARATION
# =============================================================================

# Load Data
base_path = "/home/lee/gromacs/whitlockite/70/allatom/analysis"
df_time = pd.read_csv(f"{base_path}/integrated_timepoint_scores_21metals.csv")
df_spatial = pd.read_csv(f"{base_path}/spatial_heterogeneity_results_complete.csv")
df_pmf = pd.read_csv("Experiment/ai/pmf_results.csv")

df_train = pd.merge(df_time[['Metal', 'MSD_50ns']], 
                    df_spatial[['metal', 'lindemann_mean']], 
                    left_on='Metal', right_on='metal')
df_train = df_train.drop(columns=['metal'])
df_train = pd.merge(df_train, df_pmf[['metal', 'PMF_depth']], left_on='Metal', right_on='metal', how='left')
df_train.rename(columns={'PMF_depth': 'PMF'}, inplace=True)
df_train = df_train.dropna()

# Atomic Features
atomic_data = {
    'Mg': [12, 0.72, 24.31, 1.31, 15.0], 'Ca': [20, 1.00, 40.08, 1.00, 11.9],
    'Sr': [38, 1.18, 87.62, 0.95, 11.0], 'Ba': [56, 1.35, 137.3, 0.89, 10.0],
    'Ra': [88, 1.48, 226.0, 0.90, 10.1], 'Be': [4, 0.45, 9.01, 1.57, 18.2],
    'V':  [23, 0.79, 50.94, 1.63, 14.2], 'Cr': [24, 0.80, 52.00, 1.66, 16.5],
    'Mn': [25, 0.83, 54.94, 1.55, 15.6], 'Fe': [26, 0.78, 55.85, 1.83, 16.2],
    'Co': [27, 0.75, 58.93, 1.88, 17.1], 'Ni': [28, 0.69, 58.69, 1.91, 18.2],
    'Cu': [29, 0.73, 63.55, 1.90, 20.3], 'Zn': [30, 0.74, 65.38, 1.65, 18.0],
    'Pd': [46, 0.86, 106.4, 2.20, 19.4], 'Cd': [48, 0.95, 112.4, 1.69, 16.9],
    'Pt': [78, 0.63, 195.1, 2.28, 18.6], 'Au': [79, 0.85, 197.0, 2.54, 20.5],
    'Hg': [80, 1.02, 200.6, 2.00, 18.8], 'Sc': [21, 0.75, 44.96, 1.36, 12.8],
    'Ti': [22, 0.67, 47.87, 1.54, 13.6], 'Y': [39, 0.90, 88.91, 1.22, 12.2],
    'Zr': [40, 0.72, 91.22, 1.33, 13.1], 'Nb': [41, 0.72, 92.91, 1.60, 14.3],
    'Mo': [42, 0.69, 95.95, 2.16, 16.2], 'Tc': [43, 0.65, 98.00, 1.90, 15.3],
    'Ru': [44, 0.68, 101.1, 2.20, 16.8], 'Rh': [45, 0.67, 102.9, 2.28, 18.1],
    'Ag': [47, 1.15, 107.9, 1.93, 21.5], 'Hf': [72, 0.71, 178.5, 1.30, 14.9],
    'Ta': [73, 0.72, 181.0, 1.50, 16.2], 'W': [74, 0.66, 183.8, 2.36, 17.7],
    'Re': [75, 0.63, 186.2, 1.90, 16.6], 'Os': [76, 0.63, 190.2, 2.20, 17.0],
    'Ir': [77, 0.68, 192.2, 2.20, 17.0], 'Sn': [50, 0.69, 118.7, 1.96, 14.6],
    'Pb': [82, 1.19, 207.2, 2.33, 15.0], 'Sm': [62, 0.96, 150.4, 1.17, 11.1],
    'Eu': [63, 0.95, 152.0, 1.20, 11.2], 'Er': [68, 0.89, 167.3, 1.24, 11.9],
    'Yb': [70, 0.87, 173.1, 1.10, 12.2], 'La': [57, 1.03, 138.9, 1.10, 11.1],
    'Ce': [58, 1.01, 140.1, 1.12, 10.9], 'Pr': [59, 0.99, 140.9, 1.13, 10.6],
    'Nd': [60, 0.98, 144.2, 1.14, 10.7], 'Pm': [61, 0.97, 145.0, 1.13, 10.9],
    'Gd': [64, 0.94, 157.3, 1.20, 12.1], 'Tb': [65, 0.92, 158.9, 1.20, 11.5],
    'Dy': [66, 0.91, 162.5, 1.22, 11.7], 'Ho': [67, 0.90, 164.9, 1.23, 11.8],
    'Tm': [69, 0.88, 168.9, 1.25, 12.1], 'Lu': [71, 0.86, 175.0, 1.27, 13.9]
}

# Theoretical Values
osse_map = {
    'Ni': 12.0, 'Co': 8.0, 'Fe': 4.0, 'Mn': 0.0, 'Cr': 12.0, 'V': 8.0,
    'Cu': 6.0, 'Zn': 0.0, 'Mg': 0.0, 'Ca': 0.0, 'Sr': 0.0, 'Ba': 0.0,
    'Pd': 0.0, 'Pt': 0.0, 'Au': 0.0, 'W': 0.0, 'Mo': 0.0 # Low spin / Non-d8 = 0
}

radius_map = {k: v[1] for k, v in atomic_data.items()}

# =============================================================================
# 2. TRAIN & PREDICT
# =============================================================================

X_train, y_msd, y_lind, y_pmf = [], [], [], []
for idx, row in df_train.iterrows():
    m = row['Metal']
    if m in atomic_data:
        features = atomic_data[m] + [osse_map.get(m, 0.0)]
        X_train.append(features)
        y_msd.append(row['MSD_50ns'])
        y_lind.append(row['lindemann_mean'])
        y_pmf.append(row['PMF'])

model_msd = GradientBoostingRegressor(random_state=42).fit(X_train, y_msd)
model_lind = GradientBoostingRegressor(random_state=42).fit(X_train, y_lind)
model_pmf = GradientBoostingRegressor(random_state=42).fit(X_train, y_pmf)

results = []
for m, props in atomic_data.items():
    features = [props + [osse_map.get(m, 0.0)]]
    
    results.append({
        'Metal': m,
        'MSD': model_msd.predict(features)[0],
        'Lindemann': model_lind.predict(features)[0],
        'PMF': model_pmf.predict(features)[0],
        'Radius_Mismatch': abs(radius_map[m] - 0.72), # vs Mg
        'OSSE': osse_map.get(m, 0.0)
    })

df_res = pd.DataFrame(results)

# =============================================================================
# 3. PARETO OPTIMIZATION
# =============================================================================

scaler = MinMaxScaler()
df_norm = df_res.copy()

df_norm['Score_MSD'] = 1 - scaler.fit_transform(df_res[['MSD']])
df_norm['Score_Lind'] = 1 - scaler.fit_transform(df_res[['Lindemann']])
df_norm['Score_PMF'] = 1 - scaler.fit_transform(df_res[['PMF']])
df_norm['Score_Rad'] = 1 - scaler.fit_transform(df_res[['Radius_Mismatch']])
df_norm['Score_OSSE'] = scaler.fit_transform(df_res[['OSSE']]) # Max is better

costs = df_norm[['Score_MSD', 'Score_Lind', 'Score_PMF', 'Score_Rad', 'Score_OSSE']].values
pareto_indices = []

for i in range(len(costs)):
    dominated = False
    for j in range(len(costs)):
        if i == j: continue
        if np.all(costs[j] >= costs[i]) and np.any(costs[j] > costs[i]):
            dominated = True
            break
    if not dominated:
        pareto_indices.append(i)

df_res['Is_Pareto'] = False
df_res.iloc[pareto_indices, df_res.columns.get_loc('Is_Pareto')] = True

pareto_metals = df_res[df_res['Is_Pareto']]['Metal'].tolist()
print(f"\nPareto Frontier (5D): {pareto_metals}")

# =============================================================================
# 4. VISUALIZATION
# =============================================================================

plt.figure(figsize=(16, 8))

cols = ['Score_MSD', 'Score_Lind', 'Score_PMF', 'Score_Rad', 'Score_OSSE']
labels = ['Stability', 'Structure', 'Binding', 'Size Fit', 'Geometry']

# Plot Ni
ni_row = df_norm[df_norm['Metal'] == 'Ni'].iloc[0]
plt.plot(range(5), ni_row[cols], color='red', linewidth=5, marker='o', label='Ni', zorder=10)

# Plot Others (Survivors)
for metal in pareto_metals:
    if metal != 'Ni':
        row = df_norm[df_res['Metal'] == metal].iloc[0]
        plt.plot(range(5), row[cols], color='gray', alpha=0.4, linewidth=1.5)

plt.xticks(range(5), labels, fontsize=14, fontweight='bold')
plt.ylabel('Normalized Score (1.0 = Best)', fontsize=14)
plt.title('5D Pareto Frontier: Why Ni?', fontsize=18, fontweight='bold')
plt.legend(loc='upper right')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('Experiment/ai-result/final_5d_pareto.png', dpi=300)
print("Saved: Experiment/ai-result/final_5d_pareto.png")

if 'Ni' in pareto_metals:
    print("SUCCESS: Ni is a 5D Pareto Solution!")
else:
    print("WARNING: Ni dominated.")
