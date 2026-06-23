# AI/ML Screening - 5D Pareto and Utopia-Distance Analysis

This note documents how the computational results in this repository form a predictive system for **rational materials design**. The 5D screen combines a theoretical descriptor (OSSE/CFSE-related octahedral stabilization) with MD-derived descriptors (PMF, MSD, Lindemann) to identify the optimal metal substituent for whitlockite.

---

## 1. Methodology: a data-driven screen

MD simulations of 21 metals provide the training data. XGBoost then predicts key descriptors for **52 candidate elements**, and the candidates are evaluated across five dimensions.

### The five metrics (5D)

1. **Stability** - MSD (dynamic stability; minimize)
2. **Structure** - Lindemann index (structural rigidity; minimize)
3. **Binding** - PMF, potential of mean force (M-O binding; minimize / deeper)
4. **Size fit** - radius mismatch vs. Mg (geometric compatibility; minimize)
5. **Geometry** - OSSE, octahedral site stabilization energy (octahedral preference; maximize)

---

## 2. Pareto optimization and Utopia-distance selection

### 2.1 Raw frontier vs. Tier-1 selection

The raw 5D Pareto frontier is intentionally permissive and large. In `outputs/pareto_5d_xgboost.csv`, **38 metals are non-dominated**. The same output includes `Dist` and `Rank` columns, which rank candidates by distance from the ideal Utopia point.

The manuscript-facing **Top-12 is the Utopia-distance Tier-1 selection**, not the raw non-dominated set. The authoritative ranking is `data/final_ranking_5d.csv`, which matches the XGBoost script output `outputs/pareto_5d_xgboost.csv`.

### 2.2 Authoritative Top-12

The authoritative Top-12 Utopia-distance ranking is:

1. **Ni**
2. **Cr**
3. **V**
4. **Co**
5. **Cu**
6. **W**
7. **Eu**
8. **Ho**
9. **Dy**
10. **Tb**
11. **Tc**
12. **Au**

Ni is **Rank #1**, and the leading 3d-metal Top-5 is **Ni, Cr, V, Co, Cu**.

### 2.3 Period distribution

| Period | Elements (count) | Character |
|---|---|---|
| **4 (3d)** | **Ni, Cr, V, Co, Cu (5)** | Leading Utopia-distance Top-5; light and geometrically compatible. |
| **5 (4d)** | Tc (1) | Tc is radioactive. |
| **6 (5d/4f)** | W, Eu, Ho, Dy, Tb, Au (6) | Heavy elements with useful predicted descriptors but chemical viability limits. |

**Takeaway:** the 3d transition-metal candidates occupy the Top-5, and Ni is the best-balanced candidate by Utopia distance.

---

## 3. Final ranking and chemistry filters

The XGBoost pipeline `src/run_5d_pareto_xgboost.py` reproduces `data/final_ranking_5d.csv` exactly, including Ni Rank #1 and the 3d Top-5 (Ni, Cr, V, Co, Cu).

One-line disposition of each non-Ni authoritative Top-12 candidate:

| candidate(s) | disposition |
|---|---|
| Cr, V, Co, Cu | Viable 3d M2+ candidates, but rank below Ni by Utopia distance. |
| W | High-valence W(+6) chemistry creates charge imbalance in the divalent substitution site. |
| Eu, Tb, Ho, Dy | Rare-earth +3 substitution weakens the lattice through charge-compensating defects. |
| Tc | Radioactive; not viable for a biomaterial. |
| Au | Noble-metal redox favors reduction to Au(0) rather than stable M2+ substitution. |

**Conclusion:** the 5D Utopia-distance ranking and chemistry filters identify **Ni as the optimal substituent**. Experimental validation is reported in the manuscript and its Supporting Information.
