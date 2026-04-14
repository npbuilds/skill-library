---
name: infrastructure-orchestrator
description: >
  Orchestrate skill library management across the full lifecycle. Use when the user wants to
  create a new skill, audit the library, build a domain from scratch, run diagnostics, export
  skills, or perform any multi-step operation that involves coordinating multiple infrastructure
  tools — scaffold, registry, health, test, analyze, network, dashboard, export, or fork.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Infrastructure Orchestrator — The Architect

Coordinate the skill library's self-management tools. When a user says "build me a new skill," "audit the library," or "set up a new domain," this orchestrator sequences the right infrastructure tools in the right order to get the job done.

## Phases

### Phase 1 — Understand the Operation

Before invoking any tool, classify what the user needs:

- **Scope** — Single skill, subdomain, full domain, or entire library?
- **Operation type** — Create, read, update, delete, audit, export, or analyze?
- **Urgency** — Quick one-off or thorough deep process?
- **Context** — Is this a new domain from scratch, or maintenance on existing skills?

If the user provides a vague request like "clean up the library" or "add something for X," ask targeted questions to determine scope and operation type before proceeding.

### Phase 2 — Classify and Route

Determine which infrastructure skill(s) to invoke.

**Operation routing summary:**

| Operation | Primary Skill | Supporting Skills | When |
|-----------|--------------|-------------------|------|
| Create a skill | `skill-scaffold` | `skill-registry`, `skill-health` | User wants a new skill |
| Check skill quality | `skill-health` | `skill-registry` | User asks "is this skill good?" |
| Run tests on a skill | `skill-test` | `skill-health` | User wants to validate behavior |
| Analyze API/patterns | `skill-analyze` | `skill-registry` | Deep skill structure analysis |
| Visualize the library | `skill-dashboard` | `skill-registry` | User wants a status overview |
| Map relationships | `skill-network` | `skill-registry` | User wants dependency/connection graphs |
| Export skills | `skill-export` | `skill-registry` | User wants to package skills for sharing |
| Fork/decompose | `skill-fork` | `skill-scaffold`, `skill-registry` | User wants to split or derive skills |
| Full audit | `skill-health` | All others | User wants a comprehensive library checkup |
| Build new domain | `skill-scaffold` | `skill-registry`, `skill-health`, `skill-test` | User wants a complete new domain |

### Phase 3 — Plan the Sequence

Multi-step operations require careful sequencing. Common workflows:

**Create a Single Skill:**
1. `skill-scaffold` → generate files from template
2. `skill-registry` → register the new skill
3. `skill-health` → validate it passes quality gates

**Build a New Domain:**
1. Determine domain structure (orchestrator, directors, knowledge skills)
2. `skill-scaffold` → create orchestrator first (it defines the domain's routing)
3. `skill-scaffold` → create directors for each subdomain
4. `skill-scaffold` → create knowledge skills under each director
5. `skill-registry` → register all skills with proper relationships
6. `skill-health` → run health checks on everything
7. `skill-network` → map the new domain's internal connections
8. `skill-dashboard` → generate updated overview

**Full Library Audit:**
1. `skill-registry` → sync (discover new, flag missing)
2. `skill-health` → run health checks on all skills
3. `skill-analyze` → deep analysis on any flagged skills
4. `skill-network` → check for orphans, broken references, isolated clusters
5. `skill-dashboard` → generate comprehensive report

**Fork a Skill:**
1. `skill-analyze` → understand current skill structure
2. `skill-fork` → determine decomposition strategy
3. `skill-scaffold` → create the new skills
4. `skill-registry` → register new skills, update relationships on the original
5. `skill-health` → validate all new skills

### Phase 4 — Execute

Invoke the infrastructure skills in sequence. After each step:

1. Verify the step succeeded (check output, validate files exist)
2. Pass relevant context to the next step (registry entry, health results, etc.)
3. If a step fails, diagnose and recover rather than continuing with broken state

For domain-building operations, launch sub-agents for parallel skill creation when skills are independent (e.g., knowledge skills under different directors can be scaffolded in parallel).

### Phase 5 — Report

After the operation completes:

1. **Summary** — What was done, what changed, what was created
2. **Health status** — Are all affected skills healthy?
3. **Registry state** — Is the registry in sync?
4. **Next steps** — What should the user do next? (edit SKILL.md content, add references, run tests)

```
OPERATION COMPLETE — {operation name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scope:       {single skill / subdomain / domain / library}
Skills:      {N} created, {N} updated, {N} flagged
Health:      {all healthy / N warnings / N critical}
Registry:    {in sync / N unregistered}

Next steps:
  1. {most important follow-up}
  2. {second priority}
```

## Knowledge Layer

The infrastructure tools are all action skills — they do things rather than explain things. Route directly to the skill that matches the operation.

**Available infrastructure skills:**

| Skill | Path | What It Does |
|-------|------|-------------|
| skill-scaffold | `skills/infrastructure/skill-scaffold/SKILL.md` | Create new skills from templates |
| skill-registry | `skills/infrastructure/skill-registry/SKILL.md` | Manage the skill catalog |
| skill-health | `skills/infrastructure/skill-health/SKILL.md` | Check skill quality and health |
| skill-test | `skills/infrastructure/skill-test/SKILL.md` | Run tests on skill behavior |
| skill-analyze | `skills/infrastructure/skill-analyze/SKILL.md` | Deep structural analysis |
| skill-dashboard | `skills/infrastructure/skill-dashboard/SKILL.md` | Visual status overview |
| skill-network | `skills/infrastructure/skill-network/SKILL.md` | Dependency and relationship mapping |
| skill-export | `skills/infrastructure/skill-export/SKILL.md` | Package skills for sharing |
| skill-fork | `skills/infrastructure/skill-fork/SKILL.md` | Decompose or derive skills |

## Failure Recovery

- If scaffolding fails, check templates exist and paths are valid before retrying
- If registration fails, verify the SKILL.md file was actually created
- If health check reports critical issues on a brand new skill, it's likely a template problem — check the template, not the skill
- If the user asks for something no infrastructure skill handles, say so rather than forcing a tool to do something it wasn't built for
- For domain-building operations, checkpoint after each major phase (orchestrator, directors, knowledge skills) so partial progress isn't lost

## Scope Boundaries

This orchestrator handles **skill library lifecycle operations**. It does NOT:
- Write the actual content of skills (it creates the structure; the user or another orchestrator fills in domain knowledge)
- Make decisions about what domains or skills to build (it asks the user or takes direction from Sentinel Prime)
- Manage the MCP server or plugin configuration (those are separate infrastructure)
- Interact with external systems (no git, no deployment — those are user operations)
