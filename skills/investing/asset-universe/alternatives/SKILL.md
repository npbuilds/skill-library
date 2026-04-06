---
name: alternatives
description: >
  Alternative investment frameworks — private equity, private credit, real estate, infrastructure,
  hedge funds, and managed futures. Reference when evaluating illiquid investments, sizing
  alternative allocations, understanding the illiquidity premium, or accessing non-traditional
  return streams.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Alternatives — Beyond Stocks and Bonds

Alternative investments are everything outside of publicly traded stocks, bonds, and cash. They exist because public markets do not capture the full opportunity set — private companies, direct real estate, complex trading strategies, and illiquid credit all offer returns that are partially inaccessible through traditional portfolios. The trade-off is always the same: you give up liquidity, transparency, and simplicity in exchange for (hopefully) higher returns, lower correlation, or both.

## Private Equity

### The Three Main Strategies

**Buyout**: Acquire a controlling stake in a mature company, typically using significant leverage (60-70% debt). Improve the company through operational efficiency, cost cutting, add-on acquisitions, and financial engineering. Exit in 3-7 years through sale or IPO.

- **Return drivers**: Leverage amplifies equity returns (a 20% increase in enterprise value becomes a 50%+ increase in equity value at 3x leverage). Operational improvement increases EBITDA. Multiple expansion (buying at 8x EBITDA, selling at 10x) adds additional return.
- **Historical returns**: Top-quartile buyout funds have generated 15-20% net IRR. Median funds have generated 10-14% net IRR. Bottom-quartile funds have returned single digits or worse.
- **Risk**: Leverage works both ways. A 20% decline in enterprise value at 3x leverage wipes out 60% of equity. Buyout funds underperform significantly during recessions when portfolio companies struggle and exit markets freeze.

**Growth equity**: Take a minority stake (20-40%) in a high-growth company, typically with little or no leverage. The company uses the capital to scale — expand into new markets, hire, invest in product development. Exit in 3-5 years.

- **Return drivers**: Revenue growth and margin expansion drive value creation. No leverage amplification — returns come purely from business improvement and multiple expansion.
- **Historical returns**: Similar to buyout at the top quartile (15-20% net IRR) but with a wider dispersion of outcomes and longer time to liquidity.
- **Risk**: Growth companies can fail to scale, burn cash, or lose competitive position. No leverage means no downside amplification, but also no debt cushion if the equity thesis fails.

**Venture capital**: Invest in early-stage companies (seed, Series A, Series B) with the potential for transformative growth. Extreme power-law distribution — most investments fail, and returns are driven by a small number of massive winners.

- **Return drivers**: The occasional 50-100x return on a company that becomes a category leader. These winners must compensate for the 50-70% of portfolio companies that fail entirely.
- **Historical returns**: Top-decile VC funds have generated 25%+ net IRR. Median VC returns are mediocre — approximately equal to public equities. VC is the most manager-dependent asset class in investing.
- **Risk**: Extreme illiquidity (10+ year fund life), extreme loss rates (majority of investments go to zero), and extreme dependence on manager skill (the difference between top and bottom quartile is 15-20%+ in IRR).

### Key PE Metrics

**IRR (Internal Rate of Return)**: The annualized return accounting for the timing of cash flows. IRR is the standard PE performance metric but can be manipulated — subscription line facilities (fund-level borrowing) artificially boost IRR by delaying capital calls. Always ask for IRR both with and without subscription line usage.

**MOIC (Multiple on Invested Capital)**: Total value returned divided by total capital invested. MOIC is harder to manipulate than IRR because it is time-insensitive. A 2.0x MOIC means you doubled your money. A 3.0x MOIC over 5 years is approximately 25% IRR. Over 10 years, it is approximately 12% IRR. Always look at both IRR and MOIC together.

**DPI (Distributions to Paid-In Capital)**: The ratio of actual cash returned to investors versus capital invested. A fund with high TVPI (total value) but low DPI is still holding unrealized gains — these are paper returns that may not materialize. A mature fund should have DPI approaching or exceeding 1.0x within 6-8 years.

### The J-Curve

PE funds exhibit a "J-curve" pattern — negative returns in the early years (management fees are charged on committed capital while investments are still being made and have not yet appreciated), followed by accelerating positive returns as portfolio companies mature and are exited.

**Implications**: Investors must commit to a PE program for the long term (10-15 years). Early-year losses are expected and should not trigger concern. The J-curve also means that starting a PE program requires patience — it takes 3-5 years before the portfolio generates meaningful positive returns.

