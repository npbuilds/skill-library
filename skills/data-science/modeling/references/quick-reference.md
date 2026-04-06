# Modeling — Quick Reference


## Quick Reference

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

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| model-evaluation says complex model is more accurate but interpretability is required | Simpler model wins unless accuracy gap is large and stakes are high | Interpretability enables trust and debugging; accuracy alone isn't sufficient for most business contexts |
| time-series recommends ARIMA but model-evaluation shows tree-based model performs better on held-out data | Depends on forecast horizon — ARIMA for short-term with clear temporal structure, ML for complex multi-feature prediction | Match the model to the data-generating process, not just the error metric |
| model-evaluation says Model A wins on accuracy, Model B wins on calibration | Calibration wins for decision-making contexts; accuracy wins for ranking contexts | Well-calibrated probabilities are more valuable when decisions depend on the predicted probability itself |
| time-series says the series is non-stationary, model-evaluation says the model fits well on train data | Time series wins — non-stationarity means train performance doesn't predict future performance | Temporal validity constraints override in-sample fit |
