# Health Threshold Configuration

These thresholds determine skill health status. Adjust as your skill collection matures.

## Threshold Table

| Metric | Critical | Warning | Healthy | Rationale |
|--------|----------|---------|---------|-----------|
| `body_words` | > 5,000 | > 2,000 | ≤ 2,000 | SKILL.md should be 1,500-2,000 words. Beyond 5,000 is unacceptable. |
| `estimated_tokens_body` | > 6,000 | > 3,000 | ≤ 3,000 | Each triggered skill costs context. Keep it lean. |
| `description_words` | — | > 100 or < 15 | 15-100 | Description is always loaded. Too long wastes context; too short misses triggers. |
| `section_count` | — | > 8 or < 2 | 2-8 | Too many sections signals a skill doing too much. Too few signals weak structure. |
| `reference_files` | — | 0 when body > 1,500 | any | Large skills need progressive disclosure via references/. |

## Progressive Disclosure Check

A skill passes the progressive disclosure check if ANY of:
- `body_words ≤ 1000` (small enough to be self-contained)
- `reference_files > 0` (has supporting references)
- `type == "knowledge"` (knowledge skills are inherently reference-like)

## Description Quality Check

A description passes quality if ALL of:
- Word count between 15 and 100
- Contains at least one action verb from: use, create, build, add, update, fix, analyze, check, run, generate, scaffold, fork, test, export, browse, search, manage, audit, review, optimize
- Written in third person ("Use when..." or "This skill should be used when...")
- Contains specific trigger phrases (not just vague "helps with development")

## Trigger Conflict Risk Levels

| Level | Criteria | Action |
|-------|----------|--------|
| HIGH | Two descriptions share a 3+ word phrase (e.g., "create a new skill") | FLAG as warning, suggest immediate differentiation |
| MEDIUM | Two descriptions share 2+ key nouns AND a verb | NOTE in report, monitor |
| LOW | Descriptions are in the same domain but use different language | No action needed |

## Score Penalty Table

Used to compute auto_score deductions from the base of 100:

| Factor | Weight | Perfect (100) | Zero (0) |
|--------|--------|---------------|----------|
| Token efficiency | 30% | body ≤ 1,500 words | body ≥ 5,000 words |
| Progressive disclosure | 20% | Has references/ when body > 1,000 | Body > 1,500 with no references/ |
| Description quality | 20% | 20-60 words, has trigger verbs | < 10 or > 100 words |
| Structure | 15% | 3-6 sections | < 2 or > 8 sections |
| Documentation | 15% | Has references/ or examples/ | Large skill with no supporting files |
