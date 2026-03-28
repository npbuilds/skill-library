# Skill Style Guide

Standards for skill structure, size, and metadata. Every new skill must conform; existing skills should migrate at next edit.

---

## Token Budget Caps

These limits ensure skills fit within Claude's effective reasoning window when loaded alongside context blocks and user prompts.

| Type | Max Tokens | Max Words | Max Sections | Rationale |
|------|-----------|-----------|-------------|-----------|
| **Orchestrator** | 4,000 | 2,500 | 15 | Loaded alone; needs room for context block + user prompt |
| **Director** | 3,000 | 1,800 | 12 | Loaded by orchestrator; routing tables + conflict rules |
| **Knowledge** | 5,000 | 3,000 | 20 | Loaded by director/agent; densest content type |
| **Action** | 4,000 | 2,500 | 12 | Loaded by agent; procedural steps + output template |
| **Observer** | 2,000 | 1,200 | 8 | Lightweight monitoring; should be fast to parse |

**Enforcement:** `scripts/validate-structure.sh` checks these limits. The `skill-file-watcher.sh` hook flags violations at write time.

**Over budget?** Split into a parent skill + child knowledge skills. Move reference material to `references/` files (loaded on demand, not counted against the budget).

---

## Required Frontmatter

Every SKILL.md must begin with YAML frontmatter:

```yaml
---
name: skill-name
description: >
  One to three sentences. Must be specific enough for search and routing.
  Describe WHEN to use this skill, not just WHAT it contains.
tools: Read        # Comma-separated tool list, or omit if knowledge-only
---
```

**Rules:**
- `name` must match the directory name exactly
- `description` must include activation triggers ("Use when...", "Activate for...")
- `tools` is optional for pure knowledge skills, required for action/orchestrator/director

---

## Required Sections by Type

### Orchestrator
1. **Guiding Principles** — 3-7 rules governing all routing decisions
2. **Classification / Routing Table** — Maps user intent to target skills
3. **Delegation Protocol** — What context to pass, in what order
4. **Synthesis** — How to harmonize multi-skill outputs

### Director
1. **Description** — When this director activates
2. **Child Skills** — Table of skill-id, file, and purpose
3. **Routing Table** — User signal → skill mapping with rationale
4. **Conflict Resolution** — Priority rules when multiple children match

### Knowledge
1. **Description** — What this skill teaches
2. **Core Content** — The actual knowledge (bulk of the skill)
3. *(Optional)* **Diagnostic Cues** — How to apply this knowledge in practice
4. *(Optional)* **Common Mistakes** — What to avoid

### Action
1. **Description** — What this skill produces
2. **Input** — What context/data it expects (the input contract)
3. **Process** — Step-by-step procedure
4. **Output** — Template or format specification (the output contract)

### Observer
1. **Description** — What it monitors
2. **Triggers** — When it activates
3. **Assessment Criteria** — What it evaluates
4. **Notification Format** — How it reports findings

---

## Naming Conventions

- **Directory names:** lowercase, hyphenated (`magic-system-design`, not `MagicSystemDesign`)
- **Skill names:** match directory name exactly
- **Orchestrators:** `{domain}-orchestrator` or a thematic name (e.g., `bacchus`, `archon`)
- **Directors:** named for their subdomain (`visual-communication`, `tasting-evaluation`)
- **Knowledge/Action:** named for their specific concern (`color-theory`, `pairing-engine`)

---

## Reference Files

- Store supplementary material in `references/` subdirectory
- References are loaded on demand, not counted against token budget
- Use for: taxonomies, lookup tables, extended examples, external standards
- Reference files must be `.md` format
- Name descriptively: `cms-deductive-grid.md`, not `ref1.md`

---

## Tags

Every registry entry must include at minimum:
- `domain:{domain}` — top-level directory (e.g., `domain:sommelier`)
- `layer:{type}` — skill type (e.g., `layer:knowledge`)

Optional but encouraged:
- `subdomain:{subdomain}` — grouping within domain
- `level:foundational` / `level:advanced` — depth indicator

---

## Anti-Patterns

1. **The God Skill** — A knowledge skill with 40+ sections trying to cover an entire field. Split it.
2. **The Orphan** — A skill with no `parent`, no `depends_on`, no `referenced_by`. Wire it into an orchestrator or delete it.
3. **The Ghost** — A registry entry whose file doesn't exist on disk. Run `sync-registry.py` to detect.
4. **The Drifter** — A skill whose on-disk metadata doesn't match its registry entry. Run `sync-registry.py` to detect.
5. **The Format Rebel** — A skill using inline metadata (`## skill-metadata`, `**Type:** X`) instead of YAML frontmatter. Migrate it.
