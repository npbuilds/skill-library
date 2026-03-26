# Model Selection Guide — Time Series Forecasting

This reference provides structured decision frameworks for choosing forecasting models based on data characteristics, requirements, and constraints.

## Decision Tree: Data Characteristics to Model

Use the following flow to narrow candidates before detailed comparison.

### Step 1: Data Size

| Observations | Series Count | Recommended Tier |
|---|---|---|
| < 50 | Single | ETS, naive methods, foundation models (zero-shot) |
| 50-500 | Single | ARIMA/SARIMA, ETS, Prophet, foundation models |
| 500-10k | Single | Full classical suite, Prophet, gradient-boosted trees |
| 10k+ | Single | All methods viable; ML and deep learning gain advantage |
| Any | 10-100 related series | VAR/VECM (if few), global ML models, foundation models |
| Any | 1000+ heterogeneous series | Foundation models (zero-shot), global deep learning (N-BEATS, TFT) |

### Step 2: Seasonality

| Seasonality Pattern | Recommended Models |
|---|---|
| None | ARIMA, ETS (simple), XGBoost, foundation models |
| Single period (e.g., yearly) | SARIMA, Holt-Winters, Prophet, any ML with calendar features |
| Multiple periods (e.g., daily + weekly + yearly) | Prophet, TBATS/MSTL, TFT, foundation models |
| Evolving seasonality (shape changes over time) | Prophet (adaptive Fourier), TFT, foundation models |
| Intermittent / lumpy demand | Croston's, SBA, INARMA, ADIDA |

### Step 3: Exogenous Variables

| Exogenous Availability | Recommended Models |
|---|---|
| None available | ARIMA, SARIMA, ETS, N-BEATS, Chronos-2, Lag-Llama |
| Available and known at forecast time | SARIMAX, Prophet, XGBoost/LightGBM, TFT, MOIRAI-2 |
| Available but NOT known at forecast time | Two-stage: forecast exogenous vars first, then use as inputs |
| Static metadata (category, location) | TFT (static covariates), global ML models with group features |

### Step 4: Forecast Horizon

| Horizon Relative to Seasonality | Guidance |
|---|---|
| Very short (< 1 seasonal cycle) | Most methods work; simpler is often better. ETS, ARIMA strong. |
| Medium (1-3 seasonal cycles) | Classical and ML both competitive. Evaluate on your data. |
| Long (> 3 seasonal cycles) | Trend estimation dominates. Prophet, TFT, foundation models handle trend extrapolation better. Widen prediction intervals aggressively. |
| Ultra-long (years ahead) | No model is reliable. Use scenario analysis, not point forecasts. |

---

## Full Model Comparison Table

| Model | Handles Trend | Handles Seasonality | Multivariate | Exogenous Vars | Probabilistic Forecasts | Compute Cost | Min Data | Interpretability |
|---|---|---|---|---|---|---|---|---|
| ARIMA | Yes (differencing) | No | No | No | Yes (analytic) | Very low | 30+ obs | High |
| SARIMA | Yes | Single period | No | No | Yes (analytic) | Low | 2+ full seasons | High |
| SARIMAX | Yes | Single period | No | Yes | Yes (analytic) | Low | 2+ full seasons | High |
| ETS (Holt-Winters) | Yes (additive/multiplicative) | Single period (add/mult) | No | No | Yes (analytic) | Very low | 2+ full seasons | Very high |
| Prophet | Yes (piecewise linear/logistic) | Multiple (Fourier) | No | Yes (regressors + holidays) | Yes (MCMC or MAP) | Low-medium | 1+ year ideally | High |
| XGBoost temporal | Via features | Via features | Via features | Yes (any) | Via quantile regression | Medium | 500+ obs recommended | Medium (SHAP) |
| N-BEATS | Yes (trend block) | Yes (seasonality block) | No (univariate) | No | Via ensemble | Medium-high (GPU) | 1000+ obs or many series | Medium (interpretable variant) |
| TFT | Yes | Yes (learned) | Yes | Yes (known future + observed past + static) | Yes (quantile outputs) | High (GPU) | 5000+ obs recommended | Medium-high (attention weights) |
| Chronos-2 | Yes | Yes | No (univariate) | No | Yes (token distribution) | Medium (GPU for large) | 0 (zero-shot) | Low |
| MOIRAI-2 | Yes | Yes | Yes (any-variate) | Yes (covariates) | Yes (mixture distribution) | Medium-high (GPU) | 0 (zero-shot) | Low |
| TimesFM | Yes | Yes | No (univariate) | No | Yes | Medium (GPU) | 0 (zero-shot) | Low |
| Lag-Llama | Yes | Yes | No (univariate) | No | Yes (distribution head) | Medium (GPU) | 0 (zero-shot) | Low |
| VAR | Via differencing | Via seasonal differencing | Yes (core design) | Via exogenous block (VARX) | Yes (analytic) | Low-medium | 50+ obs per series | High |
| VECM | Yes (cointegration) | Limited | Yes (core design) | Via exogenous block | Yes (analytic) | Low-medium | 100+ obs per series | High (economic theory) |

---

## Foundation Model Comparison

