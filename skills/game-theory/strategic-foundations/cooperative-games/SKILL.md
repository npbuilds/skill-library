---
name: cooperative-games
description: >
  Cooperative game theory foundations for coalition analysis, fair allocation, bargaining, and
  matching. Reference when evaluating how groups should form, how to fairly divide value,
  how to structure negotiations, or how to design stable matching systems. Use when analysis
  requires binding agreements, coalition reasoning, or normative fairness concepts.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Cooperative Games — The Coalitions

Cooperative game theory asks: when players can make binding agreements, how should they cooperate, and how should they divide the gains? Where classical (non-cooperative) game theory predicts what *will* happen, cooperative theory prescribes what *should* happen — given axioms about fairness, stability, or efficiency. Grounded primarily in Maschler/Solan/Zamir (2013) Ch.13-18, Osborne & Rubinstein (1994) Part IV, and Roth & Sotomayor (1990).

## The Cooperative Framework

A **coalitional game** (N, v) specifies:
- **N** = {1, 2, ..., n}: the set of players
- **v**: a **characteristic function** mapping each coalition S ⊆ N to the value v(S) that coalition can guarantee for its members

The central question: given v, how should the grand coalition N divide v(N) among its members?

**Transferable utility (TU)**: value can be freely redistributed within coalitions (money, divisible goods). Most cooperative theory assumes TU.

