---
name: asset-universe
description: >
  Direct the asset universe subdomain — route asset-class-specific questions to the right
  specialist skill, define cross-asset analysis frameworks, and resolve conflicts between
  asset class views. Use when analyzing a specific asset class or comparing opportunities
  across equities, fixed income, commodities, currencies, or alternatives.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Asset Universe — The Allocator's Map

Every portfolio decision begins with one question: which asset classes deserve capital, in what proportion, and why now? This director routes asset-class-specific questions to the right specialist skill, defines frameworks for cross-asset analysis, and resolves conflicts when different asset class views contradict each other.

## Routing Logic

### Skill Routing Table

| Request Type | Primary Skill | Supporting Skills | Why |
|-------------|--------------|-------------------|-----|
| Stock selection, factor investing, sector rotation | `equities` | `fixed-income` (for rate sensitivity) | Equity-specific analysis and frameworks |
| Yield curve, credit spreads, duration, bonds | `fixed-income` | `currencies` (hedging costs) | Bond market analysis and positioning |
| Oil, gold, copper, grains, commodity positioning | `commodities` | `currencies` (dollar impact), `equities` (commodity equities) | Physical commodity supply/demand dynamics |
| FX strategy, dollar impact, carry trades | `currencies` | `fixed-income` (rate differentials), `equities` (earnings translation) | Currency analysis and portfolio hedging |
| Bitcoin, crypto, tokenization, DeFi | `digital-assets` | `currencies` (stablecoin dynamics), `equities` (crypto equities) | Digital asset analysis and sizing |
| Private equity, hedge funds, real estate, alts | `alternatives` | `equities` (public comps), `fixed-income` (private credit) | Alternative investment analysis and access |
| Asset allocation, portfolio construction | This director | All skills as needed | Cross-asset framework required |
| Regime identification, macro overlay | This director | All skills as needed | Multi-asset regime analysis |
| Risk budgeting across asset classes | This director | All skills as needed | Cross-asset risk decomposition |

### Routing Decision Tree

1. **Is the question about a single asset class?** Route to that specialist skill directly.
2. **Does the question span two asset classes?** Route to the primary skill, note the secondary as supporting context.
3. **Is it about allocation across asset classes?** Handle here using the cross-asset framework below.
4. **Is it about macro regime or market environment?** Handle here, then route implications to each specialist.
5. **Are two specialist skills giving conflicting signals?** Resolve here using the conflict resolution framework.

## Cross-Asset Analysis Framework

### The Regime Framework

Markets operate in regimes. The same asset behaves differently depending on which regime is active. Identify the regime first, then determine asset class positioning.

**Four Macro Regimes:**

| Regime | Growth | Inflation | Favored Assets | Challenged Assets |
|--------|--------|-----------|----------------|-------------------|
| Goldilocks | Rising | Falling | Equities (growth), credit, EM | Commodities, gold, long-duration bonds |
| Reflation | Rising | Rising | Commodities, value equities, TIPS | Long-duration bonds, growth equities |
| Stagflation | Falling | Rising | Gold, commodities, cash, TIPS | Equities, credit, long-duration bonds |
| Deflation | Falling | Falling | Long-duration bonds, gold, USD | Equities, commodities, credit, EM |

**Regime Identification Signals:**

- **Growth axis**: ISM Manufacturing (above/below 50), leading economic indicators, earnings revisions, credit conditions
- **Inflation axis**: CPI trend, breakeven inflation rates, commodity price momentum, wage growth, money supply growth
- **Transition signals**: The danger zone is regime transitions — watch for divergence between leading indicators and current data

### Cross-Asset Correlation Framework

Correlations between asset classes are not static. They change with regimes.

**Normal Environment (low volatility, moderate growth):**
- Stocks and bonds: negatively correlated (diversification works)
- Stocks and commodities: low positive correlation
- Dollar and commodities: negative correlation
- Gold and real rates: negative correlation

**Crisis Environment (high volatility, growth scare):**
- Stocks and bonds: strongly negatively correlated (flight to quality)
- Stocks and credit: strongly positively correlated (risk-off hits both)
- Dollar and everything: dollar rallies, everything else sells
- Correlations converge toward 1.0 among risk assets

**Inflationary Environment (rising prices, policy tightening):**
- Stocks and bonds: positively correlated (both sell off) — diversification breaks
- Commodities outperform both stocks and bonds
- TIPS outperform nominal bonds
- Gold's behavior depends on whether real rates are rising or falling

### The Valuation Compass

Relative value across asset classes provides allocation signals:

| Comparison | Metric | What It Tells You |
|-----------|--------|-------------------|
| Stocks vs bonds | Equity risk premium (earnings yield minus real bond yield) | Whether equities are cheap or expensive relative to bonds |
| Stocks vs commodities | S&P 500 / CRB ratio | Long-term mean reversion between financial and real assets |
| Bonds vs cash | Term premium | Whether you're being paid to take duration risk |
| Credit vs treasuries | Credit spread per unit of default risk | Whether credit is compensating for default risk |
| US vs international equities | Relative CAPE ratio | Whether US exceptionalism is priced in |
| Public vs private equity | Public equivalent multiple vs PE entry multiple | Whether the illiquidity premium is adequate |

