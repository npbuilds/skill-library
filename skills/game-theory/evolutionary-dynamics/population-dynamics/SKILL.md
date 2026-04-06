---
name: population-dynamics
description: >
  Population dynamics foundations for evolutionary game theory. Reference when analyzing
  replicator equations, phase portraits, fixation probabilities, stochastic dynamics, or
  convergence properties of evolutionary processes. Use when the question is about how
  populations change over time, not just what the stable states are.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Population Dynamics — The Trajectories

Evolutionary games identify stable strategies. Population dynamics answers the harder question: **how does the population get there?** This skill covers the mathematical machinery of evolutionary change — replicator equations, phase portraits, basins of attraction, stochastic dynamics in finite populations, and convergence results. Grounded primarily in Sandholm (2010), Hofbauer & Sigmund (1998), and Nowak (2006).

## Replicator Dynamics

The central dynamical system of evolutionary game theory (Taylor & Jonker 1978).

### The Replicator Equation

For a population with n strategies and strategy frequencies x = (x₁, ..., xₙ):

ẋᵢ = xᵢ [fᵢ(x) - f̄(x)]

Where:
- fᵢ(x) = fitness of strategy i given population state x
- f̄(x) = Σⱼ xⱼ fⱼ(x) = average population fitness
- ẋᵢ = rate of change of strategy i's frequency

**Interpretation**: A strategy grows when its fitness exceeds the population average, and shrinks when below. The growth rate is proportional to both the fitness advantage and the current frequency.

**For a 2-strategy game** with payoff matrix [[a,b],[c,d]]:
ẋ = x(1-x)[(a-c)x + (b-d)(1-x)]

This is a single ODE that can be fully analyzed graphically.

### Properties of Replicator Dynamics

**Fixed points**: Every Nash equilibrium is a fixed point of the replicator dynamics (strategies with above-average fitness grow, so at a NE where no deviation improves fitness, the system is stationary). The converse is not true — some fixed points are not NE (e.g., interior fixed points where all strategies have equal fitness but the point is unstable).

**ESS connection**: Every ESS is an asymptotically stable fixed point of the replicator dynamics. An ESS attracts all nearby population states. But an asymptotically stable fixed point need not be an ESS (stability under replicator dynamics is slightly weaker than evolutionary stability).

**Dominated strategies**: Strictly dominated strategies go extinct under replicator dynamics (their frequency → 0 as t → ∞). This is the dynamic analog of iterated elimination.

**Folk theorem of evolutionary game theory** (Nachbar 1990): If the replicator dynamics converge to a point, that point must be a Nash equilibrium.

## Phase Portrait Analysis

For 2-strategy games, the dynamics live on the interval [0,1]. For 3-strategy games, the state space is the 2-simplex (a triangle). Phase portraits show trajectories from all initial conditions.

### 2-Strategy Games

