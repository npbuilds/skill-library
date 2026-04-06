---
name: time-series
description: >
  Time series analysis and forecasting methods from classical statistics to foundation models.
  Reference when decomposing temporal patterns, selecting forecasting models, handling seasonality,
  evaluating forecast accuracy, or deciding between classical and modern approaches. Use when
  the data has a temporal dimension and the goal is understanding or predicting trends.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Time Series — The Temporal Lens

Time series data is ordered by time, and that ordering is the signal. Unlike tabular ML where rows are exchangeable, the position of each observation carries information about trend, cycles, and seasonality. Respecting temporal structure in every stage — decomposition, modeling, and evaluation — is the single most important discipline in this domain.

This skill covers the full pipeline: decomposing raw series into interpretable components, transforming data into a form models can learn from, choosing between classical statistical methods and modern ML/foundation model approaches, and evaluating forecasts honestly.

## 1. Decomposition

Every time series can be viewed as the combination of trend (long-run direction), seasonality (repeating patterns at fixed intervals), and residual (what remains). The first modeling decision is how these combine.

**Additive vs. Multiplicative:**

| Signal | Additive (Y = T + S + R) | Multiplicative (Y = T * S * R) |
|---|---|---|
| Seasonal amplitude | Constant over time | Grows/shrinks with the level |
| Diagnostic | Plot seasonal swings — if they stay flat, additive | If swings widen as level rises, multiplicative |
| Transform trick | Take log of multiplicative series to make it additive | Revert with exp() after modeling |

**STL Decomposition** (Seasonal-Trend using LOESS) is the workhorse. It handles additive decomposition with robust estimation, tolerates outliers, and lets you control the smoothness of trend and seasonal components independently. Use `period` to specify the seasonal cycle length. For multiplicative patterns, apply log first, then STL, then exponentiate.

**Decision guide:** Plot the raw series. If the seasonal "envelope" fans out, use multiplicative (or log + additive). If roughly parallel, use additive. When uncertain, compare residual variance from both and pick the one with smaller, more random residuals.

## 2. Stationarity & Transforms

Most classical models assume stationarity — constant mean, constant variance, and autocovariance that depends only on lag, not on time. Non-stationary data produces spurious correlations and unreliable parameter estimates.

**Testing for stationarity:**

- **ADF (Augmented Dickey-Fuller):** Null hypothesis is unit root (non-stationary). p < 0.05 suggests stationary.
- **KPSS:** Null hypothesis is stationary. p < 0.05 suggests non-stationary.
- Run both. If they disagree, the series likely needs one round of differencing.

**Transform decision sequence:**

1. Variance increasing with level? Apply **log transform** or **Box-Cox** (finds optimal power transform automatically).
2. Still has a trend after transform? Apply **first differencing** (subtract previous value).
3. Still has seasonal pattern? Apply **seasonal differencing** (subtract value from one full period ago).
4. Re-run ADF/KPSS to confirm stationarity.

Most real-world series need at most d=1 (first difference) and D=1 (seasonal difference). If you need d=2, reconsider whether a simpler transform was missed.

## 3. Classical Methods

Classical methods remain the right default for univariate series under ~10k observations with clear seasonal structure. They are fast, interpretable, and produce calibrated prediction intervals out of the box.

**Model identification via ACF/PACF:**
- ACF tails off, PACF cuts off at lag p: AR(p)
- ACF cuts off at lag q, PACF tails off: MA(q)
- Both tail off: ARMA(p,q) — use information criteria (AICc) to select order

**`auto_arima`** (from `pmdarima` in Python or `forecast` in R) automates order selection by searching over (p,d,q)(P,D,Q)m combinations and minimizing AICc. Start here for ARIMA family models.

| Method | Strengths | Weaknesses | Best For |
|---|---|---|---|
| ARIMA | Well-understood theory, fast, prediction intervals | Univariate only, linear, manual order selection | Short-to-medium horizon, stationary-after-differencing data |
| SARIMA | Handles fixed-period seasonality natively | Single seasonality only, can be slow to fit at high m | Monthly/quarterly data with yearly season |
| SARIMAX | Adds exogenous regressors (weather, price, events) | Exogenous vars must be known at forecast time | When external drivers are available and forecastable |
| ETS (Holt-Winters) | Explicit trend + seasonality, additive or multiplicative | No exogenous variables, limited to single seasonality | Retail demand, inventory planning |
| VAR | Captures cross-series dynamics | All series must be stationary, curse of dimensionality | Small groups (2-5) of related economic indicators |

