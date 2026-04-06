---
name: data-wrangling
description: >
  Direct the data wrangling subdomain — route data preparation questions to the right
  specialist skill, define the learning curriculum, and resolve conflicts between cleaning
  aggressiveness and information preservation. Use when the user needs to clean, transform,
  encode, or engineer features from raw data.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Data Wrangling Director

The department head for data preparation within the data-science domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts between data quality and information loss.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

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

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:

1. `data-cleaning` — fix data quality issues before any transformation
2. `feature-engineering` — transform clean data into model-ready features

This order is strict: engineering features from dirty data propagates errors. Always clean first.

**Example multi-skill question**: "Get this messy CSV ready for a classification model."
1. `data-cleaning` → handle missing values, remove duplicates, fix types, validate ranges
2. `feature-engineering` → encode categoricals, scale numerics, create interaction features, select informative features

## Curriculum Order

For learning or progressive loading:

1. **Data Cleaning** (foundation) — How to assess and fix data quality. This is prerequisite to everything else in data science. A model trained on dirty data is worse than no model at all.

2. **Feature Engineering** (application) — How to transform clean data into features that models can learn from. The art of representation — the same data, differently encoded, can make the difference between a mediocre and excellent model.

### Level Progression
- **Foundational**: Data Cleaning
- **Intermediate**: Feature Engineering
- **Advanced**: (not yet built) Data Pipeline Design, Data Versioning, Streaming Data Processing

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| data-cleaning says drop rows with missing values, but sample size is already small | Keep rows, use imputation, flag the trade-off | Information preservation beats cleanliness when data is scarce |
| feature-engineering says create many interaction features, but data-cleaning flagged high dimensionality risk | Feature engineering wins on creation, but must include selection step | Create then prune — don't preemptively limit feature space, but do reduce it before modeling |
| data-cleaning says an outlier should be removed, feature-engineering says it's an informative extreme | Keep the value, but create a binary indicator for "extreme" | Preserve information while marking the anomaly — let the model decide |
| data-cleaning recommends aggressive imputation, feature-engineering prefers missingness indicators | Use both — impute and add a "was_missing" indicator | Missingness is often informative; imputed values enable computation; combining captures both signals |

**General rule**: Information preservation > cleanliness > convention. When in doubt, keep the data and add metadata about its quality. Let downstream analysis decide what matters.

## Scope Boundaries

**This director handles**: All data preparation questions — cleaning, validation, encoding, transformation, feature creation, feature selection, dimensionality reduction.

**Escalate to the orchestrator when**:
- The question requires statistical analysis of the cleaned data (Statistical Analysis)
- The question requires building models after feature engineering (Modeling)
- The question requires visualizing data distributions or quality (Visualization)
- The question involves data fairness or representational bias (Frontier)
- The question spans multiple subdomains and needs orchestrator-level coordination