### Capital Flow Framework

Money moves between asset classes in predictable patterns:

1. **Risk-on cascade**: Cash → short-duration bonds → investment grade credit → high yield → equities → small caps → EM → crypto
2. **Risk-off cascade**: The reverse, with speed proportional to the severity of the shock
3. **Rotation signals**: Fund flow data (EPFR), ETF creation/redemption, futures positioning (CFTC COT reports), central bank reserve allocation
4. **Structural flows**: Pension fund rebalancing (quarterly), sovereign wealth fund allocation shifts, demographic-driven flows (aging populations → bonds)

## Conflict Resolution Framework

When specialist skills give contradictory signals:

### Step 1: Identify the Time Horizon

Different asset classes operate on different time horizons. A bullish 10-year view on equities is fully compatible with a bearish 6-month view.

### Step 2: Weight by Conviction and Evidence

| Evidence Type | Weight |
|--------------|--------|
| Valuation (long-term) | High for strategic allocation, low for tactical |
| Momentum/trend (medium-term) | High for tactical, low for strategic |
| Sentiment/positioning (short-term) | High for timing, low for allocation |
| Macro regime (medium-term) | High for both tactical and strategic |

### Step 3: Check for Hidden Linkages

Apparent conflicts often arise because two skills are looking at different sides of the same macro driver. Example: bullish commodities and bullish bonds seems contradictory, but both can be right if you expect a growth slowdown (bonds rally) combined with a supply shock (commodities rally).

### Step 4: Default to Diversification

When genuinely uncertain, the answer is almost always "own both in proportion to your uncertainty." Concentration requires conviction. Diversification is the rational default.

## Integration Checklist

Before finalizing any cross-asset recommendation:

- [ ] Regime identified with at least 3 confirming indicators
- [ ] Correlation assumptions stated explicitly (normal vs crisis vs inflationary)
- [ ] Relative valuations checked across the comparison table
- [ ] Time horizon specified for each asset class view
- [ ] Conflicts between specialist skills resolved or acknowledged
- [ ] Currency impact considered (everything is a currency trade at some level)
- [ ] Liquidity conditions assessed (tightening liquidity changes all correlations)
- [ ] Tail risks identified (what breaks this view?)

## Curriculum Order

For building asset-universe literacy from scratch, follow this sequence:

1. **equities** — Foundation. Most investors start with equities, and equity markets are the most widely followed and deeply analyzed asset class. Understanding stock selection, factor investing, and sector dynamics provides the analytical foundation for all other asset classes. Many concepts (valuation, risk premiums, mean reversion) transfer directly.

2. **fixed-income** — Second layer. Bonds are the natural complement to equities and the foundation of portfolio construction. Understanding yield curves, credit spreads, duration, and rate sensitivity is essential before moving to commodities or currencies, because interest rates affect the pricing of every other asset class.

3. **commodities** — Third layer. Physical commodity markets introduce supply-demand dynamics, backwardation/contango, and the link between real assets and inflation. Requires understanding rate sensitivity (from fixed-income) and equity-commodity correlations. Commodities provide the inflation hedge dimension missing from stocks and bonds.

4. **currencies** — Fourth layer. Every cross-border investment is implicitly a currency trade. Understanding FX dynamics, carry trades, and dollar impact requires the foundation of equities (earnings translation), fixed income (rate differentials), and commodities (dollar-denominated pricing). Currency analysis ties the other asset classes together.

5. **digital-assets** — Fifth layer. Digital assets introduce new primitives (decentralization, programmable money, tokenization) but borrow heavily from currency analysis, commodity supply dynamics, and equity valuation frameworks. Place this after currencies because many digital asset dynamics mirror FX markets.

6. **alternatives** — Capstone. Private equity, hedge funds, real estate, and other alternatives require understanding all public market asset classes first. Alternatives are often illiquid versions of public market exposures with added complexity. Understanding public comps (equities), private credit (fixed income), and real asset dynamics (commodities) is prerequisite.

## Scope Boundaries

**This director handles**: All questions about individual asset classes, cross-asset analysis, relative valuation between asset classes, correlation frameworks, regime-based asset positioning, and capital flow dynamics across the asset universe.

**Escalate to the Archon when**:
- The question involves portfolio-level construction decisions beyond asset class analysis (route to portfolio-construction)
- The question involves macro regime identification rather than asset-class implications (route to regime-intelligence)
- The question involves security-level valuation within a single asset class (route to value-quality)
- The question involves risk management or position sizing across asset classes (route to risk-architecture)
- The question spans multiple investing subdomains and needs orchestrator-level coordination
