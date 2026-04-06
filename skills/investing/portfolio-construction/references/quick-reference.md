# Portfolio Construction — Quick Reference


## Skill Routing Table

| Request Type | Primary Skill | Supporting Skills | Why |
|-------------|--------------|-------------------|-----|
| Strategic allocation, tactical shifts, risk parity, glide paths | `asset-allocation` | `factor-exposure` (factor-aware allocation) | Core allocation framework and regime positioning |
| Factor tilts, smart beta, value/momentum/quality exposure | `factor-exposure` | `asset-allocation` (allocation context) | Factor selection, timing, and portfolio integration |
| Put protection, tail risk, hedging strategy, insurance | `hedging-architecture` | `asset-allocation` (what's being hedged) | Downside protection and convexity design |
| Tax-loss harvesting, asset location, direct indexing | `tax-optimization` | `asset-allocation` (rebalancing context) | After-tax return maximization |
| Full portfolio build from scratch | This director | All skills sequentially | Requires coordinated multi-skill construction |
| Portfolio review or audit | This director | All skills as needed | Cross-cutting analysis of existing portfolio |
| Rebalancing decisions | `asset-allocation` + `tax-optimization` | `factor-exposure` (factor drift) | Rebalancing involves both allocation and tax |

## Quick Reference

| Conflict | Resolution |
|----------|------------|
| Allocation wants to rebalance, tax says harvesting window is open | Tax-loss harvest first, then rebalance with the proceeds |
| Factor exposure wants high turnover, tax wants low turnover | Constrain factor implementation to tax-efficient vehicles (ETFs in taxable, active in tax-deferred) |
| Hedging costs reduce expected returns, allocation targets a return level | Size hedging to risk budget, not return target — protection is non-negotiable |
| Asset location conflicts with factor tilt placement | Factor tilts in tax-advantaged accounts where turnover is free |

## Formula / Pseudocode

```
1. ALLOCATE  →  Strategic allocation based on risk tolerance, time horizon, regime
2. TILT      →  Factor exposures layered onto the allocation (value, momentum, quality)
3. HEDGE     →  Protection architecture matched to portfolio risk profile
4. OPTIMIZE  →  Tax-efficient implementation across account types
```
