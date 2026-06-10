# Vault Reader — Quick Reference


## Input

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
