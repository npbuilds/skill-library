# Metrics Catalog — Complete Reference

This catalog provides formulas, ranges, trade-offs, and practical guidance for every metric referenced in the model-evaluation skill.

---

## Classification Metrics

| Metric | Formula (text) | Range | Optimum | Sensitive to Imbalance? | Interpretability | Typical Use Case |
|---|---|---|---|---|---|---|
| **Accuracy** | (TP + TN) / (TP + TN + FP + FN) | [0, 1] | 1 | Yes — misleading when classes are skewed | High — "percent correct" | Balanced binary/multiclass problems with equal error costs |
| **Precision** | TP / (TP + FP) | [0, 1] | 1 | Moderate — depends on positive rate | High — "of those I flagged, how many were right?" | Spam detection, fraud alerts, any setting where false positives are expensive |
| **Recall (Sensitivity)** | TP / (TP + FN) | [0, 1] | 1 | Moderate — depends on negative rate | High — "of the true positives, how many did I catch?" | Disease screening, security threats, any setting where misses are dangerous |
| **F1 Score** | 2 * (Precision * Recall) / (Precision + Recall) | [0, 1] | 1 | Moderate | Medium — harmonic mean, less intuitive than precision/recall alone | When you need a single number balancing precision and recall |
| **AUC-ROC** | Area under the ROC curve (TPR vs FPR across thresholds) | [0, 1] | 1 | Yes — can be overly optimistic with imbalanced data because FPR denominator is large | Medium — probability that a random positive ranks above a random negative | Threshold-independent ranking quality on reasonably balanced data |
| **AUC-PR** | Area under the Precision-Recall curve across thresholds | [0, 1] (baseline = positive rate) | 1 | No — directly reflects minority class performance | Medium — focuses on positive class performance | Imbalanced classification (rare events, anomaly detection) |
| **Log Loss** | -mean(y * log(p) + (1-y) * log(1-p)) | [0, +inf) | 0 | Moderate | Low — requires understanding of information theory | When probability quality matters, not just ranking (calibration-sensitive) |
| **MCC** | (TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)) | [-1, +1] | +1 | No — balanced measure using all four confusion matrix cells | Medium — correlation between predicted and actual | Imbalanced data when you want a single robust scalar |
| **Cohen's Kappa** | (observed agreement - expected agreement) / (1 - expected agreement) | [-1, +1] (typically [0, 1]) | +1 | No — chance-corrected | Medium — improvement over random agreement | Inter-rater agreement, comparing model to human labelers |

## Regression Metrics

| Metric | Formula (text) | Range | Optimum | Sensitive to Outliers? | Interpretability | Typical Use Case |
|---|---|---|---|---|---|---|
| **MSE** | mean((y - y_hat)^2) | [0, +inf) | 0 | Yes — squares amplify large errors | Low — units are squared | Optimization objective; penalizes large errors heavily |
| **RMSE** | sqrt(mean((y - y_hat)^2)) | [0, +inf) | 0 | Yes | High — same units as target | Reporting regression error in interpretable units |
| **MAE** | mean(abs(y - y_hat)) | [0, +inf) | 0 | No — linear penalty | High — average absolute deviation | Robust error reporting; when outliers should not dominate |
| **MAPE** | mean(abs((y - y_hat) / y)) * 100 | [0, +inf) | 0 | Moderate | High — percentage error familiar to business | Business forecasting; fails when y values near zero |
| **R-squared** | 1 - SS_res / SS_tot | (-inf, 1] | 1 | Moderate | High — "proportion of variance explained" | Communicating model quality to non-technical stakeholders |
| **Adjusted R-squared** | 1 - (1-R^2)(n-1)/(n-p-1) | (-inf, 1] | 1 | Moderate | High | Comparing models with different numbers of features |
| **Median Absolute Error** | median(abs(y - y_hat)) | [0, +inf) | 0 | No — ignores tails entirely | High — typical error magnitude | Skewed error distributions, heavy-tailed targets |

## Ranking Metrics