## 4. Modern ML Approaches

ML methods shine when you have large datasets, complex nonlinear patterns, or many exogenous features. They trade interpretability for flexibility.

**Gradient-boosted trees (XGBoost/LightGBM):** Treat forecasting as supervised regression. Engineer lag features (y_{t-1}, y_{t-7}, ...), rolling statistics (mean, std over windows), calendar features (day-of-week, month, holiday flags), and any exogenous variables. These models handle missing values, mixed types, and feature interactions naturally. Downside: no built-in uncertainty quantification (use quantile regression or conformal prediction), and feature engineering is manual.

**Prophet:** Designed for business forecasting at scale. Decomposes into trend (with changepoints), seasonality (Fourier terms, multiple periods), and holidays. Excellent for daily data with weekly + yearly seasonality and known events. Less effective on high-frequency (sub-hourly) or very short series.

**N-BEATS:** Pure deep learning for univariate forecasting. Uses backward/forward residual connections to decompose the forecast. Competitive with ensembles on M4 competition data. Requires meaningful training set size (thousands of series or long history).

**Temporal Fusion Transformers (TFT):** Attention-based architecture that handles static covariates, known future inputs, and observed past inputs simultaneously. Provides interpretable attention weights showing which features and time steps matter. Strong on complex multivariate problems. Needs substantial data and GPU compute.

**When ML beats classical:** Large datasets (100k+ observations or many related series), many exogenous features, nonlinear relationships, cross-series learning opportunities. **When classical wins:** Small data, single univariate series, need for interpretability, when quick iteration matters more than marginal accuracy.

## 5. Foundation Models (2025-2026)

The largest paradigm shift in time series since Box-Jenkins. Pre-trained on billions of time points across domains, these models perform zero-shot forecasting — point them at a new series with no training and get competitive forecasts.

**Key models:**
- **Chronos-2 (Amazon):** Tokenizes time series values, uses a T5-based architecture. Multiple sizes from 20M to 710M parameters. Strong zero-shot performance, especially on short series where classical methods struggle with limited history.
- **MOIRAI-2 (Salesforce):** Any-variate (handles multivariate natively), any-frequency. Uses mixture distributions for probabilistic forecasts. Particularly strong on irregular and multi-frequency data.
- **TimesFM (Google):** Decoder-only architecture pre-trained on 100B+ time points from Google Trends, Wiki, and synthetic data. Fast inference, good on long-horizon forecasts.
- **Lag-Llama:** Open-source, builds on the Llama architecture with lag-based tokenization. Fully fine-tunable, strong community ecosystem.

**Decision framework for foundation models:**
- **Zero-shot** (no domain data needed): Use when you have limited history (< 100 observations), cold-start problems, or need quick baselines across many heterogeneous series.
- **Few-shot adaptation** (provide a handful of examples): When you have domain-specific patterns not well-represented in pre-training data.
- **Fine-tuning** (train on your data): When you have substantial domain data (10k+ observations) and the zero-shot baseline underperforms a tuned classical model by a meaningful margin.

Foundation models do not obsolete classical methods. For a single well-behaved univariate series with long history, a well-tuned SARIMA or ETS often matches or beats a foundation model. The value is in scale (thousands of heterogeneous series), cold-start, and reducing practitioner effort.

See `references/model-selection-guide.md` for detailed comparison tables and decision trees.

## 6. Evaluation

Time series evaluation must respect temporal ordering. Random cross-validation is invalid because it leaks future information into training.

**Cross-validation strategies:**

- **Expanding window:** Train on [1..t], test on [t+1..t+h]. Increment t, repeat. Most realistic but computationally expensive.
- **Sliding window:** Train on [t-w..t], test on [t+1..t+h]. Fixed training window, slides forward. Use when the data-generating process changes over time (regime shifts).

**Metric selection:**

