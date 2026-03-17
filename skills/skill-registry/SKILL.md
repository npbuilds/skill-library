---
name: skill-registry
description: >
  Manage the skill registry — the central catalog of all skills in the mycelial network.
  Use when the user wants to browse skills, search the catalog, add or update a skill entry,
  remove a skill, sync the registry with the filesystem, or when any other infrastructure
  skill needs to look up skill metadata, locations, or relationships.
tools: Read, Write, Bash, Glob, Grep, Agent
---

# Skill Registry — The Map

The registry at `data/registry.json` is the single source of truth for all skill metadata in the infrastructure. Every other skill reads from or writes to the registry through the patterns documented here.

## Registry Location

The registry file path relative to this plugin's root:
```
data/registry.json
```

Read the `references/registry-schema.md` file for the full JSON schema and field definitions.

## Operations

### Browse / Search

Read `data/registry.json` and present skills to the user.

**Browse all:**
- Read registry, extract all skill entries
- Present as a formatted table: name, type, source, health_status, lifecycle status, composite_score, estimated_tokens_total
- Group by domain tags if domains exist

**Search / Filter:**
- Accept filter criteria: `domain:<tag>`, `type:<knowledge|action|orchestrator>`, `source:<custom|external|self>`, `health:<healthy|warning|critical>`, `status:<active|deprecated|archived>`
- Apply filters to registry entries
- Present matching results as formatted table

### Add Skill

Register a new skill in the catalog.

1. Verify the SKILL.md file exists at the given path
2. Run `scripts/analyze-skill.sh <path>` to compute metrics
3. Parse YAML frontmatter from SKILL.md to extract: name, description, tools, context, user-invocable, disable-model-invocation
4. Determine skill type from content analysis:
   - **knowledge**: has `user-invocable: false` or no tools list
   - **orchestrator**: has `context: fork` or launches agents
   - **action**: has `disable-model-invocation: true` or has tools list (default)
5. Determine source:
   - **self**: skill is inside this plugin's `skills/` directory
   - **custom**: skill is in a user-created plugin or project
   - **external**: skill is in an official/installed plugin
6. Create registry entry with all fields (see schema reference)
7. Set lifecycle status to `active`, health_status to `healthy` (pending first health check)
8. Set initial ratings: auto_score computed from metrics, manual_rating null
9. Append changelog entry: `{date, action: "created", note: "Initial registration"}`
10. Write updated registry back to `data/registry.json`

### Update Skill

Re-scan an existing skill to refresh its metrics and metadata.

1. Find the skill entry in registry by name or path
2. Re-run `scripts/analyze-skill.sh` on its SKILL.md
3. Re-parse frontmatter for any metadata changes
4. Update metrics, preserve manual_rating and relationships
5. Recompute auto_score and composite_score
6. Append changelog entry with what changed
7. Write updated registry

### Remove Skill

Remove a skill from the registry.

1. Find the skill entry by name
2. Clean up relationships: remove this skill from other entries' `referenced_by`, `depends_on`, etc.
3. Remove the entry from the skills map
4. Update network domain indexes
5. Append no changelog (entry is gone) — but log the removal action to stdout
6. Write updated registry

Note: This only removes the registry entry. It does NOT delete the actual skill files. For full deprecation/archival, use the deprecation lifecycle.

### Deprecate Skill

Mark a skill as deprecated with optional replacement.

1. Find the skill entry by name
2. Set `status` to `deprecated`
3. Set `deprecated_date` to current date
4. Set `replacement_skill` if provided
5. Set `deprecation_reason` if provided
6. Append changelog entry
7. Write updated registry

### Sync (Full Scan)

Discover all SKILL.md files and reconcile with registry.

1. Run `scripts/scan-skills.sh` with the plugin root as an additional directory
2. For each discovered SKILL.md:
   - If not in registry: run Add Skill workflow
   - If in registry: run Update Skill workflow (refresh metrics)
3. For each registry entry:
   - If SKILL.md no longer exists at recorded path: flag as WARNING, do not auto-remove
4. Update `last_scan` timestamp in registry root
5. Report: skills added, skills updated, skills missing

For a full system-wide scan (including all installed plugins), launch the `registry-scanner` agent which handles the broader filesystem search.

## Auto-Score Computation

Compute `auto_score` (0-100) from metrics:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Token efficiency | 30 | 100 if body <1500 words, linear decrease to 0 at 5000 |
| Progressive disclosure | 20 | 100 if has references/ when body >1000 words, 50 if no references needed, 0 if body >1500 with no references |
| Description quality | 20 | 100 if description 20-60 words, penalties for too short (<15) or too long (>100) |
| Structure | 15 | 100 if 3-6 sections, penalties for too few (<2) or too many (>8) |
| Documentation | 15 | 100 if has examples or references, 70 if standalone but small, 40 if large with no supporting files |

Composite score: `auto_score * 0.7 + (manual_rating / 5 * 100) * 0.3` (if manual_rating is null, composite = auto_score)

## Output Formatting

When presenting registry data to the user, use formatted ASCII tables:

```
┌─────────────────┬────────┬──────────┬────────┬───────┬────────┐
│ Name            │ Type   │ Health   │ Status │ Score │ Tokens │
├─────────────────┼────────┼──────────┼────────┼───────┼────────┤
│ skill-registry  │ action │ healthy  │ active │   85  │  1,200 │
│ skill-health    │ action │ healthy  │ active │   92  │    980 │
└─────────────────┴────────┴──────────┴────────┴───────┴────────┘
```
