# Special Situations — Quick Reference


## Routing Table

| Signal / Topic | Route To |
|---|---|
| Spinoffs, split-offs, carve-outs, corporate restructurings, rights offerings, bankruptcy, distressed debt, Form 10-12B | `spinoffs-restructuring` |
| Insider buying, insider selling, Form 4, 10b5-1 plans, Section 16, cluster buys, insider ownership | `insider-signals` |
| Holding company discounts, sum-of-parts, stub trades, closed-end fund discounts, multi-class shares, net-nets, conglomerate discount | `complexity-premium` |
| Merger arbitrage, activist investing, 13D filings, catalysts, event-driven, hostile takeovers, index additions, FDA decisions | `event-driven` |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Insider buying in a spinoff but complexity analysis says discount is structural | Consult both `spinoffs-restructuring` and `insider-signals` — weight insider buying more heavily if it is a cluster buy by multiple insiders | Insider cluster buys in structural discounts are among the highest-conviction special-situations signals; insiders see the catalyst you don't |
| Event-driven says the activist will win but insider signals show insiders selling | Insider selling wins as the caution signal | Insiders know the business better than activists; selling during an activist campaign suggests the activist's thesis may be flawed |
| Spinoff analysis says "buy" but event-driven says the merger arb spread is more attractive | Compare risk-adjusted returns — spinoffs have higher variance but higher upside; merger arb has more predictable but capped returns | Match the opportunity to portfolio needs: merger arb for steady compounding, spinoffs for outsized gains with higher uncertainty |
| Complexity premium says "deep discount" but insider signals are silent (no transactions) | Absence of insider buying is not bearish — it is inconclusive; rely on complexity-premium analysis but size conservatively | Insiders may be restricted, uninformed about market price, or simply not transacting. Lack of signal is not a negative signal. |

## Sub-Skill Locations

```
special-situations/
  spinoffs-restructuring/SKILL.md   — Corporate actions that create forced selling and mispricing
  insider-signals/SKILL.md          — Reading insider transactions for informational content
  complexity-premium/SKILL.md       — Structural complexity that creates persistent discounts
  event-driven/SKILL.md             — Catalysts and arbitrage in corporate events
```
