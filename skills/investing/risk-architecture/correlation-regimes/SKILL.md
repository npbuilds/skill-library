---
name: correlation-regimes
description: >
  Deep expertise in cross-asset correlation regimes — how correlations shift across market
  environments, why diversification fails in crises, and how to identify true diversifiers.
  Use when stress-testing portfolio diversification or analyzing regime-dependent behavior.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Correlation Regimes — When Diversification Works and When It Lies

The most dangerous assumption in portfolio construction is that correlations measured in normal times will hold in extreme times. They won't. Correlations are regime-dependent: they change based on the macro environment, liquidity conditions, and the nature of the shock. This skill covers how to think about correlations dynamically, what truly diversifies, and how to stress-test a portfolio's correlation assumptions.

The core insight: **Diversification is a fair-weather friend. It works when you don't need it and fails when you need it most.**

## Normal Regime Correlations

In a typical economic expansion with moderate inflation and accommodative monetary policy, the major cross-asset correlations look roughly like this:

| Asset Pair | Normal Correlation | Mechanism |
|-----------|-------------------|-----------|
| Stocks / Bonds | -0.2 to -0.4 (negative) | Flight to safety: when stocks fall, bonds rally as investors seek safe havens |
| Stocks / Commodities | +0.1 to +0.3 (low positive) | Both benefit from economic growth, but different drivers |
| Stocks / Gold | ~0 to -0.1 (near zero) | Gold is driven by real rates and fear, not growth |
| Bonds / Gold | +0.1 to +0.3 (low positive) | Both benefit from falling real rates and risk-off |
| Stocks / USD | -0.1 to -0.3 (weakly negative) | Dollar strength tends to tighten financial conditions |
| EM Equities / USD | -0.3 to -0.5 (negative) | Dollar strength is a headwind for EM (dollar-denominated debt) |
| Commodities / USD | -0.3 to -0.5 (negative) | Most commodities are priced in dollars; strong dollar = lower commodity prices |

These "normal" correlations form the basis of most portfolio construction. The 60/40 stock/bond portfolio relies entirely on the negative stock-bond correlation. Risk parity strategies assume these correlations are stable enough to lever up.

**The problem**: These correlations are averages across regimes. They obscure the fact that correlations shift dramatically when regimes change.

## Crisis Regime: Everything Sells Together

### The Correlation-to-One Phenomenon

In severe market crises, correlations among risk assets spike toward +1. Assets that appeared diversifying in normal times sell off together. The mechanism:

1. **Margin calls**: Leveraged investors face margin calls and must sell whatever is liquid, regardless of fundamentals
2. **Redemptions**: Fund redemptions force managers to sell across the portfolio
3. **Risk model feedback**: VaR models detect rising correlations and force deleveraging, which increases correlations further
4. **Liquidity withdrawal**: Market makers widen spreads and reduce size; liquidity evaporates across all markets simultaneously
5. **Contagion**: Selling in one asset class triggers selling in others through cross-asset risk limits

### What Holds Up in Crisis

| Asset Class | Crisis Behavior | Reliability |
|------------|----------------|-------------|
| US Treasuries (short-duration) | Rally strongly (flight to safety) | High, but failed partially in March 2020 liquidity seizure |
| Cash | Preserves value by definition | Highest — the ultimate safe haven |
| Gold | Usually rallies but can sell off initially for liquidity | Moderate — reliable in sustained crises, shaky in flash crashes |
| Long volatility (VIX calls, tail funds) | Explodes higher | High — mechanically tied to crisis |
| Managed futures / trend following | Profits from sustained moves in either direction | Moderate to high — depends on speed of move |
| Crypto | Sells off aggressively | Low — acts as a risk asset, not a hedge |
| Investment-grade corporate bonds | Sells off (credit spreads widen) | Low — not a crisis hedge despite being "bonds" |
| REITs | Sells off with or worse than equities | Low — leveraged real assets with equity-like crisis behavior |

