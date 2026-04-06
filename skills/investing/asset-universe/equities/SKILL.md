---
name: equities
description: >
  Equity investing frameworks — factor investing, sector rotation, geographic allocation,
  earnings analysis, and market structure. Reference when analyzing stocks, building equity
  portfolios, evaluating market conditions, or understanding what drives equity returns.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Equities — The Ownership Premium

Equities are ownership claims on future cash flows. Every equity framework ultimately reduces to one question: what are the future cash flows, and what discount rate should you apply? Everything else — factors, sectors, geographies — is a lens for answering that question more precisely.

## Factor Investing Framework

Factors are persistent, well-documented sources of excess return that matter for equity selection. Each represents compensation for bearing a specific risk or exploiting a behavioral bias. The five key equity factors are:

- **Value**: Buy cheap stocks relative to fundamentals (P/E, EV/EBITDA, FCF yield). Compensates for distress risk and exploits overreaction to bad news.
- **Momentum**: Buy recent winners, sell recent losers (12-1 month return). Exploits slow information diffusion and herding behavior.
- **Quality**: Buy companies with high profitability, low leverage, and stable earnings (ROIC, gross margins, accruals). The all-weather factor — works in most environments.
- **Low Volatility**: Buy low-beta stocks. Exploits lottery preference and leverage constraints — delivers similar returns with 30-40% less risk.
- **Size**: Buy small-cap stocks. Compensates for illiquidity and neglect, but the standalone premium has been weak since the 1980s — works best combined with value or quality.

The best factor combination across all environments is value + momentum + quality. These three have low or negative correlation with each other and collectively explain most of the cross-section of equity returns. Factor performance is highly cyclical across business cycle phases — value and size favor early recovery, momentum and quality favor mid-expansion, quality and low volatility favor late cycle and recession.

For complete factor analysis including detailed definitions, historical premia, evidence, timing signals, factor crowding, smart beta implementation, and regime mapping, consult the `factor-exposure` knowledge skill in the Portfolio Construction subdomain.

## Sector Rotation Through the Business Cycle

Sectors are industry groupings that share economic sensitivity. Sector rotation is the practice of overweighting sectors positioned to outperform in the current business cycle phase.

### The Business Cycle Sector Map

**Early Cycle (recovery from recession — GDP accelerating, rates low, credit loosening)**:
- **Overweight**: Financials (steepening yield curve, improving credit quality), Consumer Discretionary (pent-up demand), Industrials (capex recovery), Real Estate (low rates, recovery in occupancy).
- **Underweight**: Utilities (expensive after defensive positioning, rising rates hurt), Consumer Staples (rotate away from defensive), Healthcare (less need for defensive positioning).
- **Why**: The most cyclical, most leveraged sectors benefit most from economic recovery. The earnings snapback is largest in sectors that were hit hardest.

**Mid Cycle (expansion — GDP growing steadily, rates normalizing, profits growing)**:
- **Overweight**: Technology (earnings growth premium, capex cycle beneficiary), Industrials (continued capex), Communication Services (advertising spend grows with economy).
- **Underweight**: Utilities (rising rates, no growth premium), Materials (commodity prices stabilizing).
- **Why**: Growth becomes the scarce resource. Investors pay up for sectors that can grow earnings above the decelerating economy-wide rate.

**Late Cycle (peak — GDP growth decelerating, rates high, margins under pressure)**:
- **Overweight**: Energy (commodity prices peak late), Materials (inflation beneficiaries), Consumer Staples (pricing power in inflation), Healthcare (defensive with growth characteristics).
- **Underweight**: Consumer Discretionary (consumers tapped out), Financials (flattening/inverting yield curve, rising credit costs), Technology (valuation compression as rates peak).
- **Why**: Inflation and margin pressure dominate. Sectors with pricing power and tangible assets outperform. The shift from growth to value begins.

**Recession (contraction — GDP falling, rates being cut, earnings declining)**:
- **Overweight**: Healthcare (inelastic demand), Utilities (regulated earnings, dividend yield), Consumer Staples (people still eat), Long-duration bonds (not equity, but the key competitor).
- **Underweight**: Financials (credit losses), Industrials (capex cuts), Consumer Discretionary (spending cuts), Energy (demand destruction).
- **Why**: Earnings resilience is the only thing that matters. Sectors with stable, non-cyclical cash flows outperform.

### Sector Rotation Pitfalls

- **Timing is hard**: The business cycle is identified with certainty only in hindsight. Leading indicators help but are noisy.
- **Sector composition changes**: "Technology" in 2000 was Cisco and Intel. "Technology" in 2024 is Apple, Microsoft, Nvidia. The sector label is the same; the exposure is completely different.
- **Concentration risk**: The S&P 500 is not an equally weighted sector portfolio. Technology + Communication Services can be 40%+ of the index. Underweighting these sectors is a massive active bet.

