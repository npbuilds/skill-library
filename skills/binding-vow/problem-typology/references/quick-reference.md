# Problem Typology — Quick Reference


## The Five Types

| Type | Definition | Decomp method | Mode default |
|---|---|---|---|
| **Well-defined** | Inputs, constraints, success criteria all explicit; tame in Rittel terms | 5 Whys or skip decomposition | quick |
| **Ill-defined** | Some inputs or criteria fuzzy but stable; can be tightened to well-defined with effort | Fishbone | standard |
| **Wicked** | Rittel & Webber 1973; formulation is provisional and shifts with action | CRT or stakeholder rotation | deep |
| **Mess** | Ackoff 1974; multiple interrelated problems; the unit of analysis is wrong | Step out — call `ackoff-mess`; consider dissolution | deep |
| **Adaptive** | Heifetz; requires changes in values, beliefs, behaviors, loyalties; technical fixes will fail | Stakeholder rotation + `values-excavator` | deep |

## Quick Reference

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

## Edge Cases

| Pattern | Handling |
|---|---|
| Statement is multi-paragraph and shifts types across paragraphs | The statement is compound; route to `claim-decomposer` (research) first, then run typology on each atomic claim. The compound statement is itself a Mess of sub-problems |
| User insists their problem is well-defined when typology suggests adaptive | Flag the conflict; the user's framing may be Type III (right answer to wrong question). Run `xy-detector` for confirmation |
| Confidence is low across all five types | The statement is underspecified — return to Phase 1 (Intake) for restatement before retrying classification |
| The problem is partially well-defined and partially wicked (common) | Tag the more-upstream component. If the wicked component drives the decision, classify as wicked even if implementation has well-defined steps |

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