### Vintage Year Importance

The year a PE fund begins investing (its vintage) has a significant impact on returns because it determines the valuation environment for entry. Funds that invested in 2009-2010 (post-GFC, low valuations) generated exceptional returns. Funds that invested in 2006-2007 (pre-GFC, high valuations) underperformed. Vintage diversification — committing to PE funds annually rather than in a single large commitment — is essential for smoothing returns.

## Private Credit

### The Strategies

**Direct lending**: Providing senior secured loans directly to middle-market companies (typically $10-100M EBITDA). These loans would historically have been made by banks, but post-GFC regulations pushed banks away from this market, creating an opportunity for non-bank lenders.

- **Yields**: SOFR + 400-650 bps, depending on credit quality and market conditions. All-in yields of 9-12% have been common since 2022.
- **Seniority**: Senior secured — first claim on assets in default. Recovery rates historically 60-80 cents on the dollar.
- **Default rates**: 1-3% annually for direct lending portfolios, though this varies significantly by cycle.

**Mezzanine**: Subordinated debt — junior to senior secured debt but senior to equity. Higher yield to compensate for lower priority in the capital structure.

- **Yields**: SOFR + 700-1000 bps, often with equity kickers (warrants or equity co-investment).
- **Risk**: Higher default losses than direct lending because of subordination. Recovery rates of 30-50 cents on the dollar.

**Distressed debt**: Buying the debt of companies in or near bankruptcy at steep discounts and either holding for recovery or participating in restructuring to gain equity ownership.

- **Returns**: Highly cyclical. 20%+ returns in post-recession vintages. Minimal opportunity in healthy economies.
- **Skill required**: Distressed investing requires deep legal and restructuring expertise. It is more akin to special-situation equity investing than traditional lending.

### Illiquidity Premium in Private Credit

Private credit yields exceed public bond yields of comparable credit quality by approximately 150-300 bps. This "illiquidity premium" compensates investors for:
- Inability to sell before maturity (no secondary market liquidity).
- Less transparency (private company financials, not SEC filings).
- Higher operational complexity (direct origination, monitoring, restructuring).
- Concentrated positions (single loans rather than diversified bond index).

### Private Credit Risks

- **Cycle risk**: The post-GFC era was exceptionally benign for credit — low rates, low defaults, easy refinancing. The true test of private credit portfolios comes during economic stress. Many private credit funds have never been through a real default cycle.
- **Valuation opacity**: Private credit is marked to model, not marked to market. Funds can (and do) maintain stable NAVs even when underlying credit quality is deteriorating. This creates an illusion of low volatility that masks true risk.
- **Leverage on leverage**: Many private credit funds use fund-level leverage (1.0-1.5x) on top of already-leveraged borrowers. This amplifies returns in good times and losses in bad times.
- **Crowding**: The rapid growth of private credit ($1.7 trillion market as of 2025) has compressed spreads and loosened lending standards. Today's vintages are lending at tighter spreads with weaker covenants than five years ago.

## Real Estate

### REITs vs Direct Real Estate

**REITs (Real Estate Investment Trusts)**:
- **Publicly traded**: Liquid, transparent, easy to buy and sell. But they trade like stocks — correlated with the equity market in the short term, even if the underlying real estate fundamentals are different.
- **Valuation**: REITs trade at a premium or discount to Net Asset Value (NAV). When REITs trade at a deep discount to NAV (as in late 2022), they may be undervalued relative to the underlying real estate. When they trade at a premium to NAV, they may be overvalued.
- **Dividend yield**: REITs must distribute 90%+ of taxable income as dividends. This creates high current income (4-6% yields typical) but limits retained capital for growth.
- **Interest rate sensitivity**: REITs are negatively correlated with interest rates in the short term — rising rates increase financing costs and make REIT dividend yields less attractive relative to bonds. But over the long term, REITs have outperformed during periods of rising rates when rate increases were driven by economic growth.

**Direct real estate**:
- **Illiquid**: Transactions take months and involve significant costs (brokerage fees, legal, due diligence). You cannot sell 2% of a building.
- **Control**: Direct ownership provides control over operations, leasing, capital improvements, and financing. This control is the source of alpha in real estate — good operators can improve property value through active management.
- **Leverage**: Real estate is typically financed with 60-75% debt. This leverage amplifies returns (and losses). A property generating a 6% unlevered yield can generate 10-15% levered equity returns.
- **Illiquidity premium**: Direct real estate returns have historically exceeded REIT returns by approximately 1-2% per year, consistent with an illiquidity premium.

