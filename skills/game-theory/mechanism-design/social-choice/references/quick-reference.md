# Social Choice — Quick Reference


## Positional Scoring Rules

| Rule | Scoring | Properties |
|------|---------|-----------|
| **Plurality** | 1 point for first place, 0 otherwise | Simple; spoiler effect; not Condorcet-consistent |
| **Borda Count** | M-1 points for 1st, M-2 for 2nd, ..., 0 for last | Less susceptible to spoilers; violates IIA; violates Condorcet criterion |
| **Anti-plurality** | 0 for last place, 1 otherwise | Eliminates the most disliked; rarely used alone |

## Quick Reference

| Rule | Method | When No Condorcet Winner |
|------|--------|------------------------|
| **Copeland** | Most pairwise victories | Ties common |
| **Kemeny-Young** | Ranking that minimizes disagreement with voters | NP-hard to compute |
| **Ranked Pairs (Tideman)** | Lock in pairwise results from strongest to weakest, skip contradictions | Cloneproof |
| **Schulze** | Strongest path between alternatives | Used by many organizations (Debian, Wikimedia, Pirate Parties) |

## Quick Reference

| Axiom | Plurality | Borda | Condorcet | Approval |
|-------|-----------|-------|-----------|----------|
| **Condorcet winner** | No | No | Yes | Sometimes |
| **Condorcet loser** | No | Yes | Depends | Sometimes |
| **Monotonicity** | Yes | Yes | Depends | Yes |
| **Clone independence** | No | No | Some methods | Yes |
| **Participation** | Yes | Yes | No (some) | Yes |
| **IIA** | No | No | No | Partial |