| Metric | Formula (text) | Range | Optimum | Interpretability | Typical Use Case |
|---|---|---|---|---|---|
| **NDCG** | DCG / ideal DCG, where DCG = sum(relevance_i / log2(i+1)) | [0, 1] | 1 | Medium — normalized against perfect ranking | Search engines, recommendation with graded relevance |
| **MAP** | Mean of average precision across queries; AP = sum of precision@k at relevant positions / total relevant | [0, 1] | 1 | Medium | Information retrieval with binary relevance |
| **MRR** | mean(1 / rank_of_first_relevant_item) | [0, 1] | 1 | High — "how far down do I find the answer?" | Question answering, navigational search |
| **Precision@k** | Number of relevant items in top-k / k | [0, 1] | 1 | High | Fixed-size recommendation lists |
| **Recall@k** | Number of relevant items in top-k / total relevant items | [0, 1] | 1 | High | Retrieval completeness in top-k results |

## Clustering Metrics

| Metric | Formula (text) | Range | Optimum | Requires Ground Truth? | Typical Use Case |
|---|---|---|---|---|---|
| **Silhouette Score** | mean((b - a) / max(a, b)) where a=intra-cluster dist, b=nearest-cluster dist | [-1, +1] | +1 | No | General-purpose cluster quality; works with any distance metric |
| **Calinski-Harabasz** | (between-cluster dispersion / within-cluster dispersion) * (n - k) / (k - 1) | [0, +inf) | Higher | No | Fast computation; favors convex, well-separated clusters |
| **Davies-Bouldin** | mean of max similarity ratio for each cluster pair | [0, +inf) | 0 | No | Penalizes overlapping clusters; no global comparison needed |
| **Adjusted Rand Index** | (Rand Index - Expected Rand Index) / (Max Rand Index - Expected Rand Index) | [-0.5, 1] | +1 | Yes | Comparing clustering output to known labels; chance-corrected |

---

## Threshold-Dependent vs Threshold-Independent Metrics

This distinction is critical for understanding what a metric actually measures.

**Threshold-dependent metrics** require converting continuous scores into discrete predictions at a specific cutoff. Accuracy, precision, recall, F1, and confusion-matrix-derived measures all fall in this category. Their values change as you move the decision threshold — a model with poor precision at 0.5 may have excellent precision at 0.9.

**Threshold-independent metrics** evaluate the model across all possible thresholds simultaneously. AUC-ROC, AUC-PR, and log loss belong here. They measure ranking quality or probability quality without committing to a specific operating point.

**Practical guidance:**
- During model development and comparison, prefer threshold-independent metrics (AUC-PR for imbalanced data, AUC-ROC for balanced). They give a fuller picture of model capability.
- Before deployment, select a threshold based on the cost structure and report threshold-dependent metrics at that operating point. The threshold is a business decision, not a modeling one.
- Always report both: a threshold-independent metric for overall model quality and threshold-dependent metrics at the chosen operating point for deployment-specific performance.

---

## Metric Relationships and Trade-offs

### Precision-Recall Trade-off

Precision and recall are inversely related at any fixed model quality level. Lowering the classification threshold increases recall (you catch more positives) but decreases precision (you also flag more false positives). The trade-off is governed by the model's discriminative ability — a better model pushes the precision-recall curve toward the top-right corner.

**How to navigate this trade-off:**
1. Plot the full precision-recall curve.
2. Identify the threshold that matches your cost structure. If a false negative costs 10x a false positive, operate at high recall even at the expense of precision.
3. Use F-beta score to encode the trade-off explicitly: F-beta = (1 + beta^2) * (precision * recall) / (beta^2 * precision + recall). Beta > 1 weights recall higher; beta < 1 weights precision higher. F1 is the special case where beta = 1.
4. Report the chosen operating point and the reason for choosing it.

### Bias-Variance Trade-off (Diagnostic, Not a Metric)

This is not a metric you compute directly but a diagnostic framework revealed through evaluation patterns:

- **High bias (underfitting):** Training and validation scores are both low and close together. The model is too simple to capture the signal. Fix: increase model capacity, add features, reduce regularization.
- **High variance (overfitting):** Training score is high but validation score is much lower. The model memorizes training noise. Fix: more training data, stronger regularization, simpler model, dropout, ensemble methods.
- **Learning curves** are the primary diagnostic tool. Plot training and validation performance as a function of training set size. Convergence patterns reveal which regime you are in.

