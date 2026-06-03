# SCQA Formatter — Story-Shape Compression

SCQA (Situation, Complication, Question, Answer) is Minto's canonical introduction structure. Where BLUF puts the answer first because the reader is short on time, SCQA earns the answer through narrative because the reader needs the complication to feel like a real problem before they accept the answer.

For the canonical specification, see [[minto-scqa]].

## When to Use SCQA (and Which Variant)

Three valid variants exist; pick by audience disposition:

| Variant | Use when | Structure |
|---|---|---|
| **Standard SCQA** | Reader is informed but unfocused; trust is intact | Situation → Complication → Question → Answer |
| **SCRA** (Resolution) | Reader knows the answer; you're proposing what to do | Situation → Complication → Resolution (replaces Question + Answer) |
| **Concern-priming** | Reader is skeptical; lead with their objection | Concern → Situation → Complication → Question → Answer (the Answer must address the Concern) |

If the audience is purely time-pressured and trusting, use BLUF instead (`bluf-shaper`). If the audience is an executive needing a full memo, use `executive-distiller`. SCQA's sweet spot is *peer*, *self-as-essay-reader*, and *colleague-presentation* audiences.

## Process

### Step 1 — Identify the Situation

A *familiar truth* the reader already accepts. Not your interpretation, not the spin — something they'd nod at without resistance.

Test: if you said this sentence to the audience cold, would they push back? If yes, it's not Situation, it's Complication or Answer in disguise.

Examples (good):
- "We've grown 3× in two years."
- "TYK2 inhibitors have shown CNS penetrance signal in our HV study."

Examples (bad — too contested for Situation):
- "Our growth has been undisciplined." (interpretation, not fact)
- "Our TYK2 program is in trouble." (your conclusion, not shared starting point)

### Step 2 — Identify the Complication

Something that *changed* or a *tension* that emerged from the Situation. The reader feels the bump.

Examples:
- "But customer churn has accelerated to 12%."
- "But CSF-level data doesn't predict retinal exposure."

Test: does the Complication, paired with the Situation, naturally raise a question? If yes, you have the right Complication. If the question is forced, the Complication is wrong.

### Step 3 — Frame the Question

The implicit question the Complication raises. Often you don't need to *write* the Question explicitly — the reader generates it. But you must be able to state it, because the Answer must answer it.

Examples:
- (Situation: 3× growth; Complication: churn ↑) → Q: "What's driving the churn and what do we do?"
- (Situation: CNS signal; Complication: no retinal data) → Q: "What evidence would let us decide whether to advance into NPDR?"

If you write the Question explicitly, do so in one sentence.

### Step 4 — State the Answer

The Answer is the governing thought (top of the Minto Pyramid if you extend the structure below). Not the full reasoning; the conclusion.

The Answer may be:
- A recommendation: "Rebuild onboarding in Q3 with 4 engineers."
- A diagnosis: "Onboarding is the dominant churn driver."
- A plan: "Run preclinical PK in [model X] with retinal-tissue LC-MS/MS readout, then decide."

### Step 5 (Optional) — One-level Pyramid Below the Answer

For longer outputs, add 2–4 supporting subthoughts under the Answer. Each must be MECE-checked (mutually exclusive, collectively exhaustive). For deeper recursion, escalate to `executive-distiller`.

## Output Format

```
SITUATION:    [familiar truth the reader accepts]

COMPLICATION: [what changed, or what tension emerged]

QUESTION:     [implicit Q raised; optional to state explicitly]

ANSWER:       [the governing thought — recommendation, diagnosis, or plan]

[OPTIONAL] SUPPORTING:
  1. [subthought 1 — MECE with siblings]
  2. [subthought 2]
  3. [subthought 3]

[OPTIONAL] VARIANT NOTE: [if SCRA or Concern-priming, note the variant and why]
```

## Variant Examples

### SCRA (when answer is known)

```
SITUATION:    We've identified onboarding as the dominant churn driver.
COMPLICATION: Q3 budget allocates only 1 engineer to the rebuild; the team estimate
              is 4 engineer-quarters minimum.
RESOLUTION:   Reallocate 3 engineers from low-priority Q3 features; defer the
              [feature X] launch to Q4.
```

### Concern-priming (when reader is skeptical)

```
CONCERN:      "Aren't we already over-invested in onboarding fixes?"
SITUATION:    Yes — we ran two onboarding revisions in the last 12 months.
COMPLICATION: But neither targeted the 90-second activation window, where the
              Farrar et al. data shows 60% of churn originates.
QUESTION:     Should we run a third onboarding effort if it targets the right window?
ANSWER:       Yes. Different intervention point, different evidence base, different
              expected outcome.
```

## Failure Modes

| Failure | Response |
|---|---|
| Situation requires explanation to be accepted | It's not a Situation; it's contested. Find a more upstream fact the reader does accept |
| Complication doesn't naturally raise a question | The Complication is wrong — find one that produces a felt-need for the Answer |
| Answer is multi-paragraph | Pyramid is collapsing into the introduction; promote the multi-paragraph content to "SUPPORTING" subthoughts and keep the Answer one sentence |
| Reader-skepticism signal but no Concern-priming applied | Re-shape with the variant; the standard form will be rejected before the Answer lands |
| Statement is too short to be meaningfully shaped | Re-grade specificity in `statement-grader`; SCQA needs enough material to have a story |

## Output Contract for `six-eyes`

Phase 5 audience routing:
- Audience `peer` → standard SCQA
- Audience `self` → standard SCQA, optionally skip the Question line (you already have the Situation)
- Audience `public` with skepticism flag → Concern-priming variant
- Audience `exec` with length budget short → route to `bluf-shaper` instead
- Audience `exec` with length budget long → route to `executive-distiller`

## Scope Boundaries

- **scqa-formatter handles:** building the four-component introduction (and optional one-level pyramid).
- **scqa-formatter does NOT:** build deep recursive pyramids — that's `executive-distiller`'s job. Pick variant; if you find yourself wanting >1 level of supporting, escalate.

## Connections

- `minto-scqa` (binding-vow) — canonical reference for SCQA structure and variants
- `bluf-shaper` (binding-vow) — sibling for time-pressured audiences
- `executive-distiller` (binding-vow) — sibling for full memo-shape outputs
- `argument-structure` (writing/rhetoric) — Toulmin/Rogerian/classical scaffolding for the supporting layer when needed

## Sources

- Minto, B. (1987, 2003). *The Pyramid Principle*. (Canonical SCQA specification.)
- See [[minto-scqa]] for the full BLUF/SCQA/Pyramid comparator.
