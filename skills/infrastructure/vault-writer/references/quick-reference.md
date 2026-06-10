# Vault Writer — Quick Reference


## Quick Reference

| Parameter | Required | Notes |
|---|---|---|
| `vault_path` | yes | Absolute path to the vault root (e.g., `/Users/nirav/Documents/vault`) |
| `artifact_body` | yes | The markdown body of the note (frontmatter excluded — vault-writer renders it) |
| `target_type` | yes | One of the values in the vault's `type:` enum |
| `target_domain` | yes | One of the values in the vault's `domain:` enum |
| `slug` | yes | Lowercase, hyphen-separated, no spaces. Matches `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$` |
| `target_folder` | conditional | Defaults: `Notes/` for `type: note`, `Raw/` for the immutable side of a source pair, `skill-lab/` for `type: skill-build-plan`. Override allowed if folder exists |
| `frontmatter_extra` | optional | Type-specific fields (e.g., `suite_name`, `source_type`, `path`, `confidence`, `last_verified`, `maturity`) |
| `tags` | yes | Min 1 tag, lowercase, hyphen-separated |
| `companion_source_path` | optional | When set, also write a `type: source` companion in `Notes/` whose `path:` field references the just-written Raw artifact (Workflow 1 pattern). Requires `companion_body` |
| `companion_body` | conditional | Required when `companion_source_path` is set. Short description of what's in the Raw/ artifact, with any cross-links. No auto-default — vault-writer rejects if missing |
| `log_op` | yes | One of `ingest | query | lint | domain-added | type-added | branch-spawned | fix | archive | schema-extended | backfill` (match existing log.md ops) |
| `log_details` | yes | One-line description for the log entry |
| `index_entry` | yes | Boolean. If true, requires `index_entry_text` and `index_section` |
| `index_entry_text` | conditional | One-line bullet to insert under `index_section` |
| `index_section` | conditional | The H2 heading text in `index.md` to insert under |
| `overwrite_policy` | optional | `fail | overwrite | append`. Default `fail` |

## Error Handling

| Failure | Response |
|---|---|
| Schema file missing | Fail before any write; report `<vault_path>/_meta/frontmatter-schema.md` not found |
| Slug fails regex | Fail before any write; show the regex and the offending slug |
| Target folder doesn't exist | Fail before any write; show the path checked |
| Frontmatter validation fails | Fail before any write; report the specific field and rule violated |
| Target file exists, policy=fail | Fail before any write; report path |
| Type-specific required field missing | Fail with the schema's per-type table excerpt showing what was needed |
| Field in `frontmatter_extra` not in schema | Fail; suggest opening the schema doc to add it deliberately |
| `index.md` section not found | Fail after primary write succeeded → status `partial`; suggest creating the section first |
| Companion path collision | Fail companion write only → status `partial`; primary file remains; report the collision |
| `companion_source_path` set but `companion_body` missing or empty | Fail before any write; require a non-empty companion description |
| Write tool error mid-flight | Status `failed` if primary; status `partial` if companion or log or index; surface the underlying error |

## Formula / Pseudocode

```
INTEGRITY REPORT — vault-writer
────────────────────────────────
Wrote: <absolute path to primary file>
Wrote (companion): <absolute path, if any> | <none>
Logged: <log line as appended>
Indexed: <section / subsection> | <skipped per index_entry: false>
Schema validated against: <vault_path>/_meta/frontmatter-schema.md (modified <date>)
Overwrite policy applied: <fail | overwrite | append>

Unresolved wikilinks in artifact_body:
  - [[some-name]] — no Notes/some-name.md exists
  - [[other-name]] — no matching file in any vault folder

Warnings:
  - <any non-fatal issues — duplicate tags deduped, etc.>

Status: success | partial | failed
```
