# Cross-Domain Routing — Input/Output Contracts

The orchestrator's routing table makes calls to skills outside the `binding-vow` domain. This file specifies the contract for each: what to pass in, what comes back, and how it slots into a phase.

The `binding-vow` suite is a *coordinator* over the existing library, not a parallel reimplementation. These contracts are how that coordination stays clean.

## Phase 3 — Decompose

### `claim-decomposer` (research)

**Pass:**
- The restated statement from Phase 1 intake
- The typology tag from Phase 2 (well-defined / ill-defined / wicked / mess / adaptive)
- Any constraints the user specified

**Receive:**
- A numbered list of atomic claims, each typed (factual/causal/comparative/predictive/definitional/existential/evaluative), domain-tagged, and priority-ranked (critical/supporting/contextual)
- Hidden assumptions surfaced as separate verifiable claims
- A dependency graph
- Suggested verification strategy per claim

**Use:** atomic claim list feeds `root-vs-symptom-tagger`; dependency graph informs which reframing operations apply per-claim.

### `assumption-excavator` (philosophy/logic)

**Pass:**
- The restated statement
- Domain context (which subject area)
- Depth: `surface` (quick scan, top assumptions only) for Phase 3; `deep` for Phase 4 reframing

**Receive:**
- Hidden assumptions in six categories (Factual / Definitional / Causal / Value / Scope / Framing)
- Per-assumption properties: visibility, contestability, load-bearing, domain-standard
- Counterfactuals: "if [assumption] is false, then [consequence]"
- Most-critical-hidden-assumptions ranked list

**Use:** Phase 3 surfaces hidden premises; Phase 4 (with `depth=deep`) drives `frame-rotator` operations (including the specialize/generalize moves Polya called "level-shifting" — folded into frame-rotator per v2); Phase 6 `scope-bounder` reuses with `category=scope` filter.

## Phase 4 — Reframe

### `socratic-examiner` (philosophy/dialectical-tools)

**Pass:** the statement plus the specific reasoning step that feels stuck or unclear.

**Receive:** a structured sequence of Socratic questions with the reasoning behind each, surfacing assumptions and contradictions.

**Use:** when `frame-rotator` produces alternatives that all feel equally weak — Socratic questioning often reveals the formulation is wrong at a deeper level.

### `steel-man-forge` (philosophy/dialectical-tools)

**Pass:** the current best statement and the user's apparent position.

**Receive:** the strongest possible version of the *opposing* formulation — what someone who disagrees with this framing would say.

**Use:** to test whether the current framing survives the strongest objection. If the opposing frame is plainly stronger, swap.

### `dialectic-engine` (philosophy/dialectical-tools)

**Pass:** the statement and 2–3 candidate alternative formulations from `frame-rotator`.

**Receive:** thesis/antithesis/synthesis dialogue across multiple rounds, producing a synthesized formulation that integrates the strongest elements.

**Use:** for deeply contested formulations where multiple alternatives have merit and the right answer is a synthesis.

### `values-excavator` (philosophy/ethics)

**Pass:** the statement.

**Receive:** implicit values surfaced; competing goods identified; whose interests are centered, whose are invisible; the moral logic of the position made explicit.

**Use:** drives `stakeholder-rotator`. Especially load-bearing for adaptive (Heifetz) and wicked (Rittel) typologies, where stakeholder interests ARE the problem.

## Phase 5 — Compress

### `argument-structure` (writing/rhetoric)

**Pass:** the compressed statement and the audience tag.

**Receive:** Toulmin / Rogerian / classical / volta-shaped scaffolding appropriate to the audience.

**Use:** for document-shape outputs (executive memos, investment memos, public-facing writeups). Skip for LLM compression — that's `cursed-speech`'s job.

### `clarity-engine` (neocortex)

**Pass:** the compressed statement.

**Receive:** an accessibility check — flags jargon, missing analogies, and parts that won't land for the target audience.

**Use:** post-compression sanity check. Optional in `standard` mode; mandatory in `deep` mode.

## Phase 6 — Audit

### `evidence-evaluator` (philosophy/epistemology)

**Pass:** the statement, framed as a question; the kind of evidence that would resolve it.

**Receive:** judgment on whether the kind of evidence required exists and is accessible; assessment of how strong it would need to be.

**Use:** drives `answerability-tester`. If no evidence could resolve the statement, it's a values/preferences question masquerading as a factual one — needs reformulation.

### `demarcation-judge` (philosophy/philosophy-of-science)

**Pass:** the statement, framed as a claim.

**Receive:** falsifiability assessment using Popperian criteria; what would prove the claim wrong; whether the statement makes risky predictions.

**Use:** drives `falsifiability-checker`. A statement that cannot be falsified in principle is ungradeable on the falsifiability axis; reformulate or accept the un-falsifiable status.

### `argument-analyst` (philosophy/logic)

**Pass:** the statement plus its implicit reasoning structure (premises → conclusion).

**Receive:** validity assessment, soundness assessment, fallacy detection.

**Use:** optional Phase 6 check. Especially useful when the statement is a candidate *answer* the user wants to verify before committing — but that's solver territory, so usually deferred.

## Failure modes

| Failure | Response |
|---|---|
| Cross-domain skill is unavailable or errors | Continue with available phases; mark the missing analysis as a gap in the final output. Do not fabricate or substitute. |
| Cross-domain skill returns a result that contradicts another phase's output | Surface the contradiction to the user; do not silently reconcile. |
| Cross-domain skill expects context this orchestrator doesn't carry | Ask the user for the missing context, or skip the call and document the gap. |

## Update protocol

When a new skill is added to a domain that `six-eyes` could profitably call (e.g., a new philosophy/ethics skill that's better at stakeholder-mapping than `values-excavator`), update:

1. The routing table in this file with the new contract
2. The corresponding routing-table row in `SKILL.md`
3. The relevant phase's call list
4. (Optionally) the static map maintained by `growth-architect` for `cursed-speech`

The routing table is the binding-vow suite's API surface to the rest of the library. Keep it explicit.
