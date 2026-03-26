# Game Theory Domain Taxonomy

A map of the field grounded in the standard academic organization, with source citations for each subfield.

## Primary Division

Game theory divides into two traditions based on whether players can make binding agreements:

```
Game Theory
├── Non-Cooperative Game Theory
│   Players act independently; no binding agreements assumed.
│   Dominant in economics since Nash (1950).
│   Source: Fudenberg & Tirole (1991), Osborne & Rubinstein (1994)
│
└── Cooperative Game Theory
    Players can form binding coalitions; focus on fair allocation.
    Source: Osborne & Rubinstein Part IV, Maschler/Solan/Zamir Ch.13-18
```

This division is foundational but increasingly blurred — mechanism design uses non-cooperative tools to achieve cooperative outcomes, and Rubinstein's bargaining model provides non-cooperative foundations for cooperative solutions.

## Full Subfield Map

### 1. Strategic Foundations (Non-Cooperative + Cooperative Core)

**Static Games of Complete Information**
Normal-form games, Nash equilibrium, mixed strategies, dominance, rationalizability.
Source: Osborne & Rubinstein Ch.1-4, Maschler/Solan/Zamir Ch.1-6

**Dynamic Games of Complete Information**
Extensive-form games, subgame perfection, backward induction, repeated games, folk theorems.
Source: Fudenberg & Tirole Part II, Maschler/Solan/Zamir Ch.7-12

**Games of Incomplete Information**
Bayesian games, Harsanyi transformation, BNE, PBE, sequential equilibrium.
Source: Fudenberg & Tirole Parts III-IV, Myerson Ch.4-6

**Equilibrium Refinements**
Trembling hand perfection, sequential equilibrium, divine equilibrium, intuitive criterion, stable equilibria.
Source: Fudenberg & Tirole Ch.11, Kohlberg & Mertens (1986)

**Cooperative Game Theory**
Core, Shapley value, nucleolus, bargaining (Nash, Kalai-Smorodinsky, Rubinstein), matching, fair division.
Source: Maschler/Solan/Zamir Ch.13-18, Roth & Sotomayor (1990)

### 2. Mechanism Design ("Reverse Game Theory")

**Core Theory**
Revelation principle, incentive compatibility (DSIC, BIC), individual rationality, implementation theory.
Source: Myerson (1981), Borgers *Introduction to Mechanism Design* (2015)

**Auction Theory**
English, Dutch, first-price sealed-bid, Vickrey (second-price), revenue equivalence, optimal auctions, combinatorial auctions.
Source: Krishna *Auction Theory* (2002), Milgrom *Putting Auction Theory to Work* (2004)

**Matching and Market Design**
Gale-Shapley deferred acceptance, stable matching, school choice, kidney exchange, two-sided markets.
Source: Roth & Sotomayor (1990), Roth (2015) *Who Gets What and Why*

**Social Choice Theory**
Voting rules, Arrow's impossibility theorem, Gibbard-Satterthwaite theorem, strategy-proofness.
Source: Mas-Colell/Whinston/Green Ch.21, Moulin *Fair Division and Collective Welfare* (2003)

### 3. Evolutionary Dynamics

**Evolutionary Game Theory**
ESS (Maynard Smith & Price 1973), replicator dynamics, hawk-dove, stag hunt as evolutionary games.
Source: Weibull *Evolutionary Game Theory* (1995), Maynard Smith *Evolution and the Theory of Games* (1982)

**Population Dynamics**
Multi-population replicator dynamics, invasion analysis, fixation probabilities, stochastic dynamics.
Source: Sandholm *Population Games and Evolutionary Dynamics* (2010)

**Biological Applications**
Sex ratio evolution, animal conflict, cooperation in microbes, epidemiological game theory (vaccination games).
Source: Sigmund *The Calculus of Selfishness* (2010)

### 4. Information Economics

**Signaling and Screening**
Spence signaling model (1973), pooling vs. separating equilibria, screening (Rothschild & Stiglitz 1976).
Source: Fudenberg & Tirole Ch.8-9, Riley (2001) "Silver Signals"

**Bayesian Persuasion and Information Design**
Sender-receiver games, optimal signal design, concavification, multiple receivers.
Source: Kamenica & Gentzkow (2011), Bergemann & Morris (2016)

**Cheap Talk**
Costless communication, partial revelation, babbling equilibria, influential communication.
Source: Crawford & Sobel (1982), Farrell & Rabin (1996)

**Global Games**
Unique equilibrium selection through information perturbations, coordination under uncertainty.
Source: Carlsson & van Damme (1993), Morris & Shin (2003)

### 5. Computational Strategy

**Algorithmic Game Theory**
Computational complexity of equilibria (PPAD), price of anarchy/stability, congestion games, potential games, algorithmic mechanism design.
Source: Nisan/Roughgarden/Tardos/Vazirani *Algorithmic Game Theory* (2007)

**Behavioral Game Theory**
Level-k thinking, quantal response equilibrium, social preferences (inequity aversion, reciprocity), learning models (fictitious play, EWA).
Source: Camerer *Behavioral Game Theory* (2003)

**AI and Multi-Agent Game Theory**
MARL, self-play, PSRO, adversarial ML (GANs as games), LLM alignment as game theory, Nash learning from human feedback.
Source: Shoham & Leyton-Brown (2009), MARL-book.com, arXiv:2502.09053 (GT meets LLMs survey, 2025)

**Mean Field Games**
Infinite-player limits, continuous-population Nash equilibria, applications to crowd dynamics, macro-economics, network effects.
Source: Lasry & Lions (2007), Huang/Caines/Malhame (2006)

## Cross-Subfield Relationships

```
Mechanism Design ←uses→ Non-Cooperative GT (as analytic engine)
                ←addresses→ Cooperative GT (normative goals)

Algorithmic GT ←imports→ Non-Cooperative GT + Mechanism Design
              ←adds→ Computational complexity constraints

Behavioral GT ←tests→ Non-Cooperative GT predictions
             ←proposes→ Modified equilibrium concepts

Evolutionary GT ←provides→ Dynamic foundation for Nash equilibrium
               ←justifies→ Equilibrium selection (long-run convergence)

Information Design ←extends→ Bayesian games
                  ←endogenizes→ Information structure

Mean Field Games ←extends→ Non-Cooperative GT to infinite populations
```

## Nobel Prizes in Game Theory

| Year | Laureate(s) | Contribution |
|------|------------|--------------|
| 1994 | Nash, Harsanyi, Selten | Nash equilibrium, incomplete information games, equilibrium refinements |
| 2005 | Aumann, Schelling | Repeated games and cooperation, conflict and coordination |
| 2007 | Hurwicz, Maskin, Myerson | Mechanism design theory |
| 2012 | Roth, Shapley | Stable matching and market design |
| 2014 | Tirole | Market power and regulation (game-theoretic IO) |
| 2020 | Milgrom, Wilson | Auction theory and new auction formats |
