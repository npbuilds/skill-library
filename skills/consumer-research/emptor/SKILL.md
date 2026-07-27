---
name: emptor
description: >
  Orchestrates rigorous consumer purchase research from need to verified recommendation.
  Use when the user wants to buy something and asks "what's the best X", wants product
  options compared, or needs purchase claims verified — any consumer buying decision across
  electronics, appliances, software, services, and beyond. Runs requirements elicitation
  before any prices are seen, searches only trusted sources, verifies finalists, scores them
  on the user's own weighted criteria, and journals the outcome for calibration.
metadata:
  author: nirav
  version: "1.0"
type: orchestrator
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent WebSearch WebFetch
---

# Emptor — The Buyer's Agent

*Caveat emptor* — buyer beware. Consumer review territory is adversarial: affiliate capture, fake reviews at platform scale, zombie products in 18-34% of AI recommendations, merchants optimizing content to manipulate LLMs. Emptor is the buyer's own agent: zero monetization, full decision-trail transparency, every claim cited and confidence-tagged.

Evidence base: `research/consumer-research-landscape-2026.md`. Confidence tags per `../../research/spelunker/references/confidence-framework.md`.

## Guiding Principles

1. **Requirements before market exposure.** No search, no prices, until the spec is signed off (anchoring defense).
2. **Trusted sources only.** Site-scoped Tier 1-2 searches per `source-trust-atlas`; merchant and affiliate content is claims, never evidence.
3. **Verify before you rank.** No finalist enters the matrix without availability, claim, and review-authenticity checks.
4. **Show the whole trail.** Weights, scores, sensitivity, and evidence are all in the brief — "best" is auditable, not asserted.
5. **Satisficing is a valid exit.** When several options clear every must-have robustly, say so; do not manufacture a winner.
6. **Close the loop.** Every brief is journaled; purchases and 30-day verdicts calibrate future confidence.

## Depth Modes

| Signal | Mode | Effect |
|---|---|---|
| Low-stakes (≲$50) or "just give me a quick take" | `quick` | 3-question elicitation, 3 finalists, forensics on top pick only, no sensitivity |
| Default | `standard` | Full pipeline below |
| High-stakes (≳$500), safety-relevant, or "I need to be sure" | `deep` | Forensics + full verification on all finalists, `bias-and-funding-tracer` on key sources, agentic-researcher mutate loop |

## Phases

| # | Phase | Route to | Contract |
|---|---|---|---|
| 0 | Recall | `decision-journal` (recall) | Prior briefs, pending check-ins, preference priors for this category. Cold start = silent no-op |
| 1 | Elicit | `needs-elicitor` | Signed-off requirements spec; **no WebSearch/WebFetch may run before sign-off** |
| 2 | Source plan | `source-trust-atlas` | Category → source chain, site-scoped query templates, decay thresholds |
| 3 | Scan | inline | 15-50 candidates from Tier 1-2 only; thin Tier 1 coverage → widen to Tier 2 and lower the confidence ceiling one notch |
| 4 | Eliminate | inline | Elimination-by-aspects on must-haves in spec order → 3-6 finalists; record what each elimination removed and why |
| 5 | Verify | `product-verifier` + `review-forensics` | Per finalist: claims (via `source-triangulator`), availability, recalls, merchant trust, review authenticity. Must-have `fail` eliminates; replacements come from Phase 4's survivors |
| 6 | Evaluate | `agentic-researcher` (Phases 3-5) | Pass the spec's weighted criteria + verified finalists; receive matrix, trade-offs, ±20% sensitivity verbatim. No re-scoring downstream |
| 7 | Brief | `recommendation-brief` | EMPTOR BRIEF per contract, pre-flight audited, `CRS-` ID. Exemplar: `references/quick-reference.md` |
| 8 | Journal | `decision-journal` (persist_brief) | JSONL line + `research/consumer-briefs/CRS-<id>.md` + vault mirror when reachable |

## Delegation Protocol

Pass downstream, in order: the signed requirements spec (frozen), the atlas source plan, accumulated verification results, and the depth mode. Upstream changes (a must-have proves unsatisfiable, budget proves unrealistic) return to Phase 1 explicitly — the spec is never silently edited mid-run.

## Synthesis

`recommendation-brief` owns the final synthesis. Emptor enforces the confidence ceilings: sensitivity-unstable → co-leads, at most Likely; winner with an unverifiable must-have → at most Speculative; Tier 1 sources disagreeing on a deciding criterion → Contested, both sides shown. When ≥2 finalists clear every must-have and survive sensitivity, the SATISFICING NOTE is mandatory — especially for maximizer-leaning buyers.

## Failure Recovery

| Failure | Response |
|---|---|
| No candidate passes all must-haves | "No qualified pick" brief: nearest misses + which constraint to relax; return to Phase 1 if user relaxes |
| Tier 1-2 coverage absent for the category (e.g., services) | Proceed on Tier 3 with atlas astroturf protocol; cap brief at Speculative; say so up front |
| Sources contradict on a deciding criterion | Contested — present both with tier + freshness comparison; do not average |
| Paywalled Tier 1 evidence on a critical claim | `paywall-strategist` before Unverifiable |
| Price/availability shifts mid-run | Re-check at brief time; all such facts date-stamped |
| User wants to skip elicitation | Run `quick` elicitation anyway (3 questions); explain the anchoring rationale in one sentence |

## Scope Boundaries

**Emptor handles:** consumer purchase decisions — products, software, services; comparison, verification, recommendation, and outcome tracking.
**Emptor does not:** complete purchases, track prices continuously (no daemons; check-ins are pull-based via `/purchase-review`), give financial/medical/legal advice, or replace hands-on trial for fit-dependent goods (it says when in-person verification is the right next step).

## Related Skills

- Children: `needs-elicitor`, `source-trust-atlas`, `review-forensics`, `product-verifier`, `recommendation-brief`, `decision-journal`.
- Reused: `agentic-researcher` (evaluation engine), `source-triangulator`, `paywall-strategist`, `bias-and-funding-tracer`, `vault-writer`/`vault-reader`.
- `spelunker` routes consumer purchase questions here; investigative non-purchase questions go the other way.

## Learn Block

After emptor, learn `spelunker` — the same epistemic discipline applied to questions that aren't purchases.
