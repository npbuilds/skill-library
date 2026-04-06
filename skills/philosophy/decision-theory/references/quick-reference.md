# Decision Theory — Quick Reference


## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| decision-architect | `decision-architect/SKILL.md` | Action | Structure decisions: enumerate options, model outcomes, assign probabilities, clarify values |
| bias-detector | `bias-detector/SKILL.md` | Action | Identify cognitive biases distorting a decision or judgment |
| counterfactual-reasoner | `counterfactual-reasoner/SKILL.md` | Action | Run "what if" analysis, evaluate causal claims, explore possibility space |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "How should I decide?", "What are my options?", "Structure this decision for me" | decision-architect | Decision framing and structuring |
| "What's the expected value?", "How do I weigh these trade-offs?" | decision-architect | Quantitative decision analysis |
| "Am I being biased?", "What cognitive errors might I be making?" | bias-detector | Bias identification |
| "Why does this feel off?", "Am I overconfident?" | bias-detector | Metacognitive bias check |
| "What would have happened if...?", "Did X cause Y?", "What if we'd chosen differently?" | counterfactual-reasoner | Counterfactual and causal reasoning |
| "Is this correlation or causation?" | counterfactual-reasoner | Causal inference assessment |
| "Should I do X?" (moral dimension) | Escalate to orchestrator — ethics territory | Decision theory handles rationality, not morality |

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Expected-value analysis says option A; gut says option B | Check with bias-detector for biases in either direction. Gut feelings sometimes encode information EV analysis misses (experiential knowledge), but they also encode biases | Neither pure calculation nor pure intuition is reliable alone |
| Bias-detector finds biases on all sides | Report all biases; let the user decide which are more distorting. Some biases partially cancel each other | Debiasing is about awareness, not elimination |
| Counterfactual analysis says the decision was good but the outcome was bad | Distinguish decision quality from outcome quality. A good bet that loses is still a good bet | Resulting fallacy: judging decisions by outcomes rather than process |
| Decision-architect produces a clear winner but the user resists | Check for unstated values or constraints not captured in the model. The model may be right given its inputs but missing something | Models are only as good as their inputs |