| Metric | Formula Intuition | Use When | Avoid When |
|---|---|---|---|
| MAE | Mean absolute error | Default for point forecasts, robust to outliers | Need to penalize large errors more |
| RMSE | Root mean squared error | Large errors are costly (e.g., capacity planning) | Outliers skew results |
| MAPE | Mean absolute percentage error | Comparing across different-scale series | Values near or at zero (explodes) |
| sMAPE | Symmetric MAPE | Avoids MAPE asymmetry | Still unstable near zero |
| MASE | Mean absolute scaled error | Scale-free, handles zero values, benchmarks against naive | Rarely — this is the most robust single metric |
| CRPS | Continuous ranked probability score | Evaluating full predictive distributions | Point-forecast-only models |

**MASE is the recommended default.** It compares your model's error to a naive seasonal forecast, is scale-independent, handles zeros, and is symmetric. CRPS is the gold standard when you have probabilistic forecasts.

## 7. Seasonality & Special Patterns

**Multiple seasonalities:** Many real series have overlapping cycles — e.g., hourly electricity demand has daily (24h), weekly (168h), and yearly (8760h) patterns. SARIMA handles only one. Use Prophet (Fourier terms for each period), TBATS, or MSTL for multiple seasonalities.

**Holiday and event effects:** Encode known future events (holidays, promotions, outages) as binary or categorical exogenous variables. Prophet has built-in holiday handling. For tree-based models, add them as features.

**Changepoints:** Structural breaks where the trend slope shifts. Prophet detects these automatically. For classical methods, use CUSUM or Bai-Perron tests. Ignoring changepoints biases long-horizon forecasts.

**Intermittent demand:** Series with many zeros (spare parts, rare events). Standard methods fail. Use **Croston's method** or its SBA (Syntetos-Boylan Approximation) variant, which separately model the inter-arrival time and the demand size.

**Irregular time series:** Unevenly spaced observations. Resample to regular intervals (with appropriate fill/interpolation), or use methods that handle irregular spacing natively (Gaussian processes, some foundation models like MOIRAI-2).

## Common Mistakes

1. **Random train/test split.** Shuffling time series data leaks future information. Always split chronologically. This is the single most common error in applied forecasting.
2. **Ignoring seasonality.** Residuals with seasonal patterns mean the model is systematically wrong at certain times. Always check residual ACF for remaining seasonal spikes.
3. **Overfitting to recent data.** Recency bias leads to models that perform well on the last few months but fail on the next regime shift. Evaluate across multiple time windows.
4. **Missing prediction intervals.** A point forecast without uncertainty is incomplete. Decision-makers need ranges. Every production forecast should include at least 80% and 95% intervals.
5. **Using MAPE with near-zero values.** MAPE divides by actual values — near zero, it explodes to infinity. Use MASE or MAE instead.
6. **Over-differencing.** Applying d=2 or D=2 when d=1 suffices introduces spurious negative autocorrelation and degrades forecast quality. Check stationarity tests after each round.

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

**Recommended starting stack (Python):** `statsmodels` + `pmdarima` for classical methods, `darts` or Nixtla's `statsforecast`/`neuralforecast`/`mlforecast` for a unified API across method families, `chronos-forecasting` for zero-shot foundation model forecasting.

## When This Applies

- Forecasting demand, revenue, or resource usage over time
- Anomaly detection on temporal streams (monitoring, IoT sensors)
- Capacity planning with seasonal patterns
- Economic and financial modeling (stock, macro indicators)
- Any problem where "what will happen next?" depends on what happened before
- Signal processing and sensor data analysis
- Cold-start forecasting across many heterogeneous series (foundation models)

## Cross-Domain Connections

- **Investing/regime-intelligence/macro-cycles**: Macro cycle positioning is time-series analysis applied to economic indicators — leading indicator decomposition, structural break detection (regime shifts), and trend/cycle separation are the same methods used in different language.
- **Investing/risk-architecture/correlation-regimes**: Regime-switching models (HMM, Markov-switching GARCH) are time-series models that detect when the correlation structure of assets has fundamentally changed. DCC-GARCH for dynamic correlation monitoring is advanced time-series methodology.
