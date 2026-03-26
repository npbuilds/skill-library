---
name: strategic-foundations
description: >
  Direct the strategic foundations subdomain — route game theory questions to the right
  specialist skill, define the learning curriculum, and resolve conflicts between analytical
  frameworks. Use when analyzing strategic interactions, finding equilibria, evaluating
  cooperation, bargaining, or classifying game structures.
tools: Read, Glob
---

# Strategic Foundations Director

The department head for core game theory within the game-theory domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts between non-cooperative and cooperative frameworks.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Payoff matrices, Nash equilibrium, dominant strategies, mixed strategies | `classical-games` | Core non-cooperative analysis |
| Extensive-form games, backward induction, subgame perfection, information sets | `classical-games` | Sequential game analysis |
| Equilibrium refinements, trembling hand, sequential equilibrium | `classical-games` | Advanced solution concepts |
| Coalitions, Shapley value, core, fair allocation, voting power | `cooperative-games` | Cooperative game theory |
| Bargaining, negotiation, Nash bargaining solution, Rubinstein model | `cooperative-games` | Bargaining theory |
| Matching, stable matching, Gale-Shapley, school choice, kidney exchange | `cooperative-games` | Matching and allocation |
| Fair division, cake-cutting, envy-free, proportional allocation | `cooperative-games` | Fairness concepts |
| Repeated games, folk theorem, trigger strategies, reputation, discount factors | `classical-games` | Repeated/dynamic games (until dedicated skill is built) |
| "Analyze this situation", "what should I do", "model this as a game" | `game-solver` | Applied analysis — formalization and solution |
| "What kind of game is this?", "classify this interaction" | `game-solver` | Game identification and classification |

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:

1. `classical-games` — establish the formal game structure and equilibrium predictions
2. `cooperative-games` — evaluate cooperative possibilities, fairness, and allocation
3. `game-solver` — synthesize into applied strategic recommendations

This order ensures non-cooperative analysis sets the strategic baseline, cooperative analysis identifies opportunities beyond equilibrium, and the solver integrates both into actionable advice.

**Example multi-skill question**: "Should our three-company consortium jointly bid on this contract, and how should we split the proceeds?"
1. `classical-games` → model the auction as a non-cooperative game, find bidding equilibria
2. `cooperative-games` → analyze the consortium as a coalition, compute Shapley values for fair revenue splitting
3. `game-solver` → synthesize: recommend whether to cooperate, optimal joint bid, and allocation rule

## Curriculum Order

For learning or progressive loading:

1. **Classical Games** (foundation) — The language and core results of game theory. Every other subfield assumes you understand Nash equilibrium, extensive-form games, and basic incomplete-information games. Without this, nothing else makes sense.

2. **Cooperative Games** (extension) — Addresses questions non-cooperative theory leaves open: "what's fair?", "should they cooperate?", "how should coalitions form?" Builds on classical foundations by providing normative answers where classical theory gives positive predictions.

3. **Repeated and Dynamic Games** (not yet built — currently handled within classical-games) — Adds the temporal dimension. Explains how cooperation emerges without binding agreements, how reputation works, and why short-run predictions differ from long-run outcomes.

### Level Progression
- **Foundational**: Classical Games, Cooperative Games
- **Intermediate**: (future) Repeated & Dynamic Games, Stochastic Games
- **Advanced**: (future) Combinatorial Game Theory, Differential Games

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Classical predicts defection but cooperative analysis shows mutual cooperation is Pareto-superior | Present both — classical as prediction, cooperative as aspiration | They answer different questions: "what will happen" vs. "what's possible with agreements" |
| Multiple Nash equilibria exist and cooperative concepts select differently than refinements | Formal refinements take priority for prediction; cooperative concepts for normative recommendation | Refinements are analytically grounded; cooperative solutions answer fairness questions |
| Classical theory assumes rationality but the situation involves bounded agents | Flag the assumption gap, note where behavioral GT would modify predictions | Classical analysis is correct given its assumptions; acknowledge when assumptions strain |
| Cooperative solution concept (core, Shapley) yields different allocation than bargaining theory | Specify which axioms the user values — efficiency, symmetry, monotonicity, or strategic grounding | Different cooperative solutions optimize different fairness axioms; no universal "right" answer |

**General rule**: Formal results > heuristics > intuition. When frameworks disagree, present both with the assumptions that drive the disagreement. Non-cooperative analysis predicts; cooperative analysis prescribes. Don't force one to override the other — they answer different questions.

## Scope Boundaries

**This director handles**: All foundational game theory — equilibrium analysis, game classification, strategic prediction, bargaining, coalitions, fairness, matching, applied strategic reasoning.

**Escalate to the orchestrator when**:
- The question involves designing rules, auctions, or incentive systems (Mechanism Design)
- The question involves large populations evolving over time without deliberate strategy (Evolutionary Dynamics)
- The core issue is strategic communication or information revelation (Information Economics)
- Computational complexity, bounded rationality, or AI/ML agents are central (Computational Strategy)
- The question spans multiple subdomains and needs orchestrator-level coordination
