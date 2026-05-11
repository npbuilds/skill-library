# Query Shape Primer (for vault-reader)

How to interpret the four operations and their parameters. The intent: every operation is narrow, deterministic, and read-only.

## Operations

### `lookup` — single-note retrieval by slug

Use when the caller knows the exact note name and wants its content.

Required: `slug`. Optional: `folders`, `full_body`, `excerpt_chars`.

Implementation: try `<vault_path>/<folder>/<slug>.md` in folder order. First match wins. No fallback to fuzzy search.

If no match, return empty `Results` with `Limitations: "tried folders [...]"`. Not an error.

### `filter` — frontmatter-aware multi-note retrieval

Use when the caller wants all notes matching a set of frontmatter predicates.

Required: `where` (map of field → value). Optional: `folders`, `min_confidence`, `max_staleness_days`, `include_archived`, `max_results`.

`where` predicate semantics:
- **Scalar field** (`type`, `domain`, `status`, `confidence`, `maturity`, `source_type`): exact match.
- **Date field** (`created`, `last_verified`, `modified`): exact-match string compare unless a future v2 adds range syntax.
- **List field** (`tags`): set-intersection — note matches when `where: {tags: [X]}` and `X` is in the note's tags list.
- **Multiple keys in `where`**: implicit AND.

Schema validation: every key in `where` must be documented in the schema; every enum value must be in the enum.

### `graph` — 1-hop wikilink graph for a single note

Use when the caller wants the note plus its immediate neighborhood.

Required: `slug`. Optional: `folders`, `resolve_wikilinks`, `known_skill_refs`.

Outbound extraction: regex `\[\[([^\]|]+)(\|[^\]]+)?\]\]` over the body. Strip the display-name part (`|...`). Deduplicate.

Inbound extraction: grep all scoped `.md` files for `[[<slug>]]` and `[[<slug>|...]]`. Return the list of files that link to this note.

Resolution: if `resolve_wikilinks: true`, try `<vault_path>/<folder>/<name>.md` in folder order. Tag each:
- `vault` — resolved to a real vault file
- `skill-library-ref` — unresolved BUT the name is in `known_skill_refs` (caller-provided list of known skill names)
- `unresolved` — unresolved and not in `known_skill_refs`

The `skill-library-ref` distinction prevents flagging legitimate cross-substrate links as broken.

### `text-search` — substring or regex over note bodies

Use when the caller wants notes mentioning a specific term.

Required: `pattern`. Optional: `regex`, `folders`, `max_results`, `excerpt_chars`.

Implementation: read each `.md` file's post-frontmatter body. Apply substring (default) or regex (`regex: true`). For each match, capture line number + 2-line surrounding context.

This is **not** semantic search. "Find notes about Zettelkasten" must use the literal word "Zettelkasten" (or a regex that matches it). For semantic intent, the caller should use `filter` on `tags` or extend the query with multiple text-searches.

## Parameter precedence

When multiple filters apply (e.g., `where`, `min_confidence`, `max_staleness_days`, `include_archived`):

1. `where` predicates evaluate first (filesystem walk + frontmatter parse)
2. Post-filters apply in order: `include_archived`, `min_confidence`, `max_staleness_days`
3. `max_results` cap applies last, after all filtering

This ordering ensures filter audit is consistent in the retrieval report's Limitations section.

## Wikilink display-name handling

`[[name|display]]` should always resolve / be checked as if it were `[[name]]`. The display part is human-readable text, never affects target resolution.

## Performance bounds

The current vault has 13 markdown files. All operations should complete in under 1 second. If the vault grows past 200 notes and operations exceed 5 seconds, the v1 architecture has hit its scaling ceiling and embedding-based search (deferred to v2) becomes load-bearing.
