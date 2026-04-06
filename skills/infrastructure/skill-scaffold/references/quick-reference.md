# Skill Scaffold — Quick Reference


## Quick Reference

| Type | Template | When to use |
|------|----------|-------------|
| knowledge | `templates/knowledge-skill.md` | Passive reference, no tools, no side effects |
| action | `templates/action-skill.md` | User-invoked, has tools, produces side effects |
| director | `templates/director-skill.md` | Subdomain manager, routes to child skills, resolves conflicts |
| orchestrator | `templates/orchestrator-skill.md` | Multi-phase, forks agents, complex coordination |

## Formula / Pseudocode

```
skills/<domain>/<skill-name>/                    # Skills at domain level
skills/<domain>/<director-name>/<skill-name>/    # Skills under a director
skills/<domain>/<orchestrator-name>/             # Orchestrators at domain root
skills/<domain>/<director-name>/                 # Directors contain child skills
```

## Formula / Pseudocode

```
skills/<domain>/[<director>/]<skill-name>/
├── SKILL.md              # From customized template
├── references/           # Always create (for future progressive disclosure)
│   └── .gitkeep
└── [templates/]          # Only for orchestrator type
    └── .gitkeep
```

## Formula / Pseudocode

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
