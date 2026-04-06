---
name: skill-network
description: >
  Visualize the skill network as an ASCII dependency graph. Use when the user wants to see
  how skills connect, trace dependency chains, find orphaned skills, or understand the
  relationship topology of the mycelial network.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Bash Grep Glob
---

# Skill Network — The Cartographer

Map and visualize the mycelial network of skill relationships. Reads the registry to produce ASCII dependency graphs, detect orphans, and reveal the network topology.

## Operations

### 1. Full Network Graph

Display all skills and their relationships as an ASCII directed graph:

```
SKILL NETWORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                       skill-registry (100)
       ┌────┬────┬────┬────┼────┬──────┬──────┐
       │    │    │    │    │    │      │      │
       ▼    ▼    ▼    ▼    ▼    ▼      ▼      ▼
     health dash test anlz fork net  export scaffold
       │         │              │             │
       │         └──► analyze   │             │
       └──► dashboard           │             │
                          ┌─────┘             │
                          ▼                   │
                     scaffold ◄───────────────┘
                          │
                          ▼
                     skill-fork

Legend: ─▶ depends_on   (100) = composite score
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nodes: 9    Edges: 14    Orphans: 0    Max depth: 4
```

### 2. Dependency Chain

Trace the full dependency chain for a specific skill:

```
CHAIN — skill-scaffold
━━━━━━━━━━━━━━━━━━━━━━━
skill-scaffold
  ├─ depends_on: skill-registry
  ├─ depends_on: skill-health
  │    └─ depends_on: skill-registry ◄ (already visited)
  │    └─ depends_on: skill-dashboard
  │         └─ depends_on: skill-registry ◄ (already visited)
  └─ depends_on: skill-dashboard ◄ (already visited)

Depth: 3    Unique dependencies: 3
```

### 3. Reverse Dependencies (Impact Analysis)

Show what breaks if a skill changes:

```
IMPACT — skill-registry
━━━━━━━━━━━━━━━━━━━━━━━
skill-registry is referenced by:
  ├─ skill-health
  ├─ skill-dashboard
  ├─ skill-scaffold
  ├─ skill-test
  ├─ skill-analyze
  ├─ skill-fork
  ├─ skill-network
  └─ skill-export

Direct dependents: 8    Total (transitive): 8
⚠ HIGH IMPACT — changes affect 100% of the network
```

### 4. Orphan Detection

Find skills with no connections (neither depends_on nor referenced_by):

```
ORPHANS
━━━━━━━━
  (none found — all skills are connected)
```

Or if orphans exist:
```
  ⚠ skill-lonely — no dependencies, not referenced by anyone
    Suggestion: connect to domain peers or consider archiving
```

## How to Build the Graph

1. Read `data/registry.json`
2. For each skill, collect `depends_on` and `referenced_by`
3. Build an adjacency list
4. Detect cycles (should not exist — warn if found)
5. Compute depth via BFS from root nodes (skills with no `depends_on`)
6. Render as ASCII using box-drawing characters

Read `references/graph-rendering.md` for ASCII rendering rules.
