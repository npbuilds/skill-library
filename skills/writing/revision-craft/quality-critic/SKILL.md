---
name: quality-critic
description: >
  Judge whether a piece of prose is actually good — not whether it is consistent, and not by
  describing its features, but by ruling PASS/FAIL on a boolean craft rubric with a floor gate.
  Use after the consistency gate passes, when prose needs an objective quality verdict before
  revision, when running a generate→critique→refine loop, or when the user asks "is this scene
  working?" Emits a diagnosis for prose-editor, never a score for the writer to chase.
type: action
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# Quality Critic — The Judge

The library has a **describer** (`style-analyzer`: "what is this prose doing?") and a **fixer** (`prose-editor`: "make it work"). This is the missing **judge**: *does it work?* It rules a boolean verdict on craft, cites the evidence for every ruling, and hands a diagnosis to the editor.

It exists to survive one specific failure mode. LLM judges reward **style over substance** — they prefer surface polish to genuine craft, rate verbose-but-hollow prose above lean-but-alive prose, and are demonstrably gameable by form. A naïve "rate this 1–10 and loop until high" critic *will* be reward-hacked into competent, lifeless prose. Every design choice below is a guard against that.

## How to Run

### Input

1. **Target text** — a scene (tight loop) or a full draft (structural loop).
2. **Level** — `scene` (the 7 textural dimensions) or `draft` (adds arc/structure). Default: `scene`.
3. **Medium profile** — selects the rubric and per-dimension floors. Default: `literary-fiction`. Others: `genre`, `rpg-playability`, `childrens`, `experimental` (form-breaking work). See `references/rubric-profiles.md`.
4. **Baseline** (optional) — the prior draft (N−1) or a reference passage, used **only** for the regression check (Step 5), never for the absolute verdict.
5. **Precondition** — the **consistency gate must already pass**. Quality runs *after* consistency; never polish inconsistent prose. If consistency status is unknown, say so and stop.

### Process

**0 — Normalize superficial cues.** Before reading for craft, consciously discount length and formatting. A longer or more elaborately formatted passage is not a better one. Judge the substance dimensions only.

**1 — Load the profile.** Read the dimension list, the boolean pass-test, and the floor for the chosen medium from `references/rubric-profiles.md`. Load `references/anti-pattern-detectors.md` — the operationalized `micro-tension` failure-table you will scan for.

