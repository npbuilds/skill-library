---
name: social-choice
description: >
  Social choice theory foundations for understanding collective decision-making and its limits.
  Reference when analyzing voting systems, evaluating fairness of aggregation rules, understanding
  impossibility theorems, or designing preference aggregation mechanisms. Use when the problem
  involves groups making collective decisions.
---

# Social Choice — The Impossibilities

Social choice theory asks: how should a group aggregate individual preferences into a collective decision? The answer, famously, is constrained by impossibility theorems — no aggregation rule can satisfy all desirable properties simultaneously. Understanding these limits is essential for any mechanism designer. Grounded primarily in Arrow (1951), Gibbard (1973), Satterthwaite (1975), and Moulin (2003).

## The Aggregation Problem

A **social choice function** maps a profile of individual preferences to a collective outcome. The challenge: different aggregation rules satisfy different desirable properties, and no rule satisfies all of them.

**Setting**: N voters, each with a complete, transitive ranking over M alternatives. A social choice function selects one alternative (or produces a ranking) based on reported preferences.

## Impossibility Theorems

### Arrow's Impossibility Theorem (1951)

No social welfare function (preference aggregation into a ranking) with 3+ alternatives satisfies all of:
1. **Universal domain**: Works for any preference profile
2. **Pareto efficiency**: If everyone prefers A to B, society ranks A above B
3. **Independence of Irrelevant Alternatives (IIA)**: Society's ranking of A vs. B depends only on individuals' rankings of A vs. B (not on how they rank C)
4. **Non-dictatorship**: No single voter's preference always determines the social ranking

**Interpretation**: Any "reasonable" ranking system either violates IIA (most practical systems do) or is dictatorial. This doesn't mean democracy is impossible — it means every voting system has flaws. The question is which flaws you accept.

### Gibbard-Satterthwaite Theorem (1973/1975)

Any social choice function (selecting a single winner) with 3+ alternatives that is:
- **Onto** (every alternative can win under some preference profile)
- **Strategy-proof** (no voter ever benefits from misreporting preferences)

must be **dictatorial** (one voter always gets their way).

**Interpretation**: Every non-dictatorial voting rule is manipulable — some voter in some situation can benefit by voting dishonestly. This is the impossibility that motivates all of mechanism design's focus on incentive compatibility.

### Sen's Impossibility of a Paretian Liberal (1970)

No social choice function satisfies both:
- **Pareto efficiency**: Unanimity is respected
- **Minimal liberalism**: Each individual is decisive over at least one pair of alternatives (personal sphere)

**Interpretation**: Individual rights can conflict with collective efficiency. A deeply philosophical result about the limits of liberal social choice.

## Voting Rules

### Positional Scoring Rules

| Rule | Scoring | Properties |
|------|---------|-----------|
| **Plurality** | 1 point for first place, 0 otherwise | Simple; spoiler effect; not Condorcet-consistent |
| **Borda Count** | M-1 points for 1st, M-2 for 2nd, ..., 0 for last | Less susceptible to spoilers; violates IIA; violates Condorcet criterion |
| **Anti-plurality** | 0 for last place, 1 otherwise | Eliminates the most disliked; rarely used alone |

### Condorcet Methods

A **Condorcet winner** beats every other alternative in pairwise majority comparison. Condorcet methods select the Condorcet winner when one exists.

| Rule | Method | When No Condorcet Winner |
|------|--------|------------------------|
| **Copeland** | Most pairwise victories | Ties common |
| **Kemeny-Young** | Ranking that minimizes disagreement with voters | NP-hard to compute |
| **Ranked Pairs (Tideman)** | Lock in pairwise results from strongest to weakest, skip contradictions | Cloneproof |
| **Schulze** | Strongest path between alternatives | Used by many organizations (Debian, Wikimedia, Pirate Parties) |

**Condorcet paradox**: Majority preferences can cycle (A beats B, B beats C, C beats A). No Condorcet winner exists. Every Condorcet method must have a tiebreaking rule for this case.

### Other Important Rules

**Approval voting**: Voters approve/disapprove each candidate. Most approvals wins. Strategy-proof in a limited sense (sincere voting is always a best response). Resists spoiler effect.

**Instant Runoff Voting (IRV) / Ranked Choice**: Eliminate the candidate with fewest first-place votes; redistribute their supporters' ballots. Repeat. Not monotone (raising a candidate in your ranking can cause them to lose).

**Majority judgment**: Voters assign grades to each candidate. Winner has the highest median grade. Resistant to strategic extremism.

## Strategy-Proofness and Manipulation

Given Gibbard-Satterthwaite, all non-dictatorial rules are manipulable. But rules differ in *how* manipulable they are:

**Restricted domains where strategy-proofness is possible**:
- **Single-peaked preferences**: If alternatives are ordered on a line and each voter has a single peak, the median voter rule is strategy-proof and efficient (Black 1948). This is the key theorem behind the Median Voter Theorem in political economy.
- **Dichotomous preferences**: With approval-style preferences, approval voting has strong incentive properties.

**Gibbard's theorem for randomized rules** (1977): Even randomized social choice functions — if they're strategy-proof and have at least 3 alternatives — must be a mixture of dictatorial and duple (two-outcome) rules.

## Axiomatic Approach

Different voting rules satisfy different axiom subsets:

| Axiom | Plurality | Borda | Condorcet | Approval |
|-------|-----------|-------|-----------|----------|
| **Condorcet winner** | No | No | Yes | Sometimes |
| **Condorcet loser** | No | Yes | Depends | Sometimes |
| **Monotonicity** | Yes | Yes | Depends | Yes |
| **Clone independence** | No | No | Some methods | Yes |
| **Participation** | Yes | Yes | No (some) | Yes |
| **IIA** | No | No | No | Partial |

**No rule satisfies all axioms** — Arrow's theorem guarantees this. The designer must choose which properties to prioritize for their specific context.

## Modern Applications

**Computational social choice**: Algorithmic questions about voting — computing winners (some rules are NP-hard), detecting manipulation, measuring manipulability. Active research area bridging social choice and computer science.

**Liquid democracy**: Voters can either vote directly or delegate their vote to a trusted proxy, who can further delegate. Used in some DAO governance systems. Game-theoretic analysis shows delegation can improve outcomes but creates new manipulation possibilities.

**Quadratic voting** (Weyl 2017): Voters buy votes at quadratic cost — 1 vote costs $1, 2 votes cost $4, 3 votes cost $9. Approximately efficient under reasonable conditions. Used experimentally in the Colorado legislature and various DAOs.

## Sources

Read `references/sources.md` for the full bibliography — primary texts (Arrow, Moulin, Mas-Colell/Whinston/Green Ch.21), key papers, and applied references.

## When This Applies

- Evaluating or designing any collective decision-making procedure
- Understanding why a voting system produces "wrong" results (it may be Arrow's theorem in action)
- Choosing between voting rules for an organization, committee, or governance system
- DAO and decentralized governance design
- Any setting where a group must aggregate conflicting preferences
