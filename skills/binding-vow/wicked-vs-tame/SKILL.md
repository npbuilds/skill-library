---
name: wicked-vs-tame
description: >
  Reference the wicked/tame problem distinction (Rittel and Webber 1973) and Heifetz's
  adaptive/technical leadership challenge framework. Use when classifying a problem
  statement, deciding whether iteration is structural or technical, or understanding why
  a problem keeps resisting clean formulation. Foundational reference for binding-vow's
  problem-typology skill.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Wicked vs Tame — The Problem Typology

Some problems are tame — well-defined, with clear inputs, knowable solutions, and a stopping rule that says "done." Others are wicked — every formulation is provisional, the problem itself shifts as you act on it, and there is no stopping rule, only good-enough. Confusing the two is the most common architectural error in problem-solving.

Two reference frames matter: Rittel & Webber 1973 (wicked vs tame) and Heifetz (adaptive vs technical). They are nearly equivalent for binding-vow's purposes; together they cover ~95% of the typology surface.

## Rittel & Webber: Ten Properties of Wicked Problems

A wicked problem exhibits most or all of these. A tame problem exhibits few or none.

| # | Property | Plain-language test |
|---|---|---|
| 1 | No definitive formulation | The problem changes as you understand it more |
| 2 | No stopping rule | You stop when resources run out, not when "solved" |
| 3 | Solutions are good-or-bad, not true-or-false | No objective verdict on correctness |
| 4 | No immediate or ultimate test of a solution | Consequences play out over years; can't AB-test |
| 5 | Every solution is a "one-shot operation" | Implementing the solution changes the problem |
| 6 | No exhaustive set of potential solutions | Solutions are invented, not enumerated |
| 7 | Every wicked problem is essentially unique | Past patterns guide but don't determine |
| 8 | Every wicked problem can be a symptom of another | Pull on a thread; another problem appears |
| 9 | Discrepancies admit multiple explanations | Causal attribution is contested |
| 10 | The planner has no right to be wrong | Stakes are real and irreversible |

Examples: urban planning, climate policy, foreign policy, organizational culture, drug development strategy, parenting.

## Heifetz: Adaptive vs Technical Challenges

| Type | Characteristics | Authority's role |
|---|---|---|
| **Technical** | Known solution exists; expert can apply it; problem and solution clear | Authority defines, decides, executes |
| **Adaptive** | No known solution; requires changes in values, beliefs, behaviors, loyalties; problem definition is itself contested | Authority frames; people closest to problem must do the adaptive work |
| **Mixed** | Has both technical and adaptive elements (most real challenges) | Authority must distinguish which is which and resist treating adaptive as technical |

The classic Heifetz failure mode: applying a technical fix to an adaptive problem. Instructive example: "we have a productivity problem" — buying productivity software (technical) when the actual issue is misaligned incentives or unclear roles (adaptive).

## Five-Way Typology (binding-vow uses this)

Binding-vow's `problem-typology` skill extends the binary into five categories:

| Type | Definition | Decomp method | Mode default |
|---|---|---|---|
| **Well-defined** | Inputs, constraints, success criteria all explicit; tame in Rittel terms | 5 Whys or skip decomposition | quick |
| **Ill-defined** | Some inputs or criteria fuzzy but stable; can be tightened to well-defined | Fishbone | standard |
| **Wicked** | Rittel & Webber 1973; formulation is provisional and shifts with action | CRT (Goldratt) or stakeholder rotation | deep |
| **Mess** | Ackoff 1974; multiple interrelated problems; the unit of analysis is wrong | Step out — call `ackoff-mess`; consider dissolution | deep |
| **Adaptive** | Heifetz; requires changes in values/beliefs; technical fixes will fail | Stakeholder rotation + values-excavator | deep |

Most real-world fuzzy dumps land in *ill-defined* or *adaptive*. Pure *well-defined* is rare in the wild; pure *wicked* requires a body of evidence.

## Diagnostic Heuristics

Quick triage for `problem-typology`:

| Signal | Likely type |
|---|---|
| "How do I [verb] [object]?" with stable inputs | Well-defined |
| "Why isn't X working?" with multiple possible causes | Ill-defined |
| "What should we do about [contested societal issue]?" | Wicked |
| "We've tried solving X but Y, Z, and W keep coming up" | Mess |
| "We know what to do but we can't get the team to do it" | Adaptive |

## Common Mistakes

- Treating wicked as tame — buying a solution off the shelf and being surprised it doesn't fit.
- Treating tame as wicked — over-thinking, over-stakeholdering, never converging on something simple.
- Treating adaptive as technical — Heifetz's diagnostic case. The hardest typology error to detect from inside.
- Treating a *mess* as a single problem — Ackoff's diagnostic. Symptom: every solution creates two new problems.
- Demanding a definitive formulation up-front for a wicked problem — Rittel: "the formulation is the work."

## Connections

- `problem-typology` (binding-vow, future) — implements the five-way classifier above
- `ackoff-mess` (binding-vow) — when typology returns "mess," route here
- `values-excavator` (philosophy/ethics) — adaptive problems require this
- `claim-decomposer` (research) — implements the decomp methods this typology selects between
- Vault note: `skill-lab/root-cause-methods-comparator.md`

## Sources

- Rittel, H. W. J., & Webber, M. M. (1973). "Dilemmas in a General Theory of Planning." *Policy Sciences*, 4, 155–169.
- Heifetz, R. A. (1994). *Leadership Without Easy Answers*. Belknap Press.
- Heifetz, R. A., Linsky, M., & Grashow, A. (2009). *The Practice of Adaptive Leadership*. Harvard Business Press.
- Ackoff, R. L. (1974). *Redesigning the Future*. Wiley. (Source of the "mess" concept that extends Rittel's wicked.)
