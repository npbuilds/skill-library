# Workflow Guide Primer (for vault-writer)

How vault-writer encodes the vault's ingest workflow. Reference: the user's `<vault_path>/_meta/workflow-guide.md`.

## Workflow 1 — Ingest a source

When `companion_source_path` is set, vault-writer implements Workflow 1:

1. Save the raw file to `Raw/<source-slug>.<ext>` — never edits it. (For internal artifacts like research briefs, the extension is `.md`.) **vault-writer does not handle file uploads** — the caller has already produced the Raw content; vault-writer writes it.
2. Create a companion note (`Notes/<source-slug>.md`) with `type: source` frontmatter pointing at the Raw path.
3. Integration into existing notes (adding wikilinks) is the **caller's** responsibility, not vault-writer's. vault-writer only writes the new artifacts.
4. Append one line to `log.md`: `<YYYY-MM-DD> <log_op> <log_details>`.
5. If a top-level concept emerged, the caller passes `index_entry: true` with the entry text.

## Workflow 2 — Query the vault

When the calling skill is answering a query and writing the answer back as a note (per CLAUDE.md ingest/query/lint loop):

1. Calling skill chooses the destination — usually `Notes/<topic-slug>.md`.
2. `target_type: note`, `target_domain: <relevant>`.
3. `log_op: query`, `log_details: "<short question>" → <note written/updated>`.
4. The note links to whichever existing notes informed the answer (caller responsibility).

## Workflow 5 — Ambiguous destination

If the caller doesn't know the right domain, prefer `00-Inbox/` with `type: inbox`:

- `target_folder: 00-Inbox/`
- `target_type: inbox`
- `frontmatter_extra: { source: "skill-X output", status: unprocessed }`

Never lose the artifact to chat. The user processes the inbox manually (Workflow 4).

## Anti-patterns vault-writer must not produce

From the user's CLAUDE.md and workflow-guide.md:

- Files without frontmatter
- Schema drift (`high` vs `High` vs `HIGH`)
- `topic-v2.md` files (the `overwrite_policy` defaults to `fail` to enforce this — re-runs collide rather than create siblings)
- Writes that bypass `log.md`
- Notes with `tags: []` (schema requires ≥1 tag)
- Files in `Raw/` that get edited (vault-writer never touches existing Raw files; only writes new ones)

## When vault-writer should refuse

- Calling skill passes a `target_type` not in the schema → refuse, suggest extending schema first
- Calling skill passes empty `tags` → refuse, list of tags is mandatory
- Calling skill passes a slug that already exists with `overwrite_policy: fail` → refuse, suggest a different slug or explicit overwrite
- Calling skill asks to write to `Raw/` for `type: note` (mismatch — Raw is for sources, Notes is for notes) → refuse with the type/folder mismatch
