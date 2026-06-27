---
name: scheherazade
description: Run the agentic world→character→story loop — generate or extend a fictional world and write a story in it, gated by the critic suite (consistency · quality · macro) with human checkpoints at the creative forks
argument-hint: "<seed/premise to build from, or a pointer to an existing world>"
---

You are activating the Scheherazade narrative meta-orchestrator.

1. Fetch the full skill: use `mcp__skill-library__get_skill` with `skill_name: "scheherazade"` (include references).
2. Read the returned SKILL.md and both reference docs (`build-order-dag`, `loop-protocol`) completely.
3. Determine the **mode** from `$ARGUMENTS`: **greenfield** (a premise/genre to build a new world from) or **brownfield** (a pointer to an existing world-bible/vault to draft in). Confirm the `medium` (selects the quality-critic profile) and the `world_state` location.
4. Drive the loop per the skill: Phase A (world build — greenfield, or brownfield gaps only) → Phase B (story loop), gating every step through the critic suite — **consistency** (hard gate) → **quality** (soft gate, scene) → **whole-story-judge** (macro gate, chapter/draft) — with human checkpoints at the four creative forks (tone/medium · central system · central conflict · protagonist).
5. Use the allowed tools in the skill frontmatter: Read, Write, Bash, Glob, Grep, Agent.
6. Honor the loop protocol: hard gates reject (never flag), caps are upper bounds (stop early on a pass), and a non-empty stub-queue must be drained before the draft is done.

If `$ARGUMENTS` is empty, ask the user for a seed (premise/genre) **or** an existing world to write in, plus the medium.
