---
name: xy-detector
description: >
  Detect XY-pattern problem statements where someone asks about an attempted solution rather
  than the underlying goal. Use during binding-vow's Phase 6 audit, or directly when a
  question feels narrowly mechanical for the apparent stakes. Returns the inferred underlying
  goal Y if a pattern is detected, plus a reformulated statement, or 'no XY pattern' otherwise.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# XY Detector — The Underlying-Goal Surfacer

The XY problem (Raymond, *Jargon File*): someone asks how to do X (their attempted solution) instead of asking about Y (their actual goal). All XY problems are Type III errors waiting to happen — the right answer to X leaves Y unaddressed.

XY patterns are surprisingly hard to detect from inside; that's why a dedicated skill exists. The detector applies three diagnostic moves and returns either the inferred Y or a confident "no XY pattern."

## Detection Signals

The statement is more likely to be an XY pattern when one or more of these hold:

| Signal | Pattern | Strength |
|---|---|---|
| **Mechanism question** | "How do I [specific technical action]?" with no stated reason | Strong |
| **Disguised constraint** | "I want X but Y prevents it" — Y is presented as constraint, but Y might *be* the goal | Strong |
| **Solution-as-noun** | The X being asked about is a noun that names a specific tool/method/format | Medium |
| **Mismatch in stakes** | The mechanical specificity of X seems disproportionate to the framing's apparent stakes | Medium |
| **No "because"** | The statement has no causal grounding; the speaker hasn't surfaced *why* X matters | Medium |
| **Pattern-matches a known stack** | X fits a familiar engineering/business pattern; the speaker may have copied the pattern without checking the goal | Weak |

A statement with two or more signals is a likely XY pattern. A statement with a strong signal alone is also a likely XY pattern.

## Three-Question Diagnostic

For any candidate XY pattern, run these in order:

### Q1 — What changes if X is achieved exactly as stated?

If the answer is "the user gets X but their underlying situation isn't materially different," it's an XY pattern. The X is a means, not the end.

If the answer is "the user's underlying situation is improved in a way that matches the stakes," it's not XY. The X *is* the goal at this scale.

### Q2 — Why this specific X and not a sibling?

If the answer is "I just thought of this one" or "this is what others do," the X may be cargo-culted. The speaker has chosen a solution shape without checking whether it's the right shape.

If the answer is "X is uniquely qualified for [specific reason]," the X is grounded. Less likely XY.

### Q3 — What would the speaker do *with* X, once obtained?

If the answer is concrete and reveals the actual goal, that goal is Y. The candidate XY pattern is confirmed; reformulate around Y.

If the answer is "use X for its own sake" (rare, valid in pure-research contexts), it's not XY.

## Process

1. **Read the statement.**
2. **Count detection signals** (table above). If two or more, or one strong signal alone, proceed to Q1-Q3. Otherwise return "no XY pattern" with reasoning.
3. **Run Q1.** If the answer is "underlying situation unchanged," candidate XY confirmed.
4. **Run Q2 and Q3** to characterize the actual Y. **Note: more than one Y may be operative** — see Multi-Y case below.
5. **Reformulate.** Produce a candidate Y-shaped statement (or multiple, if Multi-Y) and a brief explanation of the X→Y move.

## Output Format

```
XY DETECTION — [first 60 chars of statement...]
─────────────────────────────────────────────
Signals matched: [list, with strength]
Verdict: [XY pattern detected | XY pattern detected (multi-Y) | No XY pattern | Ambiguous — recommend Socratic examination]

If XY detected (single Y):
  X (stated): [the attempted solution being asked about]
  Y (inferred): [the underlying goal]
  Reformulation: [Y-shaped problem statement]
  Confidence: [high | medium | low]
  Note: [any context the user should know about the inference]

If XY detected (multi-Y):
  X (stated): [the attempted solution]
  Y₁ (empirical): [the empirically-shaped underlying goal]
  Y₂ (values):    [the values-shaped underlying goal, if present]
  [Y₃, Y₄ ...]:   [additional Ys at different layers, if present]
  Recommendation: split into separate grader runs after reformulation. Empirical
                  Ys can run through the standard pipeline; values-shaped Ys
                  should escalate to values-excavator (philosophy/ethics) before
                  continuing.
  Confidence per Y: [...]
```

