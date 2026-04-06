# Time Series — Quick Reference


## Quick Reference

| Signal | Additive (Y = T + S + R) | Multiplicative (Y = T * S * R) |
|---|---|---|
| Seasonal amplitude | Constant over time | Grows/shrinks with the level |
| Diagnostic | Plot seasonal swings — if they stay flat, additive | If swings widen as level rises, multiplicative |
| Transform trick | Take log of multiplicative series to make it additive | Revert with exp() after modeling |

## Quick Reference

| Method | Strengths | Weaknesses | Best For |
|---|---|---|---|
| ARIMA | Well-understood theory, fast, prediction intervals | Univariate only, linear, manual order selection | Short-to-medium horizon, stationary-after-differencing data |
| SARIMA | Handles fixed-period seasonality natively | Single seasonality only, can be slow to fit at high m | Monthly/quarterly data with yearly season |
| SARIMAX | Adds exogenous regressors (weather, price, events) | Exogenous vars must be known at forecast time | When external drivers are available and forecastable |
| ETS (Holt-Winters) | Explicit trend + seasonality, additive or multiplicative | No exogenous variables, limited to single seasonality | Retail demand, inventory planning |
| VAR | Captures cross-series dynamics | All series must be stationary, curse of dimensionality | Small groups (2-5) of related economic indicators |

## Quick Reference

| Metric | Formula Intuition | Use When | Avoid When |
|---|---|---|---|
| MAE | Mean absolute error | Default for point forecasts, robust to outliers | Need to penalize large errors more |
| RMSE | Root mean squared error | Large errors are costly (e.g., capacity planning) | Outliers skew results |
| MAPE | Mean absolute percentage error | Comparing across different-scale series | Values near or at zero (explodes) |
| sMAPE | Symmetric MAPE | Avoids MAPE asymmetry | Still unstable near zero |
| MASE | Mean absolute scaled error | Scale-free, handles zero values, benchmarks against naive | Rarely — this is the most robust single metric |
| CRPS | Continuous ranked probability score | Evaluating full predictive distributions | Point-forecast-only models |

## Implementation Libraries

| Method | Python | R |
|--------|--------|---|
| ARIMA, ETS, VAR, VECM, decomposition | `statsmodels` | `forecast`, `fable` |
| Auto-ARIMA (automated order selection) | `pmdarima` | `forecast::auto.arima` |
| Prophet (trend + seasonality) | `prophet` | `prophet` |
| Unified classical + ML + neural forecasting | `darts` | `fable` + `modeltime` |
| High-performance classical models (AutoARIMA, ETS, Theta) | `statsforecast` (Nixtla) | `fable` |
| Neural forecasting (N-BEATS, TFT, PatchTST) | `neuralforecast` (Nixtla) | — |
| ML-based forecasting (XGBoost, LightGBM temporal) | `mlforecast` (Nixtla) | `modeltime` |
| scikit-learn compatible time series toolkit | `sktime` | `tsibble` + `fable` |
| AutoML for time series | `autogluon-timeseries` | — |
| Foundation: Chronos-2 (Amazon) | `chronos-forecasting` | — |
| Foundation: MOIRAI-2 (Salesforce) | `uni2ts` | — |
| Foundation: TimesFM (Google) | `timesfm` | — |
| Foundation: Lag-Llama | `lag-llama` | — |
| Temporal data structures | `pandas` (DatetimeIndex) | `tsibble` |
