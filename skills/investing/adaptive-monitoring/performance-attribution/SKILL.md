---
name: performance-attribution
description: >
  Performance attribution frameworks for decomposing investment returns into their sources.
  Reference when analyzing what drove portfolio performance, distinguishing skill from luck,
  selecting appropriate benchmarks, or conducting risk-adjusted performance measurement.
---

# Performance Attribution — The Diagnostic Engine

Understanding WHAT drove returns is more important than knowing the returns themselves. A portfolio that gained 15% from unintended factor bets is more dangerous than one that gained 8% from deliberate, repeatable decisions. Attribution is the bridge between outcomes and process — without it, you cannot learn, improve, or distinguish luck from skill.

## The Core Question

Every attribution analysis answers: "Of my total return, how much came from each decision I made?"

Decisions decompose into:
- **Which assets to hold** (allocation)
- **Which securities within those assets** (selection)
- **When to trade** (timing)
- **How much risk to take** (sizing)

If you cannot attribute returns to specific decisions, you cannot repeat successes or avoid repeated failures.

## Brinson-Fachler Attribution Model

The foundational framework for portfolio attribution. Decomposes active return (portfolio minus benchmark) into three effects.

### Setup

Define:
- `w_p(i)` = portfolio weight in asset class i
- `w_b(i)` = benchmark weight in asset class i
- `r_p(i)` = portfolio return in asset class i
- `r_b(i)` = benchmark return in asset class i
- `R_b` = total benchmark return

### Allocation Effect

**What it measures**: The contribution from being overweight or underweight in the right asset classes.

```
Allocation_i = (w_p(i) - w_b(i)) * (r_b(i) - R_b)
```

Interpretation:
- Positive when you overweighted asset classes that outperformed the total benchmark
- Positive when you underweighted asset classes that underperformed the total benchmark
- This isolates the VALUE OF YOUR ASSET CLASS BETS, independent of security selection

Example: You held 40% equities vs benchmark 30%. Equities returned 12% vs total benchmark 8%. Allocation effect = (0.40 - 0.30) * (0.12 - 0.08) = +0.40%. Your overweight in equities added 40bps.

### Selection Effect

**What it measures**: The contribution from picking better or worse securities within each asset class.

```
Selection_i = w_b(i) * (r_p(i) - r_b(i))
```

Interpretation:
- Positive when your securities within an asset class outperformed that asset class's benchmark
- Uses BENCHMARK weights to isolate pure selection skill from allocation decisions
- This answers: "Were you a good stock picker within each bucket?"

Example: Within your equity allocation (benchmark weight 30%), your stocks returned 14% vs equity benchmark 12%. Selection effect = 0.30 * (0.14 - 0.12) = +0.60%. Your stock picking added 60bps.

### Interaction Effect

**What it measures**: The cross-product of allocation and selection — did you overweight asset classes where you also picked well?

```
Interaction_i = (w_p(i) - w_b(i)) * (r_p(i) - r_b(i))
```

Interpretation:
- Positive when you overweighted asset classes where you also outperformed in selection
- Often small but can be significant when allocation and selection are correlated
- Some practitioners fold this into either allocation or selection; purists keep it separate

Example: You overweighted equities by 10% AND your equity picks beat the equity benchmark by 2%. Interaction = 0.10 * 0.02 = +0.20%.

### Total Active Return

```
Total Active Return = Sum of (Allocation_i + Selection_i + Interaction_i) for all i
```

In our example: 0.40% + 0.60% + 0.20% = 1.20% total active return.

### Brinson-Fachler Limitations

- Assumes discrete asset class buckets — blurry for cross-asset strategies
- Single-period model — multi-period linking requires geometric attribution
- Doesn't capture timing within periods
- Doesn't account for derivatives or leverage
- Currency effects need a separate overlay attribution

### Multi-Period Linking

Single-period Brinson doesn't compound properly. Three approaches:

1. **Carino method**: Logarithmic smoothing — most theoretically sound
2. **Menchero method**: Optimized linking that preserves additivity
3. **Frongello method**: Sequential linking — simplest, slightly less precise

For most practical purposes, monthly attribution with quarterly linking is sufficient.

## Factor Attribution

Decomposes returns into systematic factor exposures and idiosyncratic alpha. More granular than Brinson because it asks: "Which RISK FACTORS drove your returns?"

### The Core Decomposition

```
Portfolio Return = Risk-Free Rate + Beta * Market Premium + Factor Tilts + Alpha
```

