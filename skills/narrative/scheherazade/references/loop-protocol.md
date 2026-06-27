# Loop Protocol — gates, cost tiers, checkpoints, stopping

The operational rules the orchestrator runs by. Premortem-derived: cost concentrates in the per-scene critic, error cascades from the foundation, and the macro level needs its own gate because local gates structurally cannot catch global failure.

## Gate order (never reorder)

Per artifact, gates fire in this order — a later gate runs only if the earlier one passed:

1. **Critic-1 · consistency (HARD).** Does it contradict the committed state? Composed of `worldbuilding-critic` (system soundness, world-build stages) and the consistency audit (`character-belief-tracker` + world-bible audit + `extrapolation-engine`, every scene). **Rejects, never flags** — a failed consistency gate forces a redo before anything else runs. *Never polish inconsistent prose.*
2. **Critic-2 · quality (SOFT).** `quality-critic` on each scene. Diagnose → hand to `prose-editor` → re-draft → re-judge, **capped at ~3** cycles. A soft gate: it loops, it doesn't hard-block.
3. **Macro gate.** `whole-story-judge` at each **chapter** and **whole-draft** boundary — payoff realization, arc shape, causal connectivity, promise kept, global coherence. Runs *above* the scene gate (scenes pass Critic-2; the whole passes this).

## Cost tiers (the expensive pass is rare)

The per-scene critic is the cost driver, so spend is tiered:

| Tier | Runs | Critic depth |
|---|---|---|
| **Scene** | every scene | single-pass `quality-critic` (cheap); generation on a cheaper model |
| **Chapter** | chapter boundary | `whole-story-judge` + (optional) a multi-persona / independent-validation quality pass |
| **Draft** | whole draft | `whole-story-judge` (full) + human sign-off |

Caps: revisions ≤ 3 per gate; respect the `caps.cost_ceiling`. If verdicts keep "improving" but the prose isn't, suspect **reward hacking** — freeze, don't keep iterating.

## Human checkpoints (the four forks + the drift alarm)

- **The forks** (mandatory yes/no): tone/medium (entry) · the central system (DAG #2) · the central conflict (DAG #6) · the protagonist (DAG #11). Autonomous *within* a stage; the human owns the fork.
- **Drift alarm** (the calibration loop): if critic verdicts keep passing but the human disagrees at a checkpoint, **the judge is being gamed.** Freeze the loop, recalibrate the offending critic against the human verdict (add the disagreement to that critic's `eval/` set as a new control pair — the human is gold). This is the only thing that keeps the proxy honest over a long run.
- **Bounded authority:** the critics flag tensions and hand *bold-vs-safe / aesthetic / direction* calls to the human. They ask "is it alive / sound / shaped?", never "is it the choice I'd make."

## Stopping rule

Caps are an **upper bound, not a requirement** — a scene/chapter that passes its gates early stops early. Two stop paths:
- **Success:** the gates pass at the current level (scene → chapter → draft) **and** the human signs off at the draft-level checkpoint. Done — do not burn remaining revision budget.
- **Escalation:** a gate keeps failing and the iteration/cost **cap is reached** → stop iterating and **escalate to the human** (don't ship sub-floor work silently, and don't loop past the cap).

A non-empty **stub-queue** (back-edge) means the world isn't yet deep enough for the story — drain it (Phase A) before declaring the draft done.

## Failure handling

- **Critic-1 fail (consistency):** reject; regenerate the stage/scene against the violated constraint. Do not proceed to quality.
- **Critic-2 fail (quality):** take the diagnosis, revise via `prose-editor`, re-judge; after the cap, escalate to the human (don't ship sub-floor prose silently).
- **Macro fail (whole-story):** the diagnosis names the dropped setup / missing climax / episodic seam + locations; route to `narrative-arc` / `narrative-geometry` / `prose-editor`'s structural pass — a structural fix, not a line edit.
- **Back-edge:** a scene needs world that doesn't exist → enqueue the stub, build it (Phase A) at its DAG position, then re-draft the scene.
