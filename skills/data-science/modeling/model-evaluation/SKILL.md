---
name: model-evaluation
description: >
  Model evaluation and selection frameworks for machine learning. Reference when choosing
  performance metrics, designing validation strategies, comparing models statistically,
  assessing calibration, or auditing models for fairness. Use when deciding which model
  to deploy or how to measure model quality.
---

# Model Evaluation — The Judge

A model that scores well on the wrong metric, validated with a leaky pipeline, and deployed without statistical rigor is worse than no model at all — it ships confident wrong answers. This skill covers the full evaluation lifecycle: picking the right metrics, validating honestly, comparing models with statistical discipline, checking calibration, and auditing for fairness before anything reaches production.

---

## 1. Metric Selection by Task

No single metric captures model quality. The right choice depends on task type, class balance, and what errors cost the business.

| Task | Metric | When to Prefer |
|---|---|---|
| **Classification** | Accuracy | Balanced classes, equal error costs |
| | Precision | False positives are expensive (spam filters, fraud alerts) |
| | Recall (Sensitivity) | False negatives are dangerous (disease screening, security threats) |
| | F1 Score | Need a single number balancing precision and recall |
| | AUC-ROC | Threshold-independent ranking ability, reasonably balanced data |
| | AUC-PR | Imbalanced data — far more informative than AUC-ROC when positives are rare |
| | Log Loss | Probability quality matters, not just ranking |
| | MCC | Imbalanced data where you want a single balanced measure (-1 to +1) |
| | Cohen's Kappa | Agreement beyond chance; useful when comparing to human labelers |
| **Regression** | MSE / RMSE | Large errors are disproportionately bad; RMSE for same-unit interpretability |
| | MAE | Robust to outliers; median-focused performance |
| | MAPE | Stakeholders want percentage-based error; fails when actuals near zero |
| | R² | Explaining variance proportion; familiar to business audiences |
| | Adjusted R² | Comparing models with different feature counts |
| | Median Absolute Error | Highly robust summary when distribution of errors is skewed |
| **Ranking** | NDCG | Graded relevance; position-weighted quality |
| | MAP | Binary relevance across queries |
| | MRR | Only the first relevant result matters (e.g., question answering) |
| | Precision@k / Recall@k | Fixed-size recommendation lists; top-k retrieval |
| **Clustering** | Silhouette Score | Cluster compactness vs separation when no ground truth exists |
| | Calinski-Harabasz | Fast, favors convex clusters |
| | Davies-Bouldin | Lower is better; penalizes overlapping clusters |
| | Adjusted Rand Index | Ground truth labels available; chance-corrected agreement |

**Key decision rules:**
- Imbalanced classification: default to AUC-PR, MCC, or F1 on the minority class. Never report accuracy alone.
- When probabilities drive decisions (setting thresholds, expected value calculations): use log loss and calibration metrics.
- Regression with outliers: prefer MAE or median absolute error over MSE.
- Ranking with graded relevance: NDCG. Binary relevance: MAP.

See `references/metrics-catalog.md` for formulas, ranges, and detailed trade-off analysis.

---

## 2. Validation Strategies

The validation strategy must match the data structure. Using random k-fold on time-series data or grouped observations produces optimistic, misleading estimates.

| Data Characteristic | Recommended Strategy | Why |
|---|---|---|
| Sufficient data (>50k), no structure | Hold-out (70/15/15 or 80/10/10) | Simple, fast, stable estimates |
| Moderate data (<50k), i.i.d. | 5- or 10-fold CV | Reduces variance of performance estimate |
| Imbalanced classes | Stratified k-fold CV | Preserves class distribution in every fold |
| Temporal ordering | Time-series CV (expanding or sliding window) | Prevents future data leaking into training |
| Grouped observations (patients, users) | Group k-fold | Prevents same group appearing in train and test |
| Hyperparameter tuning + evaluation | Nested CV (inner loop tunes, outer loop evaluates) | Prevents selection bias from tuning on test data |
| Very small data (<500) | Leave-one-out CV or repeated k-fold | Maximizes training data per split |