## The 2022 Anomaly: Stocks and Bonds Fall Together

### What Happened

In 2022, the S&P 500 fell approximately 19% while the Bloomberg US Aggregate Bond Index fell approximately 13%. This simultaneous decline in both stocks and bonds was the worst year for 60/40 portfolios in decades and shattered the assumption that bonds hedge equity risk.

### Why It Happened: The Inflation Regime

The stock-bond correlation is not a law of nature — it depends on the dominant macro regime:

| Dominant Macro Driver | Stock-Bond Correlation | Mechanism |
|----------------------|----------------------|-----------|
| Growth shocks (deflation fear) | Negative (diversifying) | Bad growth news: stocks fall, bonds rally on rate cut expectations |
| Inflation shocks | Positive (non-diversifying) | Inflation up: bonds fall (rates rise), stocks fall (margins compress, multiples contract) |
| Monetary policy shocks | Positive (non-diversifying) | Central bank tightens: rates up (bonds down), liquidity withdrawn (stocks down) |
| Liquidity crisis | Positive (non-diversifying) | Everything sells for cash simultaneously |
| Geopolitical shock | Usually negative | Stocks fall on uncertainty, bonds rally on safety |

**The key insight**: From roughly 2000-2021, the dominant macro driver was growth/deflation. Central banks responded to every growth scare by cutting rates, which made bonds rally when stocks fell. The stock-bond hedge "worked" because the macro regime supported it.

In 2022, the dominant driver shifted to inflation. The Fed tightened aggressively, which hurt both stocks (higher discount rates, tighter financial conditions) and bonds (higher yields = lower prices) simultaneously. The hedge broke because the regime changed.

**Historical precedent**: Before the late 1990s, stock-bond correlations were frequently positive. The negative correlation that dominated 2000-2021 was historically unusual, driven by the specific combination of low inflation, globalization, and aggressive central bank easing.

## Why Correlations Are Regime-Dependent

### Shared Factor Exposures

Assets don't move together or apart randomly. They share exposure to underlying macro factors, and the correlation between assets depends on which factor is dominating at any given time.

### Cross-Asset Factor Framework

#### Growth Factor

Exposure to economic growth expectations. When growth accelerates, these assets benefit; when growth slows, they suffer.

| Positively Exposed | Negatively Exposed |
|-------------------|-------------------|
| Equities (especially cyclicals) | Government bonds (longer duration) |
| High-yield credit | Safe-haven currencies (JPY, CHF) |
| Commodities (industrial) | Defensive equity sectors (utilities) |
| EM equities and debt | Gold (weakly) |
| Cyclical currencies (AUD, CAD) | |

When growth is the dominant driver, all positively-exposed assets are correlated with each other and negatively correlated with negatively-exposed assets.

#### Inflation Factor

Exposure to inflation expectations. When inflation rises, these relationships shift:

| Benefits from Higher Inflation | Harmed by Higher Inflation |
|-------------------------------|---------------------------|
| Commodities (especially energy) | Government bonds (especially long duration) |
| TIPS | Growth stocks (long-duration equity) |
| Real assets (real estate, infrastructure) | Cash flows far in the future |
| Commodity currencies | Consumer discretionary |
| Energy equities | Financials (initially, then hurt by curve inversion) |

When inflation is the dominant driver, stocks and bonds become positively correlated (both fall), breaking the traditional hedge.

#### Liquidity Factor

Exposure to financial market liquidity and central bank policy.

| Benefits from More Liquidity | Harmed by Less Liquidity |
|-----------------------------|------------------------|
| All risk assets | All risk assets (in reverse) |
| Speculative growth stocks (disproportionately) | Illiquid alternatives |
| Crypto | Small-cap stocks |
| EM assets | High-yield credit |
| Private equity / venture | Leveraged strategies |

