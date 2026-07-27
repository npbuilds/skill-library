---
name: emptor
description: Rigorous consumer purchase research — elicit needs first, search trusted sources only, verify finalists, deliver a cited recommendation brief
argument-hint: "<what you need, e.g. 'robot vacuum under $400 for pet hair'>"
---

You are activating the Emptor consumer-research orchestrator.

1. Fetch the full skill: use `mcp__skill-library__get_skill` with `skill_name: "emptor"` (include references). If the MCP server is unavailable, read `skills/consumer-research/emptor/SKILL.md` and its references directly.
2. Read the returned SKILL.md and reference documents completely.
3. Execute the 9-phase pipeline (Phases 0-8) against the purchase need: `$ARGUMENTS`
4. Select depth mode per the skill's table — budget-proportional (≲$50 → quick; ≳$500 or safety-relevant → deep; otherwise standard). Honor explicit `--quick`/`--standard`/`--deep` flags in `$ARGUMENTS`.
5. **Hard rule: no WebSearch/WebFetch before the requirements spec is signed off in Phase 1.** Budget is locked before any price is shown.
6. Deliver the EMPTOR BRIEF per the output contract with a `CRS-YYYYMMDD-<slug>` brief ID, then run Phase 8 journaling (JSONL + `research/consumer-briefs/` + vault mirror when reachable).

If `$ARGUMENTS` is empty, ask what they're looking to buy.
