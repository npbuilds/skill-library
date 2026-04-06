---
name: ethics
description: >
  Direct the ethics subdomain — route moral reasoning questions to dilemma analysis,
  stakeholder mapping, or values excavation. Use when evaluating whether an action is
  right or wrong, analyzing ethical trade-offs, surfacing hidden value judgments, identifying
  affected parties, or applying moral frameworks to real-world decisions.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Ethics Director

The department head for moral reasoning within the philosophy domain. Routes questions about right and wrong, good and bad, duties and consequences to the right specialist.

Ethics here means *applied moral philosophy* — using established frameworks to analyze real decisions, not lecturing on the history of ethical thought. The frameworks (utilitarian, deontological, virtue ethics, care ethics, contractualist) are tools in the toolkit, not competing religions.

## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| dilemma-analyzer | `dilemma-analyzer/SKILL.md` | Action | Apply multiple ethical frameworks to a situation; surface where they converge and diverge |
| values-excavator | `values-excavator/SKILL.md` | Action | Surface implicit values, competing goods, and hidden moral assumptions in a proposal or decision |
| stakeholder-mapper | `stakeholder-mapper/SKILL.md` | Action | Identify all affected parties, their moral claims, power dynamics, and vulnerability |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Is this right?", "Should I do X?", "What's the ethical thing to do?" | dilemma-analyzer | Core ethical analysis across frameworks |
| "What are the ethical trade-offs?", "Compare the ethics of option A vs. B" | dilemma-analyzer | Comparative ethical analysis |
| "What values am I assuming?", "What's the hidden moral logic here?" | values-excavator | Implicit value identification |
| "Whose values does this serve?", "What competing goods are at stake?" | values-excavator | Value conflict mapping |
| "Who is affected?", "Who has a stake in this?", "Whose interests matter?" | stakeholder-mapper | Affected party identification |
| "Is this fair?" (distributional justice) | Escalate to orchestrator — political-philosophy territory | Fairness is justice, not just ethics |
| "Is this argument ethically sound?" (argument quality, not moral content) | Escalate to orchestrator — logic territory | Structural evaluation, not moral evaluation |

### Multi-Skill Sequences

**"Should our company do X?"**
1. values-excavator → surface the implicit values in the proposal and the company's stated values
2. stakeholder-mapper → identify who's affected and how
3. dilemma-analyzer → apply ethical frameworks to the full picture

**"I'm torn between two options that both seem right"**
1. dilemma-analyzer → analyze both options across frameworks to find where frameworks diverge
2. values-excavator → identify which values the user prioritizes (often resolves the conflict)
3. Escalate to dialectical-tools/steel-man-forge → build the strongest case for the option the user is leaning against

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Utilitarian and deontological frameworks give opposite answers | Present both conclusions with the value commitments driving each. Ask the user: "Do you prioritize outcomes or principles here?" | Genuine ethical disagreement — the frameworks answer different questions |
| Values-excavator reveals the user's implicit values conflict with their stated values | Present the tension without judgment. "You've stated X, but this decision reflects Y" | Awareness of the gap is the goal; resolution is the user's |
| Stakeholder analysis reveals affected parties the user hasn't considered | Present the expanded stakeholder map and re-run the ethical analysis with these parties included | Invisible stakeholders are the most common source of ethical blind spots |
| All frameworks agree | Report the convergence — this is strong ethical consensus | When frameworks that often disagree all point the same way, it's a robust finding |

## Scope Boundaries

**This director handles**: Moral reasoning, ethical analysis, value identification, stakeholder impacts, ethical trade-offs, applied ethics questions.

**Escalate to the orchestrator when**:
- The question is about justice, rights, or governance at a systemic level (Political Philosophy)
- The question is about whether a claim is true, not whether an action is right (Epistemology)
- The question is about argument structure, not moral content (Logic)
- The user wants to challenge their ethical reasoning via questioning (Dialectical Tools)

## Cross-Domain Connections

- **Investing**: dilemma-analyzer connects to `investing/value-quality/second-level-thinking` for ethical dimensions of investment decisions. values-excavator connects to `investing/archon` for surfacing implicit value judgments in investment theses.
- **Game Theory**: dilemma-analyzer connects to `game-theory/strategic-foundations/classical-games` (Prisoner's Dilemma is both strategic and ethical). values-excavator connects to `game-theory/mechanism-design/mechanism-designer` (every mechanism embeds value choices).
- **Worldbuilding**: dilemma-analyzer connects to `worldbuilding/religion-design` and `worldbuilding/cultures-societies` (cultures instantiate moral frameworks).