The liquidity factor is the most dangerous because it affects everything simultaneously. A liquidity withdrawal (Fed tightening, credit contraction) is the factor most likely to produce the "correlation to 1" phenomenon.

#### Dollar Factor

Exposure to US dollar strength/weakness.

| Benefits from Weaker Dollar | Harmed by Stronger Dollar |
|----------------------------|--------------------------|
| EM equities and debt | EM equities and debt (reverse) |
| Commodities (priced in USD) | US imports |
| International equities (in USD terms) | Dollar-denominated debtors |
| Gold | US dollar cash (purchasing power stable) |
| Non-USD currencies | |

Dollar is particularly important for EM and commodity-heavy portfolios. A dollar spike can cause cascading losses across multiple "diversified" positions.

## Measuring Correlation Regimes

### Rolling Correlations

The simplest approach: calculate correlations over a rolling window.

**Window selection trade-offs:**

| Window | Pros | Cons |
|--------|------|------|
| 21 days (1 month) | Captures current regime quickly | Very noisy; false signals |
| 63 days (3 months) | Reasonable balance of speed and stability | Can miss rapid regime shifts |
| 126 days (6 months) | Stable, reliable estimates | Slow to detect regime changes |
| 252 days (1 year) | Very stable | Too slow; mixes regimes |

**Practical recommendation**: Monitor both 63-day and 126-day rolling correlations. When the short window diverges significantly from the long window, a regime shift may be occurring.

### DCC-GARCH (Dynamic Conditional Correlation)

A statistical model that allows correlations to change over time in a structured way:

1. Fit GARCH models to each asset's volatility (captures time-varying volatility)
2. Model the correlation matrix as a slowly-evolving process driven by recent co-movements
3. Produces daily estimates of conditional correlations that respond to new information

**Advantages over rolling windows:**
- Uses all available data, not just the window
- Captures the speed of correlation changes
- Provides statistically rigorous estimates

**Limitations:**
- Assumes correlations change smoothly (may miss sudden regime breaks)
- Computationally intensive for large portfolios
- Model specification matters (results can be sensitive to assumptions)

### Regime-Switching Models

Explicitly model the market as switching between discrete states:

- **State 1** (normal): Low volatility, "normal" correlations, growth-driven
- **State 2** (crisis): High volatility, elevated correlations, liquidity-driven
- **State 3** (inflation): Moderate volatility, positive stock-bond correlation, inflation-driven

The model estimates:
- Which state we're currently in (with probability)
- The correlation matrix within each state
- The transition probabilities between states

**This is the most powerful framework** because it explicitly acknowledges that a single correlation matrix is inadequate. The portfolio should be stress-tested under each regime's correlation assumptions, not just the average.

## The Diversification Illusion

### Why "Diversified" Portfolios Aren't

A portfolio holding US stocks, international stocks, REITs, high-yield bonds, and EM debt looks diversified. In a normal environment, correlations are moderate and the portfolio behaves as expected.

In a crisis:
- US stocks, international stocks, and EM debt: all sell (growth factor)
- REITs: sell even more (growth + leverage + liquidity factors)
- High-yield bonds: sell (growth + credit + liquidity factors)

The "diversified" portfolio has a single effective position: **long growth + long liquidity**. The apparent diversification across asset classes was an illusion created by normal-environment correlations.

### The Diversification Test

For each pair of assets in your portfolio, ask:

1. **What factor do they share?** If both are positively exposed to the same factor (growth, liquidity, dollar), they will correlate in regimes where that factor dominates.

2. **In the worst 5% of months for Asset A, what happened to Asset B?** If Asset B also lost money in most of those months, it's not diversifying when diversification matters.

3. **Is the correlation stable across environments?** Use regime-switching or conditional analysis, not unconditional correlations.

4. **Would I still call this "diversified" if a 2008-style event happened tomorrow?** If the honest answer is no, you're not diversified — you're just long the same factor through different instruments.

## True Diversifiers

