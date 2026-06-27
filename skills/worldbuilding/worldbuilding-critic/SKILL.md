---
name: worldbuilding-critic
description: >
  Judge whether an invented system — a magic system, an economy, a society, a technology — is
  actually SOUND, not merely internally consistent. Use after the consistency audit passes, when
  a world-bible needs a quality verdict, when designing or stress-testing a fantasy/SF system, or
  when the user asks "does this magic system / faction structure hold up?" Emits a diagnosis of
  the offending axioms and un-propagated consequences, never a score.
type: action
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# Worldbuilding Critic — The System Judge

The worldbuilding domain has **generators** (`magic-system-design`, `faction-design`, `extrapolation-engine`) and a **canon** (`world-bible`), but no **judge**. This is it: *is the invented system sound?* It instantiates the shared discipline in `_shared/critic-core` (evidence-anchor cap, floor gate, reason-first, steelman, guards, bounded authority) with a worldbuilding-specific rubric. Read `_shared/critic-core` first — that machinery is inherited and not repeated here.

It answers a different question than consistency. *"Does this contradict the axioms?"* is the **consistency** gate (Layer 1). *"Is the system itself good — costed, limited, generative, plausible?"* is the **soundness** judge (Layer 2). A perfectly consistent world can still be decorative, un-costed, or one inference from a god-power.

## How to Run

### Input

1. **The system(s)** — the world-bible notes for a magic system / economy / society / technology (inline, paths, or a whole `World-Bible/` + `Concepts/` set).
2. **Scope** — `system` (one system) or `world` (the axiom set + how systems interlock). Default: `system`.
3. **Precondition** — the **consistency audit (Layer 1) must pass first.** Don't judge the soundness of a self-contradicting world.

### Process

**Layer 1 — Consistency audit (the hard gate; automatable).** Before soundness, check the system doesn't contradict itself or the axioms. Extract entities, relations, and rules; look for **logical, temporal, and causal** contradictions across the notes (the corpus-inconsistency method: entity/relation + NLI + retrieval). Cite the conflicting passages. Any contradiction → FAIL Layer 1, stop, return the conflict. (This is the world's `character-belief-tracker` / `world-bible` consistency-audit analog.)

**Layer 2 — Soundness rubric (the judge).** Run the `_shared/critic-core` loop over the dimensions in `references/soundness-rubric.md`. Judge the **function**, cite the **axiom or consequence**, and apply the **steelman** before any FAIL (a deliberate genre choice — e.g. a soft, numinous magic à la Tolkien — is not a deficiency if it's owned and the story doesn't lean on it to resolve conflict). Run `references/stress-tests.md` — the "And Then What?" second-order detectors that catch the failures a *forward-built* world misses.

**Aggregate** by FLOOR GATE over the *required* dimensions (see the rubric). **Emit a diagnosis**, not a score: name the offending axiom / un-propagated consequence / un-costed power, quote it, and state the fix — for the world-builder or `extrapolation-engine` to act on. Withhold the tally (private rubric).

### Output

```
SOUNDNESS VERDICT: PASS | FAIL   (floor gate · scope: <system|world>)
Consistency audit (Layer 1): PASS (precondition met)

| Dimension          | Verdict | Cited evidence (axiom / consequence)                    |
|--------------------|---------|---------------------------------------------------------|
| Cost is real       | PASS    | "every working consumes bloomglass... casting spends money" |
| Limits > powers    | PASS    | "acts only on living information... cannot raise the dead"  |
| Propagation        | PASS    | fuel=money → bankruptcy = visible decay (Axiom 1)       |
| Enforcement physics| FAIL    | "license... quasi-magically enforced" — mechanism unstated |
| ...                | ...     | ...                                                     |

Verdict legend: advisory dims marked FAIL* (non-gating); N/A = not applicable to this system type.

DIAGNOSIS (failed required dimensions only):
- <Dimension>: <offending axiom/gap>. Why it fails: <reason>. Fix: <propagate / cost / bound / stress-test, sourced to a generator skill>.
```

## Scope Boundaries

**Handles**: judging the soundness of invented systems — cost, limits, access, propagation, plausibility, and the second-order stress-tests; with cited evidence and a diagnosis.

**Does NOT**:
- Generate systems — that's `magic-system-design`, `faction-design`, `economic-systems`, `technology-progression` (this judges their output; the diagnosis feeds back to them).
- Check prose quality — that's the quality-critic (a different domain).
- Adjudicate *taste* — soft vs hard magic, grim vs bright tone are the author's calls (bounded authority); the critic asks only "is it costed, limited, propagated, plausible?", never "is it the kind of world I'd build?"
- Decide canon — the `world-bible` is the authority; this flags soundness gaps for the human to rule on.

## Related Skills

- **Shared discipline**: `_shared/critic-core` — the judging machinery this instantiates.
- **Generators it judges** (diagnosis feeds back): `magic-system-design`, `faction-design`, `cultures-societies`, `economic-systems`, `technology-progression`.
- **Composes for evaluation**: `extrapolation-engine` (the "And Then What?" engine — Layer 2's propagation + stress-tests).
- **Sibling judges** (peers, not dependencies — see `_shared/critic-core`): quality-critic (prose), whole-story-judge (macro narrative).
- **Canon it checks against**: `world-bible`.
