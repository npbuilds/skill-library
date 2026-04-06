---
name: asset-allocation
description: >
  Strategic and tactical asset allocation frameworks — from classic models (60/40, risk parity, endowment)
  to regime-based positioning, glide path design, liability-driven investing, and rebalancing methodology.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Asset Allocation — The Foundation of Every Portfolio

Asset allocation is the single most important investment decision. The Brinson-Hood-Beebower study showed that allocation explains over 90% of return variation across time. Security selection and market timing matter at the margins. Allocation is the structure.

This skill covers the full spectrum: strategic allocation (the long-term baseline), tactical allocation (deviations based on regime and opportunity), and the mechanical frameworks for implementing and maintaining allocation targets.

---

## Part 1: Strategic vs Tactical Allocation

### Strategic Allocation — The Baseline

Strategic asset allocation (SAA) is the long-term, policy-level portfolio mix. It represents the investor's baseline risk posture, set without regard to current market conditions. SAA reflects three inputs:

**Risk tolerance.** How much drawdown can the investor withstand without abandoning the plan? This is both psychological (can they sleep?) and financial (do they need the capital?).

- Conservative: max drawdown tolerance 10-15%. Heavy fixed income, short duration.
- Moderate: max drawdown tolerance 20-30%. Balanced equity/bond mix.
- Aggressive: max drawdown tolerance 40-50%+. Equity-dominated, alternatives, illiquid.

**Time horizon.** Longer horizons permit more equity exposure because:
- Equity mean reversion: over 20+ year periods, equities have never produced negative real returns (US data)
- Recovery time: the investor has time to wait out drawdowns
- Human capital: younger investors have an implicit bond-like asset (future earnings) that supports equity allocation

**Goals and liabilities.** What is the money for? Retirement in 30 years looks different from a house down payment in 3 years. Each goal may warrant its own sub-portfolio with a distinct allocation (goal-based investing).

### Tactical Allocation — The Deviation

Tactical asset allocation (TAA) is the deliberate, temporary deviation from the strategic baseline. TAA says: "Given where we are in the cycle, I want to overweight or underweight certain asset classes relative to my long-term targets."

**How much flexibility?** Typical tactical bands are +/- 5% per major asset class. A 60/40 investor might go 55/45 or 65/35 based on regime, but not 80/20. Wider bands (up to +/- 10%) are appropriate for sophisticated investors with strong conviction and risk management.

**TAA decision framework:**

1. Identify the current macro regime (see Regime-Based Allocation below)
2. Assess valuation: are asset classes cheap or expensive relative to history?
3. Assess momentum: are trends supporting or opposing the regime thesis?
4. Set tactical tilts within defined bands
5. Define trigger to revert to strategic weights (time-based or signal-based)

**The evidence on TAA:** Most investors who attempt tactical allocation underperform those who stay strategic. The problem is behavioral — they time entries and exits poorly. TAA works only with a systematic, rules-based approach and the discipline to follow the signals.

### The Spectrum

```
Pure Strategic ←——————————————————————→ Pure Tactical
   "Set and forget"          "Active macro overlay"
   Rebalance mechanically    Adjust based on regime
   Lowest cost               Higher cost, higher complexity
   Works for most people     Works for disciplined systematists
```

Most investors should be 80% strategic, 20% tactical. Let the allocation do the work. Use tactical tilts sparingly and only with defined rules.

---

## Part 2: Classic Allocation Frameworks

### The 60/40 Portfolio

**Structure:** 60% equities (typically broad US or global), 40% bonds (typically intermediate-term investment grade).

**History and rationale:** The 60/40 has been the default balanced portfolio for institutional and individual investors for decades. The logic is straightforward — equities provide growth, bonds provide stability and income. Historically, stocks and bonds have been negatively correlated during equity sell-offs (flight to quality), making bonds an effective diversifier.

**Performance:** From 1926-2021, the 60/40 delivered roughly 8.8% annualized nominal returns with a max drawdown of approximately 35% (vs 50%+ for 100% equities). The Sharpe ratio has been competitive with all-equity portfolios.

**Why it broke in 2022:** The 60/40 lost approximately 17% in 2022, its worst year since 2008 and one of its worst ever. The mechanism:

