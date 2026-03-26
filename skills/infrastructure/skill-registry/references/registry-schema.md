# Registry Schema Reference (v1)

## Root Structure

```json
{
  "schema_version": 1,
  "plugin_version": "1.0.0",
  "last_scan": "2026-03-17T12:00:00Z",
  "skills": { "<skill-slug>": { ... } },
  "network": {
    "domains": { "<domain-tag>": ["skill-a", "skill-b"] },
    "shared_references": { "<abs-path>": ["skill-a", "skill-b"] }
  }
}
```

## Skill Entry Fields

### Identity
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Skill identifier (kebab-case, matches directory name) |
| `description` | string | yes | First sentence of the skill's description field |
| `location` | string | yes | Absolute path to SKILL.md |
| `plugin` | string | yes | Parent plugin name, or "skill-infra" for self |
| `type` | enum | yes | `knowledge`, `action`, or `orchestrator` |
| `source` | enum | yes | `self` (infra's own), `custom` (user-built), `external` (installed) |

### Config
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `context_mode` | enum | `inline` | `inline` or `fork` |
| `invocation` | enum | `both` | `both`, `user-only`, or `claude-only` |
| `version` | string | `1.0.0` | Skill version from frontmatter or default |

### Metrics (computed by analyze-skill.sh)
| Field | Type | Description |
|-------|------|-------------|
| `word_count` | int | Total words in SKILL.md |
| `body_words` | int | Words excluding frontmatter |
| `description_words` | int | Words in description field |
| `section_count` | int | Number of ## headings |
| `reference_files` | int | Files in references/ |
| `example_files` | int | Files in examples/ |
| `script_files` | int | Files in scripts/ |
| `template_files` | int | Files in templates/ |
| `estimated_tokens_metadata` | int | Tokens for description (always loaded) |
| `estimated_tokens_body` | int | Tokens for SKILL.md body (excluding frontmatter) |
| `estimated_tokens_total` | int | metadata + body |
| `precise_tokens` | int|null | Exact count via Anthropic API (when available) |

### Health
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `health_status` | enum | `healthy` | `healthy`, `warning`, or `critical` |
| `issues` | array | `[]` | List of `{severity, message}` objects |
| `last_checked` | string|null | ISO 8601 timestamp |

### Lifecycle
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | enum | `active` | `active`, `deprecated`, or `archived` |
| `deprecated_date` | string|null | ISO 8601 date when deprecated |
| `replacement_skill` | string|null | Name of replacement skill |
| `deprecation_reason` | string|null | Why this skill was deprecated |

### Ratings
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `auto_score` | int | 0 | Computed quality score (0-100) |
| `manual_rating` | int|null | User's rating (1-5) |
| `manual_notes` | string|null | User's comments |
| `composite_score` | int | 0 | Blended score: auto*0.7 + manual_scaled*0.3 |

### Relationships
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `depends_on` | array | `[]` | Skills this skill references or needs |
| `referenced_by` | array | `[]` | Skills that reference this skill |
| `shares_references_with` | array | `[]` | Skills sharing reference files |
| `forked_from` | string|null | Parent skill if this was forked |
| `forked_into` | array | `[]` | Child skills created by forking this |

### Metadata
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `tags` | array | `[]` | Strings like `domain:infrastructure`, `complexity:low` |
| `created` | string | current date | ISO 8601 date |
| `last_modified` | string | current date | ISO 8601 date |
| `changelog` | array | `[]` | List of `{date, action, note}` objects |

## Example Entry

```json
{
  "skill-registry": {
    "name": "skill-registry",
    "description": "Manage the skill registry — the central catalog of all skills in the mycelial network.",
    "location": "/Users/nirav/Desktop/Claude Playground/Skill Building/skills/skill-registry/SKILL.md",
    "plugin": "skill-infra",
    "type": "action",
    "source": "self",
    "context_mode": "inline",
    "invocation": "both",
    "version": "1.0.0",
    "metrics": {
      "word_count": 752,
      "body_words": 683,
      "description_words": 56,
      "section_count": 4,
      "reference_files": 1,
      "example_files": 0,
      "script_files": 0,
      "template_files": 0,
      "estimated_tokens_metadata": 73,
      "estimated_tokens_body": 1349,
      "estimated_tokens_total": 1422,
      "precise_tokens": null
    },
    "health_status": "healthy",
    "issues": [],
    "last_checked": "2026-03-17T00:00:00Z",
    "status": "active",
    "deprecated_date": null,
    "replacement_skill": null,
    "deprecation_reason": null,
    "auto_score": 100,
    "manual_rating": null,
    "manual_notes": null,
    "composite_score": 100,
    "depends_on": [],
    "referenced_by": [],
    "shares_references_with": [],
    "forked_from": null,
    "forked_into": [],
    "tags": ["domain:infrastructure"],
    "created": "2026-03-17",
    "last_modified": "2026-03-17",
    "changelog": [
      {"date": "2026-03-17", "action": "created", "note": "Initial registration during Phase 1 bootstrap"}
    ]
  }
}
```
