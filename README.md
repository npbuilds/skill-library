# Skill Library

A personal library of **528 expert-persona agent skills across 19 subject domains** (plus one internal metadata namespace), served over MCP and usable from both Claude and Codex. It is built on one idea: an agent gets sharper when you give it a *named expert's* methodology, typed inputs and outputs, and a way to cite its own evidence — then let those experts call each other.

I build these to think with. The architecture is the point; the domains are where I stress-tested it.

**Live:** [Neural Observatory](https://skill-library-prod.web.app/) · [Infrastructure map](https://skill-library-prod.web.app/infra)

## Start here — applied AI for drug development

The work I care most about is turning clinical-development and regulatory judgment into agents that show their reasoning:

- **[Asclepius](https://github.com/npbuilds/asclepius)** (its own repo) — an AI agent system that reasons about a single drug program end to end: probability-of-success anchored to real trial outcomes, phase-gated rNPV, an 8-pillar clinical/regulatory scorecard, and a memo that forms a *falsifiable* view and names the one readout that would flip it. Every number ships its citation.
- **`skills/biotech-venture/`** (42 skills) — the diligence engine behind it: clinical-development planning, endpoint and trial-design critique, probability-of-success estimation, regulatory-path reasoning, and evidence-tiered synthesis.

That's the through-line in all of it: **AI earns adoption when it scaffolds an expert with structured, cited synthesis — not when it tries to replace the expertise.**

## How it works

- **One registry is the source of truth** (`data/registry.json`) — every skill's metadata, dependencies, and scores. CI enforces zero drift between the skill files, the registry, and the search index.
- **Skills compose.** Orchestrator skills dispatch sub-skills through typed *Accepts / Produces* contracts wired into DAG pipelines, so a high-level ask (e.g. "diligence this asset") fans out to specialists and reassembles.
- **Served over MCP.** A read-only MCP server exposes the library to Claude and Codex — including `search_skills`, `get_skill`, `analyze_impact`, and a live health/telemetry loop. See `mcp-server/` and the [Codex gateway guide](docs/codex-skill-library-gateway.md).
- **It maintains itself.** A QA loop tracks usage, gaps, and feedback, and opens PRs to keep the registry, wiring, and scores calibrated.

## The 19 subject domains — one architecture, many experiments

I use the same skill-and-orchestration pattern everywhere I'm curious. The biotech and research domains are the serious work; the rest are where I pressure-test whether the architecture generalizes.

| Domain | Skills | | Domain | Skills |
|---|---:|---|---|---:|
| investing | 56 | | worldbuilding | 27 |
| collector | 54 | | binding-vow (prompt craft) | 27 |
| world-history | 53 | | game-theory | 22 |
| professional-development | 42 | | design | 17 |
| **biotech-venture** | **42** | | data-science | 17 |
| sommelier | 36 | | neocortex | 13 |
| writing | 34 | | infrastructure | 12 |
| product | 31 | | research | 11 |
| philosophy | 29 | | (+ artifacts, narrative, internal meta) | 5 |

## Browsing

Each skill is a `SKILL.md` with YAML frontmatter (name, description, dependencies, evidence conventions) plus reference docs and, for many, an eval harness. Start in `skills/biotech-venture/` or `skills/research/`; `data/registry.json` is the machine-readable index of everything.

---

*Built independently, for my own use. Not a product.*
