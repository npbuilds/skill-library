---
name: philosophy-of-science
description: >
  Direct the philosophy of science subdomain — route methodology and demarcation questions
  to the right specialist. Use when evaluating study design, assessing scientific methodology,
  distinguishing science from pseudoscience, identifying paradigmatic assumptions, or
  critiquing research methods.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Philosophy of Science Director

The department head for scientific reasoning within the philosophy domain. Routes questions about methodology, demarcation, and paradigms to the right specialist.

Philosophy of science asks: what makes science *science*? When is a study well-designed? When does a field's methodology actually justify its claims? These questions matter because most real-world decisions that invoke "the science says..." depend on whether the science in question is methodologically sound.

## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| methodology-critic | `methodology-critic/SKILL.md` | Action | Evaluate study design, identify methodological weaknesses, assess internal/external validity |
| demarcation-judge | `demarcation-judge/SKILL.md` | Action | Distinguish science from pseudoscience, evaluate whether a claim meets scientific standards |
| paradigm-analyst | `paradigm-analyst/SKILL.md` | Knowledge | Identify operating paradigms and their assumptions using Kuhn/Lakatos/Popper |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Is this study well-designed?", "What's wrong with this methodology?" | methodology-critic | Study design evaluation |
| "Can we trust these results?", "Is this replicable?" | methodology-critic | Results reliability assessment |
| "Is this real science?", "Is this pseudoscience?", "Is this a legitimate field?" | demarcation-judge | Science/pseudoscience demarcation |
| "What paradigm is this operating under?", "What assumptions does this field make?" | paradigm-analyst | Paradigmatic analysis |
| "Is this evidence strong?" (general evidence quality) | Escalate to orchestrator — epistemology territory | Evidence evaluation is broader than methodology |
| "Is this study ethical?" | Escalate to orchestrator — ethics territory | Research ethics, not research methodology |

### Multi-Skill Sequences

**"This study claims X — should I believe it?"**
1. methodology-critic → evaluate the study's design and methods
2. Escalate to epistemology/evidence-evaluator → place the study within the broader evidence hierarchy
3. If the field itself is in question → demarcation-judge

**"Is [field] a real science?"**
1. demarcation-judge → apply demarcation criteria
2. methodology-critic → evaluate the field's typical methodology
3. paradigm-analyst → identify the paradigmatic assumptions

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Methodology looks sound but conclusions seem wrong | Check the assumptions, not just the methods. Sound methodology with flawed premises produces rigorous nonsense | Garbage in, garbage out — even with excellent methods |
| Study passes methodology check but field fails demarcation | Report both findings. A well-designed study in a pseudoscientific field is still epistemically suspect | The field's theoretical framework matters alongside individual study quality |
| Multiple methodological standards apply | Use the standard appropriate to the field. Don't apply clinical trial standards to historical research or vice versa | Methodological pluralism — different questions require different methods |

## Scope Boundaries

**This director handles**: Research methodology evaluation, study design critique, scientific demarcation, paradigm identification, internal and external validity assessment.

**Escalate to the orchestrator when**:
- The question is about evidence quality in general, not methodology specifically (Epistemology)
- The question is about whether an argument is logically valid, not methodologically sound (Logic)
- The question is about the ethics of research, not its quality (Ethics)
- The question is about statistical analysis specifically (cross-domain to Data Science)

## Cross-Domain Connections

- **Data Science**: methodology-critic connects to `data-science/modeling/model-evaluation` (model evaluation is applied philosophy of science). demarcation-judge connects to `data-science/statistical-analysis/statistical-testing` (statistical significance as demarcation criterion).
- **Research**: methodology-critic complements `research/source-triangulator` (methodological quality as a triangulation dimension).
- **Investing**: methodology-critic connects to `investing/regime-intelligence` (evaluating economic research methodology).
