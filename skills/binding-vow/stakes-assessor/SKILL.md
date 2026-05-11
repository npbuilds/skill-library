---
name: stakes-assessor
description: >
  Assess the stakes of a problem statement as low / medium / high. Drives binding-vow's mode
  selection (quick for low / standard for medium / deep for high). The architectural answer
  to Reiter-Palmon's automaticity finding: low-stakes statements get the fast lane so the
  suite doesn't get bypassed; high-stakes get the full audit pipeline. Returns a stakes tag
  plus rationale and any flagged irreversibility signals.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Stakes Assessor — Fast-Lane vs Deep-Lane Gate

Problem construction is automatic (Reiter-Palmon). A friction-heavy suite that overlaps with cognitive default will get bypassed precisely when most needed. The fast-lane / deep-lane split is binding-vow's structural answer: low-stakes statements clear in ≤30 seconds; high-stakes statements get the full seven-phase audit. This skill makes the call.

The skill is opinionated: it defaults toward *higher* stakes when uncertain. The cost of running standard mode on a low-stakes statement is wasted seconds; the cost of running quick mode on a high-stakes statement is a misframed decision.

## The Three Levels

| Stakes | Mode default | Time budget | Phase coverage |
|---|---|---|---|
| **Low** | quick | ≤30s | Phases 1, 5, 6 (statement-grader only) |
| **Medium** | standard | 2–5 min | All phases, single pass |
| **High** | deep | 5–15 min | All phases + frame rotation ≥3 alternatives + dual-audience compression + full audit |

The mode is a *default*. The orchestrator can upgrade (e.g., quick → standard if early grader signals fail) but rarely downgrades.

## Five-Axis Scoring

Stakes are scored across five axes. Each axis returns low / medium / high; aggregate is the maximum (worst-case rules).

| Axis | Low signal | Medium signal | High signal |
|---|---|---|---|
| **Reversibility** | Easily reversible (text edit, draft) | Reversible with effort (project pivot, role change) | Irreversible (public publication, capital commitment, signed contract) |
| **Magnitude** | Personal/team scale, low resource | Mid-scope: a project, a quarter, a hire | Org-wide, multi-quarter, multi-million, public-facing |
| **Time horizon** | This week | This quarter | Multi-year or career-long |
| **Audience reach** | Self or 1–3 people | A team / department | Public, board, organization-wide, regulator |
| **Optionality** | Many easy alternatives if this is wrong | A few alternatives, with switching cost | Few or no alternatives; locked in if committed |

Aggregate rule: the *worst* (highest-stakes) of the five axes drives the verdict. A statement that's low on four axes and high on one (e.g., irreversible) is **high stakes**.

## Detection Signals

Quick triage before running the five-axis scoring:

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

## Process

1. **Quick triage** — scan for any High signal in the table above. If present, jump to step 4.
2. **Score the five axes** explicitly. Each axis: low / medium / high.
3. **Aggregate** — take the worst-case (highest) axis as the verdict.
4. **Surface irreversibility** as a separate flag — even at medium aggregate, if any axis is "irreversible," flag it. The orchestrator may upgrade to deep mode based on this alone.
5. **Return** verdict + axis scores + irreversibility flag.

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

## When to Upgrade

The orchestrator may upgrade the mode beyond the stakes default in these cases:

| Trigger | Upgrade |
|---|---|
| Irreversibility flag is set, even at medium aggregate | medium → deep |
| Audience-classifier returns `public` with skeptical sub-context | upgrade by one level |
| Problem-typology returns `wicked` or `mess` | upgrade by one level |
| Early Phase 6 grader signals show multiple-axis failure | trigger Re-state Level 3 (deep) |

Conversely, the orchestrator may *not* downgrade against the stakes verdict. A high-stakes problem doesn't get quick mode just because the user is in a hurry.

## Edge Cases

| Pattern | Handling |
|---|---|
| User explicitly requests quick mode on a high-stakes statement | Run quick mode AND surface the stakes verdict prominently. Don't silently override; let the user own the trade-off |
| Statement is high on one axis (e.g., audience reach) but the user dismisses it ("it's just a blog post") | Apply the worst-case rule; flag the disagreement. Public publication is genuinely high-reach even if the author treats it casually |
| Stakes are unclear because the statement is too vague to assess | Return "deferred — need more specificity"; route back to Phase 1 |
| Stakes shift across iterations (statement starts low-stakes but becomes high-stakes after reformulation) | Re-run stakes-assessor on the reformulated statement; mode may change |

## Output Contract for `six-eyes`

Called from Phase 2 (Diagnose), in parallel with `problem-typology` and `audience-classifier`. Returns:
- Stakes verdict (low / medium / high)
- Mode default recommendation
- Per-axis scores
- Irreversibility flag

`six-eyes` uses these to set the mode for the run. If irreversibility is flagged, the orchestrator upgrades the mode even if aggregate stakes are medium. This is the Reiter-Palmon mitigation: low-stakes statements clear fast, but anything irreversible gets full audit regardless.

## Connections

- `problem-typology` (binding-vow) — runs in parallel; some typologies (wicked, mess, adaptive) imply high stakes by default
- `audience-classifier` (binding-vow) — runs in parallel; public audience often implies high stakes
- `statement-grader` (binding-vow) — independent skill but mode-selection feedback loop: catastrophic grader failures may upgrade stakes retroactively
- `xy-detector` (binding-vow) — XY patterns often hide high-stakes decisions inside low-stakes-shaped questions

## Sources

- Reiter-Palmon, R., Mumford, M. D., & Redmond, M. R. (1994). Problem construction model — the "automatic problem construction" finding is the empirical anchor for the fast/deep split.
- The five-axis scoring is derived from synthesizing irreversibility-focused decision theory (Bezos's "Type 1 vs Type 2 decisions") with magnitude-and-reach concepts from operational risk management.
- See [[binding-vow-research-findings]] vault note for the empirical foundation discussion.
