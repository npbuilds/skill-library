# Frontmatter Schema Primer (for vault-writer)

How to parse a vault's `_meta/frontmatter-schema.md` and use the result for validation. The schema doc is human-authored Markdown; this primer specifies how to extract structured data from it.

## What to extract

When reading `<vault_path>/_meta/frontmatter-schema.md`:

1. **Universal required fields** — under the §"Universal fields (every note)" table. Read the rows; collect `type`, `domain`, `status`, `created`, `tags` as required (the column is "Required" with ✓). `modified` is auto-filled, ignore for validation.

2. **`type:` enum** — listed in:
   - The "Universal fields" table notes ("Starter values: ...")
   - The §"Type-specific fields" section headings (each `### type: <value>` is a value)
   - The §"Type registry" section (canonical list)
   - Use the union of all three; the registry is authoritative when they disagree.

3. **`domain:` enum** — under §"Domain registry". Read the bulleted list; each line starts with `` `<value>` `` followed by description.

4. **Per-type required fields** — under `### type: <value>` sections, the YAML example block shows required + commented-optional. Required = uncommented; conditional = commented with default; optional = commented or absent.

5. **Per-type status enums** — under §"Status values by type" or §"Status values by type (extended)".

6. **Field-format conventions** — under §"Conventions":
   - Dates: `YYYY-MM-DD`
   - Slugs: lowercase, hyphen-separated
   - Tags: lowercase, hyphen-separated, no `#` prefix
   - Lists: YAML list syntax
   - Empty fields: `""` (not null, not omitted)

## Schema versions

The schema is additive-only per the user's scalability principles. Track the modification time of the schema file and include it in the integrity report. If the schema changes between calls, log the new mtime.

## Schema extensions

The schema appends "extension" sections at the bottom (e.g. `### type: note — epistemic and maturity fields (added 2026-05-10)`). These are additive: the original sections still apply, and the extension adds optional fields.

When validating, treat extension fields as optional unless the extension section explicitly says they're required.

## Failure modes

- Schema file missing → fail the call (vault-writer can't operate)
- Schema file exists but malformed (no `---` frontmatter, no Universal-fields table) → fail with parse error
- A `target_type` or `target_domain` value not in any enum found → fail with the union of valid values shown
- A field in `frontmatter_extra` not documented anywhere in the schema → fail with suggestion to extend schema first

The cardinal rule: **the schema is authoritative**. If the calling skill disagrees with the schema, the schema wins. Schema extension is a deliberate user act, not a side effect of a skill call.
