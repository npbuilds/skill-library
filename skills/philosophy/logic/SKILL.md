---
name: logic
description: >
  Direct the logic subdomain — route reasoning evaluation tasks to argument analysis,
  formal logic, or assumption excavation. Use when evaluating argument validity, detecting
  fallacies, checking logical structure, formalizing natural-language reasoning, or
  surfacing hidden premises.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Logic Director

The department head for reasoning evaluation within the philosophy domain. Routes questions about argument quality, validity, fallacies, and hidden premises to the right specialist.

Logic is the skeleton of all reasoning. Every other philosophy subdomain assumes sound logical structure — ethics without logic is sentiment, epistemology without logic is opinion, decision theory without logic is guessing.

## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| argument-analyst | `argument-analyst/SKILL.md` | Action | Evaluate an argument for validity, soundness, and fallacies; produce a structured diagnosis |
| assumption-excavator | `assumption-excavator/SKILL.md` | Action | Surface hidden premises, unstated warrants, and implicit framing in any argument or text |
| formal-logic | `formal-logic/SKILL.md` | Knowledge | Propositional, predicate, and modal logic essentials for formalizing arguments |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Is this argument valid?", "Does this follow?", "What's wrong with this reasoning?" | argument-analyst | Core validity and soundness evaluation |
| "What fallacy is this?", "Is this a straw man / ad hominem / etc.?" | argument-analyst | Fallacy identification and diagnosis |
| "What am I assuming?", "What's hidden in this argument?", "What's taken for granted?" | assumption-excavator | Hidden premise and warrant extraction |
| "Formalize this argument", "Put this in logical notation", "Is this a tautology?" | formal-logic | Symbolic formalization |
| "Is this argument persuasive?" (persuasiveness, not validity) | Escalate to orchestrator — rhetoric territory | Logic evaluates structure, rhetoric evaluates force |
| "Should I believe this conclusion?" (evidence quality, not argument structure) | Escalate to orchestrator — epistemology territory | Logic checks the reasoning; epistemology checks the evidence |

### Multi-Skill Questions

Some questions need both skills in sequence:

1. **assumption-excavator first** — surface the hidden premises
2. **argument-analyst second** — evaluate the full argument (stated + excavated premises) for validity

This order ensures we evaluate the *complete* argument, not just its visible portion. Many arguments are valid given their stated premises but unsound because the hidden premises are false.

**Example**: "We should ban X because it's unnatural."
1. assumption-excavator → surfaces hidden premise: "Unnatural things are bad" (appeal to nature)
2. argument-analyst → argument is valid (if unnatural = bad, and X is unnatural, then X is bad) but unsound (the hidden premise is a known fallacy)

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Argument-analyst says valid; user insists it "feels wrong" | Check with assumption-excavator for hidden premises the user may be sensing | Intuitive discomfort often signals an unstated assumption, not a logical error |
| Multiple fallacy classifications apply | Report the primary fallacy (the one that most damages the argument) and note secondary issues | Arguments can commit multiple fallacies; prioritize by impact on conclusion |
| Argument is formally valid but substantively absurd | Distinguish validity (structure) from soundness (truth of premises) — a valid argument with false premises produces garbage | Logic's job is structural; premise truth is epistemology's job |

## Scope Boundaries

**This director handles**: Argument structure, validity, soundness, fallacies, hidden premises, logical form, informal reasoning errors.

**Escalate to the orchestrator when**:
- The question is about evidence quality or source reliability (Epistemology)
- The question is about moral reasoning, not logical structure (Ethics)
- The question is about persuasive force rather than logical validity (cross-domain to Rhetoric)
- The question asks for Socratic questioning or devil's advocacy (Dialectical Tools)
- The question spans multiple philosophy subdomains
