# Six Eyes — Quick Reference


## Quick Reference

| Audience tag | Skill |
|---|---|
| exec | `bluf-shaper` (military / executive bottom-line-up-front) or `executive-distiller` (full Minto Pyramid) |
| peer | `scqa-formatter` (Situation, Complication, Question, Answer) |
| LLM | `cursed-speech` (Anthropic-canonical structural order: role → context → longform-data → examples → numbered instructions → output format → self-check) |
| self | `scqa-formatter` with self-framing, or Polya Step 1 restatement |
| public | `executive-distiller` with audience-aware register |

## Modes

| Mode | Phases run | Wall-clock target | When to use |
|---|---|---|---|
| `quick` | 1 → 5 (compression) → 6 (statement-grader only) | ≤30s | Low-stakes statements; routine work; the architectural answer to Reiter-Palmon's automaticity finding. Skip diagnosis, decomposition, reframing, full audit. |
| `standard` | 1 → 7, single pass | 2–5 min | Genuine inquiry; default for unspecified requests. |
| `deep` | 1 → 7 with frame rotation ≥3 alternatives, full adversarial XY check, audience pass for two audiences (typically LLM + exec) | 5–15 min | High stakes; wicked or mess typology; deeply contested formulations. |

## Quick Reference

| Level | Action | Trigger |
|---|---|---|
| **L1 — Rephrase and retry** | Reformulate using different terminology or restated subject; re-run statement-grader | Cosmetic axes failing (specificity, scope) on first iteration |
| **L2 — Decompose further** | Call `claim-decomposer` to split the statement into sub-statements; re-state each independently | Compound failure; root-vs-symptom axis fails |
| **L3 — Depth upgrade** | Move `quick` → `standard` → `deep`; rerun with deeper frame rotation | Multiple axes fail across iterations; deep contestation |
| **L4 — User assist** | Ask the user what specifically isn't landing | Three iterations through L1–L3 failed |

## Quick Reference

| Phase | Skill called (domain) | Purpose |
|---|---|---|
| 3 | `claim-decomposer` (research) | Atomic-claim decomposition with dependency graph + priority tags |
| 3, 4, 6 | `assumption-excavator` (philosophy/logic) | Hidden premises (Definitional / Causal / Value / Scope / Framing) |
| 4 | `socratic-examiner` (philosophy/dialectical-tools) | Surface assumptions and contradictions when stuck |
| 4 | `steel-man-forge` (philosophy/dialectical-tools) | Strongest opposing formulation |
| 4 | `dialectic-engine` (philosophy/dialectical-tools) | Multi-round point-counterpoint |
| 4 | `values-excavator` (philosophy/ethics) | Whose interests centered, hidden values |
| 5 | `argument-structure` (writing/rhetoric) | Toulmin / Rogerian / classical document shape |
| 5 | `clarity-engine` (neocortex) | Post-compression accessibility check |
| 6 | `evidence-evaluator` (philosophy/epistemology) | Evidence quality and source reliability |
| 6 | `demarcation-judge` (philosophy/philosophy-of-science) | Popperian falsifiability |
| 6 | `argument-analyst` (philosophy/logic) | Validity, soundness, fallacy detection |

## Failure Recovery

| Failure | Response |
|---|---|
| Statement is too vague to even restate | Ask the user for one clarifying example or one specific consequence; do not proceed without it |
| Decomposition produces 15+ atomic claims | Ask the user to prioritize; investigate top claims at full depth, remainder at quick |
| Audience tag conflicts (e.g., simultaneously exec and LLM) | Run compression twice (deep mode default for two audiences); present both shapes |
| `statement-grader` fails on `audience-fit` after 3 iterations | Default to L4 user assist; the audience model may be wrong |
| Cross-domain skill returns an error or is unavailable | Continue with available phases; mark the missing analysis as a gap in the final output, do not fabricate |
| Loop reaches iteration cap with no convergence | Present the trajectory and the latest statement; flag the remaining failure axis explicitly |
