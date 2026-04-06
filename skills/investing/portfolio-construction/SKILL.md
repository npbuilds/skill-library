---
name: portfolio-construction
description: >
  Direct portfolio construction decisions across allocation, factor exposure, hedging, and tax optimization.
  Route questions about building, maintaining, and optimizing investment portfolios to the right specialist skill.
  Use when translating investment views into concrete portfolio positions, sizing, hedging, or rebalancing decisions.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Portfolio Construction — The Architect's Blueprint

Portfolio construction is where investment insight becomes investable reality. Analysis means nothing if it doesn't translate into a coherent portfolio with defined risk, intentional factor exposures, efficient tax treatment, and appropriate hedging. This director routes portfolio construction questions to the right specialist and ensures the pieces fit together.

## Routing Logic

### Skill Routing Table

| Request Type | Primary Skill | Supporting Skills | Why |
|-------------|--------------|-------------------|-----|
| Strategic allocation, tactical shifts, risk parity, glide paths | `asset-allocation` | `factor-exposure` (factor-aware allocation) | Core allocation framework and regime positioning |
| Factor tilts, smart beta, value/momentum/quality exposure | `factor-exposure` | `asset-allocation` (allocation context) | Factor selection, timing, and portfolio integration |
| Put protection, tail risk, hedging strategy, insurance | `hedging-architecture` | `asset-allocation` (what's being hedged) | Downside protection and convexity design |
| Tax-loss harvesting, asset location, direct indexing | `tax-optimization` | `asset-allocation` (rebalancing context) | After-tax return maximization |
| Full portfolio build from scratch | This director | All skills sequentially | Requires coordinated multi-skill construction |
| Portfolio review or audit | This director | All skills as needed | Cross-cutting analysis of existing portfolio |
| Rebalancing decisions | `asset-allocation` + `tax-optimization` | `factor-exposure` (factor drift) | Rebalancing involves both allocation and tax |

### Routing Decision Tree

1. **Is the question about what to own and in what proportion?** Route to `asset-allocation`.
2. **Is the question about systematic factor tilts or smart beta?** Route to `factor-exposure`.
3. **Is the question about downside protection or insurance?** Route to `hedging-architecture`.
4. **Is the question about taxes, harvesting, or account placement?** Route to `tax-optimization`.
5. **Does the question span multiple construction concerns?** Handle here, routing to each specialist in sequence.
6. **Are two specialists giving conflicting recommendations?** Resolve here using the integration framework below.

## Integration Framework

### The Construction Sequence

When building a portfolio from scratch, follow this sequence. Each step feeds the next:

```
1. ALLOCATE  →  Strategic allocation based on risk tolerance, time horizon, regime
2. TILT      →  Factor exposures layered onto the allocation (value, momentum, quality)
3. HEDGE     →  Protection architecture matched to portfolio risk profile
4. OPTIMIZE  →  Tax-efficient implementation across account types
```

Never reverse this sequence. Tax optimization does not drive allocation. Hedging does not determine factor exposure. Start from the investment thesis and work toward implementation.

### Conflict Resolution

Common conflicts between specialists and how to resolve them:

| Conflict | Resolution |
|----------|------------|
| Allocation wants to rebalance, tax says harvesting window is open | Tax-loss harvest first, then rebalance with the proceeds |
| Factor exposure wants high turnover, tax wants low turnover | Constrain factor implementation to tax-efficient vehicles (ETFs in taxable, active in tax-deferred) |
| Hedging costs reduce expected returns, allocation targets a return level | Size hedging to risk budget, not return target — protection is non-negotiable |
| Asset location conflicts with factor tilt placement | Factor tilts in tax-advantaged accounts where turnover is free |

### Portfolio Health Checklist

When reviewing any portfolio, assess across all four dimensions:

- **Allocation**: Does the allocation match the stated risk tolerance and time horizon? Is it regime-appropriate?
- **Factor exposure**: Are factor tilts intentional or accidental? Is there uncompensated risk?
- **Hedging**: Is tail risk addressed? What is the maximum drawdown scenario? Is hedging cost-efficient?
- **Tax efficiency**: Are assets in the right account types? Is harvesting being captured? Are gains being managed?

### Position Sizing Integration

Position sizing lives at the intersection of all four skills:

1. **Allocation** sets the asset class weight (e.g., 40% equities)
2. **Factor exposure** determines the tilt within that weight (e.g., value + quality within equities)
3. **Hedging** may reduce effective exposure (e.g., put protection reduces net equity beta)
4. **Tax optimization** may shift implementation across accounts (e.g., REITs in IRA, index funds in taxable)

The final position is the sum of all four layers. No single layer should be designed in isolation.

## Guiding Principles

1. **Diversification is the only free lunch.** Markowitz was right. Combine assets with low correlation to improve risk-adjusted returns without sacrificing expected return.
2. **Risk drives allocation, not return.** Set risk first. Return is the consequence of bearing risk intelligently. Never reverse this — chasing return leads to uncompensated risk.
3. **Implementation matters as much as strategy.** A great allocation in the wrong account type, without tax awareness, without hedging, underperforms a mediocre allocation that is well-implemented.
4. **Simplicity is a feature.** Every added layer of complexity must justify its cost in fees, taxes, cognitive overhead, and execution risk. The burden of proof is on complexity.
5. **No financial advice.** This is an analytical framework. Present analysis with appropriate caveats. The user makes all decisions.

## Curriculum Order

For building portfolio construction literacy from scratch, follow this sequence:

1. **asset-allocation** — Foundation. Asset allocation drives the majority of portfolio returns and risk. Strategic allocation based on risk tolerance, time horizon, and regime assessment is the single most consequential portfolio decision. Without this foundation, factor tilts, hedging, and tax optimization are optimizing within a broken structure.

2. **factor-exposure** — Second layer. Once the allocation framework is set, factor tilts (value, momentum, quality, size, low volatility) explain the systematic sources of return within each asset class. Understanding factor exposure prevents accidental bets and enables intentional portfolio tilts. Builds on allocation by explaining what drives returns within each asset class bucket.

3. **hedging-architecture** — Third layer. With allocation and factor exposure defined, hedging architecture protects the portfolio against tail events and drawdowns. Understanding put protection, tail hedging, and convexity design requires knowing what is being hedged (allocation) and what factor exposures amplify downside risk. Hedging cost is only meaningful relative to the portfolio it protects.

4. **tax-optimization** — Capstone. Tax optimization is the implementation layer that maximizes after-tax returns without distorting the investment thesis. Asset location, tax-loss harvesting, and direct indexing require understanding the full portfolio (allocation + factors + hedging) to make intelligent trade-offs between tax efficiency and investment objectives. Always the last step because tax should never drive strategy.

## Scope Boundaries

**This director handles**: All questions about portfolio-level construction decisions — asset allocation, factor exposure management, hedging architecture, tax optimization, rebalancing, portfolio health audits, and the integration of these elements into a coherent portfolio.

**Escalate to the Archon when**:
- The question involves macroeconomic regime assessment that informs allocation (route to regime-intelligence)
- The question involves security-level selection or valuation within an allocation bucket (route to value-quality)
- The question involves sourcing special-situations opportunities to include in the portfolio (route to special-situations)
- The question involves position-level risk management rather than portfolio-level construction (route to risk-architecture)
- The question involves asset-class-specific analysis rather than portfolio-level decisions (route to asset-universe)
- The question spans multiple investing subdomains and needs orchestrator-level coordination
