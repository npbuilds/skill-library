# Canonical Games Catalog

A reference catalog of the named games that form the vocabulary of game theory. Each entry includes the payoff structure, equilibria, key insight, and modern applications.

## Two-Player Symmetric Games

### Prisoner's Dilemma

```
             Player 2
           C        D
P1  C   (3,3)    (0,5)
    D   (5,0)    (1,1)
```
General form: T > R > P > S where T=temptation, R=reward, P=punishment, S=sucker's payoff.

**Equilibrium**: (D,D) is the unique Nash equilibrium in dominant strategies.
**Paradox**: (C,C) Pareto-dominates (D,D), but mutual cooperation is not an equilibrium.
**Key insight**: Individual rationality can produce collectively irrational outcomes. The tension between private and social incentives is the central problem of game theory.

**Modern applications**:
- Climate agreements: each country benefits from polluting while others reduce emissions
- Price wars: firms would profit more from high prices but each has incentive to undercut
- Open-source contribution: everyone benefits from contributions, but each developer prefers others contribute
- Arms races: mutual disarmament is better, but each side has incentive to arm
- Doping in sports: clean competition is preferred, but unilateral doping gives an edge

**Resolution mechanisms**: Repetition (folk theorem), enforceable contracts, reputation, altruistic preferences, correlated devices.

### Stag Hunt (Assurance Game)

```
             Player 2
          Stag     Hare
P1 Stag  (4,4)    (0,3)
   Hare  (3,0)    (3,3)
```