If verdict is "Ambiguous," recommend escalating to `socratic-examiner` (cross-domain — philosophy/dialectical-tools) to surface the user's actual goal through structured questioning.

### Multi-Y case

A single X often points at more than one Y. The two most common multi-Y patterns:

- **Empirical + values.** The user wants both an answer (empirical) and a resolution (values). Example: "find me second-order AI plays" hides both "given my coherent thesis, what positioning is best?" (empirical) and "how do I separate FOMO from alpha?" (values). Picking one Y throws away the other; split the audit into two runs.
- **Layered empirical.** Y₁ is one level above X; Y₂ is one level above Y₁. Example: "should we run preclinical models or AC tap?" → Y₁: "does the drug reach the retina?" → Y₂: "is this asset advanceable in NPDR given current ocular-PK signal?" Surface both; let the user pick which layer is the actual decision.

When multi-Y is detected, do NOT collapse to a single inferred Y. Surface all candidates with their type (empirical/values/layered-empirical) and let the user or the orchestrator route.

## Example: Detecting an XY Pattern

**Statement:** "How do I add a tutorial video to onboarding?"

**Signals:**
- Mechanism question (strong) ✓
- Solution-as-noun ("tutorial video") ✓
- No "because" ✓
- Pattern-matches a known stack ("tutorial videos in onboarding" is a familiar SaaS pattern) ✓

**Q1:** What changes if a tutorial video is added? — Onboarding has a video. But the user's underlying goal (presumably: improve activation) is not directly addressed. *XY confirmed.*

**Q2:** Why a tutorial video specifically? — Likely because competitors have them; cargo-culted.

**Q3:** What does the speaker want with the video? — Better activation rate, fewer support tickets.

**Output:**
```
X (stated): "Add a tutorial video to onboarding"
Y (inferred): "Improve activation rate and reduce onboarding-related support load"
Reformulation: "What changes to onboarding would meaningfully improve activation rate and reduce onboarding-related support volume?"
Confidence: medium (Y inferred; user should confirm)
```

The reformulated Y-statement opens up the solution space — a tutorial video is one of many options now, instead of the only option.

## Scope Boundaries

- **xy-detector handles:** detecting solution-disguised-as-problem patterns and inferring the candidate underlying goal.
- **xy-detector does NOT:** decide what the actual goal *should* be. The user does. The detector surfaces the question; the user answers it.

## Failure Modes

| Failure | Response |
|---|---|
| Confident "no XY pattern" but the statement has 2+ signals | Re-check signals; some may be weak or context-dependent. If still confident, document the reasoning |
| Ambiguous Q1 answer | Escalate to `socratic-examiner` rather than guess |
| Multiple plausible Ys | Surface all of them in the output; let the user pick |
| Speaker is asking about X for legitimate reasons (e.g., learning a specific technique) | "No XY pattern" is the right verdict. The Mechanism Question signal is necessary but not sufficient |

## Output Contract for `six-eyes`

When called from `six-eyes` Phase 6:

- If verdict is "XY pattern detected," feed the inferred Y and reformulation to the re-state loop at Level 1 or 2 (the reformulation is a candidate restatement)
- If verdict is "no XY pattern," return null; Phase 6 continues to other audit checks
- If verdict is "Ambiguous," set re-state level to L2 (decompose-further) with `socratic-examiner` as the recommended call

## Connections

- `statement-grader` (binding-vow) — the root-vs-symptom axis; XY patterns score 1/5 on that axis
- `kahneman-framing` (binding-vow) — XY is the canonical Type III error; this skill targets it specifically
- `socratic-examiner` (philosophy/dialectical-tools) — escalation path for ambiguous cases
- `claim-decomposer` (research) — when the inferred Y is itself compound, decompose Y rather than just substituting

## Sources

- Raymond, E. S. (compiler). *The Jargon File* — entry on the XY problem. (Folk-canonical formulation.)
- Mitroff, I. I., & Kilmann, R. H. (1978). *Methodological Approaches to Social Sciences*. Jossey-Bass. (Type III errors.)
- See [[kahneman-framing]] for the broader context of cognitive failure modes the detector targets.