- The Fed hiked rates aggressively to fight inflation
- Rising rates crushed bond prices (duration losses)
- Rising rates also crushed equity valuations (higher discount rates)
- Stocks AND bonds fell together — the negative correlation broke
- The diversification benefit of bonds evaporated precisely when it was needed most

**The lesson:** 60/40 works when inflation is low and stable. When inflation is the primary risk, bonds fail as a hedge because central bank tightening hits both stocks and bonds. In inflationary regimes, the 60/40 needs supplementation (TIPS, commodities, real assets).

**When 60/40 still works:** Disinflationary growth shocks (recessions without inflation). In a pure growth scare, bonds rally as rates fall, offsetting equity losses. This was the dominant regime from 1982-2020.

### The Endowment Model (Swensen/Yale)

**Structure:** Heavy allocation to alternatives — typically 50-70% in private equity, venture capital, real assets, hedge funds, and absolute return strategies. Only 20-30% in traditional public equities and 5-10% in fixed income.

**Rationale:** David Swensen's insight was that long-term investors (endowments have infinite horizons) should harvest the illiquidity premium. Assets that are hard to buy and sell — private equity, venture, timberland, real estate — offer excess returns precisely because most investors can't or won't accept illiquidity.

**Yale's track record:** The Yale Endowment returned 13.7% annualized from 1985-2021, dramatically outperforming a 60/40 benchmark. The key was early and deep commitment to alternatives when few institutions were doing so.

**Why most investors can't replicate it:**

- Access: The best private equity and venture funds are capacity-constrained. Yale gets into top-quartile funds due to relationships; retail investors get median or worse.
- Illiquidity: Most individuals need liquidity that endowments don't. Locking up 50%+ of a personal portfolio is inappropriate for anyone who might need the capital.
- Fee drag: Alternative investments charge 2-and-20 or similar. Median PE/VC performance net of fees is mediocre. Only top-quartile managers consistently add value.
- Complexity: Managing a multi-alternative portfolio requires a dedicated investment office. Individual investors lack the resources.

**Takeaway for individual investors:** The principle — diversify beyond stocks and bonds, accept illiquidity for premium — is sound. The implementation must be scaled: perhaps 10-20% in alternatives (liquid alts, listed REITs, listed private equity) rather than 60%.

### All-Weather / Risk Parity (Dalio/Bridgewater)

**Structure:** Allocate so that each asset class contributes equal risk to the portfolio, rather than equal capital. Typically results in roughly equal risk from four quadrants:

| Environment | Asset Class |
|------------|-------------|
| Growth rising | Equities, corporate credit, commodities |
| Growth falling | Nominal bonds, inflation-linked bonds |
| Inflation rising | Commodities, TIPS, EM |
| Inflation falling | Nominal bonds, equities |

**Mechanics:** Because bonds have lower volatility than equities, equal risk contribution requires more capital in bonds (and often leverage). A typical risk parity portfolio might be 30% equities, 55% bonds, 15% commodities — but with 1.5-2x leverage on the bond allocation to equalize risk contribution.

**Why it works (in theory):** No one knows which regime is coming next. By balancing risk across all four environments, the portfolio performs reasonably regardless of which regime materializes. It's not trying to predict — it's trying to be robust.

**Risk parity criticisms:**

- Leverage risk: Borrowing to lever up bonds introduces margin risk and borrowing costs
- Correlation regime dependence: When stock-bond correlation flips positive (2022), diversification benefit vanishes
- Complexity: Requires continuous rebalancing, leverage management, and risk measurement
- 2022 problem: Same as 60/40 but amplified by leverage — when everything correlates, risk parity fails

**When risk parity shines:** Environments where growth and inflation shocks alternate unpredictably. Over long periods with varied regimes, risk parity has delivered competitive risk-adjusted returns with lower max drawdowns than equity-heavy portfolios.

### Permanent Portfolio (Harry Browne)

**Structure:** 25% each in four asset classes:

