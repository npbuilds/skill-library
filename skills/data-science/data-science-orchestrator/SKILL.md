---
name: data-science-orchestrator
description: >
  Orchestrate data science analysis across the full project lifecycle. Use when the user needs
  to clean or prepare data, perform exploratory analysis, engineer features, run statistical
  tests, build or evaluate models, design causal studies, create visualizations, monitor
  deployed models, or apply responsible AI principles. Routes to the right specialist skill
  based on where the user is in the data science workflow.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Data Science Orchestrator — The Analyst

Route data science problems to the right analytical framework, coordinate multi-stage analyses, and synthesize results into actionable insights. The core capability is **bridging vague analytical questions to rigorous methodology** — taking "why did our revenue drop last quarter?" and producing a structured investigation combining EDA, causal reasoning, and clear visualization.

## Phases

### Phase 1 — Understand the Analytical Question

Before any analysis, determine what the user actually needs:

- **Question type** — Descriptive ("what happened?"), diagnostic ("why?"), predictive ("what will happen?"), prescriptive ("what should we do?"), causal ("does X cause Y?")
- **Data state** — Raw and messy, partially cleaned, analysis-ready, already modeled
- **Constraints** — Time pressure, computational resources, interpretability requirements, regulatory needs
- **Audience** — Technical team, executives, regulators, academic peer review
- **Success criteria** — What would a good answer look like? A number, a chart, a model, a recommendation?

If the user describes a situation vaguely ("analyze this data"), ask targeted questions to determine the analytical goal. If the user presents a specific technical question, validate that the chosen approach matches the question.

### Phase 2 — Classify and Route

Determine which subdomain applies. A problem often spans multiple subdomains — pick the primary and note supporting analyses.

Read `references/domain-taxonomy.md` for the full subfield map.

**Subdomain routing summary:**

| Subdomain | Activates When | Primary Concern |
|-----------|---------------|-----------------|
| Data Wrangling | Data is messy, incomplete, or needs transformation | Getting data analysis-ready |
| Statistical Analysis | Need rigorous inference, hypothesis testing, causal claims | Valid conclusions from data |
| Modeling | Need predictions, classifications, or forecasts | Accurate and reliable models |
| Visualization | Need to communicate findings or explore patterns visually | Clear, honest data communication |
| ML Engineering | Models are in production and need monitoring | Reliability and performance over time |
| Frontier | Fairness concerns, governance requirements, emerging methods | Responsible and compliant AI |

**Classification decision tree:**

1. Is the data ready for analysis, or does it need preparation?
   - Needs preparation → Data Wrangling
   - Ready → continue
2. Is the goal to **understand/infer** from data, or to **predict/automate**?
   - Understand/infer → continue to step 3
   - Predict/automate → continue to step 4
3. Is the question about **what causes what**, or about **patterns and associations**?
   - Causal → Statistical Analysis (causal-inference)
   - Associations/testing → Statistical Analysis (statistical-testing)
4. Does the data have a **temporal dimension** that matters?
   - Yes, forecasting needed → Modeling (time-series)
   - No → Modeling (model-evaluation for model selection)
5. Do results need to be **communicated visually**?
   - Yes → Visualization (chart-selection)
6. Is the model **already deployed** and needs monitoring?
   - Yes → ML Engineering (drift-detection)
7. Does the analysis involve **clinical/biomedical data**, survival analysis, or **regulatory submissions**?
   - Yes → Statistical Analysis (biostatistics)
8. Are there **fairness, bias, or regulatory** concerns?
   - Yes → Frontier (responsible-ai) — often runs in parallel with other subdomains

### Phase 3 — Formalize

Before delegating, establish the analytical frame:

1. **Data specification** — What data exists? What are the key variables? What is the unit of observation? What is the sample size?

2. **Methodology** — Based on the question type, select the appropriate approach:
   - Descriptive → EDA + visualization
   - Diagnostic → statistical testing + causal reasoning
   - Predictive → model building + evaluation
   - Causal → quasi-experimental design
   - Monitoring → drift detection + alerting

3. **Assumptions** — Document what we're assuming about the data-generating process, independence, stationarity, or causal structure. Flag assumptions that need validation.

4. **Deliverable** — What the user gets at the end:
   - A clean dataset ready for analysis
   - A statistical test result with effect size and confidence interval
   - A trained model with evaluation metrics
   - A visualization with annotations
   - A monitoring dashboard specification
   - A fairness audit report

### Phase 4 — Delegate

Route through the subdomain director first. The director handles routing to specific knowledge skills, curriculum order, and conflict resolution within its area.

**Always route through the director:**

| Subdomain | Director | Consult When |
|-----------|----------|-------------|
| Data Wrangling | `skills/data-science/data-wrangling/SKILL.md` | Data cleaning, transformation, encoding, feature engineering |
| Statistical Analysis | `skills/data-science/statistical-analysis/SKILL.md` | Hypothesis testing, causal inference, biostatistics, survival analysis |
| Modeling | `skills/data-science/modeling/SKILL.md` | Prediction, forecasting, model selection, evaluation |
| Visualization | (no director yet — route directly) | Chart selection, data communication |
| ML Engineering | (no director yet — route directly) | Production monitoring, drift detection |
| Frontier | (no director yet — route directly) | Fairness, bias, governance, responsible AI |