| Model | Developer | Architecture | Pre-training Data | Context Length | Zero-Shot Strength | Fine-Tuning | Probabilistic | Open Source | Notable Traits |
|---|---|---|---|---|---|---|---|---|---|
| Chronos-2 | Amazon | T5 encoder-decoder | Large-scale public + synthetic | Up to 4096 tokens | Strong on short/medium series | Supported | Yes (quantile via token bins) | Yes (Apache 2.0) | Multiple sizes (Mini to Large); tokenization of continuous values |
| MOIRAI-2 | Salesforce | Transformer with any-variate attention | LOTSA (27B observations, 9 domains) | Up to 5000 steps | Strong on multivariate and multi-frequency | Supported | Yes (mixture distributions) | Yes | Handles irregular frequencies and missing values natively |
| TimesFM | Google | Decoder-only (Transformer) | 100B+ time points (Trends, Wiki, synthetic) | Up to 2048 steps | Strong on long-horizon | Limited public fine-tune support | Yes | Partially (inference API, model weights released) | Fast inference; designed for production at scale |
| Lag-Llama | Open-source community | Llama-based decoder | Large public corpus | Up to 1024 lags | Good baseline, improves with fine-tuning | Full fine-tune support | Yes (Student-t distribution head) | Yes (MIT) | Lightweight; strong fine-tuning ecosystem; community-driven |

### When to Use Foundation Models vs. Traditional

| Scenario | Recommendation | Reasoning |
|---|---|---|
| Single well-behaved series, long history | Classical (SARIMA, ETS) | Tuned classical matches or beats zero-shot; faster, interpretable |
| Hundreds of heterogeneous series, limited per-series history | Foundation model (zero-shot) | No per-series tuning needed; amortized learning across domains |
| Cold-start (new product, new sensor) | Foundation model (zero-shot) | No historical data to fit classical models |
| High-stakes, need interpretability | Classical or Prophet | Stakeholders need to understand the forecast |
| Complex multivariate with known future inputs | TFT or MOIRAI-2 | Architecture designed for rich covariate structures |
| Rapid prototyping / baseline | Foundation model (zero-shot) | Minutes to first forecast; no feature engineering |
| Domain with strong prior knowledge (econometrics) | VECM, SARIMAX | Theory-driven specification outperforms generic models |

---

## Evaluation Metric Selection Guide

Different forecasting contexts call for different metrics. Use this guide to match your use case to the right evaluation approach.

### Point Forecast Metrics

| Metric | Formula (intuitive) | Scale-Free | Handles Zeros | Symmetric | Best Use Case |
|---|---|---|---|---|---|
| MAE | Mean of |actual - forecast| | No | Yes | Yes | Default for single-series evaluation |
| RMSE | sqrt(Mean of (actual - forecast)^2) | No | Yes | Yes | When large errors are disproportionately costly |
| MAPE | Mean of |actual - forecast| / |actual| * 100 | Yes | No (divides by zero) | No (biased toward under-forecasts) | Reporting to non-technical stakeholders on positive-valued series |
| sMAPE | Mean of |actual - forecast| / (|actual| + |forecast|) * 200 | Yes | Unstable near zero | Approximately | Slightly better MAPE variant; still problematic near zero |
| MASE | MAE / naive-seasonal-MAE | Yes | Yes | Yes | Cross-series comparison; competition benchmarking; recommended default |
| wMAPE | Sum of |actual - forecast| / Sum of |actual| | Yes | Handles sparse zeros | Yes | Retail/demand forecasting with intermittent zeros |

### Probabilistic Forecast Metrics

| Metric | What It Measures | Use When |
|---|---|---|
| CRPS | Distance between predicted CDF and observed value | Default for probabilistic forecasts; generalizes MAE |
| Pinball Loss (Quantile Loss) | Accuracy of specific quantiles (e.g., P10, P50, P90) | Evaluating prediction intervals or specific quantiles |
| Log Likelihood | Probability assigned to observed value under predicted distribution | Comparing distributional models |
| Calibration (PIT histogram) | Whether prediction intervals have correct coverage | Validating that 90% intervals contain 90% of outcomes |
| Winkler Score | Sharpness + calibration of prediction intervals | Comparing interval forecasts of fixed nominal coverage |

### Metric Selection by Context

| Context | Primary Metric | Secondary Metric | Rationale |
|---|---|---|---|
| General forecasting benchmark | MASE | RMSE | Scale-free, robust; RMSE catches catastrophic errors |
| Demand planning / inventory | wMAPE | Service level (fill rate) | Business-relevant scale; ties to actual cost |
| Energy load forecasting | RMSE | MAPE | Penalizes peaks that cause grid stress |
| Financial forecasting | MAE or RMSE | Directional accuracy | Magnitude matters; direction matters for trading |
| Probabilistic forecasts | CRPS | Calibration | Full distribution quality; reliability check |
| Intermittent demand | MASE | Precision/recall of non-zero periods | MAPE/sMAPE break down; need to assess timing separately |
| Model comparison across datasets | MASE (or relative metric) | Ranks / win rates | Need scale-independence for fair comparison |
| Reporting to executives | MAPE (if no zeros) or wMAPE | Forecast bias (mean error) | Percentage terms are intuitive; bias reveals systematic over/under |

### Backtesting Protocol

A rigorous backtest should follow this structure:

1. **Define the forecast origin(s).** Choose multiple historical cutoff dates spanning different regimes (calm periods, volatile periods, pre/post changepoints).
2. **Choose CV strategy.** Expanding window for maximum training data; sliding window if older data may be irrelevant (regime changes).
3. **Set the forecast horizon.** Match the actual production use case (e.g., if you need 7-day-ahead forecasts, evaluate at h=7, not h=1).
4. **Fit and forecast.** At each origin, fit the model on available training data only, produce forecasts for the test horizon.
5. **Aggregate metrics.** Report mean and standard deviation of metrics across origins. A model that is great on average but terrible in one window may be unacceptable.
6. **Compare to baselines.** Always include a naive baseline (seasonal naive for seasonal data, random walk for non-seasonal). If your model does not beat naive, it is not adding value.
7. **Check calibration.** For probabilistic models, verify that prediction intervals have correct empirical coverage across all test windows.
