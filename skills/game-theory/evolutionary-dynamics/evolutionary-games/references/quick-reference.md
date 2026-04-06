# Evolutionary Games — Quick Reference


## ESS and Nash Equilibrium

| Property | Nash Equilibrium | ESS |
|----------|-----------------|-----|
| **Assumes** | Rational deliberation | Evolutionary process |
| **Stability** | No profitable deviation | Resistant to invasion |
| **Always exists?** | Yes (in mixed strategies) | Not always |
| **Multiple?** | Often | Can have 0, 1, or multiple |
| **Refinement of NE?** | N/A | Every ESS is a NE (stronger concept) |
| **Dynamic foundation** | Requires separate justification | Replicator dynamics provide natural dynamic |

## Formula / Pseudocode

```
Dove        Hawk
Dove     (V/2, V/2)   (0, V)
Hawk     (V, 0)       ((V-C)/2, (V-C)/2)
```

## Stag Hunt (Evolutionary Coordination)

```
Stag        Hare
Stag     (4, 4)      (0, 3)
Hare     (3, 0)      (3, 3)
```

## Prisoner's Dilemma (Evolutionary Cooperation)

```
Cooperate   Defect
Cooperate  (3, 3)      (0, 5)
Defect     (5, 0)      (1, 1)
```

## Rock-Paper-Scissors (Cyclic Dominance)

```
Rock    Paper   Scissors
Rock      (0,0)   (-1,1)  (1,-1)
Paper     (1,-1)  (0,0)   (-1,1)
Scissors  (-1,1)  (1,-1)  (0,0)
```
