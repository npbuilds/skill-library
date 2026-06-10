# Xy Detector — Quick Reference


## Quick Reference

| Signal | Pattern | Strength |
|---|---|---|
| **Mechanism question** | "How do I [specific technical action]?" with no stated reason | Strong |
| **Disguised constraint** | "I want X but Y prevents it" — Y is presented as constraint, but Y might *be* the goal | Strong |
| **Solution-as-noun** | The X being asked about is a noun that names a specific tool/method/format | Medium |
| **Mismatch in stakes** | The mechanical specificity of X seems disproportionate to the framing's apparent stakes | Medium |
| **No "because"** | The statement has no causal grounding; the speaker hasn't surfaced *why* X matters | Medium |
| **Pattern-matches a known stack** | X fits a familiar engineering/business pattern; the speaker may have copied the pattern without checking the goal | Weak |

## Failure Modes

| Failure | Response |
|---|---|
| Confident "no XY pattern" but the statement has 2+ signals | Re-check signals; some may be weak or context-dependent. If still confident, document the reasoning |
| Ambiguous Q1 answer | Escalate to `socratic-examiner` rather than guess |
| Multiple plausible Ys | Surface all of them in the output; let the user pick |
| Speaker is asking about X for legitimate reasons (e.g., learning a specific technique) | "No XY pattern" is the right verdict. The Mechanism Question signal is necessary but not sufficient |

## Formula / Pseudocode

```
X (stated): "Add a tutorial video to onboarding"
Y (inferred): "Improve activation rate and reduce onboarding-related support load"
Reformulation: "What changes to onboarding would meaningfully improve activation rate and reduce onboarding-related support volume?"
Confidence: medium (Y inferred; user should confirm)
```
