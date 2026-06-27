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

## Tier-2 — autonomous batch run (the code-driven loop)

The steps above are **Tier-1**: you drive the loop conversationally, by hand. If the user asks for an **autonomous / batch / unattended** run (signals: "batch", "autonomous", "run the whole chapter", "--batch", "use the workflow"), drive the loop as **code** instead — the Tier-2 driver is a deterministic Workflow that fans out generator/critic subagents and enforces the gates programmatically.

> ⚠️ This spawns many subagents (~a dozen per scene) — real token cost. Confirm the user wants the batch run before launching.

1. Gather the entry contract into one `args` object:
   - `world_state` — absolute path to the **read-only** canon vault (e.g. the project's private canon vault).
   - `scratch_root` — a writable run dir for drafts/logs (e.g. `output/scheherazade/<run-id>`). **Canon is never written.**
   - `chapter_brief` — an ordered array of scene beats to draft (each may carry an `id`).
   - `medium` — `literary | genre | rpg | childrens | experimental` (selects the quality-critic profile).
   - `caps` — `{ revisions: 3, quality_revisions: 3 }` (per-gate revision caps).
   - *(This MVP is brownfield-only — there is no `mode` arg. The cost ceiling is set at the harness/turn level, e.g. a "+Nk" budget directive — not passed via args.)*
2. Invoke the driver: call the **Workflow** tool with `scriptPath: "skills/narrative/scheherazade/tier2/scheherazade.workflow.js"` and the `args` above. (It lives there, not in `.claude/workflows/`, because `.gitignore` ignores `.claude/*` — invoke by `scriptPath`, not `name`.)
3. Relay the returned `result`:
   - `awaiting_signoff` — passed every gate incl. the macro judge; present the macro verdict + any `flags`, get the user's sign-off, then **re-invoke with `args.human_signoff: true`, `args.commit_manifest` set to this result's `accepted` array, and `args.macro`**. This commits the *exact* drafts reviewed — it does not regenerate.
   - `macro_fail` — structural problem (dropped setup / arc / coherence); report the diagnosis, no commit.
   - `escalated` — a scene couldn't pass its gates within caps (or an agent died / budget hit); report `reason` for human review.
   - `canon_breach` — a write landed outside `scratch_root`; stop and investigate.
   - `committed` — done; report `committed_paths` + the run-journal.
4. Tier-2 runs autonomously per scene; the only human gate is the macro/draft sign-off (the four creative forks live in Phase A / greenfield, which this MVP does not yet drive).
