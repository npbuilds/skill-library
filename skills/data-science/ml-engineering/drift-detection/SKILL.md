---
name: drift-detection
description: >
  Model and data drift detection for production ML systems. Reference when designing monitoring
  pipelines, selecting drift detection methods, setting alert thresholds, diagnosing performance
  degradation, or deciding when to retrain models. Use when ML models are deployed and need
  ongoing quality assurance.
---

# Drift Detection — The Watchdog

A model that performs well at deployment will degrade over time. The world changes — customer behavior shifts, upstream data pipelines break, seasonal patterns rotate, new categories appear. Drift detection is the practice of catching these changes before they reach users as bad predictions. Without it, you discover model failure from angry stakeholders, not from your monitoring system.

The core principle: compare what the model sees (or produces) now against what it saw during training or a known-good reference period. When the difference exceeds a threshold, investigate and act.

## Types of Drift

| Drift Type | What Changes | Detection Approach | Typical Cause |
|---|---|---|---|
| **Data drift** (covariate shift) | Input feature distributions | Statistical tests on feature distributions | User behavior change, market shifts, seasonality |
| **Concept drift** | Relationship between X and y | Monitor prediction error rate, output distributions | World changes — what was true no longer is |
| **Label drift** | Target variable distribution | Track target distribution over time | Business process change, definition change |
| **Upstream data drift** | Schema, format, data quality | Schema validation, null rate tracking, type checks | Pipeline changes, vendor API updates, ETL bugs |

Data drift is the most commonly monitored because it requires no ground truth labels. Concept drift is the most dangerous because the model can receive familiar-looking inputs and still produce wrong outputs. Upstream data drift is the most preventable through good data contracts and validation.

## Detection Methods for Numeric Features

| Method | Detects | Sensitivity | Interpretability | Computational Cost |
|---|---|---|---|---|
| **PSI** (Population Stability Index) | Distribution shift magnitude | Medium | High — single score with known thresholds | Low |
| **KS test** (Kolmogorov-Smirnov) | Any distributional difference | High for location/shape shifts | Medium — p-value + D-statistic | Low |
| **Wasserstein distance** | Distribution shift with magnitude awareness | High | High — metric in original units | Medium |
| **Jensen-Shannon divergence** | Symmetric distributional difference | Medium-High | Medium — bounded [0, 1] | Medium |
| **Page-Hinkley test** | Mean shift in streaming data | High for gradual drift | Medium | Very Low (online) |

**PSI** bins the reference and detection distributions, then measures divergence. Simple, fast, widely understood. Weak point: binning choices affect results, and it misses shape changes within bins.

**KS test** compares empirical CDFs. No binning required. Provides a p-value for statistical rigor. Weak point: less sensitive to tail differences, p-value depends on sample size.

