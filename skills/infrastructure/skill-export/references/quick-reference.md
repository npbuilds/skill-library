# Skill Export — Quick Reference


## Formula / Pseudocode

```
skill-registry-export/
├── SKILL.md              (the skill itself)
├── references/           (all reference files)
├── manifest.json         (metadata + install instructions)
└── README.md             (human-readable description)
```

## Formula / Pseudocode

```
{
  "format_version": 1,
  "skill": {
    "name": "skill-registry",
    "version": "1.0.0",
    "description": "Manage the skill registry...",
    "type": "action",
    "source": "custom"
  },
  "metrics": {
    "body_words": 683,
    "estimated_tokens_total": 1422,
    "auto_score": 100
  },
  "dependencies": {
    "depends_on": [],
    "required_scripts": [],
    "required_data": []
  },
  "exported_from": {
    "plugin": "skill-infra",
    "plugin_version": "1.0.0",
    "export_date": "2026-03-17"
  }
}
```

## Output Format

```
EXPORT — skill-registry
━━━━━━━━━━━━━━━━━━━━━━━
Files:    3 (SKILL.md + 1 reference + manifest.json)
Size:     4.2 KB
Format:   directory bundle
Location: ./exports/skill-registry-export/

  ✓ SKILL.md copied
  ✓ references/registry-schema.md copied
  ✓ manifest.json generated
  ✓ README.md generated
```
