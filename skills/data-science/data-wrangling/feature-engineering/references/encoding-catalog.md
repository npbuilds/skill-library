# Encoding Catalog — Complete Reference

Comprehensive reference for categorical encoding methods, with comparison matrix and code patterns for the encodings that are easy to get wrong.

## Encoding Method Comparison

| Method | Cardinality Suitability | Model Compatibility | Preserves Ordinality | Handles Unseen Categories | Memory Footprint |
|--------|------------------------|--------------------|--------------------|--------------------------|-----------------|
| **Label Encoding** | Any | Tree models only (misleads linear/distance models) | No (imposes false order) | No — crashes or needs fallback | Minimal (1 column) |
| **One-Hot Encoding** | Low (< 15) | All models | No | No — unknown column missing | High (k columns) |
| **Ordinal Encoding** | Any (if order exists) | All models (when order is real) | Yes | No — needs manual mapping | Minimal (1 column) |
| **Target Encoding** | Medium to High | All models | No | Yes (falls back to global mean) | Minimal (1 column) |
| **Binary Encoding** | Medium (15-100) | All models | No | Partial (hash collision) | Low (log2(k) columns) |
| **Frequency Encoding** | Any | All models | No | No — unseen has no frequency | Minimal (1 column) |
| **Hash Encoding** | High (100+) | All models | No | Yes (hashes any string) | Fixed (n_components columns) |
| **Leave-One-Out** | Medium to High | All models | No | Yes (falls back to global mean) | Minimal (1 column) |
| **James-Stein** | Medium to High | Linear models, Bayesian | No | Yes (shrinks to global mean) | Minimal (1 column) |
| **CatBoost Encoding** | Any | Tree models (designed for CatBoost) | No | Yes (uses running statistics) | Minimal (1 column) |
| **Weight of Evidence (WoE)** | Medium | Logistic regression, scorecard models | No | No — needs fallback | Minimal (1 column) |

## Method Details

### Label Encoding

Maps each category to an integer: `{cat: 0, dog: 1, bird: 2}`. The integers have no meaningful order, so linear models and distance-based models interpret them as having a numeric relationship (dog is "between" cat and bird). Tree models are unaffected because they split on thresholds.

**Use when:** Tree-based models with any cardinality, or when feeding into an embedding layer.

### One-Hot Encoding

Creates one binary column per category. The result is a sparse matrix where exactly one column is 1 per row. Standard default for low-cardinality categoricals.

**Watch out for:** The dummy variable trap in linear models (k-1 columns needed, not k, to avoid perfect multicollinearity). Most libraries handle this with `drop='first'`.

### Ordinal Encoding

Maps categories to integers following a known order: `{low: 0, medium: 1, high: 2}`. Unlike label encoding, the numeric order reflects real-world rank.

**Use when:** The categories have a natural hierarchy (education level, severity rating, satisfaction score). Verify the order is correct — getting it wrong is worse than one-hot encoding.

### Target Encoding (Mean Encoding)

Replaces each category with the mean of the target variable for that group. Extremely powerful for high-cardinality features but prone to overfitting and target leakage if done naively.

**Must use cross-validated encoding** — see code pattern below.

### Binary Encoding

Converts category index to binary representation, then splits each bit into a separate column. A feature with 100 categories produces ceil(log2(100)) = 7 columns instead of 100.

**Use when:** Cardinality is too high for one-hot but you want a model-agnostic approach without target leakage risk.

### Frequency Encoding

Replaces each category with its count or proportion in the training set. Simple, no leakage, no target information used.

**Limitation:** Categories with the same frequency become indistinguishable. Consider combining with another encoding when frequency ties are common.

### Hash Encoding (Feature Hashing)

Applies a hash function to map categories into a fixed number of buckets. Collisions are possible but controlled by choosing an appropriate number of components.

**Use when:** Very high cardinality, online learning, or when new categories appear at inference time. Typical component counts: 8-32 for moderate cardinality, 64-256 for very high.

### Leave-One-Out Encoding

Like target encoding, but for each row, the mean is computed excluding that row's own target value. Reduces overfitting compared to naive target encoding but does not eliminate it entirely.

**Use when:** You want target-based encoding without implementing full cross-validation. Still benefits from smoothing.

### James-Stein Encoding

Shrinks category-level means toward the global mean using a Bayesian shrinkage estimator. Categories with few observations get pulled strongly toward the global mean; well-represented categories keep their own mean.

