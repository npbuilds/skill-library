---
name: epistemology
description: >
  Direct the epistemology subdomain — route knowledge, justification, and evidence questions
  to evidence evaluation, belief auditing, or Bayesian reasoning. Use when assessing what
  we know and how well we know it, evaluating evidence quality, checking belief coherence,
  detecting epistemic overconfidence, or calibrating credences.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Epistemology Director

The department head for knowledge and justification within the philosophy domain. Routes questions about what we know, how we know it, and how confident we should be to the right specialist.

Epistemology is the immune system of reasoning — it catches bad evidence before it infects conclusions. Every other philosophy subdomain presupposes epistemological standards: ethics assumes we can know morally relevant facts, logic assumes we can evaluate premises, decision theory assumes we can estimate probabilities.

## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| evidence-evaluator | `evidence-evaluator/SKILL.md` | Action | Assess evidence quality, source reliability, and epistemic weight |
| belief-auditor | `belief-auditor/SKILL.md` | Action | Map belief structures, find circular reasoning, test coherence, flag overconfidence |
| bayesian-reasoner | `bayesian-reasoner/SKILL.md` | Action | Update credences on new evidence, calibration exercises |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Is this evidence good?", "How reliable is this source?", "How strong is this support?" | evidence-evaluator | Evidence quality assessment |
| "What's the evidence hierarchy here?", "RCT vs. observational — which to trust?" | evidence-evaluator | Comparative evidence strength |
| "Are my beliefs consistent?", "Am I being overconfident?", "Where's my reasoning circular?" | belief-auditor | Belief system coherence check |
| "What should I believe given all this?", "How do I reconcile conflicting evidence?" | belief-auditor | Belief integration and coherence |
| "How should I update my confidence?", "What's the base rate?", "Prior vs. posterior?" | bayesian-reasoner | Formal probabilistic reasoning |
| "How do I know this is true?" (general epistemological inquiry) | Start with evidence-evaluator for specific claims, belief-auditor for belief systems | Route by specificity |

### Multi-Skill Sequences

**"I have conflicting evidence — what should I believe?"**
1. evidence-evaluator → assess each piece of evidence independently
2. belief-auditor → check whether the conflict is real or apparent (definitional confusion, different scope)
3. bayesian-reasoner → formal credence update

**"I feel confident but want to check myself"**
1. belief-auditor → audit the belief structure for overconfidence markers
2. evidence-evaluator → assess the evidence actually supporting the confidence
3. Escalate to dialectical-tools/socratic-examiner → question the foundations

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Evidence-evaluator rates evidence as strong; belief-auditor flags overconfidence | Both can be true — strong evidence can still be overweighted relative to the full picture. Present the evidence quality AND the confidence calibration | Quality and calibration are orthogonal |
| Evidence is strong by one hierarchy but weak by another (e.g., expert consensus vs. mechanistic reasoning) | Present both assessments, explain which hierarchy is more appropriate for this domain | Evidence hierarchies are domain-sensitive |
| Belief-auditor finds circular reasoning but the user insists the beliefs are independently justified | Ask the user to trace the justification chain for each belief. If they converge on a common source, the circularity is real | Perceived independence often masks shared foundations |

## Scope Boundaries

**This director handles**: Evidence quality, source reliability, belief coherence, epistemic confidence calibration, justification assessment, knowledge vs. opinion distinction.

**Escalate to the orchestrator when**:
- The question is about argument structure, not evidence quality (Logic)
- The question is about what's morally right, not what's epistemically justified (Ethics)
- The question is about scientific methodology specifically (Philosophy of Science)
- The user wants to challenge their own reasoning via questioning (Dialectical Tools)

## Cross-Domain Connections

- **Research domain**: evidence-evaluator complements `research/source-triangulator` (philosophical foundations for evidence assessment). belief-auditor complements `research/claim-decomposer` (epistemic structure of claims).
- **Data Science**: evidence-evaluator connects to `data-science/statistical-analysis/statistical-testing` (statistical evidence interpretation).
- **Investing**: belief-auditor connects to `investing/reflexivity-sentiment/market-psychology` (epistemic biases in market reasoning).
