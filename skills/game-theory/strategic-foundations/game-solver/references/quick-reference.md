# Game Solver — Quick Reference


## Quick Reference

| Element | Question to Answer | Example |
|---------|-------------------|---------|
| **Players** | Who are the decision-makers? | Firm A, Firm B, Regulator |
| **Strategies** | What can each player choose? | Enter/Stay Out, High Price/Low Price |
| **Timing** | Simultaneous or sequential? Repeated? | Firm A moves first (Stackelberg) |
| **Information** | What does each player know? Private info? | Firm A knows its costs, B doesn't |
| **Payoffs** | What are they optimizing? | Profit, market share, welfare |
| **Commitments** | Can they make binding agreements? | Contract possible / no enforcement |

## Quick Reference

| Game Type | Primary Solution | Also Check |
|-----------|-----------------|------------|
| Simultaneous, complete info | Nash Equilibrium (pure + mixed) | Dominated strategy elimination, correlated equilibrium |
| Sequential, perfect info | Subgame Perfect Equilibrium | Nash equilibria (to show which are non-credible) |
| Bayesian game | Bayesian Nash Equilibrium | Information value, posterior beliefs |
| Signaling game | PBE + Intuitive Criterion | Pooling vs. separating equilibria |
| Cooperative | Core + Shapley Value | Nucleolus, Nash bargaining |
| Repeated | Folk theorem bounds | Trigger strategies, renegotiation-proofness |

## Formula / Pseudocode

```
Is there private information?
├── No → Complete information
│   ├── Simultaneous → Normal-form game
│   │   ├── One-shot → Standard Nash analysis
│   │   └── Repeated → Folk theorem / repeated game analysis
│   └── Sequential → Extensive-form game
│       └── Subgame perfect equilibrium (backward induction)
│
└── Yes → Incomplete information
    ├── Simultaneous → Bayesian game
    │   └── Bayesian Nash equilibrium
    └── Sequential → Signaling / screening game
        └── Perfect Bayesian equilibrium + refinements

Can players make binding agreements?
├── Yes → Also analyze as cooperative game
│   └── Core, Shapley value, bargaining solutions
└── No → Non-cooperative analysis only
```

## Formula / Pseudocode

```
Players: {P1, P2, ...}
Strategies:
  P1: {s1a, s1b, ...}
  P2: {s2a, s2b, ...}
Payoff matrix:
         P2: s2a    P2: s2b
P1: s1a  (a,b)      (c,d)
P1: s1b  (e,f)      (g,h)
```

## Formula / Pseudocode

```
## Strategic Analysis: [Situation Name]

### Game Specification
[Formal game: players, strategies, timing, information, payoffs]

### Classification
[Game type and justification]

### Solution
[Equilibrium analysis with work shown]

### Interpretation
[Plain-language prediction and recommendation]

### Sensitivity
[Key assumptions and how results change]

### Caveats
[Where the model simplifies reality]
```