### MSE vs MAE Trade-off

MSE (and RMSE) squares errors, giving disproportionate weight to large deviations. MAE treats all errors linearly. The choice between them reflects your tolerance for outliers:
- Use MSE/RMSE when large errors are much worse than small ones (financial risk, safety-critical systems).
- Use MAE when you want the model to optimize for the median rather than the mean, or when outliers are noise rather than signal.
- If unsure, report both. Divergence between MAE and RMSE indicates the presence of large errors — RMSE will be noticeably larger than MAE when a few predictions are far off.

### AUC-ROC vs AUC-PR

Both are threshold-independent, but they tell different stories on imbalanced data:
- **AUC-ROC** uses FPR = FP / (FP + TN) on the x-axis. When TN is very large (e.g., 99% negative class), even a large number of false positives produces a small FPR, making the ROC curve look optimistic.
- **AUC-PR** uses precision on the y-axis, which is directly affected by false positives regardless of the number of true negatives. It gives a more honest picture when you care about the positive class.
- Rule of thumb: if the positive class is less than 10-15% of the data, AUC-PR should be your primary threshold-independent metric.

---

## Business Metric Alignment Guide

ML metrics exist to serve business outcomes, not the other way around. A model improvement that does not translate to business value is not an improvement.

### Mapping Framework

| Business KPI | Relevant ML Metric(s) | Connection |
|---|---|---|
| Revenue from recommendations | NDCG, Precision@k | Higher-quality recommendations drive click-through and conversion |
| Customer churn reduction | Recall at chosen threshold | Catching at-risk customers before they leave; misses = lost revenue |
| Fraud loss reduction | Precision-Recall trade-off at operational threshold | Precision controls false alert costs (investigation); recall controls missed fraud losses |
| Forecast accuracy for inventory | MAE or MAPE | Directly maps to over/under-ordering costs |
| Customer satisfaction (NPS) | Calibration (ECE) + task-specific metric | Well-calibrated confidence scores drive better user-facing decisions |
| Operational cost of model errors | Weighted confusion matrix | Assign dollar values to each cell (TP, FP, TN, FN) and minimize expected cost |
| Regulatory compliance | Fairness metrics (equalized odds, demographic parity) | Required for lending, hiring, insurance in many jurisdictions |
| Time-to-decision | MRR, latency-adjusted metrics | If the model supports search or triage, rank quality and speed both matter |

### Alignment Process

1. **Start with the business question.** What decision does the model support? What happens when it is wrong?
2. **Assign costs to error types.** A false positive in fraud detection costs an investigation ($50). A false negative costs the fraud amount (average $5,000). This 100:1 ratio directly informs threshold selection and metric weighting.
3. **Choose ML metrics that track the business cost.** In the fraud example, optimize for recall at a precision level that keeps investigation budgets feasible, and report the expected dollar loss.
4. **Build a metric dashboard that includes both.** Show ML metrics (AUC-PR, F1, calibration ECE) alongside business metrics (estimated fraud loss, investigation volume, false alert rate). When ML metrics improve but business metrics do not, the evaluation framework is broken.
5. **Set minimum thresholds, not just targets.** Define the minimum acceptable performance below which the model should not be deployed. This is often dictated by the business: "precision must be at least 0.30 or we cannot handle the investigation volume."
6. **Re-evaluate alignment periodically.** Data drift, changing business conditions, and evolving user behavior can break the link between ML metrics and business outcomes. Schedule quarterly reviews of the metric mapping.

### Anti-patterns in Business Alignment

- **Optimizing AUC-ROC when the business cares about a specific operating point.** AUC-ROC summarizes all thresholds equally. If you deploy at one threshold, report performance at that threshold.
- **Using MAPE when actuals include zeros or near-zeros.** MAPE explodes to infinity. Switch to MAE or symmetric MAPE.
- **Reporting R-squared without context.** R-squared = 0.70 sounds good for house price prediction but may be terrible for high-frequency trading. Contextualize with the domain baseline.
- **Treating model comparison as purely technical.** A model that is 0.5% worse on AUC but 10x faster to train, easier to explain, and simpler to maintain may be the better business choice. Include operational metrics in the comparison.
