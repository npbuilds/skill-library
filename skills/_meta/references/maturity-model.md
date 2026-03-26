# Domain Maturity Model

A 6-level scale for assessing how developed a domain is within the skill library.

## Levels

### Level 0 — Vacant
The domain exists as a concept but has no skills yet.
- No folder in `skills/`
- May be referenced in agent definitions or conversations but nothing is built

### Level 1 — Seedling
Has some knowledge skills but no organizational structure.
- 1-3 knowledge skills
- No director, no orchestrator
- Skills are standalone — no routing or curriculum

### Level 2 — Sprouting
Has enough knowledge to justify structure.
- 3+ knowledge skills
- May have action skills
- Still no director or orchestrator
- **Signal to build a director:** when you have 3+ skills in a clear subdomain

### Level 3 — Branching
Has directors organizing subdomains.
- At least one director skill routing to child skills
- Curriculum order defined within subdomains
- Conflict resolution rules established
- **Signal to build an orchestrator:** when you have 2+ subdomains with directors

### Level 4 — Canopy
Has an orchestrator coordinating across subdomains.
- Domain orchestrator delegates to directors
- Directors route to specialist skills
- Full hierarchy: orchestrator -> director -> knowledge/action
- Cross-subdomain references mapped

### Level 5 — Forest
Fully mature — self-maintaining ecosystem.
- All Level 4 features plus:
- Health checks and quality scores maintained
- Test cases for behavioral validation
- Cross-domain connections documented
- Curriculum progression from foundational to advanced

## Assessment Rules

Count the following for each domain:
- Knowledge skills: +1 each
- Action skills: +1 each
- Director skills: +3 each (they represent organizational investment)
- Orchestrator: +5 (strategic layer exists)
- Test coverage: +2 (skills have been validated)

| Score | Maturity Level |
|-------|---------------|
| 0     | Level 0       |
| 1-3   | Level 1       |
| 4-6   | Level 2       |
| 7-10  | Level 3       |
| 11-20 | Level 4       |
| 21+   | Level 5       |

## What Maturity Means for Recommendations

- **Level 0-1**: "You keep asking about X. Want to build a skill for it?"
- **Level 2**: "You have 3+ skills in Y. A director would help organize them."
- **Level 3**: "Domain Z has 2 subdomains. An orchestrator would coordinate them."
- **Level 4**: "Domain is well-structured. Focus on depth — advanced skills, more references."
- **Level 5**: "This domain is mature. Maintain quality and look for cross-domain opportunities."
