# Skill Health — Quick Reference


## Quick Reference

| Issue | Remediation |
|-------|-------------|
| Body too large | Move detailed content to `references/`. Keep SKILL.md as overview + instructions. |
| Description too long | Trim to 30-60 words. Focus on specific trigger phrases, not exhaustive lists. |
| Description too short | Add concrete trigger phrases: "Use when the user asks to..., mentions..., or wants to..." |
| No progressive disclosure | Create `references/` directory. Move detailed tables, schemas, examples there. |
| Too many sections | Consider forking via skill-fork. Group related sections into sub-skills. |
| Trigger conflict | Differentiate descriptions. Add qualifying context unique to each skill. |

## Formula / Pseudocode

```
HEALTH CHECK — skill-registry
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status:  ✓ healthy
Score:   85/100
Tokens:  73 (meta) + 1,349 (body) = 1,422
Words:   752 total, 683 body
Issues:  none

HEALTH CHECK — hook-development
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status:  ⚠ warning
Score:   62/100
Tokens:  82 (meta) + 4,061 (body) = 4,143
Words:   2,104 total, 2,034 body
Issues:
  ⚠ body_words (2034) exceeds 2000 — consider moving content to references/
  ⚠ section_count (17) exceeds 8 — consider decomposition via skill-fork
```
