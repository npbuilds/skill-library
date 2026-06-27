# Build-Order DAG + World-State Schema

The world is built in **dependency order** — you cannot name a culture before defining it, or write its secrets before its factions exist. Each stage reads the committed state, generates via `worldbuilding-orchestrator`, passes Critic-1 (hard gate), and commits. In **brownfield** mode the DAG is already satisfied; you walk it only to fill gaps the back-edge surfaces.

## The dependency DAG

| # | Stage | Produces | Primary skill | Critic-1 focus | Fork? |
|---|---|---|---|---|---|
| 1 | **Axioms** | the foundational rules (the "spine") | `world-bible` | Rule-of-Consequence: does each axiom propagate? | — |
| 2 | **Central system** (magic/tech) | source · cost · limits · access | `magic-system-design` | Sanderson's Laws; bright-line constraints | **★ fork** |
| 3 | **Physical world** | geography · climate · ecology | `geography-ecology`, `ecology-design` | follows from axioms; no free lunch | — |
| 4 | **Civilizations** | cultures + naming/phonetics | `cultures-societies`, `naming-system` | seven pillars; consistent with system+geo | — |
| 5 | **Belief** | religion, cosmology | `religion-design` | consistent with cosmology + cultures | — |
| 6 | **Dynamics** | the faction-conflict web | `faction-design` + world-bible | each faction: goal · lever · vulnerability; no unmotivated stability | **★ fork** (central conflict) |
| 7 | **Tech** | the tech tree / disruption | `technology-progression` | follows from the central system | — |
| 8 | **History** | the timeline | `history-builder` | causally consistent; explains the present | — |
| 9 | **Revelation layers** | L0–L3, who-knows-what | revelation layers + `character-belief-tracker` | no information leak across layers | — |
| 10 | **Depth pass** | cascaded consequences | `extrapolation-engine` | "And Then What?" — second-order coverage | — |
| 11 | **Characters** | the cast (Diamond + world-shapes-person) | `character-design` | each rooted in the world; seeds the story | **★ fork** (protagonist) |

**The four forks** (human checkpoints, principle 1): tone/medium (set at entry), the **central system** (#2), the **central conflict** (#6), the **protagonist** (#11). Gate hardest at #1–#2 and #6 — early errors cascade.

## World-state schema (the blackboard)

A markdown world-bible every agent reads and writes. Minimal layout (maps to the `worldbuilding` domain's `World-Bible/` convention):

```
world-state/
  axioms.md            # the non-negotiable rules (the spine)
  belief-graph.md      # who-believes / knows-what; the revelation layers (L0–L3)
  timeline.md          # the master chronology
  faction-web.md       # nodes + edges + vulnerabilities + triggers
  systems/             # magic/tech, economy, ecology … one concept per file
  cultures/  factions/  locations/  characters/   # one entity per file
  _log/
    generation-log.md  # decisions, checkpoint verdicts, critic diagnoses
    stub-queue.md      # the back-edge: world-gaps the story surfaced, to build
```

Rules: **one concept per file**; **commit only after Critic-1 passes**; every commit appends to `generation-log.md`; the **stub-queue** is the back-edge's work list (a scene needs X that doesn't exist → enqueue X here → Phase A builds it before the scene re-drafts).

## Notes
- The build order is a *default*, not dogma — the literature treats build order as an experiment (top-down spine here; the story layer is where bottom-up emergence can be added later).
- Brownfield worlds (e.g. an existing vault) already satisfy #1–#11; Scheherazade reads them as the committed state and runs Phase B, using the DAG only to slot back-edge stubs into the right dependency position.
