# Drift Detection Methods — Complete Reference

## Method Catalog

### PSI (Population Stability Index)

**Procedure:** Bin the reference distribution into B buckets (typically 10-20). Compute the proportion of observations in each bucket for both reference (R) and detection (D) distributions. For each bucket i, compute (D_i - R_i) * ln(D_i / R_i). Sum across all buckets.

**Null hypothesis:** None — PSI is a descriptive metric, not a formal statistical test. There is no p-value.

**Threshold conventions:**
| PSI | Interpretation |
|---|---|
| < 0.1 | No significant shift |
| 0.1 - 0.2 | Moderate shift — investigate |
| 0.2 - 0.5 | Significant shift — action required |
| > 0.5 | Severe shift — likely model failure |

**Pros:**
- Simple to compute and explain to stakeholders
- Single scalar summary of distributional change
- Works for both numeric (binned) and categorical features
- Widely adopted in financial services and credit risk

**Cons:**
- Sensitive to binning strategy (number and placement of bins)
- Not a formal test — no statistical significance
- Can miss shape changes within bins
- Undefined when a bin has zero observations in either distribution (requires smoothing)

**Best for:** Routine monitoring dashboards, regulatory reporting, quick triage of feature health.

**Computational complexity:** O(n + B) where n is sample size and B is number of bins.

**Implementations:** `evidently` (Python), `nannyml` (Python), `alibi-detect` (Python), custom implementation is trivial.

---

### KS Test (Kolmogorov-Smirnov)

**Procedure:** Compute the empirical CDF of both the reference and detection samples. The KS statistic D is the maximum absolute difference between the two CDFs: D = max|F_ref(x) - F_det(x)| over all x. The p-value is derived from the KS distribution.

**Null hypothesis:** The reference and detection samples are drawn from the same continuous distribution.

**Threshold conventions:**
- p-value < 0.05: statistically significant drift at 95% confidence
- D-statistic > 0.1: moderate practical significance (context-dependent)
- For large samples, use the D-statistic rather than the p-value (p-values become trivially small)

**Pros:**
- Non-parametric — makes no assumptions about distribution shape
- No binning required
- Well-understood statistical properties
- Available in every scientific computing library

**Cons:**
- Most sensitive to differences near the center of the distribution, less sensitive in tails
- p-value is heavily influenced by sample size — large samples detect trivial differences
- Only defined for continuous distributions (use chi-square for categoricals)
- Two-sample test only; does not quantify drift magnitude in interpretable units

**Best for:** General-purpose drift detection on numeric features, especially when you want a formal statistical test with a p-value.

**Computational complexity:** O(n log n) for sorting, O(n) for the statistic.

**Implementations:** `scipy.stats.ks_2samp` (Python), `evidently`, `alibi-detect`, R `stats::ks.test`.

---

### Wasserstein Distance (Earth Mover's Distance)

**Procedure:** For one-dimensional distributions, sort both samples. The Wasserstein-1 distance is the area between the two empirical CDFs, which equals the mean absolute difference between the sorted values of equal-sized samples. For unequal samples, interpolate or use the integral of |F_ref(x) - F_det(x)| dx.

**Null hypothesis:** None in the standard formulation — Wasserstein distance is a metric, not a test. Permutation tests can provide p-values if needed.

**Threshold conventions:** No universal thresholds. The distance is in the same units as the feature, so thresholds must be set per-feature based on the feature's scale and historical variability. A distance of 5 on a feature ranging [0, 1000] is minor; the same on a feature ranging [0, 10] is large.

**Pros:**
- Magnitude is in the feature's original units — highly interpretable
- Sensitive to both location and shape changes
- No binning required
- Mathematically well-behaved (true metric satisfying triangle inequality)

**Cons:**
- No built-in significance test (need permutation testing for p-values)
- Thresholds must be calibrated per feature
- Higher computational cost than KS or PSI for large samples
- Multivariate extension (Wasserstein for high dimensions) is expensive

**Best for:** When you need to quantify how much drift occurred in human-understandable units. Feature importance ranking for drift diagnosis.

**Computational complexity:** O(n log n) for 1D (sorting-based), O(n^3) for general multi-dimensional via linear programming.

**Implementations:** `scipy.stats.wasserstein_distance` (Python), `evidently`, `nannyml`.

---

### Jensen-Shannon Divergence (JSD)

**Procedure:** Estimate probability distributions P (reference) and Q (detection) using histograms or KDE. Compute the midpoint distribution M = (P + Q) / 2. JSD = 0.5 * KL(P || M) + 0.5 * KL(Q || M), where KL is the Kullback-Leibler divergence. The KL divergence is the sum of P_i * ln(P_i / M_i) across all bins.

