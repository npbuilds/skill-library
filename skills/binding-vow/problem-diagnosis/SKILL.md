---
name: problem-diagnosis
description: >
  Route a problem statement to the right diagnostic skill — typology classification, audience
  detection, stakes assessment, and the mess/wicked reference frameworks. Activate at the start
  of problem framing (six-eyes Phase 2) when you need a typology + audience + stakes profile
  before decomposing or reframing. This director owns the "what kind of problem is this, for
  whom, at what stakes" question.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Problem Diagnosis — Director

Before a problem can be decomposed, reframed, or compressed, it must be *diagnosed*: what kind
of problem is it, who is the statement for, and how much rides on getting it right? This director
realizes six-eyes' Phase 2 (Diagnose). It produces the typology + audience + stakes profile that
drives every downstream choice — which decomposition method applies, how aggressively to compress,
and whether to run the quick or deep lane.

Diagnosis is not solving. The output is a *profile* of the problem, handed back to the
orchestrator (`six-eyes`) to drive mode and routing.

## Routing Table

| Child skill | Use when | Output |
|---|---|---|
| `problem-typology` | You need to classify the statement on the five-way typology (well-defined / ill-defined / wicked / mess / adaptive) | A typology tag that selects the decomposition method |
| `audience-classifier` | You need to confirm who the statement is for (LLM / exec / peer / self / public) | An audience tag that drives the compression target |
| `stakes-assessor` | You need to size the consequences (low / medium / high) | A stakes tag that drives mode selection (quick / standard / deep) |
| `ackoff-mess` | The problem looks like an interrelated system of problems, not a single puzzle | Reference: Ackoff's mess concept (dissolution beats solution) |
| `wicked-vs-tame` | You need the conceptual basis for a wicked / tame / adaptive classification | Reference: Rittel & Webber (1973) + Heifetz adaptive/technical |

## Routing Logic

1. Run `problem-typology` first — it anchors everything downstream. If it returns **mess** or
   **wicked**, pull the matching reference (`ackoff-mess` / `wicked-vs-tame`) to ground the call.
2. Run `audience-classifier` and `stakes-assessor` in parallel — they are independent.
3. Hand the combined profile (typology + audience + stakes) back to `six-eyes`, which uses it to
   select the mode and the decomposition method.

## Scope Boundaries

- **In scope:** classifying the problem, its audience, and its stakes.
- **Out of scope:** decomposing the problem (→ `problem-decomposition`), reframing it
  (→ `problem-reframing`), or auditing the final statement (→ `statement-audit`).
- **Escalate to `six-eyes`** when the typology comes back contested (e.g., disagreement on
  wicked vs. ill-defined) so the orchestrator can upgrade the mode to `deep`.
