# AI/ML Screening — 5D Pareto Analysis

This note documents how the computational results in this repository form a predictive system for
**rational materials design**. In particular, it details the **5D Pareto optimization** that fuses
a theoretical descriptor (CFSE/OSSE) with MD-derived descriptors (PMF, MSD, Lindemann) to identify
the optimal metal substituent for whitlockite.

---

## 1. Methodology: a data-driven screen

Rather than a purely theory-driven approach, we use a **data-driven** strategy: MD simulations of
21 metals provide the training data; an XGBoost model then predicts the properties of all 45
candidate elements, over which the Pareto-optimal set is searched.

### The five metrics (5D)
1. **Stability** — MSD (dynamic stability; minimize)
2. **Structure** — Lindemann index (structural rigidity; minimize)
3. **Binding** — PMF, potential of mean force (M–O binding; minimize / deeper)
4. **Size fit** — radius mismatch vs. Mg (geometric compatibility; minimize)
5. **Geometry** — OSSE, octahedral site stabilization energy (octahedral preference; maximize)

---

## 2. Pareto optimization & scree-plot analysis

### 2.1 The 12 survivors
Across the five axes, the **non-dominated set (Pareto frontier)** over the 45 candidates contains
**12 elements**. Ranking by Utopia-point distance, the score drops sharply after rank 12 (an
**elbow** in the scree plot), defining these as **Tier-1 candidates**.

### 2.2 Period distribution
The periodic-table distribution of the Top-12 survivors shows a clear trend:

| Period | Elements (count) | Character |
|---|---|---|
| **4 (3d)** | **Ni, Cr, V, Co, Cu (5)** | **ranks 1–5** — light and efficient |
| **5 (4d)** | Rh, Tc (2) | |
| **6 (5d/4f)** | Pt, W, Tb, Eu, Ir (5) | heavy (good MSD), strong binding (good PMF), but geometrically unsuitable (OSSE / size) |

**Takeaway:** the **light, geometrically compatible 3d transition metals outperform** the heavy,
expensive 5d/6d elements and occupy the Top 5.

---

## 3. Final ranking (Utopia distance)

1. **Ni (Rank #1)** — the most balanced profile (OSSE 1.0, PMF 0.73, Lindemann 0.62); uniformly
   strong across all metrics.
2. **Cr (#2), V (#3)** — good OSSE but lower structural stability (Lindemann) than Ni.
3. **Co (#4), Cu (#5)** — sub-optimal analogues of Ni.
4. **Pt (#6), W (#7)** — good mass (MSD) and binding (PMF / CFSE) but **geometrically unsuitable
   (OSSE = 0)**, demoting them to mid-rank.

**Conclusion:** the 5D multi-objective optimization identifies **Ni as the optimal substituent**.
Experimental validation is reported in the manuscript and its Supporting Information.
