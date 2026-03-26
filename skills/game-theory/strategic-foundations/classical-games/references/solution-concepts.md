# Solution Concepts — Formal Definitions and Relationships

A reference for the formal definitions, relationships, and selection criteria among game-theoretic solution concepts.

## Hierarchy of Solution Concepts

From weakest (most permissive) to strongest (most selective):

```
Rationalizability (weakest — any never-dominated strategy)
    ⊇
Nash Equilibrium (mutual best response)
    ⊇
Correlated Equilibrium (generalizes Nash — allows coordination signals)
    [Note: CE ⊇ NE in the set-inclusion sense — every NE is a CE]

For sequential games:
Nash Equilibrium
    ⊇
Subgame Perfect Equilibrium (Nash in every subgame)
    ⊇
Sequential Equilibrium (consistent beliefs + sequential rationality)
    ⊇
Trembling Hand Perfect Equilibrium (robust to trembles in every subgame)
    ⊇
Proper Equilibrium (trembles on costlier mistakes are less likely)
```

## Detailed Definitions

### Nash Equilibrium (Nash 1950)

**Definition**: A strategy profile s* = (s₁*, s₂*, ..., sₙ*) is a Nash equilibrium if for every player i and every alternative strategy sᵢ:

uᵢ(s*) ≥ uᵢ(sᵢ, s*₋ᵢ)

No player can increase their payoff by unilaterally changing their strategy.

**Existence**: Every finite game (finite players, finite strategies) has at least one Nash equilibrium, possibly in mixed strategies (Nash 1950, using Kakutani's fixed point theorem).

**Computation**: Finding a Nash equilibrium of a finite game is PPAD-complete (Daskalakis, Goldberg, Papadimitriou 2009). No known polynomial-time algorithm exists, even for 2-player games.

**Interpretations**:
1. *Rational introspection*: players reason to equilibrium through common knowledge of rationality
2. *Steady state*: a convention or norm that no one has incentive to deviate from
3. *Evolutionary*: a rest point of a learning/evolutionary dynamic (not all NE are stable under all dynamics)

### Mixed Strategy Nash Equilibrium

**Definition**: A mixed strategy σᵢ for player i is a probability distribution over i's pure strategies. A mixed strategy profile σ* is a Nash equilibrium if for every player i:

Eσ*[uᵢ] ≥ Eσᵢ,σ*₋ᵢ[uᵢ] for all σᵢ

**Key property**: In a mixed-strategy NE, every pure strategy in a player's support yields the same expected payoff. If one pure strategy yielded strictly more, the player would put all probability on it.

**Computation for 2×2 games**: Player 1 chooses mixing probabilities to make Player 2 indifferent, and vice versa. The equilibrium mixing probabilities depend on the *opponent's* payoffs, not your own — a counterintuitive but fundamental result.

### Subgame Perfect Equilibrium (Selten 1965)

**Definition**: A strategy profile s* is a subgame perfect equilibrium (SPE) if its restriction to every subgame is a Nash equilibrium of that subgame.

**Algorithm**: Found by backward induction in games of perfect information. Start at terminal nodes, work backwards, choosing the optimal action at each node.

**Key property**: Eliminates non-credible threats — strategies that are part of a Nash equilibrium but that no rational player would follow through on in the relevant subgame.

**Limitation**: Only defined for proper subgames (which require information set singletons). In games with imperfect information, many off-path subgames don't exist, making SPE too permissive.

### Sequential Equilibrium (Kreps & Wilson 1982)

**Definition**: A pair (strategy profile s*, belief system μ*) is a sequential equilibrium if:
1. **Sequential rationality**: at every information set, the player's strategy maximizes expected payoff given beliefs μ*
2. **Consistency**: beliefs μ* are the limit of beliefs derived from Bayes' rule applied to a sequence of completely mixed strategies converging to s*

**Key property**: Handles games with imperfect information where subgame perfection has no bite. Forces beliefs to be "reasonable" even at off-equilibrium information sets.

### Trembling Hand Perfect Equilibrium (Selten 1975)

**Definition**: A strategy profile s* is trembling hand perfect if there exists a sequence of completely mixed strategy profiles {σᵏ} → s* such that s* is a best response to every σᵏ in the sequence.

**Intuition**: The equilibrium must be robust to the possibility that every player makes small mistakes ("trembles"). If an equilibrium relies on a player never making a mistake, it's not trembling hand perfect.

**Relationship to Nash**: Every trembling hand perfect equilibrium is Nash, but not vice versa. THPEs eliminate weakly dominated strategies.

### Proper Equilibrium (Myerson 1978)

**Definition**: A strategy profile s* is a proper equilibrium if there exists a sequence of ε-proper strategy profiles converging to s*, where in an ε-proper profile, the probability assigned to a costlier mistake is at most ε times the probability assigned to a less costly mistake.

**Intuition**: Players are more likely to make smaller mistakes than larger ones. Strengthens trembling hand perfection by restricting the nature of trembles.

### Correlated Equilibrium (Aumann 1974)

**Definition**: A probability distribution p over strategy profiles is a correlated equilibrium if, for every player i and every pair of strategies sᵢ, sᵢ':

Σₛ₋ᵢ p(sᵢ,s₋ᵢ)[uᵢ(sᵢ,s₋ᵢ) - uᵢ(sᵢ',s₋ᵢ)] ≥ 0

Given the signal (recommendation) to play sᵢ, no player benefits from deviating.

**Key properties**:
- The set of correlated equilibria is a convex polytope (can be computed efficiently via linear programming, unlike Nash)
- Every Nash equilibrium is a correlated equilibrium (but not vice versa)
- Can achieve payoffs outside the convex hull of Nash equilibrium payoffs

**Example**: In Chicken, a mediator who randomly recommends (Swerve,Straight) or (Straight,Swerve) each with probability 1/2 achieves expected payoff (2.5, 2.5) — better than the mixed NE payoff.

### Rationalizability (Bernheim 1984, Pearce 1984)

**Definition**: Strategy sᵢ is rationalizable if it survives iterated elimination of strategies that are never best responses to any belief about opponents' rationalizable strategies.

**Key property**: Weaker than Nash — does not require correct beliefs about opponents' play. Only requires that beliefs are consistent with common knowledge of rationality.

**Relationship**: In 2-player games, rationalizability = iterated elimination of strictly dominated strategies. In games with 3+ players, rationalizability can be strictly more permissive.

## Selection Criteria — When to Use What

| Situation | Recommended Concept | Why |
|-----------|-------------------|-----|
| Simultaneous move, complete info | Nash Equilibrium | Standard baseline |
| Sequential moves, perfect info | Subgame Perfect Equilibrium | Eliminates non-credible threats |
| Sequential, imperfect info | Sequential Equilibrium | Handles off-path beliefs |
| Coordination possible via signals | Correlated Equilibrium | Exploits coordination opportunities |
| Robustness to mistakes matters | Trembling Hand Perfection | Tests fragility |
| Signaling game, multiple equilibria | Intuitive Criterion | Strongest standard refinement |
| Uncertain about opponent rationality | Rationalizability | Weakest rational requirement |
| Repeated interaction | Folk Theorem analysis | Identifies cooperation possibilities |

## Relationships Diagram

```
                    Proper ⊂ THPE ⊂ Sequential ⊂ SPE ⊂ NE ⊂ CE
                                                              ⊂
                                                    Rationalizable
                                                    (for 2-player games,
                                                     NE ⊂ Rationalizable)
```

Note: ⊂ means "is a refinement of" (more restrictive, smaller set of equilibria).
