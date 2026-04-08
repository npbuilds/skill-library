# Agentic Researcher — Quick Reference


## When to Use (vs. Standard Spelunker Pipeline)

| Question Shape | Route To |
|---------------|----------|
| "Is X true?" / "What caused X?" | claim-decomposer → source-triangulator |
| "What's the best approach to X?" / "How should we design X?" | **agentic-researcher** |
| "What are the options for X?" / "Optimize X" | **agentic-researcher** |

## Quick Reference

| Mode | Initial Candidates | Iterations | Max Evaluated |
|------|-------------------|------------|---------------|
| quick | 3 | 0 | 3 |
| standard | 4 | 1 | 8 |
| deep | 5 | 2-3 | 15 |

## Error Handling

| Failure | Response |
|---------|----------|
| Can't define evaluation criteria | Ask user: "What does 'good' mean here? What are you optimizing for?" |
| All candidates score equally | Criteria aren't discriminating. Suggest more specific criteria. |
| No evidence for any candidate | Tag entire brief as Speculative. Note what would help. |
| User constraints are contradictory | Surface the contradiction. Ask which constraint to relax. |
| Solution space too large | Ask user to constrain scope. Suggest 2-3 scoping options. |
| Single candidate dominates | Adversarial check: search for "[candidate] problems". Flag lack of trade-offs as suspicious if it survives. |

## Output Format

```
AGENTIC RESEARCH BRIEF
══════════════════════
Question: [restated question]
Mode: [quick / standard / deep] | Iterations: [N]

RECOMMENDATION
──────────────
[Top candidate] — Confidence: [tag]
[2-3 sentence summary]

TRADE-OFF MAP
─────────────
[Candidate 1]: Best at [X], sacrifices [Y]
[Candidate 2]: Best at [Z], sacrifices [W]

EVALUATION MATRIX
─────────────────
[Weighted scoring matrix]

SENSITIVITY
───────────
[Decisive criteria; what would flip the recommendation]

EVIDENCE QUALITY
────────────────
[Confidence tags per candidate; evidence gaps that could change ranking]

NEXT STEPS
──────────
[What to verify before committing]
```
