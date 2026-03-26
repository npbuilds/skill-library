---
name: data-cleaning
description: >
  Data cleaning and preprocessing strategies for analytical datasets. Reference when handling
  missing values, detecting outliers, deduplicating records, validating data types, or
  establishing reproducible cleaning pipelines. Use when preparing any dataset for analysis
  or modeling.
---

# Data Cleaning — The Foundation

Data cleaning is the unglamorous work that determines whether your analysis produces insight or nonsense. Studies consistently estimate that data scientists spend 60-80% of their time on data preparation, yet most errors in production models trace back to cleaning decisions made hastily or without clear methodology. This skill provides structured decision frameworks for the five core cleaning operations: handling missing data, detecting outliers, deduplicating records, enforcing types, and designing reproducible pipelines.

Every cleaning decision is a modeling decision. Dropping rows, imputing values, and capping outliers all change the statistical properties of your data. The goal is never "clean data" in the abstract — it is data whose known imperfections are documented and whose transformations are justified by the analysis objective.

---

## Missing Data

Missing data is not a single problem — it is three distinct problems that demand different responses. Before touching a single null value, classify the missingness mechanism.

### The Three Mechanisms

| Mechanism | Definition | Example | Test |
|-----------|-----------|---------|------|
| **MCAR** (Missing Completely At Random) | Missingness is unrelated to any variable, observed or unobserved | Sensor randomly fails due to power flicker | Little's MCAR test; compare distributions of complete vs incomplete cases |
| **MAR** (Missing At Random) | Missingness depends on observed variables but not the missing value itself | Higher-income respondents skip the income question less often, but within an income bracket, missingness is random | Logistic regression predicting missingness from observed variables |
| **MNAR** (Missing Not At Random) | Missingness depends on the unobserved value itself | Patients with severe symptoms drop out of a trial because of those symptoms | Cannot be tested directly; requires domain knowledge and sensitivity analysis |

### Decision Framework for Missing Values

**Step 1: Quantify.** Calculate missingness percentage per column and per row. Visualize missingness patterns (use `missingno` or `naniar`).

**Step 2: Classify the mechanism** using the table above.

**Step 3: Choose a strategy:**

| Missingness % | Mechanism | Recommended Strategy |
|---------------|-----------|---------------------|
| < 5% | MCAR | Listwise deletion is usually safe; simple imputation acceptable |
| 5-25% | MCAR | Mean/median for numeric; mode or KNN for categorical |
| 5-25% | MAR | KNN imputation, MICE, or multiple imputation |
| > 25% | MCAR/MAR | Multiple imputation (MICE); consider whether the variable is salvageable |
| Any % | MNAR | Domain-driven imputation or explicit modeling of the missingness mechanism; add a "was_missing" indicator variable |
| > 50% | Any | Strongly consider dropping the variable unless it is critical to the analysis |

**Step 4: Validate.** Compare distributions before and after imputation. Check that correlations between variables are preserved. See `references/imputation-guide.md` for detailed method comparisons and validation techniques.

### Key Imputation Methods (Quick Reference)

- **Mean/Median** — Fast and simple. Distorts variance and weakens correlations. Use only for MCAR with low missingness.
- **KNN Imputation** — Finds k nearest neighbors using observed features, imputes from their values. Handles mixed types. Sensitive to scale and k choice.
- **MICE (Multiple Imputation by Chained Equations)** — Iteratively models each variable with missingness as a function of all other variables. Produces multiple completed datasets. Gold standard for MAR data.
- **Multiple Imputation** — Run your analysis on each imputed dataset and pool results using Rubin's rules. Properly propagates uncertainty from the imputation step into your final estimates.

---

## Outlier Detection

An outlier is not inherently wrong. It is a data point that does not conform to the expected pattern. The correct response depends entirely on why it deviates.

### Detection Methods

