# Decision Frameworks

Quick-reference for the decision-architect. Match the situation to the right analytical framework.

## Framework Selection Guide

| Situation | Framework | When to Use |
|-----------|-----------|------------|
| Probabilities estimable, outcomes quantifiable | **Expected Value (EV)** | Most common; default for well-characterized decisions |
| Can't estimate probabilities | **Minimax Regret** | Deep uncertainty; "what would I kick myself for not doing?" |
| Catastrophic downside possible | **Maximin** | Existential risk; ruin avoidance |
| Sequential decisions; information arrives over time | **Decision Tree / Real Options** | Staged investments, phased rollouts |
| Multiple competing objectives | **Multi-Criteria Decision Analysis (MCDA)** | Hiring decisions, vendor selection, policy |
| Risk of ruin in repeated decisions | **Kelly Criterion** | Investing, repeated bets, portfolio sizing |
| Must justify to stakeholders | **Satisficing + Justification** | Regulatory, committee, or group decisions |

## Expected Value

**EV = Σ (probability × payoff)** for each outcome.

Choose the option with highest EV when:
- You'll face many similar decisions (law of large numbers)
- No single outcome is catastrophic
- Probabilities are reasonably estimable

**Failure mode**: EV maximization is wrong when a single loss can be ruinous (non-ergodic situation). A 51% chance of doubling your money and 49% chance of losing everything has positive EV but leads to ruin.

## Minimax Regret (Savage)

For each option, calculate the maximum regret (difference between that option's payoff and the best payoff you could have gotten). Choose the option that minimizes the maximum regret.

**Use when**: You can't estimate probabilities but can rank outcomes. Protects against the worst case of "I wish I'd chosen differently."

## Maximin (Wald)

Choose the option whose worst-case outcome is best. Pure risk aversion.

**Use when**: Downside is catastrophic and irreversible. Better to give up upside than to risk ruin.

## Decision Trees

Map sequential decisions as a tree: decision nodes (squares), chance nodes (circles), outcomes (triangles). Solve by backward induction — start at the leaves and work back.

**Use when**: Decisions are sequential, information arrives between decisions, and the option to wait/learn has value.

## Multi-Criteria Decision Analysis

Score each option against each criterion (1-10). Weight criteria by importance. Weighted sum = overall score.

**Use when**: Multiple objectives that can't be reduced to a single metric. Makes trade-offs explicit.

**Pitfall**: Sensitive to how criteria are weighted. Run sensitivity analysis on weights.

## Kelly Criterion

Optimal bet size: f* = (bp - q) / b, where b = odds, p = probability of winning, q = 1-p.

**Use when**: Repeated decisions where you want to maximize long-term growth rate without risking ruin. Common in investing.

**Practical note**: Full Kelly is aggressive. Most practitioners use fractional Kelly (half or quarter) for safety margin.
