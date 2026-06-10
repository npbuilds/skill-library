# Collector — Quick Reference


## Phase 2 — Route

| Question Signal | Primary Route | Supporting Route |
|---|---|---|
| Specific asset class named (comics, cards, art, wine, etc.) | matching `vertical/<asset>/` director | the horizontal skill that the asset-specific question depends on |
| Discipline named without asset class | matching `horizontal/<discipline>/` skill | optional vertical for illustrative examples |
| Multi-asset portfolio question | `horizontal/portfolio-allocation/` | each vertical holding |
| Authentication question, any asset | `horizontal/authentication-provenance/` + asset-specific `vertical/<asset>/` | `horizontal/fraud-intelligence/` for red flags |
| Pricing / comp question | `horizontal/market-intelligence/` + the asset's vertical | `horizontal/buying-mechanics/` if executing |
| Insurance / storage question | `horizontal/insurance-risk/` + `horizontal/storage-preservation/` | jurisdictional notes from `horizontal/tax-estate-legal/` |
| Tax / estate / charitable question | `horizontal/tax-estate-legal/` | `horizontal/vetting-services/` for qualified-appraisal mechanics |
| Counterfeit suspicion | `horizontal/fraud-intelligence/` + `horizontal/authentication-provenance/` + asset-specific vertical | named scandals (Knoedler, Kurniawan, Mastro/Wagner) for pattern matching |
| Sourcing / discovery | `horizontal/discovery-sourcing/` | channel-asset fit table |
| Selling / deaccessioning | `horizontal/selling-deaccessioning/` + `horizontal/tax-estate-legal/` | `horizontal/market-intelligence/` for timing |

## Formula / Pseudocode

```
Connoisseur ─── [Topic]
[3–6 lines: judgment, condition, eye, authenticity, taste]

Allocator ─── [Topic]
[3–6 lines: returns, comps, indices, tax, structural friction]
```
