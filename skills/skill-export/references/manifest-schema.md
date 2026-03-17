# Export Manifest Schema

The `manifest.json` file describes an exported skill package for automated installation.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `format_version` | int | yes | Manifest format version (currently 1) |
| `skill.name` | string | yes | Skill identifier |
| `skill.version` | string | yes | Skill version at time of export |
| `skill.description` | string | yes | Full frontmatter description |
| `skill.type` | enum | yes | `knowledge`, `action`, or `orchestrator` |
| `skill.source` | string | yes | Original source (`self`, `custom`, `external`) |
| `metrics.body_words` | int | yes | Body word count at export time |
| `metrics.estimated_tokens_total` | int | yes | Token estimate at export time |
| `metrics.auto_score` | int | yes | Quality score at export time |
| `dependencies.depends_on` | array | yes | Skill names this skill needs |
| `dependencies.required_scripts` | array | yes | Scripts referenced in SKILL.md body |
| `dependencies.required_data` | array | yes | Data files referenced (e.g., registry.json) |
| `exported_from.plugin` | string | yes | Source plugin name |
| `exported_from.plugin_version` | string | yes | Source plugin version |
| `exported_from.export_date` | string | yes | ISO 8601 date |

## Installation Behavior

When importing a manifest:

1. Check `format_version` — reject if > supported version
2. Check `dependencies.depends_on` — warn if any are missing locally
3. Check `dependencies.required_scripts` — warn if any are missing
4. Register skill with `source: "custom"` (not original source)
5. Recompute `auto_score` locally (don't trust exported score)
