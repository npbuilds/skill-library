# Skill Building Project

## File Placement Rules

**Never create arbitrary files at the project root.** Every file belongs in a
designated directory; only standard repository metadata and deployment entry
points live at the root:

| Content type | Target directory | Examples |
|---|---|---|
| Skill definitions | `skills/<domain>/<skill-name>/SKILL.md` | Sommelier tasting grid |
| Neural Observatory app | `app/` | index.html, firebase.json, firestore.rules |
| MCP server code | `mcp-server/` | Server, CLI, search index |
| Cloud Run config | `cloudrun/` | service.yaml |
| Data files (JSON, JSONL) | `data/` | Registry, evolution logs, usage |
| Shell/Python scripts | `scripts/` | Automation, migration, analysis |
| Agent definitions | `agents/` | Subagent prompts |
| Slash commands | `commands/` | Codex command definitions |
| Git hooks | `hooks/` | File watchers, validators |
| Cloud/infra docs | `docs/` | Setup guides |
| Archon data pipeline | `archon-data/` | Collectors, processors, snapshots |
| Archon briefings | `archon-briefings/` | Daily HTML briefings |
| Loom briefings | `loom-briefings/` | Decision journal, emergence log |
| Research reports | `research/` | Landscape reports, skill research |
| Legacy visualizations | `output/visualizations/` | Old dashboard, skill-map, diagrams |
| Creative output | `output/art/` or `output/writing/` | Algorithmic art, fiction |
| Exports (Obsidian, etc.) | `exports/` | Vault exports |
| Repository metadata | project root | README.md, AGENTS.md, CLAUDE.md, LICENSE |
| Deployment config | project root | Dockerfile, .dockerignore |

If you're unsure where a file goes, place it in `output/` with an appropriate subdirectory.

## Project Structure

```
LICENSE             # MIT license for public reuse
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
commands/           # Codex slash command definitions
hooks/              # Git and Codex hooks
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
  └─ (daily) daily-firestore.yml → evolution snapshot + health
                                 + telemetry pull → maint:green bot PR

Cloud MCP server: strictly read-only tools; usage/gap telemetry → Firestore
(durable; local jsonl is ephemeral on Cloud Run). Feedback remains available
only through trusted local stdio until an authenticated remote surface exists.
Structural writes: local stdio tools or /maint bot PRs only.
Desktop: Neural Observatory.webloc ──→ https://skill-library-prod.web.app

INVARIANT: merge to main converges all consumers within minutes; divergence is
detected daily (meta/registry.synced_sha check) and alerted, never silent.
```

## Conventions

- Skill files follow the SKILL.md template structure with YAML frontmatter
- Registry is the source of truth for skill metadata: `data/registry.json`
- Scripts that modify registry should go through `scripts/sync-registry.py`
- The MCP server (`mcp-server/server.py`) exposes skill library tools to Codex
- Firestore sync is owned by CI (`sync-firestore.yml` on merge). Manual
  `python3 scripts/migrate_to_firestore.py` runs are backfill/recovery only
- Deploy app changes: `cd app && npx firebase-tools deploy --only hosting`

## Auto-Trigger Skills

### Spelunker (Deep Research)

When the user's request matches any of these signals, automatically invoke `/spelunker` with their question:

- Explicit: "research", "investigate", "verify", "fact-check", "look into", "dig into"
- Inquiry: "what does the evidence say", "help me understand", "is X true", "what caused X"
- Generative: "what's the best X", "how should we design X", "what are the options for X"
- Depth cues: "I need to be sure", "this is for a decision", "comprehensive analysis"

Do NOT trigger for simple factual lookups that a single web search would answer. Spelunker is for multi-source, confidence-tagged research — not quick answers.
