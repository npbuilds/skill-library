---
name: skill-scaffold
description: >
  Create new skills from templates with guided requirements gathering. Use when the user wants
  to scaffold a new skill, create a skill from scratch, generate a skill skeleton, or bootstrap
  a new action, knowledge, or orchestrator skill with proper structure and registry integration.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent WebSearch WebFetch
---

# Skill Scaffold — The Builder

Create new skills from templates with guided requirements gathering, automatic file creation, registry integration, and post-creation health validation.

## Workflow

### 1. Gather Requirements

Ask the user for (or infer from context):

- **Skill name** (kebab-case, e.g., `my-new-skill`)
- **Skill type**: knowledge, action, director, or orchestrator
- **Description**: 20-60 words, must include trigger phrases
- **Tools needed**: which tools the skill will use (action/orchestrator only)
- **Target plugin**: which plugin directory to create in (default: this plugin's `skills/`)

If the user provides a brief request like "create a skill for X", infer reasonable defaults and confirm before proceeding.

### 1.5. Domain Research (Optional)

Before building a skill, research the domain to ensure the skill is grounded in real knowledge rather than assumptions. This step uses the Spelunker research system (`skills/research/spelunker/SKILL.md`).

**When to run domain research:**
- Building a **knowledge skill** in a domain you're unfamiliar with — always research
- Building a **new domain** from scratch — always research (deep mode)
- Building an **action skill** that requires domain-specific methodology — research the methodology
- Building **infrastructure or meta skills** — skip (no domain knowledge needed)
- User explicitly requests skipping research — skip

**How to invoke:**
1. Formulate a research question: "What are the core concepts, established frameworks, key terminology, and common misconceptions in [domain/subdomain]?"
2. Route to Spelunker at `quick` or `standard` depth depending on familiarity
3. Use the research findings to:
   - Populate knowledge skill content with verified information (not assumptions)
   - Identify the right sub-skill boundaries (what deserves its own skill vs. what's a section)
   - Ensure terminology matches domain conventions
   - Surface common misconceptions to address in the skill's reference material
4. Include a `Research Provenance` note in the created skill's references, noting what was researched and key sources consulted

**Default behavior:** If the domain is unfamiliar and the skill type is knowledge, prompt the user: "This is a new domain. Would you like me to research [topic] before building the skill?"

### 2. Select Template

Read the appropriate template from `templates/`:

| Type | Template | When to use |
|------|----------|-------------|
| knowledge | `templates/knowledge-skill.md` | Passive reference, no tools, no side effects |
| action | `templates/action-skill.md` | User-invoked, has tools, produces side effects |
| director | `templates/director-skill.md` | Subdomain manager, routes to child skills, resolves conflicts |
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

### 4. Determine Placement

Ask the user (or infer) where this skill belongs in the hierarchy:

- **Which domain?** (e.g., `design`, `infrastructure`, `culinary`, or a new domain)
- **Which subdomain/director?** (optional — only if the domain has directors)

Placement rules:
```
skills/<domain>/<skill-name>/                    # Skills at domain level
skills/<domain>/<director-name>/<skill-name>/    # Skills under a director
skills/<domain>/<orchestrator-name>/             # Orchestrators at domain root
skills/<domain>/<director-name>/                 # Directors contain child skills
```

For director skills, the directory they create will contain child skills nested inside.

### 5. Create Files

Create the skill directory and files:

```
skills/<domain>/[<director>/]<skill-name>/
├── SKILL.md              # From customized template
├── references/           # Always create (for future progressive disclosure)
│   └── .gitkeep
└── [templates/]          # Only for orchestrator type
    └── .gitkeep
```

For action and orchestrator skills, also consider creating:
- `examples/` — if the skill involves complex output formats
- `scripts/` — if the skill delegates to shell scripts
- `agents/` — if the orchestrator delegates to specialist agents

### 6. Register

After file creation, register the new skill in the registry:

1. Run `scripts/analyze-skill.sh` on the new SKILL.md to compute metrics
2. Follow the skill-registry "Add Skill" workflow to create the registry entry
3. Set `source` based on location:
   - Inside this plugin's `skills/` → `self`
   - Inside another plugin → `custom`
4. Set initial `auto_score` from the rating rubric (read `skills/infrastructure/skill-dashboard/references/rating-rubric.md`)
5. Add relationship: `depends_on: ["skill-registry"]` (all skills depend on the registry)
6. Update `network.domains` if the user specifies a domain tag

### 7. Validate

Run post-creation checks:

1. Run `scripts/validate-structure.sh` on the new skill directory
2. Check metrics against health thresholds (read `skills/infrastructure/skill-health/references/health-thresholds.md`)
3. Report any issues found

### 8. Present Result

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

### 9. Suggest Cross-Domain Bridges

After registration, run the bridge suggestion tool to prevent the new skill from being born as an island:

```bash
python3 scripts/suggest-bridges.py <skill-name>
```

This uses TF-IDF cosine similarity to find skills in other domains that share meaningful conceptual overlap, boosted by domain adjacency and structural role matching. For each suggested bridge:

1. **Evaluate**: Is the connection conceptually real, or just keyword coincidence?
2. **Wire**: For valid bridges, add a `Cross-Domain Connections` section to the new skill's SKILL.md with one line per bridge explaining the relationship.
3. **Reciprocate**: Add a matching reference in the partner skill's SKILL.md.
4. **Register**: Run with `--apply` to add the edges to the registry, or add them manually.

**The 3-edge rule**: If a new skill can't identify at least 1 cross-domain connection, question whether it belongs where it is. Well-placed skills almost always have natural bridges to other domains.

## Quality Gate

Before finalizing, verify the new skill passes the quality checklist. Read `references/quality-checklist.md` for the full checklist.

Summary of must-pass items:
- SKILL.md has valid YAML frontmatter with name, description, tools
- Description is 20-60 words with action verbs
- Directory structure matches the skill type
- No health threshold violations (body < 2000 words, sections 2-8)
