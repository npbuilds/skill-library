# Investment Memo Writer — Quick Reference


## Input

| Parameter | Source | Required? |
|---|---|---|
| Completed diligence scorecard | diligence-scorecard | Yes |
| Asset name and company | User | Yes |
| Deal terms (if available) | User / deal-economics | Recommended |
| Portfolio context (if available) | portfolio-analyzer | Optional |
| Investment thesis or hypothesis | User | Recommended |

## Quick Reference

| # | Risk | Severity | Probability | Mitigant | Residual Risk |
|---|------|----------|-------------|----------|---------------|
| 1 | [risk] | [H/M/L] | [H/M/L] | [mitigant or "Unmitigated"] | [assessment] |
| 2 | [risk] | [H/M/L] | [H/M/L] | [mitigant] | [assessment] |

## Error Handling

| Scenario | Response |
|---|---|
| Scorecard not available | Cannot proceed — the memo requires scorecard as input. Generate scorecard first. |
| Missing pillar data (e.g., no team assessment) | Write the section with available information; flag gaps explicitly as "[Data not available — requires primary diligence]" |
| Conflicting signals across pillars | Present both sides transparently; do not resolve contradictions by ignoring one side |
| Deal terms not finalized | Write the memo with placeholder terms; note sensitivity of recommendation to final terms |

## Formula / Pseudocode

```
INVESTMENT MEMORANDUM — [Company / Asset Name]
Date: [date]
Author: [analyst]
Recommendation: [Strong Buy / Buy / Hold / Pass]

TABLE OF CONTENTS
1.  Executive Summary
2.  Investment Thesis
3.  Science Overview
4.  Clinical Development Plan
5.  Regulatory Strategy
6.  Competitive Landscape
7.  Commercial Opportunity
8.  Financial Model Summary
9.  Key Risks and Mitigants
10. Team Assessment
11. Deal Terms
12. Recommendation
```

## Formula / Pseudocode

```
WHAT HAS TO GO RIGHT:
1. [Clinical milestone] — [probability and timeline]
2. [Regulatory milestone] — [pathway and precedent]
3. [Commercial milestone] — [market share assumption and basis]

WHAT COULD GO WRONG:
1. [Key clinical risk] — [impact if realized]
2. [Key competitive risk] — [impact if realized]
3. [Key execution risk] — [impact if realized]
```

## Formula / Pseudocode

```
| # | Risk | Severity | Probability | Mitigant | Residual Risk |
|---|------|----------|-------------|----------|---------------|
| 1 | [risk] | [H/M/L] | [H/M/L] | [mitigant or "Unmitigated"] | [assessment] |
| 2 | [risk] | [H/M/L] | [H/M/L] | [mitigant] | [assessment] |
```

## Formula / Pseudocode

```
MEMO QUALITY CHECKLIST:
[ ] Executive summary is self-contained and <300 words
[ ] Thesis has explicit "what has to go right" / "what could go wrong"
[ ] Every quantitative claim has a stated source or assumption
[ ] Risk table includes mitigants for all identified risks
[ ] Recommendation is clear and actionable
[ ] Scorecard pillar scores are consistent with narrative
[ ] No unsubstantiated superlatives ("best-in-class" without data)
[ ] Formatting is consistent (headers, tables, numbering)
```
