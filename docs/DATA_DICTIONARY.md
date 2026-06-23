# Data Dictionary

This dictionary describes the CSV files under `data/`. Provenance labels are: MD-derived, XGBoost-predicted, experimental, and hand-coded descriptor.

## `data/md_timepoint_scores_21metals.csv`

| column | meaning / units | provenance |
|---|---|---|
| `Rank` | Rank from the integrated MD timepoint scoring workflow; unitless. | MD-derived |
| `Metal` | Metal substituent symbol. | hand-coded descriptor |
| `Integrated_Score` | Combined RDF/MSD stability score; unitless workflow score. | MD-derived |
| `RDF_10ns` | RDF-derived score at 10 ns; unitless workflow score. | MD-derived |
| `RDF_20ns` | RDF-derived score at 20 ns; unitless workflow score. | MD-derived |
| `RDF_30ns` | RDF-derived score at 30 ns; unitless workflow score. | MD-derived |
| `RDF_40ns` | RDF-derived score at 40 ns; unitless workflow score. | MD-derived |
| `RDF_50ns` | RDF-derived score at 50 ns; unitless workflow score. | MD-derived |
| `MSD_10ns` | Mean-squared-displacement-derived score at 10 ns; workflow MSD units. | MD-derived |
| `MSD_20ns` | Mean-squared-displacement-derived score at 20 ns; workflow MSD units. | MD-derived |
| `MSD_30ns` | Mean-squared-displacement-derived score at 30 ns; workflow MSD units. | MD-derived |
| `MSD_40ns` | Mean-squared-displacement-derived score at 40 ns; workflow MSD units. | MD-derived |
| `MSD_50ns` | Mean-squared-displacement-derived score at 50 ns; workflow MSD units. | MD-derived |
| `Avg_RDF_Score` | Average RDF score over sampled timepoints; unitless. | MD-derived |
| `Avg_MSD_Score` | Average MSD score over sampled timepoints; unitless. | MD-derived |
| `Final_RDF_Score` | Final weighted RDF score; unitless. | MD-derived |
| `Final_MSD_Score` | Final weighted MSD score; unitless. | MD-derived |
| `RDF_Temporal_Stability` | RDF temporal stability score; unitless. | MD-derived |
| `MSD_Temporal_Stability` | MSD temporal stability score; unitless. | MD-derived |
| `RDF_Trend_Score` | RDF trend score across timepoints; unitless. | MD-derived |
| `MSD_Trend_Score` | MSD trend score across timepoints; unitless. | MD-derived |

## `data/spatial_heterogeneity_21metals.csv`

| column | meaning / units | provenance |
|---|---|---|
| `cn_cv` | Coefficient of variation for coordination number; percent / unitless ratio. | MD-derived |
| `cn_mean` | Mean coordination number around the metal site; count. | MD-derived |
| `cn_std` | Standard deviation of coordination number; count. | MD-derived |
| `lindemann_cv` | Coefficient of variation for the Lindemann index; percent / unitless ratio. | MD-derived |
| `lindemann_mean` | Mean Lindemann index; unitless. | MD-derived |
| `lindemann_std` | Standard deviation of the Lindemann index; unitless. | MD-derived |
| `metal` | Metal substituent symbol. | hand-coded descriptor |

## `data/pmf_results.csv`

| column | meaning / units | provenance |
|---|---|---|
| `metal` | Metal substituent symbol. | hand-coded descriptor |
| `PMF_depth` | Depth of the potential-of-mean-force well; kJ/mol in this workflow. More negative values indicate deeper binding. | MD-derived |

## `data/md_potential_energy_21metals.csv`

| column | meaning / units | provenance |
|---|---|---|
| `Metal` | Metal substituent symbol. | hand-coded descriptor |
| `Group` | Periodic-table grouping used for analysis plots and summaries. | hand-coded descriptor |
| `Potential_Energy` | MD potential energy from the GROMACS workflow; kJ/mol in this workflow. | MD-derived |