- **Market beta**: Return from simply being exposed to the market
- **Factor tilts**: Return from systematic exposure to known risk factors
- **Alpha**: The residual — return unexplained by any known factor

### Factor Model Hierarchy

**CAPM (1 factor)**:
```
R_p - R_f = alpha + beta * (R_m - R_f) + epsilon
```
Simplest model. Everything unexplained by market beta is "alpha." Problem: most "alpha" is actually factor exposure.

**Fama-French 3-Factor**:
```
R_p - R_f = alpha + b1*(Market) + b2*(SMB) + b3*(HML) + epsilon
```
- SMB (Small Minus Big): size premium — small caps tend to outperform large caps
- HML (High Minus Low): value premium — high book-to-market tends to outperform low
- Explains roughly 90% of diversified portfolio return variation

**Carhart 4-Factor**:
```
Adds: b4*(MOM)
```
- MOM (Momentum): Winners keep winning, losers keep losing over 3-12 month horizons
- Important because momentum is one of the strongest documented anomalies

**Fama-French 5-Factor**:
```
Adds: b4*(RMW) + b5*(CMA)
```
- RMW (Robust Minus Weak): profitability premium — profitable firms outperform
- CMA (Conservative Minus Aggressive): investment premium — conservative investors outperform aggressive ones
- Note: adding these two factors makes HML (value) largely redundant

**Other Factors Used in Practice**:
- Low volatility / minimum variance
- Quality (composite of profitability, earnings stability, low leverage)
- Liquidity premium
- Carry (yield-seeking across asset classes)
- Dividend yield

### Interpreting Factor Attribution

Example output:
```
Total Return:          +12.0%
  Market Beta:          +8.5%  (70.8%)
  Size (SMB):           +0.5%  ( 4.2%)
  Value (HML):          -0.3%  (-2.5%)
  Momentum (MOM):       +2.1%  (17.5%)
  Alpha (residual):     +1.2%  (10.0%)
```

Reading: "Your outperformance was 70% from market exposure, 18% from momentum tilt, and 10% genuine alpha. Your value underweight cost you 25bps."

### Factor Attribution Pitfalls

- **Factor zoo problem**: With 400+ published factors, you can always find one that "explains" returns
- **Regime dependence**: Factor premiums vary enormously across market regimes
- **Multicollinearity**: Factors correlate with each other — attribution splits are somewhat arbitrary
- **Look-ahead bias**: Using factors constructed with future data invalidates the analysis
- **Survivorship bias**: Only factors that "worked" get published — reality is noisier

## Risk Attribution

Shifts focus from "where did returns come from?" to "where is risk coming from?"

### Marginal Contribution to Risk (MCR)

**Definition**: How much total portfolio risk changes when you add a tiny bit more of position i.

```
MCR_i = w_i * Cov(r_i, r_portfolio) / StdDev(r_portfolio)
```

Key properties:
- MCR values sum to total portfolio volatility
- MCR can be negative (hedging positions reduce total risk)
- MCR changes as correlations shift — it's dynamic, not static

### Percentage Contribution to Risk (PCR)

```
PCR_i = MCR_i / Total_Portfolio_Volatility
```

Interpretation: "Position X is 5% of portfolio value but contributes 12% of portfolio risk."

When PCR >> weight: the position is risk-inefficient — using more than its share of risk budget.
When PCR << weight: the position is risk-efficient or hedging — valuable diversifier.

### Risk Budgeting

**The framework**: Allocate a risk budget to each position or strategy, then monitor actual risk consumption.

Steps:
1. Set total portfolio risk target (e.g., 10% annual volatility)
2. Allocate risk budgets to each sleeve (e.g., equities get 7%, bonds get 2%, alternatives get 1%)
3. Monitor actual risk contribution vs budget
4. Rebalance or hedge when actual exceeds budget

**Risk budget breach triggers**:
- Position contributes >150% of its risk budget — investigate immediately
- Correlation spike causes risk reallocation — rerun risk decomposition
- VaR exceeds limit — reduce exposure or hedge

### Tracking Error Decomposition

For benchmarked portfolios: What explains the deviation from benchmark returns?

```
Tracking Error = StdDev(R_portfolio - R_benchmark)
```

Decompose by:
- **Active asset allocation**: different weights than benchmark
- **Active security selection**: different securities than benchmark
- **Active factor tilts**: different factor exposures than benchmark
- **Residual**: unexplained tracking error

