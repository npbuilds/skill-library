---
name: feature-engineering
description: >
  Feature engineering strategies for machine learning and statistical modeling. Reference when
  encoding categorical variables, creating interaction features, transforming numeric distributions,
  engineering temporal features, or selecting the most predictive feature subset. Use when
  building or improving model inputs.
---

# Feature Engineering — The Signal Extractor

Raw data rarely speaks the language a model needs. Feature engineering is the translation layer — converting messy, heterogeneous inputs into representations that expose the patterns a model can actually learn. A well-engineered feature set often matters more than the choice of algorithm. This skill covers the core transforms, encoding strategies, and selection methods that turn raw columns into predictive signal.

## Numeric Transforms

Numbers look simple, but their raw form often hides the relationship a model needs. Choosing the right transform depends on the distribution, the model type, and the downstream task.

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

**Decision framework:** Tree-based models (XGBoost, Random Forest) are invariant to monotonic transforms — scaling and normalization give them nothing. Linear models, SVMs, and distance-based methods need scaling. Neural networks benefit from bounded inputs (min-max or standardization). When in doubt, standardize — it rarely hurts.

**Binning strategy:** Equal-width bins work when the distribution is roughly uniform. Quantile bins ensure each bin has similar sample counts, which is better for skewed distributions. Domain-driven bins (e.g., age groups 0-17, 18-35, 36-55, 56+) encode known real-world breakpoints and often outperform automatic methods.

## Categorical Encoding

Encoding categorical variables is where the most damage gets done silently. The right choice depends on two axes: **cardinality** (how many unique values) and **model type**.

**Decision matrix — cardinality x model type:**

| | Low cardinality (< 15) | Medium (15-100) | High (100+) |
|---|---|---|---|
| **Linear models** | One-hot | Target or binary encoding | Target or hash encoding |
| **Tree models** | One-hot or ordinal | Ordinal or target encoding | Target or CatBoost encoding |
| **Neural networks** | One-hot or embeddings | Embeddings | Embeddings |
| **Bayesian models** | One-hot | Target with smoothing | Target with smoothing or WoE |

**Key encoding methods:**

- **Label encoding** — Maps categories to integers. Only valid when order is meaningful (ordinal data) or the model is tree-based (which splits on thresholds regardless).
- **One-hot encoding** — One binary column per category. Gold standard for low cardinality. Explodes dimensionally with high cardinality.
- **Ordinal encoding** — Like label, but explicitly preserves a known order (e.g., low < medium < high). Required when rank matters.
- **Target encoding** — Replaces category with mean of the target for that group. Powerful but dangerous — must use cross-validated (out-of-fold) means to avoid leakage.
- **Binary encoding** — Encodes category index in binary, then splits digits into columns. Good middle ground: log2(k) columns instead of k.
- **Frequency encoding** — Replaces category with its count or proportion. Simple, no leakage risk, but loses identity (ties when categories share frequency).
- **Hash encoding** — Hashes categories into a fixed number of buckets. Handles unseen categories gracefully and caps dimensionality.

See `references/encoding-catalog.md` for the full comparison table and code patterns for tricky encodings like target encoding with proper cross-validation.

## Temporal Features

Time-based data requires decomposition to expose the patterns hidden in timestamps.

**Date decomposition — extract all of these as starting features:**
- Year, month, day of month, day of week (0=Monday), day of year
- Quarter, week of year, hour, minute (if applicable)
- Is_weekend, is_month_start, is_month_end, is_quarter_end

**Cyclical encoding** — Months and weekdays are cyclical (December is close to January). Encode using sin/cos pairs:
- `month_sin = sin(2 * pi * month / 12)`
- `month_cos = cos(2 * pi * month / 12)`

This preserves the circular distance that ordinal encoding destroys.

**Lag features** — For time series, the most informative features are often past values of the target itself:
- lag_1, lag_7, lag_30 (yesterday, last week, last month)
- diff_1 (change from previous period)

**Rolling aggregates** — Capture trends and volatility:
- rolling_mean_7, rolling_mean_30 (smoothed trend)
- rolling_std_7 (recent volatility)
- rolling_min, rolling_max (range bounds)

**Time since events** — Days since last purchase, hours since last login, seconds since last failure. These decay features often carry more signal than raw timestamps.

**Holiday and event flags** — Binary indicators for holidays, promotional periods, or known disruptions. Combine with day-of-week for interaction effects.

## Text Features

Text requires conversion to numeric representation. The right approach depends on data volume and task complexity.

**Simple methods (start here):**
- **Count vectors (Bag of Words)** — Word frequencies. Fast, interpretable, works surprisingly well for classification with linear models.
- **TF-IDF** — Count vectors weighted by inverse document frequency. Dampens common words, highlights distinctive ones. Default starting point for most text classification.
- **N-grams** — Capture word pairs or triples (bigrams, trigrams). "not good" carries different meaning than "good" alone.

**Embedding methods (when simple falls short):**
- **Word2Vec / GloVe** — Pre-trained word embeddings. Average word vectors for document-level representation. Good when labeled data is scarce.
- **Sentence transformers** — Models like all-MiniLM-L6-v2 produce dense vectors capturing semantic meaning. Best for similarity tasks, semantic search, and transfer learning.
- **LLM embeddings** — API-based embeddings from large language models. Highest quality but highest cost and latency.

