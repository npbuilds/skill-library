---
name: vault-writer
description: >
  Write structured artifacts (research briefs, syntheses, decompositions, build plans) back to an
  Obsidian vault following the vault's CLAUDE.md ingest workflow. Validates frontmatter against
  the vault's `_meta/frontmatter-schema.md`, writes the file, appends `log.md`, optionally updates
  `index.md`. Returns an integrity report with path written, log line, and any unresolved wikilinks.
  Use when an orchestrator's output needs to persist beyond the chat session. Schema-strict and
  fail-closed — invalid frontmatter rejects the call rather than producing drift.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Edit Bash Glob
---

# Vault Writer — The Bridge

Take a structured artifact from a calling skill and persist it to the user's Obsidian vault per the vault's own conventions. The vault is the persistent layer; conversation is ephemeral. Until skills can write durable artifacts to the vault, every research run dies in chat.

This skill embodies CLAUDE.md as code: it reads the vault's schema, validates the artifact's frontmatter, writes the file atomically, updates the log, and optionally updates the index. It does one thing per invocation. It is not an orchestrator and not an editor of arbitrary files.

## Guiding principles

These are non-negotiable:

1. **Fail closed on schema violations.** If the calling skill passes frontmatter that doesn't match the vault's schema, reject the call. Do not "best effort" or partial-write.
2. **Idempotent by slug.** Given identical input + slug, produce identical output. No timestamp suffixes in filenames. If the file exists, apply the calling skill's `overwrite_policy` (default: fail).
3. **Always append to log.md.** Every successful write produces exactly one log line. Never optional.
4. **Never invent schema fields.** If the calling skill needs a field not in the vault's schema, reject the call. Schema extension is a deliberate user act, not a side effect.
5. **Never create folders.** Target folders must exist. New folders are deliberate user acts.
6. **Report unresolved wikilinks.** Do not silently create stub notes for them. The calling orchestrator decides whether to fill the gap.
7. **Respect the cardinal rule.** This skill creates new notes. The vault's CLAUDE.md cardinal rule ("don't create when an update would do") is the calling skill's responsibility — vault-writer trusts the slug it receives.

## How to Run

### Input

From the calling skill (orchestrator or action skill that produced an artifact):

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

### Steps

#### Step 1 — Read the vault's schema and workflow guide

Read `<vault_path>/_meta/frontmatter-schema.md` to extract:
- The current `type:` enum values
- The current `domain:` enum values
- Status enums per type
- Required fields per type
- Field format conventions (date format, slug regex, list syntax)

Read `<vault_path>/CLAUDE.md` if present. The vault may have project-specific overrides (folder rules, ingest conventions). Honor them.

If either file is missing, fail the call with a clear error: this is not a vault that vault-writer can write to.

#### Step 2 — Validate slug

Slug must match `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$`. No spaces, no underscores, no uppercase, no leading/trailing hyphens. Reject otherwise.

#### Step 3 — Validate destination

Compute target path: `<vault_path>/<target_folder>/<slug>.md`.

Check:
- `<vault_path>/<target_folder>/` exists. If not, reject.
- `<target_path>` does not exist (under default `overwrite_policy: fail`). If exists, apply policy:
  - `fail` → reject with "file already exists"
  - `overwrite` → proceed; warn in integrity report
  - `append` → read existing, plan to append `artifact_body` after a `\n\n---\n\n` separator preserving frontmatter; warn

#### Step 4 — Validate frontmatter against schema

Build the frontmatter from `target_type` + `target_domain` + universal required fields + `frontmatter_extra`. Required fields per type from `_meta/frontmatter-schema.md`. Check:

- All universal fields present: `type`, `domain`, `status`, `created`, `tags`
- All type-specific required fields present (e.g., `type: source` requires `source_type`, `accessed`, `path`, `url`, `author`)
- All enum values match: `type`, `domain`, `status`, `source_type`, `confidence` (if present), `maturity` (if present)
- `created` matches `YYYY-MM-DD`
- `last_verified` (if present) matches `YYYY-MM-DD` or is `""`
- `tags` is a list with ≥1 entry
- All field names in `frontmatter_extra` are documented in the schema (no invented fields)

If any check fails, reject with the specific violation. Do not partial-write.

#### Step 5 — Render frontmatter

