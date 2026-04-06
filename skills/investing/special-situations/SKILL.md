---
name: special-situations
description: >
  Route special-situations investing analysis to the appropriate specialist skill. Use when the user
  wants to analyze spinoffs, insider transactions, complexity-driven mispricings, or event-driven
  opportunities such as merger arbitrage, activist campaigns, or distressed investing.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Special Situations — The Opportunity Router

Route the user's investing question to the correct specialist skill based on the type of special situation they are analyzing.

## Routing Table

| Signal / Topic | Route To |
|---|---|
| Spinoffs, split-offs, carve-outs, corporate restructurings, rights offerings, bankruptcy, distressed debt, Form 10-12B | `spinoffs-restructuring` |
| Insider buying, insider selling, Form 4, 10b5-1 plans, Section 16, cluster buys, insider ownership | `insider-signals` |
| Holding company discounts, sum-of-parts, stub trades, closed-end fund discounts, multi-class shares, net-nets, conglomerate discount | `complexity-premium` |
| Merger arbitrage, activist investing, 13D filings, catalysts, event-driven, hostile takeovers, index additions, FDA decisions | `event-driven` |

## Routing Rules

1. Read the user's query and identify the primary special-situation type.
2. If the query spans multiple categories (e.g., "an activist pushing for a spinoff"), route to the category that represents the primary analytical framework needed — in that example, `event-driven` for the activist angle, then reference `spinoffs-restructuring` for the spinoff mechanics.
3. If the query is general ("tell me about special situations investing"), provide a brief overview of all four sub-domains and ask the user which area they want to explore.
4. Load the target skill with `Read` and follow its methodology.

## Multi-Skill Questions

Many special-situations questions require synthesizing across multiple specialist skills. Common combinations:

1. **Spinoffs + Insider Signals**: "Is this spinoff worth buying?"
   - Read `spinoffs-restructuring` for the structural mechanics — forced selling, index exclusion, institutional dumping
   - Read `insider-signals` for whether insiders at the parent or spinoff are buying
   - Synthesize: A spinoff with heavy insider buying is the strongest special-situations signal. Forced selling creates the discount; insider buying confirms the value.

2. **Spinoffs + Event-Driven**: "An activist is pushing for a spinoff — how do I play it?"
   - Read `event-driven` for the activist campaign framework, 13D analysis, and catalyst timeline
   - Read `spinoffs-restructuring` for the spinoff mechanics and post-separation valuation
   - Synthesize: The activist provides the catalyst; spinoff analysis determines the post-event value. Size the position based on probability-weighted outcomes.

3. **Complexity Premium + Insider Signals**: "This holding company trades at a 40% discount — is it a trap?"
   - Read `complexity-premium` for the structural discount framework and catalyst identification
   - Read `insider-signals` for whether insiders are buying, which signals whether the discount will narrow
   - Synthesize: Persistent discounts without insider buying often remain persistent. Insider purchases in discounted structures signal management alignment with value realization.

4. **Full Special Situations Stack**: "Evaluate this distressed company with activist involvement and insider buying."
   - Read all four skills in curriculum order
   - Build the complete picture: restructuring mechanics + insider conviction + complexity analysis + event catalyst
   - This four-dimensional assessment captures the full special-situations opportunity set

## Curriculum Order

For building special-situations literacy from scratch, follow this sequence:

1. **spinoffs-restructuring** — Foundation. Corporate restructurings create the most reliable source of mispricing because they produce forced, non-economic selling. Understanding the mechanics of spinoffs, split-offs, and bankruptcy reorganizations provides the structural foundation for all special-situations analysis. Without this, you cannot identify the source of the mispricing.

2. **insider-signals** — Second layer. Once you understand what creates forced selling and structural mispricing, you need a confirmation signal. Insider transactions — especially cluster buys, open-market purchases, and Form 4 filings — reveal whether the people with the best information think the mispricing is real. Builds on spinoff knowledge by providing a validation layer.

3. **complexity-premium** — Third layer. Structural complexity (holding company discounts, stub trades, multi-class shares, net-nets) creates persistent mispricings that require analytical patience. This skill requires understanding restructuring mechanics and insider signals to determine whether a discount will narrow or persist indefinitely.

4. **event-driven** — Capstone. Merger arbitrage, activist campaigns, and catalyst-driven investing require integrating all prior skills. An event provides the catalyst that collapses a structural discount. This skill requires understanding restructuring mechanics (what the event produces), insider signals (who is betting on it), and complexity premiums (what discount is being closed) to size and time positions correctly.

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Insider buying in a spinoff but complexity analysis says discount is structural | Consult both `spinoffs-restructuring` and `insider-signals` — weight insider buying more heavily if it is a cluster buy by multiple insiders | Insider cluster buys in structural discounts are among the highest-conviction special-situations signals; insiders see the catalyst you don't |
| Event-driven says the activist will win but insider signals show insiders selling | Insider selling wins as the caution signal | Insiders know the business better than activists; selling during an activist campaign suggests the activist's thesis may be flawed |
| Spinoff analysis says "buy" but event-driven says the merger arb spread is more attractive | Compare risk-adjusted returns — spinoffs have higher variance but higher upside; merger arb has more predictable but capped returns | Match the opportunity to portfolio needs: merger arb for steady compounding, spinoffs for outsized gains with higher uncertainty |
| Complexity premium says "deep discount" but insider signals are silent (no transactions) | Absence of insider buying is not bearish — it is inconclusive; rely on complexity-premium analysis but size conservatively | Insiders may be restricted, uninformed about market price, or simply not transacting. Lack of signal is not a negative signal. |

**General rule**: Insider signals > structural analysis when they conflict. People with asymmetric information acting with their own capital is the strongest signal in special-situations investing. But absence of insider activity is neutral, not negative.

## Scope Boundaries

**This director handles**: All questions about special-situations investing — spinoffs, restructurings, insider transactions, structural complexity discounts, merger arbitrage, activist campaigns, and event-driven catalysts.

**Escalate to the Archon when**:
- The question involves valuation methodology beyond special-situations context (route to value-quality)
- The question involves macro regime assessment that affects the special situation (route to regime-intelligence)
- The question involves portfolio-level sizing or allocation of special-situations positions (route to portfolio-construction)
- The question spans multiple investing subdomains and needs orchestrator-level coordination
- The user needs risk management frameworks for special-situations positions (route to risk-architecture)

## Cross-Domain Connections

- **Game-theory/information-economics/signaling-screening**: Insider buying is a Spence signaling game — costly, verifiable transactions that credibly reveal private information about firm quality. The signaling-screening framework formalizes why insider purchases are more informative than sales (asymmetric signaling costs).
- **Game-theory/mechanism-design/auction-theory**: M&A bidding wars are ascending auctions with common-value elements. Winner's curse directly predicts acquirer overpayment in contested deals. Auction theory explains why competitive bids extract more value for target shareholders.

## Sub-Skill Locations

```
special-situations/
  spinoffs-restructuring/SKILL.md   — Corporate actions that create forced selling and mispricing
  insider-signals/SKILL.md          — Reading insider transactions for informational content
  complexity-premium/SKILL.md       — Structural complexity that creates persistent discounts
  event-driven/SKILL.md             — Catalysts and arbitrage in corporate events
```