Target tracking error depends on mandate:
- Index fund: <50bps
- Enhanced index: 50-200bps
- Active core: 200-500bps
- High conviction: 500-1000bps+

## Performance Measurement Ratios

### Return Measures

**Time-Weighted Return (TWR)**:
- Eliminates the impact of cash flows (deposits/withdrawals)
- Use for: Evaluating manager skill — "How did the manager perform with whatever capital was available?"
- Calculation: Geometrically link sub-period returns between each cash flow
- Industry standard for manager comparison (GIPS compliant)

**Money-Weighted Return (IRR)**:
- Includes the impact of cash flow timing
- Use for: Evaluating investor experience — "What return did MY money actually earn?"
- Better for private equity, real estate, and illiquid investments
- Captures the cost of bad timing (buying high, selling low)

**When they diverge**: TWR and IRR diverge when cash flows correlate with returns. If you added money before a drawdown, your IRR is worse than TWR. This is common — investors chase performance.

### Risk-Adjusted Ratios

**Sharpe Ratio**:
```
Sharpe = (R_p - R_f) / StdDev(R_p)
```
- Measures excess return per unit of total risk
- Assumes normal distribution — fails for strategies with fat tails or skew
- Benchmarks: <0.5 poor, 0.5-1.0 acceptable, 1.0-2.0 good, >2.0 exceptional (or suspicious)
- Can be gamed: sell deep OTM puts to harvest premium, looks great until it doesn't

**Sortino Ratio**:
```
Sortino = (R_p - R_f) / Downside_Deviation
```
- Only penalizes downside volatility — upside volatility is good
- Better than Sharpe for asymmetric strategies (options, trend-following, venture)
- Downside deviation = StdDev of returns below a minimum acceptable return (often 0 or R_f)

**Max Drawdown and Calmar Ratio**:
```
Max Drawdown = Largest peak-to-trough decline
Calmar = Annualized Return / |Max Drawdown|
```
- Max drawdown is the single most psychologically relevant risk metric
- Calmar tells you: "How much return am I getting per unit of worst-case pain?"
- Benchmarks: Calmar >0.5 acceptable, >1.0 good, >2.0 exceptional

**Information Ratio**:
```
IR = (R_p - R_benchmark) / Tracking_Error
```
- Alpha per unit of active risk — the active manager's Sharpe ratio
- Measures the EFFICIENCY of active bets
- Benchmarks: >0.5 good, >1.0 exceptional, sustained >1.0 is extremely rare

### Consistency Measures

**Batting Average**:
```
Batting Average = Periods Outperforming / Total Periods
```
- Measures consistency of outperformance
- 55-60% is genuinely good — even elite managers lose 40%+ of periods
- Monthly batting average >60% sustained over 5+ years is exceptional

**Win/Loss Ratio**:
```
Win/Loss = Average Gain in Up Periods / Average Loss in Down Periods
```
- Measures the ASYMMETRY of your outcomes
- A low batting average can be profitable with a high win/loss ratio (trend-following: 35% hit rate but 3:1 win/loss)
- Combines with batting average for expected value: E[return] = (BA * Avg Win) - ((1-BA) * Avg Loss)

**Gain/Pain Ratio**:
```
Gain/Pain = Sum of All Positive Returns / |Sum of All Negative Returns|
```
- >1.0 means total gains exceed total losses
- Simpler than Sortino but captures the same intuition

## Benchmark Selection

The most important and most frequently wrong decision in performance evaluation. A bad benchmark makes all attribution meaningless.

### Appropriate Benchmark Criteria

A valid benchmark must be:

1. **Investable**: Can you actually buy the benchmark? (Custom factor portfolios often fail this)
2. **Representative**: Does it reflect the portfolio's investment universe and strategy?
3. **Measurable**: Can you get accurate, timely return data?
4. **Unambiguous**: Is the composition clearly defined and known in advance?
5. **Specified in advance**: The benchmark should be set BEFORE the measurement period, not selected afterward to make results look good

### Why S&P 500 Is Wrong for Most Portfolios

Most individual investors hold a mix of:
- US equities (large, mid, small)
- International equities (developed, emerging)
- Bonds (government, corporate, municipal)
- Real estate (REITs or direct)
- Cash and alternatives

Benchmarking this against the S&P 500 is wrong because:
- It's 100% US large-cap equity — ignores bonds, international, small-cap, alternatives
- A 60/40 portfolio will always "underperform" the S&P 500 in bull markets and "outperform" in bear markets — this tells you nothing about skill
- It creates behavioral pressure to abandon diversification

