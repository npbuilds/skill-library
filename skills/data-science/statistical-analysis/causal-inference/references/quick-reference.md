# Causal Inference — Quick Reference


## Quick Reference

| Estimand | Definition | When to use |
|----------|-----------|-------------|
| **ATE** | Average Treatment Effect across entire population | Policy affects everyone |
| **ATT** | Average Treatment Effect on the Treated | Evaluating effect on those who actually took treatment |
| **ATU** | Average Treatment Effect on the Untreated | Predicting impact of expanding a program |
| **ITT** | Intent-to-Treat: effect of being *assigned* treatment | Non-compliance exists, want conservative estimate |
| **LATE** | Local Average Treatment Effect (compliers only) | IV setting, effect for those induced by instrument |

## Quick Reference

| First-stage F-statistic | Interpretation | Action |
|------------------------|---------------|--------|
| F > 104 (Stock-Yogo) | Strong instrument | Proceed with standard 2SLS |
| 10 < F < 104 | Moderate; some bias toward OLS | Use weak-instrument robust inference (Anderson-Rubin, LIML) |
| F < 10 | Weak instrument | Do not trust 2SLS; 2SLS bias approaches OLS bias |

## Quick Reference

| Method | How it works | Strengths | Weaknesses |
|--------|-------------|-----------|------------|
| **Exact matching** | Match on identical covariate values | No functional form assumptions | Curse of dimensionality; many unmatched units |
| **Coarsened exact matching** | Coarsen covariates into bins, then exact match | Reduces dimensionality; controls imbalance bound | Requires thoughtful binning |
| **Propensity score matching** | Match on estimated P(treatment \| X) | Collapses many covariates to one score | Model-dependent; can discard data; hides imbalance |
| **Inverse probability weighting** | Weight observations by 1/P(treatment) | Uses all data; efficient | Extreme weights when propensity scores near 0 or 1 |
| **Doubly robust** | Combines outcome model + propensity weighting | Consistent if either model is correct | More complex; still requires overlap assumption |

## Implementation Libraries

| Method | Python | R |
|--------|--------|---|
| General causal inference framework, DAGs, identification | `dowhy` | `dagitty` |
| Heterogeneous treatment effects (CATE), double ML | `econml` | `grf` (generalized random forests) |
| Uplift modeling, treatment effect estimation | `causalml` | `uplift` |
| Difference-in-differences | `differences`, `pyfixest` | `fixest`, `did` (Callaway-Sant'Anna) |
| Regression discontinuity | `rdrobust` (Python port) | `rdrobust`, `rddensity` |
| IV / 2SLS, panel data | `linearmodels` | `fixest`, `ivreg` |
| Propensity score matching, weighting | `causallib`, `dowhy` | `MatchIt`, `WeightIt` |
| Synthetic control | `SparseSC`, `SyntheticControlMethods` | `Synth`, `gsynth` |
| Bayesian causal impact (structural time series) | `causalimpact`, `tfcausalimpact` | `CausalImpact` (Google) |
| Sensitivity analysis (Cinelli-Hazlett) | `pysensemakr` | `sensemakr` |
