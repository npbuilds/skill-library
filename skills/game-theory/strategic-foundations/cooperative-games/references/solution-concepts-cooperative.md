# Cooperative Solution Concepts — Formal Definitions and Axiomatic Foundations

## The Core

### Formal Definition

For a TU game (N, v), the **core** is:

C(v) = { x ∈ ℝⁿ : Σᵢ∈N xᵢ = v(N) and Σᵢ∈S xᵢ ≥ v(S) for all S ⊆ N }

### Existence — Bondareva-Shapley Theorem

The core of (N, v) is non-empty if and only if the game is **balanced**.

A game is balanced if: for every balanced collection of coalitions (where each player is "covered" by coalitions with total weight 1), the weighted sum of coalition values does not exceed v(N).

**Convex games** (where v(S ∪ T) + v(S ∩ T) ≥ v(S) + v(T) for all S, T) always have non-empty cores. In convex games, the Shapley value is always in the core.

### Interpretation

The core answers: "Is the grand coalition stable?" If the core is empty, some subgroup will always want to break away. If it's non-empty, there exist division schemes that keep everyone (every coalition) at least as well off as they could achieve independently.

**Limitation**: The core may contain many allocations or none. It identifies stability but not a unique "fair" outcome.

## Shapley Value

### Formal Definition

For a TU game (N, v):

φᵢ(v) = Σ_{S⊆N\{i}} [ |S|!(|N|-|S|-1)! / |N|! ] × [v(S ∪ {i}) - v(S)]

### Axiomatic Characterization (Shapley 1953)

The Shapley value is the **unique** function φ: Games → ℝⁿ satisfying:

1. **Efficiency**: Σᵢ φᵢ(v) = v(N)
2. **Symmetry**: If i and j are interchangeable (v(S∪{i}) = v(S∪{j}) for all S not containing i,j), then φᵢ = φⱼ
3. **Dummy player**: If v(S∪{i}) = v(S) + v({i}) for all S, then φᵢ = v({i})
4. **Additivity**: φ(v + w) = φ(v) + φ(w)

### Alternative Axiomatization (Young 1985)

The Shapley value is also the unique function satisfying efficiency, symmetry, and **strong monotonicity** (if a player's marginal contributions all weakly increase, their allocation weakly increases).

### Computational Complexity

Computing exact Shapley values requires evaluating 2ⁿ coalitions in the worst case. For structured games:
- **Weighted voting games**: polynomial-time algorithms exist (via generating functions)
- **Graph games**: polynomial for bounded treewidth
- **General games**: #P-hard, but sampling-based approximation (random orderings) converges efficiently

### Shapley-Shubik Power Index

For weighted voting games [q; w₁, ..., wₙ] (quota q, weights wᵢ), the Shapley value measures each voter's power — the probability that a voter is **pivotal** (their vote changes the outcome) over random orderings.

**Example**: In the UN Security Council, the 5 permanent members have Shapley-Shubik index ~19.6% each, while the 10 non-permanent members share ~1.9% each. The veto power creates a massive power asymmetry despite having equal "votes" on paper.

## Nucleolus

### Formal Definition

For each allocation x, define the **excess** of coalition S as: e(S, x) = v(S) - Σᵢ∈S xᵢ

The excess measures how "unhappy" coalition S is with allocation x (positive excess = S could do better alone).

The **nucleolus** is the allocation that lexicographically minimizes the vector of excesses sorted in decreasing order.

### Properties

1. **Always exists** (for games with non-empty imputations)
2. **Always unique**
3. **Always in the core** when the core is non-empty
4. If the core is empty, the nucleolus minimizes the maximum violation of core constraints
5. Satisfies a form of **reduced game consistency** — the nucleolus of a reduced game (fixing some players' allocations) is the restriction of the full nucleolus

### Computation

Computed by solving a sequence of linear programs:
1. Minimize the maximum excess over all coalitions
2. Given that constraint, minimize the second-largest excess
3. Continue lexicographically

Computationally more expensive than the Shapley value but tractable for moderate-sized games.

## Bargaining Solutions

### Nash Bargaining Solution — Formal Definition

For a bargaining problem (F, d) where F ⊆ ℝ² is the feasible set and d ∈ F is the disagreement point:

NBS(F, d) = argmax_{(u₁,u₂) ∈ F, u≥d} (u₁ - d₁)(u₂ - d₂)

### Nash's Axioms

1. **Pareto efficiency**: No feasible point gives both players strictly more
2. **Symmetry**: If the problem is symmetric, both players receive the same
3. **Independence of irrelevant alternatives (IIA)**: If the solution is in a subset of the feasible set, it's also the solution for that subset
4. **Invariance to affine transformation**: Scaling/shifting utilities doesn't change the solution (up to rescaling)

### Kalai-Smorodinsky Solution

Replaces IIA with **individual monotonicity**: if the feasible set expands such that player i's maximum possible payoff increases (holding the other's fixed), player i's allocation should not decrease.

The KS solution is the maximal feasible point on the line from d to the **utopia point** (each player's maximum feasible payoff).

### Asymmetric Nash Bargaining

Generalization with bargaining weights α, β (α + β = 1):

ANBS = argmax (u₁ - d₁)^α (u₂ - d₂)^β

Higher α gives player 1 more of the surplus. The weights can represent relative patience, outside options, or institutional advantages.

## Von Neumann-Morgenstern Stable Sets

### Definition

A set K of imputations is a **stable set** if:
1. **Internal stability**: No imputation in K dominates another in K
2. **External stability**: Every imputation not in K is dominated by some imputation in K

### Properties

- May not exist (Lucas 1969 constructed a game with no stable set)
- When they exist, may not be unique
- Historically important (first solution concept, proposed 1944) but largely superseded by the core, Shapley value, and nucleolus

## Comparison Table

| Concept | Exists? | Unique? | In Core? | Captures | Axioms Emphasized |
|---------|---------|---------|----------|----------|-------------------|
| **Core** | Not always | Not unique | (is the core) | Stability | Coalition rationality |
| **Shapley Value** | Always | Yes | Only in convex games | Fairness (marginal contribution) | Efficiency, symmetry, additivity |
| **Nucleolus** | Always* | Yes | When core non-empty | Egalitarianism | Minimize max complaint |
| **Nash Bargaining** | Always (2-player) | Yes | N/A (different framework) | Bilateral negotiation | IIA, invariance |
| **KS Solution** | Always (2-player) | Yes | N/A | Bilateral fairness | Monotonicity |

*For games with non-empty imputation sets.

## Choosing a Solution Concept

**Use the core when**: You need to check if cooperation is stable — can the grand coalition hold together?

**Use Shapley value when**: You need a unique, axiomatically fair allocation — cost sharing, profit splitting, attribution.

**Use the nucleolus when**: You want the most "robust" allocation — the one that minimizes the worst-case complaint. Good for situations where stability is paramount.

**Use Nash bargaining when**: Two parties are negotiating with known disagreement points (BATNAs). The product-maximization formula directly computes the split.

**Use Kalai-Smorodinsky when**: Nash's IIA axiom feels wrong (why should irrelevant alternatives matter?) and you prefer monotonicity (expanding opportunities should benefit the player whose opportunities expanded).