**Decision rule:** Start with TF-IDF plus a linear model. If that gets you within a few points of your target metric, stop. Move to embeddings when you need semantic understanding, multilingual support, or are working with short/noisy text where word overlap is sparse.

## Interaction & Domain Features

Individual features capture marginal effects. Interactions capture how features behave together.

**Cross-features** — Multiply or concatenate features that interact: `price_per_sqft = price / sqft`, `bmi = weight / height^2`. Domain knowledge guides which crosses matter.

**Ratio features** — Particularly powerful in financial and operational contexts: `debt_to_income`, `click_through_rate = clicks / impressions`, `capacity_utilization = output / max_capacity`.

**Feature crosses for different model types:**
- **Tree models** discover interactions naturally through sequential splits — explicit crosses add less value but can still speed up learning.
- **Linear models cannot learn interactions** unless you create them explicitly. Polynomial features and manual crosses are essential.
- **Neural networks** learn interactions through hidden layers, but providing obvious domain crosses as inputs still helps convergence.

**Domain-driven combinations** — The highest-value features almost always come from domain expertise, not mechanical generation. Talk to subject matter experts. Examples: recency-frequency-monetary (RFM) features in marketing, technical indicators in finance, vital sign ratios in healthcare.

## Feature Selection

More features is not better. Irrelevant features add noise, increase training time, and cause overfitting. Select deliberately.

**Filter methods** — Fast, model-independent, run first:
- **Correlation** — Drop features with near-zero correlation to target, or near-perfect correlation with each other (redundancy).
- **Mutual information** — Captures nonlinear relationships that correlation misses. Good general-purpose filter.
- **Chi-square** — For categorical features vs. categorical target. Tests independence.
- **Variance threshold** — Drop near-constant features (zero variance = zero information).

**Wrapper methods** — Use model performance to guide selection:
- **Recursive Feature Elimination (RFE)** — Train model, drop weakest feature, repeat. Effective but expensive.
- **Forward selection** — Start empty, add the feature that improves performance the most, repeat.
- **Backward elimination** — Start with all features, drop the least impactful one, repeat.

**Embedded methods** — Selection happens during model training:
- **L1 regularization (Lasso)** — Drives weak coefficients to exactly zero. Built-in selection for linear models.
- **Tree-based importance** — XGBoost/LightGBM report feature importance via gain or split count. Fast, but can be biased toward high-cardinality features.
- **Permutation importance** — Shuffle a feature and measure performance drop. Model-agnostic and less biased than built-in importance.

**When to use which:** Start with variance threshold and correlation filters to cheaply remove obvious noise. Use mutual information to rank survivors. If still too many features, apply RFE with your target model or rely on L1/tree importance. For final production models, validate selected features with permutation importance on a holdout set.

## Automated Feature Engineering

Manual engineering is powerful but slow. Automated tools can supplement (not replace) domain expertise.

- **Deep Feature Synthesis (featuretools)** — Automatically generates aggregations and transforms across relational tables. Excellent for multi-table datasets. Can produce thousands of candidates that then need selection.
- **AutoFeat** — Constructs and selects polynomial and interaction features with built-in L1 selection. Good for tabular data with linear models.
- **LLM-based feature engineering** — Using LLMs to suggest feature ideas based on column names and sample data. Emerging approach — useful for brainstorming but needs human validation.

**When manual beats automated:** Small datasets, strong domain knowledge available, regulatory requirements for interpretability. **When automated beats manual:** Large relational databases, hundreds of tables, time pressure, exploratory phase where you need a broad feature search.

The best practice is to combine both: use automated tools to generate candidates, then apply domain knowledge to prune, validate, and name the survivors meaningfully.

## Common Mistakes

1. **Target leakage through encoding** — Computing target encoding using the full dataset instead of out-of-fold means. The model memorizes noise, validation looks great, production fails. Always use cross-validated encoding.
2. **High-cardinality one-hot explosion** — One-hot encoding a column with 10,000 categories creates 10,000 sparse columns. Use target, hash, or embedding-based encoding instead.
3. **Fitting transforms on the full dataset** — Fitting scalers, encoders, or imputers on train+test, then splitting. Information from the test set leaks into the transform. Fit only on training data, apply to test.
4. **Ignoring feature interactions in linear models** — Assuming a linear model can capture `price * location` effects without explicitly creating the interaction term. It cannot.
5. **Dropping features based on univariate analysis alone** — A feature with zero correlation to the target may be highly predictive in combination with another feature. Univariate filters miss this — use them as a first pass, not the final word.
6. **Treating ordinal data as nominal** — One-hot encoding a feature like education level (high school < bachelor's < master's < PhD) destroys the rank information. Use ordinal encoding to preserve it.

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

**Recommended starting stack (Python):** `sklearn.preprocessing` + `sklearn.feature_selection` for core transforms, `category_encoders` for advanced categorical encoding, `featuretools` for automated feature generation, `polars` for high-performance transforms on large datasets.

## When This Applies

Activate this skill when:
- Building or refining input features for any supervised or unsupervised model
- Encountering new data types (timestamps, categories, text) that need numeric representation
- Model performance has plateaued and better features may help more than a better algorithm
- Preparing data for a model that has specific input requirements (scaling for SVMs, encoding for linear models)
- Reviewing someone else's feature pipeline for leakage or missed opportunities
