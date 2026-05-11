---
name: six-eyes
description: >
  Orchestrate problem-statement quality across diagnosis, decomposition, reframing, compression,
  and audit. Use when stating a problem to an LLM, executive, peer, or yourself; when a question
  feels off but the issue isn't obvious; or when high-stakes work depends on getting the
  formulation right before solving. Routes to typology, audience-fit, and statement-grading
  sub-skills with a re-state loop for sub-threshold outputs.
metadata:
  author: nirav
  version: "2.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent WebSearch WebFetch
---

# Six Eyes — The Problem-Statement Orchestrator

A problem well stated is a problem half solved. The bottleneck in most reasoning — human and machine — is not the reasoner, it is the formulation handed to the reasoner. Six Eyes takes fuzzy intent and produces a statement that is correctly typed, decomposed to atomic, fit to its audience, and audited for the standard failure modes (XY substitution, attribute substitution, Einstellung, Type III error). It is invoked explicitly, not by default, and supports a fast lane for low-stakes statements and a deep lane for high-stakes ones.

## Guiding Principles

These are non-negotiable and override all other instructions:

1. **Fix the statement, not the solver.** Six Eyes does not solve problems. It produces a statement another skill or human can solve.
2. **Assume the first description is misleading.** Reiter-Palmon: problem construction is automatic; users don't know they're constructing. Restate before processing.
3. **Audience-fit is a hard constraint.** A statement that doesn't fit its audience has failed regardless of its other qualities.
4. **Loop, don't pipeline.** Wicked problems (Rittel & Webber) require iteration. The re-state loop is structural, not optional.
5. **Compression is force.** A self-imposed constraint that amplifies power: give up scope, gain force. Fewer precise words compel a sharper response.
6. **No silent looping.** Cap iterations and surface the convergence trajectory when the loop terminates.

## Phases

### Phase 1 — Intake

Parse the dump and establish parameters:

1. **Restate the dump in precise terms.** If the restatement changes meaning, confirm with the user.
2. **Detect audience** — LLM / exec / peer / self / public. Drives the compression target.
3. **Assess stakes** — low / medium / high. Drives mode selection.
4. **Select mode** — `quick`, `standard`, or `deep` (see Modes section).
5. **Classify question type** preliminarily — well-defined / ill-defined / wicked / mess / adaptive. The `problem-typology` sub-skill (Phase 2) will refine this.

If the user doesn't specify mode, default to `standard`. Upgrade to `deep` if Phase 6 audit reveals deep contestation.

### Phase 2 — Diagnose

Route to the diagnosis subdomain:

- `problem-typology` — refine the typology classification (well-defined / ill-defined / wicked / mess / adaptive). Drives which decomposition method applies in Phase 3.
- `audience-classifier` — confirm or revise the audience tag from intake.
- `stakes-assessor` — confirm mode selection given the typology.

Output: a typology + audience + stakes profile.

### Phase 3 — Decompose

Route to the decomposition subdomain:

1. **Call `claim-decomposer` (cross-domain — research)** to break the statement into atomic claims with type tags, dependency graph, and priority tiers.
2. **Apply `root-vs-symptom-tagger`** to select among 5 Whys / Fishbone / dependency mapping / Current Reality Tree based on typology, and tag each atomic claim as root vs symptom.
3. **Call `assumption-excavator` (cross-domain — philosophy/logic)** with `depth=surface` to surface hidden premises in the Definitional, Causal, Value, Scope, and Framing categories.

If decomposition produces 15+ atomic claims, ask the user to prioritize before continuing.

### Phase 4 — Reframe

Rotate frames to expose that the formulation is not unique:

- `frame-rotator` — produce 2–3 alternative formulations using IDEO's HMW formula (`How might we [verb] for [user] so that [outcome]`); also performs Polya's specialize/generalize operations and calls `assumption-excavator` for framing-assumptions analysis.
- `inversion-tool` — Munger inversion: "what would guarantee failure?" Distinct from steel-manning the opposing view.
- `stakeholder-rotator` — calls `values-excavator` (cross-domain — philosophy/ethics) to surface whose interests are centered and whose are invisible.

For stuck or contested cases:
- Call `socratic-examiner` (cross-domain — philosophy/dialectical-tools) for systematic Socratic questioning.
- Call `steel-man-forge` to construct the strongest opposing formulation.
- Call `dialectic-engine` for multi-round point-counterpoint when the reframe itself is contested.

### Phase 5 — Compress

Route to the compression subdomain by audience:

| Audience tag | Skill |
|---|---|
| exec | `bluf-shaper` (military / executive bottom-line-up-front) or `executive-distiller` (full Minto Pyramid) |
| peer | `scqa-formatter` (Situation, Complication, Question, Answer) |
| LLM | `cursed-speech` (Anthropic-canonical structural order: role → context → longform-data → examples → numbered instructions → output format → self-check) |
| self | `scqa-formatter` with self-framing, or Polya Step 1 restatement |
| public | `executive-distiller` with audience-aware register |

`cursed-speech` also recommends downstream Archon skills for the formulated prompt to invoke (hybrid: static map + runtime `mcp__skill-library__search_skills` query).

For document-shape outputs, call `argument-structure` (cross-domain — writing/rhetoric) for Toulmin / Rogerian / classical scaffolding. Optionally call `clarity-engine` (cross-domain — neocortex) as a post-compression accessibility check.

