---
name: algorithmic-game-theory
description: >
  Algorithmic game theory foundations covering computational complexity of equilibria, price of
  anarchy/stability, congestion games, potential games, and algorithmic mechanism design. Reference
  when asking whether equilibria can be computed, how much efficiency is lost from selfish behavior,
  or how to design computationally tractable mechanisms.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Algorithmic Game Theory — The Complexity Theorist

Where game theory meets theoretical computer science. Classical game theory proves equilibria *exist* (Nash 1950). Algorithmic game theory asks: *can we compute them?* The answer — generally no (PPAD-hard) — is one of the most important results in modern game theory. It means players can't be expected to find equilibria, mechanisms can't always be efficiently implemented, and we need new solution concepts. Grounded primarily in Nisan, Roughgarden, Tardos & Vazirani (2007) and Roughgarden (2016).

## Computational Complexity of Equilibria

### PPAD-Completeness of Nash Equilibrium

**The problem**: Given a game, find a Nash equilibrium.

**The result** (Daskalakis, Goldberg & Papadimitriou 2009; Chen, Deng & Teng 2009): Computing a Nash equilibrium in a two-player game is **PPAD-complete** — at least as hard as any problem in the complexity class PPAD.

**What PPAD means**: PPAD (Polynomial Parity Arguments on Directed graphs) captures problems where a solution is guaranteed to exist (by a parity argument or fixed-point theorem) but finding one may be computationally intractable. It's believed that PPAD ⊄ P — meaning no polynomial-time algorithm exists.

**Implications**:
- Players in complex games cannot generally be expected to compute Nash equilibria
- The Nash equilibrium concept, while mathematically elegant, may not predict behavior in computationally complex settings
- This motivates: (1) studying special cases where computation is tractable, (2) using weaker solution concepts like correlated equilibrium, (3) studying learning dynamics that converge to approximate equilibria

### When Nash IS Tractable

| Game Class | Complexity | Key Property |
|------------|-----------|--------------|
| **Two-player zero-sum** | Polynomial (linear programming) | Minimax theorem, LP duality |
| **Potential games** | Best-response converges (but may be exponential in worst case) | Exists an exact potential function |
| **Congestion games** | PLS-complete (finding pure NE) | Special structure of payoff functions |
| **Correlated equilibrium** | Polynomial (linear programming) | Weaker concept than Nash |
| **Graphical games (bounded treewidth)** | Polynomial in n (exponential in treewidth) | Sparse interaction structure |
| **Symmetric games** | Polynomial for constant # of strategies | Symmetry reduces dimensionality |

### Correlated Equilibrium

A **correlated equilibrium** (Aumann 1974, 1987) is a joint distribution over strategy profiles such that, when a mediator recommends an action to each player (drawn from the distribution), no player wants to deviate.

**Key advantage**: Computing a correlated equilibrium is a **linear program** — tractable even for large games. This makes CE a more computationally practical solution concept than Nash.

**Relationship to Nash**: Every Nash equilibrium is a correlated equilibrium (product distributions are a special case). CE allows coordination through correlation.

## Price of Anarchy and Stability

### The Efficiency Question

When selfish players optimize individually, how much worse is the outcome compared to socially optimal?

**Price of Anarchy (PoA)** (Koutsoupias & Papadimitriou 1999):
PoA = (cost of worst-case Nash equilibrium) / (cost of social optimum)

**Price of Stability (PoS)**:
PoS = (cost of best Nash equilibrium) / (cost of social optimum)

PoA ≥ PoS ≥ 1. When PoA = 1, selfishness causes no inefficiency (e.g., in dominant-strategy mechanisms).

### Selfish Routing (Roughgarden & Tardos 2002)

Pigou's example: Two routes from A to B. Route 1: travel time = 1 (constant). Route 2: travel time = x (congestion-dependent, where x is the fraction of traffic using it).

- **Social optimum**: Split traffic 1/2 on each route. Average travel time = 3/4.
- **Nash equilibrium**: All traffic uses Route 2 (since x < 1 is better than 1, until x = 1). Average travel time = 1.
- **Price of Anarchy** = 1/(3/4) = 4/3.

**Key result**: For linear latency functions, PoA ≤ 4/3. For polynomial latency of degree d, PoA grows with d but remains bounded.

**Braess's paradox**: Adding a new road to a network can *increase* total travel time at equilibrium. Selfish routing on the augmented network is worse than without the new road. Counterintuitive but proven: more options can hurt when behavior is uncoordinated.

### The Smoothness Framework (Roughgarden 2015)

A unified technique for bounding PoA across game classes. A game is (λ, μ)-smooth if for all strategy profiles s, s*:
Σᵢ cᵢ(sᵢ*, s₋ᵢ) ≤ λ · C(s*) + μ · C(s)

This implies PoA ≤ λ/(1-μ). The smoothness framework applies to pure, mixed, correlated, and coarse correlated equilibria — making PoA bounds robust to the equilibrium concept used.

## Congestion and Potential Games

### Congestion Games (Rosenthal 1973)

Players choose subsets of shared resources. The cost of each resource depends only on how many players use it. Fundamental model for network routing, facility location, and load balancing.

**Key result**: Every congestion game has a **pure Nash equilibrium** (proven via an exact potential function). Best-response dynamics converge, but convergence may take exponentially many steps.

### Potential Games (Monderer & Shapley 1996)

A game has an **exact potential function** Φ if, for every player i and every unilateral deviation, the change in i's payoff equals the change in Φ.

Properties: Every potential game has a pure NE (minimizer/maximizer of Φ). Best-response dynamics converge to NE. Congestion games are the canonical example.

**Identification**: A game is a potential game iff the "improvement paths" form a DAG (no improvement cycles).

## Algorithmic Mechanism Design (AMD)

Mechanism design assumes the mechanism can be computed efficiently. AMD asks: what if the mechanism's allocation and payment rules must be *polynomial-time computable*?

**Key tension**: VCG is truthful and efficient, but computing the efficient allocation may be NP-hard (e.g., combinatorial auctions). If we approximate the allocation, truthfulness can break.

**Maximal-in-range mechanisms**: Restrict the allocation rule to a subset of allocations over which optimization is tractable. VCG payments applied to this restricted range preserve truthfulness but sacrifice optimality.

**Monotone allocation algorithms**: For single-parameter settings, an allocation rule is implementable (admits truthful payments) if and only if it is monotone (more bidding → more winning). This characterization enables the design of polynomial-time truthful mechanisms.

## Sources

Read `references/sources.md` for the full bibliography — primary texts (Nisan et al., Roughgarden), key papers, and the PPAD-completeness results.

## When This Applies

- Assessing whether an equilibrium concept is computationally feasible for a given game
- Quantifying efficiency loss from selfish/decentralized behavior
- Designing mechanisms that are both incentive-compatible and computationally tractable
- Analyzing network routing, traffic, or resource allocation under selfish agents
- Understanding when Nash equilibrium predictions are undermined by computational complexity
