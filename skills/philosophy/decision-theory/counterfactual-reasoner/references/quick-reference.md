# Counterfactual Reasoner — Quick Reference


## Quick Reference

| Rule | Why | Example |
|------|-----|---------|
| **Change one thing at a time** | Isolates the causal contribution of each factor | "What if we'd launched a month earlier?" not "What if everything were different?" |
| **Keep background conditions stable** | The counterfactual world should be as similar to the actual world as possible | If asking "what if we'd hired differently," don't also assume the market was different |
| **Respect causal structure** | Changes propagate forward in time, not backward | If asking "what if it rained?", don't assume the rain also changes yesterday's weather |
| **Consider multiple paths** | The same cause can produce different outcomes through different mechanisms | "If we'd raised prices, customers might have left OR perceived higher quality" |

## Quick Reference

| Finding | Causal Status | Confidence |
|---------|--------------|------------|
| Y would not have happened without X, and X reliably produces Y | X is a strong cause of Y | High |
| Y would not have happened without X, but X only sometimes produces Y | X is a contributing cause (necessary but not sufficient) | Moderate |
| Y might have happened anyway, but X made it more likely | X is a risk factor / probabilistic cause | Moderate |
| Y would have happened regardless of X | X is not a cause of Y (mere correlation or coincidence) | High |
| Cannot determine | Causal relationship is uncertain | Low — flag for further investigation |

## Formula / Pseudocode

```
Counterfactual: [what changes]
  → Immediate effect: [first consequence]
    → Second-order effect: [consequence of the consequence]
      → Downstream effect: [further propagation]
    → Alternative second-order: [another path the consequence could take]
```
