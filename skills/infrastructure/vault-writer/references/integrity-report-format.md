# Integrity Report Format (for vault-writer output)

The structured report vault-writer returns to the calling orchestrator.

## Format

```
INTEGRITY REPORT — vault-writer
────────────────────────────────
Wrote: <absolute path to primary file>
Wrote (companion): <absolute path | "none">
Logged: <log line as appended>
Indexed: <"section / subsection" | "skipped per index_entry: false">
Schema validated against: <vault_path>/_meta/frontmatter-schema.md (modified <YYYY-MM-DD>)
Overwrite policy applied: <fail | overwrite | append>

Unresolved wikilinks in artifact_body:
  - [[some-name]] — no Notes/some-name.md exists
  - [[other-name]] — no matching file in any vault folder
  (or: "(none)")

Warnings:
  - <text>
  (or: "(none)")

Status: <success | partial | failed>
```

## Status semantics

| Status | Meaning |
|---|---|
| `success` | All writes completed; vault state is consistent |
| `partial` | Primary write succeeded; one or more of {companion, log, index} failed. Vault state is partially updated; calling orchestrator should decide whether to roll forward or fix manually |
| `failed` | No writes performed; vault state unchanged |

## What the orchestrator does with the report

- **Always log it.** The calling skill should attach the report to its own session log so failures are auditable.
- **Stub-creation decision.** If `Unresolved wikilinks` is non-empty and the orchestrator wants graph completeness, it can call vault-writer again for each missing link with a stub body. This is the orchestrator's choice, not vault-writer's.
- **Partial recovery.** On `partial` status, the orchestrator can:
  - Retry the failed sub-step (e.g., re-attempt index update with a corrected section name)
  - Surface the partial state to the user
  - Roll forward (accept the partial write as the new state)
- **Schema drift detection.** The "Schema validated against" line tracks the schema's mtime. If two consecutive vault-writer calls show different mtimes, the schema changed mid-session — the orchestrator may want to flag this.