| Asset | Purpose | Shines When |
|-------|---------|-------------|
| Stocks | Growth and prosperity | Economic expansion |
| Long-term bonds | Deflation protection | Falling rates, recession |
| Gold | Inflation protection | Rising inflation, crisis |
| Cash/T-bills | Stability and optionality | Rising rates, uncertainty |

**Philosophy:** Simplicity as a feature. The permanent portfolio rejects the premise that investors can predict regimes or time markets. By holding equal weights in four assets that respond to different environments, the portfolio always has something working.

**Track record:** From 1972-2023, the permanent portfolio delivered roughly 8% annualized with remarkably low volatility and drawdowns under 15%. It has never had a catastrophic year because at least one quadrant is always performing.

**Strengths:**

- Extreme simplicity — anyone can implement it with 4 funds
- Low maintenance — rebalance annually
- Psychologically robust — shallow drawdowns reduce panic selling
- No prediction required

**Weaknesses:**

- Suboptimal in strong bull markets (only 25% equities)
- Gold allocation is controversial (no yield, behavioral volatility)
- Cash drag in low-rate environments (25% earning near zero for a decade)
- Does not harvest the equity risk premium fully

### Golden Butterfly

**Structure:** A modification of the permanent portfolio:

- 20% Total stock market
- 20% Small-cap value
- 20% Long-term bonds
- 20% Short-term bonds
- 20% Gold

**Rationale:** The golden butterfly adds a small-cap value tilt (the most robust equity factor premium) and splits the bond allocation between long and short duration. This captures more of the equity risk premium while maintaining the permanent portfolio's regime diversification.

**Track record:** Historically outperforms the permanent portfolio by 0.5-1% annually with similar drawdown characteristics. The small-cap value tilt adds return without proportionally adding risk due to its low correlation with large-cap growth.

---

## Part 3: Risk Parity Deep Dive

### Equal Risk Contribution (ERC)

The core principle: each asset class should contribute equally to total portfolio risk (measured by volatility or, more precisely, marginal contribution to portfolio variance).

**The math intuition:** If you have two assets — equities (vol 16%) and bonds (vol 4%) — and you want equal risk contribution, you need roughly 4x as much capital in bonds as in equities. A 20% equity / 80% bond split would give approximately equal risk contribution before accounting for correlation.

**With correlation:** Correlation adjusts the marginal contributions. When stock-bond correlation is negative, bonds actually reduce total portfolio risk, requiring even more bond allocation for equal marginal contribution.

### Why Bonds Need Leverage

