# Scqa Formatter — Quick Reference


## Quick Reference

| Variant | Use when | Structure |
|---|---|---|
| **Standard SCQA** | Reader is informed but unfocused; trust is intact | Situation → Complication → Question → Answer |
| **SCRA** (Resolution) | Reader knows the answer; you're proposing what to do | Situation → Complication → Resolution (replaces Question + Answer) |
| **Concern-priming** | Reader is skeptical; lead with their objection | Concern → Situation → Complication → Question → Answer (the Answer must address the Concern) |

## Failure Modes

| Failure | Response |
|---|---|
| Situation requires explanation to be accepted | It's not a Situation; it's contested. Find a more upstream fact the reader does accept |
| Complication doesn't naturally raise a question | The Complication is wrong — find one that produces a felt-need for the Answer |
| Answer is multi-paragraph | Pyramid is collapsing into the introduction; promote the multi-paragraph content to "SUPPORTING" subthoughts and keep the Answer one sentence |
| Reader-skepticism signal but no Concern-priming applied | Re-shape with the variant; the standard form will be rejected before the Answer lands |
| Statement is too short to be meaningfully shaped | Re-grade specificity in `statement-grader`; SCQA needs enough material to have a story |

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

## SCRA (when answer is known)

```
SITUATION:    We've identified onboarding as the dominant churn driver.
COMPLICATION: Q3 budget allocates only 1 engineer to the rebuild; the team estimate
              is 4 engineer-quarters minimum.
RESOLUTION:   Reallocate 3 engineers from low-priority Q3 features; defer the
              [feature X] launch to Q4.
```

## Concern-priming (when reader is skeptical)

```
CONCERN:      "Aren't we already over-invested in onboarding fixes?"
SITUATION:    Yes — we ran two onboarding revisions in the last 12 months.
COMPLICATION: But neither targeted the 90-second activation window, where the
              Farrar et al. data shows 60% of churn originates.
QUESTION:     Should we run a third onboarding effort if it targets the right window?
ANSWER:       Yes. Different intervention point, different evidence base, different
              expected outcome.
```
