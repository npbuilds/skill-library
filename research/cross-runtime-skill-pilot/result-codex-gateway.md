# Codex Gateway Validation

Date: 2026-07-19

## Outcome

**PASS**

The installed Codex plugin loaded the gateway skill and retrieved unchanged
canonical skills through the deployed Skill Library MCP server.

## Checks

| Check | Result |
|---|---|
| Gateway skill validator | PASS |
| Plugin validator | PASS |
| Marketplace installation | PASS |
| MCP protocol initialization | PASS — 10 server tools discovered |
| Codex tool restriction | PASS — 5 content-retrieval tools allowlisted |
| `color-theory` retrieval | PASS — canonical heading returned |
| `prose-editor` retrieval and application | PASS |
| `spelunker` plus references retrieval | PASS — 3 references returned |
| Remote search-query privacy | PASS — text omitted by default; explicit opt-in tested |
| Marketplace migration | PASS — legacy `@personal` installation removed |
| Protected Claude surfaces | PASS — unchanged |

## Runtime finding

The first CLI calls were canceled because plugin MCP reads inherited interactive
approval behavior. Adding `default_tools_approval_mode: "approve"` together with
an explicit five-tool allowlist fixed non-interactive execution. A fresh Codex
CLI session then returned the canonical `color-theory` content through
`get_skill`.

The gateway also returned all Spelunker references:

- `confidence-framework.md`
- `domain-routing.md`
- `quick-reference.md`

Its required output contract remained intact:

1. `RESEARCH BRIEF`
2. `KEY FINDINGS`
3. `DETAILED FINDINGS`
4. `EVIDENCE MAP`
5. `GAPS & LIMITATIONS`
6. `CONFIDENCE SUMMARY`
7. `SOURCES`
8. `NEXT STEPS`

The older Codex CLI's separate web-search stall remains a runtime limitation for
full Spelunker research, not a gateway retrieval failure.

## Hardening follow-up

The marketplace now uses the repository-specific name `skill-building-local`
instead of the collision-prone `personal`. The updater removes the exact legacy
installation before reinstalling the current plugin, preventing duplicate skill
and MCP registration.

Search telemetry is runtime-aware: local stdio mode retains query text for the
existing Claude workflow, while remote mode records result counts without raw
query text unless the service owner explicitly sets
`TELEMETRY_SEARCH_QUERIES=1`. This applies whether remote mode is selected by
environment variable or the `--remote` CLI flag. The gateway independently
reduces fuzzy searches to short, non-sensitive keywords.

The follow-up bug pass also closes four failure paths: explicit HTTP transports
now enforce restricted remote mode, Firestore telemetry gating follows late
`--remote` activation, redacted gaps render as meaningful aggregate events, and
the updater verifies the replacement before removing the legacy installation.
Microsecond-resolution cachebusters prevent rapid update collisions.

The final failure-path pass makes remote restriction fail closed and idempotent,
rolls back partial or cache-mismatched plugin installations together with the
source manifest, and accepts valid SemVer containing both prerelease and build
metadata.
