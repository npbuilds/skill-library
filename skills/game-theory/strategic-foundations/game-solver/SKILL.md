---
name: game-solver
description: >
  Analyze strategic situations through a game-theoretic lens. Use when the user describes a
  competitive, cooperative, or mixed-motive scenario and needs it formalized as a game, solved
  for equilibria, or interpreted as strategic advice. Handles business strategy, negotiation,
  political dynamics, technology competition, and fictional world scenarios.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# Game Solver — The Analyst

Every strategic situation is a game, whether the participants realize it or not. This skill takes informal descriptions of strategic interactions — pricing decisions, negotiations, platform competition, political dynamics, fictional faction conflicts — and produces rigorous game-theoretic analysis with actionable interpretation.

The core capability is **formalization**: bridging the gap between "I'm trying to decide whether to enter this market" and a well-specified entry deterrence game with equilibrium predictions.

## How to Run

### Input

The user provides one or more of:
1. **A situation description** — informal narrative of who's involved, what they can do, and what they want
2. **A specific question** — "should I cooperate?", "what's the likely outcome?", "is this agreement stable?"
3. **A formal game** — already specified with players, strategies, and payoffs (skip to Step 3)
4. **A real-world scenario** — business, political, technological, biological, or fictional context needing strategic analysis

### Steps

#### Step 1 — Extract the Strategic Elements

From the user's description, identify:

| Element | Question to Answer | Example |
|---------|-------------------|---------|
| **Players** | Who are the decision-makers? | Firm A, Firm B, Regulator |
| **Strategies** | What can each player choose? | Enter/Stay Out, High Price/Low Price |
| **Timing** | Simultaneous or sequential? Repeated? | Firm A moves first (Stackelberg) |
| **Information** | What does each player know? Private info? | Firm A knows its costs, B doesn't |
| **Payoffs** | What are they optimizing? | Profit, market share, welfare |
| **Commitments** | Can they make binding agreements? | Contract possible / no enforcement |

If elements are ambiguous, ask the user to clarify rather than assuming. The quality of the analysis depends on the quality of the formalization.

#### Step 2 — Classify the Game

Map to the appropriate game type using the classification tree:

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

Read `references/formalization-patterns.md` for common real-world-to-game mappings.

#### Step 3 — Formalize the Game

Produce the formal game specification:

**For normal-form games:**
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

**For extensive-form games:**
Describe the game tree with decision nodes, information sets, actions, and terminal payoffs. Use indentation to show the tree structure.

**For cooperative games:**
Specify the characteristic function v(S) for relevant coalitions.

#### Step 4 — Solve

Apply the appropriate solution concept:

| Game Type | Primary Solution | Also Check |
|-----------|-----------------|------------|
| Simultaneous, complete info | Nash Equilibrium (pure + mixed) | Dominated strategy elimination, correlated equilibrium |
| Sequential, perfect info | Subgame Perfect Equilibrium | Nash equilibria (to show which are non-credible) |
| Bayesian game | Bayesian Nash Equilibrium | Information value, posterior beliefs |
| Signaling game | PBE + Intuitive Criterion | Pooling vs. separating equilibria |
| Cooperative | Core + Shapley Value | Nucleolus, Nash bargaining |
| Repeated | Folk theorem bounds | Trigger strategies, renegotiation-proofness |

Show your work. For small games, enumerate strategies and check each cell. For larger games, use best-response analysis or dominance reasoning.

#### Step 5 — Interpret

Translate the formal results into plain-language strategic insight:

1. **Prediction**: What does the equilibrium say will happen?
2. **Recommendation**: Given the prediction, what should the user do?
3. **Robustness**: What assumptions drive the result? What changes if they shift?
4. **Comparison**: How does this compare to the cooperative optimum? Is there a Pareto improvement available through commitment or communication?
5. **Real-world caveats**: Where might the model oversimplify? Behavioral biases, institutional constraints, enforcement problems?

#### Step 6 — Sensitivity Analysis

Identify the key parameters and how the equilibrium changes:

- What if a player gets a new strategy option?
- What if information structure changes (player learns something)?
- What if the game is repeated instead of one-shot?
- What if players are boundedly rational?

### Output

A structured analysis document containing:

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

## Error Handling

**Situation is too vague**: Ask the user to specify players and what they can choose. "A competitive situation" needs more structure before analysis.

**Multiple equilibria**: Present all equilibria with selection criteria (risk-dominance, payoff-dominance, focal points, evolutionary stability). Don't arbitrarily pick one.

**No pure-strategy equilibrium**: Compute the mixed-strategy equilibrium and explain what randomization means in context (e.g., "the auditor should randomly select 30% of returns for review").

**Game is too large to solve by hand**: Identify dominant strategies and use iterated elimination to reduce the game. Note the computational complexity and suggest algorithmic approaches if needed.

**Cooperative and non-cooperative analyses disagree**: Present both. The non-cooperative analysis predicts what happens without enforcement; the cooperative analysis shows what's achievable with binding agreements. The gap between them quantifies the "value of commitment."
