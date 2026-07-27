---
name: needs-elicitor
description: >
  Interviews a buyer before any product research happens: jobs-to-be-done framing, MoSCoW
  must-haves, deal-breakers, and a budget locked before any price is seen. Use when starting
  a purchase decision and the real requirements are not yet pinned down — emptor's elicit
  phase, or standalone when someone says "help me figure out what I actually need". Produces
  a signed-off requirements spec with weighted criteria; performs no web searching itself.
metadata:
  author: nirav
  version: "1.0"
type: action
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Needs Elicitor — The Interviewer

Action skill: turn "I need a robot vacuum" into an auditable requirements spec — before a single price or product page is seen. The decision-science evidence is blunt: anchoring (first price seen sways ~70% of buyers), spec-sheet seduction, and social proof all enter through premature exposure to the market. This skill is the bias gate.

## Description

Elicits the buyer's actual job, hard constraints, and priorities, then locks them. Downstream phases (scan, eliminate, evaluate) treat the spec as frozen; changing it means returning here explicitly. The spec's weighted criteria feed `agentic-researcher`'s evaluation matrix directly.

## Input

| Parameter | Required | Notes |
|---|---|---|
| `request` | yes | The raw purchase intent ("best X for Y") |
| `priors` | no | Preference profile + prior briefs from `decision-journal` Phase-0 recall |
| `depth` | no | `quick` (3 questions, low-stakes purchases) / `standard` (full interview, default) |

## Process

1. **Frame the job (JTBD).** Ask what situation the purchase should change — functional job (the task), emotional job (how they want to feel), social job (if any). A stand mixer's job might be "weekly bread without arm fatigue", not "600W motor".
2. **Capture constraints (MoSCoW).** Must-haves (pass/fail — budget cap, size limits, compatibility, safety), should-haves, could-haves, won't-haves. Challenge each "must": *"If an otherwise-perfect option lacked this, is it really out?"* — the classic failure is conflating strongly-wanted with required.
3. **Lock the budget before price exposure.** Elicit the cap (and stretch tolerance, if any) from the buyer's situation — never from market prices. Record `locked_before_prices: true`. No WebSearch/WebFetch happens in this skill, by design.
4. **Weight the soft criteria.** Rank should/could-haves by importance; assign weights summing to 1.0 via direct assignment or quick pairwise comparison. Confirm aloud: "reliability 0.3, pickup performance 0.35 — sound right?"
5. **Read the buyer's style.** Satisficer ("good enough, decided fast") vs maximizer ("must be the best") — one question suffices. Maximizer-leaning buyers get the satisficing exit emphasized later (maximizers are measurably less satisfied post-purchase).
6. **Apply priors with consent.** If the preference profile suggests recurring must-haves or weight priors, propose them — never silently apply: "last time you weighted reliability heavily — still true?"
7. **Sign off.** Present the spec; the buyer confirms or amends. Only a confirmed spec unlocks the search phases.

In `quick` mode, compress to: the functional job, must-haves + budget, top-2 priorities.

## Output

```yaml
requirements_spec:
  job: {functional: "...", emotional: "...", social: null}
  must_haves: ["<= $400", "..."]        # pass/fail, elimination order = list order
  wont_haves: ["..."]
  weighted_criteria:                     # soft criteria, weights sum to 1.0
    - {criterion: "...", weight: 0.35, rationale: "..."}
  budget: {cap: 400, currency: USD, stretch: null, locked_before_prices: true}
  buyer_style: satisficer | maximizer | mixed
  priors_applied: ["..."]                # from profile, confirmed by user
  signed_off: true
```

## Error Handling

| Failure | Response |
|---|---|
| Contradictory constraints (budget can't satisfy must-haves — discovered later) | Downstream returns here; relax one constraint explicitly, never silently |
| Buyer says "just tell me the best" | Run `quick` mode anyway — three questions beat zero; explain why in one sentence |
| Buyer anchors on a product they've seen | Record it as a candidate, but elicit the job and budget as if it didn't exist |

## Scope Boundaries

**Handles:** requirements, constraints, weights, budget lock.
**Does not:** search the web, name candidate products, or estimate market prices — that contaminates the anchor-free elicitation.

## Related Skills

- Output feeds `emptor` Phases 3-6 and `agentic-researcher`'s criteria framing; priors come from `decision-journal`.

## Learn Block

Next, learn `source-trust-atlas` — where the now-specified research should actually look.
