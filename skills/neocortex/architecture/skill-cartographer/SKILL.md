---
name: skill-cartographer
description: >
  Map the skill library's coverage, white space, and structural health. Use when identifying
  gaps in the library, finding underdeveloped areas, assessing domain coverage, discovering
  orphaned or disconnected skills, or understanding where the library is strong vs. thin.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep bash
---

# Skill Cartographer — The Mapmaker

Draws the map of what the skill library knows and — more importantly — what it doesn't. Every library has blind spots. The cartographer's job is to find them before they matter.

Think of the skill library as a city. Some neighborhoods are fully developed (investing, sommelier, philosophy), some have a few buildings (research), and some are empty lots waiting for a plan. The cartographer walks every street and reports back: where's the density, where are the gaps, and where are roads that lead to dead ends.

## Core Function

Produce a comprehensive map of the library's coverage, identifying:

1. **Developed zones** — Domains with deep skill trees, rich references, strong cross-connections
2. **Frontier zones** — Domains that exist but are thin — few skills, shallow depth, sparse edges
3. **White space** — Topics that should exist but don't — gaps between existing domains, missing subdirectories
4. **Structural issues** — Orphan skills (no connections), hub overload (too many dependencies on one skill), missing bridges between related domains

## Mapping Dimensions

### Coverage Map
For each domain, assess:

| Dimension | Metric | Healthy | Warning | Critical |
|-----------|--------|---------|---------|----------|
| Depth | Levels in skill tree | 3+ levels | 2 levels | 1 level (flat) |
| Breadth | Skills per domain | 15+ | 5-14 | < 5 |
| Edge density | Cross-domain connections | 5+ edges | 2-4 edges | 0-1 edges |
| Reference coverage | Skills with reference files | > 60% | 30-60% | < 30% |
| Type balance | Mix of action/knowledge/director | All types present | Missing one type | Only one type |

### Gap Detection

Three types of gaps to look for:

**1. Adjacent gaps** — Topics that sit between two existing domains but belong to neither.
- Method: For each pair of domains, ask: "What topic lives in the space between these two?"
- Example: Between investing and game-theory, there's "market mechanism design" — neither domain fully covers it.

**2. Depth gaps** — A domain exists but is missing obvious subdirectories.
- Method: For each domain, list what a comprehensive treatment would include. Compare to what exists.
- Example: A writing domain without a "research writing" or "technical writing" subdomain.

**3. Bridge gaps** — Two domains that should be connected but have no cross-domain edges.
- Method: For each domain pair, ask: "Would an expert in domain A ever need knowledge from domain B?"
- Example: If philosophy/ethics and investing exist but have no connection, that's a bridge gap — investment decisions have ethical dimensions.

### Structural Health

| Pattern | What It Means | Action |
|---------|--------------|--------|
| **Hub overload** | One skill has 10+ dependents | Consider splitting — single points of failure are fragile |
| **Orphan cluster** | Group of skills with no outside connections | Either connect them or question if they belong |
| **Long chains** | A → B → C → D → E with no shortcuts | Add direct edges where they make sense |
| **Circular dependencies** | A depends on B depends on A | Resolve by clarifying which skill is primary |
| **Ghost references** | Skills reference paths that don't exist | Fix the dead references |

## Mapping Process

### Quick Map (domain-level)
1. Read `data/registry.json` for the full skill inventory
2. Count skills per domain, assess type distribution
3. Count cross-domain edges
4. Identify the top 3 gaps by impact

### Full Map (comprehensive audit)
1. **Inventory** — Read the registry, verify against filesystem (Glob for all SKILL.md files)
2. **Coverage scoring** — Rate each domain on all 5 dimensions
3. **Gap analysis** — Run all three gap detection methods
4. **Structural audit** — Check for all structural patterns
5. **Visualization** — Present as a domain map with color-coded health

## Output Format

```
SKILL LIBRARY MAP — [Date]
Total Skills: [N] across [M] domains

Domain Coverage:
  [Domain] ████████░░ [score] — [N skills, M edges, key gap]
  [Domain] ██████░░░░ [score] — [N skills, M edges, key gap]
  ...

Top Gaps (by impact):
  1. [Gap description] — between [Domain A] and [Domain B]
     Impact: [why this matters]
     Suggested fix: [new skill/edge/domain]

  2. ...

Structural Issues:
  [Issue type]: [description and location]

White Space Candidates:
  - [Topic] — adjacent to [existing domains], would serve [use case]
  - ...
```

## Cross-Domain Connections

- **Infrastructure/skill-health**: Cartographer assesses strategic coverage; skill-health checks operational status
- **Infrastructure/skill-network**: Network shows the connection graph; cartographer interprets what it means
- **Neocortex/growth-architect**: Cartographer identifies gaps; growth-architect prioritizes which to fill
- **Neocortex/pattern-synthesizer**: Patterns may reveal why certain gaps exist or suggest structural solutions