**Use when:** Working with Bayesian models or when you want principled regularization of target encoding without manual tuning.

### CatBoost Encoding (Ordered Target Encoding)

Computes target statistics using only the rows that appear before the current row in a random permutation. This simulates an "online" encoding that prevents leakage by design.

**Use when:** Training CatBoost models (it applies this internally) or when you want a leakage-resistant target encoding without cross-validation overhead.

### Weight of Evidence (WoE)

Measures the "strength of evidence" for each category to predict a binary outcome. Defined as `ln(% of events / % of non-events)` for each category. Positive WoE means the category is associated with the event; negative means it predicts non-event.

**Use when:** Building credit scorecards or logistic regression models in financial risk. Often paired with Information Value (IV) for feature selection.

## Code Patterns

### Target Encoding with Proper Cross-Validation

Naive target encoding leaks the target into the features. The correct approach computes the encoding using out-of-fold data only.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

def target_encode_cv(train_df, column, target, n_folds=5, smoothing=10):
    """
    Target encoding with cross-validated out-of-fold means.

    Args:
        train_df: Training DataFrame
        column: Categorical column name to encode
        target: Target column name
        n_folds: Number of CV folds
        smoothing: Smoothing factor — higher values shrink more toward
                   the global mean. Controls regularization.

    Returns:
        encoded: Series with encoded values for training data
        mapping: Dict mapping category -> smoothed mean (for test data)
    """
    global_mean = train_df[target].mean()
    encoded = pd.Series(index=train_df.index, dtype=float)

    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)

    for train_idx, val_idx in kf.split(train_df):
        # Compute means using only the training fold
        fold_train = train_df.iloc[train_idx]
        means = fold_train.groupby(column)[target].agg(['mean', 'count'])

        # Apply smoothing: blend category mean with global mean
        # weight = count / (count + smoothing)
        smooth_mean = (
            means['mean'] * means['count'] + global_mean * smoothing
        ) / (means['count'] + smoothing)

        # Encode the validation fold using training fold statistics
        encoded.iloc[val_idx] = train_df.iloc[val_idx][column].map(smooth_mean)

    # Fill any NaN (unseen in fold) with global mean
    encoded.fillna(global_mean, inplace=True)

    # Build full mapping for encoding test data
    full_stats = train_df.groupby(column)[target].agg(['mean', 'count'])
    mapping = (
        (full_stats['mean'] * full_stats['count'] + global_mean * smoothing)
        / (full_stats['count'] + smoothing)
    ).to_dict()

    return encoded, mapping


def apply_target_encoding(test_df, column, mapping, global_mean):
    """Apply pre-computed target encoding to test data."""
    return test_df[column].map(mapping).fillna(global_mean)


# Usage:
# train_encoded, encoding_map = target_encode_cv(train, 'city', 'price')
# test_encoded = apply_target_encoding(test, 'city', encoding_map, train['price'].mean())
```

**Why smoothing matters:** A category that appears only twice with both target values = 1 gets a mean of 1.0 — pure noise. Smoothing blends the category mean toward the global mean, with the blending strength inversely proportional to sample size. A smoothing value of 10-20 is a reasonable default; increase it for noisier data or rarer categories.

### Cyclical Encoding for Temporal Features

Ordinal encoding of months (1-12) tells the model that December (12) and January (1) are maximally distant. Cyclical encoding using sin/cos preserves the circular nature.

```python
import numpy as np
import pandas as pd

def cyclical_encode(series, period):
    """
    Encode a cyclical feature as sin/cos pair.

    Args:
        series: Numeric series (e.g., month 1-12, hour 0-23, day_of_week 0-6)
        period: The cycle length (12 for months, 24 for hours, 7 for weekdays)

    Returns:
        sin_component, cos_component: Two Series forming the encoding
    """
    radians = 2 * np.pi * series / period
    return np.sin(radians), np.cos(radians)


# Usage:
# df['month_sin'], df['month_cos'] = cyclical_encode(df['month'], period=12)
# df['hour_sin'],  df['hour_cos']  = cyclical_encode(df['hour'],  period=24)
# df['dow_sin'],   df['dow_cos']   = cyclical_encode(df['day_of_week'], period=7)
```

**Why two components:** A single sin or cos is ambiguous — sin(month=3) equals sin(month=9). The pair together uniquely identifies each position in the cycle. Both columns must be included; dropping one reintroduces the ambiguity.

### Weight of Evidence (WoE) Encoding

Used primarily in credit risk scorecard development. Requires a binary target.

```python
import numpy as np
import pandas as pd