**Expanding vs sliding window for time series:** Expanding window grows the training set over time (mirrors production where you retrain on all history). Sliding window uses a fixed-size recent window (better when the data distribution drifts and old data hurts).

**Nested CV protocol:**
1. Outer loop: k-fold split producing train/test pairs.
2. Inner loop: for each outer fold, run k-fold CV on the training portion to select hyperparameters.
3. Retrain with selected hyperparameters on the full outer training fold, evaluate on the outer test fold.
4. Report: mean and standard deviation across outer folds.

This gives an unbiased estimate of generalization performance for the tuned model.

---

## 3. Statistical Model Comparison

Reporting "Model A: 0.85, Model B: 0.83" without a significance test is not a comparison — it is anecdote. Performance differences must survive statistical scrutiny.

| Method | When to Use | Notes |
|---|---|---|
| Paired t-test on CV folds | k-fold CV results, roughly normal differences | Fast but assumes independence of folds (violated in practice) |
| Corrected resampled t-test (Nadeau-Bengio) | k-fold CV results | Corrects for non-independence by adjusting variance estimate; preferred over naive paired t-test |
| McNemar's test | Two classifiers on the same test set | Tests whether disagreement patterns are symmetric; does not need CV |
| Wilcoxon signed-rank test | Non-normal differences, small sample of datasets | Non-parametric; robust when normality assumption fails |
| Bayesian comparison | Want probability statements, not p-values | Produces P(A > B), P(rope), P(B > A); more informative than frequentist tests |

**Practical protocol:**
1. Run both models under identical CV splits (same random seed, same folds).
2. Record per-fold performance differences.
3. Apply the Nadeau-Bengio corrected t-test (or Wilcoxon if differences are non-normal).
4. For multiple model comparison across multiple datasets, use the Friedman test followed by Nemenyi post-hoc.
5. Report effect size alongside p-values — a statistically significant but tiny improvement may not justify deployment complexity.

---

## 4. Calibration

A model that outputs 0.7 probability for an event should be right about 70% of the time. Many models (gradient-boosted trees, SVMs, neural networks) produce scores that rank well but are not calibrated probabilities.

**Why calibration matters:** Any decision that uses predicted probabilities directly — expected cost calculations, threshold selection, risk stratification, uncertainty-aware downstream systems — requires calibration. A well-discriminating but poorly calibrated model will set thresholds incorrectly and misestimate expected outcomes.

**Diagnostic tools:**
- **Reliability diagram:** Bin predictions by predicted probability, plot mean predicted vs mean observed. A perfectly calibrated model follows the diagonal.
- **Expected Calibration Error (ECE):** Weighted average of per-bin |predicted - observed|. Lower is better. Typical target: ECE < 0.05.

**Calibration methods:**
- **Platt scaling:** Fit a logistic regression on the model's raw outputs using a held-out calibration set. Works well for sigmoid-shaped distortions. Two parameters.
- **Isotonic regression:** Non-parametric monotonic fit. More flexible than Platt scaling but needs more calibration data (risk of overfitting with <1,000 samples).
- **Temperature scaling:** Single parameter (temperature T) dividing logits before softmax. Popular for neural networks, especially in multi-class settings.

**Protocol:** Always calibrate on a held-out set, never on training data. After calibrating, re-check the reliability diagram and ECE to confirm improvement.

---

## 5. Fairness Auditing

Model quality means nothing if the model systematically harms protected groups. Fairness auditing is not optional — it is a deployment requirement.

**Core fairness criteria:**

| Criterion | Definition | Intuition |
|---|---|---|
| Demographic Parity | P(positive prediction) is equal across groups | Selection rates are the same regardless of group membership |
| Equalized Odds | TPR and FPR are equal across groups | The model makes errors at the same rate for all groups |
| Equal Opportunity | TPR is equal across groups | Among true positives, all groups have equal chance of being correctly identified |
| Predictive Parity | Precision is equal across groups | A positive prediction means the same thing regardless of group |

**The impossibility theorem:** Except in trivial cases (equal base rates across groups or perfect prediction), you cannot simultaneously satisfy demographic parity, equalized odds, and predictive parity. You must choose which criterion aligns with your application's values and legal context.