## Geographic Allocation

### US Equities

**Structural advantages**: Deepest capital markets, strongest rule of law, most innovative technology sector, global reserve currency, shareholder-friendly corporate governance, share buyback culture.

**When to overweight**: Dollar strength, US economic outperformance, technology-led market, risk-off (flight to quality), wide interest rate differentials favoring USD.

**When to underweight**: Extreme valuation premium vs rest of world (US CAPE at 35+ vs EAFE at 15-18 as of 2025 suggests long-term underperformance), dollar peaking, fiscal concerns, concentration risk (top 10 stocks = 35%+ of S&P 500).

**Key risk**: US exceptionalism has been priced in for a decade. The valuation gap between US and non-US equities is at historic extremes. Mean reversion is not guaranteed but is the way to bet over 10+ year horizons.

### Developed International (EAFE — Europe, Australasia, Far East)

**Structural characteristics**: More value-oriented sectors (financials, industrials, energy), higher dividend yields, lower valuation multiples, more exposure to global trade, different sector composition than US.

**When to overweight**: Dollar weakening (non-US earnings translate to more dollars), value factor outperforming, global trade expanding, European reforms or stimulus, Japan reflation.

**When to underweight**: Dollar strengthening, US growth outperformance, European political risk (elections, EU fragmentation), Japan deflation relapse.

**Key opportunity**: Japan's corporate governance revolution — Tokyo Stock Exchange reforms pushing companies to improve ROE, unwind cross-shareholdings, and return capital. Could be a decade-long tailwind.

### Emerging Markets

**Structural characteristics**: Higher GDP growth, younger demographics, commodity exposure, higher volatility, lower governance standards, FX risk, political risk, state-owned enterprise drag.

**When to overweight**: Dollar weakening (EM debt is often dollar-denominated, weak dollar eases financial conditions), commodity prices rising, China stimulus, wide valuation discount to developed markets, EM reforms.

**When to underweight**: Dollar strengthening (the dollar wrecking ball crushes EM), rising US rates (capital flows back to US), China slowdown, commodity price decline, geopolitical risk elevation.

**Key risk**: EM has consistently disappointed over the past decade. EM GDP growth has not translated to equity market returns because of dilution (new share issuance), state-owned enterprise misallocation, and governance problems. Selectivity within EM matters enormously — India and Mexico have structural tailwinds; others are more challenged.

## Small Cap vs Large Cap Dynamics

### The Small Cap Premium — Alive or Dead?

The academic small-cap premium (small stocks outperform large stocks) was documented by Fama and French in 1992. Since then, the standalone premium has been statistically insignificant. But this headline masks important nuances:

**The small-cap premium is alive within value and quality**: Small-cap value stocks and small-cap quality stocks have continued to outperform. The "death" of the small-cap premium is driven by small-cap growth and small-cap junk stocks, which are essentially lottery tickets with negative expected returns.

**Liquidity discount**: Small caps trade at a persistent valuation discount to large caps. This discount widens during stress and narrows during risk-on environments. The discount partially compensates for the higher transaction costs and lower liquidity of small-cap trading.

**The neglect factor**: Small caps with no analyst coverage, no ETF ownership, and no institutional attention outperform small caps that are widely followed. This is a pure information advantage — prices are less efficient when nobody is watching.

**When small caps outperform**: Early-cycle recovery (highest beta to economic acceleration), falling interest rates (small caps are more leveraged, so lower rates help more), and periods of domestic economic strength (small caps are more US-focused).

**When small caps underperform**: Recessions, rising rates, flight to quality, and periods when passive investing concentrates capital in large-cap index heavyweights.

## Earnings Analysis

### Earnings Quality Assessment

Not all earnings are created equal. High-quality earnings are sustainable, cash-backed, and not dependent on accounting choices.

**The Earnings Quality Hierarchy** (from highest to lowest quality):
1. **Free cash flow from recurring revenue**: Subscription businesses, long-term contracts, installed base maintenance. Predictable and cash-backed.
2. **Free cash flow from growing operations**: Revenue growth translating to proportional or better cash flow growth. Organic, not acquisition-driven.
3. **GAAP earnings backed by cash flow**: Reported earnings with FCF/net income ratio consistently above 1.0. Accounting and economics agree.
4. **GAAP earnings with moderate accruals**: Earnings growing faster than cash flow, but the gap is explained by working capital changes (inventory build for a product launch, receivables growth from expanding sales).
5. **GAAP earnings with high accruals**: Earnings growing but cash flow stagnant or declining. Red flag. Possible causes: aggressive revenue recognition, capitalizing expenses, lengthening depreciation schedules.
6. **Adjusted/non-GAAP earnings**: Companies telling you to ignore stock-based compensation, restructuring charges, or acquisition costs. Sometimes legitimate, often misleading.

