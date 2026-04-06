# Skill Evolutionist — Quick Reference


## Quick Reference

| Stage | Description | Typical Age | What It Needs |
|-------|------------|-------------|---------------|
| **Nascent** | Just built, untested in real use | 0-2 weeks | Usage and feedback — is the design right? |
| **Settling** | Being used, rough edges appearing | 2-8 weeks | Bug fixes, scope adjustments, missing edge cases |
| **Stable** | Working well, clear scope, reliable | 2-6 months | Monitoring for environmental changes |
| **Mature** | Battle-tested, well-connected, refined | 6+ months | Watch for staleness — success breeds complacency |
| **Stale** | Assumptions outdated, scope drifted, edges broken | Varies | Evaluate: evolve, split, or retire |

## Quick Reference

| Indicator | Signal | Example |
|-----------|--------|---------|
| **Capability gap** | AI can now do something the skill doesn't account for | Skill predates tool-use; still instructs manual workarounds |
| **Context shift** | Token limits, speed, or cost changed enough to alter approach | Skill budgets 500 tokens for a reference that could now be 5,000 |
| **Ecosystem change** | New tools, integrations, or platforms emerged | Skill doesn't know about MCP servers that provide its data |
| **Knowledge drift** | Domain knowledge has evolved | Investing skill references pre-2024 monetary policy assumptions |

## Quick Reference

| Indicator | Signal | Example |
|-----------|--------|---------|
| **Missing edges** | New related skills exist but no cross-references | Philosophy built an ethics domain; investing skills don't link to it |
| **Scope creep** | Skill tries to do what a newer specialist handles | Director still says "handle directly" for a question that now has a dedicated child |
| **Orphan risk** | Skills that depended on this one have been rewritten | Referenced-by list is stale |
| **Duplicate coverage** | Two skills now cover the same territory | One should be retired or merged |

## Quick Reference

| Indicator | Signal | Example |
|-----------|--------|---------|
| **Thin references** | No reference files where they'd help | Action skill with complex taxonomy but no reference doc |
| **Vague routing** | Director routes are ambiguous or overlapping | Two question patterns route to the same skill for different reasons |
| **Weak output format** | No structured output template | Skill produces unstructured prose when a template would be clearer |

## Evolution Actions

| Action | When to Use | Scope |
|--------|------------|-------|
| **Patch** | Minor fix — stale reference, broken edge, outdated example | Single line or section |
| **Upgrade** | Skill is sound but needs modernization | Rewrite sections while keeping structure |
| **Refactor** | Skill's internal structure needs reorganization | Restructure without changing external interface |
| **Split** | Skill is trying to do two things | Create two skills from one, update parent routing |
| **Merge** | Two skills cover the same ground | Combine into one, retire the other |
| **Retire** | Skill is obsolete or fully superseded | Mark deprecated, update dependents |

## Output Format

```
EVOLUTION ASSESSMENT — [Skill Name]
Domain: [domain/subdomain]
Maturity Stage: [nascent / settling / stable / mature / stale]
Last Modified: [date]

Staleness Check:
  Environmental: [clean / warning / stale] — [details]
  Structural: [clean / warning / stale] — [details]
  Quality: [clean / warning / stale] — [details]

Overall Verdict: [healthy / evolve / urgent]

Recommended Actions:
  1. [Action type]: [specific change with file and section reference]
  2. ...

Priority: [low / medium / high / critical]
Dependencies: [what must happen before or after these changes]
```