### Cap Rates and Property Types

**Cap rate (Capitalization Rate)**: Net operating income / property value. The real estate equivalent of an earnings yield. A 5% cap rate means the property generates 5% of its value in annual net operating income. Lower cap rates = more expensive. Higher cap rates = cheaper (but may indicate higher risk).

**Property type characteristics**:

| Type | Cap Rate Range (2025) | Growth Profile | Recession Sensitivity |
|------|----------------------|----------------|----------------------|
| Industrial/logistics | 4.5-6.0% | Strong growth (e-commerce, nearshoring) | Low — essential for supply chains |
| Multifamily/apartments | 4.5-5.5% | Moderate growth (housing shortage) | Low — people always need housing |
| Data centers | 4.0-5.5% | Very strong growth (AI, cloud) | Very low — mission-critical |
| Office | 6.0-9.0% | Challenged (remote work) | High — cyclical, tenant-dependent |
| Retail | 5.5-8.0% | Mixed (experiential retail OK, commodity retail challenged) | Moderate to high |
| Healthcare | 5.5-7.0% | Steady (aging demographics) | Low — essential services |

### Interest Rate Sensitivity

Real estate is the most interest-rate-sensitive asset class because of its heavy reliance on debt financing. Higher rates increase mortgage costs, reduce property values (higher cap rates), and slow transaction activity. The 2022-2023 rate hiking cycle caused a 15-25% correction in commercial real estate values.

**The positive case for rising rates**: If rates are rising because the economy is strong, rents also rise, partially offsetting the cap rate expansion. The worst environment for real estate is rising rates during a weak economy — higher costs with no offsetting revenue growth.

## Infrastructure

### The Investment Case

Infrastructure assets — toll roads, airports, utilities, pipelines, cell towers, renewable energy installations — share common characteristics that make them attractive for long-term investors:

**Stable, predictable cash flows**: Many infrastructure assets operate under long-term contracts, regulated tariff structures, or concession agreements that provide revenue visibility 10-30 years into the future.

**Inflation linkage**: Infrastructure revenues are often explicitly or implicitly linked to inflation. Toll roads have inflation-adjusted toll rates. Utilities have CPI-linked tariff adjustments. Renewables have power purchase agreements (PPAs) with inflation escalators. This makes infrastructure a natural inflation hedge.

**Essential services**: People need electricity, water, transportation, and communications regardless of economic conditions. This makes infrastructure demand relatively inelastic — recession-resistant compared to most other asset classes.

**Long asset lives**: Infrastructure assets last 30-100 years. This creates long-duration cash flow streams that are well-suited for pension funds and endowments with long-term liabilities.

### Infrastructure Sub-Sectors

- **Transportation**: Toll roads, airports, ports, rail. Revenue driven by traffic volume (GDP-linked) and toll/fee increases (inflation-linked). Airports have the highest growth potential; toll roads have the most predictable cash flows.
- **Utilities**: Regulated electricity, gas, and water distribution. Returns are set by regulators (cost-plus model). Very stable but with limited upside. Regulatory risk is the primary concern.
- **Renewables**: Solar, wind, battery storage. Revenue from PPAs and merchant power sales. Growth driven by decarbonization mandates and declining technology costs. Returns are more variable than traditional infrastructure due to weather variability and merchant price exposure.
- **Digital infrastructure**: Cell towers, fiber networks, data centers. The fastest-growing infrastructure sector. Driven by 5G rollout, AI compute demand, and cloud computing growth. Higher growth but also higher technology obsolescence risk.

## Hedge Fund Strategies

### Long/Short Equity

The original hedge fund strategy. Buy undervalued stocks (long book), sell overvalued stocks (short book). Net market exposure can range from 0% (market neutral) to 70%+ (net long with a hedge).

**Return drivers**: Stock selection alpha on both the long and short side. The short book provides a hedge against market declines — in theory, the long book's alpha is preserved while the market exposure is reduced.

**Reality check**: The average long/short equity fund has not justified its fees since 2010. Net exposure has crept higher (most funds are 40-60% net long), making them expensive beta. The best long/short managers add alpha through differentiated research, but manager selection is critical — the dispersion between top and bottom quartile is enormous.

### Global Macro

Trade directional views on interest rates, currencies, commodities, and equity indices based on macroeconomic analysis. Uses futures, options, and forwards across global markets.

**Return drivers**: Directional macro calls. George Soros breaking the Bank of England (1992) is the archetype. Global macro funds thrive during regime changes — interest rate pivot points, currency crises, and structural economic shifts.

