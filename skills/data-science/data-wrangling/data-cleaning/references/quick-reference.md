# Data Cleaning — Quick Reference


## The Three Mechanisms

| Mechanism | Definition | Example | Test |
|-----------|-----------|---------|------|
| **MCAR** (Missing Completely At Random) | Missingness is unrelated to any variable, observed or unobserved | Sensor randomly fails due to power flicker | Little's MCAR test; compare distributions of complete vs incomplete cases |
| **MAR** (Missing At Random) | Missingness depends on observed variables but not the missing value itself | Higher-income respondents skip the income question less often, but within an income bracket, missingness is random | Logistic regression predicting missingness from observed variables |
| **MNAR** (Missing Not At Random) | Missingness depends on the unobserved value itself | Patients with severe symptoms drop out of a trial because of those symptoms | Cannot be tested directly; requires domain knowledge and sensitivity analysis |

## Quick Reference

| Missingness % | Mechanism | Recommended Strategy |
|---------------|-----------|---------------------|
| < 5% | MCAR | Listwise deletion is usually safe; simple imputation acceptable |
| 5-25% | MCAR | Mean/median for numeric; mode or KNN for categorical |
| 5-25% | MAR | KNN imputation, MICE, or multiple imputation |
| > 25% | MCAR/MAR | Multiple imputation (MICE); consider whether the variable is salvageable |
| Any % | MNAR | Domain-driven imputation or explicit modeling of the missingness mechanism; add a "was_missing" indicator variable |
| > 50% | Any | Strongly consider dropping the variable unless it is critical to the analysis |

## Detection Methods

| Method | How It Works | Best For | Limitations |
|--------|-------------|----------|-------------|
| **IQR Rule** | Flag points below Q1 - 1.5*IQR or above Q3 + 1.5*IQR | Univariate, roughly symmetric distributions | Fails on skewed data; arbitrary multiplier |
| **Z-Score** | Flag points with |z| > 3 | Normally distributed data | Sensitive to the outliers themselves (mean and SD are affected) |
| **Modified Z-Score** | Uses median and MAD instead of mean and SD | Robust univariate detection | Still univariate |
| **Isolation Forest** | Tree-based anomaly scoring; outliers are isolated in fewer splits | Multivariate, high-dimensional data | Requires tuning contamination parameter |
| **Local Outlier Factor (LOF)** | Compares local density of a point to its neighbors | Clusters of varying density | Sensitive to k; computationally expensive |
| **Domain Rules** | Hard-coded business constraints (e.g., age must be 0-120) | Known constraints | Only catches violations of known rules |

## Decision Table: What To Do With Outliers

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Data entry error (impossible value) | **Remove or correct** | Not real data |
| Measurement error (sensor malfunction) | **Remove** and flag for data source investigation | Not representative |
| Genuine extreme value, robust method available | **Keep** | Real signal; use median-based or tree-based models |
| Genuine extreme value, sensitive method required | **Winsorize/cap** at a percentile (e.g., 1st/99th) | Preserves the observation while limiting leverage |
| Rare but valid event (fraud, equipment failure) | **Keep and study separately** | May be exactly what you are looking for |

## Quick Reference

| Algorithm | Strength | Use When |
|-----------|----------|----------|
| **Levenshtein Distance** | Catches insertions, deletions, substitutions | Short strings; names, product codes |
| **Jaro-Winkler** | Weights prefix matches more heavily | Person names (where first characters are most reliable) |
| **Soundex / Metaphone** | Phonetic matching | Names that may be spelled differently but sound alike |
| **TF-IDF + Cosine Similarity** | Handles longer text, word reordering | Addresses, descriptions, free-text fields |

## Common Mismatches and Fixes

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Dates sort incorrectly | Stored as strings in varying formats | Parse to datetime with explicit format; standardize to ISO 8601 |
| Numeric column has `object` dtype | Mixed types or stray non-numeric values (commas, currency symbols, "N/A") | Strip formatting characters, coerce with `errors='coerce'`, inspect resulting nulls |
| Categorical treated as continuous | Encoded as integers (1, 2, 3) but represent unordered categories | Cast to `category` dtype or string; never compute mean of nominal codes |
| Zip/phone codes truncated | Leading zeros dropped by numeric parsing | Store as strings |
| Boolean ambiguity | "Yes"/"No", "Y"/"N", 1/0, "True"/"False" mixed in one column | Map to canonical boolean with explicit lookup dict; reject unknown values |

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

## Recommended Order of Operations

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
