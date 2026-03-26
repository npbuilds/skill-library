# Simulation Parameters Reference

## Default Parameter Values

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| **Dynamics model** | Replicator (continuous) | Replicator, Moran, Best Response, Logit | Choose based on modeling assumptions |
| **Population size** | Infinite (deterministic) | 10 — 10,000 | Finite triggers Moran process |
| **Selection intensity** | β = 1.0 | 0.01 — 10.0 | Low β ≈ neutral; high β ≈ strong selection |
| **Mutation rate** | μ = 0 | 0 — 0.1 | Positive μ creates stationary distribution |
| **Time horizon** | 1000 generations | 100 — 100,000 | Until convergence or limit |
| **Integration step** | dt = 0.01 | 0.001 — 0.1 | For ODE solver; smaller = more accurate |
| **Replicates** | 1000 | 100 — 100,000 | For stochastic simulations (fixation probability) |
| **Initial conditions** | Grid over simplex | Specific points or grid | Multiple ICs reveal basins of attraction |

## Dynamics Model Selection Guide

### When to Use Replicator Dynamics
- Infinite (or very large) population
- Agents update strategies by imitating successful neighbors
- Continuous-time is acceptable approximation
- Want to identify basins of attraction and convergence properties

### When to Use Moran Process
- Finite population where stochastic effects matter
- Interested in fixation probabilities and times
- Population size is biologically meaningful (small groups, finite firms)
- Want to test whether analytical ESS predictions hold for realistic population sizes

### When to Use Best Response Dynamics
- Agents have full information and switch to currently optimal strategy
- Want to model strategic learning rather than imitation
- Interested in convergence in potential games (best response always converges)
- Faster convergence than replicator for many games

### When to Use Logit Dynamics
- Agents make noisy best responses (bounded rationality)
- The noise parameter β captures rationality level:
  - β → 0: uniform random (fully irrational)
  - β → ∞: best response (fully rational)
  - Intermediate β: realistic bounded rationality
- Always has a unique stationary distribution (no multiple equilibria problem)
- Good for modeling human behavior in experiments

## Interpreting Common Trajectory Patterns

### Convergence to a Point
**Pattern**: All trajectories flow to a single fixed point.
**Meaning**: The game has a globally stable equilibrium. This is the evolutionary prediction.
**Examples**: Prisoner's Dilemma (all defect), dominant strategy games.

### Two Basins of Attraction
**Pattern**: Trajectories flow to one of two boundary points, depending on initial conditions.
**Meaning**: A coordination game. The initial composition determines which equilibrium is reached.
**Key metric**: The **basin boundary** — the critical frequency where trajectories switch between attractors.

### Stable Interior Fixed Point
**Pattern**: All interior trajectories spiral or flow to an interior point.
**Meaning**: The population maintains diversity at the mixed ESS. No strategy goes extinct.
**Examples**: Hawk-Dove with V < C.

### Cycling (Closed Orbits)
**Pattern**: Trajectories form closed loops around an interior fixed point.
**Meaning**: No convergence. Strategy frequencies oscillate perpetually. The time average may correspond to the interior NE, but the instantaneous state is always moving.
**Examples**: Rock-Paper-Scissors (symmetric zero-sum).

### Heteroclinic Cycles
**Pattern**: Trajectories approach the boundary and follow edges of the simplex in a cycle, spending increasing time near each vertex.
**Meaning**: Strategies take turns dominating. Slower and slower cycling. In finite populations, this typically leads to random fixation at one vertex.
**Examples**: RPS with asymmetric payoffs.

### Divergence / Chaos
**Pattern**: Trajectories are sensitive to initial conditions, no convergence.
**Meaning**: Rare in standard evolutionary games but possible with high-dimensional strategy spaces or multi-population dynamics. Verify numerical accuracy before concluding chaos.

## Finite Population Corrections

### Fixation Probability Formulas

**Moran process, 2 strategies, constant fitness**:
For a single mutant A in a population of N-1 agents playing B:

ρ_A = (1 - 1/r) / (1 - 1/r^N)

where r = fitness(A) / fitness(B).

- If r = 1 (neutral): ρ = 1/N
- If r > 1 (advantageous): ρ > 1/N (selection favors A)
- If r < 1 (deleterious): ρ < 1/N (selection opposes A, but fixation still possible via drift)

### Frequency-Dependent Fixation (Nowak et al. 2004)

For a game with payoff matrix A = [[a,b],[c,d]], the fixation probability of a single mutant playing strategy 1 in a population of N-1 playing strategy 2 depends on all four payoffs through the frequency-dependent fitness:

The **1/3 rule**: Under weak selection, strategy 1 is favored if:
a + 2b > c + 2d

This is equivalent to asking: is strategy 1's payoff higher when the population is 1/3 strategy 1 and 2/3 strategy 2?

### When Stochastic Effects Matter Most

- **Small populations** (N < 50): Drift dominates selection for weakly beneficial mutations
- **Weak selection** (β < 0.1): Nearly neutral evolution, fixation probabilities close to 1/N
- **Near basin boundaries**: Stochastic fluctuations can push populations across boundaries that deterministic dynamics cannot cross
- **Absorbing states**: Without mutation, populations eventually fixate at a pure strategy through drift, even in games with stable interior equilibria
