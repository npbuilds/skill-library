# Codex Result — Spelunker

Runtime observations:

- Current Codex desktop task: methodology and output-contract execution completed.
- Codex CLI 0.142.5 with `gpt-5.4`: canonical skill and all three references loaded, but automated primary-source web search stalled and the run was stopped before synthesis.

Status: **PASS in Codex desktop; BLOCKED in the installed Codex CLI**

## Desktop user-facing result

RESEARCH BRIEF
CORE CLAIM CONFIDENCE: Confirmed
Brief ID: SPK-20260719-shared

The same core Agent Skills directory can be consumed by Claude Code and Codex without duplicating its instructions, because both implement the `SKILL.md` directory model. Discovery locations, plugin manifests, invocation controls, permissions, and tool names remain client-specific and need thin adapters. [1][2][3]

KEY FINDINGS

- Both clients consume a directory containing `SKILL.md`, optional scripts, references, and assets. [1][2][3]
- Claude discovers project skills through `.claude/skills/`; Codex discovers repository skills through `.agents/skills/`. [1][2]
- Claude plugins use `.claude-plugin/plugin.json`, while Codex plugins use `.codex-plugin/plugin.json`; both can point at a root `skills/` collection. [1][2]
- `allowed-tools` is experimental in the shared specification, so support and permission semantics may vary by client. [3]

DETAILED FINDINGS

Core format — Confidence: Confirmed because OpenAI, Anthropic, and the Agent Skills specification describe the same `SKILL.md`-centered directory structure. [1][2][3]

Execution parity — Confidence: Likely because instruction and reference content is portable, but vendor-specific constructs such as Claude's `$ARGUMENTS`, `context: fork`, dynamic command injection, and permission behavior require adaptation rather than blind reuse. [1][2][3]

EVIDENCE MAP

- Shared directory format ↔ Sources 1, 2, and 3.
- Discovery and plugin differences ↔ Sources 1 and 2.
- Variable tool-field support ↔ Source 3.

GAPS & LIMITATIONS

- Quick mode was used; no adversarial pass was performed.
- The installed Codex CLI's web-search path stalled, although the current Codex desktop environment could access the documentation.
- No authenticated Claude CLI execution was available for a fresh side-by-side output comparison.

CONFIDENCE SUMMARY

Confirmed: 2 · Likely: 1 · Speculative: 0 · Contested: 0 · Unverifiable: 0

SOURCES

1. OpenAI, "Build skills" and "Build plugins," accessed 2026-07-19, Tier 1, Used for: Codex structure, discovery, and packaging — https://learn.chatgpt.com/docs/build-skills and https://learn.chatgpt.com/docs/build-plugins
2. Anthropic, "Extend Claude with skills," accessed 2026-07-19, Tier 1, Used for: Claude structure, discovery, invocation, and plugins — https://code.claude.com/docs/en/slash-commands
3. Agent Skills, "Specification," accessed 2026-07-19, Tier 1, Used for: common fields and portability boundary — https://agentskills.io/specification

NEXT STEPS

- Keep canonical instructions shared.
- Preserve client-specific manifests and runtime adapters separately.
- Validate tool-heavy skills on each client before declaring full operational parity.

─────────────────────────────────────
Was this brief useful? Reply `/feedback spelunker <1-5> [optional notes]` to log.
Brief ID: SPK-20260719-shared · Calibrate later: `/calibrate <brief_id> <claim_id> <true|false|partial>`

## Evaluation

| Dimension | Score | Evidence |
|---|---:|---|
| Activation | 100 | Read the canonical skill and all references |
| Relevance | 100 | Answered the narrow portability question |
| Format | 100 | Satisfied the eight-section Spelunker output contract and footer |
| Completeness | 100 | Addressed shared format, discovery, packaging, tools, sources, and gaps |

Desktop weighted score: **100/100**

CLI automation status: **BLOCKED**, not scored. The failure occurred in runtime web search after successful skill activation.
