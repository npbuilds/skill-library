# Decision Architect — Quick Reference


## Quick Reference

| Situation | Framework | How It Works |
|-----------|-----------|-------------|
| Probabilities estimable, outcomes quantifiable | **Expected Value** | Probability × payoff for each outcome; choose highest EV |
| Outcomes quantifiable but probabilities unknown | **Minimax Regret** | For each option, calculate worst-case regret; minimize the maximum regret |
| High uncertainty, catastrophic downside possible | **Maximin** | Choose the option whose worst-case outcome is least bad |
| Decision is sequential / information will arrive | **Decision Tree / Real Options** | Map the decision sequence; value the option to learn and adapt |
| Multiple competing objectives | **Multi-Criteria Decision Analysis** | Score each option against each criterion; weight criteria by importance |
| Risk of ruin / non-ergodic situation | **Kelly Criterion / Ruin Avoidance** | Never bet enough to face ruin, even if EV is positive |

## Formula / Pseudocode

```
Option A:
  Outcome A1 (best case):  [description] — Probability: [estimate]
  Outcome A2 (base case):  [description] — Probability: [estimate]
  Outcome A3 (worst case): [description] — Probability: [estimate]
```
