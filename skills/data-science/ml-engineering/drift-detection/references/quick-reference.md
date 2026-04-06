# Drift Detection — Quick Reference


## Types of Drift

| Drift Type | What Changes | Detection Approach | Typical Cause |
|---|---|---|---|
| **Data drift** (covariate shift) | Input feature distributions | Statistical tests on feature distributions | User behavior change, market shifts, seasonality |
| **Concept drift** | Relationship between X and y | Monitor prediction error rate, output distributions | World changes — what was true no longer is |
| **Label drift** | Target variable distribution | Track target distribution over time | Business process change, definition change |
| **Upstream data drift** | Schema, format, data quality | Schema validation, null rate tracking, type checks | Pipeline changes, vendor API updates, ETL bugs |

## Detection Methods for Numeric Features

| Method | Detects | Sensitivity | Interpretability | Computational Cost |
|---|---|---|---|---|
| **PSI** (Population Stability Index) | Distribution shift magnitude | Medium | High — single score with known thresholds | Low |
| **KS test** (Kolmogorov-Smirnov) | Any distributional difference | High for location/shape shifts | Medium — p-value + D-statistic | Low |
| **Wasserstein distance** | Distribution shift with magnitude awareness | High | High — metric in original units | Medium |
| **Jensen-Shannon divergence** | Symmetric distributional difference | Medium-High | Medium — bounded [0, 1] | Medium |
| **Page-Hinkley test** | Mean shift in streaming data | High for gradual drift | Medium | Very Low (online) |

## Quick Reference

| PSI Value | Interpretation | Action |
|---|---|---|
| < 0.1 | No significant drift | Continue monitoring |
| 0.1 - 0.2 | Moderate drift | Investigate, increase monitoring frequency |
| > 0.2 | Significant drift | Investigate immediately, consider retraining |
| > 0.5 | Severe drift | Likely model failure, trigger retraining pipeline |

## Retraining Triggers

| Trigger Type | Mechanism | Best When | Risk |
|---|---|---|---|
| **Performance-based** | Metric drops below threshold | Labels are available quickly | Delayed labels mean late detection |
| **Drift-based** | Statistical test exceeds threshold | Labels are delayed or unavailable | May retrain unnecessarily if drift is benign |
| **Scheduled** | Calendar cadence (weekly, monthly) | Drift is gradual and predictable | Wastes resources if no drift; misses sudden drift |
| **Hybrid** | Drift triggers evaluation; performance confirms | You want efficiency + safety | More complex to implement |

## Implementation Libraries

| Task | Python | R |
|------|--------|---|
| Comprehensive drift monitoring (reports, dashboards) | `evidently` | — |
| Performance estimation without ground truth | `nannyml` | — |
| Drift detection algorithms (KS, MMD, tabular, text, image) | `alibi-detect` | — |
| Data logging and profiling for monitoring | `whylogs` | — |
| Streaming drift detection (ADWIN, DDM, EDDM, Page-Hinkley) | `river` | — |
| Statistical tests (KS, chi-square, Wasserstein) | `scipy.stats` | `stats` |
| **Commercial platforms** | Fiddler, Arize, Arthur, Superwise | — |
