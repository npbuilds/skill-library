# Skill Building Project

## File Placement Rules

**Never create files at the project root.** Every file belongs in a designated directory:

| Content type | Target directory | Examples |
|---|---|---|
| Skill definitions | `skills/<domain>/<skill-name>/SKILL.md` | Sommelier tasting grid |
| Archon briefings | `archon-briefings/` | Daily HTML briefings |
| Visualizations & dashboards | `output/visualizations/` | dashboard.html, skill-map.html |
| Creative output (art, writing) | `output/art/` or `output/writing/` | Algorithmic art, fiction |
| Architecture diagrams | `output/visualizations/` | architecture-diagram.html |
| Research reports | `research/` | Landscape reports, skill research |
| Data files (JSON, JSONL) | `data/` | Registry, evolution logs, usage |
| Shell scripts | `scripts/` | Automation, analysis, migration |
| Python scripts | `scripts/` | Graph wiring, scoring, detection |
| Agent definitions | `agents/` | Subagent prompts |
| MCP server code | `mcp-server/` | Server, CLI, search index |
| Archon data pipeline | `archon-data/` | Collectors, processors, snapshots |
| Git hooks | `hooks/` | File watchers, validators |
| Exports (Obsidian, etc.) | `exports/` | Vault exports |
| Deployment config | project root (Dockerfile only) | Dockerfile, .dockerignore |

If you're unsure where a file goes, place it in `output/` with an appropriate subdirectory.

## Project Structure

```
skills/           # Skill SKILL.md files organized by domain
data/             # Registry, logs, evolution data
scripts/          # All automation scripts (sh + py)
mcp-server/       # MCP server for skill library
archon-data/      # Investment briefing data pipeline
archon-briefings/ # Generated archon briefing outputs
output/           # All generated artifacts (gitignored)
  visualizations/ # Dashboards, diagrams, maps
  art/            # Algorithmic art
  writing/        # Creative writing output
research/         # Research reports and analysis
agents/           # Subagent prompt definitions
hooks/            # Git and Claude Code hooks
exports/          # Obsidian vault and other exports
commands/         # Claude Code slash command definitions
```

## Conventions

- Skill files follow the SKILL.md template structure with YAML frontmatter
- Registry is the source of truth for skill metadata: `data/registry.json`
- Scripts that modify registry should go through `scripts/sync-registry.py`
- The MCP server (`mcp-server/server.py`) exposes skill library tools to Claude

## Auto-Trigger Skills

### Spelunker (Deep Research)

When the user's request matches any of these signals, automatically invoke `/spelunker` with their question:

- Explicit: "research", "investigate", "verify", "fact-check", "look into", "dig into"
- Inquiry: "what does the evidence say", "help me understand", "is X true", "what caused X"
- Generative: "what's the best X", "how should we design X", "what are the options for X"
- Depth cues: "I need to be sure", "this is for a decision", "comprehensive analysis"

Do NOT trigger for simple factual lookups that a single web search would answer. Spelunker is for multi-source, confidence-tagged research — not quick answers.
