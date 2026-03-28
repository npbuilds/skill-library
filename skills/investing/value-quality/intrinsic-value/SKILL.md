---
name: intrinsic-value
description: >
  Expert knowledge on business valuation from first principles — DCF methodology, owner earnings,
  margin of safety, moat analysis, valuation multiples, and asset-based approaches. Covers the
  complete toolkit for determining what a business is actually worth. Use when evaluating whether
  a specific business or asset is trading above or below its fundamental worth.
---

# Intrinsic Value — What Is This Business Actually Worth?

The central question of investing is deceptively simple: what is this asset worth? Every valuation method is an attempt to answer this question, and every method has blind spots. Mastery means knowing which tool to use, when each tool lies to you, and how much uncertainty to attach to the answer.

## Owner Earnings — Buffett's True Measure of Value

Reported earnings are an accounting construct. Owner earnings represent the actual cash a business owner could extract while maintaining the business's competitive position.

### The Formula

```
Owner Earnings = Net Income
                 + Depreciation & Amortization
                 - Maintenance Capital Expenditure
                 - Changes in Working Capital
```

### Component Analysis

**Net income** — Start here, but treat it as a starting point only. Adjust for:
- One-time charges and gains (restructuring, asset sales, litigation)
- Stock-based compensation (a real cost that GAAP used to ignore)
- Pension adjustments and actuarial assumption changes
- Mark-to-market gains/losses on investments (Berkshire's earnings are useless because of this)

**Depreciation and amortization** — Added back because it's a non-cash charge, but this is where most analysts get lazy. D&A is only a true add-back to the extent it exceeds maintenance capex. For asset-heavy businesses (airlines, railroads, telecom), D&A roughly equals maintenance capex and shouldn't be added back at all.

**Maintenance capex** — The critical and most difficult number. This is the capex required to maintain the business's current earning power, excluding growth capex. Companies never disclose this cleanly.

Estimation approaches:
- **Management commentary**: Some CEOs (Buffett at Berkshire, Malone at Liberty) explicitly separate maintenance from growth capex. Trust them only if they have a track record of honesty.
- **Depreciation proxy**: For stable businesses, maintenance capex approximately equals depreciation over full cycles. If capex consistently exceeds depreciation, some portion is growth. If capex is consistently below depreciation, the company is underinvesting (a red flag).
- **Capex/revenue ratio**: For mature businesses, plot capex as a percentage of revenue over 10+ years. The floor of the range approximates maintenance intensity. Spikes above represent growth investments.
- **Industry benchmarks**: Compare capex intensity to peers at similar scale and growth rates.

**Working capital changes** — Cash consumed or released by changes in receivables, inventory, and payables. Negative working capital businesses (Amazon, Costco, insurance companies) collect cash before paying suppliers — working capital changes are a source of cash as they grow. Capital-intensive manufacturers and distributors tie up cash in inventory and receivables — working capital is a use of cash as they grow.

### Owner Earnings vs Free Cash Flow

Owner earnings and FCF are related but not identical:

| Metric | Includes growth capex? | Includes SBC? | Best for |
|--------|----------------------|---------------|----------|
| Owner Earnings | No (maintenance only) | Adjusted out | Valuing the business as-is |
| Free Cash Flow (GAAP) | No (all capex deducted) | Usually not adjusted | Cash available after all investment |
| Adjusted FCF | Growth capex added back | Adjusted out | Valuing the core business + growth option |

Use owner earnings when you want to understand the sustainable cash generation of the existing business. Use FCF when you want to understand what's left after the company funds its own growth.

## DCF — Building a Valuation from First Principles

A DCF translates future cash flows into a present value. It is the theoretically correct way to value any cash-flow-producing asset. It is also the easiest model to manipulate by tweaking assumptions.

### Step 1: Revenue Modeling

Two approaches, ideally triangulated:

**Top-down**: Start with total addressable market (TAM), estimate market share trajectory, apply to derive revenue.
- Good for: new markets, category creators, businesses with clear market share opportunities
- Bad for: mature businesses where TAM is well-known and share is stable
- Pitfall: TAM estimates are notoriously inflated. A $100B TAM means nothing if the company can only address $5B of it profitably.

**Bottom-up**: Start with units (customers, subscribers, stores, contracts) multiplied by revenue per unit.
- Good for: businesses with observable unit economics (SaaS, retail, subscription)
- Bad for: businesses with complex, multi-product revenue streams
- Strength: forces you to make concrete, falsifiable assumptions (e.g., "net new subscribers per quarter")

**Revenue modeling checklist**:
- What is the organic growth rate, separated from acquisition-driven growth?
- Is growth accelerating, stable, or decelerating? What drives the trend?
- What is the pricing power? Can the business raise prices without losing volume?
- What is the customer acquisition cost (CAC) trend? Rising CAC signals market saturation.
- What is the retention/churn rate? For recurring revenue businesses, this is the most important number.

### Step 2: Margin Analysis and Normalization

Forecast operating margins, not just revenue. Margins tell you whether growth creates value or destroys it.

**Margin normalization** — Remove cyclical, one-time, and accounting distortions:
- Average margins over a full business cycle (7-10 years) for cyclical businesses
- Exclude restructuring charges, litigation, and other one-time items
- Adjust for stock-based compensation (treat it as a real cash cost)
- Normalize for acquisition-related amortization (this is an accounting artifact for quality acquirers)

**Margin trajectory analysis**:
- **Expanding margins**: Operating leverage (fixed costs spread over growing revenue), pricing power, mix shift toward higher-margin products. Sustainable if driven by scale; temporary if driven by cost-cutting.
- **Stable margins**: Mature business in competitive equilibrium. Good for predictability.
- **Compressing margins**: Competition, commodity input inflation, regulatory cost, loss of pricing power. The most dangerous trend — it compounds negatively.

**The incremental margin question**: What margin does the company earn on each additional dollar of revenue? If incremental margins exceed average margins, the business has operating leverage and margins should expand with growth. If incremental margins are below average margins, growth is dilutive.

### Step 3: Working Capital and Capex Modeling

**Working capital**: Model as a percentage of revenue for stable businesses. For growing businesses, calculate the incremental working capital required per dollar of revenue growth. Negative working capital businesses generate cash from growth — this is a significant competitive advantage.

**Capital expenditure**: Separate maintenance from growth. Model maintenance capex as a percentage of revenue or fixed assets. Model growth capex as a function of revenue growth targets. For capital-light businesses (software, marketplaces), capex is minimal. For capital-heavy businesses (energy, telecom, manufacturing), capex modeling is often more important than revenue modeling.

### Step 4: Terminal Value

The terminal value typically represents 60-80% of a DCF's total value, which means the most uncertain assumption drives most of the answer. This is the fundamental weakness of DCF analysis.

**Perpetuity growth method**:
```
Terminal Value = FCF_final × (1 + g) / (WACC - g)
```
Where g = perpetuity growth rate.

Rules:
- g should not exceed long-term nominal GDP growth (typically 2-4%)
- For most businesses, g = 2-3% is appropriate (inflation + minimal real growth)
- For declining industries, g can be 0% or negative
- g > 4% is almost never defensible for terminal value — it implies the company eventually becomes larger than the economy
- Sensitivity test: a 0.5% change in g can swing the valuation by 20-30%

**Exit multiple method**:
```
Terminal Value = EBITDA_final × Exit Multiple
```

Rules:
- Use when comparable transactions or trading multiples are more reliable than perpetuity assumptions
- The exit multiple should reflect a "mature state" multiple, not current elevated or depressed multiples
- Common approach: use the median historical multiple for the industry
- Cross-check: convert the implied exit multiple from your perpetuity growth model and vice versa — they should be consistent

**When to use which**:
- Perpetuity growth: stable businesses with predictable cash flows (consumer staples, utilities, regulated industries)
- Exit multiple: businesses where comparable multiples are well-established and growth is harder to forecast
- Both: always cross-check one method against the other. If they diverge significantly, your assumptions are inconsistent.

### Step 5: Discount Rate — WACC Construction

```
WACC = (E/V × Re) + (D/V × Rd × (1 - Tax Rate))
```

**Cost of equity (Re)** — CAPM approach:
```
Re = Risk-Free Rate + Beta × Equity Risk Premium + Size Premium + Specific Risk Premium
```

- **Risk-free rate**: 10-year or 20-year government bond yield (match duration to your forecast horizon)
- **Beta**: Measure of systematic risk relative to the market. Use 2-year weekly returns against the broad market index. Unlevered beta for comparisons across capital structures.
- **Equity risk premium (ERP)**: The most debated number in finance.
  - Historical average (US): ~5-6% arithmetic, ~4-5% geometric
  - Forward-looking estimates (Damodaran): typically 4-6%, varies with market conditions
  - Higher for emerging markets, small caps, and illiquid assets
  - The ERP should be higher when markets are euphoric (prices are high, expected returns are low) and lower when markets are depressed — this is counterintuitive but mathematically correct
- **Size premium**: Small-cap stocks have historically earned 1-3% more than large caps, though this premium may have shrunk or disappeared in recent decades
- **Specific risk premium**: For private companies, add 2-5% for illiquidity and key-person risk

**Cost of debt (Rd)**: Use the yield on the company's existing debt, or the yield on comparable-rated debt. Not the coupon rate — the market yield.

**Capital structure weights**: Use market values, not book values. For the target capital structure, use the company's long-term average or the industry median.

**WACC problems and alternatives**:
- WACC assumes a constant capital structure — breaks down for LBOs and highly leveraged situations
- WACC assumes a constant risk profile — inappropriate for high-growth companies whose risk declines as they mature
- Alternative: Adjusted Present Value (APV) — value the unlevered business separately, then add the tax shield of debt
- Buffett's approach: Ignore WACC entirely. Use the long-term Treasury rate or a fixed 10% hurdle rate. Compensate for risk in the cash flow estimates, not the discount rate. This is intellectually cleaner but harder to standardize.

## Margin of Safety — Graham's Core Principle

Margin of safety is the difference between your estimate of intrinsic value and the price you pay. It exists to protect you from three things: (1) errors in your valuation, (2) bad luck, and (3) the unknowable.

### How Much Is Enough?

The required margin of safety depends on the quality and predictability of the business:

| Business Quality | Predictability | Minimum Margin of Safety |
|-----------------|---------------|------------------------|
| World-class compounder (>25% ROIC, wide moat, long runway) | High | 15-25% |
| Good business (15-25% ROIC, solid moat) | Moderate-high | 25-35% |
| Average business (10-15% ROIC, narrow moat) | Moderate | 35-50% |
| Cyclical or capital-intensive | Low | 40-60% |
| Turnaround, restructuring, or distressed | Very low | 50%+ or asset-based valuation |
| "I don't understand this business well" | N/A | Don't invest — no margin is large enough |

### Margin of Safety in Practice

- **Valuation range, not point estimate**: Never present a single intrinsic value number. Present a range (bear case, base case, bull case) and invest only when the market price is below your bear case.
- **Multiple valuation methods**: If DCF, owner earnings, and multiples all point to undervaluation, your margin of safety is real. If only one method says it's cheap, you may be fooling yourself.
- **Stress test the assumptions**: What happens to your valuation if revenue growth is 3% instead of 7%? If margins compress by 200bps? If the discount rate is 12% instead of 10%? The sensitivity analysis IS the margin of safety calculation.
- **The newspaper test**: Buffett's question — would you be comfortable owning this business if the stock market closed for 10 years? If the answer requires "the multiple will re-rate" or "the market will recognize the value," your thesis depends on other people agreeing with you, which is not a margin of safety.

## Moat Analysis — Competitive Advantage Framework

A moat is a structural competitive advantage that protects a business's excess returns from being competed away. Moats determine the sustainability of earnings, which determines the reliability of any valuation.

### The Five Sources of Moat (Morningstar/Dorsey Framework)

**1. Network Effects**
Each additional user increases the value of the product for all existing users. The strongest moats in the modern economy.

- **Direct network effects**: More users = more value for each user (social networks, messaging platforms, phone networks). Value scales roughly with n^2 (Metcalfe's Law, directionally correct if overstated).
- **Indirect/platform network effects**: More users on one side attract more users on the other (marketplaces, app stores, payment networks). Requires reaching critical mass on both sides.
- **Data network effects**: More users generate more data, which improves the product, which attracts more users (search engines, recommendation systems, mapping).
- **Strength test**: Can a well-funded competitor replicate the network? If a competitor offered users $100 to switch, would they? The answer reveals the true depth of the network effect.

**2. Switching Costs**
The pain of changing providers exceeds the benefit. Switching costs can be financial, procedural, or relational.

- **Financial**: Contractual penalties, retraining costs, data migration expenses, hardware incompatibility
- **Procedural**: Workflow disruption, learning curves, integration complexity, regulatory re-approval
- **Relational**: Trust built over years, relationship-specific knowledge, customization that would need to be rebuilt
- **Strength test**: What is the total cost of switching (monetary + time + risk + opportunity cost) relative to the annual spend? If switching cost > 2x annual spend, the moat is deep.

**3. Intangible Assets**
Brands, patents, regulatory licenses — assets that don't appear on the balance sheet at fair value but generate economic rent.

- **Brands**: Only a moat if they command pricing power. A well-known brand that competes on price has awareness, not a moat. Test: can the company raise prices 5% without losing more than 1-2% of volume?
- **Patents**: Provide temporary monopolies but expire. Pharmaceutical patents create enormous moats for 10-15 years, then collapse. Evaluate the patent cliff — when do the key patents expire, and what's in the pipeline to replace them?
- **Regulatory licenses**: Government-granted barriers to entry (banking charters, spectrum licenses, utility franchises, gaming licenses). Among the most durable moats because they're structurally maintained by the government. Risk: regulatory change.

**4. Cost Advantages**
Structural ability to produce at lower cost than competitors.

- **Process-driven**: Proprietary manufacturing processes, superior logistics, automation advantages. Toyota's production system, Nucor's mini-mill process.
- **Location-based**: Proximity to raw materials, customers, or distribution networks that competitors cannot replicate. Quarries, mines, regional refineries.
- **Unique resource access**: Exclusive contracts, mineral rights, proprietary data sources.
- **Scale-based**: Cost per unit declines with volume. Fixed cost leverage (software), purchasing power (Walmart, Costco), distribution efficiency. The most common cost advantage and often the hardest to sustain because competitors can grow too.

**5. Efficient Scale**
Markets that are only large enough to support one or a few profitable competitors. New entrants would drive returns below the cost of capital for all participants, so rational competitors don't enter.

- **Natural monopolies**: Utilities, toll roads, airports, railroads, waste disposal in regional markets
- **Niche dominance**: Businesses that dominate small markets that aren't worth competing in. The best hidden moats are companies that dominate boring niches.
- **Test**: Is the market large enough to support another competitor at the minimum efficient scale? If not, the moat is structural.

### Moat Erosion Signals

Moats erode. The most dangerous time is when a company's financials look great but the moat is quietly weakening. Watch for:

- **Declining ROIC over 3-5 year periods**: The single best quantitative signal of moat erosion. If ROIC is trending from 25% to 20% to 16%, the moat is narrowing even if the company is still highly profitable.
- **Market share loss**: Especially when combined with price increases — the company is harvesting the moat, not maintaining it.
- **Pricing power deterioration**: Having to discount, offer promotions, or match competitor prices. Track net revenue per unit over time.
- **Customer acquisition cost inflation**: Rising CAC suggests the easy-to-acquire customers have been captured and the company is fighting harder for marginal customers.
- **Increasing capex intensity**: If the business needs to spend more to maintain its competitive position, the moat may be narrowing.
- **Technology disruption**: A new technology that changes the cost structure or value proposition. Newspapers had moats until the internet created near-zero distribution costs.
- **Regulatory change**: Government can create moats (spectrum licenses) and destroy them (deregulation, generic drug approvals).

## Valuation Multiples — When and How to Use Them

Multiples are shortcuts. They compress a DCF into a single ratio. This makes them useful for quick comparisons but dangerous when used without understanding what they embed.

### Multiple Taxonomy

| Multiple | Formula | Best For | Watch Out For |
|----------|---------|----------|---------------|
| P/E | Price / Earnings per Share | Stable, profitable businesses | Earnings manipulation, cyclicality, capital structure differences |
| EV/EBITDA | Enterprise Value / EBITDA | Comparing businesses with different capital structures and tax rates | Ignores capex intensity, working capital, tax differences |
| P/FCF | Price / Free Cash Flow per Share | Capital allocation assessment, actual cash returns | FCF can be manipulated via capex timing, working capital management |
| P/B | Price / Book Value per Share | Banks, insurers, asset-heavy businesses | Book value is historical cost, not market value; useless for asset-light businesses |
| EV/Revenue | Enterprise Value / Revenue | High-growth pre-profit businesses | Says nothing about profitability; a last resort metric |
| EV/EBIT | Enterprise Value / Operating Income | Businesses with varying D&A profiles | Better than EV/EBITDA for capital-intensive businesses |

### Relative Valuation Pitfalls

**"Cheap relative to peers" is not cheap.** The entire sector can be expensive. In 1999, a tech stock trading at 40x earnings was "cheap" relative to peers at 80x. It still lost 60% of its value. Always anchor relative valuation to absolute valuation — what is the implied growth rate, and is it achievable?

**Multiple compression destroys returns.** A company growing earnings at 15% per year but seeing its P/E compress from 25x to 15x over five years delivers approximately 0% total return. Growth without multiple stability is a treadmill.

**Cyclical businesses fool you with multiples.** A cyclical company looks cheapest (lowest P/E) at the peak of the cycle when earnings are highest. It looks most expensive (highest P/E) at the trough when earnings are depressed. The correct approach: normalize earnings over the full cycle, then apply the multiple to normalized earnings.

## Asset-Based Valuation

When to use: when the value of a business resides primarily in its assets rather than its earning power.

**Appropriate contexts**:
- **Banks and financial institutions**: Book value is a meaningful proxy for asset value because most assets are marked to market or close to it. P/B ratio is the standard metric. Tangible book value is more conservative.
- **REITs**: Net asset value (NAV) based on property appraisals. Compare market cap to NAV. A discount to NAV may indicate a buying opportunity or justified skepticism about property values.
- **Holding companies and conglomerates**: Sum-of-parts analysis — value each subsidiary separately and compare the sum to the market cap. Persistent discounts to sum-of-parts may indicate a "conglomerate discount" (management complexity, capital allocation concerns) or hidden value.
- **Liquidation scenarios**: What are the assets worth in an orderly liquidation? Inventory at liquidation value (typically 50-80% of book), receivables at collection probability, real estate at market, equipment at auction value. Benjamin Graham's "net-net" — buying below net current asset value — is the deepest value approach.

## Sum-of-Parts Valuation

Conglomerates and multi-segment businesses often trade at discounts to the sum of their parts because:
- The market applies a single multiple to blended earnings instead of valuing each segment appropriately
- Management complexity and capital allocation risk justify some discount
- Minority shareholders cannot access individual segment value

**Methodology**:
1. Identify each operating segment's revenue, EBIT/EBITDA, and capital employed
2. Select appropriate comparable multiples for each segment (using pure-play peers)
3. Value each segment independently
4. Add non-operating assets (cash, investments, real estate) at market value
5. Subtract holding company costs and debt at market value
6. Compare the sum to the current market cap

**Catalysts that unlock sum-of-parts value**: Spinoffs, asset sales, activist investors, management changes, IPOs of subsidiaries. Without a catalyst, a conglomerate discount can persist indefinitely.

## The Buffett Newspaper Test

The ultimate sanity check: if the stock market closed for 10 years and you couldn't sell, would you still buy this business at this price?

This question forces you to evaluate:
- **Cash flow reliability**: Will the business generate predictable cash flows for a decade without needing the stock market for financing?
- **Competitive position durability**: Will the moat be wider or narrower in 10 years?
- **Management quality**: Do you trust the people running this business with your capital for a decade?
- **Capital allocation**: Will management reinvest cash at high rates of return, or waste it on empire-building acquisitions and vanity projects?
- **Valuation discipline**: Are you paying a price where the business itself generates an adequate return, regardless of what happens to the stock price?

If your investment thesis requires "the market will re-rate this stock" or "the multiple will expand," you are speculating on sentiment, not investing based on value. The newspaper test eliminates this dependency and forces genuine intrinsic value thinking.

## Related Skills

- **`macro-cycles`** (Regime Intelligence) — consult when valuing cyclical businesses; normalized earnings require understanding where we are in the cycle
- **`quality-compounders`** (Value & Quality) — consult when analyzing ROIC sustainability, reinvestment runway, and the compounding math that drives long-term intrinsic value
- **`second-level-thinking`** (Value & Quality) — consult when assessing what the market has already priced into the valuation and whether your variant perception is justified
