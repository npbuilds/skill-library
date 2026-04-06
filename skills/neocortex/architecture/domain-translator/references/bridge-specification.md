# Bridge Specification — Actionable Wiring Template

When domain-translator identifies a viable translation, use this template to produce an actionable bridge spec that can be directly executed. A bridge is not just a conceptual insight — it's a set of concrete edits.

## What a Bridge Consists Of

Every cross-domain bridge has three layers:

| Layer | What It Is | Where It Lives |
|-------|-----------|---------------|
| **Registry edges** | `depends_on` / `referenced_by` entries linking the two skills | `data/registry.json` |
| **SKILL.md cross-references** | Cross-Domain Connections sections naming the partner skill and explaining the relationship | Both skills' SKILL.md files |
| **Shared concept** (optional) | A reference doc explaining the structural core that both domains share | Either skill's `references/` directory, or a shared location |

## Bridge Spec Format

```
BRIDGE SPEC — [Source Skill] ↔ [Target Skill]
Domains: [domain-a] ↔ [domain-b]
Bridge Type: [parallel / isomorphism / shared-tool / dependency]
Confidence: [high / medium / low]

─── Structural Core ───
[One sentence: the domain-independent principle these skills share]

─── Registry Edits ───
  Source skill ([name]):
    depends_on: + [target-skill-name]
  Target skill ([name]):
    referenced_by: + [source-skill-name]

  (or vice versa — use depends_on for "needs knowledge from"
   and referenced_by for "provides knowledge to")

─── SKILL.md Edits ───
  In [source-skill]/SKILL.md, add to Cross-Domain Connections:
    "- **[domain-b]/[target-skill]**: [one-line relationship description]"

  In [target-skill]/SKILL.md, add to Cross-Domain Connections:
    "- **[domain-a]/[source-skill]**: [one-line relationship description]"

─── Shared Reference (if needed) ───
  Create: [path]/references/[name].md
  Content: [brief description of what the shared concept doc should cover]

─── Translation Notes ───
  Where it holds: [what transfers cleanly]
  Where it breaks: [honest limits]

─── Payoff ───
  [What both domains gain from this bridge being active]
```

## Bridge Types

| Type | Description | Example |
|------|------------|---------|
| **Parallel** | Same architecture, different content — skills structured identically | mechanism-design ↔ magic-system-design |
| **Isomorphism** | Different names for the same underlying concept | reflexivity (investing) ↔ feedback loops (game-theory) |
| **Shared-tool** | One domain's methodology directly serves another | statistical-testing (data-science) → model-evaluation (investing) |
| **Dependency** | One skill genuinely needs another to function well | time-series (data-science) → macro-cycles (investing) |

## Bridge Bundles

When connecting two domains, bridges often come in bundles — a set of related bridges that should be wired together. Document the full bundle before executing:

```
BRIDGE BUNDLE — [Domain A] ↔ [Domain B]
Total bridges: [N]

1. [skill-a] ↔ [skill-b]: [type] — [one-line core]
2. [skill-a2] ↔ [skill-b2]: [type] — [one-line core]
...

Wiring order: [which bridges to do first, based on dependencies]
```

## Quality Checks

Before executing a bridge spec:

| Check | Question |
|-------|---------|
| **Real vs. forced** | Would an expert in both domains agree this connection is meaningful? |
| **Bidirectional value** | Does both sides benefit, or is it one-way? |
| **Actionable** | Can a user invoking skill A actually benefit from knowing about skill B? |
| **Not redundant** | Does this bridge already exist under a different name? |
| **Correct direction** | Is the depends_on / referenced_by direction right? (depends_on = "I need this"; referenced_by = "this uses me") |
