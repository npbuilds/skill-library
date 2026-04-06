# Liquidity Topology — Quick Reference


## Quick Reference

| Spread Behavior | Interpretation |
|---|---|
| Tight and stable | Normal liquidity, low information asymmetry, confident market makers |
| Gradually widening | Market makers reducing risk appetite. Early warning of stress. Increase attention. |
| Sharply widening | Acute stress. Market makers pulling back or withdrawing. Information asymmetry spiking. Adverse selection fears dominant. |
| Bid disappears entirely | Market maker withdrawal. Liquidity vacuum. Prices will gap. This is the precursor to flash crash dynamics. |
| Spread tightens after widening | Confidence returning. Market makers re-engaging. Recovery phase. |

## Quick Reference

| State | Characteristics | Appropriate Action |
|---|---|---|
| **Robust** | Tight spreads, deep book, balanced flow, low toxicity | Normal trading. Execute in size. Standard algorithms. |
| **Adequate** | Normal spreads, moderate depth, some flow imbalance | Standard trading but use patience. Slice large orders. Monitor for deterioration. |
| **Fragile** | Widening spreads, declining depth, elevated toxicity, HFTs reducing size | Reduce urgency. Use dark pools for large orders. Avoid market orders. Set wider stop-losses (tight stops will be hunted). |
| **Broken** | Extreme spreads, minimal depth, market maker withdrawal, circuit breakers triggering | Do not use market orders. Use limit orders only. Consider whether liquidity will return before acting. In a flash crash, panic selling at the worst moment is the primary wealth destruction mechanism. |
