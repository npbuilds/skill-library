# Retrieval Report Format (for vault-reader output)

The structured report vault-reader returns to the calling skill. Mirrors vault-writer's `integrity-report-format.md` in shape — same audit-trail discipline, different content.

## Format

```
RETRIEVAL REPORT — vault-reader
────────────────────────────────
Query: {operation: <op>, parameters: <pretty-printed>}
Searched: <N> markdown files across <M> folders [<folder list>]
Schema validated against: <vault_path>/_meta/frontmatter-schema.md (modified <YYYY-MM-DD>)
Matched: <K> notes (after filters)

Results:
  1. <absolute path>
     - frontmatter: {type, domain, status, confidence, maturity, last_verified, tags}
     - excerpt: "<first <excerpt_chars> chars>" (or "full body: <body>" when full_body: true)
     - inbound links: <count> [list when graph op]
     - outbound links: <count> [list when graph op, each tagged vault | skill-library-ref | unresolved]
  2. ...

Skipped (no valid frontmatter):
  - <path>
  (or: "(none)")

Limitations:
  - Folders not searched: <list of subfolders excluded>
  - Filters applied: <list including which had effect>
  - Truncated to <max_results>; <N_total> total matches before cap (when applicable)
  - Archived-excluded: <K_arch> notes matched but were excluded by include_archived: false (when applicable)
  - Schema changed during session: <prior_mtime> → <current_mtime> (when applicable)

Status: <success | partial | failed>
```

## Status semantics

| Status | Meaning |
|---|---|
| `success` | Query executed; results returned (possibly empty); no errors |
| `partial` | Query executed but some folders / files could not be read; non-fatal |
| `failed` | Query rejected (schema validation, parameter validation, vault not found); no results to return |

## What the calling orchestrator does with the report

- **Pre-check decision.** If `Matched: K > 0` with `confidence >= likely`, the orchestrator can surface those results to the user before proceeding with expensive external work. The user decides "this is sufficient" vs "re-verify anyway."
- **Schema-drift detection.** The "Schema validated against (modified ...)" line tracks the schema's mtime. If two consecutive vault-reader calls in a session show different mtimes, the schema changed mid-session — surface this; consider re-validating prior results.
- **Truncation handling.** When `Truncated to N` is present, the orchestrator can decide whether to re-query with a higher `max_results` or accept the cap.
- **Empty-result handling.** `Matched: 0` is a finding, not an error. "No prior investigation on this topic" is useful information for the orchestrator's Phase 1.
- **Unresolved-link handling.** For `graph` operations, `unresolved` outbound links indicate missing notes the orchestrator might propose creating; `skill-library-ref` links indicate intentional cross-substrate references.

## Performance notes

- Report generation should be a small fraction of total query time. If composing the report dominates, the file walk is too fast — performance ceiling is elsewhere.
- The report intentionally omits large arrays unless requested. Full link lists are returned only on `graph` op. Full bodies only when `full_body: true`. Excerpts default to 300 chars.
