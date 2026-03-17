---
name: skill-dashboard
description: >
  Display skill dashboards: token efficiency breakdown, skill quality ratings, health
  overview, and rating leaderboard. Use when the user asks to see their skill metrics,
  token costs, ratings, efficiency reports, or wants an overview of their skill collection.
tools: Read, Bash, Glob, Grep
---

# Skill Dashboard — The Observatory

Terminal-based ASCII dashboards for monitoring skill collection health, token efficiency, and quality ratings.

## Dashboards Available

### 1. Token Efficiency Dashboard

Shows the token cost of every skill, sorted by expense.

**How to generate:**
1. Read `data/registry.json`
2. For each skill, extract metrics: `estimated_tokens_metadata`, `estimated_tokens_body`, `estimated_tokens_total`
3. Sort by `estimated_tokens_total` descending
4. Compute aggregates: total metadata cost (always loaded), average body cost, total if all triggered

**Output format:**
```
TOKEN EFFICIENCY DASHBOARD
══════════════════════════════════════════════════════════════
                          Meta    Body    Total   Budget
  hook-development          82   4,061    4,143   ██████████ ⚠
  skill-registry            73   1,565    1,638   ████░░░░░░
  skill-health              78   1,200    1,278   ███░░░░░░░
  example-skill             35     420      455   █░░░░░░░░░

──────────────────────────────────────────────────────────────
  AGGREGATE
  Always loaded (metadata):    268 tokens (4 skills)
  Average body cost:         1,854 tokens
  Max single skill:          4,143 tokens (hook-development)
  Total if all triggered:    7,514 tokens
══════════════════════════════════════════════════════════════
```

The bar chart uses 10 characters scaled to the max token cost. Skills exceeding 3,000 tokens get a `⚠` warning marker.

### 2. Skill Quality Dashboard

Composite view of ratings and health across all skills.

**How to generate:**
1. Read `data/registry.json`
2. For each skill, extract: `auto_score`, `manual_rating`, `composite_score`, `health_status`, `type`, `source`
3. Sort by `composite_score` descending
4. Group by health status

**Output format:**
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

### 3. Rating Leaderboard

Skills ranked by composite score with filtering.

**How to generate:**
1. Read `data/registry.json`
2. Accept optional filter from user: `domain:<tag>`, `type:<type>`, `source:<source>`
3. Sort by `composite_score` descending
4. Show rank, name, composite score, and score breakdown

**Output format:**
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

### 4. Domain Summary

Aggregate metrics by domain tag.

**How to generate:**
1. Read `data/registry.json` network.domains
2. For each domain, compute: skill count, avg composite_score, total tokens, health distribution
3. Present as compact domain overview

**Output format:**
```
DOMAIN SUMMARY
══════════════════════════════════════════════════════════════
  Domain           Skills   Avg Score   Tokens   Health
  infrastructure        4        85.5    5,200   ✓✓✓⚠
  development           2        72.0    6,800   ✓⚠
  (untagged)            1        78.0      455   ✓
══════════════════════════════════════════════════════════════
```

## Presentation Guidelines

- Always read the latest `data/registry.json` before generating any dashboard
- Round scores to integers
- Format token counts with commas for readability (1,638 not 1638)
- Use `✓` for healthy, `⚠` for warning, `✗` for critical
- Use `—` for null/missing values (not "N/A" or "null")
- If the user doesn't specify which dashboard, show the Token Efficiency Dashboard as default (most actionable)
