---
name: problem-typology
description: >
  Classify a problem statement on the five-way typology — well-defined / ill-defined / wicked
  (Rittel and Webber) / mess (Ackoff) / adaptive (Heifetz). Use during binding-vow's Phase 2
  diagnosis to drive mode selection (quick/standard/deep) and decomposition-method choice.
  Returns a typology tag plus rationale and confidence.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Problem Typology — The Five-Way Classifier

Most problems are mistyped on first encounter. Treating a wicked problem as tame (with off-the-shelf solutions) produces failure. Treating a mess as a problem (decomposing what shouldn't be decomposed) produces compound failure. Treating an adaptive challenge as technical (buying tools instead of changing culture) is Heifetz's diagnostic case. Right typology unlocks right method.

Foundational references: [[wicked-vs-tame]] and [[ackoff-mess]]. This skill operationalizes the diagnostic heuristics in those references.

## The Five Types

| Type | Definition | Decomp method | Mode default |
|---|---|---|---|
| **Well-defined** | Inputs, constraints, success criteria all explicit; tame in Rittel terms | 5 Whys or skip decomposition | quick |
| **Ill-defined** | Some inputs or criteria fuzzy but stable; can be tightened to well-defined with effort | Fishbone | standard |
| **Wicked** | Rittel & Webber 1973; formulation is provisional and shifts with action | CRT or stakeholder rotation | deep |
| **Mess** | Ackoff 1974; multiple interrelated problems; the unit of analysis is wrong | Step out — call `ackoff-mess`; consider dissolution | deep |
| **Adaptive** | Heifetz; requires changes in values, beliefs, behaviors, loyalties; technical fixes will fail | Stakeholder rotation + `values-excavator` | deep |

Most fuzzy dumps land in *ill-defined* or *adaptive*. Pure *well-defined* is rare in the wild; pure *wicked* requires a body of evidence.

## Diagnostic Signals

Triage by scanning the statement for these patterns:

| Signal | Likely typology |
|---|---|
| "How do I [verb] [object]?" with stable inputs and clear success criteria | Well-defined |
| "Why isn't X working?" with multiple plausible causes | Ill-defined |
| "What should we do about [contested societal/organizational issue]?" | Wicked |
| "We've tried solving X but Y, Z, and W keep coming up" | Mess |
| "We know what to do but we can't get the team / people / org to do it" | Adaptive |
| Sub-problem that's solvable but its solution would make other parts worse | Mess |
| Stakeholders disagree on what the problem IS, not just what to do about it | Mess or Wicked |
| Improving any single metric makes another important metric worse | Mess |
| Solution requires changes to values/beliefs, not just tools/process | Adaptive |

A statement may show signals from multiple types. Pick the *most upstream* type — if both Ill-defined and Wicked apply, choose Wicked; if both Mess and Adaptive apply, the typology depends on whether the dissolution would have to address values (Adaptive) or system structure (Mess).

## Decision Tree

1. Are inputs, constraints, and success criteria all explicit and stable?
   - Yes → **Well-defined**. Stop.
   - No → continue.
2. Does the statement involve multiple interrelated problems where interactions matter?
   - Yes → **Mess**. Stop.
   - No → continue.
3. Does resolution require changes in values, beliefs, behaviors, or loyalties?
   - Yes → **Adaptive**. Stop.
   - No → continue.
4. Is the problem formulation itself contested (different stakeholders define the problem differently)?
   - Yes → **Wicked**. Stop.
   - No → continue.
5. Are some inputs or criteria fuzzy but resolvable with effort?
   - Yes → **Ill-defined**. Stop.
   - No → return to Step 1 — the statement may be underspecified.

## Output Format

```
PROBLEM TYPOLOGY — [first 60 chars of statement...]
─────────────────────────────────────────────
Type:        [well-defined | ill-defined | wicked | mess | adaptive]
Confidence:  [high | medium | low]
Rationale:   [which signals matched; which decision-tree branch fired]
Alternative: [second-most-plausible type, if relevant — note when this matters]

Downstream routing implications:
- Mode default:           [quick | standard | deep]
- Decomp method:          [5 Whys | Fishbone | dependency | CRT | step out]
- Notable phases:         [any phases that change behavior for this type]
```

## Downstream Routing

The orchestrator (`six-eyes`) uses the typology tag to adjust phases:

- **Well-defined**: skip Phase 4 (reframing) and most of Phase 6 (audit) — use quick mode
- **Ill-defined**: standard pipeline; emphasize Phase 3 (decomposition) and Phase 6 (audit specifically the answerability and scope axes)
- **Wicked**: deep mode; mandatory ≥3-alternative frame rotation in Phase 4; statement-grader threshold relaxed (wicked problems can't fully satisfy specificity)
- **Mess**: deep mode AND skip `claim-decomposer` in Phase 3 (atomic decomp destroys the mess structure); call `ackoff-mess` reference; consider dissolution before solution
- **Adaptive**: deep mode; mandatory `stakeholder-rotator` in Phase 4; call `values-excavator` (philosophy/ethics) before any compression

## Edge Cases

| Pattern | Handling |
|---|---|
| Statement is multi-paragraph and shifts types across paragraphs | The statement is compound; route to `claim-decomposer` (research) first, then run typology on each atomic claim. The compound statement is itself a Mess of sub-problems |
| User insists their problem is well-defined when typology suggests adaptive | Flag the conflict; the user's framing may be Type III (right answer to wrong question). Run `xy-detector` for confirmation |
| Confidence is low across all five types | The statement is underspecified — return to Phase 1 (Intake) for restatement before retrying classification |
| The problem is partially well-defined and partially wicked (common) | Tag the more-upstream component. If the wicked component drives the decision, classify as wicked even if implementation has well-defined steps |

## Output Contract for `six-eyes`

Called from Phase 2 (Diagnose). Returns the typology tag, confidence, rationale, and downstream routing implications. These feed:
- `stakes-assessor` (which may adjust the mode default based on stakes)
- Phase 3 decomposition (which routes to `root-vs-symptom-tagger` with the typology tag)
- Phase 4 reframing intensity
- Phase 6 audit threshold adjustments

If confidence is low, recommend re-running Phase 1 Intake rather than proceeding with a weak classification.

## Connections

- `wicked-vs-tame` (binding-vow) — foundational reference for Rittel + Heifetz typology
- `ackoff-mess` (binding-vow) — foundational reference for the Mess type
- `stakes-assessor` (binding-vow) — downstream classifier that adjusts mode based on stakes
- `audience-classifier` (binding-vow) — runs in parallel; together they define the Phase 2 profile
- `root-vs-symptom-tagger` (binding-vow) — downstream consumer; uses typology to select decomp method
- `claim-decomposer` (research) — escalation path for compound multi-typology statements
- `xy-detector` (binding-vow) — escalation path for user-typology mismatches

## Sources

- Rittel, H. W. J., & Webber, M. M. (1973). "Dilemmas in a General Theory of Planning." *Policy Sciences*, 4, 155–169.
- Ackoff, R. L. (1974). *Redesigning the Future*. Wiley.
- Heifetz, R. A. (1994). *Leadership Without Easy Answers*. Belknap Press.
- See [[wicked-vs-tame]] and [[ackoff-mess]] for the operationalized diagnostic patterns this skill encodes.
