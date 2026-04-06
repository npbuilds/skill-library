# Computational Strategy — Quick Reference


## Quick Reference

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| PPAD-completeness, complexity of Nash, can we compute equilibria? | `algorithmic-game-theory` | Computational complexity |
| Price of anarchy, price of stability, efficiency of selfish routing | `algorithmic-game-theory` | Efficiency of equilibria |
| Congestion games, potential games, Braess paradox | `algorithmic-game-theory` | Network/algorithmic games |
| Algorithmic mechanism design, computational mechanism design | `algorithmic-game-theory` | Intersection with mechanism design |
| Level-k thinking, cognitive hierarchy, depth of reasoning | `behavioral-game-theory` | Bounded rationality models |
| QRE, quantal response, noisy best response | `behavioral-game-theory` | Stochastic choice models |
| Social preferences, fairness, inequality aversion, reciprocity | `behavioral-game-theory` | Non-standard preferences |
| Experimental game theory, lab results, real humans playing games | `behavioral-game-theory` | Empirical evidence |
| Fictitious play, no-regret learning, regret matching | `learning-in-games` | Learning algorithms |
| Multi-agent reinforcement learning (MARL), self-play, AlphaGo | `learning-in-games` | AI/ML game theory |
| Mean field games, large population limits | `learning-in-games` | Continuum approximations |
| LLM alignment, RLHF, AI safety as game theory | `learning-in-games` | Frontier AI applications |
| "How would real people play this?", "Is the Nash realistic?" | `behavioral-game-theory` first, then `learning-in-games` | Behavioral prediction |
| "Can a computer solve this game?" | `algorithmic-game-theory` | Complexity assessment |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Algorithmic GT says "Nash is PPAD-hard to compute" but learning GT says "no-regret learning converges" | Both correct but converge to different concepts — no-regret converges to coarse correlated equilibrium (CCE), which is weaker than Nash. Present the distinction: CCE is computable, Nash is not (in general) | Different solution concepts have different computational properties |
| Behavioral GT predicts level-2 play but learning GT predicts convergence to Nash after 1000 rounds | Time scale matters — behavioral predictions apply to early/few-shot play; learning predictions apply to repeated interaction. Both can be correct for different time horizons | Short-run ≠ long-run behavior |
| Nash says defect in PD but behavioral GT shows 40-60% cooperation in experiments | Present both — Nash is the rational benchmark, behavioral evidence shows humans deviate due to social preferences, reciprocity, and bounded rationality. Neither is "wrong" — they answer different questions | Normative (what should you do?) vs. descriptive (what do people do?) |
| Price of anarchy is large but learning dynamics converge to efficient outcomes | PoA measures worst-case. Learning dynamics may avoid worst-case equilibria. Report both — PoA as a bound, dynamics as a prediction | Worst-case vs. typical-case analysis |
