# Skill Dashboard — Quick Reference


## Formula / Pseudocode

```
SKILL QUALITY DASHBOARD
══════════════════════════════════════════════════════════════
  HEALTHY (3 skills)
  Name                 Type        Auto  Manual  Composite
  skill-health         action        92     —        92
  skill-registry       action        85    4/5       87
  example-skill        knowledge     78     —        78

  WARNING (1 skill)
  Name                 Type        Auto  Manual  Composite
  hook-development     action        62     —        62
    ⚠ body exceeds 2000 words
    ⚠ section count exceeds 8

  CRITICAL (0 skills)
══════════════════════════════════════════════════════════════
```

## Formula / Pseudocode

```
SKILL RATING LEADERBOARD
══════════════════════════════════════════════════════════════
  #   Name                 Score   Auto  Manual  Domain
  1.  skill-health           92      92    —      infrastructure
  2.  skill-registry         87      85   4/5     infrastructure
  3.  example-skill          78      78    —      —
  4.  hook-development       62      62    —      development
══════════════════════════════════════════════════════════════
```

## Formula / Pseudocode

```
DOMAIN SUMMARY
══════════════════════════════════════════════════════════════
  Domain           Skills   Avg Score   Tokens   Health
  infrastructure        4        85.5    5,200   ✓✓✓⚠
  development           2        72.0    6,800   ✓⚠
  (untagged)            1        78.0      455   ✓
══════════════════════════════════════════════════════════════
```
