# Skill Cartographer — Quick Reference


## Quick Reference

| Dimension | Metric | Healthy | Warning | Critical |
|-----------|--------|---------|---------|----------|
| Depth | Levels in skill tree | 3+ levels | 2 levels | 1 level (flat) |
| Breadth | Skills per domain | 15+ | 5-14 | < 5 |
| Edge density | Cross-domain connections | 5+ edges | 2-4 edges | 0-1 edges |
| Reference coverage | Skills with reference files | > 60% | 30-60% | < 30% |
| Type balance | Mix of action/knowledge/director | All types present | Missing one type | Only one type |

## Structural Health

| Pattern | What It Means | Action |
|---------|--------------|--------|
| **Hub overload** | One skill has 10+ dependents | Consider splitting — single points of failure are fragile |
| **Orphan cluster** | Group of skills with no outside connections | Either connect them or question if they belong |
| **Long chains** | A → B → C → D → E with no shortcuts | Add direct edges where they make sense |
| **Circular dependencies** | A depends on B depends on A | Resolve by clarifying which skill is primary |
| **Ghost references** | Skills reference paths that don't exist | Fix the dead references |

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
