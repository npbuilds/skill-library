# Infrastructure Orchestrator — Quick Reference


## Quick Reference

| Operation | Primary Skill | Supporting Skills | When |
|-----------|--------------|-------------------|------|
| Create a skill | `skill-scaffold` | `skill-registry`, `skill-health` | User wants a new skill |
| Check skill quality | `skill-health` | `skill-registry` | User asks "is this skill good?" |
| Run tests on a skill | `skill-test` | `skill-health` | User wants to validate behavior |
| Analyze API/patterns | `skill-analyze` | `skill-registry` | Deep skill structure analysis |
| Visualize the library | `skill-dashboard` | `skill-registry` | User wants a status overview |
| Map relationships | `skill-network` | `skill-registry` | User wants dependency/connection graphs |
| Export skills | `skill-export` | `skill-registry` | User wants to package skills for sharing |
| Fork/decompose | `skill-fork` | `skill-scaffold`, `skill-registry` | User wants to split or derive skills |
| Full audit | `skill-health` | All others | User wants a comprehensive library checkup |
| Build new domain | `skill-scaffold` | `skill-registry`, `skill-health`, `skill-test` | User wants a complete new domain |

## Quick Reference

| Skill | Path | What It Does |
|-------|------|-------------|
| skill-scaffold | `skills/infrastructure/skill-scaffold/SKILL.md` | Create new skills from templates |
| skill-registry | `skills/infrastructure/skill-registry/SKILL.md` | Manage the skill catalog |
| skill-health | `skills/infrastructure/skill-health/SKILL.md` | Check skill quality and health |
| skill-test | `skills/infrastructure/skill-test/SKILL.md` | Run tests on skill behavior |
| skill-analyze | `skills/infrastructure/skill-analyze/SKILL.md` | Deep structural analysis |
| skill-dashboard | `skills/infrastructure/skill-dashboard/SKILL.md` | Visual status overview |
| skill-network | `skills/infrastructure/skill-network/SKILL.md` | Dependency and relationship mapping |
| skill-export | `skills/infrastructure/skill-export/SKILL.md` | Package skills for sharing |
| skill-fork | `skills/infrastructure/skill-fork/SKILL.md` | Decompose or derive skills |

## Formula / Pseudocode

```
OPERATION COMPLETE — {operation name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scope:       {single skill / subdomain / domain / library}
Skills:      {N} created, {N} updated, {N} flagged
Health:      {all healthy / N warnings / N critical}
Registry:    {in sync / N unregistered}

Next steps:
  1. {most important follow-up}
  2. {second priority}
```