**Wasserstein distance** (Earth Mover's Distance) quantifies how much "work" it takes to transform one distribution into another. Advantage: the magnitude is in the feature's original units, making it interpretable. Preferred when you need to know not just whether drift occurred but how large it is.

**Jensen-Shannon divergence** is a symmetric, bounded version of KL divergence. Useful when you want a normalized similarity score. Works well for comparing probability distributions directly.

**Page-Hinkley** is designed for streaming scenarios. It maintains a running statistic and fires when cumulative deviation from the mean exceeds a threshold. Low memory, no windowing required.

See `references/detection-methods.md` for formulas, implementation details, and threshold conventions for each method.

## Detection Methods for Categorical Features

**Chi-square test** — compares observed vs expected category frequencies. Standard statistical test with well-understood properties. Sensitive to sample size; large samples detect trivially small differences.

**PSI for categoricals** — treats each category as a bin. Same formula as numeric PSI. Works well when category sets are stable. Breaks down when new categories appear.

**Top-k frequency comparison** — track the ranking and relative frequency of the most common categories. Detects when previously rare categories become dominant or vice versa. Simple and robust.

**Cardinality monitoring** — track the number of distinct values. A sudden increase suggests new categories appearing (possibly from upstream bugs or schema changes). A decrease may indicate data filtering issues.

**New category detection** — flag any category value not present in the reference set. Critical for models using one-hot encoding or embedding lookups, where unseen categories cause errors or silent mishandling.

## Output/Prediction Drift

Monitoring model outputs catches concept drift faster than monitoring inputs. If the input distribution is stable but prediction distributions shift, the model's learned relationship is breaking down.

**Score distribution monitoring** — track the distribution of predicted probabilities (for classifiers) or predicted values (for regressors). Shifts indicate the model is responding differently to incoming data.

**Confidence calibration drift** — compare predicted probabilities against observed outcomes. When a model predicts 80% confidence but actual positive rate drops to 50%, calibration has drifted.

**Abstain rate changes** — if you have a confidence threshold below which the model abstains, track the abstain rate. Rising abstain rates indicate the model encounters increasingly unfamiliar inputs.

**Prediction distribution shift** — for classifiers, track the proportion of each predicted class. A model that suddenly predicts 90% class A when the historical rate was 60% is likely failing.

Output monitoring is especially valuable when ground truth labels are delayed (fraud detection, medical diagnosis, loan default) because you do not need labels to detect prediction drift.

## Monitoring Architecture

```
Reference Window          Detection Window
[---- Training Data ----] [-- Recent Production Data --]
        or
[-- Last Known Good -----] [-- Current Batch/Stream ---]
                                    |
                          +---------v----------+
                          | Statistical Tests  |
                          | (per feature +     |
                          |  per output)       |
                          +---------+----------+
                                    |
                          +---------v----------+
                          | Threshold Engine   |
                          | (adaptive or fixed)|
                          +---------+----------+
                                    |
                     +--------------+--------------+
                     |              |              |
                  [Info]       [Warning]       [Critical]
                  Log only    Notify team    Page on-call
```

**Reference window** — the baseline distribution. Options: training data, a validated production period, or a rolling window. Training data is simplest but becomes stale. Rolling windows adapt but can mask gradual drift.

**Detection window** — recent production data to compare against the reference. Larger windows increase statistical power but add latency in detecting drift. Smaller windows detect faster but produce noisier signals.

**Window sizing trade-offs:**
- Small windows (hours/hundreds of samples): fast detection, high false positive rate, suits rapid drift
- Medium windows (days/thousands of samples): balanced detection speed and reliability
- Large windows (weeks/tens of thousands): high confidence, slow detection, suits gradual drift

**Batch vs streaming:** Batch detection runs on a schedule (hourly, daily). Simpler to implement, easier to debug. Streaming detection (Page-Hinkley, ADWIN, CUSUM) updates continuously. Use streaming when latency matters — fraud detection, real-time bidding, safety-critical systems.

**Feature-level vs dataset-level:** Monitor each feature independently for specific diagnosis. Use multivariate methods (Maximum Mean Discrepancy, domain classifier) when feature interactions matter. Start with feature-level; add dataset-level if you have correlated feature drift that individual tests miss.

**Alert fatigue management:** With hundreds of features, some will always trigger by chance. Use Bonferroni correction or false discovery rate control. Aggregate feature-level alerts into a single dashboard score. Require multiple features to trigger simultaneously before escalating.

## Threshold Setting & Alerting

**PSI threshold conventions** (widely adopted):

| PSI Value | Interpretation | Action |
|---|---|---|
| < 0.1 | No significant drift | Continue monitoring |
| 0.1 - 0.2 | Moderate drift | Investigate, increase monitoring frequency |
| > 0.2 | Significant drift | Investigate immediately, consider retraining |
| > 0.5 | Severe drift | Likely model failure, trigger retraining pipeline |

**Adaptive thresholds** — set thresholds based on historical drift measurements rather than fixed values. Compute the mean and standard deviation of drift scores over a stable period. Alert when the current score exceeds mean + N standard deviations. This accounts for natural variability in each feature.

**Alert severity tiers:**
1. **Info** — drift detected but within historical norms. Log for trend analysis.
2. **Warning** — drift exceeds adaptive threshold. Notify data science team via Slack/email.
3. **Critical** — drift exceeds hard threshold OR prediction performance has degraded. Page on-call, block automated redeployment.

**Reducing false positives:** require drift to persist across multiple consecutive detection windows before alerting. A single spike is noise; sustained drift is signal. Combine statistical drift detection with downstream performance monitoring — alert only when drift correlates with metric degradation.

## Retraining Triggers

| Trigger Type | Mechanism | Best When | Risk |
|---|---|---|---|
| **Performance-based** | Metric drops below threshold | Labels are available quickly | Delayed labels mean late detection |
| **Drift-based** | Statistical test exceeds threshold | Labels are delayed or unavailable | May retrain unnecessarily if drift is benign |
| **Scheduled** | Calendar cadence (weekly, monthly) | Drift is gradual and predictable | Wastes resources if no drift; misses sudden drift |
| **Hybrid** | Drift triggers evaluation; performance confirms | You want efficiency + safety | More complex to implement |

**Decision framework:**
- If you get labels within hours: use performance-based triggers primarily. Drift monitoring serves as an early warning.
- If labels are delayed by days or weeks: use drift-based triggers to catch problems early. Validate with performance once labels arrive.
- If labels are delayed by months: drift-based is your only real-time signal. Combine with periodic manual evaluation.
- If retraining is expensive: use hybrid — let drift detection flag candidates, but only retrain when performance degradation is confirmed.

## Root Cause Analysis

When drift is detected, diagnosis follows a structured path:

1. **Feature attribution** — rank features by drift magnitude. Which features drifted most? If a single feature dominates, the cause is often upstream. If many features drift together, the cause is often a population shift.

2. **Temporal correlation** — when did drift start? Plot drift scores over time. A sharp step change suggests a pipeline break or deployment event. A gradual slope suggests organic population shift or seasonality.

3. **Upstream tracing** — check data pipeline logs around the drift start time. Did a new data source come online? Did a transformation change? Did a vendor update their API schema? Cross-reference with deployment logs and data contract violations.

4. **Seasonal vs genuine drift** — compare against the same period from previous years. If the pattern repeats annually, it is seasonal and may not require retraining — a calendar-aware model or separate seasonal models may be the right fix.

5. **Segment analysis** — break drift down by user segment, geography, or product line. Drift may be concentrated in a new market or customer cohort rather than affecting the entire population.

## Common Mistakes

1. **Monitoring only inputs, ignoring outputs.** Input distributions can look stable while the model's predictions go haywire. Always monitor prediction distributions alongside feature distributions.

2. **Using training data as the permanent reference window.** Training data becomes stale. If your model has been retrained, update the reference window to match the current training set or a recent validated period.

3. **Setting fixed thresholds without calibration.** PSI > 0.2 is a convention, not a law. Calibrate thresholds to your specific features and their natural variability. A volatile feature with PSI 0.15 may be normal; a stable feature with PSI 0.12 may be alarming.

4. **Alerting on every feature independently.** With 200 features and a 5% significance level, you expect 10 false alarms per test cycle. Use multiple-testing correction and require corroborated evidence before escalating.

5. **Ignoring the feedback loop.** If your model's predictions influence the data it receives (recommendations, pricing, fraud blocking), drift may be self-induced. Distinguish exogenous drift (world changed) from endogenous drift (model changed the world).

6. **Treating all drift as bad.** Some drift is benign — the distribution shifted but the model still performs well. Always pair drift detection with performance monitoring to avoid unnecessary retraining.

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

**Note:** `scikit-multiflow` was historically used for streaming drift detection but is now **deprecated and unmaintained**. Use `river` instead — it is the actively maintained successor with the same algorithms (ADWIN, DDM, EDDM, Page-Hinkley) plus modern streaming ML capabilities.

**Recommended starting stack (Python):** `evidently` for dashboard-style drift reports + `scipy.stats` for custom statistical tests + `river` for streaming detection. Add `whylogs` for data profiling at scale.

## When This Applies

- Any ML model serving predictions in production
- Batch scoring pipelines running on recurring schedules
- Real-time inference endpoints receiving live traffic
- Models where ground truth labels are delayed (fraud, churn, medical outcomes)
- Systems with upstream data dependencies that may change without notice
- Regulated environments requiring model performance documentation
- Models that have not been retrained in more than one quarter — start monitoring immediately
