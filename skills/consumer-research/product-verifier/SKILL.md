---
name: product-verifier
description: >
  Verifies a shortlisted product's hard facts before it can be recommended: marketing claims
  against independent test data, current availability and discontinuation status, recall and
  reliability history, and merchant trustworthiness for purchase links. Use during emptor's
  verify phase on each finalist, or standalone when the user asks "is this product's claim
  actually true?" or "is this store legit?".
metadata:
  author: nirav
  version: "1.0"
type: action
compatibility: Designed for Claude Code
allowed-tools: Read WebSearch WebFetch Agent
---

# Product Verifier — The Inspector

Action skill: per-finalist hard checks. AI shopping assistants demonstrably skip these — 18-34% of their recommendations point to discontinued "zombie" products, specs get hallucinated, and scam merchants poison results with cloned listings. No finalist reaches emptor's evaluation matrix unverified.

## Description

Four checks per finalist: claim verification, availability, safety/reliability history, merchant trust. Claim verification reuses `source-triangulator` (research domain) at quick depth — standard depth for claims that decide must-have compliance. Source weighting follows `source-trust-atlas`; paywalled Tier 1 evidence on critical claims routes through `paywall-strategist` before being declared unverifiable.

## Input

| Parameter | Required | Notes |
|---|---|---|
| `finalist` | yes | Product name + exact model/SKU if known |
| `claims_to_verify` | yes | The spec/marketing claims that matter to the requirements spec (esp. must-have compliance) |
| `depth` | no | quick / standard (default) / deep |

## Process

1. **Pin the exact SKU.** Model-year revisions and regional variants invalidate reviews silently; record which variant every piece of evidence applies to.
2. **Verify claims.** For each claim: route to `source-triangulator` with the claim, type, and the atlas-derived source chain. Manufacturer copy is the claim, never the evidence. Must-have-deciding claims get standard depth and a confidence tag each.
3. **Check availability.** Confirm the product is in production and purchasable today: manufacturer product page live, ≥2 reputable merchants stocking it, no "discontinued/replaced by" notices. Record status — `in production` / `discontinued (successor: X)` / `limited stock` / `unclear` — with a check date.
4. **Check safety & reliability history.** Recalls (CPSC/NHTSA/FDA as applicable), known failure modes from Tier 1 reliability data, firmware/support status for connected products, warranty terms.
5. **Trust-check purchase merchants.** For each where-to-buy candidate: domain age and reputation, marketplace seller vs first-party, return policy, price plausibility (a 40%-below-market price on a fresh domain is a scam signal), FTC/consumer-protection history. Verdict per merchant: `verified` / `caution` / `avoid`.
6. **Report** with one block per finalist; every fact date-stamped and cited.

## Output

```
PRODUCT VERIFICATION — <finalist> (<exact SKU>)
Claims:
  - "<claim>": Confirmed|Likely|Speculative|Contested|Unverifiable because <evidence + [N]>
Availability: <status> (checked <date>) — <evidence>
Safety/reliability: <recalls, failure modes, support status, or "none found — searched X, Y">
Merchants:
  - <merchant>: verified|caution|avoid — <reason>
Must-have compliance: pass | fail (<which must-have>) | unverifiable (<which>)
```

A finalist whose must-have compliance is `fail` is eliminated; `unverifiable` caps the brief's TOP PICK confidence at Speculative if that finalist wins.

## Error Handling

| Failure | Response |
|---|---|
| Spec claim only on manufacturer site | Tag Unverifiable-pending; try independent teardowns/tests before giving up |
| Availability unclear (regional, fluctuating) | Report `unclear` with what was checked; never assume in-stock |
| All merchants are marketplace third parties | Verdict ceiling `caution`; say why |
| Paywalled Tier 1 review decides a must-have | Route to `paywall-strategist` first |

## Scope Boundaries

**Handles:** facts about a specific product and its merchants.
**Does not:** score review authenticity (`review-forensics`), rank finalists (evaluation phase), or decide requirements (`needs-elicitor`).

## Related Skills

- Depends on `source-triangulator` and `source-trust-atlas`; verdicts feed emptor's VERIFICATION & AUTHENTICITY and WHERE TO BUY sections.

## Learn Block

Next, learn `recommendation-brief` — how verified evidence becomes an auditable recommendation.
