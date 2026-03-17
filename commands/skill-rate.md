---
description: Rate a skill with a manual score and optional notes
argument-hint: "<skill-name> <1-5> [optional notes]"
---

Rate a skill with a manual usefulness/satisfaction score.

Parse `$ARGUMENTS` for:
1. Skill name (required) — first argument
2. Rating (required) — integer 1-5
3. Notes (optional) — remaining text

Steps:
1. Read `data/registry.json`
2. Find the skill by name. If not found, list available skills and ask the user to pick one.
3. Update `manual_rating` with the given score (1-5)
4. Update `manual_notes` with the given notes (or leave unchanged if no notes provided)
5. Recompute `composite_score`: `round(auto_score * 0.7 + (manual_rating / 5 * 100) * 0.3)`
6. Append changelog entry: `{date, action: "rated", note: "Manual rating: X/5"}`
7. Write updated registry

Confirm the update to the user:
```
Rated skill-registry: 4/5
Notes: "Core infrastructure, reliable and well-structured"
Composite score: 85 → 84 (auto: 85, manual: 4/5)
```

Rating scale:
- 5: Essential, use frequently, works perfectly
- 4: Very useful, reliable
- 3: Useful but has issues
- 2: Rarely useful
- 1: Unused or broken
