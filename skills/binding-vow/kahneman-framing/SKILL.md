---
name: kahneman-framing
description: >
  Reference framing effects, attribute substitution (replacing a hard question with an
  easier one), Einstellung effect (functional fixedness in problem-solving), and Type III
  errors (right answer to wrong question). Use when binding-vow's audit subdomain checks
  for cognitive failure modes in problem statements, or when diagnosing why a formulation
  feels off.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Kahneman Framing — Cognitive Failure Modes in Problem Statements

The four failure modes binding-vow's audit subdomain checks for are not bugs in reasoning — they are features of how human cognition produces problem statements automatically. Understanding the mechanism makes detection routine; without the mechanism, detection feels like art.

The four modes are independent. A single problem statement can exhibit all of them simultaneously.

## 1. Framing Effects (Tversky & Kahneman)

The same factual content, presented in different framings, produces systematically different judgments and choices. Framing is not noise — it is a determinant of decision.

Canonical example (Asian disease problem, 1981):
- Frame A: "200 of 600 will be saved" → 72% choose certain
- Frame B: "400 of 600 will die" → 78% choose risky

The two frames are mathematically identical. The choices reverse.

| Framing axis | Effect |
|---|---|
| **Gain vs loss** | Loss frames produce risk-seeking; gain frames produce risk-aversion |
| **Default vs opt-in** | Default settings dominate even when costs are negligible |
| **Reference point** | Performance evaluated against a salient anchor; arbitrary anchors stick |
| **Granularity** | Same data presented per-event vs per-aggregate produces different judgments |
| **Active vs passive voice** | "Mistakes were made" vs "I made mistakes" allocates blame differently |

**Implication for problem statements:** before treating a stated problem as the problem, ask what frame is in use. The frame chooses what counts as evidence and what counts as a solution.

## 2. Attribute Substitution (Kahneman & Frederick)

When asked a hard question, the mind unconsciously substitutes an easier question and answers that one instead. The substitution is automatic and invisible.

| Hard question | Substituted (easier) question |
|---|---|
| "Is this candidate qualified for the job?" | "How likable is this candidate?" |
| "What is the probability this startup succeeds?" | "How vivid / coherent is the founder's pitch?" |
| "Should I take this medication?" | "How do I feel about the doctor?" |
| "Is this argument valid?" | "Do I agree with the conclusion?" |
| "What's the right answer?" | "What's the easy answer?" |

The substitution mechanism is universal and automatic (System 1, in *Thinking, Fast and Slow*). The detection mechanism is rare and effortful (System 2). Binding-vow's audit makes the detection routine by asking explicitly: *what easier question might be answering instead?*

## 3. Einstellung Effect (Luchins 1942)

Once a familiar problem-solving pattern has worked, it suppresses awareness of better alternatives. The pattern doesn't just compete with the alternative — it makes the alternative invisible.

Original water-jar studies (Luchins 1942): subjects taught a 5-step solution for measuring water volumes failed to see a 2-step solution that was available, even when the 2-step was the only valid solution for a later problem.

**Modern instances:**

| Domain | Einstellung pattern |
|---|---|
| Software | "We've always done it with a relational DB" — graph or document store invisible |
| Medicine | "The differential includes A, B, C" — D never considered because A-C are the trained set |
| Investing | "This looks like the 2008 setup" — current setup's distinguishing features ignored |
| Strategy | "Our playbook works" — opponent has read the playbook |

**Implication for problem statements:** when a stated problem fits a familiar pattern, the audit must check whether the pattern is suppressing better formulations. Pattern-matching produces the *first* viable framing, not the best.

## 4. Type III Error (Mitroff & Kilmann 1978)

A Type I error is a false positive (rejecting a true null). A Type II error is a false negative (failing to reject a false null). A Type III error is *the right answer to the wrong question* — a perfectly valid solution to a problem that wasn't the actual problem.

Type III errors are the most expensive cognitive failure mode in real-world work because:
- They look successful from inside the analysis (the math checks out)
- They require external feedback (something that should have happened didn't) to detect
- The cost is fully incurred before detection is possible

The XY problem (Raymond, *Jargon File*) is a special case: someone asks how to do X (their attempted solution) instead of asking about Y (their actual goal). All XY problems are Type III errors waiting to happen.

**Diagnostic for Type III:**
- Did anyone ever ask "is this the right question to be asking"?
- Could the proposed answer be correct AND the situation still be unimproved?
- Has the question been audited against the actual goal, or against a proxy goal?

## How binding-vow uses these four modes

Each mode maps to a specific audit skill (Phase 6):

| Cognitive mode | Audit skill | Detection question |
|---|---|---|
| Framing effect | `frame-rotator` (Phase 4 reframing) + `assumption-excavator` (framing category) | "What other frames exist? What does each make visible?" |
| Attribute substitution | `answerability-tester` + `statement-grader` (specificity axis) | "What easier question might this statement be answering instead of the hard one?" |
| Einstellung | `frame-rotator` (Munger inversion) + `inversion-tool` | "What pattern is suppressing alternatives here?" |
| Type III | `xy-detector` + `statement-grader` (root-vs-symptom axis) | "What is the actual goal? Is this the question that gets us there?" |

The audit subdomain is Reiter-Palmon's "automatic problem construction" finding made operational. Construction is automatic; the audit makes the failure modes detectable.

## Common Mistakes

- Treating framing effects as bias to be eliminated. They cannot be eliminated; only made explicit.
- Looking for attribute substitution only in others' reasoning. Yours has it too. Especially yours.
- Believing Einstellung only affects novices. Experts are *more* susceptible — the pattern library is denser.
- Confusing Type III with Type I/II. Type I and II are statistical; Type III is conceptual. Different machinery, different detection.
- Relying on intuition to detect any of these. The whole point is that intuition produces the failure mode in the first place.

## Connections

- `xy-detector` (binding-vow, future) — primary Type III detection
- `statement-grader` (binding-vow, future) — six-axis grader checks all four modes implicitly
- `answerability-tester` (binding-vow, future) — primary attribute-substitution detection
- `frame-rotator`, `inversion-tool` (binding-vow, future) — primary framing-effect and Einstellung mitigation
- `assumption-excavator` (philosophy/logic) — surfaces framing assumptions explicitly

## Sources

- Tversky, A., & Kahneman, D. (1981). "The Framing of Decisions and the Psychology of Choice." *Science*, 211(4481), 453–458.
- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux. (Comprehensive treatment of System 1 / System 2 and attribute substitution.)
- Kahneman, D., & Frederick, S. (2002). "Representativeness Revisited: Attribute Substitution in Intuitive Judgment." In *Heuristics and Biases* (Gilovich, Griffin, & Kahneman, eds.), Cambridge University Press.
- Luchins, A. S. (1942). "Mechanization in Problem Solving: The Effect of Einstellung." *Psychological Monographs*, 54(6), 1–95.
- Mitroff, I. I., & Kilmann, R. H. (1978). *Methodological Approaches to Social Sciences*. Jossey-Bass. (Type III error.)
- Raymond, E. S. (compiler). *The Jargon File* — entry on the XY problem. (Folk-canonical formulation.)
