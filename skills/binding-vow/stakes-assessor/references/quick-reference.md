# Stakes Assessor — Quick Reference


## The Three Levels

| Stakes | Mode default | Time budget | Phase coverage |
|---|---|---|---|
| **Low** | quick | ≤30s | Phases 1, 5, 6 (statement-grader only) |
| **Medium** | standard | 2–5 min | All phases, single pass |
| **High** | deep | 5–15 min | All phases + frame rotation ≥3 alternatives + dual-audience compression + full audit |

## Quick Reference

| Axis | Low signal | Medium signal | High signal |
|---|---|---|---|
| **Reversibility** | Easily reversible (text edit, draft) | Reversible with effort (project pivot, role change) | Irreversible (public publication, capital commitment, signed contract) |
| **Magnitude** | Personal/team scale, low resource | Mid-scope: a project, a quarter, a hire | Org-wide, multi-quarter, multi-million, public-facing |
| **Time horizon** | This week | This quarter | Multi-year or career-long |
| **Audience reach** | Self or 1–3 people | A team / department | Public, board, organization-wide, regulator |
| **Optionality** | Many easy alternatives if this is wrong | A few alternatives, with switching cost | Few or no alternatives; locked in if committed |

## Quick Reference

| Phrase / context | Likely stakes |
|---|---|
| "Quick thought on...", "FYI...", "rough draft" | Low |
| "I'm noodling on...", "thinking through..." | Low or Medium |
| "We need to decide whether..." | Medium |
| "This is for the board / regulator / public release" | High |
| "Once we ship this we can't roll back" | High (irreversibility) |
| "Multi-quarter program", "8-figure decision", "headcount allocation" | High (magnitude) |
| "Career decision", "company strategy", "legal exposure" | High |
| Statement is about an essay angle (not yet drafted) | Low to Medium (draft is reversible) |
| Statement is about a public-facing artifact about to ship | High (irreversibility + reach) |

## Quick Reference

| Trigger | Upgrade |
|---|---|
| Irreversibility flag is set, even at medium aggregate | medium → deep |
| Audience-classifier returns `public` with skeptical sub-context | upgrade by one level |
| Problem-typology returns `wicked` or `mess` | upgrade by one level |
| Early Phase 6 grader signals show multiple-axis failure | trigger Re-state Level 3 (deep) |

## Edge Cases

| Pattern | Handling |
|---|---|
| User explicitly requests quick mode on a high-stakes statement | Run quick mode AND surface the stakes verdict prominently. Don't silently override; let the user own the trade-off |
| Statement is high on one axis (e.g., audience reach) but the user dismisses it ("it's just a blog post") | Apply the worst-case rule; flag the disagreement. Public publication is genuinely high-reach even if the author treats it casually |
| Stakes are unclear because the statement is too vague to assess | Return "deferred — need more specificity"; route back to Phase 1 |
| Stakes shift across iterations (statement starts low-stakes but becomes high-stakes after reformulation) | Re-run stakes-assessor on the reformulated statement; mode may change |

## Output Format

```
STAKES — [first 60 chars of statement...]
─────────────────────────────────────────────
Verdict: [low | medium | high]
Mode default recommendation: [quick | standard | deep]

Axis scores:
  Reversibility:     [low | medium | high]   [signal]
  Magnitude:         [low | medium | high]   [signal]
  Time horizon:      [low | medium | high]   [signal]
  Audience reach:    [low | medium | high]   [signal]
  Optionality:       [low | medium | high]   [signal]

Irreversibility flag: [none | present — note]
Rationale: [which axis drove the verdict]
```
