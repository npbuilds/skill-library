---
name: scheherazade
description: >
  Meta-orchestrator for the agentic world→character→story loop. Generates (or extends) a fictional
  world, its characters, and a story set in it by driving the worldbuilding and writing domains over
  one shared world-state, closed by the critic suite (consistency + quality + macro) with human
  checkpoints at the creative forks. Use to generate a world and a story end-to-end, or to draft
  quality-gated prose grounded in an existing world-bible. Not for single-skill asks (just worldbuild
  or just draft) — those route to the domain orchestrators.
type: orchestrator
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Scheherazade — the narrative meta-orchestrator

Sits **above** `worldbuilding-orchestrator` and `prose-orchestrator` and consumes them. It does not generate prose or worlds itself — it **drives the loop**: build or extend a world on a shared blackboard, hand off to draft a story in it, gate every step through the critic suite, and surface world-gaps back into the build. Medium-agnostic (novel · genre · RPG · screenplay).

The loop exists because of two research-backed facts: a single editable **shared state** is the consensus fix for narrative drift, and **evaluation** (not generation) is the binding constraint. So the orchestrator's whole job is to *manage the state and run the gates*. A generator cannot self-correct without an external signal; the critics are that signal — load-bearing, not optional.

## Guiding principles

1. **Checkpointed autonomy.** Autonomous within a stage; the human decides at the four creative forks — tone/medium · the central system (magic/tech) · the central conflict · the protagonist. The human is the ground-truth signal that keeps the critics calibrated (the drift alarm), not decoration.
2. **Gate hardest at the foundation.** An early world-build error cascades downstream (~100% infection in multi-stage pipelines), so the earliest DAG stages get the strongest consistency gate *and* a mandatory checkpoint.
3. **Hard gates reject; soft gates revise.** Consistency (Critic-1) is a **hard** gate — it rejects, never flags (detection-without-blocking ≈ 3% effective). Quality (Critic-2) is a **soft** gate — diagnose → revise, capped at ~3.
4. **The world grows only as deep as the story needs.** The back-edge (`world-to-story`'s iceberg test) turns a scene's unmet need into a queued build task, not a failure.
5. **Markdown state now; retrieval at scale.** The shared world-bible is markdown at scene/chapter scale; switch to retrieval before novel length (drift is linear in length).

## Activation

### Entry contract
- `seed` — premise/genre/logline (greenfield) **or** a pointer to an existing world (brownfield).
- `mode` — **greenfield** (build the world from the seed) | **brownfield** (consume an existing world-bible and run/extend the story; the back-edge re-enters the build only for gaps).
- `world_state` — the shared blackboard: a markdown world-bible (new, or an existing vault). Schema in `references/build-order-dag.md`.
- `medium` — selects the `quality-critic` profile (literary · genre · rpg · childrens · experimental).
- `caps` — revision cap (default 3) · cost ceiling.

### Triggers
Invoke for the **closed loop**: "generate a world and a story", "write a story in <world>", "run the narrative loop", `/scheherazade`. **Not** for single-skill asks (just worldbuild / just draft) — route those straight to the domain orchestrator.

## The loop (drive this; detail in `references/`)

**Phase A — world build** (greenfield, or brownfield gaps only). Walk the dependency DAG (`references/build-order-dag.md`). Per stage: generate via `worldbuilding-orchestrator` → **Critic-1** (`worldbuilding-critic` + consistency audit) **hard gate** → revise-or-commit to the world-state. Checkpoint at the forks.

**Phase B — story loop.** brief → `world-to-story` bridge → draft scene via `prose-orchestrator` → **Critic-1** (consistency: `character-belief-tracker` + world-bible audit) **hard gate** → **Critic-2** (`quality-critic`, scene gate) **soft gate** (≤3) → checkpoint. At each chapter / whole-draft boundary → **`whole-story-judge`** (macro gate).

**Back-edge.** When the iceberg test surfaces a world the scene needs but the state lacks → enqueue a "stub to build" → re-enter Phase A for that stub only.

**Stop** when the gates pass, the caps are hit, and the human signs off. Gate order, cost tiers, and stopping rules: `references/loop-protocol.md`.

## Delegation protocol

- **To `worldbuilding-orchestrator`:** the current stage, the world-state so far, the relevant axioms/constraints. It routes to the right knowledge/action skill.
- **To `prose-orchestrator`:** the editorial brief, the Voice Card, and only the scene's world-context that a character needs *now* (the iceberg test).
- **To each critic:** the artifact + the upstream-gate status. Critics return a **diagnosis, not a score** (the rubric stays private from the generator), and run under a **different persona** than the generator (to blunt self-preference). Critic order: consistency (hard) → quality (soft, scene) → macro (chapter/draft).

## Synthesis (output)

Three artifacts evolve together: the **world-state** (the world-bible), the **prose** (gated scenes/chapters), and a **generation log** (decisions, checkpoints, the stub queue). On a passing draft, the macro gate's verdict plus the human sign-off close the loop.

## Scope boundaries

**Handles:** driving the closed world→story loop end-to-end, or quality-gated drafting in an existing world.
**Does NOT:** generate prose or worlds itself (it delegates); judge craft or canon (the critics do); replace the domain orchestrators for single-skill work.

## Related skills

- **Below it (consumed):** `worldbuilding-orchestrator` · `prose-orchestrator`.
- **The gates (critic suite, sharing `_shared/critic-core`):** `worldbuilding-critic` · `quality-critic` · `whole-story-judge`.
- **Bridge & state:** `world-to-story` · `character-belief-tracker` · `extrapolation-engine`.
