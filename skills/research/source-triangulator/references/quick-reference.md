# Source Triangulator — Quick Reference


## Quick Reference

| Mode | Direct Queries | Lateral Queries | Domain-Specific | Adversarial |
|------|---------------|-----------------|-----------------|-------------|
| quick | 1 | 0 | 0-1 | 0 |
| standard | 2 | 1 | 1 | 1 |
| deep | 3 | 2 | 2 | 2 |

## Quick Reference

| Claim Type | Primary Approach | Secondary Approach |
|-----------|-----------------|-------------------|
| Factual | Direct search for the specific fact | Authority search (who would have this data?) |
| Causal | Search for studies/experiments testing causation | Search for mechanism explanations |
| Comparative | Search for head-to-head comparisons, benchmarks | Search each side independently |
| Predictive | Search for forecasts, models, expert predictions | Search for base rates and historical precedents |
| Definitional | Search authoritative definitions (standards bodies, textbooks) | Search for usage patterns |
| Existential | Search for direct records or documentation | Search for absence evidence |
| Evaluative | Search for established criteria, standards, expert assessments | Search for outcome-based evidence and alternative evaluations |

## Formula / Pseudocode

```
EVIDENCE MAP: [Claim text]
─────────────────────────────
Supporting (agree with claim):
  Source A [Tier 1] — [key finding]
  Source B [Tier 2] — [key finding]
  Independence: A and B are independent ✓ / share upstream ✗

Contradicting (disagree with claim):
  Source C [Tier 1] — [contradicting finding]
  Independence from supporting sources: ✓

Tangential (related but don't directly address):
  Source D [Tier 2] — [what it says and why it's relevant]

Not found:
  [What would constitute strong evidence but could not be located]
```
