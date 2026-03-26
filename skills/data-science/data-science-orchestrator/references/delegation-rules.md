# Delegation Rules

Rules for routing questions to the right skill when the classification is ambiguous or multi-skill.

## Ambiguous Routing

| User Says | Seems Like | Actually Route To | Why |
|-----------|-----------|-------------------|-----|
| "Analyze this data" | Everything | Ask: "What decision are you trying to make?" | Too vague — the decision reveals the method |
| "Is this significant?" | statistical-testing | statistical-testing | But clarify: statistically significant or practically significant? |
| "Predict next quarter" | model-evaluation | time-series | Temporal prediction = time series, not general ML |
| "Why did this metric change?" | statistical-testing | causal-inference + chart-selection | "Why" implies causation, not just association |
| "Clean up this dataset" | data-cleaning | data-cleaning | Straightforward, but ask about downstream use to set cleaning depth |
| "Build a model" | model-evaluation | feature-engineering → model-evaluation | Can't evaluate without features; pipeline both |
| "Is my model biased?" | responsible-ai | responsible-ai + model-evaluation | Need evaluation metrics to quantify bias |
| "Visualize these results" | chart-selection | chart-selection | But ask: what message should the chart convey? |
| "Monitor this model" | drift-detection | drift-detection | But ask: what metrics matter most in production? |
| "Which features matter?" | feature-engineering | feature-engineering + model-evaluation | Feature importance requires a model; pipeline both |

## Multi-Skill Patterns

### Pattern 1: Full Analysis Pipeline
**Trigger**: User has raw data and wants end-to-end analysis.
**Sequence**: data-cleaning → feature-engineering → model-evaluation → chart-selection
**Pass forward**: Each stage passes its output specification to the next.

### Pattern 2: Causal Investigation
**Trigger**: User asks "does X cause Y?" or "what's the effect of X?"
**Sequence**: data-cleaning → causal-inference → chart-selection
**Pass forward**: Cleaning passes data quality assessment; causal inference passes estimates and confidence.

### Pattern 3: Model Deployment
**Trigger**: User is moving a model to production.
**Sequence**: model-evaluation → responsible-ai → drift-detection
**Pass forward**: Evaluation passes baseline metrics; responsible-ai passes fairness constraints; drift-detection receives monitoring specs.

### Pattern 4: Diagnostic Deep-Dive
**Trigger**: User asks "why did metric X change?"
**Sequence**: statistical-testing → causal-inference → chart-selection
**Pass forward**: Testing identifies significant changes; causal inference attempts to identify root causes; visualization communicates findings.

### Pattern 5: Forecasting Project
**Trigger**: User needs to predict future values of a time-dependent quantity.
**Sequence**: data-cleaning → feature-engineering → time-series → chart-selection
**Pass forward**: Standard pipeline with time-series-specific feature engineering (lags, rolling stats).

### Pattern 6: Fairness Audit
**Trigger**: User needs to assess or certify model fairness.
**Sequence**: model-evaluation → responsible-ai → chart-selection
**Pass forward**: Evaluation provides performance by subgroup; responsible-ai applies fairness criteria; visualization creates the audit report.

## Priority Rules

When skills give conflicting guidance:

| Conflict | Resolution |
|----------|-----------|
| data-cleaning says drop rows, but sample size is already small | Keep rows, use imputation, flag the trade-off |
| statistical-testing says not significant, but effect size is meaningful | Report both — statistical significance ≠ practical significance |
| model-evaluation says Model A is better on accuracy, but responsible-ai flags fairness issues | Fairness constraints take priority — a biased model that's accurate is still harmful |
| causal-inference says "can't identify causal effect," but user wants a causal claim | Hold the line — report as association, not causation. Suggest study designs that would support causal claims |
| time-series recommends a complex model, but user needs interpretability | Simpler model with explanation trumps black-box accuracy, unless the accuracy gap is large and stakes are high |
| chart-selection says use a specific chart type, but data has too many categories | Aggregate or filter first, then visualize. The data drives the chart, not the other way around |

## Escalation Rules

**Escalate to the user when:**
- The analytical question is ambiguous and routing depends on the answer
- Multiple valid approaches exist and the trade-offs are meaningful
- Data quality is too poor for the intended analysis
- Results are surprising or counterintuitive — the user should validate domain interpretation
- Fairness/ethical concerns arise that require human judgment
- The analysis requires domain expertise the orchestrator lacks (medical, legal, financial specifics)

**Never escalate for:**
- Choosing between equivalent statistical tests (pick the more robust one)
- Selecting visualization details (follow chart-selection best practices)
- Deciding imputation methods when one clearly fits better (follow the decision tree)