**2 — Score each dimension, in order. Judge the _effect_, not the device.** Every pass-test names a *function* the prose must achieve (e.g. micro-tension's function is "the page is alive"); the conventional device (an unresolved contradiction) is the **default evidence**, not the only path. A deliberately flat, hypnotic scene that achieves the function by other means still passes. You are judging whether the prose is **alive and earned**, never whether it is conventional. For every dimension:
   - **a. Extract evidence.** Quote the *exact* sentence(s) in the text that bear on this dimension. Verbatim, with no paraphrase.
   - **b. Reason, then rule.** State what the cited evidence shows against the pass-test — *before* you give a verdict. Reason-first, verdict-second.
   - **c. Verdict** — boolean **PASS / FAIL**. No 1–10. No "mostly."
   - **d. Evidence-anchor cap (the load-bearing rule).** A dimension **cannot PASS without a cited verbatim sentence that grounds the pass.** If you cannot quote the line that earns it, the dimension **auto-FAILS** — regardless of how good the prose "feels." Ungrounded passes are exactly how style beats substance; this rule forbids them. *This same rule unmasks pretension:* an earned transgression has an effect you can cite; pretentious prose doesn't.
   - **e. Steelman before you FAIL (mistake vs. choice).** Before failing any dimension on an anti-pattern or a broken convention, write the **strongest case that the deviation is intentional, patterned, and load-bearing** — that it achieves an effect the conventional move couldn't. A rule-break **passes** if (i) it is consistent across the passage (not a one-off slip) and (ii) you can **name the effect** it buys. Only if that case collapses does it FAIL. A deficiency is unearned; a transgression is earned. Do not mistake one for the other.
   - **f. N/A when the precondition is absent.** A dimension whose precondition does not apply to this passage — e.g. Dialogue subtext on a passage with **no dialogue** — is scored **N/A**, not FAIL. N/A dimensions are excluded from the gate (Step 3); the evidence-anchor cap does not fire on them. Never penalize a narration-only scene for lacking dialogue.

**3 — Aggregate by FLOOR GATE.** The text passes the quality gate **iff every _required_ dimension passes its floor.** One required FAIL fails the gate. Dimensions the active profile marks **advisory** are scored and reported but do **not** gate; **N/A** dimensions (Step 2f) are excluded entirely. **Never average** the required dimensions — averaging lets a dead scene buy its way through on purple prose, the precise trade this critic exists to forbid. (Floors and the required/advisory split are per-profile; see `references/rubric-profiles.md`.)

**4 — Iterate, capped.** If the gate fails, hand the diagnosis to `prose-editor`, take the revision back, re-judge. **Cap at ~3 cycles.** If verdicts keep "improving" but the prose isn't, suspect reward hacking (Step 6) rather than progress.

**5 — Regression check (optional, comparative).** If a baseline is supplied, ask one narrow question: *on the dimensions that failed last round, is draft N better than draft N−1?* Anchor to the fixed baseline and **swap reading order** to cancel positional bias. This confirms a revision improved — it **never** sets the absolute verdict (Step 3 owns that).

**6 — Emit the diagnosis (not the score).** Output per Output below. Pass back **the diagnosis only** — the failed dimensions, the offending lines, the craft fix. **Withhold the rubric weights, floors, and pass/fail tally from the generator.** You cannot optimize against a target you cannot see; a private rubric is the cheapest anti-gaming guard.

### Output

A **Critic Report**:

```
QUALITY VERDICT: PASS | FAIL   (floor gate · profile: <medium> · level: <scene|draft>)
Consistency gate: PASS (precondition met)

| Dimension        | Verdict | Cited evidence (verbatim)            |
|------------------|---------|--------------------------------------|
| Micro-tension    | FAIL    | "Her heart pounded as she ran."      |
| Scene turns      | PASS    | "...and so she finally said no."     |
| Dialogue subtext | N/A     | (narration-only — excluded from gate)|
| ...              | ...     | ...                                  |

Verdict legend: PASS / FAIL gate; tag advisory dimensions FAIL* (non-gating); N/A = precondition absent, excluded.

DIAGNOSIS (for prose-editor — failed _required_ dimensions only):
- <Dimension>: <offending line>. Why it fails: <reason>. Fix: <craft move, sourced to the skill>.

REGRESSION (if baseline supplied): draft N vs N−1 on failed dims — improved / not improved.
```

## Anti-Gaming Guards

The critic is a proxy for "good." Keeping the proxy honest is the whole job.

- **Evidence-anchoring + cap** (Step 2d) — the one guard with direct empirical support. No ungrounded passes.
- **Floor gate** (Step 3) — no gameable average.
- **Private rubric** (Step 6) — diagnosis out, scores withheld.
- **Critic ≠ generator.** Run the critic under a different model family or persona than the writer, to blunt self-preference (a judge favors its own family's prose).
- **Blind superficial cues** (Step 0) — normalize length and formatting; judge substance.
- **Drift alarm.** If critic verdicts keep passing but a human disagrees at a checkpoint, the judge is being gamed. Freeze the loop and recalibrate the rubric against the human verdict — the human is the ground-truth signal, not decoration.
- **Onset monitoring.** Reward hacking has a signature: scores rising while substance stalls, and a drift toward the cheapest-to-fake dimension. Watch for it; favor pass-tests that can't be satisfied without doing the real craft work.

## Validity Harness

This critic is validated, not assumed. `eval/validity-set.yaml` holds adversarial pairs of three kinds — **style-trap** (hollow-polished should FAIL vs plain-substantive should PASS), **transgression-trap** (pretentious-unearned should FAIL vs rule-breaking-but-brilliant should PASS), and **originality-trap** (competent-generic should FAIL vs fresh-surprising should PASS). `eval/score-validity.py` reports two failure rates: **style-bias susceptibility** (passed something hollow) and **conformity rate** (failed an earned transgression — the critic crushing creativity). A judge that agrees with itself but flunks this set is *reliable but not valid* — run it before trusting the critic in a loop. See `eval/README.md`.

## Scope Boundaries

**This skill handles**: ruling a boolean quality verdict on prose against a craft rubric, with cited evidence and a diagnosis for revision.

**This skill does NOT**:
- Describe style without judging — that's `style-analyzer`.
- Edit or rewrite — that's `prose-editor` (it consumes this diagnosis).
- Check consistency/canon — that's the consistency gate (`character-belief-tracker`, world-bible audit); it runs *before* this.
- Emit a numeric score to the writer — by design. The verdict is boolean; the handoff is a diagnosis.
- Adjudicate **bold-vs-safe aesthetic direction** — that is the writer's call at the creative forks, not the critic's. The critic asks only "is it alive and earned?", never "is it the kind of thing I'd expect?" Enforcing convention is a failure mode, not a feature.

## Related Skills

- **Rubric sources** (one per dimension): `micro-tension`, `scene-craft`, `character-interiority`, `dialogue`, `concrete-detail`, `narrative-arc` / `narrative-geometry`, `style-analyzer`.
- **Consumes this**: `prose-editor` (turns the diagnosis into edits).
- **Sibling**: `style-analyzer` (describes; explicitly refuses to judge — this fills that gap).
- **Upstream**: the consistency gate runs first; this is the second, softer gate.
- **Shared discipline**: `_shared/critic-core` — the judging machinery (evidence-anchor cap, floor gate, steelman, guards) this skill instantiates; the rubric above is its prose-specific profile.