## `data/ai_prediction_raw_45elements.csv`

Historical filename note: this CSV contains **52 candidate elements**.

| column | meaning / units | provenance |
|---|---|---|
| `Metal` | Candidate metal element symbol. | hand-coded descriptor |
| `MSD` | Candidate MSD descriptor used by the 5D screen; MD-derived for training metals and XGBoost-predicted for unsimulated candidates. | MD-derived / XGBoost-predicted |
| `Lindemann` | Candidate Lindemann descriptor; MD-derived for training metals and XGBoost-predicted for unsimulated candidates. | MD-derived / XGBoost-predicted |
| `CN_std` | Coordination-number standard deviation used as a local heterogeneity descriptor; count. | MD-derived / XGBoost-predicted |
| `CFSE` | Crystal-field stabilization energy proxy used as an electronic descriptor; relative descriptor units. | hand-coded descriptor |
| `Is_Pareto` | Boolean membership in the raw Pareto set in the earlier screening table. | XGBoost-predicted |

## `data/final_ranking_5d.csv`

This is the authoritative XGBoost ranking for the manuscript-facing 5D Utopia-distance selection.

| column | meaning / units | provenance |
|---|---|---|
| `Metal` | Candidate metal element symbol. | hand-coded descriptor |
| `MSD` | Candidate MSD descriptor used in the 5D ranking. | MD-derived / XGBoost-predicted |
| `Lindemann` | Candidate Lindemann descriptor used in the 5D ranking; unitless. | MD-derived / XGBoost-predicted |
| `PMF` | Candidate PMF depth used in the 5D ranking; kJ/mol in this workflow. | MD-derived / XGBoost-predicted |
| `Radius_Mismatch` | Absolute ionic-radius mismatch relative to the reference site radius; angstrom in this workflow. | hand-coded descriptor |
| `OSSE` | Octahedral site stabilization energy proxy; relative descriptor units. | hand-coded descriptor |
| `S_MSD` | Normalized MSD score, scaled so higher is better; unitless. | XGBoost-predicted |
| `S_Lind` | Normalized Lindemann score, scaled so higher is better; unitless. | XGBoost-predicted |
| `S_PMF` | Normalized PMF score, scaled so higher is better; unitless. | XGBoost-predicted |
| `S_Rad` | Normalized radius-mismatch score, scaled so higher is better; unitless. | hand-coded descriptor |
| `S_OSSE` | Normalized OSSE score, scaled so higher is better; unitless. | hand-coded descriptor |
| `Dist` | Euclidean distance from the 5D Utopia point; lower is better. | XGBoost-predicted |
| `Rank` | Utopia-distance rank; 1 is best. | XGBoost-predicted |

## `data/hardness_4metals.csv`

| column | meaning / units | provenance |
|---|---|---|
| `Metal` | Metal substituent symbol. | hand-coded descriptor |
| `atomic_num` | Atomic number. | hand-coded descriptor |
| `ionic_radius` | Ionic radius; angstrom. | hand-coded descriptor |
| `electronegativity` | Pauling electronegativity. | hand-coded descriptor |
| `d_electrons` | Nominal d-electron count. | hand-coded descriptor |
| `CFSE` | Crystal-field stabilization energy proxy; relative descriptor units. | hand-coded descriptor |
| `ionization_E` | First ionization energy descriptor; eV. | hand-coded descriptor |
| `atomic_mass` | Atomic mass; atomic mass units. | hand-coded descriptor |
| `valence_e` | Valence electron count. | hand-coded descriptor |
| `electron_affinity` | Electron affinity descriptor; eV. | hand-coded descriptor |
| `polarizability` | Atomic polarizability descriptor; cubic angstrom in this workflow. | hand-coded descriptor |
| `exp_hardness_MPa` | Experimentally measured hardness used for the n = 4 hardness model; MPa. | experimental |
