---
name: recommendation-brief
description: >
  Assembles the final EMPTOR BRIEF for a purchase decision and runs its pre-flight audit:
  ranked pick with confidence-and-because clauses, trade-off map, evaluation matrix,
  sensitivity, forensics flags, trust-checked merchants, freshness stamps, and the feedback
  footer. Use during emptor's brief phase after evaluation completes, or standalone to
  re-render an existing evaluation into the brief contract. Rejects and regenerates rather
  than delivering an unauditable brief.
metadata:
  author: nirav
  version: "1.0"
type: action
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Recommendation Brief — The Closer

Action skill: the output contract of the consumer-research suite. Commercial AI shopping tools have a documented explainability void — users can't see why X beat Y. The EMPTOR BRIEF is the inverse: every claim cited, every confidence tagged with a because-clause, every weight visible, and the brief declares its own expiry.

## Description

Consumes the evaluation matrix (produced by `agentic-researcher` — verbatim, no re-scoring), verification and forensics results, and the requirements spec; renders the graded brief; runs the pre-flight audit; emits the `CRS-YYYYMMDD-<slug>` brief ID that `/calibrate`, `/purchase-log`, and `/purchase-review` key on. Confidence tags follow `skills/research/spelunker/references/confidence-framework.md`.

## Input

| Parameter | Required | Notes |
|---|---|---|
| `requirements_spec` | yes | From `needs-elicitor` (signed off) |
| `evaluation` | yes | Matrix + trade-offs + sensitivity from `agentic-researcher` |
| `verification` | yes | Per-finalist blocks from `product-verifier` |
| `forensics` | yes | Per-finalist verdicts from `review-forensics` |
| `sources` | yes | Numbered source list with tiers and dates |

## Process

1. **Generate the brief ID**: `CRS-YYYYMMDD-<6-char-slug>`.
2. **Set TOP PICK CONFIDENCE** from the weakest load-bearing link: evidence quality of the winning finalist, sensitivity stability, and verification status. Ceiling rules — sensitivity-unstable → at most Likely (and present co-leads); any must-have `unverifiable` on the winner → at most Speculative; Tier 1 disagreement on a deciding criterion → Contested, present both.
3. **Render sections** in contract order (below). RUNNERS-UP each get a "choose this instead if…" condition. SATISFICING NOTE appears whenever ≥2 finalists clear every must-have and survive sensitivity — mandatory phrasing for maximizer-leaning buyers.
4. **Stamp freshness**: every price/availability fact carries its check date; GAPS & FRESHNESS states the date the brief should be considered stale (earliest decaying source per atlas rules).
5. **Run the pre-flight audit.** Reject and regenerate once on any failure; second failure → fix in place before delivery. Checks:
   - TOP PICK CONFIDENCE on line 2; Brief ID on line 3.
   - Every empirical claim has `[N]` or `[no source]`; every tag has a because-clause.
   - Every finalist has an availability verdict; every WHERE TO BUY merchant has a trust verdict.
   - SOURCES numbered with Tier and Used-for; no orphan/unused citation numbers.
   - GAPS & FRESHNESS non-empty; footer verbatim.
6. **Deliver**, then hand to `decision-journal` for persistence.

## Output

```
RECOMMENDATION BRIEF
TOP PICK CONFIDENCE: <Confirmed|Likely|Speculative|Contested>
Brief ID: CRS-YYYYMMDD-<slug>
<One-paragraph verdict with [N] citations.>

REQUIREMENTS SNAPSHOT      — job, must-haves, weights, budget (locked before price exposure: yes/no)
TOP PICK                   — product (exact SKU), price @ date, why; Confidence: [Tag] because …
RUNNERS-UP                 — each: "choose this instead if …"
TRADE-OFF MAP              — per finalist: best at X, sacrifices Y
EVALUATION MATRIX          — weighted scores, weights shown (verbatim from evaluation)
SENSITIVITY                — stable/unstable; which weight shift flips the pick
VERIFICATION & AUTHENTICITY — availability per finalist (dated), recalls, forensics verdicts
WHERE TO BUY               — merchant + trust verdict + price + return policy, all dated
GAPS & FRESHNESS           — unverified claims, missing data; "stale after: <date>"
SOURCES                    — numbered; Tier N; date; Used for: …
SATISFICING NOTE           — when applicable
NEXT STEPS                 — what to verify in person / before checkout

─────────────────────────────────────
Was this brief useful? Reply `/feedback emptor <1-5> [optional notes]` to log.
Brief ID: CRS-... · Bought something? `/purchase-log CRS-... <product> [price] [merchant]` · 30 days later: `/purchase-review CRS-... <1-5>`
```

## Error Handling

| Failure | Response |
|---|---|
| Evaluation matrix missing or partially scored | Return to caller — do not improvise scores |
| Winner's evidence is all Tier 3 | Cap confidence at Speculative; say so in the verdict paragraph |
| No finalist passes all must-haves | Deliver a "no qualified pick" brief: closest options + which constraint to relax |

## Scope Boundaries

**Handles:** rendering, auditing, and grading the final brief.
**Does not:** score candidates, verify facts, or persist anything (that's `decision-journal`).

## Related Skills

- Consumes `agentic-researcher` output verbatim; cites the spelunker confidence framework; hands off to `decision-journal`.

## Learn Block

Next, learn `decision-journal` — where the brief, the decision, and the 30-day verdict live on.
