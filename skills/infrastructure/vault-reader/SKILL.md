---
name: vault-reader
description: >
  Read structured artifacts from an Obsidian vault following the vault's CLAUDE.md frontmatter schema.
  Supports four operations: slug lookup, frontmatter filter (with `where` predicates validated against
  the schema), 1-hop wikilink graph, and substring/regex text search. Strictly read-only — never
  writes to the vault, never creates cache files. Returns a retrieval report with matches, schema
  validation status, and filter audit trail. Use when a calling skill needs to check "does this vault
  already have an answer / claim / context for X?" before doing expensive external work. Schema-strict
  and fail-closed — invalid queries are rejected rather than returning misleading results.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Bash Glob
---

# Vault Reader — The Other Half of the Bridge

The mirror of `vault-writer`. Where vault-writer turns conversation → vault (write-side), vault-reader turns vault → conversation (read-side). Together they form the read/write half of the `vault-bridge` suite: skills can both persist artifacts to the vault and query it before doing expensive external work.

vault-reader does one thing per invocation. It is not an orchestrator, not a search engine, and not a semantic-similarity engine. It reads the vault's existing frontmatter and content with schema-aware filters and returns honest results — including honest "nothing matched."

## Guiding principles

These are non-negotiable:

1. **Read-only, always.** No writes. No cache files. No side effects on the vault. The `allowed-tools` declaration enforces this; the skill's discipline enforces it more strongly.
2. **Schema-strict.** Reject queries whose field names or enum values are not in the vault's `_meta/frontmatter-schema.md`. Silent mismatch (caller queries `Confidence` when field is `confidence`) destroys query reliability over time.
3. **Fail closed on missing schema or invalid vault path.** Do not "best effort" against a non-vault directory.
4. **Always read fresh from disk.** No in-memory caching in v1. The vault is small; caching is premature.
5. **Folder-scope by default.** Default scope `[Notes/, skill-lab/]`. Excluding `Raw/`, `_meta/`, `_bases/`, `_templates/`, `00-Inbox/` by default. Override via explicit `folders` parameter.
6. **Honest about confidence and staleness.** Return `confidence` and `last_verified` in every result. Apply them as filters when requested, but do not rank — the caller decides what matters.
7. **Excerpts by default.** Full bodies opt-in via `full_body: true`. Default `excerpt_chars: 300`.
8. **`status: archived` excluded by default.** Opt-in via `include_archived: true`.
9. **Distinguish "not found" from "couldn't search."** No matches is a finding. Failed to access the vault is an error.
10. **No semantic search in v1.** Substring + regex + frontmatter filter + 1-hop wikilink graph only.

## How to Run

### Input

| Parameter | Required | Notes |
|---|---|---|
| `vault_path` | yes | Absolute path to the vault root |
| `operation` | yes | One of: `lookup`, `filter`, `graph`, `text-search` |
| `slug` | conditional | Required for `lookup` and `graph` |
| `where` | conditional | Required for `filter`; map of `field: value` constraints. Field names and values validated against schema |
| `pattern` | conditional | Required for `text-search`; substring (default) or regex (with `regex: true`) |
| `regex` | optional | Boolean. Default `false`. When true, `pattern` is treated as a regex |
| `folders` | optional | List of subfolder names relative to vault root. Default `["Notes/", "skill-lab/"]`. Special value `["all"]` includes all vault folders |
| `full_body` | optional | Boolean. Default `false` |
| `excerpt_chars` | optional | When `full_body: false`. Default `300` |
| `max_results` | optional | Cap on results. Default `25` |
| `min_confidence` | optional | One of `confirmed \| likely \| contested \| speculative \| unverifiable`. Notes whose `confidence` field meets-or-exceeds this in the ordering (`confirmed > likely > contested > speculative > unverifiable`) pass. Notes missing the `confidence` field are excluded by this filter |
| `max_staleness_days` | optional | Filter to notes whose `last_verified >= today - N`. Notes with empty or missing `last_verified` pass through (never-verified ≠ stale) |
| `include_archived` | optional | Boolean. Default `false` |
| `resolve_wikilinks` | optional | For `graph`, whether to resolve `[[name]]` to absolute paths. Default `true` |
| `known_skill_refs` | optional | For `graph` and unresolved-link reporting, a list of names that should be tagged as `skill-library-ref` rather than `unresolved`. Caller-provided |

### Steps

#### Step 1 — Read the vault schema

Read `<vault_path>/_meta/frontmatter-schema.md`. Extract:
- The `type:` enum values (from the Type registry section)
- The `domain:` enum values (from the Domain registry section)
- The `status:` enums per type
- The `confidence:` and `maturity:` enum values (from extension sections)
- The `source_type:` enum

Read `<vault_path>/CLAUDE.md` if present to detect any vault-specific overrides.

If the schema file is missing, fail the call before any further work: this is not a vault that vault-reader can operate against.

#### Step 2 — Validate query parameters

