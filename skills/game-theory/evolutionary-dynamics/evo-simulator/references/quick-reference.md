# Evo Simulator — Quick Reference


## Formula / Pseudocode

```
A = [[a, b],
     [c, d]]
```

## Formula / Pseudocode

```
A = [[a, b, c],
     [d, e, f],
     [g, h, i]]
```

## Formula / Pseudocode

```
import numpy as np
from scipy.integrate import odeint

def replicator(x, t, A):
    fitness = A @ x
    avg_fitness = x @ fitness
    return x * (fitness - avg_fitness)

# Solve ODE from initial condition x0 over time grid t
trajectory = odeint(replicator, x0, t, args=(A,))
```

## Formula / Pseudocode

```
def moran_step(population, A, N):
    # Compute fitness of each strategy type
    counts = np.bincount(population, minlength=len(A))
    freqs = counts / N
    fitness = A @ freqs

    # Select reproducer proportional to fitness
    reproducer_type = np.random.choice(len(A), p=fitness*freqs/sum(fitness*freqs))

    # Select random individual to die
    death_idx = np.random.randint(N)
    population[death_idx] = reproducer_type
    return population
```

## Formula / Pseudocode

```
## Evolutionary Simulation: [Game Name]

### Game Specification
[Payoff matrix, dynamics model, parameters]

### Analytical Predictions
[Fixed points, ESS, expected basins of attraction]

### Simulation Results
[Trajectory descriptions, convergence behavior, fixation probabilities]
[Visualizations or descriptions of phase portraits]

### Sensitivity Analysis
[How results change with parameter variation]

### Interpretation
[What the dynamics tell us about the strategic situation]
```
