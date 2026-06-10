# Bluf Shaper — Quick Reference


## When to Use BLUF (and When Not To)

| Use BLUF | Don't use BLUF |
|---|---|
| Reader has ≤30 seconds before deciding | Reader needs to be persuaded — use SCQA |
| The recommendation is well-grounded and the reader trusts you | Reader is skeptical and needs the reasoning to land before the answer |
| You're delivering to an executive, on-call engineer, or operational decision-maker | You're writing a document for archive or training |
| Channel is short-form (slack, email subject + first line, briefing card) | Channel is a memo or essay |
| Audience tag from `audience-classifier` is `exec` AND length budget is short | Audience is `peer`, `self`, `public`, or `LLM` (different formats apply) |

## Failure Modes

| Failure | Response |
|---|---|
| Bottom line is two sentences | Compress further; if you can't, the statement isn't BLUF-ready — re-grade specificity |
| Background takes >3 lines | You're writing a memo, not a BLUF — switch to `executive-distiller` |
| Discussion has >5 points | You're padding; cut to the strongest 3 |
| Recommendation is vague ("we should consider...") | Force specificity: who does what by when? If you can't, the recommendation isn't ready |
| Reader is skeptical of you or the topic | BLUF is wrong format — switch to `scqa-formatter` so the complication earns the answer |

## Output Format

```
BOTTOM LINE: [one sentence — the answer or recommendation]

BACKGROUND:
- [fact 1; minimum context]
- [fact 2; only if essential]

DISCUSSION:
1. [strongest reason]
2. [second-strongest]
3. [supporting reason; optional if length-constrained]

RECOMMENDATION: [specific action requested, or "FYI — no action needed"]

[OPTIONAL] RISK IF DEFERRED: [single sentence on cost of inaction; only if material]
```