- `operation` is one of the four valid values
- Conditional parameters present for their operation (slug for lookup/graph; where for filter; pattern for text-search)
- For `filter`: every key in `where` is a field name documented in the schema; every value in `where` for an enum field is a valid enum value
- For `min_confidence`: value is in the confidence enum
- For `folders`: each folder (after resolving `["all"]`) exists as a directory under `<vault_path>`

Reject on any validation failure with a specific message pointing to the violating parameter and what the schema says is valid.

#### Step 3 — Execute the operation

**3a — lookup**
- For each folder in scope (in order), test `<vault_path>/<folder>/<slug>.md`
- First match wins; return full record with frontmatter + body (or excerpt)
- If no match, return empty results with explicit "tried these folders" in the report

**3b — filter**
- Walk all `.md` files in scoped folders (`Glob`)
- For each file, parse frontmatter (first `---`-delimited YAML block)
- Skip files without frontmatter; count them in the skipped list for the report
- Apply each predicate in `where`: a note matches when every predicate evaluates true
  - Scalar fields: exact match (`domain: meta` matches when frontmatter has `domain: meta`)
  - List fields (tags): set intersection (`tags: [pkm]` matches when `pkm` is in the note's tags)
- Return matching set

**3c — graph**
- Read the target note (same lookup logic as 3a)
- Extract outbound wikilinks from the body via regex: `\[\[([^\]|]+)(\|[^\]]+)?\]\]`
- For each, if `resolve_wikilinks: true`, search `Notes/<name>.md`, `skill-lab/<name>.md`, `_meta/<name>.md` in that order; tag resolution as one of `vault | skill-library-ref | unresolved`
- For inbound: grep across scoped folders for `\[\[<target-slug>(\|[^\]]+)?\]\]`
- Return both lists with resolution categories

**3d — text-search**
- Walk all `.md` files in scoped folders
- For each file, read post-frontmatter body (strip the leading `---` block)
- Apply `pattern` as substring (default) or regex (when `regex: true`)
- For each match, capture line number and 2 lines of surrounding context
- Return matches grouped by file

#### Step 4 — Apply post-filters

- `include_archived: false` excludes notes with `status: archived`
- `min_confidence`: applies the confidence ordering filter (notes without `confidence` excluded by this filter when set)
- `max_staleness_days`: applies the `last_verified` filter (notes without `last_verified` set, or with `last_verified: ""`, pass)

#### Step 5 — Apply `max_results` cap

Truncate to `max_results`. Report the truncation count in the report's Limitations section.

#### Step 6 — Compose the retrieval report

Read `references/retrieval-report-format.md` for the format spec.

### Output

A structured retrieval report (see `references/retrieval-report-format.md`):

```
RETRIEVAL REPORT — vault-reader
────────────────────────────────
Query: {operation: <op>, parameters: <…>}
Searched: <N> markdown files across <M> folders [<folder list>]
Schema validated against: <vault_path>/_meta/frontmatter-schema.md (modified <YYYY-MM-DD>)
Matched: <K> notes (after filters)

Results:
  1. <absolute path>
     - frontmatter: {type, domain, status, confidence, maturity, last_verified, tags}
     - excerpt: "<first <excerpt_chars> chars of body>"
     - inbound links: <count> [list if requested via graph op]
     - outbound links: <count> [list if requested via graph op]
  2. ...

Skipped (no valid frontmatter):
  - <path>
  (or: "(none)")

Limitations:
  - Folders not searched: <list>
  - Filters applied: <list>
  - Truncated to <max_results>; <N_total> total matches before cap (when applicable)

Status: success | partial | failed
```

## Error Handling

| Failure | Response |
|---|---|
| Schema file missing | Fail before any read; report `<vault_path>/_meta/frontmatter-schema.md` not found |
| Vault path is not a directory | Fail with the resolved path |
| `where` contains field not in schema | Fail; list valid field names |
| `where` value not in enum (e.g., `domain: investng`) | Fail; list valid enum values for that field |
| `slug` for `lookup` matches no file in any scoped folder | Return success with empty results + "tried" list; not an error |
| `regex` flag set but `pattern` is not a valid regex | Fail with the regex compile error |
| `folders` includes a path that doesn't exist | Fail with the missing folder name |
| File has no frontmatter | Skip; counted in report's Skipped section |
| Note matches `where` but is `status: archived` and `include_archived: false` | Excluded; counted in report's archived-excluded line |

## Scope Boundaries

**vault-reader handles:** Single-query reads against an Obsidian vault following CLAUDE.md conventions. Frontmatter parsing and validation against the schema. The 4 operations above. Confidence and staleness filters. Retrieval reporting with audit trail.

**vault-reader does NOT:**
- Write to the vault (use vault-writer)
- Create cache files, indexes, or any side effect on disk
- Run embedding-based / semantic / similarity search (deferred to v2; current `data/skill_embeddings.npy` is empirically broken)
- Run multi-hop graph traversal (1-hop only in v1)
- Aggregate or summarize across results (caller's job)
- Execute `.base` queries (read them as files if scoped, but don't interpret)
- Rank results (return order is filesystem walk order plus tie-breakers; caller ranks if needed)
- Resolve cross-vault links (single vault per call)
- Mutate any global state, including in-memory caches in v1
