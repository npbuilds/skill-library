# Feature Engineering — Quick Reference


## Quick Reference

| Transform | When to Use | Effect on Distribution |
|-----------|-------------|----------------------|
| **Standardization** (z-score) | Features on different scales feeding linear models, SVMs, or k-NN | Centers at 0, unit variance; preserves shape |
| **Min-Max** (0-1 scaling) | Neural networks, algorithms needing bounded inputs | Compresses to [0,1]; preserves shape, sensitive to outliers |
| **Robust Scaling** (median/IQR) | Data with significant outliers | Centers at median, scales by IQR; dampens outlier influence |
| **Log Transform** | Right-skewed data (income, counts, prices) | Compresses right tail, pulls toward normality |
| **Box-Cox** | Right-skewed, strictly positive data | Optimally normalizes via parameterized power transform |
| **Yeo-Johnson** | Skewed data including zeros and negatives | Generalized Box-Cox that handles non-positive values |
| **Quantile Transform** | Extreme skew, need uniform or normal output | Forces any distribution to target shape; destroys distances |
| **Binning** (equal-width/quantile) | Capturing nonlinear effects in linear models, reducing noise | Converts continuous to ordinal; loses granularity |
| **Polynomial Features** | Known nonlinear relationships in linear models | Creates x^2, x^3, x1*x2 terms; watch dimensionality blow-up |

## Quick Reference

| | Low cardinality (< 15) | Medium (15-100) | High (100+) |
|---|---|---|---|
| **Linear models** | One-hot | Target or binary encoding | Target or hash encoding |
| **Tree models** | One-hot or ordinal | Ordinal or target encoding | Target or CatBoost encoding |
| **Neural networks** | One-hot or embeddings | Embeddings | Embeddings |
| **Bayesian models** | One-hot | Target with smoothing | Target with smoothing or WoE |

## Implementation Libraries

| Task | Python | R |
|------|--------|---|
| Scaling, normalization, polynomial features | `sklearn.preprocessing` | `recipes` (tidymodels) |
| Categorical encoding (target, WoE, binary, hash, etc.) | `category_encoders` | `embed` (tidymodels) |
| Feature selection (RFE, mutual info, chi-square) | `sklearn.feature_selection` | `recipes` step functions |
| Automated feature engineering (DFS) | `featuretools` | — |
| sklearn-compatible feature transforms | `feature-engine` | `recipes` |
| High-performance DataFrame operations | `polars`, `pandas` | `data.table`, `dplyr` |
| Text vectorization (TF-IDF, count vectors) | `sklearn.feature_extraction.text` | `tidytext`, `text2vec` |
| Embeddings (sentence-level) | `sentence-transformers` | — |
