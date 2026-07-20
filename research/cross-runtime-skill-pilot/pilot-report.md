# Cross-Runtime Skill Compatibility Pilot — Results

Date: 2026-07-19

## Outcome

**CONDITIONAL GO**

The shared-core architecture and MCP-backed Codex gateway work for instruction, reference, transformation, and orchestrator behavior without modifying the canonical Claude-authored skills. Fresh Claude-versus-Codex parity remains unmeasured because the installed Claude CLI is not authenticated.

## Results

| Case | Canonical structure | Codex desktop | Codex CLI | Claude CLI | Result |
|---|---|---:|---:|---:|---|
| Color theory | PASS | Not run | 100/100 | Blocked: unauthenticated | Codex PASS |
| Prose editor | PASS | Not run | 100/100 | Blocked: unauthenticated | Codex PASS |
| Spelunker | PASS | 100/100 | Blocked: web search stalled | Blocked: unauthenticated | Desktop PASS; CLI tooling block |

## Gateway follow-up

The additive gateway proof completed after the initial pilot:

- A repo-local Codex marketplace and `skill-library` plugin were created under `mcp-server/codex-marketplace/`.
- The plugin installs one native `skill-library-gateway` skill instead of registering all canonical skills.
- The deployed MCP endpoint passed protocol initialization and exposed the required library tools.
- Codex CLI retrieved `color-theory`, retrieved and applied `prose-editor`, and retrieved `spelunker` with all three references.
- An explicit five-tool allowlist prevents the plugin from exposing non-gateway server operations.
- Remote search telemetry omits raw query text by default, while preserving the existing local Claude telemetry behavior.
- The collision-safe `skill-building-local` marketplace and updater remove the legacy `@personal` installation.
- No canonical skill or Claude workflow surface changed.

See `result-codex-gateway.md` for the validation record.

## What the pilot established

1. Codex can read unchanged skills whose frontmatter says `Designed for Claude Code`.
2. Codex followed progressive disclosure by loading local references when relevant.
3. Claude tool names in `allowed-tools` did not prevent read-only Codex execution.
4. The generic instruction to adapt platform-specific tools was sufficient for the first two cases.
5. The strictest output contract, Spelunker, was reproducible in the current Codex desktop environment.
6. No protected Claude workflow surface changed.

## Runtime findings

These are environment issues rather than canonical skill defects:

- Claude Code 2.1.193 is installed but reports `loggedIn: false`, with no `ANTHROPIC_API_KEY` present.
- Codex CLI 0.142.5 is too old for the configured `gpt-5.6-sol` model, so CLI cases used explicit `gpt-5.4`.
- The CLI's model cache emitted schema warnings.
- The tool-heavy CLI case stalled while using web search and was stopped cleanly.

## Protected-surface verification

No changes were detected under:

- `skills/`
- `.claude/`
- `.claude-plugin/`
- `commands/`
- `agents/`
- `hooks/`
- `CLAUDE.md`
- `AGENTS.md`

The only pilot additions are under `research/cross-runtime-skill-pilot/`. The pre-existing modifications to `data/frontier-scans.jsonl` and `data/usage.jsonl` were left untouched.

## Decision

Proceed with an additive Codex adapter proof of concept, but do not bulk-edit or relocate the canonical skills. The next proof should add one repo-scoped Codex gateway skill, rerun these cases through native skill discovery, and repeat the Claude side after authentication.

## Recommended gate for broader rollout

Broader rollout should wait until:

1. Claude produces fresh baselines for these same prompts.
2. The installed Codex CLI is upgraded or the desktop app is selected as the supported Codex runtime.
3. One MCP-backed Codex gateway passes all three cases. **Complete.**
4. At least one Claude-specific construct (`$ARGUMENTS`, `Agent`, or `context: fork`) is exercised through an explicit adapter.
