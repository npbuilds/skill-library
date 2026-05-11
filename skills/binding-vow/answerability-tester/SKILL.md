---
name: answerability-tester
description: >
  Test whether a problem statement is answerable in principle: could any evidence resolve it?
  Coordinates with philosophy/epistemology/evidence-evaluator to assess what evidence type
  would resolve the question and whether such evidence exists or is accessible. Use in
  binding-vow's Phase 6 audit. Returns answerable/unanswerable status, the evidence pathway,
  or flags the statement as values-disguised-as-fact.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Answerability Tester — Could Any Evidence Resolve This?

A statement that no evidence could resolve isn't a problem statement; it's a values commitment, a definitional choice, or a circular claim wearing a problem-statement's clothes. Answerability is the precondition for everything downstream — there is no point auditing falsifiability or scope on a statement that fundamentally cannot be answered.

This skill coordinates with `evidence-evaluator` (philosophy/epistemology) for the evidence-quality assessment. The binding-vow contribution is the *framing* — translating problem-statement context into the evidence-type question that `evidence-evaluator` can answer.

## The Three Diagnostic Questions

### Q1 — What evidence would resolve this if observed?

Name the specific kind of observation, data, study, or demonstration that would settle the question. Be concrete: not "research," but "a randomized trial of N≥500 with X measured at Y intervals."

If you cannot name the evidence type, the statement is provisionally unanswerable. Try Q2 to see whether that's a framing issue or a deeper one.

### Q2 — Could that evidence exist in principle?

Sometimes the evidence type is namable but logically impossible to obtain (counterfactual histories, predictions about a singular event before it occurs, claims about subjective experiences of others).

| Outcome | Verdict |
|---|---|
| Evidence is namable AND obtainable in principle | Provisionally answerable; continue to Q3 |
| Evidence is namable but logically impossible | **Unanswerable in principle** — needs reformulation |
| No evidence type satisfies the question even in principle | **Values-question** masquerading as a fact-question |

### Q3 — Is that evidence accessible to the user?

Even when evidence is namable and possible in principle, practical access matters. A statement that requires a 10-year longitudinal study the user cannot fund is *technically* answerable but functionally not.

| Outcome | Verdict |
|---|---|
| Evidence is accessible (data exists, can be collected, can be queried) | **Answerable** |
| Evidence exists but requires resources beyond the user's reach | **Hard-but-answerable** (downgrade scoring; consider reformulation to a tractable proxy) |
| Evidence is in principle obtainable but practically not in this user's context | **Hard-but-answerable** with note |

## Coordination with `evidence-evaluator`

For the Q1 evidence-type assessment, call `evidence-evaluator` with:

- **Pass:** the candidate evidence type (from Q1), the kind of claim being made, the field/domain
- **Receive:** judgment on the evidence's epistemic weight if obtained; common confounders; comparable bodies of evidence

`evidence-evaluator` evaluates *strength* of evidence; this skill evaluates *answerability*. They are complementary: a question can be answerable (some evidence resolves it) but the available evidence weak (Q3 returns "Hard-but-answerable").

For the Q2 logical-possibility check, the determination is largely linguistic:

| Linguistic pattern | Likely Q2 verdict |
|---|---|
| "What if X had happened?" (counterfactual past) | Logically impossible — no evidence of an unrun history |
| "Will X happen?" (prediction about singular future event) | Possible only after the fact; provisional answers via base rates and reference classes |
| "Does Y truly feel Z?" (other minds, qualia) | Logically constrained — proxies only |
| "Is X the right thing to do?" (normative) | Values-question; not a fact-question |
| Moral/aesthetic adjectives applied to people without behavioral specifics ("CEOs are crazy", "founders are visionaries", "managers are toxic") | Values-question — the adjective is doing values work, not descriptive work. Push for behavioral specifics; if they're not forthcoming, route to values-excavator |
| "Is X effective for purpose Y?" (instrumental claim) | Possible — evidence of effectiveness is the evidence type |

## Process

1. **Read the statement.**
2. **Q1:** Name the evidence type that would resolve. If you can't, jump to Q2 directly.
3. **Q2:** Check logical possibility using the linguistic patterns above.
4. **If Q2 returns "logically impossible" or "values-question," halt** — return verdict immediately.
5. **Otherwise proceed to Q3:** assess accessibility. Optionally call `evidence-evaluator` for evidence-strength side-information.
6. **Produce output** in the structured format below.

## Output Format

```
ANSWERABILITY — [first 60 chars of statement...]
─────────────────────────────────────────────
Verdict: [Answerable | Hard-but-answerable | Unanswerable as posed | Values-question]
Evidence type (Q1): [the kind of evidence that would resolve, or "none nameable"]
Logical possibility (Q2): [possible | impossible | values-shaped]
Practical accessibility (Q3): [accessible | hard | unreachable | N/A]

If Unanswerable as posed:
  Reformulation suggestion: [a different question that IS answerable and gets at the same goal]

If Values-question:
  Underlying values: [what's being commitment-claimed disguised as fact]
  Reformulation: [the value claim made explicit]

If Hard-but-answerable:
  Tractable proxy: [a simpler question that's answerable and approximates the original]
```

## Verdicts and What to Do With Them

| Verdict | What it means | Re-state level recommendation |
|---|---|---|
| **Answerable** | Evidence exists and is accessible; statement is well-formed for empirical resolution | None — passes this axis |
| **Hard-but-answerable** | Possible but expensive; downgrade or use a proxy | L1 (rephrase to use the proxy) |
| **Unanswerable as posed** | Logically impossible to resolve as currently framed | L2 (decompose — there's a sub-question that IS answerable) |
| **Values-question** | Not a fact-question; resolution requires ethical/political commitment, not evidence | L3 (depth upgrade — call `values-excavator` cross-domain to surface the values explicitly) or L4 (user assist) |

## Output Contract for `six-eyes`

When called from Phase 6:

- Return verdict + evidence type + accessibility assessment
- Feed the answerability axis on `statement-grader` (axes 5)
- If verdict is "Values-question," set re-state level to L3 and recommend `values-excavator` (philosophy/ethics) as the next call

## Failure Modes

| Failure | Response |
|---|---|
| Q1 returns multiple plausible evidence types | List all of them; the one with the best Q3 access wins |
| User insists on the original framing despite Values-question verdict | Surface the values explicitly via `values-excavator`; don't force-fit empirical framing |
| Evidence-evaluator returns inconclusive | Default to "Hard-but-answerable" with note; that's the honest verdict |
| Statement is partially answerable (some sub-claims answerable, others not) | Recommend decomposition via `claim-decomposer` (research) before continuing |

## Connections

- `statement-grader` (binding-vow) — feeds the answerability axis
- `xy-detector` (binding-vow) — XY patterns often flag as "Hard-but-answerable" until Y is surfaced
- `evidence-evaluator` (philosophy/epistemology) — primary cross-domain call
- `values-excavator` (philosophy/ethics) — escalation path for Values-question verdicts
- `claim-decomposer` (research) — for partial-answerability cases

## Sources

- Popper, K. R. (1959). *The Logic of Scientific Discovery*. (Background on the empirical/non-empirical distinction.)
- Hume, D. (1739). *A Treatise of Human Nature*. (The is/ought distinction underlying values-vs-fact verdicts.)
- See [[kahneman-framing]] for attribute-substitution patterns where unanswerable questions get silently swapped for answerable ones.
