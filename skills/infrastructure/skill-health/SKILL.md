---
name: skill-health
description: >
  Run health checks on skills to detect issues: oversized SKILL.md, poor trigger descriptions,
  missing progressive disclosure, excessive token usage, trigger conflicts between skills,
  or structural problems. Use when the user wants to audit skills, check health, optimize
  token efficiency, or find problems in their skill collection.
tools: Read, Bash, Glob, Grep, Write, Agent
---

# Skill Health — The Doctor

Analyze skills for quality, efficiency, and structural correctness. Produces health reports with actionable remediation suggestions.

## How to Run

### Single Skill Check

1. Read the skill's SKILL.md file
2. Run `scripts/analyze-skill.sh <path>` to get metrics
3. Apply threshold rules (see below) to generate issues list
4. Compute auto_score using the scoring rubric
5. Update the skill's registry entry with new health_status, issues, auto_score, last_checked
6. Present findings to the user

### Batch Health Check

1. Read `data/registry.json`
2. For each active skill entry, run Single Skill Check
3. Aggregate results into a summary report
4. Present: total skills checked, healthy/warning/critical counts, top issues

### Deep Audit

For thorough analysis beyond metric thresholds, use the Agent tool to launch the `skill-auditor` agent (from `agents/skill-auditor.md`):
- Reads every file in the skill directory
- Checks for broken reference links
- Verifies script executability
- Assesses writing quality and trigger specificity
- Returns structured findings

## Threshold Rules

Read `references/health-thresholds.md` for the full configurable threshold table.

Summary of default thresholds:

**CRITICAL** (health_status → critical):
- `body_words > 5000` — skill is far too large for a single SKILL.md
- `estimated_tokens_body > 6000` — exceeds practical context budget

**WARNING** (health_status → warning):
- `body_words > 2000` — approaching the recommended ceiling
- `description_words > 100` — description is too verbose, wastes always-loaded context
- `description_words < 15` — description too brief, may not trigger reliably
- `body_words > 1500 AND reference_files == 0` — content should use progressive disclosure
- `section_count > 8` — too many sections, consider decomposition
- `section_count < 2` — too few sections, may lack structure
- Description lacks action verbs (checked via grep for common trigger words)

**INFO** (no status change, but noted):
- Skill has no relationships in registry (isolated node)
- Skill has no examples/ directory for action or orchestrator type
- Skill version is still default `1.0.0` with multiple changelog entries

## Trigger Conflict Detection

Detect when two skills have overlapping trigger descriptions that could cause false activations.

1. Read all skill descriptions from registry
2. Extract key trigger phrases from each description (split on commas, "or", "when")
3. For each pair of skills, compare trigger phrases:
   - Exact substring match → HIGH conflict risk
   - Shared key verbs + nouns → MEDIUM conflict risk
4. Flag conflicting pairs as WARNING with both skill names
5. Suggest differentiation:
   - Make triggers more specific (add qualifying context)
   - Differentiate description keywords so skills don't overlap
   - Rename skill to clarify scope

## Auto-Score Computation

Compute `auto_score` (0-100) from metrics. Read `skills/skill-dashboard/references/rating-rubric.md` for the detailed scoring pseudocode — it is the canonical definition.

After computing auto_score, update composite_score:
- If manual_rating is null: `composite_score = auto_score`
- If manual_rating exists: `composite_score = round(auto_score * 0.7 + (manual_rating / 5 * 100) * 0.3)`

## Remediation Suggestions

For each issue, provide a specific fix:

| Issue | Remediation |
|-------|-------------|
| Body too large | Move detailed content to `references/`. Keep SKILL.md as overview + instructions. |
| Description too long | Trim to 30-60 words. Focus on specific trigger phrases, not exhaustive lists. |
| Description too short | Add concrete trigger phrases: "Use when the user asks to..., mentions..., or wants to..." |
| No progressive disclosure | Create `references/` directory. Move detailed tables, schemas, examples there. |
| Too many sections | Consider forking via skill-fork. Group related sections into sub-skills. |
| Trigger conflict | Differentiate descriptions. Add qualifying context unique to each skill. |

## Output Format

Present health results as formatted ASCII:

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
