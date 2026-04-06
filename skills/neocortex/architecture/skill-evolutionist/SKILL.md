---
name: skill-evolutionist
description: >
  Track how skills mature over time, identify staleness, propose upgrades, and assess
  when skills need refactoring, splitting, or retiring. Use when evaluating whether
  existing skills are still current, when AI capabilities have outgrown a skill's design,
  or when planning skill maintenance and evolution.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep Bash
---

# Skill Evolutionist — The Naturalist

Studies how skills grow, adapt, and sometimes need to die. Like a naturalist observing species in an ecosystem — tracking which organisms thrive, which are struggling, and which environmental changes demand adaptation.

Skills aren't static. A skill written when context windows were 8K tokens operates differently in a world of 200K. A skill designed before tool-use existed might be crippled by not knowing tools are available. The evolutionist watches for these mismatches between what a skill assumes and what's actually true now.

## Core Function

Assess the maturity and currency of existing skills, identify evolution opportunities, and propose concrete upgrade paths. Every assessment answers:

1. **Is this skill still accurate?** — Do its assumptions match current reality?
2. **Is this skill still well-scoped?** — Has its domain grown or shifted since it was written?
3. **Is this skill still well-connected?** — Are there new cross-domain edges it should have?
4. **What's the upgrade path?** — Specific changes, not vague "needs improvement"

## Maturity Model

Skills move through stages. Knowing where a skill is helps predict what it needs next.

| Stage | Description | Typical Age | What It Needs |
|-------|------------|-------------|---------------|
| **Nascent** | Just built, untested in real use | 0-2 weeks | Usage and feedback — is the design right? |
| **Settling** | Being used, rough edges appearing | 2-8 weeks | Bug fixes, scope adjustments, missing edge cases |
| **Stable** | Working well, clear scope, reliable | 2-6 months | Monitoring for environmental changes |
| **Mature** | Battle-tested, well-connected, refined | 6+ months | Watch for staleness — success breeds complacency |
| **Stale** | Assumptions outdated, scope drifted, edges broken | Varies | Evaluate: evolve, split, or retire |

## Staleness Indicators

### Environmental Staleness
The world changed; the skill didn't.

| Indicator | Signal | Example |
|-----------|--------|---------|
| **Capability gap** | AI can now do something the skill doesn't account for | Skill predates tool-use; still instructs manual workarounds |
| **Context shift** | Token limits, speed, or cost changed enough to alter approach | Skill budgets 500 tokens for a reference that could now be 5,000 |
| **Ecosystem change** | New tools, integrations, or platforms emerged | Skill doesn't know about MCP servers that provide its data |
| **Knowledge drift** | Domain knowledge has evolved | Investing skill references pre-2024 monetary policy assumptions |

### Structural Staleness
The library changed; the skill didn't keep up.

| Indicator | Signal | Example |
|-----------|--------|---------|
| **Missing edges** | New related skills exist but no cross-references | Philosophy built an ethics domain; investing skills don't link to it |
| **Scope creep** | Skill tries to do what a newer specialist handles | Director still says "handle directly" for a question that now has a dedicated child |
| **Orphan risk** | Skills that depended on this one have been rewritten | Referenced-by list is stale |
| **Duplicate coverage** | Two skills now cover the same territory | One should be retired or merged |

### Quality Staleness
The skill was always a bit weak; time made it obvious.

| Indicator | Signal | Example |
|-----------|--------|---------|
| **Thin references** | No reference files where they'd help | Action skill with complex taxonomy but no reference doc |
| **Vague routing** | Director routes are ambiguous or overlapping | Two question patterns route to the same skill for different reasons |
| **Weak output format** | No structured output template | Skill produces unstructured prose when a template would be clearer |

## Evolution Assessment Process

### Quick Assessment (single skill)

1. **Read the skill** — Understand its current design, assumptions, and scope
2. **Check environment** — Has anything changed in AI capabilities, tools, or the domain since it was written?
3. **Check structure** — Are its cross-domain edges current? Is its parent/director routing still accurate?
4. **Check quality** — Does it meet current quality standards (reference files, output format, routing clarity)?
5. **Classify** — What maturity stage is it in? What staleness indicators apply?
6. **Prescribe** — Specific upgrade actions, or confirm "stable, no action needed"

### Domain Assessment (full domain audit)

1. **Inventory** — List all skills in the domain with creation dates and last-modified dates
2. **Environmental scan** — What's changed in AI and the domain since the oldest skill was written?
3. **Quick-assess each skill** — Run the single-skill process on every skill
4. **Prioritize** — Rank evolution needs by impact (foundational skills first, leaves last)
5. **Sequence** — Plan the upgrade order respecting dependencies

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

## What This Skill Does NOT Do

- **Rewrite skills** — The evolutionist diagnoses and prescribes. The human + Claude do the surgery.
- **Replace infrastructure/skill-health** — Health checks current operational status (token counts, thresholds). Evolutionist tracks *change over time* and *strategic fitness*.
- **Predict the future** — That's scenario-planner's job. Evolutionist assesses current state against current reality.

## Cross-Domain Connections

- **Neocortex/architecture/skill-cartographer**: Cartographer maps what exists; evolutionist assesses whether what exists is still fit for purpose
- **Neocortex/architecture/growth-architect**: Evolution findings feed into build planning — sometimes upgrading beats building new
- **Neocortex/foresight/frontier-scanner**: Environmental changes from the frontier inform staleness detection
- **Infrastructure/skill-health**: Complementary — health is point-in-time operational status; evolution is longitudinal strategic fitness
- **Infrastructure/skill-registry**: Registry provides creation dates, modification history, and dependency data for assessment
