---
name: skill-scaffold
description: >
  Create new skills from templates with guided requirements gathering. Use when the user wants
  to scaffold a new skill, create a skill from scratch, generate a skill skeleton, or bootstrap
  a new action, knowledge, or orchestrator skill with proper structure and registry integration.
tools: Read, Write, Bash, Glob, Grep
---

# Skill Scaffold — The Builder

Create new skills from templates with guided requirements gathering, automatic file creation, registry integration, and post-creation health validation.

## Workflow

### 1. Gather Requirements

Ask the user for (or infer from context):

- **Skill name** (kebab-case, e.g., `my-new-skill`)
- **Skill type**: knowledge, action, or orchestrator
- **Description**: 20-60 words, must include trigger phrases
- **Tools needed**: which tools the skill will use (action/orchestrator only)
- **Target plugin**: which plugin directory to create in (default: this plugin's `skills/`)

If the user provides a brief request like "create a skill for X", infer reasonable defaults and confirm before proceeding.

### 2. Select Template

Read the appropriate template from `templates/`:

| Type | Template | When to use |
|------|----------|-------------|
| knowledge | `templates/knowledge-skill.md` | Passive reference, no tools, no side effects |
| action | `templates/action-skill.md` | User-invoked, has tools, produces side effects |
| orchestrator | `templates/orchestrator-skill.md` | Multi-phase, forks agents, complex coordination |

### 3. Customize Template

Replace template placeholders with gathered requirements:

- `{{SKILL_NAME}}` — kebab-case skill name
- `{{SKILL_TITLE}}` — title-cased display name
- `{{SKILL_SUBTITLE}}` — short tagline (derive from description)
- `{{DESCRIPTION}}` — full description text
- `{{TOOLS}}` — comma-separated tool list
- `{{DESCRIPTION_EXPANDED}}` — one-sentence expanded explanation for the body intro

For the description, ensure it:
- Is 20-60 words
- Contains action verbs (use, create, build, analyze, check, run, generate, etc.)
- Includes specific trigger phrases ("Use when the user asks to...", "Use when...")
- Written in third person

### 4. Create Files

Create the skill directory and files:

```
skills/<skill-name>/
├── SKILL.md              # From customized template
├── references/           # Always create (for future progressive disclosure)
│   └── .gitkeep
└── [templates/]          # Only for orchestrator type
    └── .gitkeep
```

For action and orchestrator skills, also consider creating:
- `examples/` — if the skill involves complex output formats
- `scripts/` — if the skill delegates to shell scripts

### 5. Register

After file creation, register the new skill in the registry:

1. Run `scripts/analyze-skill.sh` on the new SKILL.md to compute metrics
2. Follow the skill-registry "Add Skill" workflow to create the registry entry
3. Set `source` based on location:
   - Inside this plugin's `skills/` → `self`
   - Inside another plugin → `custom`
4. Set initial `auto_score` from the rating rubric (read `skills/skill-dashboard/references/rating-rubric.md`)
5. Add relationship: `depends_on: ["skill-registry"]` (all skills depend on the registry)
6. Update `network.domains` if the user specifies a domain tag

### 6. Validate

Run post-creation checks:

1. Run `scripts/validate-structure.sh` on the new skill directory
2. Check metrics against health thresholds (read `skills/skill-health/references/health-thresholds.md`)
3. Report any issues found

### 7. Present Result

Show the user what was created:

```
SCAFFOLD COMPLETE — my-new-skill
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type:        action
Location:    skills/my-new-skill/
Files:       SKILL.md, references/.gitkeep
Words:       285 (body)
Tokens:      ~370 (body) + 42 (meta) = ~412
Health:      ✓ healthy
Score:       95/100
Registry:    ✓ registered

Next steps:
  1. Edit SKILL.md to add your skill's specific instructions
  2. Add reference files to references/ as needed
  3. Run /skill-status to verify in the dashboard
```

## Quality Gate

Before finalizing, verify the new skill passes the quality checklist. Read `references/quality-checklist.md` for the full checklist.

Summary of must-pass items:
- SKILL.md has valid YAML frontmatter with name, description, tools
- Description is 20-60 words with action verbs
- Directory structure matches the skill type
- No health threshold violations (body < 2000 words, sections 2-8)
