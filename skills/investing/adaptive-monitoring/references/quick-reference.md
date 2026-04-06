# Adaptive Monitoring — Quick Reference


## Quick Reference

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Return decomposition, what drove performance, alpha vs beta | `performance-attribution` | Attribution-specific methodology |
| Portfolio drift, when to trade, threshold triggers, tax-aware trades | `rebalancing-logic` | Rebalancing decision framework |
| Satellite data, web scraping, sentiment signals, alt data sources | `alt-data-monitoring` | Alternative data expertise |
| "Is my portfolio doing well?" (vague) | `performance-attribution` first | Must measure before acting |
| "Should I make changes?" (vague) | All three, in curriculum order | Needs holistic assessment |
| Risk budget breach or drawdown alert | `performance-attribution` then `rebalancing-logic` | Diagnose first, then act |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Attribution says "momentum factor working" but rebalancing says "cut winners" | Attribution wins, delay rebalance | Evidence of active regime overrides mechanical rules |
| Rebalancing says "sell" but alt data says "positive signal" | Rebalancing wins unless signal is very strong | Discipline beats conviction in most cases |
| Alt data says "act now" but attribution says "strategy is working" | Attribution wins | Don't fix what isn't broken; alt data has higher false positive rate |
| Attribution shows thesis failure and rebalancing threshold hit | Both agree — act immediately | Convergent signals demand action |