Assets that genuinely diversify a portfolio must have one or more of these properties:
- Negative or zero correlation with risk assets **in crisis environments** (not just on average)
- Returns driven by a different factor than the dominant portfolio factor
- Structural features that produce gains during stress (convexity, trend-following)

### Managed Futures / Trend Following

- Strategy: systematically go long assets in uptrends and short assets in downtrends, across commodities, currencies, bonds, and equities
- Crisis behavior: tends to profit from sustained moves, whether up or down
- Correlation with equities: near zero on average, often negative in sustained equity drawdowns
- Mechanism: crisis periods produce strong trends (flight to safety, forced selling), which trend followers capture
- Limitation: poor performance in choppy, trendless markets; can whipsaw in V-shaped recoveries

### Long Volatility

- Strategy: explicitly long volatility through options, variance swaps, or volatility ETPs
- Crisis behavior: profits dramatically when volatility spikes (VIX doubles or triples in crashes)
- Correlation with equities: strongly negative in crash environments
- Mechanism: volatility is mechanically linked to market declines (leverage effect, panic)
- Limitation: bleeds during calm markets (theta decay); expensive to maintain permanently

### Gold

- Behavior: partial safe haven — usually rises during sustained crises but can sell off in initial liquidity panics
- Correlation with equities: near zero on average, weakly negative in crises
- Driven by: real interest rates (inversely), fear/uncertainty, dollar weakness
- Limitation: not reliable in short, sharp crashes (March 2020: gold initially sold off)
- Best role: structural portfolio allocation (5-10%) for long-term inflation hedge and partial crisis hedge

### Cash

- The ultimate diversifier: zero correlation with everything by definition
- Provides optionality: the ability to buy distressed assets after a crash
- Psychological benefit: portfolio with cash is easier to hold through drawdowns
- Cost: opportunity cost in normal times (forgone returns)
- Optimal allocation: enough to survive a crisis and deploy opportunistically, but not so much that you miss bull markets

## The Liquidity Trap: ETF-Driven Correlated Selling

### The Mechanism

The growth of ETFs and passive investing has created a new source of correlated selling:

1. ETFs hold baskets of securities, including ones with very different fundamentals
2. When ETF shares are redeemed, the authorized participant must sell the entire basket
3. This forces selling of all securities in the ETF simultaneously, regardless of individual merit
4. In a crisis, massive ETF redemptions create indiscriminate selling across all holdings
5. Securities that should be uncorrelated become correlated through the ETF mechanism

### Implications for Diversification

- **Index membership matters**: Being in a major index means you're exposed to index-driven selling in crises
- **Factor ETFs concentrate**: A "value ETF" holds stocks that are correlated by factor, not just by basket. Selling concentrates in the factor, not the individual stock.
- **Liquidity mismatch**: High-yield bond ETFs trade intraday but hold bonds that trade by appointment. In a crisis, the ETF can trade at a discount to NAV, and redemptions force selling of the most liquid bonds first, leaving the illiquid dregs.
- **Correlation injection**: ETFs inject correlation into otherwise uncorrelated securities simply by holding them in the same wrapper

## Practical Framework: Stress-Testing Correlation Assumptions

### Step 1 — Map Factor Exposures

For each position in the portfolio, identify exposures to the four key factors:

| Position | Growth | Inflation | Liquidity | Dollar |
|----------|--------|-----------|-----------|--------|
| [Name] | [+/-/0] | [+/-/0] | [+/-/0] | [+/-/0] |

Count the total portfolio exposure to each factor. If the portfolio is long growth in 80% of positions, it's not diversified — it's a concentrated growth bet.

### Step 2 — Compute Regime-Conditional Correlations

Don't use the full-sample correlation matrix. Instead, compute correlations under different regimes:

