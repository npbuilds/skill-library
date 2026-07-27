# Skill Building Project

## Machinery-Only Repo (public)

This repo is **public** and carries machinery only. No creative-project content may enter it — not in code, fixtures, tests, docs, file names, commit messages, or PR titles/bodies. That includes project/world names, character names, coined terms, prose samples, and private workspace paths. Eval fixtures that need real project content live in the private workspace, never here; drivers stay project-agnostic (content arrives only via runtime args).

Enforced twice: locally by `hooks/leak-guard.sh` (pre-commit, commit-msg, and pre-push git hooks; reads a private term list via `git config leakguard.file` — the list itself is never committed) and in CI by `.github/workflows/leak-guard.yml` (term list held in the `LEAK_TERMS` repo secret; the job reports file paths only, never matched text). If the guard blocks you, move the content out — bypassing (`LEAK_GUARD_SKIP=1`) is for false positives only.

## File Placement Rules

**Never create files at the project root.** Every file belongs in a designated directory:

| Content type | Target directory | Examples |
|---|---|---|
| Skill definitions | `skills/<domain>/<skill-name>/SKILL.md` | Sommelier tasting grid |
| Neural Observatory app | `app/` | index.html, firebase.json, firestore.rules |
| MCP server code | `mcp-server/` | Server, CLI, search index |
| Cloud Run config | `cloudrun/` | service.yaml |
| Data files (JSON, JSONL) | `data/` | Registry, evolution logs, usage |
| Shell/Python scripts | `scripts/` | Automation, migration, analysis |
| Agent definitions | `agents/` | Subagent prompts |
| Slash commands | `commands/` | Claude Code command definitions |
| Git hooks | `hooks/` | File watchers, validators |
| Cloud/infra docs | `docs/` | Setup guides |
| Archon data pipeline | `archon-data/` | Collectors, processors, snapshots |
| Archon briefings | `archon-briefings/` | Daily HTML briefings |
| Loom briefings | `loom-briefings/` | Decision journal, emergence log |
| Research reports | `research/` | Landscape reports, skill research |
| Legacy visualizations | `output/visualizations/` | Old dashboard, skill-map, diagrams |
| Creative output | `output/art/` or `output/writing/` | Algorithmic art, fiction |
| Exports (Obsidian, etc.) | `exports/` | Vault exports |
| Deployment config | project root (Dockerfile only) | Dockerfile, .dockerignore |

If you're unsure where a file goes, place it in `output/` with an appropriate subdirectory.

## Project Structure

```
app/                # Neural Observatory — Firebase Hosting (live app)
  index.html        #   Dashboard with Firestore data layer
  js/               #   Firebase config, data adapter modules
  firebase.json     #   Hosting + Firestore emulator config
  firestore.rules   #   Security rules (public read, auth write)
skills/             # Skill SKILL.md files organized by domain
data/               # Local data (registry.json, JSONL logs)
mcp-server/         # MCP server for skill library (Cloud Run)
cloudrun/           # Cloud Run service config
scripts/            # All automation scripts (sh + py)
  migrate_to_firestore.py  # Push local data → Firestore
  serve.py          # Legacy local HTTP server
agents/             # Subagent prompt definitions
commands/           # Claude Code slash command definitions
hooks/              # Git and Claude Code hooks
docs/               # Infrastructure setup guides
archon-data/        # Investment briefing data pipeline
archon-briefings/   # Generated archon briefing outputs
loom-briefings/     # Decision journal, emergence log
research/           # Research reports and analysis
output/             # Generated artifacts (mostly gitignored)
  visualizations/   # Legacy dashboards, diagrams, maps
exports/            # Obsidian vault exports
```

## Live Deployments

| Service | URL | Platform |
|---|---|---|
| Neural Observatory | https://skill-library-prod.web.app | Firebase Hosting |
| MCP Server | Cloud Run (skill-library-mcp) | GCP Cloud Run |
| Firestore | skill-library-prod (us-central1) | GCP Firestore |

## Data Flow

Git is the single source of truth. Merge to main (CI green) fans out automatically:

```
Merge to main (CI green)
  ├─ deploy.yml         → Cloud Run image (registry + skills + search index baked in)
  ├─ sync-firestore.yml → Firestore skills/meta/changelogs (dashboard)
  │                     + meta/usage_rollup (usage aggregate from committed jsonl)
  └─ (daily) daily-firestore.yml → evolution snapshot + health
                                 + telemetry pull → maint:green bot PR

Cloud MCP server: read-only tools + record_skill_feedback; usage/gap/feedback
telemetry → Firestore (durable; local jsonl is ephemeral on Cloud Run).

Usage telemetry has two producers, segmented by the `source` field:
  source=mcp    → server.py _log_event (MCP tool calls; mirrored to Firestore)
  source=plugin → hooks/skill-invocation-telemetry.sh (Claude Code's native
                  Skill tool + slash commands, which never touch the MCP
                  server) → scripts/log_skill_invocation.py → data/usage.jsonl
The plugin hook is registered in ~/.claude/settings.json, not this repo's
.claude/settings.json — plugin skills are invoked from other projects, and a
project-scoped hook would miss them (registering both would double-count).
Its registration guards on the script existing, so an unmerged/moved checkout
makes it a silent no-op — if source=plugin counts are flat, check that
hooks/skill-invocation-telemetry.sh exists at the registered path.

Plugin-name resolution is strict (registry names, data/skill_aliases.json,
our own plugin prefixes). Unresolved names are written as `skill_raw`, never
`skill`: recalibrate_scores.py divides by max_usage across every name in the
log, so a foreign name would become the denominator and deflate every real
skill. skill_aliases.json ships EMPTY on purpose — see
`python3 scripts/log_skill_invocation.py --report` for what is unattributed.

Structural writes: local stdio tools or /maint bot PRs only.
Desktop: Neural Observatory.webloc ──→ https://skill-library-prod.web.app

Dashboard usage (scripts/usage_rollup.py): the raw Firestore `usage` collection
has ONE writer, the Cloud Run MCP mirror — local stdio and plugin-native loads
(source=plugin) never reach it, yet both feed auto_score. The dashboard
therefore reads meta/usage_rollup (a full-snapshot aggregate of committed
data/usage.jsonl, so all writers appear, broken down by source) plus the
`usage` docs newer than data/.telemetry_watermark for a live cloud tail. The
watermark is the exact boundary of what the pull loop has already landed in
git, so the two halves never overlap. NEVER push usage.jsonl into the `usage`
collection to make it visible (`--include-telemetry` is backfill only): that
append double-counts and gets re-pulled as duplicates. The rollup is an
idempotent single-doc overwrite instead.

INVARIANT: usage shown on the dashboard and usage behind auto_score are both
derived from data/usage.jsonl with the same skill-load filter, so a score is
always explainable by the usage panel.

INVARIANT: merge to main converges all consumers within minutes; divergence is
detected daily (meta/registry.synced_sha check) and alerted, never silent.
```

## Conventions

- Skill files follow the SKILL.md template structure with YAML frontmatter
- Registry is the source of truth for skill metadata: `data/registry.json`
- Scripts that modify registry should go through `scripts/sync-registry.py`
- The MCP server (`mcp-server/server.py`) exposes skill library tools to Claude
- Firestore sync is owned by CI (`sync-firestore.yml` on merge). Manual
  `python3 scripts/migrate_to_firestore.py` runs are backfill/recovery only
- The cloud MCP endpoint removes structural write tools; to use them, point
  `skill-library` in `~/.claude.json` at a local stdio server
  (`python3 mcp-server/server.py`), not the Cloud Run URL
- Deploy app changes: `cd app && npx firebase-tools deploy --only hosting`

## Auto-Trigger Skills

### Spelunker (Deep Research)

When the user's request matches any of these signals, automatically invoke `/spelunker` with their question:

- Explicit: "research", "investigate", "verify", "fact-check", "look into", "dig into"
- Inquiry: "what does the evidence say", "help me understand", "is X true", "what caused X"
- Generative: "what's the best X", "how should we design X", "what are the options for X"
- Depth cues: "I need to be sure", "this is for a decision", "comprehensive analysis"

Do NOT trigger for simple factual lookups that a single web search would answer. Spelunker is for multi-source, confidence-tagged research — not quick answers.

### Investing Strategists (Execution Layer)

When the user's request matches an execution-class signal, route directly to the matching strategist under `skills/investing/strategists/`. Strategists are loadable individually via the `Skill` tool. The full routing table is in `skills/investing/archon/references/delegation-rules.md` §"Strategist Routing".

Signal → strategist:

- "DCA into X" / "automated weekly investing" / "schedule buys" → `dca-investor`
- "Rebalance my book" / "drift from target" / "am I overweight X" → `rebalancer`
- "Swing trade X" / "is X oversold" / "RSI buy candidate" → `swing-trader`
- "Day trade X" / "intraday setup" / "opening range" → `day-trader`
- "Earnings setup X" / "beat-but-down" / "post-earnings" → `earnings-event-trader`
- "Reflexive setup X" / "narrative trade" / "Soros-style" → `reflexivity-trader`
- "Macro overlay" / "what regime / how to tilt" → `macro-overlay-trader`
- "CSP on X" / "covered call" / "options income" → `options-strategist` (Claude Code analyst mode only; not loadable in `autotrader` Hermes profile)

Important:
- Strategists default to `mode: review`. They produce a `## tick_decision` JSON block; never paraphrase it — surface verbatim.
- Live placement happens only in the `autotrader` Hermes profile, never in Claude Code (executor enforces). Claude Code is analyst-only.
- The `_shared/executor` skill is the single broker gate. Never invoke it directly from CLAUDE.md or Archon — only strategists call it.
- If the user asks about live execution while in Claude Code, explain that placement requires the Hermes `autotrader` profile and is paper-mode by default (see plan at `~/.claude/plans/i-have-a-skill-replicated-tide.md`).