**Equilibria**: Two pure-strategy Nash equilibria: (Stag,Stag) and (Hare,Hare), plus one mixed.
**Key insight**: (Stag,Stag) is **payoff-dominant** (better for everyone) but (Hare,Hare) is **risk-dominant** (safer — guaranteed payoff regardless of partner's choice). The game captures the tension between efficiency and safety.

**Modern applications**:
- Technology adoption: everyone benefits if all adopt the same standard, but switching is risky if others don't follow
- Team production: high effort produces the best outcome, but only if everyone commits
- Social contracts: cooperation is optimal but requires trust
- Bank runs: if everyone stays calm, banks are solvent; panic causes collapse even of healthy banks

### Battle of the Sexes (Coordination Game)

```
             Player 2
          Opera    Football
P1 Opera  (3,2)    (0,0)
   Foot   (0,0)    (2,3)
```

**Equilibria**: Two pure-strategy NE: (Opera,Opera) and (Football,Football), plus one mixed.
**Key insight**: Players prefer coordination to miscoordination, but disagree on which coordinated outcome is best. Communication and focal points matter.

**Modern applications**:
- Standard-setting: companies prefer different standards but any standard beats incompatibility
- Meeting coordination: both parties prefer meeting over not, but disagree on venue
- Platform ecosystems: developers and users need to coordinate on a platform

### Chicken (Hawk-Dove)

```
             Player 2
          Swerve   Straight
P1 Swerve (3,3)    (1,4)
   Str    (4,1)    (0,0)
```

**Equilibria**: Two pure-strategy NE: (Swerve,Straight) and (Straight,Swerve), plus one mixed. No symmetric pure-strategy equilibrium.
**Key insight**: Commitment has strategic value — credibly committing to "Straight" forces the other player to swerve. But mutual commitment is catastrophic. The game formalizes **brinkmanship**.

**Modern applications**:
- Nuclear deterrence: Schelling's analysis of Cold War strategy
- Labor disputes: both sides lose from a strike, but threatening to strike gains leverage
- Legislative bargaining: government shutdown threats
- Pedestrian/driver interactions: both prefer the other yields, but collision is the worst outcome

### Matching Pennies

```
             Player 2
          Heads    Tails
P1 Heads  (1,-1)   (-1,1)
   Tails  (-1,1)   (1,-1)
```

**Equilibrium**: Unique Nash equilibrium is mixed: each player plays Heads and Tails with probability 1/2.
**Key insight**: No pure-strategy equilibrium exists. This is the simplest **zero-sum game** — one player's gain is the other's loss. Optimal play requires randomization.

**Modern applications**:
- Penalty kicks in soccer: kicker and goalkeeper must randomize (empirically confirmed by Chiappori, Levitt & Groseclose 2002)
- Tax auditing: auditor randomizes which returns to audit; taxpayers randomize compliance
- Cybersecurity: attacker and defender randomize over attack/defense vectors
- Rock-paper-scissors and its strategic extensions

## Asymmetric and Multi-Player Games

### Ultimatum Game

Player 1 proposes a split of a fixed sum. Player 2 accepts or rejects. Rejection means both get nothing.

**Subgame perfect equilibrium**: Player 1 offers the minimum positive amount; Player 2 accepts.
**Behavioral reality**: Offers below ~30% are typically rejected. Modal offer is 40-50%. This is one of the most replicated findings in experimental economics and a cornerstone of behavioral game theory.

Source: Guth, Schmittberger & Schwarze (1982); Camerer (2003) Ch.2.

### Dictator Game

Player 1 allocates a sum between themselves and Player 2. Player 2 has no strategic choice.

**Prediction under self-interest**: Player 1 keeps everything.
**Behavioral reality**: Average allocation to Player 2 is ~20-30%. Demonstrates social preferences beyond pure self-interest.

### Centipede Game

Sequential game: players alternate choosing to "take" (ending the game) or "pass" (increasing the total pot). Backward induction predicts immediate taking at round 1.

**Behavioral reality**: Most players pass for several rounds. A key example where backward induction predictions diverge sharply from observed behavior.

Source: Rosenthal (1981); McKelvey & Palfrey (1992).

### Public Goods Game (N-Player Prisoner's Dilemma)

N players simultaneously contribute to a public good. Each unit contributed is multiplied by a factor m (1 < m < N) and shared equally.

**Nash equilibrium**: Zero contribution (free-riding).
**Key insight**: The N-player generalization of the Prisoner's Dilemma. Captures problems of collective action, commons management, and public goods provision.

**Modern applications**: Open-source software, team performance bonuses, carbon emission reduction, vaccine uptake.

## Market/Economic Games

### Cournot Competition (Quantity Competition)

Two firms simultaneously choose production quantities. Market price decreases with total quantity.

**Nash equilibrium**: Each firm produces more than the monopoly quantity but less than the competitive quantity. Total output is between monopoly and competitive levels.
**Key insight**: Oligopoly produces outcomes between monopoly (worst for consumers) and perfect competition (best). More firms → outcome closer to competitive.

Source: Cournot (1838); modern treatment in Tirole *Theory of Industrial Organization* (1988).

### Bertrand Competition (Price Competition)

Two firms with identical products simultaneously set prices. Consumers buy from the cheaper firm.

**Nash equilibrium**: Both firms price at marginal cost (the competitive outcome), earning zero profit — even with only two firms.
**Key insight**: The **Bertrand paradox** — price competition is dramatically more competitive than quantity competition, even with the same market structure. Resolution: product differentiation, capacity constraints (Edgeworth), or search costs restore positive profits.

### Entry Deterrence

An incumbent faces a potential entrant. The incumbent can invest in capacity (costly) that makes price war credible if entry occurs.

**Subgame perfect analysis**: The incumbent deters entry only if the cost of capacity is low enough that price war is credible. Empty threats of "price war if you enter" without capacity commitment are not subgame perfect.
**Key insight**: Credible commitment — strategic pre-commitment that constrains your own future actions — can be valuable precisely because it limits your flexibility.

## Information and Signaling Games

### Beer-Quiche Game (Cho & Kreps 1987)

A player is either Strong or Weak (known only to them). They choose to eat beer or quiche for breakfast. An observer decides whether to fight them based on the breakfast choice.

**Key insight**: Demonstrates the intuitive criterion refinement. The pooling equilibrium where both types eat quiche (to avoid a fight) is eliminated because only the Weak type could possibly benefit from deviating to quiche. This refines away "unreasonable" beliefs off the equilibrium path.

### Market for Lemons (Akerlof 1970)

Sellers know their product quality; buyers don't. High-quality sellers can't credibly communicate quality.

**Equilibrium result**: The market unravels — only low-quality goods are traded. The quintessential adverse selection problem.
**Modern applications**: Used car markets, insurance markets, hiring, online marketplaces (solved partially by reputation systems, warranties, certifications).

## Game Relationships

```
                    Zero-Sum ────── Matching Pennies
                   /
Pure Conflict ────
                   \
                    General-Sum ─── Prisoner's Dilemma
                                    (partial conflict)
                   /
Coordination ─────  Battle of the Sexes
                   \  (agree to coordinate, disagree on how)
                    Stag Hunt
                    (agree on best, disagree on risk)

Anti-Coordination ── Chicken/Hawk-Dove
                    (prefer opponent yields)
```
