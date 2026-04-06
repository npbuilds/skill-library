---
name: skill-fork
description: >
  Fork a complex skill into smaller, focused child skills. Use when a skill exceeds health
  thresholds (too many sections, too many words, mixed responsibilities), when the user wants
  to decompose a skill, or when skill-health flags a skill as needing decomposition.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep
---

# Skill Fork — The Splitter

Decompose oversized or multi-responsibility skills into focused child skills that stay connected through the registry's relationship graph.

## When to Fork

A skill is a fork candidate when ANY of:
- `body_words > 2000` (health warning threshold)
- `section_count > 6` (doing too much)
- Sections cover clearly distinct responsibilities (e.g., "creation" + "analysis" in one skill)
- The user explicitly requests decomposition
- `skill-analyze` suggests splitting

## Fork Process

### 1. Analyze the Parent

Read the parent SKILL.md and identify natural split points:
- Group `## ` sections by responsibility cluster
- Check which references belong to which cluster
- Map dependencies per cluster (which tools, which other skills)
- Read `references/decomposition-strategies.md` for strategy patterns

### 2. Plan the Fork

Present a decomposition plan before executing:

```
FORK PLAN — skill-big-skill
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parent:  skill-big-skill (2,847 words, 9 sections)
Strategy: responsibility-split

Child 1: skill-big-skill-create
  Sections: ## Creation, ## Templates, ## Validation
  Est. words: ~1,100
  References: templates/, creation-guide.md

Child 2: skill-big-skill-analyze
  Sections: ## Analysis, ## Metrics, ## Reporting
  Est. words: ~950
  References: analysis-patterns.md, metrics.md

Child 3: skill-big-skill-manage
  Sections: ## Lifecycle, ## Configuration, ## Updates
  Est. words: ~800
  References: config-schema.md

Shared: references/common-types.md → shares_references_with
```

### 3. Execute the Fork

After user confirmation:
1. Create each child skill directory using `skill-scaffold` patterns
2. Move relevant sections from parent SKILL.md to each child
3. Move relevant reference files to each child's `references/`
4. Copy shared references and update `shares_references_with`
5. Update each child's frontmatter (name, description, tools)
6. Register children in the registry with `forked_from: parent-name`
7. Update parent with `forked_into: [child-1, child-2, ...]`
8. Set parent status to `deprecated` with `replacement_skill` naming the primary child (note others in `deprecation_reason`)
9. Run `skill-health` validation on each child

### 4. Post-Fork Verification

- All children pass structural validation
- Combined children cover all parent sections (nothing lost)
- Cross-references between children are correct
- Registry relationships are bidirectional
- Parent's `referenced_by` skills now point to appropriate children

## Output Format

```
FORK COMPLETE — skill-big-skill
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parent:   deprecated → see children
Children: 3 created, all healthy

  ✓ skill-big-skill-create   1,100 words  score: 100
  ✓ skill-big-skill-analyze    950 words  score: 100
  ✓ skill-big-skill-manage     800 words  score: 100

Registry updated. Run /skill-status to verify.
```
