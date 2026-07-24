# Data Science Domain Taxonomy

A map of the field organized by analytical purpose, with connections to the skill library.

## Primary Division

Data science work divides by the question being asked:

```
Data Science
├── Descriptive Analytics
│   "What happened?" — Summarization, aggregation, visualization
│   Skills: data-cleaning, chart-selection
│
├── Diagnostic Analytics
│   "Why did it happen?" — Root cause analysis, statistical testing, causal inference
│   Skills: statistical-testing, causal-inference, chart-selection
│
├── Predictive Analytics
│   "What will happen?" — Forecasting, classification, regression
│   Skills: feature-engineering, model-evaluation, time-series
│
├── Prescriptive Analytics
│   "What should we do?" — Optimization, decision support, causal reasoning
│   Skills: causal-inference, model-evaluation, responsible-ai
│
└── Operational Analytics
    "Is it still working?" — Monitoring, drift detection, quality assurance
    Skills: drift-detection, responsible-ai
```

## Full Subfield Map

### 1. Data Wrangling (Preparation)

**Data Cleaning**
Missing value handling, outlier detection, deduplication, type validation, schema enforcement.
Skill: `data-cleaning` | Status: Active

**Feature Engineering**
Encoding, transforms, feature creation, feature selection, automated feature engineering.
Skill: `feature-engineering` | Status: Active

**Data Integration** (not yet built)
ETL/ELT pipelines, data joining strategies, entity resolution, data lake organization.

**Data Quality** (not yet built)
Data contracts, Great Expectations-style validation, data lineage, observability.

### 2. Statistical Analysis (Inference)

**Hypothesis Testing**
Parametric and non-parametric tests, power analysis, effect sizes, multiple comparisons, Bayesian inference.
Skill: `statistical-testing` | Status: Active

**Causal Inference**
Quasi-experimental methods, treatment effects, DAGs, sensitivity analysis.
Skill: `causal-inference` | Status: Active

**Bayesian Analysis** (not yet built)
Prior specification, posterior inference, hierarchical models, model comparison via Bayes factors.

**Survey Methodology** (not yet built)
Sampling design, weighting, questionnaire design, response bias.

### 3. Modeling (Prediction)

**Model Evaluation**
Metrics, validation strategies, model comparison, calibration, fairness auditing.
Skill: `model-evaluation` | Status: Active

**Time Series**
Temporal decomposition, forecasting, classical methods, foundation models.
Skill: `time-series` | Status: Active

**Supervised Learning** (not yet built)
Algorithm selection (trees, linear models, neural networks, SVMs), hyperparameter tuning, ensemble methods, AutoML.

**Unsupervised Learning** (not yet built)
Clustering (k-means, DBSCAN, hierarchical), dimensionality reduction (PCA, UMAP, t-SNE), anomaly detection.

**Deep Learning** (not yet built)
Architectures (CNN, RNN, Transformer), transfer learning, fine-tuning, training dynamics.

**NLP** (not yet built)
Text preprocessing, embeddings, classification, NER, summarization, RAG patterns.

### 4. Visualization (Communication) — has a director as of 2026-07

Director: `visualization` | Status: Active

**Chart Selection**
Message-first chart design, type selection, accessibility (WCAG 2.2, Wong palette), anti-patterns.
Skill: `chart-selection` | Status: Active

**Interactive Dashboards**
Rendering by data volume (SVG/Canvas/WebGL-WebGPU), 2026 framework selection (ECharts 6, Recharts/Visx/Nivo, deck.gl 9, Vega-Lite 6), linked views, progressive disclosure, streaming, embedded analytics.
Skill: `interactive-dashboards` | Status: Active

**Data Storytelling**
Narrative spine, annotation-as-message, guided reveal & pacing, scrollytelling (Scrollama), context adaptation.
Skill: `data-storytelling` | Status: Active

**Geospatial / Animation / Notebook-EDA visualization** (not yet built)
Map-based encoding, transitions-as-explanation, notebook-native exploratory plots.

### 5. ML Engineering (Production)

**Drift Detection**
Data drift, concept drift, monitoring architecture, retraining triggers.
Skill: `drift-detection` | Status: Active

**MLOps** (not yet built)
CI/CD for ML, model registry, pipeline orchestration, experiment tracking, versioning.

**Model Serving** (not yet built)
Batch vs real-time, containerization, API design, latency optimization, A/B testing infrastructure.

### 6. Frontier (Emerging & Governance)

**Responsible AI**
Fairness metrics, bias mitigation, governance frameworks, model cards, transparency.
Skill: `responsible-ai` | Status: Active

**LLM-Augmented Analytics** (not yet built)
Agentic RAG, text-to-SQL, LLM-as-analyst patterns, prompt engineering for data tasks.

**Synthetic Data** (not yet built)
Generation techniques, privacy guarantees, validation, use cases.

## Cross-Subfield Relationships

```
Data Wrangling ─feeds→ All other subfields
               (garbage in, garbage out)

Statistical Analysis ←validates→ Modeling
                     (are model improvements statistically significant?)

Causal Inference ←constrains→ Modeling
                 (prediction ≠ causation; different methods needed)

Visualization ←communicates→ All other subfields
              (every analysis needs to be communicated)

ML Engineering ←monitors→ Modeling
               (deployed models need ongoing quality assurance)

Responsible AI ←audits→ Modeling + Statistical Analysis
               (fairness and governance apply across the pipeline)
```

## The Data Science Lifecycle

```
Problem Definition
    ↓
Data Collection → Data Wrangling (clean, transform, engineer features)
    ↓
Exploratory Analysis (statistical testing, visualization)
    ↓
Modeling (train, evaluate, select) ←→ Feature Engineering (iterate)
    ↓
Deployment → Monitoring (drift detection, responsible AI audits)
    ↓
Insights → Communication (visualization, storytelling)
    ↓
Decision → (loop back to problem definition for next question)
```
