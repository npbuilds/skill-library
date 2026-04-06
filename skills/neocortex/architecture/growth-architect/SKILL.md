---
name: growth-architect
description: >
  Design and prioritize the skill library's growth — turn gap analyses, frontier scans,
  and pattern insights into concrete, sequenced build plans. Use when deciding what domain
  to build next, how to sequence skill construction, where to invest effort, or how to
  evolve existing domains.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep
---

# Growth Architect — The Urban Planner

Turns raw intelligence (frontier scans, gap maps, pattern reports) into sequenced build plans. The other Neocortex skills gather data; this one makes decisions.

Like an urban planner: you don't just build where there's empty land. You build where the roads already lead, where the demand is, and where the infrastructure can support it. A beautiful building in the wrong location is a waste.

## Core Function

Synthesize inputs from all other Neocortex skills into prioritized, actionable growth plans for the skill library. Every plan answers:

1. **What to build** — Specific domains, skills, or connections
2. **In what order** — Dependencies, prerequisites, and logical sequence
3. **Why this sequence** — The strategic logic behind the prioritization
4. **What to skip** — Equally important: what NOT to build yet, and why

## Prioritization Framework

### The Four Lenses

Every candidate skill or domain is evaluated through four lenses:

**1. Cross-Domain Value (weight: high)**
How many existing domains benefit from this addition?

| Score | Criteria |
|-------|----------|
| 5 | Connects to 4+ existing domains with meaningful edges |
| 4 | Connects to 3 domains |
| 3 | Connects to 2 domains |
| 2 | Connects to 1 domain |
| 1 | Standalone — no meaningful connections |

*Rationale: Skills that create connections make the whole library smarter. Isolated skills are expensive to maintain for limited value.*

**2. Foundation Strength (weight: high)**
Does this skill/domain provide infrastructure that future skills will build on?

| Score | Criteria |
|-------|----------|
| 5 | Required prerequisite for 3+ planned domains |
| 4 | Required prerequisite for 1-2 planned domains |
| 3 | Useful context for multiple future skills |
| 2 | Self-contained value, minimal downstream dependency |
| 1 | Terminal node — nothing depends on it |

**3. User Demand (weight: medium)**
How often does the user actually invoke this kind of thinking?

| Score | Criteria |
|-------|----------|
| 5 | Used daily or multiple times per week |
| 4 | Used weekly |
| 3 | Used a few times per month |
| 2 | Used occasionally |
| 1 | Niche — rarely needed |

**4. Build Complexity (weight: inverse)**
How hard is this to build well? (Lower complexity = easier to capture value quickly)

| Score | Criteria |
|-------|----------|
| 5 | Simple — 3-5 skills, clear boundaries, well-understood domain |
| 4 | Moderate — 6-10 skills, some fuzzy boundaries |
| 3 | Substantial — 11-20 skills, requires research phase |
| 2 | Complex — 20+ skills, overlapping concerns, novel architecture needed |
| 1 | Massive — entire new paradigm, unclear scope |

### Composite Score

```
Priority = (CrossDomain × 3) + (Foundation × 3) + (UserDemand × 2) + (BuildComplexity × 1)
```

Cross-domain value and foundation strength are weighted highest because they compound — a well-connected foundational domain makes every future addition more valuable.

## Build Plan Structure

### Domain-Level Plan

For proposing new domains:

```
GROWTH PLAN — [Domain Name]
Priority Score: [N] / 45
Rationale: [2-3 sentences — why this, why now]

Tier Assessment:
  Cross-Domain Value: [score] — [connects to X, Y, Z]
  Foundation Strength: [score] — [enables A, B, C]
  User Demand: [score] — [usage pattern]
  Build Complexity: [score] — [estimated N skills]

Architecture Sketch:
  Orchestrator: [name] — [one-line purpose]
  Directors:
    - [director-1] — [purpose] → [child skills]
    - [director-2] — [purpose] → [child skills]
  Estimated total: [N] skills

Build Sequence:
  Wave 1: [skills] — [why these first]
  Wave 2: [skills] — [why these second]
  Wave 3: [skills] — [remaining]

Dependencies:
  Requires: [existing domains/skills this depends on]
  Enables: [future domains/skills this unlocks]

Cross-Domain Edges (planned):
  - [this skill] → [existing skill]: [relationship]
  - ...

Skip List:
  - [Topic that seems related but shouldn't be included yet]: [why not]
```

### Evolution Plan

For expanding or restructuring existing domains:

```
EVOLUTION PLAN — [Domain Name]
Current State: [N skills, M edges, health score]
Proposed Changes:

  Add:
    - [New skill]: [purpose, connects to X]

  Split:
    - [Existing skill] → [Skill A] + [Skill B]: [why]

  Connect:
    - [Skill] → [Other domain/skill]: [new edge]

  Retire:
    - [Skill]: [why it's no longer needed]

Sequence: [order of operations]
Risk: [what could go wrong]
```

## Strategic Principles

1. **Build outward from strength** — New domains should connect to existing strong domains, not float independently
2. **Depth before breadth at the domain level** — Better to have 3 deep domains than 7 shallow ones
3. **Breadth before depth at the library level** — Cover the major knowledge areas before going ultra-deep in any one
4. **The 3-edge rule** — Don't build a domain unless you can identify at least 3 meaningful cross-domain connections before starting
5. **Respect the build rhythm** — Wave-based construction with bug checks between waves. Never rush to "done"; each wave should be solid before the next begins

## Cross-Domain Connections

- **Neocortex/frontier-scanner**: Frontier developments create new build opportunities and shift priorities
- **Neocortex/skill-cartographer**: Gap map is the primary input for growth planning
- **Neocortex/pattern-synthesizer**: Patterns reveal structural opportunities (missing abstractions become build candidates)
- **Neocortex/clarity-engine**: Growth plans should be explainable — if the "why" can't be made intuitive, the plan isn't ready
- **Infrastructure/skill-scaffold**: Once a plan is approved, scaffolding turns the plan into directory structure and SKILL.md templates
