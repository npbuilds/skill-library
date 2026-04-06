# Position Sizing — Quick Reference


## Quick Reference

| Fraction | Expected Growth (% of Kelly) | Drawdown Reduction | Use When |
|----------|------------------------------|-------------------|----------|
| Full Kelly (1.0) | 100% | Baseline | Never in practice |
| Half Kelly (0.5) | 75% | ~50% reduction | High confidence in edge estimate |
| Quarter Kelly (0.25) | ~56% | ~75% reduction | Moderate confidence, or correlated bets |
| Tenth Kelly (0.1) | ~34% | ~90% reduction | Low confidence, exploratory positions |

## Quick Reference

| Strategy | Max loss per position | Rationale |
|----------|----------------------|-----------|
| Core holdings | 3-5% of portfolio | High conviction, long time horizon |
| Tactical trades | 1-2% of portfolio | Moderate conviction, defined catalyst |
| Speculative/binary | 0.25-0.5% of portfolio | Low probability, high payoff |
| Hedges | N/A (premium is the cost) | Insurance cost, not a loss budget |

## Quick Reference

| Factor | Weak Conviction (small size) | Strong Conviction (large size) |
|--------|------------------------------|-------------------------------|
| Thesis quality | Pattern recognition, analogy | Deep fundamental understanding of causation |
| Variant perception | Consensus-adjacent | Clearly differentiated from market consensus |
| Asymmetry | Symmetric upside/downside | Highly asymmetric (much more upside) |
| Catalyst clarity | Vague timing | Specific catalyst with defined timeline |
| Downside understanding | Unclear what could go wrong | Exhaustive bear case that you've specifically rebutted |
| Edge persistence | Edge might be arbitraged away quickly | Structural edge (behavioral, informational, analytical) |

## Quick Reference

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Position is profitable | Consider adding (pyramiding) | The market is confirming your thesis; let winners run |
| Position is at entry | Hold at current size | No new information |
| Position is at a small loss | Reduce or hold, depending on thesis | Mild negative signal |
| Position is at a large loss | Reduce or exit | Strong negative signal; the market knows something you don't |

## Quick Reference

| Heat Level | Total risk | Action |
|------------|-----------|--------|
| Cool | < 5% portfolio | Room to add positions; may be under-invested |
| Comfortable | 5-10% portfolio | Normal operating range for most strategies |
| Warm | 10-15% portfolio | Approaching limits; only add if conviction is high |
| Hot | 15-20% portfolio | At capacity; no new positions unless one is closed |
| Overheated | > 20% portfolio | Reduce immediately; you're one bad week from trouble |

## Summary Decision Tree

```
Start
  |
  v
R:R >= 2:1? --No--> Pass on trade
  |
  Yes
  v
Calculate Kelly ceiling (fractional)
  |
  v
Calculate risk-budget size
  |
  v
Take the SMALLER of Kelly and risk-budget
  |
  v
Adjust for volatility (size inversely to vol)
  |
  v
Adjust for conviction (0.5x to 1.5x)
  |
  v
Check portfolio heat --Overheated--> Defer or reduce
  |
  OK
  v
Enter position, document everything
```
