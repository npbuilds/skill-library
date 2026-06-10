# Answerability Tester — Quick Reference


## Quick Reference

| Outcome | Verdict |
|---|---|
| Evidence is namable AND obtainable in principle | Provisionally answerable; continue to Q3 |
| Evidence is namable but logically impossible | **Unanswerable in principle** — needs reformulation |
| No evidence type satisfies the question even in principle | **Values-question** masquerading as a fact-question |

## Quick Reference

| Outcome | Verdict |
|---|---|
| Evidence is accessible (data exists, can be collected, can be queried) | **Answerable** |
| Evidence exists but requires resources beyond the user's reach | **Hard-but-answerable** (downgrade scoring; consider reformulation to a tractable proxy) |
| Evidence is in principle obtainable but practically not in this user's context | **Hard-but-answerable** with note |

## Quick Reference

| Linguistic pattern | Likely Q2 verdict |
|---|---|
| "What if X had happened?" (counterfactual past) | Logically impossible — no evidence of an unrun history |
| "Will X happen?" (prediction about singular future event) | Possible only after the fact; provisional answers via base rates and reference classes |
| "Does Y truly feel Z?" (other minds, qualia) | Logically constrained — proxies only |
| "Is X the right thing to do?" (normative) | Values-question; not a fact-question |
| Moral/aesthetic adjectives applied to people without behavioral specifics ("CEOs are crazy", "founders are visionaries", "managers are toxic") | Values-question — the adjective is doing values work, not descriptive work. Push for behavioral specifics; if they're not forthcoming, route to values-excavator |
| "Is X effective for purpose Y?" (instrumental claim) | Possible — evidence of effectiveness is the evidence type |

## Verdicts and What to Do With Them

| Verdict | What it means | Re-state level recommendation |
|---|---|---|
| **Answerable** | Evidence exists and is accessible; statement is well-formed for empirical resolution | None — passes this axis |
| **Hard-but-answerable** | Possible but expensive; downgrade or use a proxy | L1 (rephrase to use the proxy) |
| **Unanswerable as posed** | Logically impossible to resolve as currently framed | L2 (decompose — there's a sub-question that IS answerable) |
| **Values-question** | Not a fact-question; resolution requires ethical/political commitment, not evidence | L3 (depth upgrade — call `values-excavator` cross-domain to surface the values explicitly) or L4 (user assist) |

## Failure Modes

| Failure | Response |
|---|---|
| Q1 returns multiple plausible evidence types | List all of them; the one with the best Q3 access wins |
| User insists on the original framing despite Values-question verdict | Surface the values explicitly via `values-excavator`; don't force-fit empirical framing |
| Evidence-evaluator returns inconclusive | Default to "Hard-but-answerable" with note; that's the honest verdict |
| Statement is partially answerable (some sub-claims answerable, others not) | Recommend decomposition via `claim-decomposer` (research) before continuing |