### Phase 6 — Audit

Run the audit subdomain in this order:

1. `xy-detector` — flag attempted-solution-as-problem patterns. Returns the inferred underlying goal if an XY pattern is detected.
2. `answerability-tester` — could any evidence resolve this? Calls `evidence-evaluator` (cross-domain — philosophy/epistemology) for the evidence-quality test.
3. `falsifiability-checker` — Popperian falsifiability test; thin coordinator over `demarcation-judge` (cross-domain — philosophy/philosophy-of-science).
4. `scope-bounder` — thin coordinator over `assumption-excavator` with category=scope, surfacing time, population, and context boundaries.
5. `statement-grader` — six-axis score: specificity, falsifiability, scope, audience-fit, answerability, root-vs-symptom. Threshold: any axis below 3/5 triggers the re-state loop.

Optionally call `argument-analyst` (cross-domain — philosophy/logic) on the candidate statement for validity, soundness, and fallacy detection.

### Phase 7 — Re-state (loop)

If `statement-grader` returns sub-threshold on any axis, return to Phase 4 with the failure diagnosis as input. Apply the Re-state Loop (next section). Cap at 3 iterations total.

## Modes

| Mode | Phases run | Wall-clock target | When to use |
|---|---|---|---|
| `quick` | 1 → 5 (compression) → 6 (statement-grader only) | ≤30s | Low-stakes statements; routine work; the architectural answer to Reiter-Palmon's automaticity finding. Skip diagnosis, decomposition, reframing, full audit. |
| `standard` | 1 → 7, single pass | 2–5 min | Genuine inquiry; default for unspecified requests. |
| `deep` | 1 → 7 with frame rotation ≥3 alternatives, full adversarial XY check, audience pass for two audiences (typically LLM + exec) | 5–15 min | High stakes; wicked or mess typology; deeply contested formulations. |

If early Phase 6 audit reveals deep contestation or multi-axis grader failure, upgrade `quick` → `standard` or `standard` → `deep` automatically and announce the upgrade.

## Re-state Loop (Reentry Protocol)

Mirrors `spelunker`'s Reentry Protocol Levels 1–4, adapted from evidence-verification to problem-statement quality:

| Level | Action | Trigger |
|---|---|---|
| **L1 — Rephrase and retry** | Reformulate using different terminology or restated subject; re-run statement-grader | Cosmetic axes failing (specificity, scope) on first iteration |
| **L2 — Decompose further** | Call `claim-decomposer` to split the statement into sub-statements; re-state each independently | Compound failure; root-vs-symptom axis fails |
| **L3 — Depth upgrade** | Move `quick` → `standard` → `deep`; rerun with deeper frame rotation | Multiple axes fail across iterations; deep contestation |
| **L4 — User assist** | Ask the user what specifically isn't landing | Three iterations through L1–L3 failed |

After 3 total iterations or Level 4, present:
1. The latest statement
2. The convergence trajectory (each iteration's grader scores)
3. The remaining failure axis and a candidate explanation

Never loop silently past 3 iterations.

## Cross-Domain Routing Table (first-class)

These calls are explicit, not implicit. The orchestrator uses them at the phases listed:

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

When invoking a cross-domain skill, pass: the current statement, the typology + audience + stakes profile from Phase 2, and the specific question scoped to that skill's domain.

## Failure Recovery

| Failure | Response |
|---|---|
| Statement is too vague to even restate | Ask the user for one clarifying example or one specific consequence; do not proceed without it |
| Decomposition produces 15+ atomic claims | Ask the user to prioritize; investigate top claims at full depth, remainder at quick |
| Audience tag conflicts (e.g., simultaneously exec and LLM) | Run compression twice (deep mode default for two audiences); present both shapes |
| `statement-grader` fails on `audience-fit` after 3 iterations | Default to L4 user assist; the audience model may be wrong |
| Cross-domain skill returns an error or is unavailable | Continue with available phases; mark the missing analysis as a gap in the final output, do not fabricate |
| Loop reaches iteration cap with no convergence | Present the trajectory and the latest statement; flag the remaining failure axis explicitly |

## Scope Boundaries

**Six Eyes handles:** turning fuzzy intent into a clear, audience-fit, audited problem statement. It produces statements; it does not produce solutions.

**Six Eyes does NOT:**
- Solve the problem (that's the downstream skill or human's job)
- Choose the audience for the user (audience must be inferable from intake or specified)
- Run silently past 3 loop iterations
- Replace domain expertise (a clinical reframer or investing reframer may be needed for domain-specific framing; v2 leaves hooks for these)
- Auto-invoke (explicit invocation only — Reiter-Palmon mitigation)
- Guarantee that the resulting statement is right (it guarantees the statement is well-formed, audited, and audience-fit; correctness of the underlying claim is downstream)

## Connections

- Mirrors `spelunker` (research) structurally — Phase-1 intake, depth modes, Reentry Protocol Levels 1–4
- Cross-domain caller of `philosophy-orchestrator` subdomain skills (logic, dialectical-tools, ethics, epistemology, philosophy-of-science)
- Calls `claim-decomposer` (research) and `argument-structure` (writing/rhetoric)
- Build plan: `skill-lab/binding-vow-build-plan-v2.md` (vault)
- Research foundations: `skill-lab/binding-vow-research-findings.md` (vault)
