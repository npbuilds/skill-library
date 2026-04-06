---
name: evolutionary-dynamics
description: >
  Direct the evolutionary dynamics subdomain — route questions about evolutionary game theory,
  population dynamics, ESS, replicator dynamics, fitness landscapes, and biological or cultural
  strategy to the right specialist skill. Use when analyzing large populations adapting over
  time without central design or full rationality.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Evolutionary Dynamics Director — The Naturalist

The department head for evolutionary game theory within the game-theory domain. Evolutionary dynamics removes the rationality assumption — strategies spread through populations based on fitness, imitation, or learning, not deliberate optimization. Routes questions to the right specialist, defines the learning order, and resolves conflicts between evolutionary and classical frameworks.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| ESS, evolutionarily stable strategy, can a mutant invade, invasion resistance | `evolutionary-games` | Core evolutionary stability |
| Hawk-Dove, war of attrition, producer-scrounger, evolutionary versions of classical games | `evolutionary-games` | Canonical evolutionary games |
| Relationship between ESS and Nash, evolutionary justification for equilibrium | `evolutionary-games` | Foundational connections |
| Replicator dynamics, replicator equation, strategy frequency over time | `population-dynamics` | Dynamic analysis |
| Phase portraits, trajectories, basins of attraction, convergence | `population-dynamics` | Geometric/qualitative dynamics |
| Finite populations, fixation probability, Moran process, stochastic dynamics | `population-dynamics` | Stochastic evolutionary models |
| Fitness landscapes, adaptive dynamics, mutation-selection balance | `population-dynamics` | Landscape analysis |
| "Simulate this evolutionary game", "show me the dynamics", "run replicator equations" | `evo-simulator` | Computational simulation |
| Multi-population dynamics, co-evolution, predator-prey game dynamics | `population-dynamics` | Multi-population models |
| Cultural evolution, meme spreading, norm emergence, convention formation | `evolutionary-games` + `population-dynamics` | Cultural applications of evolutionary GT |

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:

1. `evolutionary-games` — establish the game structure, identify candidate ESS
2. `population-dynamics` — analyze whether and how the population converges to the ESS
3. `evo-simulator` — visualize trajectories and validate analytical predictions

This order ensures the static analysis (what are the stable states?) comes before the dynamic analysis (how does the population get there?), which comes before computational verification.

**Example multi-skill question**: "Will cooperation evolve in a population playing the Prisoner's Dilemma?"
1. `evolutionary-games` → Defect is the unique ESS in the one-shot PD; cooperation cannot invade
2. `population-dynamics` → Under replicator dynamics, defectors drive cooperators to extinction; but with spatial structure, assortment, or group selection, cooperation can persist
3. `evo-simulator` → Simulate to show extinction trajectory in well-mixed populations vs. persistence under spatial structure

## Curriculum Order

For learning or progressive loading:

1. **Evolutionary Games** (foundation) — The concepts: ESS, evolutionary stability, the canonical games reinterpreted through an evolutionary lens. Essential vocabulary for everything else.

2. **Population Dynamics** (dynamics) — The mathematics: replicator equations, phase portraits, stochastic dynamics, convergence. Adds the temporal dimension to evolutionary stability.

3. **Evo-Simulator** (computation) — The tool: simulate and visualize dynamics for games too complex for analytical solutions. Builds intuition through experimentation.

### Level Progression
- **Foundational**: Evolutionary Games, Population Dynamics
- **Intermediate**: (future) Spatial Evolutionary Games, Multi-Level Selection
- **Advanced**: (future) Adaptive Dynamics, Evolutionary Mechanism Design

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| ESS analysis says strategy X is stable, but replicator dynamics show it has a tiny basin of attraction | Both are correct — X is locally stable but unlikely to be reached. Present both: "X is an ESS, but the population is unlikely to arrive there from most initial conditions" | ESS is a local concept; basins of attraction are global |
| Deterministic dynamics predict fixation at X, but stochastic model shows persistent polymorphism | Stochastic model is more realistic for finite populations. Flag population size as the key parameter | Finite population effects (drift) can sustain strategies that deterministic models eliminate |
| Classical Nash analysis predicts one outcome, evolutionary analysis predicts another | Present both with context — classical assumes rational deliberation, evolutionary assumes adaptive dynamics. In biological settings, evolutionary predictions are primary; in strategic human settings, both matter | Different models of player behavior produce different predictions |
| Simulation shows unexpected behavior not predicted by analytical models | Investigate — this usually indicates a modeling assumption that breaks under simulation parameters (e.g., discrete vs. continuous time, finite vs. infinite population). Don't dismiss either; reconcile | Simulation reveals what analysis simplifies away |

**General rule**: Dynamic results > static predictions when the question is about outcomes over time. ESS identifies candidates; dynamics determines which are reached. When in doubt, simulation resolves analytical ambiguity.

## Scope Boundaries

**This director handles**: All questions about strategy evolution in populations — biological evolution, cultural evolution, norm emergence, adaptive dynamics, and the dynamic foundations of equilibrium concepts.

**Escalate to the orchestrator when**:
- Players are rational agents making deliberate choices (not adapting populations) → Strategic Foundations
- The question involves designing rules for a population → Mechanism Design
- The question is about strategic information revelation → Information Economics
- The question involves computational agents or AI → Computational Strategy
- The biological context requires domain-specific knowledge beyond game theory (genetics, ecology) → flag for the user

## Cross-Domain Connections

- **Investing/reflexivity-sentiment**: Herd behavior in markets is an evolutionary dynamic — "follow the crowd" is an ESS until the bubble pops and contrarians invade. Replicator dynamics model how investment strategies (value, momentum, passive) compete for capital and how one strategy's success seeds its own destruction.
- **Investing/reflexivity-sentiment/market-psychology**: Crowd psychology maps directly to population dynamics — sentiment extremes are unstable equilibria where a small perturbation (catalyst) can trigger a phase transition (crash/melt-up).
