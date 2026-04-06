# Skill Fork — Quick Reference


## Formula / Pseudocode

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