YAML frontmatter, lexicographic field order within tier (universal fields first in this canonical order: `type`, `domain`, `status`, `created`, then optional: `confidence`, `last_verified`, `maturity`, then type-specific fields, then `tags` last). Use `""` for empty strings; `[item, item]` for lists; ISO `YYYY-MM-DD` for dates.

Wrap in `---` delimiters.

#### Step 6 — Compose file content

`<frontmatter_block>\n\n<artifact_body>`. Ensure exactly one blank line between frontmatter and body. Ensure file ends with a single trailing newline.

#### Step 7 — Atomic write

Use the Write tool to write the full file content to `<target_path>`. (Write tool overwrites; under default `overwrite_policy: fail` we've already verified non-existence; under `overwrite` we write directly.)

#### Step 8 — Companion-source dual-write (if `companion_source_path` set)

This is the Workflow-1 pattern: a Raw/ source plus a Notes/ companion.

The primary write (Steps 3–7) handled the Raw/ artifact. Now write the companion:
- Path: `<vault_path>/Notes/<slug>.md` — same slug; type and folder disambiguate
- Frontmatter: `type: source`, `domain: <target_domain>`, `status: active`, `created: <today>`, `source_type: internal-doc` (or whatever the calling skill specified), `url: ""`, `author: ""`, `accessed: <today>`, `path: <companion_source_path>` (relative path inside Raw/, e.g. `Raw/<slug>-<date>.md`), `tags: [source, ...]`
- Body: the calling skill **must** provide `companion_body` (a short description of what's in the Raw/ artifact, with any cross-links). If `companion_source_path` is set but `companion_body` is missing or empty, reject the call before any write — no auto-default. Rationale: a stub-only companion produces low-signal notes that pollute the Notes/ surface; callers that produce Raw artifacts almost always have an abstract or summary cheap to pass.

If the companion path collides with an existing file, reject without writing the companion. The primary write has already happened — surface this in the integrity report and let the orchestrator recover.

#### Step 9 — Append log.md

Read `<vault_path>/log.md` to detect format conventions (separator: space vs tab; check the most recent few entries). Match exactly.

Append a single line: `<YYYY-MM-DD> <log_op> <log_details>`. Use vault-local date.

Use Edit (not Write) to append, preserving prior content.

#### Step 10 — Update index.md (if `index_entry: true`)

Read `<vault_path>/index.md`. Locate the H2 heading matching `index_section`. Reject the call if the heading does not exist (do not create sections silently).

Insert `index_entry_text` as a new bullet under that heading, preserving any existing sort order. If the section has nested bullets (e.g. under "Domains"), the calling skill must specify `index_subsection` or insert at top level — error if ambiguous.

Use Edit to perform the insertion.

#### Step 11 — Detect unresolved wikilinks

Scan `artifact_body` (and `companion_body` if applicable) for `\[\[([^\]|]+)(\|[^\]]+)?\]\]` patterns. For each match, check whether `<vault_path>/Notes/<name>.md` or `<vault_path>/<any_other_folder>/<name>.md` exists. Skill-library wikilinks (e.g., `[[claim-decomposer]]`) will appear as unresolved — that's expected. Distinguish vault-resolvable from skill-library by whether the calling skill provided a `known_skill_refs` list; otherwise list everything unresolved.

Return the unresolved list in the integrity report. **Do not auto-create stubs.**

### Output

Return a structured integrity report:

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

Status semantics:
- `success` — all writes completed, no unexpected state
- `partial` — primary write succeeded, secondary (companion / index / log) failed; integrity report describes which
- `failed` — nothing written; reason in report

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

## Scope Boundaries

**vault-writer handles:** Single-artifact writes that follow the vault's existing CLAUDE.md ingest workflow. One file or one source-pair per invocation. Frontmatter validation and rendering. `log.md` append. Optional `index.md` insertion. Integrity reporting.

**vault-writer does NOT:**
- Update existing notes in place (defer to a future `vault-updater` or merge-mode v2)
- Create folders, types, or domains (these are deliberate user acts via schema extension)
- Generate frontmatter values the calling skill didn't supply (no auto-tagging, no auto-confidence)
- Auto-create stub notes for unresolved wikilinks
- Write to multiple separate artifacts in a single call (orchestrator calls vault-writer N times for N artifacts)
- Modify `_meta/`, `_templates/`, or `_bases/` content
- Run lint operations (those belong in a separate skill)
- Resolve "should this update an existing note instead?" — the calling skill chooses the slug
