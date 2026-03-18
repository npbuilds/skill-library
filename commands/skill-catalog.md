---
name: skill-catalog
description: Browse and search the skill catalog with filtering
argument-hint: "Optional filter: domain:<tag>, type:<action|knowledge|orchestrator>, health:<healthy|warning|critical>, source:<self|custom|external>"
---

Read `data/registry.json` and display skills in a browsable catalog format.

If `$ARGUMENTS` contains a filter (e.g., `domain:infrastructure`, `type:action`, `health:warning`, `source:external`), apply it. Multiple filters can be combined with spaces.

**Without filters:** Group skills by domain tag. Show name, type, description (truncated to 60 chars), score, and token cost for each.

**With filters:** Show matching skills in a flat table with full details.

For each skill, show: name, type, source, health, score, tokens, and first line of description.

Format as ASCII tables grouped by domain. If a skill has no domain tag, group under "(untagged)".
