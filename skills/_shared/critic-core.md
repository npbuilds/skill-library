# Critic-Core — the shared judging discipline

The reusable **discipline** every evaluation critic in the library imports. It is **not a skill and not a rubric** — it is the domain-agnostic *machinery* of a trustworthy LLM-as-judge. Each critic supplies its own **domain rubric**; they all share this loop and these guards.

> **Why share the machinery but not the rubric.** Research (GER-Eval, arXiv 2602.08672) tested a universal judge core and found there isn't one: a model is internally consistent applying its own rubric (70–90%) but human-alignment **collapses across domains** (ICC 0.7–0.8 → <0.2 on knowledge-intensive tasks). The transferable thing is the *application discipline*; the rubric must be domain-specific. So: one core, separate critics.

Used by: `quality-critic` (prose) · `worldbuilding-critic` (invented systems) · `whole-story-judge` (macro narrative). Add new critics by importing this file and defining a rubric.

---

## The core loop (domain-agnostic)

**0 — Precondition.** Run only after any upstream *hard* gate (consistency/canon) has passed. Don't polish something that's broken underneath. If the precondition is unknown, say so and stop.

**1 — Load the rubric.** Each dimension is **boolean**, names a **function** (the effect it protects), cites a **source**, and carries a **floor**: `required` (gates) · `advisory` (reported, doesn't gate) · `required-if-present` (conditional → N/A when its precondition is absent).

**2 — Score each dimension. Judge the _effect_, not the device.** The conventional device is *default evidence*, not the only path; a deliberate, unconventional means that achieves the function still passes. For each dimension:
- **a. Extract evidence** — quote the exact source text (verbatim).
- **b. Reason, then rule** — state what the evidence shows against the pass-test *before* the verdict (reason-first; arXiv 2509.13332).
- **c. Verdict** — boolean **PASS / FAIL**. No scales.
- **d. Evidence-anchor cap** *(the load-bearing guard)* — a dimension **cannot PASS without a cited verbatim line that grounds it**; no citation → auto-FAIL (Rulers, arXiv 2601.08654). This same test unmasks pretension: an earned move has a citable effect; an empty one doesn't.
- **e. Steelman before you FAIL** — before failing on a broken convention, write the strongest case it's *intentional, patterned, and achieves a nameable effect*. If that holds, it PASSes (a choice, not a deficiency). Mistake vs. choice.
- **f. N/A** — a dimension whose precondition doesn't apply is N/A, excluded from the gate; the cap doesn't fire on it.

**3 — Aggregate by FLOOR GATE.** Pass iff **every _required_ dimension passes its floor**. One required FAIL fails the gate. **Never average** — averaging lets a dead artifact buy its way through on a strong-but-irrelevant dimension. Advisory dims report but don't gate; N/A dims are excluded.

**4 — Iterate, capped (~3).** Hand the diagnosis back, take the revision, re-judge. If verdicts keep "improving" but the artifact isn't, suspect reward hacking, not progress.

**5 — Emit the diagnosis, not the score.** Pass back the failed dimensions, the offending lines, and the fix — **withhold the rubric weights, floors, and tally** from the generator. You can't optimize against a target you can't see (the cheapest anti-gaming guard).

---

## The guards (the anti-reward-hacking discipline)

A critic is a *proxy* for "good"; keeping the proxy honest is the whole job.

- **Evidence-anchoring + cap** — the one guard with direct empirical support. No ungrounded passes.
- **Floor gate** — no gameable average.
- **Private rubric** — diagnosis out, scores withheld.
- **Critic ≠ generator** — run under a different model family/persona to blunt self-preference (arXiv 2411.15594).
- **Blind superficial cues** — discount length/formatting; judge substance (style-over-substance is the documented bias: arXiv 2409.15268, 2510.02025).
- **Drift alarm** — if verdicts keep passing but a human disagrees at a checkpoint, the judge is being gamed: freeze and recalibrate against the human (the ground-truth signal).
- **Onset monitoring** — reward hacking has a signature (scores rise while substance stalls); favor pass-tests that can't be satisfied without doing the real work.
- **Bounded authority** — the critic flags tensions and *hands aesthetic / bold-vs-safe / direction calls back to the human*. Enforcing convention is a failure mode, not a feature.

---

## Build the validity harness alongside the critic (non-negotiable)

A judge you can't measure is **reliable-but-invalid** — it agrees with itself while tracking the wrong thing. Every critic ships an `eval/` harness:
- **Adversarial control pairs** with neutral `fail_passage` (should FAIL) / `pass_passage` (should PASS) slots, tagged by `kind` (one kind per failure direction the critic must resist).
- **A scorer** reporting the two error rates — **false-pass** (too lenient / fooled) and **false-fail** (too harsh / e.g. conformity) — broken down by kind, with named headline metrics.
- **A protocol**: run the critic blind on each passage, record verdicts, score; missing/malformed verdicts force a FAIL (an incomplete run never passes).
- **Drift calibration**: when a human disagrees in real use, add that case as a new control pair (the human verdict is gold). The set grows toward the human signal.

---

## How to instantiate a new critic

1. **Define the rubric** — dimensions as *functions* (effect protected), each with a boolean pass-test, a source skill, and a floor. Make profiles swappable if the medium/domain varies; note any **inversions** (a virtue here that's a defect there).
2. **Import this core** — the loop (§core loop) and the guards (§guards) are inherited verbatim; don't re-litigate them.
3. **Build the harness** — control pairs for *each* failure direction the critic must resist (at minimum: fooled-by-surface and crushes-the-good).
4. **Register trinity-clean** — `type: action`, wire into the parent director's `referenced_by`, run sync → wire → recalibrate, confirm zero new drift.

## Research basis (one line each)

- Evidence-anchoring + mechanical cap is the only empirically-supported anti-reward-hacking guard — Rulers, 2601.08654.
- No universal judge core; decouple rubric design from application — GER-Eval, 2602.08672.
- Boolean/checklist rubrics lower judge variance — 2602.05125 and the rubric-generation line.
- Reason-before-verdict improves accuracy/robustness — 2509.13332.
- Style-over-substance bias is real and capability-independent — 2409.15268, 2510.02025.
