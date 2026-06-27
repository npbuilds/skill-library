# Skill Building Project

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

```
Local:   data/registry.json ──→ scripts/migrate_to_firestore.py ──→ Firestore
Live:    MCP server tools ──→ Firestore collections ──→ app/index.html (real-time)
Desktop: Neural Observatory.webloc ──→ https://skill-library-prod.web.app
```

## Conventions

- Skill files follow the SKILL.md template structure with YAML frontmatter
- Registry is the source of truth for skill metadata: `data/registry.json`
- Scripts that modify registry should go through `scripts/sync-registry.py`
- The MCP server (`mcp-server/server.py`) exposes skill library tools to Claude
- After adding skills locally, run `python3 scripts/migrate_to_firestore.py` to sync to Firestore
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