Equal risk contribution with unlevered allocations produces a portfolio with very low expected returns (because it's bond-dominated). The insight of risk parity is to lever up the low-volatility assets:

1. Start with equal risk contribution weights (e.g., 25% equity, 75% bonds)
2. Apply leverage to the whole portfolio (e.g., 1.5x) or just the bond leg
3. Result: more absolute return per unit of risk than either stocks or bonds alone

**Leverage sources:** Futures (most common — embedded leverage via margin), repo agreements (institutional), total return swaps. Each has different costs and risks.

**Leverage cost:** The cost of leverage is approximately the short-term interest rate. When rates are near zero, leverage is nearly free and risk parity shines. When rates are 5%, leverage costs eat into the premium.

### Risk Parity Variants

**Naive risk parity:** Weight inversely proportional to volatility. Simple, but ignores correlation.

**Full ERC:** Solve for weights where marginal risk contribution equals 1/N for each of N assets. Requires a covariance matrix estimate.

**Hierarchical risk parity (HRP):** Uses hierarchical clustering to build a tree of asset similarities, then allocates inversely to cluster-level volatility. More robust to estimation error in the covariance matrix.

**Risk parity across risk factors:** Instead of balancing across asset classes, balance across risk factors (growth, inflation, liquidity, credit). More conceptually pure but harder to implement.

---

## Part 4: Regime-Based Allocation

### The Four Regimes

Every macro environment can be mapped to a combination of growth trajectory and inflation trajectory. This creates four regimes, each favoring different asset classes:

### Regime 1: Growth Rising + Inflation Falling ("Goldilocks")

**Environment:** The ideal. Economic expansion with disinflation. Central banks are accommodative or neutral. Credit is expanding. Corporate earnings are growing.

**Asset class positioning:**
- Overweight: equities (especially growth and tech), corporate credit (spread tightening), EM equities
- Neutral: short-duration bonds, real estate
- Underweight: gold, commodities, cash, long-duration treasuries (opportunity cost)

**Factor positioning:** Growth > value, momentum works, low vol underperforms, quality is neutral.

**Historical examples:** 1995-1999, 2013-2019, mid-2023 to early 2024.

### Regime 2: Growth Rising + Inflation Rising ("Reflation")

**Environment:** Strong growth with rising prices. Commodity demand surging. Wages rising. Central banks beginning to tighten but behind the curve.

**Asset class positioning:**
- Overweight: commodities (energy, industrial metals), value equities, short-duration bonds, TIPS
- Neutral: broad equities, real estate
- Underweight: long-duration bonds (rate risk), growth equities (rate sensitivity), investment-grade credit

**Factor positioning:** Value > growth, momentum rotates to cyclicals, quality underperforms, size premium is strong.

**Historical examples:** 2003-2007, H2 2021 into 2022.

### Regime 3: Growth Falling + Inflation Falling ("Deflation/Recession")

**Environment:** Economic contraction with falling prices. Flight to quality. Central banks cutting rates. Credit contracting.

**Asset class positioning:**
- Overweight: long-duration treasuries (rate cuts drive capital gains), quality equities (defensive), gold (fear premium)
- Neutral: investment-grade credit (spread widening offset by rate decline)
- Underweight: equities (especially cyclicals), commodities, high-yield credit, EM

**Factor positioning:** Quality dominates, low vol outperforms, value gets crushed (value traps in recession), momentum crashes.

**Historical examples:** 2008-2009, March 2020, 2001.

### Regime 4: Growth Falling + Inflation Rising ("Stagflation")

**Environment:** The worst quadrant. Economic contraction with rising prices. Central banks are trapped — can't cut (inflation) or hike (recession). No good answers.

**Asset class positioning:**
- Overweight: gold, TIPS, cash/T-bills, managed futures (trend following profits from extended moves)
- Neutral: short-duration bonds, commodity producers (but be selective)
- Underweight: equities (margin compression + multiple contraction), long-duration bonds (inflation), corporate credit (default risk + rate risk)

**Factor positioning:** Nothing works cleanly. Quality is the least bad factor. Value works if you avoid deep cyclicals. Momentum works if trends persist. Low vol provides relative protection.

**Historical examples:** 1973-1974, 1979-1981, parts of 2022.

### Regime Identification Signals

Identifying the current regime requires monitoring both real-time and forward-looking indicators:

**Growth signals:**
- ISM Manufacturing PMI: above 50 = expansion, below 50 = contraction. Direction matters more than level.
- Initial jobless claims: rising claims signal growth deterioration. Below 250K = strong, above 400K = trouble.
- Credit conditions: Senior Loan Officer Survey (SLOOS), high-yield spreads, bank lending standards.
- Earnings revisions: breadth of upward vs downward revisions. Leading indicator of profit cycle.
- Conference Board Leading Economic Index (LEI): composite of 10 leading indicators.

**Inflation signals:**
- Breakeven inflation rates (TIPS spread): market-implied inflation expectations.
- Commodity price trends: broad commodity indices (GSCI, BCOM) as real-time inflation proxies.
- Wage growth: Employment Cost Index (ECI), Atlanta Fed wage tracker.
- ISM Prices Paid: leading indicator of PPI and CPI.
- M2 money supply growth: leading inflation indicator with 12-18 month lag.

### Regime Transition Rules

Regimes don't switch overnight. Transitions provide the most valuable positioning opportunities:

1. **Confirm the transition:** Require at least 3 of 5 signals to confirm a regime change. Single indicators produce false signals.
2. **Adjust in stages:** Move allocation in 2-3 steps over 1-3 months. Don't make the full tactical shift immediately.
3. **Maintain strategic anchors:** Never deviate more than +/- 10% from strategic weights, even in strong regime conviction.
4. **Set reversion triggers:** Define what data would signal the regime has ended. Without exit rules, tactical shifts become permanent drift.

---

## Part 5: Liability-Driven Investing (LDI)

### Core Concept

Match the duration, cash flow timing, and inflation sensitivity of assets to the investor's liabilities (future obligations). The portfolio's job is not to maximize return — it's to ensure liabilities can be met.

**Who uses LDI:**
- Pension funds: match assets to pension obligations
- Insurance companies: match assets to claim reserves
- Individuals with known future expenses: college tuition, home purchase, retirement income needs

### LDI Mechanics

**Duration matching:** If liabilities have a duration of 15 years, the bond portfolio should also have a duration of roughly 15 years. This immunizes the portfolio against interest rate movements — if rates rise, both asset and liability values fall proportionally.

**Cash flow matching:** For near-term liabilities (1-5 years), use individual bonds or bond ladders that mature when the cash is needed. This eliminates reinvestment risk entirely.

**Surplus optimization:** The assets above and beyond what's needed to match liabilities (the surplus) can be invested more aggressively. This creates a two-bucket approach:
- Bucket 1 (LDI): Bonds matched to liabilities — conservative, duration-matched
- Bucket 2 (Return-seeking): Equities, alternatives — growth-oriented

### Individual Application

Even individual investors can apply LDI principles:

1. **Identify future liabilities:** Retirement income needs, education expenses, major purchases
2. **Match near-term liabilities (0-5 years):** Bond ladder, CDs, money market
3. **Match medium-term liabilities (5-15 years):** Duration-matched bond portfolio, TIPS for inflation-linked liabilities
4. **Invest surplus for growth:** Equities, alternatives for obligations 15+ years away

---

## Part 6: Glide Path Design

### The Concept

A glide path defines how allocation changes over time as the investor's time horizon shortens. The most common application is target-date funds (lifecycle funds).

### Standard Glide Path

Age 25: 90% equity, 10% bonds
Age 35: 80% equity, 20% bonds
Age 45: 70% equity, 30% bonds
Age 55: 60% equity, 40% bonds
Age 65: 45% equity, 55% bonds
Age 75: 35% equity, 65% bonds

### "To" vs "Through" Retirement

**"To" glide path:** Reaches its most conservative allocation AT retirement. Assumes the investor will spend down the portfolio.

**"Through" glide path:** Continues to de-risk for 10-15 years AFTER retirement, reaching most conservative allocation around age 75-80. Rationale: a 65-year-old has a 20-30 year horizon — still long enough to justify meaningful equity exposure.

**Evidence favors "through":** Vanguard, Fidelity, and academic research suggest that maintaining 40-50% equity through early retirement improves outcomes, particularly against longevity risk (outliving your money).

### Dynamic Glide Paths

Standard glide paths only adjust for age. A dynamic glide path also adjusts for:

- **Wealth level:** If you've already saved enough to meet all goals, de-risk regardless of age
- **Market valuation:** If equities are extremely expensive, accelerate de-risking
- **Personal circumstances:** Job loss, health events, inheritance — adjust the glide path for life events
- **Sequence of returns risk:** The 5 years before and after retirement are the "danger zone" where bad returns are most damaging. Consider extra conservatism during this window.

---

## Part 7: Rebalancing

### Why Rebalance

Portfolios drift from target allocations as assets generate different returns. A 60/40 portfolio after a strong equity year might be 68/32. Rebalancing returns it to target, which:

1. Maintains the intended risk profile
2. Forces a "sell high, buy low" discipline
3. Harvests the diversification return (rebalancing bonus from mean reversion)

### Rebalancing Methods

**Calendar rebalancing:** Rebalance on a fixed schedule (monthly, quarterly, annually). Simple, easy to automate. Evidence shows quarterly or annual is sufficient — monthly is unnecessary and increases transaction costs.

**Threshold rebalancing:** Rebalance when any asset class deviates from target by more than a defined band (e.g., +/- 5%). More responsive to large moves, avoids unnecessary trades during calm periods. Most institutional investors use 5% absolute or 25% relative deviation thresholds.

**Momentum-aware rebalancing:** Standard rebalancing fights momentum — it sells winners and buys losers. Momentum-aware approaches introduce a delay:
- Let winners run until momentum signals weaken
- Rebalance only when mean reversion is more likely
- Evidence is mixed but intriguing: Granger (2014) showed a 3-12 month rebalancing delay improved returns by 0.3-0.5% annually

**Hybrid approach (recommended):**
1. Set threshold bands (e.g., +/- 5%)
2. When a threshold is breached, assess momentum: if the trend is still strong, wait (up to a maximum delay of 3 months)
3. After the delay, rebalance regardless
4. This captures most of the rebalancing benefit while respecting momentum

### Tax-Aware Rebalancing

Rebalancing in taxable accounts triggers capital gains. Minimize tax impact by:
- Using new contributions to rebalance (direct new cash to underweight asset classes)
- Rebalancing within tax-advantaged accounts first (no tax impact)
- Combining rebalancing with tax-loss harvesting (sell losers to rebalance down)
- Using cash flows (dividends, interest) to rebalance

See `tax-optimization` for the full tax-aware rebalancing framework.

---

## Part 8: Practical Framework — Building a Personal Strategic Allocation

### Step 1: Define Inputs

- **Risk tolerance:** Conservative / Moderate / Aggressive (validated by drawdown tolerance test)
- **Time horizon:** When is the money needed? Multiple horizons = multiple sub-portfolios
- **Income needs:** Does the portfolio need to generate current income?
- **Tax situation:** High marginal rate? Taxable vs tax-advantaged accounts?
- **Existing assets:** Employer stock, real estate equity, pension, Social Security
- **Behavioral tendency:** Will you panic sell? If yes, allocate more conservatively than your "ideal" risk tolerance suggests.

### Step 2: Select a Framework

Choose a base framework based on complexity tolerance:

| Investor Type | Framework | Why |
|--------------|-----------|-----|
| Simple, set-and-forget | Permanent portfolio or golden butterfly | Maximum simplicity, minimal monitoring |
| Balanced, moderate engagement | 60/40 variant (adjust equity/bond split for risk tolerance) | Well-understood, easy to implement |
| Sophisticated, willing to monitor | Risk parity (unlevered) or all-weather | Better regime diversification, requires rebalancing |
| Institutional/advanced | Endowment-light with 10-20% alternatives | Illiquidity premium access with realistic constraints |

### Step 3: Apply Regime Overlay

Identify the current macro regime. Apply tactical tilts (within +/- 5% bands) to the base allocation:

1. Assess growth trajectory (leading indicators, PMI, claims)
2. Assess inflation trajectory (breakevens, commodities, wages)
3. Map to one of four regimes
4. Adjust allocations per the regime table
5. Define reversion triggers

### Step 4: Implement

- Select specific instruments (index funds, ETFs, individual bonds)
- Apply asset location principles (see `tax-optimization`)
- Set rebalancing rules (threshold + momentum-aware)
- Document the plan and the decision rules

### Step 5: Monitor and Maintain

- Review allocation quarterly
- Reassess regime monthly
- Rebalance per rules (not emotion)
- Update strategic allocation annually or when life circumstances change
- Track performance relative to the strategic benchmark

### The Anti-Checklist: What NOT to Do

- Do not change strategic allocation based on market headlines
- Do not over-diversify (more than 10-12 asset classes adds complexity without benefit)
- Do not mistake tactical drift for strategic change
- Do not ignore correlation regime shifts (the most dangerous assumption)
- Do not rebalance purely on calendar when thresholds aren't breached (unnecessary costs)
- Do not neglect the behavioral dimension (the best allocation is the one you can stick with)

## Related Skills

- **`macro-cycles`** (Regime Intelligence) — consult when identifying the current macro regime for regime-based tactical tilts; cycle phase drives which asset classes to overweight or underweight
- **`factor-exposure`** (Portfolio Construction) — consult when implementing factor tilts within the allocation framework; factor positioning adds a layer of precision beyond asset class weights
- **`correlation-regimes`** (Risk Architecture) — consult when stress-testing diversification assumptions; allocation decisions based on normal-regime correlations can fail catastrophically in crisis regimes
- **`tax-optimization`** (Portfolio Construction) — consult when implementing allocation changes in taxable accounts; tax-aware rebalancing and asset location can significantly improve after-tax returns