**Correlation benefit**: Global macro has historically had low correlation with both equities and bonds, making it a genuine portfolio diversifier. Returns are episodic — long periods of modest returns punctuated by large gains during macro dislocations.

### Systematic/Quantitative

Use computer models to identify patterns and execute trades across asset classes. Sub-strategies include statistical arbitrage (exploiting short-term price relationships), trend following (CTA/managed futures), and machine learning-based approaches.

**Trend following deserves special attention** — see the section on managed futures below.

### Event-Driven

Invest around corporate events — mergers, acquisitions, restructurings, spin-offs, activist campaigns. Returns are driven by the event's completion and the price gap between the current market price and the expected outcome.

**Sub-strategies**: Merger arbitrage (buy target, short acquirer after deal announcement — earn the spread if the deal closes), activist (buy a stake and push for changes to unlock value), distressed (buy the debt or equity of companies in or near bankruptcy).

**Correlation**: Event-driven strategies have moderate correlation with equities (deal activity correlates with market health). Merger arbitrage has the lowest equity correlation; activist and distressed have higher correlation.

## Managed Futures / Trend Following

### The Crisis Alpha Proposition

Managed futures (CTA) strategies systematically follow price trends across futures markets in equities, bonds, commodities, and currencies. They buy assets that are going up and sell assets that are going down.

**Why trend following works**: Trends exist in financial markets because of behavioral biases (herding, anchoring, underreaction to new information), institutional flows (rebalancing, central bank intervention), and structural market features (momentum in economic fundamentals). These causes persist because they are rooted in human psychology and market structure, not in temporary anomalies that can be arbitraged away.

**Crisis alpha**: The most valuable property of trend following is its tendency to generate strong positive returns during sustained market crises — precisely when portfolios need protection most:
- 2008 global financial crisis: The SG CTA index returned +13% while the S&P 500 fell 37%.
- 2022 rate shock: Managed futures were the best-performing strategy, gaining 20%+ while both stocks and bonds fell.
- COVID crash (2020): Limited benefit — the crisis was too fast for trend-following systems to respond. Trend following protects against sustained crises, not sudden shocks.

**Correlation with traditional assets**: Managed futures have near-zero long-term correlation with equities and bonds. This is the most powerful diversification benefit in alternative investments. Adding a 10-15% allocation to managed futures has historically reduced portfolio drawdowns by 20-30% while maintaining or improving returns.

**Performance characteristics**: Modest returns during calm markets (5-8% annually), strong returns during sustained trends, and losses during choppy, mean-reverting markets. The Sharpe ratio is moderate (0.4-0.6 for diversified CTA strategies), but the crisis-protection characteristic makes the portfolio-level contribution much more valuable than the standalone return suggests.

## Democratization of Alternatives

### New Access Vehicles

Historically, alternative investments were available only to institutional investors and ultra-high-net-worth individuals through limited partnership structures with $1M+ minimums. This is changing:

**Interval funds**: Registered closed-end funds that offer periodic liquidity (typically quarterly, for 5% of NAV). They invest in private credit, real estate, and other illiquid strategies. Minimums as low as $2,500. Examples: Cliffwater Corporate Lending Fund, Bluerock Total Income Real Estate Fund.

**BDCs (Business Development Companies)**: Publicly traded or non-traded companies that make loans to middle-market businesses. Publicly traded BDCs (like Ares Capital, Blue Owl Capital Corporation) provide daily liquidity. Non-traded BDCs offer higher yields but limited liquidity.

**Non-traded REITs**: Private REITs not listed on exchanges. They offer stable NAVs (because they are not subject to daily market pricing) and higher yields. But limited liquidity — redemptions are typically quarterly and can be restricted during stress. Blackstone BREIT's 2022-2023 redemption restrictions highlighted this risk.

### SEC Regulatory Changes

The SEC has been gradually expanding access to private markets. Key developments include raising the thresholds for accredited investor status to include people with specific professional knowledge, expanding Regulation A+ offerings, and allowing greater private fund access through registered fund structures. These changes broaden the investor base for alternatives but also raise investor protection concerns — illiquid, complex investments are not suitable for all investors.

## The Illiquidity Premium

### Quantifying the Extra Return

The illiquidity premium is the additional return investors earn for holding assets they cannot easily sell. Estimates vary:

