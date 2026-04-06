# Skill Network — Quick Reference


## Formula / Pseudocode

```
CHAIN — skill-scaffold
━━━━━━━━━━━━━━━━━━━━━━━
skill-scaffold
  ├─ depends_on: skill-registry
  ├─ depends_on: skill-health
  │    └─ depends_on: skill-registry ◄ (already visited)
  │    └─ depends_on: skill-dashboard
  │         └─ depends_on: skill-registry ◄ (already visited)
  └─ depends_on: skill-dashboard ◄ (already visited)

Depth: 3    Unique dependencies: 3
```

## Formula / Pseudocode

```
IMPACT — skill-registry
━━━━━━━━━━━━━━━━━━━━━━━
skill-registry is referenced by:
  ├─ skill-health
  ├─ skill-dashboard
  ├─ skill-scaffold
  ├─ skill-test
  ├─ skill-analyze
  ├─ skill-fork
  ├─ skill-network
  └─ skill-export

Direct dependents: 8    Total (transitive): 8
⚠ HIGH IMPACT — changes affect 100% of the network
```

## Formula / Pseudocode

```
ORPHANS
━━━━━━━━
  (none found — all skills are connected)
```

## Formula / Pseudocode

```
⚠ skill-lonely — no dependencies, not referenced by anyone
    Suggestion: connect to domain peers or consider archiving
```
