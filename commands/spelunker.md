---
name: spelunker
description: Deep research with epistemic rigor — investigates questions, verifies claims, and synthesizes findings with confidence tags
argument-hint: "<research question or topic>"
---

You are activating the Spelunker research orchestrator.

1. Fetch the full skill: use `mcp__skill-library__get_skill` with `skill_name: "spelunker"` (include references).
2. Read the returned SKILL.md and all reference documents completely.
3. Execute the skill's 6-phase methodology against the research question: `$ARGUMENTS`
4. Use the allowed tools listed in the skill frontmatter: Read, Write, Bash, Glob, Grep, Agent, WebSearch, WebFetch.
5. For generative questions ("what's the best X?", "how should we design X?"), route to `agentic-researcher` as specified in the skill.
6. Deliver the final research brief in Phase 6 format with confidence tags, gaps, and next steps.

If `$ARGUMENTS` is empty, ask the user what they'd like to research.
