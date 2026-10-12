# Codex Skill Library Gateway

## Purpose

Use the canonical Claude-authored skill library from Codex without copying,
relocating, or rewriting the files under `skills/`.

The Codex integration is additive:

1. Claude continues to use the existing repository workflow.
2. Codex installs one plugin containing one gateway skill.
3. The gateway searches and loads canonical skills through the deployed,
   content-read Skill Library MCP surface.
4. The gateway adapts Claude-specific tool vocabulary at runtime.

## Location

The repo-local marketplace is at:

```text
mcp-server/codex-marketplace/
├── .agents/plugins/marketplace.json
└── plugins/skill-library/
    ├── .codex-plugin/plugin.json
    ├── .mcp.json
    └── skills/skill-library-gateway/
        ├── SKILL.md
        └── agents/openai.yaml
```

Only the gateway skill is installed natively. The canonical skill collection
is loaded on demand, avoiding a large discovery and context footprint.

## Install

From the repository root:

```bash
codex plugin marketplace add "$PWD/mcp-server/codex-marketplace"
codex plugin add skill-library@skill-building-local
```

Start a new Codex task after installation so the plugin skill and MCP tools are
loaded into the new session.

## Use

Examples:

```text
Use my skill library to find the best workflow for this task.
Use the prose-editor skill from my shared library on this draft.
What library skills are relevant to designing a biotech diligence process?
```

The gateway selects one primary skill and at most two distinct supporting
skills. It initially loads skills without references, then retrieves references
only when the selected workflow requires them.

## MCP boundary

The plugin connects to:

```text
https://skill-library-mcp-ifvybw46na-uc.a.run.app/mcp
```

The plugin exposes only these seven content-retrieval tools to Codex:

- `list_skills`
- `search_skills`
- `get_skill`
- `get_skill_details`
- `list_skill_files`
- `get_skill_file`
- `get_system_overview`

These allowlisted tools use approval mode `approve` so non-interactive Codex CLI
sessions do not cancel each MCP read. Other server tools are not enabled by the
plugin.

Search telemetry records result counts, and skill loads record the selected
skill name. Raw search-query text is omitted in remote mode unless the service
owner explicitly sets `TELEMETRY_SEARCH_QUERIES=1`. The gateway also reduces
goals to short, non-sensitive keywords before searching. Redacted gap events
carry an explicit marker, so analytics report aggregate redacted searches and
zero-result counts instead of blank or misleading query labels.

Any explicit HTTP transport (`sse` or `streamable-http`) enforces restricted
remote mode. Structural mutation tools are available only through local stdio;
selecting an HTTP transport cannot accidentally expose them. Restriction setup
is fail-closed: a removal error or surviving write tool aborts startup.

Because the gateway uses the deployed MCP service, unmerged local skill edits
become visible after the normal merge-to-main deployment converges. When Codex
is running inside this repository and MCP is unavailable, the gateway may read
the local registry and canonical skill files as a fallback.

## Update

After changing the plugin or gateway, run:

```bash
scripts/update-codex-skill-library.sh
```

The repository-owned script validates the marketplace, MCP allowlist, manifest,
and gateway; creates a microsecond-resolution cachebuster; ensures the
marketplace is configured; installs and verifies
`skill-library@skill-building-local`; and only then removes the legacy
`skill-library@personal` installation if present. Use `--check` to validate
without changing the version or installation. Any failed or unverified install
restores the previous manifest and installed-plugin state. The validator accepts
standard SemVer with prerelease and build metadata together.

The marketplace entry should not be hand-edited during the update loop.

## Compatibility boundary

The gateway preserves domain methodology, ordering, quality criteria, and
output contracts. It translates Claude tool names to available Codex tools and
treats Claude `allowed-tools` metadata as compatibility information rather than
authorization.

The canonical skill library and all Claude workflow surfaces remain the source
of truth. Platform-specific behavior belongs in the thin gateway, not in
duplicated skill variants.

## Portable delivery

`get_skill(name, include_references=false)` returns the main instructions only.
Use `list_skill_files` to discover relative supporting-file paths and hashes,
then `get_skill_file` to load a single reference, agent, script, template, or
asset. Text uses UTF-8; binary content is base64 in the returned JSON. Files over
256 KiB require a native export. Hidden files and symlinks are excluded.

`bash scripts/package-skill.sh <skill-dir> [output-dir]` generates a complete
snapshot of non-hidden authored files, including nested supporting directories.
The manifest derives versions and dependency relationships from existing source
metadata, records the Git revision and relevant working-tree state, and hashes
each authored file. Generated installation notes and the manifest itself are
not included in that authored-file hash map. Declared related skills remain
external; the bundle explicitly does not claim a verified execution closure.
Review its warnings when choosing a host. No extra metadata authoring is required.

Search does not derive task context from shared telemetry. HTTP events carry an
instance ID and `anonymous_event` attribution with a unique legacy session key
per event; this prevents unrelated callers from being grouped as one session.
Local stdio retains `stdio_process` attribution, which is not a task identifier.

For rollout, deploy the server changes before running the existing plugin update
script so installed clients can discover the two added read tools. Repository
configuration updates alone do not update an already-installed plugin cache.
