# Frontmatter Schema Primer (for vault-reader)

How to parse a vault's `_meta/frontmatter-schema.md` and use the result to validate read-side queries.

## What to extract

When reading `<vault_path>/_meta/frontmatter-schema.md`:

1. **Universal field names** — under the §"Universal fields" table. These are the keys every note has (or should have): `type`, `domain`, `status`, `created`, `tags`, plus `modified` (auto).

2. **`type:` enum values** — from the §"Type registry" section (authoritative when it disagrees with other lists) plus the `### type: <value>` section headings.

3. **`domain:` enum values** — from §"Domain registry". Each line begins with `` `<value>` ``.

4. **Per-type `status:` enums** — from §"Status values by type" and the extension §"Status values by type (extended)".

5. **`source_type:` enum** — for `type: source` notes, from the YAML example block under `### type: source`.

6. **Extension fields** — at the bottom of the schema. Currently the only extension is the `type: note` epistemic block adding `confidence`, `last_verified`, and `maturity`. Treat extension fields as optional unless the extension explicitly says required.

7. **`confidence:` enum** — `confirmed | likely | contested | speculative | unverifiable`. Plus the ordering: `confirmed > likely > contested > speculative > unverifiable` (used by `min_confidence` filter).

8. **`maturity:` enum** — `seedling | budding | evergreen`.

## Schema validation for queries

Before executing a `filter` operation, validate every `where` predicate:

- The key (field name) must appear somewhere in the schema (universal or type-specific or extension).
- The value, if the field is an enum field, must be in the enum.
- The value, if the field is a list field (e.g., `tags`), is treated as a set-intersection check.
- The value, for date fields (`created`, `last_verified`, `modified`), must match `YYYY-MM-DD` or be `""`.

On any violation, reject the call before any file read.

## Schema versions

The schema is additive-only per the vault's scalability principles. Track the modification time of the schema file and include it in the retrieval report. If the schema's mtime differs between two consecutive calls in a session, the schema was extended; surface this in the report ("Schema changed during session — re-validate prior results if cached") but do not fail.

## Failure modes

- Schema file missing → fail before any read
- Schema file malformed (no Universal-fields table or no Type registry) → fail with parse error
- `target_field` in `where` not in any documented section → fail with the union of valid field names shown
- Value for enum field not in the enum → fail with the valid values listed

The cardinal rule mirrors vault-writer: **the schema is authoritative**. The skill is a reader, not an interpreter; it does not add fields, infer types, or normalize values.
