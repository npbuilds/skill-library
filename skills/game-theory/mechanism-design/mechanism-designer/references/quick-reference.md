# Mechanism Designer — Quick Reference


## Quick Reference

| Dimension | Options | Implications |
|-----------|---------|-------------|
| **Transfers** | Money available / restricted / none | With money → auctions, VCG. Without → matching, voting |
| **Items** | Single / multiple / combinatorial | Multiple items → combinatorial complexity, complementarities |
| **Agents** | Symmetric / asymmetric | Asymmetric → standard results may not apply |
| **Values** | Private / common / interdependent | Common values → winner's curse, information aggregation matters |
| **Repetition** | One-shot / repeated | Repeated → dynamic mechanism design, renegotiation |
| **Verification** | Outcomes verifiable / not | Unverifiable → moral hazard, contract theory |

## Formula / Pseudocode

```
## Mechanism Design: [Problem Name]

### Problem
[What's being allocated, to whom, under what constraints]

### Design Objectives
[Priority-ordered list of goals]

### Impossibility Constraints
[Which theorems limit what's achievable]

### Proposed Mechanism
[Full specification — elicitation, allocation, payments]

### Incentive Analysis
[IC, IR, efficiency, fairness properties with justification]

### Practical Considerations
[Computational, communicational, robustness, simplicity]

### Alternatives Considered
[Other mechanism classes and why the proposed one was chosen]
```