| Method | How It Works | Best For | Limitations |
|--------|-------------|----------|-------------|
| **IQR Rule** | Flag points below Q1 - 1.5*IQR or above Q3 + 1.5*IQR | Univariate, roughly symmetric distributions | Fails on skewed data; arbitrary multiplier |
| **Z-Score** | Flag points with |z| > 3 | Normally distributed data | Sensitive to the outliers themselves (mean and SD are affected) |
| **Modified Z-Score** | Uses median and MAD instead of mean and SD | Robust univariate detection | Still univariate |
| **Isolation Forest** | Tree-based anomaly scoring; outliers are isolated in fewer splits | Multivariate, high-dimensional data | Requires tuning contamination parameter |
| **Local Outlier Factor (LOF)** | Compares local density of a point to its neighbors | Clusters of varying density | Sensitive to k; computationally expensive |
| **Domain Rules** | Hard-coded business constraints (e.g., age must be 0-120) | Known constraints | Only catches violations of known rules |

### Decision Table: What To Do With Outliers

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Data entry error (impossible value) | **Remove or correct** | Not real data |
| Measurement error (sensor malfunction) | **Remove** and flag for data source investigation | Not representative |
| Genuine extreme value, robust method available | **Keep** | Real signal; use median-based or tree-based models |
| Genuine extreme value, sensitive method required | **Winsorize/cap** at a percentile (e.g., 1st/99th) | Preserves the observation while limiting leverage |
| Rare but valid event (fraud, equipment failure) | **Keep and study separately** | May be exactly what you are looking for |

**Rule of thumb:** If you are removing more than 2-3% of your data as outliers, re-examine your detection threshold or your assumptions about the distribution.

---

## Deduplication

Duplicate records inflate counts, bias aggregations, and cause data leakage when splits are not deduplicated before modeling.

### Matching Strategies

**Exact Matching** — Group by a unique key or composite key and keep the first, last, or most complete record. Use when you have reliable identifiers (primary keys, UUIDs, composite natural keys). Always the first approach to try.

**Fuzzy Matching** — Required when identifiers are unreliable (typos in names, inconsistent formatting).

| Algorithm | Strength | Use When |
|-----------|----------|----------|
| **Levenshtein Distance** | Catches insertions, deletions, substitutions | Short strings; names, product codes |
| **Jaro-Winkler** | Weights prefix matches more heavily | Person names (where first characters are most reliable) |
| **Soundex / Metaphone** | Phonetic matching | Names that may be spelled differently but sound alike |
| **TF-IDF + Cosine Similarity** | Handles longer text, word reordering | Addresses, descriptions, free-text fields |

**Record Linkage** — When deduplicating across datasets (entity resolution), use blocking to reduce comparison pairs, then score candidate pairs with a probabilistic model (Fellegi-Sunter) or a trained classifier. Libraries: `dedupe`, `recordlinkage`, `splink`.

**Tip:** Always log which records were merged and what resolution logic was applied. Deduplication is often the hardest cleaning step to audit after the fact.

---

## Type Validation & Coercion

Silent type mismatches cause subtle, dangerous bugs: string "0" treated as falsy, dates sorted lexicographically, zip codes losing leading zeros when cast to integers.

### Common Mismatches and Fixes

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Dates sort incorrectly | Stored as strings in varying formats | Parse to datetime with explicit format; standardize to ISO 8601 |
| Numeric column has `object` dtype | Mixed types or stray non-numeric values (commas, currency symbols, "N/A") | Strip formatting characters, coerce with `errors='coerce'`, inspect resulting nulls |
| Categorical treated as continuous | Encoded as integers (1, 2, 3) but represent unordered categories | Cast to `category` dtype or string; never compute mean of nominal codes |
| Zip/phone codes truncated | Leading zeros dropped by numeric parsing | Store as strings |
| Boolean ambiguity | "Yes"/"No", "Y"/"N", 1/0, "True"/"False" mixed in one column | Map to canonical boolean with explicit lookup dict; reject unknown values |

### Validation Frameworks

Use schema validation to catch problems at ingestion rather than during analysis:

- **Great Expectations** — Define expectations (column X is never null, column Y is between 0 and 100) as code. Run validation suites as part of your pipeline.
- **Pandera** — Schema validation for pandas DataFrames with type checking, statistical checks, and hypothesis tests.
- **Pydantic / dataclasses** — Row-level validation when loading structured records.
- **JSON Schema / Avro / Protobuf** — Schema enforcement at the data contract layer for upstream producers.

---

## Cleaning Pipeline Design

The order in which you clean matters. Deduplicating after imputation wastes compute and risks imputing from duplicate records. Outlier detection on data with type errors produces meaningless results.

### Recommended Order of Operations

