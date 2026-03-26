---
name: modeling
description: >
  Direct the modeling subdomain — route prediction and forecasting questions to the right
  specialist skill, define the learning curriculum, and resolve conflicts between model
  complexity and interpretability. Use when the user needs to build, evaluate, select,
  or forecast with predictive models.
tools: Read, Glob
---

# Modeling Director

The department head for predictive modeling within the data-science domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts between accuracy and interpretability.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Model accuracy, precision, recall, F1, AUC, calibration | `model-evaluation` | Performance measurement |
| Cross-validation, train/test split, overfitting, regularization | `model-evaluation` | Validation methodology |
| Model comparison, model selection, ensemble methods | `model-evaluation` | Choosing between models |
| Forecasting, time series, seasonality, trend, ARIMA, Prophet | `time-series` | Temporal prediction |
| Stationarity, autocorrelation, lag features, rolling statistics | `time-series` | Time series diagnostics |
| Changepoint detection, anomaly detection in temporal data | `time-series` | Temporal pattern analysis |
| "Which model should I use?" | `model-evaluation` | Model selection framework |
| "Predict next quarter's revenue" | `time-series` | Temporal prediction = time series |
| "How good is my model?" | `model-evaluation` | Performance assessment |

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:

1. `time-series` — if the data has a temporal dimension, establish temporal structure first
2. `model-evaluation` — evaluate model performance and select the best approach

This order ensures temporal structure is respected before general evaluation metrics are applied. Time series models have different validation requirements (no random splitting, walk-forward validation) that model-evaluation needs to know about.

**Example multi-skill question**: "Build a demand forecasting model and tell me how confident we should be in it."
1. `time-series` → decompose the series, identify seasonality and trend, fit forecasting models
2. `model-evaluation` → evaluate forecast accuracy with appropriate temporal metrics (MAE, MAPE, coverage), compare against baselines

## Curriculum Order

For learning or progressive loading:

1. **Model Evaluation** (foundation) — How to measure model quality. Without this, you can't tell if a model is good, bad, or overfit. Every modeling task requires evaluation, so this is the universal prerequisite.

2. **Time Series** (specialization) — Temporal data requires its own methodology. Standard ML assumptions (i.i.d. data, random splits) break down. Time series teaches you why temporal structure matters and how to work with it.

### Level Progression
- **Foundational**: Model Evaluation
- **Intermediate**: Time Series
- **Advanced**: (not yet built) Deep Learning, Reinforcement Learning, AutoML, Probabilistic Modeling

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| model-evaluation says complex model is more accurate but interpretability is required | Simpler model wins unless accuracy gap is large and stakes are high | Interpretability enables trust and debugging; accuracy alone isn't sufficient for most business contexts |
| time-series recommends ARIMA but model-evaluation shows tree-based model performs better on held-out data | Depends on forecast horizon — ARIMA for short-term with clear temporal structure, ML for complex multi-feature prediction | Match the model to the data-generating process, not just the error metric |
| model-evaluation says Model A wins on accuracy, Model B wins on calibration | Calibration wins for decision-making contexts; accuracy wins for ranking contexts | Well-calibrated probabilities are more valuable when decisions depend on the predicted probability itself |
| time-series says the series is non-stationary, model-evaluation says the model fits well on train data | Time series wins — non-stationarity means train performance doesn't predict future performance | Temporal validity constraints override in-sample fit |

**General rule**: Temporal validity > accuracy metrics > model complexity. When in doubt, prefer the model you can explain and the evaluation you can trust.

## Scope Boundaries

**This director handles**: All predictive modeling questions — model building, evaluation, selection, comparison, forecasting, time series analysis, validation methodology.

**Escalate to the orchestrator when**:
- The question requires data cleaning or feature engineering before modeling (Data Wrangling)
- The question requires causal inference, not just prediction (Statistical Analysis)
- The question requires visualizing model results or forecasts (Visualization)
- The question involves model fairness or production monitoring (Frontier / ML Engineering)
- The question spans multiple subdomains and needs orchestrator-level coordination
