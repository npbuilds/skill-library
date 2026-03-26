---
name: classical-games
description: >
  Classical game theory foundations for strategic analysis. Reference when modeling strategic
  interactions, finding Nash equilibria, analyzing sequential games, evaluating mixed strategies,
  or understanding equilibrium refinements. Use when any analysis needs the core language and
  results of non-cooperative game theory.
---

# Classical Games — The Foundations

The core analytical framework for strategic interaction between rational decision-makers. Every other branch of game theory builds on these concepts. Grounded primarily in Osborne & Rubinstein (1994), Fudenberg & Tirole (1991), and Maschler/Solan/Zamir (2013).

## Game Representations

### Normal (Strategic) Form

A simultaneous-move game specified by:
- **Players**: N = {1, 2, ..., n}
- **Strategy sets**: S₁, S₂, ..., Sₙ (what each player can choose)
- **Payoff functions**: uᵢ(s₁, s₂, ..., sₙ) for each player i

Presented as a matrix for 2-player games. Player 1 chooses rows, Player 2 chooses columns, each cell contains (payoff₁, payoff₂).

Use when: players move simultaneously (or without observing each other's choices), strategy sets are finite and small enough to enumerate.

### Extensive Form

A game tree specified by:
- **Nodes**: decision points and terminal nodes
- **Information sets**: which nodes a player can't distinguish (captures imperfect information)
- **Actions**: available choices at each node
- **Payoffs**: assigned to terminal nodes

Use when: moves are sequential, timing matters, or information structure is important. Every normal-form game has an extensive-form representation, but not vice versa — extensive form is strictly more expressive.

## Core Solution Concepts

### Dominant Strategies

A strategy is **strictly dominant** if it yields a higher payoff than any alternative, regardless of what opponents do. If one exists, play it — no further analysis needed.

A strategy is **strictly dominated** if some other strategy always does better. Rational players never play dominated strategies. **Iterated elimination of strictly dominated strategies (IESDS)** can simplify games dramatically.

The Prisoner's Dilemma is the canonical example: Defect strictly dominates Cooperate for both players, yet mutual cooperation Pareto-dominates mutual defection. This tension — individual rationality vs. collective optimality — is the fundamental insight of game theory.

### Nash Equilibrium

A strategy profile where no player can improve their payoff by unilaterally changing their strategy. The central solution concept of non-cooperative game theory (Nash 1950).

**Key properties:**
- Every finite game has at least one Nash equilibrium (possibly in mixed strategies) — Nash's existence theorem
- Nash equilibrium may not be unique — many games have multiple equilibria
- Nash equilibrium may not be efficient — the Prisoner's Dilemma's unique equilibrium is Pareto-dominated

**Finding Nash equilibria:**
- 2×2 games: check each cell for profitable deviations, or use best-response analysis
- Larger games: best-response correspondences, support enumeration, Lemke-Howson algorithm
- Mixed strategies: make opponents indifferent between strategies in their support

### Mixed Strategies

A probability distribution over pure strategies. Player i plays strategy sᵢ with probability pᵢ(sᵢ).

**When they matter:** Games with no pure-strategy Nash equilibrium always have a mixed-strategy equilibrium (Matching Pennies is the classic example). Mixed strategies also appear in games where predictability is costly — sports, military strategy, auditing.

**Key intuition:** In a mixed-strategy equilibrium, each player is indifferent between the strategies they randomize over. You don't mix to confuse yourself — you mix to make your opponent unable to exploit your predictability.

### Subgame Perfect Equilibrium

A Nash equilibrium that also constitutes a Nash equilibrium in every subgame (Selten 1965). Found by **backward induction** in games of perfect information.

Eliminates **non-credible threats** — strategies that are part of a Nash equilibrium but that a player would never actually follow through on. The canonical example: entry deterrence, where an incumbent threatens a price war but would actually accommodate entry.

### Bayesian Nash Equilibrium

Extends Nash equilibrium to games of **incomplete information** — where players have private types (private valuations, costs, or information). Each player's strategy maps their type to an action, maximizing expected payoff given beliefs about other players' types.

Harsanyi's contribution (1967-68): any game of incomplete information can be modeled as a game where Nature moves first, assigning types according to a known prior distribution.

## Equilibrium Refinements

When a game has multiple Nash equilibria, refinements select among them. Read `references/solution-concepts.md` for formal definitions.

| Refinement | Selects By | Eliminates | Source |
|------------|-----------|------------|--------|
| **Subgame Perfection** | Backward induction in every subgame | Non-credible threats | Selten (1965) |
| **Trembling Hand Perfection** | Robustness to small probability mistakes | Equilibria that rely on opponents never trembling | Selten (1975) |
| **Sequential Equilibrium** | Consistent beliefs + sequential rationality | Equilibria with unreasonable off-path beliefs | Kreps & Wilson (1982) |
| **Intuitive Criterion** | Restricts off-path beliefs in signaling games | Implausible pooling equilibria | Cho & Kreps (1987) |

**Practical hierarchy**: Subgame perfection is the minimum refinement for sequential games. Apply trembling hand perfection when you suspect an equilibrium is "fragile." Use sequential equilibrium for signaling games. The intuitive criterion is the strongest commonly applied refinement.

## Beyond Nash

### Correlated Equilibrium (Aumann 1974)

Players can coordinate through a shared signal (a "mediator" or "correlation device"). Strictly generalizes Nash equilibrium — every Nash equilibrium is a correlated equilibrium, but correlated equilibria can achieve outcomes no Nash equilibrium reaches.

**Real-world example**: traffic lights. Each driver conditions their strategy on the signal. No driver has an incentive to deviate given their signal. The outcome is better than any Nash equilibrium of the uncoordinated game.

### Rationalizability (Bernheim 1984, Pearce 1984)

The set of strategies that survive iterated elimination of strategies that are never best responses. Weaker than Nash equilibrium — rationalizable strategies include all Nash equilibrium strategies but may include more. Useful when Nash equilibrium assumptions (correct beliefs about opponents' play) are too strong.

## Repeated and Dynamic Games

When a game is played more than once, the strategic landscape changes fundamentally. Cooperation can emerge even among self-interested players.

### Finitely Repeated Games

If both players know the game ends after T rounds, backward induction from round T unravels cooperation — the unique subgame perfect equilibrium of a finitely repeated Prisoner's Dilemma is defection in every round. However, with incomplete information about opponents' types or rationality, cooperation can be sustained even in finite games (Kreps, Milgrom, Roberts & Wilson 1982).

### Infinitely Repeated Games and the Folk Theorem

When the game repeats indefinitely (or ends each round with continuation probability δ), the **folk theorem** states: any individually rational payoff profile can be sustained as a Nash equilibrium if players are sufficiently patient (δ close to 1).

**Trigger strategies** enforce cooperation:
- **Grim trigger**: cooperate until the opponent defects, then defect forever. Sustains cooperation when δ ≥ (T-R)/(T-P) in the Prisoner's Dilemma.
- **Tit-for-tat**: copy the opponent's previous action. Famously won Axelrod's tournaments (1984). Simple, forgiving, retaliatory.

**Key insight**: The shadow of the future enables cooperation. The longer the relationship, the more future punishment deters present defection. This explains why firms cooperate with long-term suppliers but exploit one-time vendors, and why reputation matters.

### Stochastic (Markov) Games

Games where the state transitions probabilistically based on players' actions. Each state has its own stage game. Generalizes both repeated games (single state) and Markov decision processes (single player). Foundational for multi-agent reinforcement learning.

Source: Shapley (1953) "Stochastic Games," Fudenberg & Tirole Ch.5, Ch.13.

## Canonical Games

Read `references/canonical-games.md` for a complete catalog with payoff matrices, equilibria, and real-world applications. The essential ones:

| Game | Key Insight | Real-World Mapping |
|------|------------|-------------------|
| **Prisoner's Dilemma** | Individual rationality leads to collective irrationality | Arms races, price wars, climate agreements, doping in sports |
| **Stag Hunt** | Cooperation requires trust; payoff-dominant vs. risk-dominant equilibria | Technology adoption, team production, social contracts |
| **Battle of the Sexes** | Coordination is valuable even with preference disagreement | Standard-setting, meeting locations, platform compatibility |
| **Chicken (Hawk-Dove)** | Brinkmanship and commitment have strategic value | Nuclear deterrence, labor strikes, legislative bargaining |
| **Matching Pennies** | Pure-strategy equilibrium doesn't exist; mixed strategies essential | Penalty kicks, auditing, cybersecurity |
| **Cournot/Bertrand Competition** | Quantity vs. price competition yield radically different outcomes | Oligopoly markets, platform pricing |

## Sources

Read `references/sources.md` for the full bibliography grounding this skill — primary texts (Osborne & Rubinstein, Fudenberg & Tirole, Maschler/Solan/Zamir), key papers, and experimental references.

## When This Applies

- Any situation where multiple decision-makers interact and outcomes depend on everyone's choices
- Analyzing competitive or cooperative strategic situations
- Evaluating whether a proposed strategy is robust to opponent responses
- Understanding why rational agents produce collectively suboptimal outcomes
- Classifying real-world interactions into known game structures