**Practical audit workflow:**
1. Identify protected attributes (even if not used as features — proxy variables can encode them).
2. Compute all four criteria above, disaggregated by group.
3. Choose the criterion most appropriate to the domain (e.g., equal opportunity for lending, demographic parity for hiring screens).
4. Quantify disparity: ratios (e.g., adverse impact ratio > 0.8 under the 4/5 rule) or absolute differences.
5. If disparities exceed thresholds, intervene: re-sample training data, apply in-processing constraints, or post-process predictions.
6. Document decisions and trade-offs. Fairness is a policy choice, not a purely technical one.

---

## 6. Beyond Single Metrics

Single-number metrics compress too much information. Supplement them with deeper analysis.

- **Confusion matrix deep dives:** Go beyond aggregate rates. Segment by subpopulation, feature range, or data source. A model with 95% overall accuracy can have 40% accuracy on a critical subgroup.
- **Error analysis — systematic vs random:** Cluster misclassifications. If errors concentrate on specific patterns (short texts, low-resolution images, a demographic), the model has a systematic blind spot that more data or architectural changes can fix. Random errors suggest you are near the irreducible error floor.
- **Learning curves:** Plot training and validation performance vs training set size. Diverging curves (high training, low validation) signal high variance — get more data or regularize. Converging low curves signal high bias — increase model capacity.
- **Prediction interval coverage:** For regression, check that your 90% prediction intervals actually contain 90% of observations. Under-coverage means your uncertainty estimates are overconfident.

---

## Common Mistakes

1. **Reporting accuracy on imbalanced data.** A 95/5 class split gives 95% accuracy by predicting the majority class every time. Use AUC-PR, F1, or MCC instead.

2. **Data leakage in cross-validation.** Fitting a scaler, selecting features, or oversampling (SMOTE) on the full dataset before splitting. All preprocessing that uses statistics from data must happen inside each fold.

3. **Optimizing a proxy metric that diverges from business value.** Improving log loss by 0.01 means nothing if the business cares about precision at a specific operating threshold. Map ML metrics to business KPIs explicitly.

4. **Comparing models without statistical tests.** A 2-point difference on one random split is noise. Use corrected resampled t-tests or Bayesian comparison on multiple folds.

5. **Ignoring calibration before deploying probability-based decisions.** Ranking ability (AUC) does not guarantee calibrated probabilities. Platt scaling or isotonic regression is cheap insurance.

6. **Treating fairness as a post-hoc checkbox.** Auditing for fairness after the model is built limits your options. Build fairness considerations into the problem formulation, data collection, and metric selection from the start.

---

## Implementation Libraries

| Task | Python | R |
|------|--------|---|
| Classification/regression/clustering metrics | `sklearn.metrics` | `yardstick` (tidymodels) |
| Visual model diagnostics (learning curves, residuals) | `yellowbrick` | `performance` (easystats) |
| Cross-validation, train/test splitting | `sklearn.model_selection` | `rsample` (tidymodels) |
| Hyperparameter tuning | `optuna`, `hyperopt` | `tune` (tidymodels) |
| Calibration (Platt, isotonic) | `sklearn.calibration` | `probably` |
| Fairness evaluation | `fairlearn` | `fairness` |
| Statistical model comparison | `baycomp`, `scipy.stats` | `tidyposterior` |
| Imbalanced data handling (SMOTE, etc.) | `imbalanced-learn` | `themis` (tidymodels) |

**Recommended starting stack (Python):** `sklearn.metrics` + `sklearn.model_selection` for core evaluation, `optuna` for tuning, `yellowbrick` for visual diagnostics, `fairlearn` for fairness audits.

## When This Applies

Reference this skill when you are:
- Choosing which metric(s) to report for a modeling project
- Designing a cross-validation strategy for a new dataset
- Deciding between two or more candidate models
- Preparing a model for deployment and need calibrated probabilities
- Conducting a fairness or bias review before launch
- Performing error analysis to diagnose why a model underperforms
- Writing a model card or evaluation report for stakeholders

For detailed metric formulas, ranges, and trade-off analysis, see `references/metrics-catalog.md`.
