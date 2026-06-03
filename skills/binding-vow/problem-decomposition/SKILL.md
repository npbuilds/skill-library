---
name: problem-decomposition
description: >
  Route a diagnosed problem to the right decomposition method — root-cause technique selection
  and the Polya heuristic catalog. Activate at six-eyes Phase 3 (Decompose), after a typology
  profile exists, when you need to break a statement into atomic, root-tagged parts before
  reframing or auditing. This director owns the "break it down to its real components" question.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Problem Decomposition — Director

A diagnosed problem is rarely atomic. This director realizes six-eyes' Phase 3 (Decompose): it
selects the right root-cause method for the problem's typology and stakes, tags each piece as
root vs. symptom, and grounds the work in Polya's problem-solving heuristics. The goal is a set
of atomic, root-tagged claims that downstream reframing and audit can operate on cleanly.

Decomposition partners with the research domain's `claim-decomposer` (cross-domain) for atomic-claim
extraction; this director focuses on *root-cause structure* — which split is causal, which is
cosmetic.

## Routing Table

| Child skill | Use when | Output |
|---|---|---|
| `root-vs-symptom-tagger` | You need to pick a root-cause method (5 Whys / Fishbone / dependency map / Current Reality Tree) and tag each part root vs. symptom | Method choice + per-claim root/symptom tags |
| `polya-method` | You need the heuristic basis for understand → plan → execute → look-back, or specialize/generalize moves | Reference: Polya's *How to Solve It* catalog |

## Routing Logic

1. Take the typology tag from `problem-diagnosis`. It selects the method: dependency mapping for
   **mess**, Current Reality Tree for **wicked**, 5 Whys / Fishbone for **well-** or
   **ill-defined**. `root-vs-symptom-tagger` performs this selection.
2. Pull `polya-method` when the decomposition stalls — its specialize/generalize operations and
   the "understand the problem" step often unstick a tangled statement.
3. If decomposition yields 15+ atomic claims, hand back to `six-eyes` to ask the user to
   prioritize before continuing.

## Scope Boundaries

- **In scope:** selecting a decomposition method, root vs. symptom tagging, Polya heuristics.
- **Out of scope:** classifying the problem (→ `problem-diagnosis`), generating alternative
  formulations (→ `problem-reframing`).
- **Cross-domain:** atomic-claim extraction proper is `research/claim-decomposer`; this director
  routes to it via the orchestrator rather than duplicating it.
