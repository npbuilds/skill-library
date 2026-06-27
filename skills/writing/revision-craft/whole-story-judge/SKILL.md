---
name: whole-story-judge
description: >
  Judge whether a whole story works as a whole — not scene by scene. Checks the macro properties
  that only exist at the level of the complete draft: are the setups paid off, does the arc have a
  shape, do events connect causally, is the opening's promise kept, is it globally consistent? Use
  after the scene-level quality gate passes, on a complete draft or outline, when a story is "fine
  scene by scene but doesn't add up," or when the user asks "does the whole thing hold together?"
type: action
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# Whole-Story Judge — The Macro Gate

`quality-critic` judges the scene; this judges the **whole**. They are different questions: a story can pass every scene gate — each scene tense, turning, alive — and still be a pile of good scenes that doesn't cohere. The macro properties (a fired setup, a shaped arc, a kept promise) **only exist at the level of the complete draft**, so they need their own judge.

It instantiates the shared discipline in `_shared/critic-core` (evidence-anchor cap, floor gate, reason-first, steelman, guards, bounded authority) with a macro-narrative rubric. Read `_shared/critic-core` first — that machinery is inherited and not repeated here. This judge runs **above** the scene gate: scenes pass `quality-critic`, the whole passes this.

> **Why it's needed (research).** LLMs "generate compelling setups but fail to deliver promised resolutions" — the Chekhov's-gun gap (CFPG, arXiv 2601.07033). And macro-level structural evaluation (story grammar, discourse coherence) substantially outperforms local/lexical signal (arXiv 2604.27846). Local gates structurally cannot catch global failure; this closes that gap.

## How to Run

### Input

1. **The whole** — a complete draft, or a full outline/beat-sheet if the draft is too long to hold at once (judge the structure either way).
2. **Setups ledger** (optional) — a list of planted setups/foreshadows/promises if the author has one; otherwise the judge extracts them.
3. **Precondition** — the **scene-level gate should already pass.** Don't macro-judge prose that fails scene by scene; fix the scenes first.

### Process

Run the `_shared/critic-core` loop over the dimensions in `references/macro-rubric.md`. The macro adaptations:

- **Extract the setups ledger first.** Scan the whole for planted promises — a named gun, a withheld secret, a posed question, a stated stake, a foreshadow. This ledger is the evidence base for the Payoff dimension; every entry must be traced to a payoff, a deliberate subversion, or marked dropped.
- **Cite across distance.** Macro evidence is a *pair of locations* — setup here, payoff there (or its absence). Quote both ends. The evidence-anchor cap means: a Payoff PASS must cite the setup *and* its fulfilment; you cannot pass it on vibes.
- **Steelman before FAIL.** A setup deliberately left unfired, an arc that refuses catharsis, an ambiguous ending — these can be earned macro choices, not failures. Apply the mistake-vs-choice test: is the omission patterned and effect-bearing? (See the `subversion` note in the rubric.)
- **Aggregate by FLOOR GATE** over the required dimensions. **Emit a diagnosis** — name the dropped setup / the missing climax / the episodic seam, cite the locations, and state the structural fix (for `narrative-arc`, `narrative-geometry`, or `prose-editor`'s structural pass). Withhold the tally (private rubric).

### Output

```
WHOLE-STORY VERDICT: PASS | FAIL   (floor gate · level: draft)
Scene gate: PASS (precondition met)

Setups ledger: <N planted> → <paid> / <subverted> / <DROPPED>

| Dimension          | Verdict | Cited evidence (setup ↔ payoff / structure)             |
|--------------------|---------|---------------------------------------------------------|
| Payoff realization | FAIL    | setup: "the locked western door" (ch.2) → never reopened |
| Arc shape          | PASS    | complication (ch.3) → climax "she signed it" (ch.11)    |
| Causal connectivity| PASS    | each turn caused by the last, not merely sequential      |
| Global coherence   | PASS    | no character/plot/world contradiction across the whole   |
| Promise kept       | PASS    | opening promises a heist; ending delivers/subverts it    |

Verdict legend: advisory dims marked FAIL* (non-gating).

DIAGNOSIS (failed required dimensions only):
- <Dimension>: <the dropped setup / missing beat / seam>, at <locations>. Why it fails: <reason>.
  Fix: <fire it, cut it, or add the beat — sourced to narrative-arc / narrative-geometry>.
```

## Scope Boundaries

**Handles**: judging macro-narrative properties of a complete work — payoff, arc, causality, promise, global consistency — with cross-distance cited evidence and a structural diagnosis.

**Does NOT**:
- Judge scene-level craft (tension, interiority, voice) — that's `quality-critic`, which runs first.
- Check world-canon soundness — that's the worldbuilding-critic (a different domain).
- Rewrite — that's `prose-editor` (structural pass); this feeds it.
- Dictate the *kind* of arc or ending — tragic vs triumphant, resolved vs ambiguous are the author's calls (bounded authority). The judge asks "is it shaped, paid off, causal, coherent?", never "is it the ending I'd choose."

## Related Skills

- **Shared discipline**: `_shared/critic-core` — the judging machinery this instantiates.
- **Runs after**: `quality-critic` (scene gate) — the macro gate is the second, higher gate.
- **Rubric sources**: `narrative-arc`, `narrative-geometry` (arc/shape), `scene-craft` (turns aggregate to arc), `character-belief-tracker` (global consistency).
- **Consumes this**: `prose-editor` (structural pass acts on the diagnosis).
- **Sibling judges** (peers, not dependencies — see `_shared/critic-core`): `quality-critic` (prose), worldbuilding-critic (systems).
