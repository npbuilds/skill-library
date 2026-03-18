---
name: skill-infra-upgrade
description: >
  Upgrade the skill-infra plugin as a whole unit. Runs a self-audit, checks for schema
  migrations, re-validates all skills, recomputes all scores, and reports the upgrade status.
tools: Read, Write, Bash, Glob, Grep, Agent
---

# /skill-infra-upgrade

Run a full self-upgrade cycle on the skill-infra plugin.

## What This Does

1. **Schema Migration**: Run `scripts/migrate-registry.sh` to apply any pending schema updates
2. **Full Scan**: Launch `registry-scanner` agent to discover new or moved skills
3. **Re-validate All**: Run `scripts/validate-structure.sh` on every registered skill
4. **Recompute Metrics**: Run `scripts/analyze-skill.sh` on every registered SKILL.md
5. **Recompute Scores**: Recalculate all `auto_score` and `composite_score` values
6. **Health Check**: Run health checks on all skills, update `health_status` and `issues`
7. **Integrity Verify**: Check all bidirectional relationships, domain tags, network consistency
8. **Version Bump**: Update `.claude-plugin/plugin.json` version if changes were made

## Usage

```
/skill-infra-upgrade
```

No arguments needed. Operates on the entire infrastructure.

## Expected Output

```
SKILL-INFRA UPGRADE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Version: 0.9.0 → 1.0.0

Migration:    ✓ schema v1 (current)
Discovery:    ✓ 9/9 skills tracked, 0 new found
Validation:   ✓ 9/9 pass structural checks
Metrics:      ✓ 9/9 recomputed
Scores:       ✓ 9/9 recalculated (2 changed)
Health:       ✓ 8 healthy, 1 warning
Integrity:    ✓ all relationships bidirectional
Version:      ✓ bumped to 1.0.0

Score Changes:
  skill-dashboard:  97 → 97  (unchanged)
  skill-scaffold:   97 → 95  (body grew past threshold)

Health Warnings:
  ⚠ skill-registry: body_words 853 (healthy but approaching 1000)

Upgrade complete in 4.2s
```
