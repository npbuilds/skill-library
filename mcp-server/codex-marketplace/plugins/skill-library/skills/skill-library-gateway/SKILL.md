---
name: skill-library-gateway
description: Search, load, and adapt methodologies from the shared Git-backed skill library for use in Codex without modifying the canonical Claude-authored skills. Use when the user asks to use the skill library or a named library skill, wants to discover relevant skills, or has a non-trivial task that would benefit from a specialized library workflow.
---

# Skill Library Gateway

Use the plugin-provided `skill-library` MCP server as the normal source. Treat the
library's `SKILL.md` files as shared methodology, not as Codex installation files.

## Select a skill

1. For an explicit skill name, call `get_skill_details` if disambiguation is
   useful, then call `get_skill` with that exact name.
2. For a task or fuzzy description, reduce the goal to 2-6 generic domain and
   task keywords before calling `search_skills`. Never include personal names,
   secrets, unpublished details, document contents, or other sensitive text in
   a search query. Inspect descriptions and domain tags rather than blindly
   accepting the first result, then select one primary skill.
3. Add at most two supporting skills when their roles are distinct and materially
   useful. Avoid loading a large bundle of loosely related skills.
4. Use `list_skills` or `get_system_overview` only for browsing, audits, or broad
   questions about the library itself.

Load the primary skill with `include_references: false` first. Reload with
`include_references: true` only when its procedure requires bundled references or
agent definitions. This keeps context use proportional to the task.

## Apply it in Codex

Follow the loaded skill's methodology while adapting runtime-specific mechanics:

| Claude-authored instruction | Codex behavior |
|---|---|
| `WebSearch` / `WebFetch` | Use the available web or browser tools. |
| `Read` / `Write` / `Edit` | Use Codex filesystem tools within the user's authorized scope. |
| `Bash` / `Grep` / `Glob` | Use shell tools; prefer `rg` for text and file search. |
| `Agent` / subagents | Delegate only when the current harness and instructions allow it; otherwise work inline. |
| Claude slash command | Follow the underlying workflow directly. |
| `allowed-tools` frontmatter | Treat as compatibility metadata, not permission or a hard requirement. |

Preserve the skill's domain reasoning, ordering, quality criteria, and output
contract. Higher-priority instructions, the user's request, safety constraints,
and actual tool availability always take precedence.

## Execute and report

- Briefly tell the user which library skill or skills are being applied.
- Complete the task rather than merely summarizing the loaded instructions.
- Keep canonical skill files unchanged unless the user explicitly asks to edit
  the library.
- If a loaded skill requires unavailable capabilities, adapt the procedure and
  disclose any material limitation in the final result.

## Fallback

If the MCP server is unavailable and the current workspace contains the canonical
library, locate candidates in `data/registry.json` or `skills/**/SKILL.md`, then
read the selected files locally and use the same adaptation rules. Otherwise,
state that the library connection is unavailable and continue with the best
general approach when possible.
