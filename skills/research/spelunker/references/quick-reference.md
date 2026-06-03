# Spelunker — Quick Reference

## Synthetic exemplar (grading contract)

_Minimal fake brief — not real research. Shows mandatory `CORE CLAIM CONFIDENCE` placement (second line under RESEARCH BRIEF), refutation stance on a false claim, and citation hygiene._

```
RESEARCH BRIEF
CORE CLAIM CONFIDENCE: Contested
Brief ID: SPK-20260603-exemplar
The claim that megadose vitamin C cures the common cold is false and not supported by credible evidence [1].

KEY FINDINGS
- Controlled trials show no meaningful cure effect; the claim is debunked [1].

DETAILED FINDINGS
Core claim — Confidence: Contested because multiple RCTs find no benefit and the claim is unsupported [1].

EVIDENCE MAP
- Claim ↔ Source 1 (Tier 1): no cure effect.

GAPS & LIMITATIONS
- No new primary trial was run for this exemplar.

CONFIDENCE SUMMARY
Confirmed: 0 · Likely: 0 · Speculative: 0 · Contested: 1 · Unverifiable: 0

SOURCES
1. Cochrane review (synthetic), Tier 1, Used for: null effect of vitamin C on colds.

NEXT STEPS
- N/A (synthetic exemplar).
```

## Depth Mode Selection Guide

| Signal | Mode | Rationale |
|--------|------|-----------|
| "Quick question", "just curious", single-fact lookup | `quick` | Low stakes, well-trodden ground |
| "Research this", "what does the evidence say", "help me understand" | `standard` | Genuine inquiry, deserves triangulation |
| "I need to be sure", "this is for a decision", "comprehensive analysis" | `deep` | High stakes, must be thorough |
| Early results show contradictions | Upgrade to `deep` | Contested territory requires full adversarial pass |
| Topic is politically or commercially charged | Upgrade to `deep` | Higher risk of biased sources |

## Immediate Responses

| Failure | Response | Reentry Point |
|---------|----------|---------------|
| No sources found for a claim | Tag as Unverifiable. State what was searched. | → Reentry Protocol below |
| All sources are low-quality | Tag as Speculative. Note the evidence quality gap. | → Reentry Protocol below |
| Sources contradict each other irreconcilably | Tag as Contested. Present both sides with evidence quality comparison. Do NOT pick a winner. | No reentry needed — Contested is a valid outcome |
| Tool access fails (rate limit, paywall, timeout) | Note the failure in Gaps. Explain what information might be behind the barrier. Continue with available sources. | → Reentry Protocol if the claim is critical |
| Question is too broad to research meaningfully | Return to Phase 1. Ask the user to narrow scope. Suggest specific sub-questions. | → Phase 1 |
| Decomposition produces 15+ atomic claims | Ask the user to prioritize. Investigate the top claims at full depth, remainder at `quick` depth. | → Phase 3 with prioritized subset |