```
1. Schema Validation & Type Coercion
   - Enforce expected types, reject or quarantine malformed rows
   - Standardize formats (dates, strings, encodings)

2. Deduplication
   - Remove exact duplicates
   - Resolve fuzzy duplicates

3. Missing Data Handling
   - Classify missingness mechanism
   - Apply appropriate imputation strategy

4. Outlier Detection & Treatment
   - Apply statistical and domain-based detection
   - Remove, cap, or flag as appropriate

5. Feature-Level Validation
   - Cross-field consistency checks
   - Business rule validation

6. Final Audit
   - Row count reconciliation
   - Distribution comparison (pre vs post cleaning)
   - Generate cleaning report
```

### Reproducibility Principles

**Code-first, always.** Never clean data in a spreadsheet or through manual edits. Every transformation must be scripted so it can be re-run on new data.

**Idempotent pipelines.** Running the pipeline twice on the same input should produce the same output. Avoid operations that depend on run order or mutable state.

**Version raw data.** Store the original dataset immutably. Apply cleaning as a transformation layer. If your cleaning logic changes, you can always re-derive the cleaned dataset.

**Data contracts.** Agree on schema, formats, and acceptable value ranges with upstream data producers. Validate incoming data against the contract before cleaning. This shifts errors left and reduces the cleaning burden.

**Documentation.** For every cleaning decision, record: what was done, why, how many records were affected, and what the alternative was. A cleaning log is not optional — it is part of the deliverable.

---

## Common Mistakes

1. **Dropping all rows with any missing value.** Listwise deletion on a dataset with 20 columns, each 5% missing independently, discards ~64% of your data. Analyze missingness patterns before dropping.

2. **Imputing before understanding the missingness mechanism.** Mean imputation on MNAR data actively biases your results toward the observed population. Classify first, impute second.

3. **Cleaning test data with training statistics.** If you compute imputation values (means, medians) on the full dataset before splitting, you leak information from the test set into training. Fit imputers on training data only; transform test data using those fitted values.

4. **Treating all outliers as errors.** Removing genuine extreme values because they are inconvenient destroys real signal. Always investigate before removing.

5. **Using a single imputed dataset for inference.** Single imputation understates uncertainty. If your analysis involves hypothesis tests or confidence intervals, use multiple imputation and pool results with Rubin's rules.

6. **Cleaning in place without preserving the raw data.** If you overwrite the original file with cleaned data and later discover a bug in your cleaning logic, you cannot recover. Always keep raw and cleaned data separate.

---

## Implementation Libraries

| Task | Python | R |
|------|--------|---|
| Core DataFrame operations, cleaning transforms | `pandas`, `polars` | `dplyr`, `tidyr` (tidyverse) |
| Clean APIs for common cleaning tasks | `pyjanitor` | `janitor` |
| Missing data visualization | `missingno` | `naniar` |
| Imputation (KNN, iterative/MICE, simple) | `sklearn.impute` | `mice`, `Amelia` |
| Advanced imputation (random forest, MICE) | `miceforest` | `missForest` |
| Label error detection | `cleanlab` | — |
| Record linkage, deduplication | `dedupe`, `splink`, `recordlinkage` | `RecordLinkage` |
| Schema validation, data contracts | `pandera`, `great_expectations` | `validate`, `pointblank` |
| Type validation | `pydantic` | — |

**Recommended starting stack (Python):** `pandas` or `polars` for DataFrame operations, `pyjanitor` for clean chaining syntax, `sklearn.impute` for imputation, `pandera` for schema validation, `missingno` for missing data visualization.

## When This Applies

**Use this skill when:**
- Preparing any tabular dataset for analysis, modeling, or reporting
- Building ETL or ELT pipelines that ingest messy source data
- Conducting exploratory data analysis and encountering nulls, duplicates, or type inconsistencies
- Designing data quality checks for production systems
- Reviewing someone else's data preparation code

**Out of scope:**
- Feature engineering (transformations that create new analytical variables belong in a separate skill)
- Unstructured data cleaning (text normalization, image preprocessing) — these have their own domain-specific methods
- Data collection design (sampling strategies, survey design) — cleaning cannot fix fundamentally flawed collection
- Real-time streaming data quality — the principles apply but the tooling and latency constraints differ significantly
