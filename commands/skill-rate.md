---
name: skill-rate
description: Rate a skill with a manual score and optional notes
argument-hint: "<skill-name> <1-100> [optional notes]"
---

Rate a skill with a manual usefulness/satisfaction score.

Parse `$ARGUMENTS` for:
1. Skill name (required) — first argument
2. Rating (required) — integer 1-100
3. Notes (optional) — remaining text

Steps:
1. Read `data/registry.json`
2. Find the skill by name. If not found, list available skills and ask the user to pick one.
3. Use the MCP `update_skill_metadata` tool to set `manual_rating` and
   `manual_notes`. If the MCP tool is unavailable, update those fields while
   preserving every unrelated registry field.
4. Update `manual_notes` with the given notes (or leave unchanged if no notes provided)
5. Recompute `composite_score` with the canonical policy:
   `round(auto_score * 0.60 + manual_rating * 0.40)`.
6. Append changelog entry: `{date, action: "rated", note: "Manual rating: X/100"}`
7. Write updated registry

Confirm the update to the user:
```
Rated skill-registry: 84/100
Notes: "Core infrastructure, reliable and well-structured"
Composite score: 85 → 85 (auto: 85, manual: 84/100)
```

Rating scale:
- 90-100: Essential, excellent, and reliable
- 75-89: Strong and useful; minor improvements possible
- 50-74: Useful but has notable gaps
- 25-49: Weak or rarely useful
- 1-24: Broken, misleading, or effectively unused
