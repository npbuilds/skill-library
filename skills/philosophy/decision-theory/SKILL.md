---
name: decision-theory
description: >
  Direct the decision theory subdomain — route choice-under-uncertainty problems to decision
  structuring, bias detection, or counterfactual analysis. Use when the user needs to make a
  decision with incomplete information, structure a complex choice, identify cognitive biases
  affecting their judgment, evaluate options under uncertainty, or reason about what would
  have happened under different choices.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Decision Theory Director

The department head for rational choice within the philosophy domain. Routes questions about decisions under uncertainty, cognitive biases, and counterfactual reasoning to the right specialist.

Decision theory sits at the intersection of philosophy, psychology, and economics. Where logic checks *whether* reasoning is valid, decision theory checks *whether* choices are rational given what the agent knows and values. Where ethics asks *what's right*, decision theory asks *what's rational*.

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

### Multi-Skill Sequences

**"I'm facing a big decision and I'm not sure I'm thinking clearly"**
1. bias-detector → scan for cognitive biases affecting the framing
2. decision-architect → structure the decision with biases identified
3. counterfactual-reasoner → stress-test by exploring "what if" scenarios for each option

**"We chose X and it went badly — was it the wrong decision?"**
1. counterfactual-reasoner → analyze what would have happened under alternatives
2. bias-detector → check for hindsight bias (outcome was bad ≠ decision was bad)
3. decision-architect → reconstruct the decision as it appeared ex ante

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Expected-value analysis says option A; gut says option B | Check with bias-detector for biases in either direction. Gut feelings sometimes encode information EV analysis misses (experiential knowledge), but they also encode biases | Neither pure calculation nor pure intuition is reliable alone |
| Bias-detector finds biases on all sides | Report all biases; let the user decide which are more distorting. Some biases partially cancel each other | Debiasing is about awareness, not elimination |
| Counterfactual analysis says the decision was good but the outcome was bad | Distinguish decision quality from outcome quality. A good bet that loses is still a good bet | Resulting fallacy: judging decisions by outcomes rather than process |
| Decision-architect produces a clear winner but the user resists | Check for unstated values or constraints not captured in the model. The model may be right given its inputs but missing something | Models are only as good as their inputs |

## Scope Boundaries

**This director handles**: Decision structuring, option evaluation, probability assessment, cognitive bias identification, counterfactual reasoning, causal inference, decision quality assessment.

**Escalate to the orchestrator when**:
- The decision involves moral dimensions beyond rational choice (Ethics)
- The question is about evidence quality rather than decision quality (Epistemology)
- The decision involves strategic interaction with other agents (cross-domain to Game Theory)
- The user wants to challenge their decision framework itself (Dialectical Tools)

## Cross-Domain Connections

- **Investing**: decision-architect connects to `investing/portfolio-construction/asset-allocation` (portfolio = applied decision theory). bias-detector connects to `investing/reflexivity-sentiment/market-psychology` (market biases). counterfactual-reasoner connects to `investing/risk-architecture/tail-risk` (counterfactual reasoning about extreme scenarios).
- **Game Theory**: decision-architect connects to `game-theory/computational-strategy/behavioral-game-theory` (bounded rationality). bias-detector connects to `game-theory/computational-strategy/behavioral-game-theory` (behavioral deviations from equilibrium).
- **Data Science**: bias-detector connects to `data-science/modeling/model-evaluation` (model selection biases). counterfactual-reasoner connects to `data-science/statistical-analysis/causal-inference` (causal inference methods).
