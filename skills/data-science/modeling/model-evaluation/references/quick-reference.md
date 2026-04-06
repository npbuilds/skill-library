# Model Evaluation — Quick Reference


## Quick Reference

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

## Quick Reference

| Data Characteristic | Recommended Strategy | Why |
|---|---|---|
| Sufficient data (>50k), no structure | Hold-out (70/15/15 or 80/10/10) | Simple, fast, stable estimates |
| Moderate data (<50k), i.i.d. | 5- or 10-fold CV | Reduces variance of performance estimate |
| Imbalanced classes | Stratified k-fold CV | Preserves class distribution in every fold |
| Temporal ordering | Time-series CV (expanding or sliding window) | Prevents future data leaking into training |
| Grouped observations (patients, users) | Group k-fold | Prevents same group appearing in train and test |
| Hyperparameter tuning + evaluation | Nested CV (inner loop tunes, outer loop evaluates) | Prevents selection bias from tuning on test data |
| Very small data (<500) | Leave-one-out CV or repeated k-fold | Maximizes training data per split |

## Quick Reference

| Method | When to Use | Notes |
|---|---|---|
| Paired t-test on CV folds | k-fold CV results, roughly normal differences | Fast but assumes independence of folds (violated in practice) |
| Corrected resampled t-test (Nadeau-Bengio) | k-fold CV results | Corrects for non-independence by adjusting variance estimate; preferred over naive paired t-test |
| McNemar's test | Two classifiers on the same test set | Tests whether disagreement patterns are symmetric; does not need CV |
| Wilcoxon signed-rank test | Non-normal differences, small sample of datasets | Non-parametric; robust when normality assumption fails |
| Bayesian comparison | Want probability statements, not p-values | Produces P(A > B), P(rope), P(B > A); more informative than frequentist tests |

## Quick Reference

| Criterion | Definition | Intuition |
|---|---|---|
| Demographic Parity | P(positive prediction) is equal across groups | Selection rates are the same regardless of group membership |
| Equalized Odds | TPR and FPR are equal across groups | The model makes errors at the same rate for all groups |
| Equal Opportunity | TPR is equal across groups | Among true positives, all groups have equal chance of being correctly identified |
| Predictive Parity | Precision is equal across groups | A positive prediction means the same thing regardless of group |

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