**Null hypothesis:** None in standard form. Permutation tests can provide significance.

**Threshold conventions:**
| JSD | Interpretation |
|---|---|
| < 0.05 | Minimal divergence |
| 0.05 - 0.1 | Moderate divergence |
| 0.1 - 0.2 | Significant divergence |
| > 0.2 | Severe divergence |

Note: JSD is bounded in [0, 1] when using base-2 logarithm, [0, ln(2)] with natural log.

**Pros:**
- Symmetric (unlike KL divergence)
- Bounded — easy to normalize and compare across features
- Always defined (no division-by-zero issues, unlike raw KL divergence)
- Square root of JSD is a true metric

**Cons:**
- Requires density estimation (binning or KDE), which introduces its own parameters
- Less interpretable than Wasserstein (units are nats or bits, not feature units)
- Sensitive to density estimation quality in sparse regions

**Best for:** Comparing distributions when you want a bounded, symmetric divergence score. Useful for dashboard displays and cross-feature comparison.

**Computational complexity:** O(n + B) where B is the number of bins or KDE evaluation points.

**Implementations:** `scipy.spatial.distance.jensenshannon` (Python), `alibi-detect`, `evidently`.

---

### Anderson-Darling Test

**Procedure:** Compare two empirical CDFs with extra weight on the tails. The statistic is a weighted integral of the squared difference between CDFs, where the weight function increases in the tails: A^2 = -n - (1/n) * sum[(2i - 1) * (ln(F(x_i)) + ln(1 - F(x_{n+1-i})))]. For the two-sample version, the combined sorted sample is used.

**Null hypothesis:** Both samples are drawn from the same distribution.

**Threshold conventions:** Critical values depend on sample sizes. Use tabulated values or the `scipy` implementation which provides the significance level directly.

**Pros:**
- More sensitive to tail differences than KS test
- Useful for detecting drift in extreme values (important for risk models)
- Non-parametric

**Cons:**
- More complex to compute than KS
- Less widely known — harder to explain to stakeholders
- Two-sample version has limited tabulated critical values

**Best for:** Financial risk models, insurance, fraud detection — any domain where tail behavior matters.

**Computational complexity:** O(n log n).

**Implementations:** `scipy.stats.anderson_ksamp` (Python).

---

### Cramer-von Mises Test

**Procedure:** Compute the integrated squared difference between the two empirical CDFs: W^2 = integral of (F_ref(x) - F_det(x))^2 dF_combined(x). In practice, this is a sum over the combined sorted sample.

**Null hypothesis:** Both samples come from the same distribution.

**Threshold conventions:** Use p-values from the test. Significance at p < 0.05 is standard.

**Pros:**
- Considers the entire distribution (not just the maximum difference like KS)
- More powerful than KS for many alternatives
- Non-parametric

**Cons:**
- Less sensitive to tail differences than Anderson-Darling
- Less well-known than KS
- Slightly higher computational cost than KS

**Best for:** When KS test is too focused on a single point of maximum divergence and you want a test that considers the entire distribution.

**Computational complexity:** O(n log n).

**Implementations:** `scipy.stats.cramervonmises_2samp` (Python).

---

### Chi-Square Test

**Procedure:** For each category, compute expected frequency E_i (from reference proportions scaled to detection sample size) and observed frequency O_i (from detection data). The statistic is the sum of (O_i - E_i)^2 / E_i across all categories. Compare against the chi-square distribution with (k-1) degrees of freedom.

**Null hypothesis:** The detection sample follows the same categorical distribution as the reference.