**Revenue Quality Matters More Than EPS**:
- Revenue is harder to manipulate than earnings. Revenue growth is the best predictor of long-term equity returns.
- Organic revenue growth (excluding M&A and FX) is the purest signal.
- Revenue per share (adjusts for dilution from acquisitions and share issuance) is more informative than total revenue.
- Recurring revenue percentage: SaaS businesses with 90%+ recurring revenue are fundamentally different from project-based businesses with 0% recurring revenue, even if current earnings are identical.

**Margin Analysis**:
- Gross margin trend: Improving gross margins indicate pricing power or efficiency gains. Declining gross margins indicate competitive pressure or input cost inflation.
- Operating leverage: The rate at which operating income grows relative to revenue growth. High operating leverage means small revenue changes produce large earnings changes — a double-edged sword.
- Margin sustainability: Peak margins in cyclical businesses are not sustainable. The market often capitalizes peak earnings at average multiples, which is a recipe for overpaying.

### Earnings Revision Momentum

Consensus earnings estimates are systematically biased — analysts herd, anchor to management guidance, and are slow to revise. This creates a tradeable pattern:

- **Upward revision momentum**: When estimates are being revised upward, the stock usually continues to outperform. The magnitude and breadth of revisions matter — one analyst raising estimates is less meaningful than all analysts raising simultaneously.
- **Estimate dispersion**: Wide dispersion in analyst estimates (high standard deviation of estimates) indicates uncertainty. Resolution of uncertainty — in either direction — drives large price moves.
- **Earnings surprise persistence**: Companies that beat estimates tend to keep beating them. This is the SUE (Standardized Unexpected Earnings) effect, one of the most robust anomalies in finance.

## Market Cap Concentration Risk

### The Concentration Problem

As of late 2025, the top 10 stocks in the S&P 500 represent approximately 35-38% of the index by market capitalization. This is the highest concentration since the early 1970s (the Nifty Fifty era).

**Measuring Concentration**:
- **Top N weight**: The weight of the top 5, 10, or 20 stocks in the index. Simple and intuitive.
- **Herfindahl-Hirschman Index (HHI)**: Sum of squared weights. An HHI above 0.15 indicates high concentration. The S&P 500 HHI has risen from ~0.01 in the 2000s to ~0.03+ in 2025. This sounds small but represents a dramatic shift — the effective number of stocks (1/HHI) has fallen from ~100 to ~30.
- **Equal-weight vs cap-weight spread**: When the cap-weighted index significantly outperforms the equal-weighted index, it means returns are being driven by a few mega-caps rather than broad participation. This is a breadth warning signal.

**Why Concentration Matters**:
1. **Index fragility**: When 7-10 stocks drive the majority of index returns, a correction in those stocks creates an outsized index-level drawdown.
2. **Hidden sector concentration**: The Magnificent 7 are all technology-adjacent. Owning the S&P 500 means having 30%+ in de facto technology, regardless of official sector classifications.
3. **Passive investing feedback loop**: As passive investing grows, more capital flows into the largest stocks (because they have the highest index weight), which makes them larger, which increases their weight, which attracts more passive capital. This is a reflexive process that can persist for years but creates fragility.
4. **Equal-weight as an alternative**: The S&P 500 Equal Weight Index provides the same 500 stocks with equal weighting, effectively embedding a size, value, and anti-momentum tilt. Over the very long term, equal weight has outperformed cap weight, but it underperforms during mega-cap-led markets.

**Practical Implication**: Investors who own only the S&P 500 market-cap-weighted index are making an implicit bet that the largest companies will continue to grow faster than the other 490. This bet has worked brilliantly since 2013 but represents a historically extreme concentration of risk.

## Practical Framework: Equity Portfolio Construction

### Step 1: Determine Your Equity Style Budget

Decide how much active risk you want to take relative to the market. This determines whether you tilt toward factors or just own the index.

### Step 2: Apply Factor Tilts Based on Regime

Use the factor timing regime map above. In practice, a value + quality + momentum combination works across most environments.

### Step 3: Set Geographic Weights

Start with global market-cap weights (~62% US, ~27% developed ex-US, ~11% EM as of 2025). Then tilt based on:
- Relative valuation (CAPE ratios)
- Currency outlook (favor markets with weakening currencies if you are a dollar-based investor)
- Macro regime (favor EM in commodity upcycles, favor US in technology upcycles)

### Step 4: Choose Sector Tilts

Apply business-cycle sector rotation with humility. Small tilts (2-5% over/underweight) are more appropriate than large bets given the difficulty of timing.

### Step 5: Monitor Concentration and Breadth

Track the equal-weight vs cap-weight spread, market breadth (advance-decline line, percentage of stocks above 200-day moving average), and new highs vs new lows. Narrowing breadth with a rising index is a warning sign.
