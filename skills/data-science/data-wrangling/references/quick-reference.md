# Data Wrangling — Quick Reference


## Quick Reference

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Missing values, nulls, NaN handling, imputation | `data-cleaning` | Core cleaning task |
| Outliers, anomalous values, data validation | `data-cleaning` | Data quality assessment |
| Deduplication, record linkage, entity resolution | `data-cleaning` | Data integrity |
| Type casting, date parsing, string normalization | `data-cleaning` | Data standardization |
| One-hot encoding, label encoding, target encoding | `feature-engineering` | Categorical encoding |
| Feature creation, interaction terms, polynomial features | `feature-engineering` | Feature synthesis |
| Scaling, normalization, log transforms, Box-Cox | `feature-engineering` | Numerical transforms |
| Feature selection, importance ranking, dimensionality reduction | `feature-engineering` | Feature optimization |
| Binning, discretization, bucketing continuous variables | `feature-engineering` | Numerical → categorical transforms |
| "Clean up this dataset" | `data-cleaning` | But ask about downstream use to set cleaning depth |
| "Prepare this data for modeling" | Both, sequentially | Clean first, then engineer features |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| data-cleaning says drop rows with missing values, but sample size is already small | Keep rows, use imputation, flag the trade-off | Information preservation beats cleanliness when data is scarce |
| feature-engineering says create many interaction features, but data-cleaning flagged high dimensionality risk | Feature engineering wins on creation, but must include selection step | Create then prune — don't preemptively limit feature space, but do reduce it before modeling |
| data-cleaning says an outlier should be removed, feature-engineering says it's an informative extreme | Keep the value, but create a binary indicator for "extreme" | Preserve information while marking the anomaly — let the model decide |
| data-cleaning recommends aggressive imputation, feature-engineering prefers missingness indicators | Use both — impute and add a "was_missing" indicator | Missingness is often informative; imputed values enable computation; combining captures both signals |