**Threshold conventions:** p-value < 0.05 for statistical significance. Effect size (Cramer's V) provides practical significance: V < 0.1 small, 0.1-0.3 medium, > 0.3 large.

**Pros:**
- Standard test for categorical data
- Well-understood, widely implemented
- Provides both statistical significance and effect size

**Cons:**
- Requires sufficient expected counts per category (>5 is the common rule of thumb)
- Sensitive to sample size — large samples find trivial differences significant
- Does not handle new categories (categories with zero reference count)

**Best for:** Categorical feature drift detection when category sets are stable.

**Computational complexity:** O(n + k) where k is the number of categories.

**Implementations:** `scipy.stats.chisquare` (Python), `evidently`.

---

### Page-Hinkley Test

**Procedure:** Maintain a running sum of deviations from the overall mean. At each new observation x_t, update: m_T = m_{T-1} + (x_t - x_bar - delta), where delta is a tolerance parameter. Track the minimum m_min seen so far. Alarm when m_T - m_min > lambda (the threshold parameter).

**Null hypothesis:** The mean of the sequence has not changed.

**Threshold conventions:**
- delta (tolerance): typically 0.005 to 0.05 of the feature's standard deviation. Higher delta reduces sensitivity.
- lambda (detection threshold): set based on acceptable false alarm rate. Typical values: 20-100. Higher lambda reduces false alarms but increases detection delay.

**Pros:**
- True streaming algorithm — processes one observation at a time
- Very low memory (constant space)
- Detects gradual drift (mean shift) effectively
- Fast computation

**Cons:**
- Only detects changes in the mean — misses variance changes or shape changes
- Requires tuning delta and lambda parameters
- Not suitable for multivariate drift
- Assumes observations are somewhat stationary before the change point

**Best for:** Real-time streaming monitoring, low-latency drift detection for individual features.

**Computational complexity:** O(1) per observation (online algorithm).

**Implementations:** `river` (Python, `river.drift.PageHinkley`), `scikit-multiflow` (deprecated — use `river`).

---

### CUSUM (Cumulative Sum Control Chart)

**Procedure:** Maintain two cumulative sums tracking upward and downward shifts. For each observation x_t: S_high = max(0, S_high + x_t - mu_0 - k) and S_low = max(0, S_low - x_t + mu_0 - k), where mu_0 is the target mean and k is the allowance (typically 0.5 * expected_shift). Alarm when either S_high or S_low exceeds threshold h.

**Null hypothesis:** The process mean equals the target value mu_0.

**Threshold conventions:**
- k (allowance): 0.5 * expected shift magnitude for optimal detection of that shift size
- h (decision interval): set based on desired Average Run Length (ARL). h = 4-5 for quick detection, h = 8-10 for fewer false alarms.

**Pros:**
- Detects both upward and downward mean shifts
- Well-established theory from statistical process control
- Can be tuned for specific shift sizes
- Low memory, streaming-compatible

**Cons:**
- Designed for normally distributed data (though robust to violations)
- Requires specifying expected shift size (k parameter)
- Only detects mean shifts
- Needs resetting after an alarm

**Best for:** Industrial process monitoring, quality control-style model monitoring, detecting specific magnitude of mean shift.

**Computational complexity:** O(1) per observation.

**Implementations:** `river` (Python), custom implementation is straightforward, `detecta` (Python).

---

### ADWIN (Adaptive Windowing)

**Procedure:** Maintain a variable-length window of recent observations. At each step, test whether any split of the current window into two sub-windows shows a statistically significant difference in means (using Hoeffding's bound). If a significant cut is found, drop all data before the cut point, effectively shrinking the window to contain only post-drift data.

**Null hypothesis:** The mean is constant across the entire window.

**Threshold conventions:**
- delta (confidence parameter): probability of false detection. Typical values: 0.002 to 0.05. Lower delta means fewer false alarms but slower detection.

**Pros:**
- Automatically adapts window size — no manual window tuning
- Rigorous theoretical guarantees (bounded false positive and false negative rates)
- Handles both gradual and abrupt drift
- Memory-efficient (uses exponential histogram compression)

**Cons:**
- Only monitors the mean of a single variable
- More complex to implement than CUSUM or Page-Hinkley
- Can be slow to detect very gradual drift
- Compressed representation loses some statistical power

**Best for:** Streaming environments where you do not know the drift speed in advance. Adaptive monitoring without manual window configuration.

**Computational complexity:** O(log W) per observation, where W is the current window size. Memory: O(log W).

**Implementations:** `river` (Python, `river.drift.ADWIN`), `scikit-multiflow` (deprecated — use `river`), `MOA` (Java).

---

### DDM (Drift Detection Method)

**Procedure:** Monitor the error rate of the model on a stream of predictions. Track the running mean p_t and standard deviation s_t = sqrt(p_t * (1 - p_t) / t). Define warning level when p_t + s_t >= p_min + 2 * s_min and drift level when p_t + s_t >= p_min + 3 * s_min, where p_min and s_min are the minimum values of p + s observed so far.

**Null hypothesis:** The model error rate has not increased.

**Threshold conventions:**
- Warning level: 2 standard deviations above minimum (configurable)
- Drift level: 3 standard deviations above minimum (configurable)
- Minimum sample size before detection: typically 30 observations

**Pros:**
- Directly monitors what matters — model error rate
- Simple to implement and understand
- Low computational cost
- Integrates naturally with online learning

**Cons:**
- Requires ground truth labels (not suitable when labels are delayed)
- Designed for binary classification error — less natural for regression
- Slow to detect gradual drift
- Can produce false alarms during early observations (small sample)

**Best for:** Online learning systems where labels are available immediately. Binary classification monitoring.

**Computational complexity:** O(1) per observation.

**Implementations:** `river` (Python, `river.drift.DDM`), `scikit-multiflow` (deprecated — use `river`).

---

### EDDM (Early Drift Detection Method)

**Procedure:** Similar to DDM but monitors the distance between classification errors rather than the error rate itself. Track the running mean d_t and standard deviation s_d of distances between consecutive errors. Warning when (d_t + 2*s_d) / (d_max + 2*s_d_max) < alpha (typically 0.95). Drift when the ratio drops below beta (typically 0.9).

**Null hypothesis:** The spacing between errors has not decreased (error rate has not increased).

**Threshold conventions:**
- alpha (warning threshold): 0.95 (ratio of current to maximum distance metric)
- beta (drift threshold): 0.90
- Minimum number of errors before detection: typically 30

**Pros:**
- More sensitive to gradual drift than DDM
- Detects drift earlier than DDM in many scenarios
- Same low computational cost as DDM

**Cons:**
- Requires ground truth labels
- Can be less stable than DDM on noisy streams
- Only applicable to classification tasks
- Higher false alarm rate than DDM on stationary streams

**Best for:** Scenarios where early detection of gradual drift is more important than low false alarm rates. Use alongside DDM for complementary coverage.

**Computational complexity:** O(1) per observation.

**Implementations:** `river` (Python, `river.drift.EDDM`), `scikit-multiflow` (deprecated — use `river`).

---

## Window Sizing Guide

### Factors Affecting Window Size

| Factor | Smaller Windows | Larger Windows |
|---|---|---|
| **Data volume** | Low-volume streams need larger windows for statistical power | High-volume streams can use smaller windows |
| **Drift speed** | Sudden drift detected faster with smaller windows | Gradual drift needs larger windows to accumulate signal |
| **Acceptable detection latency** | Low latency demands require smaller windows | Tolerance for delay allows larger, more stable windows |
| **Feature variability** | Noisy features need larger windows to avoid false alarms | Stable features can use smaller windows |
| **Number of features** | More features monitored means more chances for false alarms — larger windows help | Few features allow tighter windows |

### Recommended Sizes by Scenario

| Scenario | Reference Window | Detection Window | Rationale |
|---|---|---|---|
| **High-volume API (>10k req/hour)** | 1-7 days of data | 1-4 hours | Enough volume for statistical power in short windows |
| **Daily batch scoring (1k-10k records)** | 30-90 days | 1-7 days | Need multiple days to accumulate sufficient detection sample |
| **Weekly batch (100-1k records)** | 6-12 months | 2-4 weeks | Small volumes require long accumulation periods |
| **Streaming with rapid feedback** | Rolling 30-day baseline | ADWIN (adaptive) | Let the algorithm manage window size |
| **Seasonal business (retail, travel)** | Same period from previous year | Current period (1-4 weeks) | Year-over-year comparison avoids seasonal false alarms |
| **Post-retraining validation** | New training data | First 24-48 hours of production | Verify the retrained model encounters expected data |

### Sliding vs Tumbling Windows

**Sliding window:** overlapping windows that advance by a step size. Produces more frequent drift scores and catches drift earlier. Higher computational cost due to overlapping computation.

**Tumbling window:** non-overlapping, fixed-size windows that reset completely. Simpler to implement, lower computational cost. Can miss drift that straddles two window boundaries.

**Recommendation:** Use sliding windows for critical models where detection latency matters. Use tumbling windows for routine monitoring of large feature sets where simplicity and cost efficiency are priorities.

---

## Production Monitoring Checklist

### Before Deployment

- [ ] Define reference dataset (training data or validated production baseline)
- [ ] Select detection methods per feature type (numeric, categorical, text, embedding)
- [ ] Set initial thresholds based on validation data variability
- [ ] Configure window sizes based on data volume and acceptable latency
- [ ] Set up multiple-testing correction for high-dimensional feature sets
- [ ] Define alert routing: which team, which channel, which severity
- [ ] Establish retraining trigger criteria (drift-based, performance-based, or hybrid)
- [ ] Document the monitoring setup for regulatory or audit requirements

### At Deployment

- [ ] Validate that the monitoring pipeline receives production data correctly
- [ ] Run baseline drift check: compare first production batch against reference to verify near-zero drift scores
- [ ] Confirm alert routing delivers test alerts to the correct recipients
- [ ] Verify that logging captures drift scores, feature statistics, and metadata for debugging

### Ongoing Operations

- [ ] Review drift dashboards weekly (even when no alerts fire)
- [ ] Recalibrate thresholds quarterly based on observed false positive / false negative rates
- [ ] Update reference windows after validated retraining cycles
- [ ] Audit upstream data sources for schema or quality changes monthly
- [ ] Track alert-to-resolution time and optimize escalation workflows
- [ ] Review seasonal patterns and adjust monitoring around known events (holidays, promotions, fiscal quarters)
- [ ] Archive drift scores and investigation records for trend analysis and audits