- **Private equity vs public equity**: 1-3% per year after adjusting for leverage, size, and sector biases. The premium is higher for venture capital and smaller buyout funds (where illiquidity is most severe).
- **Private credit vs public credit**: 1.5-3% per year for comparable credit quality. The premium reflects both illiquidity and the complexity of direct origination.
- **Direct real estate vs REITs**: 1-2% per year. The premium reflects transaction costs, operational complexity, and illiquidity.

**The premium is not guaranteed**: Illiquidity premium estimates are backward-looking and subject to survivorship bias (failed funds are underrepresented in databases). The premium also varies by cycle — it is highest when capital is scarce (post-crisis) and lowest when capital is abundant (late cycle).

**Who should bear illiquidity**: Investors with long time horizons (pensions, endowments, young individuals), stable capital bases (no risk of forced selling), and sufficient scale to diversify across vintage years and managers. Investors who may need the capital within 3-5 years, who have concentrated positions, or who cannot tolerate NAV losses (even if temporary) should avoid illiquid alternatives.

### The Denominator Effect

When public market portfolios decline sharply (as in 2022), the allocation to alternatives mechanically increases as a percentage of total portfolio value (because alternatives are not marked down as quickly). This "denominator effect" can force investors to sell alternatives at inopportune times to rebalance back to target allocation. The denominator effect is a practical constraint that limits how large an alternative allocation can be — even for long-term investors.

## Practical Framework: Alternative Allocation

### Step 1: Determine Your Illiquidity Budget

How much of your portfolio can you lock up for 5-10+ years without creating a liquidity crisis? This is the binding constraint on alternative allocation. A common framework:

- **Personal liquidity buffer**: Maintain 1-2 years of expenses in liquid assets before considering alternatives.
- **Portfolio liquidity**: No more than 20-30% of a long-term portfolio in illiquid alternatives (for most individual investors). Institutional investors (endowments, pensions) can go higher — 30-50% — because of their perpetual time horizon and stable capital base.

### Step 2: Choose Strategies Based on Objective

| Objective | Primary Strategy | Why |
|-----------|-----------------|-----|
| Return enhancement | Private equity (buyout/growth), venture capital | Highest return potential with corresponding highest risk and illiquidity |
| Income generation | Private credit, real estate | High current yield, inflation protection (real estate) |
| Diversification / crisis protection | Managed futures, global macro | Low correlation with stocks and bonds, crisis alpha |
| Inflation protection | Real estate, infrastructure, commodities | Real asset exposure, inflation-linked cash flows |
| Volatility reduction | Market neutral hedge funds, managed futures | Low or negative equity beta |

### Step 3: Implement Vintage Year Diversification

For PE and private credit, commit capital across multiple vintage years rather than making a single large commitment. This diversifies across valuation environments and economic cycles. A common approach: commit 1/5 of the target PE allocation annually over 5 years.

### Step 4: Select Managers Ruthlessly

In alternatives, manager selection is the primary determinant of returns — far more than in public equity investing. The spread between top-quartile and bottom-quartile PE managers is 10-15% in IRR. The spread in venture capital is even wider.

**Manager selection criteria**:
- Track record across multiple cycles (at least 3 funds).
- Consistency of team (key person departures are a red flag).
- Strategy differentiation (what do they do that others cannot?).
- Alignment of interests (GP commitment of 2-5% of fund, no GP-level leverage, reasonable fee structures).
- Reasonable fund size (funds that grow too large lose the ability to invest in their sweet spot).

### Step 5: Monitor and Rebalance Thoughtfully

Alternative investments cannot be rebalanced daily. Rebalancing happens through commitment pacing — if the current alternative allocation is above target (because public markets have fallen), slow the pace of new commitments. If below target (because public markets have rallied), accelerate commitments. This is a multi-year process, not a quarterly adjustment.

### Step 6: Understand the Fee Drag

Alternatives are expensive. Typical fee structures:
- **PE/VC**: 2% management fee + 20% carry (performance fee above a hurdle rate, typically 8%).
- **Hedge funds**: 1.5-2% management fee + 15-20% incentive fee. Some funds charge lower management fees with higher incentive fees (better alignment).
- **Private credit**: 1-1.5% management fee + 10-15% incentive fee.
- **Interval funds/BDCs**: 1-2% management fee, plus potential incentive fees.

**The fee math**: A PE fund that generates 15% gross returns and charges 2/20 delivers approximately 11-12% net to investors. The net return must be compared to a public market equivalent (what you could have earned in a comparable public market index). If the PE fund's net return does not exceed the public market equivalent by at least 2-3%, the illiquidity and complexity are not being adequately compensated.
