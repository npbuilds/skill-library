# Synthesis Templates — Output Formats

The standard output format for Spelunker research briefs. Every brief follows this structure for consistency and readability.

## Full Research Brief Template

```
RESEARCH BRIEF
══════════════════════════════════════════════

Question: [The restated research question]
Depth: [quick / standard / deep]
Date: [Date of investigation]
Claims investigated: [N] | Sources evaluated: [N]

──────────────────────────────────────────────
KEY FINDINGS
──────────────────────────────────────────────

[Confidence Tag] Finding 1
  [1-2 sentence plain-language summary]

[Confidence Tag] Finding 2
  [1-2 sentence plain-language summary]

...

Overall confidence: [High / Moderate / Low / Insufficient evidence]
[1 sentence explaining why]

──────────────────────────────────────────────
DETAILED FINDINGS
──────────────────────────────────────────────

### Finding 1: [Finding title]

Confidence: [Tag] — because [specific reasoning with evidence counts]

Evidence:
  - [Source A, Tier N]: [What it says, how it supports/contradicts]
  - [Source B, Tier N]: [What it says, how it supports/contradicts]
  Independence: [verified/not verified] — [explanation]

Adversarial check: [What counterevidence was searched for, what was found]

### Finding 2: [Finding title]
...

──────────────────────────────────────────────
EVIDENCE MAP
──────────────────────────────────────────────

[Provenance chains showing how findings trace back to sources]

Finding → Atomic Claim → Evidence → Source

Example:
  "Creatine is safe for long-term use in healthy adults"
    ← Claim #2: Creatine monohydrate is safe at 5g/day for 1+ years
      ← 3 independent Tier 1 sources agree
      ← Independence verified: different research groups
      ← Adversarial check: no credible contradicting evidence
    → Confidence: Confirmed

[Include one chain per key finding. Omit for quick mode.]

──────────────────────────────────────────────
GAPS & LIMITATIONS
──────────────────────────────────────────────

What wasn't found:
  - [Gap 1]: [What's missing and why it matters]
  - [Gap 2]: [What's missing and why it matters]

Access limitations:
  - [Tool/source that was inaccessible and what it might have contained]

What would resolve the gaps:
  - [Specific action, database, or expert that would fill the gap]

──────────────────────────────────────────────
CONFIDENCE SUMMARY
──────────────────────────────────────────────

[N] Confirmed | [N] Likely | [N] Speculative | [N] Contested | [N] Unverifiable

Critical dependencies:
  [If any — which findings depend on which premises]

Adversarial assessment:
  [Summary of self-check results]

──────────────────────────────────────────────
SOURCES
──────────────────────────────────────────────

[Ranked by relevance and authority tier]

1. [Source title] — [URL/citation] — Tier [N] — Used for: [which findings]
2. ...

──────────────────────────────────────────────
NEXT STEPS (if applicable)
──────────────────────────────────────────────

To increase confidence:
  - [Specific follow-up investigation that would upgrade Speculative → Likely or Likely → Confirmed]

Unresolved questions:
  - [Questions that emerged during research but were out of scope]
```

## Quick Mode Abbreviated Template

For quick-depth investigations, use a shorter format:

```
QUICK RESEARCH: [Question]
════════════════════════════

[Confidence Tag] [Finding — 1-2 sentences]
  Sources: [N] ([brief source list])

[Confidence Tag] [Finding — 1-2 sentences]
  Sources: [N] ([brief source list])

Gaps:
  - Not checked: [Claims or aspects that were skipped]
  - Not accessible: [Sources behind paywalls or tool limitations, if any]
  - Adversarial check: skipped (quick mode)

Note: Quick-mode research. Run at standard/deep depth for triangulation and adversarial checking.
```

## Contested Claim Special Format

When a claim is tagged Contested, use this expanded format to present both sides fairly:

```
CONTESTED: [Claim text]

Position A: [What one side claims]
  Evidence: [Sources supporting this position, with tiers]
  Strongest argument: [The best case for this position]

Position B: [What the other side claims]
  Evidence: [Sources supporting this position, with tiers]
  Strongest argument: [The best case for this position]

Evidence quality comparison:
  Position A: [N] Tier 1 sources, [N] Tier 2 sources
  Position B: [N] Tier 1 sources, [N] Tier 2 sources

What would resolve this:
  [Specific study type, data point, or methodological question]

Note: Spelunker does not pick a winner in contested claims. The evidence is presented for the user to evaluate.
```

## Formatting Rules

1. **Confidence tags always lead.** The first thing a reader sees for each finding is the confidence level.
2. **Because-clauses are mandatory.** Every confidence tag has an explanation. "Confirmed" alone is not acceptable — "Confirmed — 3 independent Tier 1 sources agree, no contradicting evidence found" is.
3. **Gaps come before sources.** The reader should know what's missing before they see what was found.
4. **Sources are ranked, not just listed.** Most relevant and authoritative first.
5. **Next steps are actionable.** Not "do more research" but "search [specific database] for [specific thing]."
6. **Plain language in Key Findings, precision in Detailed Findings.** The Key Findings section is for busy readers. The Detailed Findings section is for skeptical readers.