def woe_encode(train_df, column, target, regularization=0.5):
    """
    Weight of Evidence encoding for binary classification.

    Args:
        train_df: Training DataFrame
        column: Categorical column to encode
        target: Binary target column (0/1)
        regularization: Added to numerator/denominator to prevent
                        division by zero and log(0). Default 0.5.

    Returns:
        encoded: Series with WoE values
        woe_map: Dict mapping category -> WoE (for test data)
        iv: Information Value for this feature (for selection)
    """
    total_events = train_df[target].sum()
    total_non_events = len(train_df) - total_events

    grouped = train_df.groupby(column)[target].agg(['sum', 'count'])
    grouped.columns = ['events', 'total']
    grouped['non_events'] = grouped['total'] - grouped['events']

    # Distribution of events and non-events per category
    grouped['pct_events'] = (grouped['events'] + regularization) / (total_events + regularization)
    grouped['pct_non_events'] = (grouped['non_events'] + regularization) / (total_non_events + regularization)

    # WoE = ln(% events / % non-events)
    grouped['woe'] = np.log(grouped['pct_events'] / grouped['pct_non_events'])

    # Information Value = sum((pct_events - pct_non_events) * WoE)
    grouped['iv_component'] = (grouped['pct_events'] - grouped['pct_non_events']) * grouped['woe']
    iv = grouped['iv_component'].sum()

    woe_map = grouped['woe'].to_dict()
    encoded = train_df[column].map(woe_map)

    return encoded, woe_map, iv


# Usage:
# train_woe, woe_map, iv = woe_encode(train, 'occupation', 'default')
# test_woe = test['occupation'].map(woe_map).fillna(0)
#
# IV interpretation:
#   < 0.02  — useless predictor
#   0.02-0.1 — weak predictor
#   0.1-0.3  — medium predictor
#   0.3-0.5  — strong predictor
#   > 0.5   — suspicious (possible overfitting or leakage)
```

### CatBoost-Style Ordered Encoding

This replicates the encoding CatBoost uses internally. Rows are processed in sequence, and each row's encoding uses only the target values of rows that appeared before it.

```python
import numpy as np
import pandas as pd

def catboost_encode(train_df, column, target, smoothing=1.0, random_state=42):
    """
    Ordered target encoding (CatBoost-style).

    Rows are shuffled, then each row is encoded using the running
    mean of the target for its category from preceding rows only.

    Args:
        train_df: Training DataFrame
        column: Categorical column to encode
        target: Target column name
        smoothing: Prior strength (higher = more regularization)
        random_state: Seed for shuffle reproducibility

    Returns:
        encoded: Series with encoded values
    """
    df = train_df.sample(frac=1, random_state=random_state).reset_index(drop=True)
    global_mean = df[target].mean()

    cumsum = df.groupby(column)[target].cumsum() - df[target]
    cumcount = df.groupby(column).cumcount()

    encoded = (cumsum + global_mean * smoothing) / (cumcount + smoothing)

    # Restore original order
    encoded.index = df.index
    return encoded.sort_index()

# Usage:
# train['city_encoded'] = catboost_encode(train, 'city', 'price')
```

## Encoding Selection Checklist

When choosing an encoding method, walk through these questions in order:

1. **Is there a natural order?** If yes, use ordinal encoding.
2. **How many unique values?** If < 15, one-hot is usually fine. If 15-100, consider binary or target encoding. If 100+, use target, hash, or embeddings.
3. **What model are you using?** Tree models tolerate label/ordinal encoding. Linear models need one-hot or target encoding. Neural networks benefit from embeddings for high cardinality.
4. **Is the target binary?** WoE is an option and provides built-in feature selection via IV.
5. **Will unseen categories appear at inference?** If yes, use hash encoding or target encoding with a global mean fallback. One-hot and label encoding break on unseen values.
6. **Is interpretability required?** WoE and ordinal encoding are interpretable. Target and hash encoding are harder to explain.
7. **Is target leakage a concern?** Always, with any target-based encoding. Use CV-based target encoding, leave-one-out, or CatBoost-style ordered encoding. Never compute target statistics on the full dataset.
