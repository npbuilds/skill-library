---
name: review-forensics
description: >
  Scores the authenticity of a product's review corpus using a five-signal ensemble
  (velocity, verified-purchase ratio, rating distribution, account patterns, cross-product
  repetition). Use when evaluating whether crowd reviews for a specific product can be
  trusted as evidence — typically during emptor's verify phase, or standalone when the user
  asks "are these reviews fake?". Returns a per-product authenticity verdict, never a guess:
  signals that cannot be checked are reported as unchecked.
metadata:
  author: nirav
  version: "1.0"
type: action
compatibility: Designed for Claude Code
allowed-tools: Read WebSearch WebFetch
---

# Review Forensics — The Authenticator

Action skill: given a product and its review corpus (Amazon, Google, Yelp, app stores…), produce an auditable authenticity verdict. Fills the gap left by Fakespot's shutdown (July 2025) using the ensemble approach the detection literature supports — no single heuristic suffices.

## Description

Fake reviews operate at platform scale (Amazon removed 275M in 2024; AI-generated reviews grow ~80% month-over-month and beat human detection). Emptor therefore never weights crowd ratings as evidence until this skill has scored them. Thresholds and scoring rubric live in `references/detection-heuristics.md`.

## Input

From the caller (usually `emptor` Phase 5, or the user directly):

| Parameter | Required | Notes |
|---|---|---|
| `product` | yes | Name + platform listing(s) to inspect |
| `review_data` | no | Anything already fetched (rating histogram, counts, dates, sample reviews); the skill fetches what it can otherwise |
| `depth` | no | `quick` (signals retrievable in ≤2 fetches) / `standard` (all five signals attempted, default) |

## Process

1. **Gather observables.** For each listing: total review count, rating histogram, review dates (velocity), verified-purchase proportion if displayed, a sample of recent reviews with account links where visible.
2. **Score each signal** against the thresholds in `references/detection-heuristics.md`:
   - velocity spikes; verified-purchase ratio; rating-distribution shape (natural J-curve vs manufactured peaks); reviewer-account patterns; cross-product/template repetition. Linguistic checks use perplexity-style cues (hyper-coherent, emotionally flat, template phrasing) — never generic "AI detector" verdicts.
3. **Mark unobtainable signals as `unchecked`** — a platform that hides verified status yields `unchecked`, not a default pass. Never infer a signal you could not observe.
4. **Compose the verdict** by counting flagged signals among those actually checked (rubric in the reference). Strong-flag shortcuts (e.g., near-certain bought-review patterns) can override to `suspect` directly.
5. **State the consequence**: how much weight the caller may put on this product's crowd ratings, and what (if anything) would upgrade the verdict.

## Output

```
REVIEW FORENSICS — <product>
Verdict: clean | mixed | suspect | unverifiable
Signals checked: <n>/5
  velocity:            ok | flag | unchecked — <one-line observation>
  verified ratio:      ok | flag | unchecked — <value if known>
  rating distribution: ok | flag | unchecked — <shape note>
  account patterns:    ok | flag | unchecked — <note>
  cross-product:       ok | flag | unchecked — <note>
Consequence: <how to weight crowd ratings for this product>
Upgrade path: <what evidence would change the verdict>
```

Verdict semantics: `clean` (0 flags, ≥3 signals checked), `mixed` (1 flag), `suspect` (≥2 flags or one strong flag), `unverifiable` (<3 signals checkable — crowd ratings carry no evidential weight).

## Error Handling

| Failure | Response |
|---|---|
| Platform blocks fetching | Mark affected signals `unchecked`; verdict ceiling is `mixed` |
| Review corpus tiny (<25 reviews) | Report `unverifiable` — too little signal either way |
| Caller supplies only a star average | Refuse to score; request histogram/dates or fetch them |

## Scope Boundaries

**Handles:** authenticity of a specific product's review corpus.
**Does not:** judge the product itself (that's `product-verifier` + evaluation), rank sources (that's `source-trust-atlas`), or detect astroturfing in forum threads (atlas protocol covers that).

## Related Skills

- Consumes `source-trust-atlas` tier context; feeds verdicts into `emptor` Phase 5 and the VERIFICATION & AUTHENTICITY section of the brief.

## Learn Block

Next, learn `product-verifier` — claims, availability, and recalls for the same finalists this skill screens.
