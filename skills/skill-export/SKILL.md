---
name: skill-export
description: >
  Export skills as portable packages for sharing or backup. Use when the user wants to
  package a skill for distribution, create a shareable archive, generate a standalone
  skill bundle, or back up specific skills with their references and metadata.
tools: Read, Write, Bash, Glob, Grep
---

# Skill Export — The Courier

Package skills into portable, self-contained bundles for sharing, backup, or migration between environments.

## Export Formats

### 1. Directory Bundle

A self-contained directory with everything needed to install the skill:

```
skill-registry-export/
├── SKILL.md              (the skill itself)
├── references/           (all reference files)
├── manifest.json         (metadata + install instructions)
└── README.md             (human-readable description)
```

### 2. Tar Archive

Compressed version of the directory bundle:
```
skill-registry-export.tar.gz
```

## Export Process

1. Read the skill's registry entry for metadata
2. Run `scripts/package-skill.sh <skill-dir> <output-dir>` to create the bundle
3. Verify the bundle is complete (all referenced files included)
4. Present the export summary

## Manifest Format

The `manifest.json` describes the package for automated installation:

```json
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
    "body_words": 784,
    "estimated_tokens_total": 1638,
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

## Import Process

To install an exported skill:
1. Extract the bundle to the target `skills/` directory
2. Read `manifest.json` for dependency information
3. Verify dependencies are available (or flag missing ones)
4. Register the skill in the local registry
5. Run health checks on the imported skill

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