### Benchmark Selection Guide

| Portfolio Type | Appropriate Benchmark |
|---------------|----------------------|
| US large cap equity | S&P 500 or Russell 1000 |
| US total equity | Russell 3000 or CRSP Total Market |
| Global equity | MSCI ACWI or FTSE All-World |
| US aggregate bonds | Bloomberg US Aggregate Bond Index |
| 60/40 balanced | 60% MSCI ACWI / 40% Bloomberg Global Agg |
| Multi-asset with alts | Custom blend reflecting target allocation |
| Absolute return / hedge fund | Cash + spread (e.g., T-bills + 300bps) |
| Private equity | Public market equivalent (PME) with illiquidity premium |

### Custom Benchmark Construction

When no standard benchmark fits:
1. Start with the policy portfolio (target allocation)
2. Assign an index to each asset class sleeve
3. Weight indices by policy weights
4. Rebalance the benchmark on the same schedule as the policy
5. Document the methodology — it must be replicable

## Luck vs Skill

The most uncomfortable truth in investing: it takes a LOT of data to distinguish skill from luck.

### The Statistics of Outperformance

Given a manager with true alpha of `a` and tracking error of `TE`:
```
Years needed for 95% confidence that alpha > 0:
  n = (1.96 * TE / a)^2
```

Example: A manager with 2% alpha and 6% tracking error needs:
```
n = (1.96 * 6 / 2)^2 = (5.88)^2 = ~35 years
```

Thirty-five years to be statistically confident the outperformance is real. Most manager tenures are 3-5 years.

### Implications

- A 3-year track record is nearly meaningless for distinguishing skill from luck
- Even a 10-year record is insufficient unless alpha is large relative to tracking error
- Information ratio (IR) is the signal-to-noise ratio — higher IR means faster skill detection
- This is why process matters more than outcomes over short periods

### What to Look for Instead of Short-Term Returns

1. **Process consistency**: Does the manager do what they say they'll do?
2. **Factor exposures**: Are returns explainable by intentional, articulated factor bets?
3. **Drawdown behavior**: Does the manager manage risk during stress, or freeze?
4. **Capacity awareness**: Does the manager close to new assets before strategy degrades?
5. **Alignment of interests**: Does the manager eat their own cooking (invested in the fund)?
6. **Fee reasonableness**: After fees, is the expected alpha positive?

## Monthly Attribution Review Checklist

A practical framework for conducting systematic attribution analysis.

### Step 1 — Return Decomposition (15 minutes)
- [ ] Calculate total portfolio return (TWR) for the period
- [ ] Calculate benchmark return for the same period
- [ ] Compute active return (portfolio minus benchmark)
- [ ] Run Brinson-Fachler attribution: allocation, selection, interaction
- [ ] Identify the top 3 contributors and top 3 detractors

### Step 2 — Factor Analysis (15 minutes)
- [ ] Run factor regression against chosen factor model
- [ ] Compare factor exposures to intended tilts
- [ ] Flag any UNINTENDED factor exposures (style drift)
- [ ] Calculate residual alpha — is it positive, negative, or noise?

### Step 3 — Risk Review (15 minutes)
- [ ] Calculate current portfolio volatility and compare to target
- [ ] Compute marginal contribution to risk for each position
- [ ] Check: any position contributing >2x its weight in risk?
- [ ] Review correlation matrix — any surprising correlation changes?
- [ ] Calculate current max drawdown and compare to drawdown budget

### Step 4 — Benchmark Integrity (5 minutes)
- [ ] Confirm benchmark is still representative of the strategy
- [ ] Check for benchmark reconstitution effects (index additions/deletions)
- [ ] Note any benchmark drift that may warrant a benchmark change

### Step 5 — Synthesis and Action (10 minutes)
- [ ] Summarize: What worked, what didn't, and WHY
- [ ] Separate controllable factors from uncontrollable factors
- [ ] Decide: Any position changes warranted?
- [ ] Document the decision rationale for future attribution reviews
- [ ] Flag anything that warrants a thesis review or rebalancing trigger

### Red Flags That Demand Immediate Attention

- Unintended factor exposure >20% of active risk
- Single position contributing >30% of portfolio risk
- Tracking error exceeding mandate by >50%
- Max drawdown exceeding 75% of drawdown budget
- Attribution showing returns from unintended sources for 3+ consecutive months
