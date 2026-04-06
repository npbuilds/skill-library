---
name: foresight
description: >
  Direct the foresight subdomain — route AI landscape tracking, future scenario modeling,
  and strategic briefing requests to the right specialist. Use when the user asks what's
  new in AI, wants to explore possible futures for the library, or needs a strategic
  summary of where things stand and where they're headed.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Foresight Director — The Watchtower

The outward-looking arm of Neocortex. While the Architecture director examines the library itself, Foresight watches the horizon — tracking what's changing in AI, modeling where things could go, and distilling it all into strategic intelligence.

Foresight answers one question at every level of zoom: **"What's coming, and what does it mean for us?"**

## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| frontier-scanner | `frontier-scanner/SKILL.md` | Action | Track AI capabilities, model releases, tool ecosystem changes, paradigm shifts |
| scenario-planner | `scenario-planner/SKILL.md` | Action | Model multiple plausible futures and stress-test library strategy against them |
| briefing-engine | `briefing-engine/SKILL.md` | Action | Synthesize foresight + architecture intelligence into strategic briefings |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "What's new in AI?", "What just launched?", "What capabilities changed?" | frontier-scanner | Current-state AI landscape tracking |
| "What could happen next?", "What if X happens?", "What futures should we prepare for?" | scenario-planner | Prospective multi-scenario modeling |
| "Give me the big picture", "What's our strategy?", "Brief me" | briefing-engine | Synthesized strategic output |
| "Is this AI development real or hype?" | frontier-scanner → escalate to philosophy/epistemology if deeper analysis needed | Capability assessment with epistemic rigor |
| "How does this AI development affect domain X?" | frontier-scanner → hand off to architecture/growth-architect | Impact flows through to build planning |

### Multi-Skill Sequences

**"What should we prepare for?"**
1. frontier-scanner → current landscape snapshot
2. scenario-planner → model 3-5 plausible futures from current state
3. briefing-engine → synthesize into actionable strategic brief

**"Is this AI trend real and what does it mean?"**
1. frontier-scanner → assess the development
2. Escalate to philosophy/epistemology/evidence-evaluator if evidence quality is in question
3. scenario-planner → model implications if the trend holds
4. Hand off to architecture/growth-architect for build planning

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Frontier-scanner identifies a breakthrough; scenario-planner shows it doesn't change strategy | Report both. A real breakthrough that doesn't affect the library is useful context, not an action item | Not every development requires a response |
| Multiple scenarios conflict on what to build | Identify robust strategies that work across scenarios. Flag scenario-dependent strategies as bets, not plans | Hedging across futures beats betting on one |
| User wants a briefing but frontier data is stale | Briefing-engine should flag data freshness. "Last scan was [date] — recommend a fresh frontier-scan first" | Transparency about data quality |

## Scope Boundaries

**This director handles**: AI landscape tracking, capability trend analysis, future scenario modeling, strategic briefings, development impact assessment.

**Escalate to the orchestrator when**:
- The question is about library structure, gaps, or patterns (Architecture director)
- The question is about explaining a concept, not tracking a development (clarity-engine via Architecture)
- The question requires domain-specific analysis beyond AI landscape (route to relevant domain)
- The question is about evidence quality of AI claims (philosophy/epistemology)
