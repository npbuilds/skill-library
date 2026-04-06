# Evolutionary Dynamics — Quick Reference


## Quick Reference

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

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| ESS analysis says strategy X is stable, but replicator dynamics show it has a tiny basin of attraction | Both are correct — X is locally stable but unlikely to be reached. Present both: "X is an ESS, but the population is unlikely to arrive there from most initial conditions" | ESS is a local concept; basins of attraction are global |
| Deterministic dynamics predict fixation at X, but stochastic model shows persistent polymorphism | Stochastic model is more realistic for finite populations. Flag population size as the key parameter | Finite population effects (drift) can sustain strategies that deterministic models eliminate |
| Classical Nash analysis predicts one outcome, evolutionary analysis predicts another | Present both with context — classical assumes rational deliberation, evolutionary assumes adaptive dynamics. In biological settings, evolutionary predictions are primary; in strategic human settings, both matter | Different models of player behavior produce different predictions |
| Simulation shows unexpected behavior not predicted by analytical models | Investigate — this usually indicates a modeling assumption that breaks under simulation parameters (e.g., discrete vs. continuous time, finite vs. infinite population). Don't dismiss either; reconcile | Simulation reveals what analysis simplifies away |
