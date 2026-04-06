---
name: matching-markets
description: >
  Market design foundations for matching and allocation without prices. Reference when designing
  or analyzing matching systems, two-sided markets, assignment mechanisms, or allocation rules.
  Use when the problem involves matching agents to agents, agents to objects, or allocating
  indivisible resources where monetary transfers are limited or absent.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Matching Markets — The Matchmaker

The theory and practice of designing markets where prices alone cannot clear the market — because goods are indivisible, money is restricted, or preferences are heterogeneous in ways that prices can't capture. School choice, medical residencies, kidney exchange, and housing allocation are the canonical applications. Grounded primarily in Roth & Sotomayor (1990), Roth (2015), and Abdulkadiroglu & Sonmez (2003).

## The Design Problem

Traditional markets use prices: supply meets demand at the market-clearing price. Matching markets fail this model because:
- **Indivisibility**: You can't get half a school seat or half a kidney
- **Transfer restrictions**: You can't (or shouldn't) buy a transplant organ or a residency position
- **Heterogeneous preferences**: A school isn't just "good" or "bad" — different families value different schools differently
- **Two-sided preferences**: Both sides must agree — a student wants a school, but the school has preferences over students

The designer must choose an **allocation mechanism** — an algorithm that takes preference reports and outputs a matching.

## Key Properties of Mechanisms

| Property | Definition | Why It Matters |
|----------|-----------|---------------|
| **Stability** | No unmatched pair prefers each other to their assignments | Prevents justified envy; markets unravel without stability |
| **Strategy-proofness** | Truth-telling is a dominant strategy for participants | Participants don't need to game the system; levels the playing field |
| **Pareto efficiency** | No reallocation makes someone better off without making another worse off | No wasted opportunities |
| **Individual rationality** | No one is worse off than being unmatched | Participation is voluntary |

**The fundamental tension**: No mechanism can be stable, strategy-proof for all participants, and Pareto efficient simultaneously. Every practical mechanism sacrifices at least one property.

## Core Mechanisms

### Deferred Acceptance (DA) — Gale & Shapley 1962

The workhorse of matching market design.

**Student-proposing DA**:
- Students propose to their top-choice school
- Schools tentatively hold the best applicants up to capacity, reject others
- Rejected students propose to their next choice
- Repeat until no rejections

**Properties**: Stable, strategy-proof for proposing side, produces proposer-optimal stable matching. NOT strategy-proof for the receiving side.

### Top Trading Cycles (TTC) — Shapley & Scarf 1974

Each agent "owns" a position. Agents point to the agent who owns their most-preferred position. Cycles are identified and executed (agents in a cycle trade). Remove traded agents, repeat.

**Properties**: Strategy-proof for all participants, Pareto efficient, but NOT stable (violated justified envy is possible). Used when efficiency for one side matters more than two-sided stability.

### Serial Dictatorship

Agents take turns choosing in a fixed order. The first agent gets their top choice, the second gets their top choice among remaining, etc.

**Properties**: Strategy-proof, Pareto efficient, extremely simple. But the ordering is arbitrary, creating fairness concerns. Random Serial Dictatorship (RSD) randomizes the ordering.

### Probabilistic Serial (PS) — Bogomolnaia & Moulin 2001

Agents simultaneously "eat" their most-preferred remaining object at equal speed. When an object is fully consumed, agents move to their next choice.

**Properties**: Ordinally efficient (no stochastic dominance improvement), envy-free in expectation. Not strategy-proof, but manipulations are limited and require substantial information.

## Landmark Deployments

Read `references/market-design-cases.md` for detailed case studies.

| Market | Mechanism | Year | Scale | Key Innovation |
|--------|-----------|------|-------|---------------|
| NRMP (US medical residencies) | Applicant-proposing DA (Roth-Peranson) | 1952/1998 redesign | ~35,000/year | Couples matching; supplemental lists |
| NYC school choice | Student-proposing DA | 2003 | ~80,000/year | Replaced congested system where 30,000 students were unmatched |
| Boston school choice | Student-proposing DA (replaced Boston mechanism) | 2005 | ~4,000/year | Eliminated strategic disadvantage for unsophisticated families |
| Kidney exchange (US) | Cycle/chain optimization | 2004+ | ~550 transplants/year | Non-simultaneous altruistic donor chains |
| Teacher assignment (multiple countries) | Various DA/TTC variants | 2010s+ | Varies | Adapted for institutional constraints |

## Design Principles (Roth 2008)

Successful matching markets are:

1. **Thick**: Enough participants on both sides for good matches. Design must attract participation.
2. **Uncongested**: Participants have enough time to evaluate options. Mechanisms must be computationally efficient and informationally manageable.
3. **Safe**: Participants can reveal preferences honestly without penalty. Strategy-proofness creates safety.

Markets that lack these properties **unravel** — transactions happen earlier and earlier (before information is available), matches deteriorate, and participants game the system.

## Matching with Transfers (Assignment Games)

When money can be used, matching becomes an assignment game (Shapley & Shubik 1971). The core is always non-empty and corresponds to competitive equilibrium prices. Each stable matching has an associated price vector.

**Applications**: Labor markets (wages = transfers), housing markets (rent = transfers), procurement (bids = transfers). The assignment game unifies matching theory with competitive equilibrium theory.

## Sources

Read `references/sources.md` for the full bibliography — primary texts (Roth & Sotomayor, Abdulkadiroglu & Sonmez), key papers, and applied references.

## When This Applies

- Designing allocation systems where prices don't or can't clear the market
- School choice, residency matching, organ exchange, or housing allocation
- Evaluating tradeoffs between stability, efficiency, and strategy-proofness
- Two-sided platforms where both sides have preferences (job markets, dating, roommate matching)
- Any resource allocation problem with indivisible goods and limited transfers