**Direct knowledge skill paths** (prefer routing through the director when one exists):

| Skill | Path | Activates When |
|-------|------|----------------|
| Data Cleaning | `skills/data-science/data-wrangling/data-cleaning/SKILL.md` | Missing values, outliers, deduplication, type issues |
| Feature Engineering | `skills/data-science/data-wrangling/feature-engineering/SKILL.md` | Encoding, transforms, feature creation, feature selection |
| Statistical Testing | `skills/data-science/statistical-analysis/statistical-testing/SKILL.md` | Hypothesis tests, power analysis, multiple comparisons |
| Causal Inference | `skills/data-science/statistical-analysis/causal-inference/SKILL.md` | Treatment effects, quasi-experiments, causal identification |
| Biostatistics | `skills/data-science/statistical-analysis/biostatistics/SKILL.md` | Survival analysis, clinical trial design, diagnostic tests, epidemiological measures, meta-analysis, regulatory stats |
| Model Evaluation | `skills/data-science/modeling/model-evaluation/SKILL.md` | Metrics, validation, model comparison, calibration, fairness |
| Time Series | `skills/data-science/modeling/time-series/SKILL.md` | Temporal data, forecasting, seasonality, trend analysis |
| Chart Selection | `skills/data-science/visualization/chart-selection/SKILL.md` | Choosing charts, design principles, accessibility |
| Drift Detection | `skills/data-science/ml-engineering/drift-detection/SKILL.md` | Production monitoring, drift types, retraining triggers |
| Responsible AI | `skills/data-science/frontier/responsible-ai/SKILL.md` | Fairness metrics, bias, governance, model cards |

When launching an agent for analysis, always pass:
- The formalized question from Phase 3
- The specific data context (variables, sample size, constraints)
- What deliverable the user expects

For multi-stage analyses, execute sequentially — each stage receives prior results to maintain coherence. Common multi-stage patterns:

- **Full pipeline**: data-cleaning → feature-engineering → model-evaluation → chart-selection
- **Causal study**: data-cleaning → causal-inference → chart-selection
- **Production deployment**: model-evaluation → drift-detection → responsible-ai
- **Diagnostic deep-dive**: statistical-testing → causal-inference → chart-selection

### Phase 5 — Synthesize and Present

After analysis completes:

1. **Plain-language interpretation** — Translate statistical results into business insight. "The DiD estimate is 12.3 percentage points (95% CI: 8.1-16.5, p < 0.001)" becomes "the new feature increased conversion by about 12 percentage points, and we're highly confident the true effect is between 8 and 17 points."

2. **Limitations and caveats** — Every analysis has them. Be explicit about what assumptions could be wrong, what data limitations exist, and what the analysis cannot tell us.

3. **Recommendations** — If the user asked "what should we do?", provide ranked options with the analytical justification behind each.

4. **Next steps** — What additional analysis would strengthen the conclusions? What data would we need? What experiments could we run?

5. **Cross-domain connections** — Note when the analysis connects to other domains:
   - Design: data visualization principles, dashboard design, chart aesthetics
   - Game Theory: strategic implications of findings, incentive design
   - Worldbuilding: data-driven world parameters, realistic simulations
   - Investing: performance attribution (causal-inference), macro cycles (time-series), factor validation (statistical-testing), alt data signals (feature-engineering), strategy monitoring (drift-detection), risk model calibration (model-evaluation)

## Knowledge Layer

**Always route through the orchestrator first** — don't load knowledge skills directly unless the user explicitly names one.

| Subdomain | Skills | Consult When |
|-----------|--------|-------------|
| Data Wrangling | data-cleaning, feature-engineering | Data preparation, transformation, encoding |
| Statistical Analysis | statistical-testing, causal-inference, biostatistics | Inference, hypothesis testing, treatment effects, survival analysis, clinical trials |
| Modeling | model-evaluation, time-series | Prediction, forecasting, model selection |
| Visualization | chart-selection | Data communication, chart design |
| ML Engineering | drift-detection | Production monitoring, model degradation |
| Frontier | responsible-ai | Fairness, bias, governance, compliance |

## Failure Recovery

- If the user's question doesn't map cleanly to a subdomain, ask what decision they're trying to make — the decision usually reveals the right analytical approach
- If data quality is too poor for the intended analysis, route to data-cleaning first and be transparent about limitations
- If multiple analytical approaches apply (e.g., both predictive and causal), explain the trade-off and let the user choose
- If the user rejects an analysis, ask which assumption or framing feels wrong rather than re-running the same approach
- If a skill is not yet built for the specific task, provide the best analysis possible from the orchestrator level and note what specialist depth would add

## Scope Boundaries

This orchestrator handles **data science analysis and methodology**. It does NOT:
- Write production-grade code (it provides methodology; implementation is a separate task)
- Replace domain expertise (it provides analytical frameworks; domain interpretation requires context)
- Make business decisions (it provides evidence and recommendations; decisions are human)
- Guarantee causal claims without appropriate study design (it flags when causal language is warranted vs. not)
- Serve as a statistics textbook (it provides practical decision frameworks, not theoretical proofs)
