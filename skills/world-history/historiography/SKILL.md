---
name: historiography
description: >
  Route questions about historical methods, source evaluation, schools of interpretation,
  historical thinking skills, and how history is written and contested. Activate when users
  ask how we know what we know about the past, how to evaluate evidence, or how different
  historians interpret the same events.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
tools: Read
---

# Historiography — The Scriptorium

The Scriptorium is where history turns inward and examines itself. Before you can learn *what* happened, you need to understand *how we know* what happened — and *why different historians disagree* about what it means. This wing teaches the craft of history: the cognitive tools, the evidentiary standards, the interpretive traditions, and the art of constructing arguments from imperfect sources.

Historiography is not a single skill but a family of related competencies. Historical thinking (how to process evidence) is distinct from schools of thought (how traditions shape interpretation), which is distinct from source criticism (how to evaluate individual pieces of evidence), which is distinct from historical argument (how to build a case).

## Child Skills

| Skill | Type | Path | Handles |
|---|---|---|---|
| `historical-thinking` | knowledge | `historical-thinking/SKILL.md` | The cognitive toolkit: sourcing, contextualization, corroboration, perspective-taking, ethical judgment |
| `schools-of-thought` | knowledge | `schools-of-thought/SKILL.md` | Ranke, Marxist, Annales, postcolonial, gender, linguistic turn, digital humanities, non-Western traditions |
| `source-criticism` | knowledge | `source-criticism/SKILL.md` | Evaluating specific sources: primary/secondary, bias, provenance, reliability |
| `historical-argument` | knowledge | `historical-argument/SKILL.md` | Building and critiquing claims: thesis, evidence, causation, counterfactuals |
| `source-evaluator` | action | `source-evaluator/SKILL.md` | Structured source evaluation with output template |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| "How do historians know...," "how do we know," "what's the evidence for" | `source-criticism` | Questions about evidentiary basis |
| "How should I think about," "how to analyze," "what's the framework for" | `historical-thinking` | Questions about cognitive approach |
| "Why do historians disagree about," "what are the different interpretations" | `schools-of-thought` | Questions about interpretive traditions |
| "Is this argument convincing," "how would you prove," "what caused" | `historical-argument` | Questions about claims and causation |
| "Evaluate this source," "what can this document tell us," "is this reliable" | `source-evaluator` → `source-criticism` | Specific source in hand → evaluate it |
| "How has the study of X changed over time" | `schools-of-thought` | Meta-historiographical questions |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "How do we know the Battle of Thermopylae really happened?" | source-criticism → historical-argument | First evaluate what sources exist, then assess how they build the case |
| "Why do Marxist and liberal historians disagree about the Industrial Revolution?" | schools-of-thought → historical-argument | First explain the traditions, then show how they construct different arguments from the same evidence |
| "Teach me to think like a historian" | historical-thinking → source-criticism → historical-argument | Foundation → application → synthesis |

## Curriculum Order

1. **`historical-thinking`** (foundation) — The cognitive operating system. Must be internalized before any content skill is useful.
2. **`source-criticism`** (core method) — How to evaluate individual pieces of evidence.
3. **`historical-argument`** (synthesis) — How to construct and evaluate claims.
4. **`schools-of-thought`** (advanced) — How traditions shape interpretation.

### Level Progression
- **Foundational**: historical-thinking, source-criticism
- **Intermediate**: historical-argument
- **Advanced**: schools-of-thought, source-evaluator (action)

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Source says X but tradition interprets as Y | Source-criticism wins | Evidence trumps tradition; but name the tradition's reasoning |
| Two valid interpretive frameworks disagree | Present both, name stakes | The Scriptorium teaches the debate, not the verdict |
| Historical-thinking heuristic vs. content-specific knowledge | Content-specific wins for that case | General heuristics are defaults; domain expertise overrides when warranted |

**General rule**: Method before conclusion. When in doubt, teach the user how to figure it out rather than what to think.

## Scope Boundaries

**This director handles**: All questions about how history works as a discipline — methods, evidence, interpretation, argument, and the history of history itself.

**Escalate to wan-shi-tong when**:
- The question is about a specific historical event (route to the thematic wing)
- The question is about applying history to present decisions (route to applied-history)
- The question requires regional expertise (route to regional-atlas)