**Case 1: Dominant strategy** (e.g., Prisoner's Dilemma)
One strategy dominates — all trajectories converge to the dominant strategy regardless of initial conditions. Single globally stable fixed point.

**Case 2: Coordination game** (e.g., Stag Hunt)
Two stable fixed points (each pure strategy), separated by an unstable interior fixed point. The **basin of attraction** of each stable point determines which equilibrium is reached from a given initial condition. The risk-dominant equilibrium has the larger basin.

**Case 3: Anti-coordination** (e.g., Hawk-Dove with V < C)
Two unstable corners, one stable interior fixed point (the mixed ESS). All interior trajectories converge to the mixed equilibrium. The population maintains diversity at the ESS frequency.

**Case 4: Cyclic** (e.g., Rock-Paper-Scissors)
Interior fixed point exists but is not asymptotically stable. Orbits cycle around it. In the standard RPS game with symmetric payoffs, orbits are closed (neutral stability — Lyapunov stable but not asymptotically stable).

### 3-Strategy Phase Portraits on the Simplex

The 2-simplex Δ = {(x₁,x₂,x₃) : xᵢ ≥ 0, Σxᵢ = 1} is a triangle. Vertices are pure-strategy populations, edges are 2-strategy mixtures, interior points are fully mixed populations.

Key patterns:
- **Single interior attractor**: All trajectories spiral or flow to one point (generalized hawk-dove)
- **Multiple basins**: Triangle partitioned into regions flowing to different corners (coordination)
- **Heteroclinic cycles**: Trajectories follow edges in a cycle (near RPS dynamics)
- **Limit cycles**: Closed orbits not on the boundary (require specific payoff structures)

## Finite Population Dynamics

Real populations are finite. This introduces **stochastic effects** that can dramatically change predictions.

### Moran Process

The standard model for finite-population evolutionary dynamics:

1. Population of N agents. At each time step:
   - Select one agent to reproduce, proportional to fitness
   - The offspring replaces a randomly selected agent (possibly the parent)
2. Population size stays fixed at N

**Fixation probability**: The probability that a single mutant playing strategy A takes over a population of N-1 agents playing strategy B.

For neutral drift (equal fitness): ρ = 1/N
For a mutant with relative fitness r: ρ = (1 - 1/r) / (1 - 1/rᴺ)

**Key result**: In finite populations, strategies can fixate even if they're not ESS, purely through drift. And ESS strategies can be displaced by drift when populations are small. The "1/3 rule" (Nowak et al. 2004): selection favors a strategy if its fixation probability exceeds 1/N, which occurs approximately when it performs well against a population that is 1/3 its own type and 2/3 the resident type.

### Wright-Fisher Process

Alternative to Moran: all N agents are replaced simultaneously. Each new agent adopts a strategy proportional to the fitness of that strategy in the current generation. Introduces more variance per generation than Moran.

### Stochastic Stability

When selection is weak (fitness differences are small relative to drift), **stochastic stability** selects among absorbing states. A state is stochastically stable if its probability remains positive as the mutation rate goes to zero.

Key result (Kandori, Mailath & Rob 1993; Young 1993): In 2×2 coordination games with random matching and imitation, the risk-dominant equilibrium is stochastically stable — it's selected in the long run even though both equilibria are equally ESS in infinite populations.

## Multi-Population Dynamics

When different populations interact (e.g., predators vs. prey, buyers vs. sellers), each population has its own replicator equation coupled through cross-population payoffs.

**Asymmetric games**: Two populations with different strategy sets. The combined dynamics live on the product of two simplices. Can exhibit richer behavior than single-population models — limit cycles, chaos.

**Lotka-Volterra connection**: The replicator dynamics for n strategies are equivalent to generalized Lotka-Volterra equations for n-1 species. This connects evolutionary game theory to mathematical ecology.

## Revision Protocols

Replicator dynamics assume a specific "revision protocol" — how agents update strategies. Different protocols produce different dynamics:

| Protocol | Update Rule | Resulting Dynamics |
|----------|-----------|-------------------|
| **Imitation (proportional)** | Copy a random agent's strategy with probability proportional to their fitness | Replicator dynamics |
| **Best response** | Switch to the current best response to the population | Best response dynamics |
| **Logit (perturbed BR)** | Choose strategies proportional to exp(β × fitness) | Logit dynamics (with noise parameter β) |
| **Smith** | Switch to a better strategy with rate proportional to improvement | Smith dynamics |
| **Pairwise comparison** | Meet a random agent; switch if they're doing better, with probability proportional to the difference | Pairwise comparison dynamics |

**Convergence results vary by protocol**: Best response dynamics always converge in potential games. Replicator dynamics may cycle. Logit dynamics always have a unique stationary distribution for finite β.

## Sources

Read `references/sources.md` for the full bibliography — primary texts (Sandholm, Hofbauer & Sigmund, Nowak), key papers on replicator dynamics, stochastic evolution, and convergence.

## When This Applies

- Predicting which equilibrium a population will reach from a given starting point
- Analyzing whether cooperation/convention can emerge from random initial conditions
- Modeling finite-population effects (drift, fixation, stochastic stability)
- Understanding speed of convergence to equilibrium
- Comparing different learning/imitation rules and their long-run consequences
