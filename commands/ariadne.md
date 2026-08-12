---
name: ariadne
description: Triage stale working-idea threads across configured project vaults — advance, sharpen, snooze, or drop, with every decision written back to the ledger
argument-hint: "[vault] [--all | --digest | --table]"
---

You are activating the Ariadne thread-triage skill.

1. Fetch the full skill: use `mcp__skill-library__get_skill` with `skill_name: "ariadne"` (include references).
2. Read the returned SKILL.md and its `references/setup-and-config.md` completely.
3. Execute the skill's 5-step process with runtime arguments: `$ARGUMENTS`
4. Honor the Non-Negotiables verbatim — especially: `status: dropped` only on the user's explicit word, and no paths beyond what the local config names.
5. If the config at `~/.config/ariadne/config.json` is missing, walk the user through setup per the reference doc instead of scanning anything.

If `$ARGUMENTS` is empty, run the default interactive triage across all configured vaults.
