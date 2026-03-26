---
name: evolutionary-games
description: >
  Evolutionary game theory foundations for understanding strategy evolution in populations.
  Reference when analyzing evolutionarily stable strategies, interpreting classical games through
  an evolutionary lens, or understanding how cooperation, conflict, and conventions emerge
  without rational deliberation. Use when rationality is replaced by natural selection or imitation.
---

# Evolutionary Games — The Survivors

Evolutionary game theory replaces the rational player with a population of agents using inherited or imitated strategies. Strategies don't "choose" — they spread or die based on fitness. This framework explains how cooperation emerges, why conflict persists, and how conventions form — all without assuming anyone does any strategic reasoning. Grounded primarily in Maynard Smith (1982), Weibull (1995), and Sandholm (2010).

## The Evolutionary Framework

Instead of "players choose strategies," evolutionary GT says:
- A **large population** of agents is randomly matched to play a game
- Each agent uses a **fixed strategy** (inherited, learned, or culturally transmitted)
- Payoffs determine **fitness** — higher payoff → more offspring / more imitators
- Over time, fitter strategies **spread** and less fit strategies **decline**
- **Equilibrium** is a population state that resists invasion by alternative strategies

This removes two key assumptions of classical game theory: (1) agents don't need to know the game structure, and (2) agents don't need to be rational. Evolution is the optimizer.

## Evolutionarily Stable Strategy (ESS)

The central concept (Maynard Smith & Price 1973):

A strategy s* is an **ESS** if, when the entire population plays s*, no small fraction of mutants playing any alternative strategy s can invade.

**Formal definition**: s* is an ESS if for all s ≠ s*:
1. u(s*, s*) > u(s, s*), OR
2. u(s*, s*) = u(s, s*) AND u(s*, s) > u(s, s)

Condition 1: s* is a strict best response to itself (a **strict Nash equilibrium** is always an ESS).
Condition 2: If s does equally well against s*, then s* must do better against the mutant s than the mutant does against itself.

**Key properties**:
- Every ESS is a Nash equilibrium (but not every NE is an ESS)
- ESS may not exist (some games have no ESS, only mixed ESS)
- A strict Nash equilibrium is always an ESS
- A completely mixed Nash equilibrium is an ESS if and only if the game matrix satisfies certain negative-definiteness conditions

## Canonical Evolutionary Games

### Hawk-Dove (The Fundamental Conflict Game)

Two animals compete for a resource of value V. Hawks fight; Doves share or retreat.

```
            Dove        Hawk
Dove     (V/2, V/2)   (0, V)
Hawk     (V, 0)       ((V-C)/2, (V-C)/2)
```

Where C = cost of fighting.

**If V > C** (low-cost fighting): Hawk is the unique ESS. Aggression pays.
**If V < C** (costly fighting): No pure ESS. The mixed ESS is p* = V/C (proportion of Hawks). This is the canonical example of a **frequency-dependent equilibrium** — Hawks thrive when rare (easy targets), suffer when common (costly fights).

**Biological insight**: The hawk-dove model explains why animals in the same species rarely fight to the death — C is usually high, so the mixed ESS involves a lot of display behavior (dove) with occasional escalation (hawk).

### Stag Hunt (Evolutionary Coordination)

```
            Stag        Hare
Stag     (4, 4)      (0, 3)
Hare     (3, 0)      (3, 3)
```

**Two ESS**: All-Stag and All-Hare. Both are evolutionarily stable — once established, neither can be invaded. But their **basins of attraction** under replicator dynamics differ. If initial Stag frequency > 3/4, population converges to All-Stag; otherwise to All-Hare.

**Key insight**: The risk-dominant equilibrium (Hare) has a larger basin of attraction than the payoff-dominant equilibrium (Stag). Evolution favors safety over optimality when coordination failure is costly. This explains why inferior conventions persist — they're harder to dislodge.

### Prisoner's Dilemma (Evolutionary Cooperation)

```
            Cooperate   Defect
Cooperate  (3, 3)      (0, 5)
Defect     (5, 0)      (1, 1)
```

**Defect is the unique ESS** in the one-shot game. Cooperation cannot invade a population of defectors, and defection can always invade a population of cooperators.

**How cooperation evolves despite this**:
- **Kin selection** (Hamilton 1964): Copies of your strategy in relatives make cooperation viable when relatedness × benefit > cost
- **Direct reciprocity** (Trivers 1971): Repeated interaction. Tit-for-tat and other reciprocal strategies are ESS in repeated games
- **Indirect reciprocity** (Nowak & Sigmund 1998): Reputation — cooperate with cooperators, defect on defectors
- **Spatial structure**: On networks/lattices, cooperators can cluster and protect each other from exploitation
- **Group selection** (multi-level): Groups of cooperators outcompete groups of defectors, even if defectors outcompete cooperators within groups

These are the "five mechanisms for the evolution of cooperation" (Nowak 2006).

### Rock-Paper-Scissors (Cyclic Dominance)

```
          Rock    Paper   Scissors
Rock      (0,0)   (-1,1)  (1,-1)
Paper     (1,-1)  (0,0)   (-1,1)
Scissors  (-1,1)  (1,-1)  (0,0)
```

**No pure ESS**. The unique Nash equilibrium (1/3, 1/3, 1/3) is NOT an ESS — it fails condition 2. Under replicator dynamics, orbits cycle perpetually around the interior fixed point without converging.

**Biological significance**: Models cyclic dominance in nature. The side-blotched lizard (*Uta stansburiana*) has three male morphs — orange (aggressive), blue (mate-guarders), yellow (sneakers) — that cycle in frequency, matching the RPS dynamic (Sinervo & Lively 1996).

## ESS and Nash Equilibrium

| Property | Nash Equilibrium | ESS |
|----------|-----------------|-----|
| **Assumes** | Rational deliberation | Evolutionary process |
| **Stability** | No profitable deviation | Resistant to invasion |
| **Always exists?** | Yes (in mixed strategies) | Not always |
| **Multiple?** | Often | Can have 0, 1, or multiple |
| **Refinement of NE?** | N/A | Every ESS is a NE (stronger concept) |
| **Dynamic foundation** | Requires separate justification | Replicator dynamics provide natural dynamic |

**The connection**: ESS provides an evolutionary justification for Nash equilibrium. If a population converges to an ESS, it's playing a Nash equilibrium — without anyone knowing what a Nash equilibrium is.

## Beyond Two-Player Symmetric Games

**Asymmetric games** (different roles): In asymmetric contests, ESS is defined for the population of role pairs. The "owner vs. intruder" model shows how property conventions emerge — "owners fight, intruders retreat" is an ESS even when roles are assigned randomly (Maynard Smith 1982).

**Multi-player games**: ESS generalizes to population games with n-player interactions. Payoffs depend on the population strategy distribution, not just a single opponent.

**Continuous strategy spaces**: When strategies are real-valued (e.g., investment level, body size), ESS analysis uses calculus. Convergence-stability and evolutionary branching become relevant (adaptive dynamics framework).

## Sources

Read `references/sources.md` for the full bibliography — primary texts (Maynard Smith, Weibull, Sandholm), key papers on ESS, cooperation evolution, and biological applications.

## When This Applies

- Analyzing competition or cooperation in biological populations
- Understanding how norms, conventions, or cultural practices emerge and persist
- Evaluating whether a Nash equilibrium is evolutionarily plausible
- Modeling situations where agents adapt rather than optimize
- Understanding frequency-dependent phenomena (strategies that succeed when rare)