**Non-transferable utility (NTU)**: payoffs are not freely redistributable (e.g., matching — you can't transfer the "value" of being matched with your preferred partner).

## Core Solution Concepts

### The Core (Gillies 1953)

The set of allocations where no coalition can do better on its own.

**Definition**: An allocation x = (x₁, ..., xₙ) is in the core if:
- **Efficiency**: Σxᵢ = v(N) (the full value is distributed)
- **Coalition rationality**: Σᵢ∈S xᵢ ≥ v(S) for every coalition S (no group can profitably deviate)

**Properties**:
- May be empty (not all games have a non-empty core)
- When non-empty, may contain many allocations — the core doesn't select a unique outcome
- **Bondareva-Shapley theorem**: the core is non-empty if and only if the game is "balanced"

**Intuition**: The core captures *stability* — no group wants to leave the grand coalition. If the core is empty, full cooperation is inherently unstable.

### Shapley Value (Shapley 1953)

The unique allocation satisfying four axioms: efficiency, symmetry, dummy player, and additivity.

**Formula**: Player i's Shapley value is their expected marginal contribution, averaged over all possible orderings of players:

φᵢ(v) = Σ over all orderings: [v(S ∪ {i}) - v(S)] / n!

where S is the set of players who precede i in the ordering.

**Intuition**: Imagine players arriving one at a time in a random order. Each player receives their marginal contribution — the additional value they bring. The Shapley value is this marginal contribution averaged over all possible arrival orders.

**Properties**:
- Always exists and is unique
- May lie outside the core (Shapley value isn't always stable)
- Computable in polynomial time for many game structures (convex games, weighted voting games)

**Applications**:
- Cost allocation (airport runway costs, shared infrastructure)
- Voting power measurement (Shapley-Shubik power index)
- Attribution in ML (SHAP values for feature importance are literally Shapley values)
- Fair division of joint venture profits

### Nucleolus (Schmeidler 1969)

Minimizes the maximum "unhappiness" of any coalition — the allocation that makes the most dissatisfied coalition as satisfied as possible.

**Properties**:
- Always exists, always unique, always in the core (when the core is non-empty)
- Computationally harder than Shapley value (requires solving a sequence of linear programs)
- Captures the "egalitarian" intuition — minimize the worst-case complaint

Read `references/solution-concepts-cooperative.md` for formal definitions and axiomatic characterizations of all cooperative solution concepts.

## Bargaining Theory

When two players negotiate over a surplus, bargaining theory provides normative solutions.

### Nash Bargaining Solution (Nash 1950)

Maximizes the product of players' gains over the disagreement point:

max (u₁ - d₁)(u₂ - d₂)

where d = (d₁, d₂) is the **disagreement point** (what each player gets if negotiation fails).

**Axioms**: efficiency, symmetry, independence of irrelevant alternatives, invariance to affine transformations.

**Key insight**: The disagreement point — your **BATNA** (best alternative to negotiated agreement) — is the most important factor in bargaining. A better outside option means a better negotiated outcome.

### Rubinstein Bargaining Model (1982)

Non-cooperative foundation for Nash bargaining. Two players alternate offers; delay is costly (discount factor δ < 1).

**Result**: Unique subgame perfect equilibrium where the first mover offers the split that makes the other player indifferent between accepting and waiting. As δ → 1 (patience increases), the split approaches 50-50.

**Key insight**: Provides a non-cooperative justification for the cooperative Nash bargaining solution. Patience is power — the more patient player gets a larger share.

### Kalai-Smorodinsky Solution (1975)

Equalizes the ratio of each player's gain to their maximum possible gain. Replaces Nash's "independence of irrelevant alternatives" axiom with **monotonicity** — if the feasible set expands in a way that benefits player i, player i's payoff should not decrease.

## Matching Theory

Read `references/matching-and-fairness.md` for detailed coverage of matching algorithms, real-world deployments (NRMP, school choice, kidney exchange), and fair division protocols.

Two-sided matching: agents on two sides of a market are matched to each other.

### Gale-Shapley Deferred Acceptance (1962)

**Algorithm**: One side proposes, the other side tentatively accepts the best offer and rejects others. Rejected proposers propose to their next choice. Repeat until stable.

**Result**: Always produces a stable matching (no pair prefers each other to their assigned matches). The proposing side gets their best stable match; the receiving side gets their worst.

**Properties**:
- Strategy-proof for the proposing side (truth-telling is dominant)
- NOT strategy-proof for the receiving side (they may benefit from misreporting preferences)

### Real-World Deployments

| Application | Mechanism | Scale | Source |
|-------------|-----------|-------|--------|
| US medical residency (NRMP) | Roth-Peranson (DA variant) | ~35,000 matches/year | Roth & Peranson (1999) |
| School choice (Boston, NYC) | Deferred acceptance | ~80,000 students/year (NYC) | Abdulkadiroglu & Sonmez (2003) |
| Kidney exchange | Top trading cycles + chains | ~550 transplants/year (US) | Roth, Sonmez & Unver (2004) |

## Fair Division

How to divide a resource among agents with different preferences.

**Envy-freeness**: No agent prefers another agent's allocation to their own.
**Proportionality**: Each of n agents gets at least 1/n of the total value (by their own valuation).
**Efficiency (Pareto optimality)**: No reallocation can make someone better off without making another worse off.

**Key impossibility**: For indivisible goods, envy-free allocation may not exist. Approximate solutions (envy-free up to one good, EF1) are guaranteed and computable.

**Cake-cutting**: For divisible goods, the moving-knife procedure and Selfridge-Conway protocol achieve envy-free division for 2 and 3 players respectively. For n players, Aziz & Mackenzie (2016) proved a bounded envy-free protocol exists.

## Sources

Read `references/sources.md` for the full bibliography grounding this skill — primary texts (Maschler/Solan/Zamir, Osborne & Rubinstein, Roth & Sotomayor), key papers on Shapley value, bargaining, matching, and fair division.

## When This Applies

- Dividing costs, profits, or resources among coalition members
- Evaluating whether a cooperative arrangement is stable (will anyone defect?)
- Structuring negotiations (identifying BATNAs, designing bargaining protocols)
- Designing matching markets (school choice, residency matching, organ allocation)
- Measuring voting power or influence in weighted committees
- Any situation where binding agreements are possible and fairness matters

## Cross-Domain Connections

- **Philosophy/political-philosophy**: Fair division and the Shapley value formalize questions about distributive justice. The core of a cooperative game tells you which allocations are stable — political philosophy asks which are *just*. Consult `political-philosophy/rights-reasoner` for the normative framework behind coalition bargaining.
- **Philosophy/ethics**: Cooperative game solutions (Nash bargaining, Kalai-Smorodinsky) embed different fairness axioms — each implicitly answers an ethical question about what constitutes a "fair" outcome.