| Regime | Define By | Use For |
|--------|-----------|---------|
| Normal (growth-driven) | VIX < 20, positive GDP growth | Baseline portfolio optimization |
| Inflation shock | CPI acceleration, bond yields rising | Test stock-bond correlation break |
| Liquidity crisis | VIX > 30, credit spreads widening | Test "correlation to 1" scenario |
| Dollar spike | DXY up > 10% in 6 months | Test EM and commodity exposure |

### Step 3 — Run Scenario Analysis

For each regime, apply the regime-specific correlation matrix to the portfolio:

1. What is the portfolio's expected drawdown under each regime?
2. Which positions contribute most to drawdown in each regime?
3. Does any position act as a diversifier in ALL regimes? (These are the true diversifiers)
4. Is there a regime where the portfolio is catastrophically concentrated?

### Step 4 — Identify Diversification Gaps

After the scenario analysis, you'll see where the portfolio is vulnerable:

| Gap | Fix |
|-----|-----|
| All positions correlated in liquidity crisis | Add cash, managed futures, or long volatility |
| Stock-bond hedge fails in inflation regime | Add commodities, TIPS, or reduce bond duration |
| EM and commodities both fail in dollar spike | Hedge dollar exposure or reduce EM/commodity weight |
| No position benefits from rising volatility | Add explicit long-volatility allocation |

### Step 5 — Implement True Diversifiers

Based on the gaps identified, add assets that provide genuine crisis diversification:

| Diversifier | Allocation | Purpose | Cost |
|------------|-----------|---------|------|
| Managed futures / trend following | 5-15% | Crisis alpha, trend capture | Fees + tracking error in calm markets |
| Long volatility allocation | 2-5% | Explicit crash protection | Carry cost (theta) |
| Gold | 5-10% | Inflation hedge, partial safe haven | Opportunity cost (no yield) |
| Cash | 5-15% | Ultimate safety, optionality | Opportunity cost |
| Short-term TIPS | 5-10% | Inflation protection with safety | Low yield in normal times |

### Step 6 — Monitor for Regime Shifts

Set up monitoring for regime changes that would alter correlation assumptions:

| Signal | Implication | Action |
|--------|------------|--------|
| Stock-bond correlation turns positive (63-day rolling) | Possible shift to inflation regime | Reduce bond hedge reliance, add inflation hedges |
| VIX crosses above 25 from below | Possible crisis regime entry | Validate hedges are in place, prepare to deploy cash |
| Credit spreads widen > 100bps in 30 days | Liquidity tightening | Reduce illiquid positions, increase cash |
| DXY rallies > 5% in 30 days | Dollar regime stress | Check EM and commodity exposure |
| Rolling correlations among portfolio positions spike | Loss of diversification | Identify which factor is driving; hedge or reduce |

### Decision Summary

```
Start
  |
  v
Map every position's factor exposures (growth, inflation, liquidity, dollar)
  |
  v
Is the portfolio concentrated in one or two factors? --Yes--> Diversify factor exposure
  |
  No
  v
Compute regime-conditional correlations (normal, crisis, inflation, dollar)
  |
  v
Stress test portfolio under each regime
  |
  v
Catastrophic loss in any regime? --Yes--> Add true diversifiers for that regime
  |
  No
  v
Set up regime-shift monitoring signals
  |
  v
Review quarterly and after any major market event
```

## Related Skills

- **`asset-allocation`** (Portfolio Construction) — consult when designing diversification strategy; allocation decisions must account for regime-conditional correlations, not just unconditional averages
- **`tail-risk`** (Risk Architecture) — consult when assessing crisis behavior where correlations spike toward one and standard diversification assumptions fail catastrophically
- **`macro-cycles`** (Regime Intelligence) — consult when understanding why correlations are regime-dependent; the dominant macro driver (growth, inflation, liquidity) determines which assets move together

## Cross-Domain Connections

- **Data-science/modeling/time-series**: Regime-switching models (HMM, Markov-switching GARCH, DCC-GARCH) are advanced time-series methodology. Detecting when correlation regimes have shifted uses the same structural break and change-point detection methods from the time-series skill.
