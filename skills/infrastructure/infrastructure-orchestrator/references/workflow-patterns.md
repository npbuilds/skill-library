# Workflow Patterns

Common multi-skill orchestration patterns for infrastructure operations.

## Pattern Catalog

### 1. Single Skill Creation
**Trigger**: "Create a skill for X"
**Sequence**: scaffold → registry → health
**Duration**: Quick (1-2 minutes)

### 2. Domain Bootstrap
**Trigger**: "Build a new domain for X"
**Sequence**:
1. Design hierarchy (user input + meta-observer guidance)
2. scaffold orchestrator
3. scaffold directors (can parallelize)
4. scaffold knowledge skills (can parallelize per director)
5. registry sync
6. health audit
7. network map
8. dashboard refresh

**Duration**: Medium (5-15 minutes depending on domain size)

### 3. Full Library Audit
**Trigger**: "Run a full diagnostic" / "Audit everything"
**Sequence**: registry sync → health audit all → analyze flagged → network orphan check → dashboard report
**Duration**: Medium (3-10 minutes)

### 4. Skill Decomposition
**Trigger**: "This skill is too big" / "Split X into pieces"
**Sequence**: analyze → fork plan → scaffold new skills → registry update → health check
**Duration**: Medium (5-10 minutes)

### 5. Health Recovery
**Trigger**: "Fix all the warnings"
**Sequence**: health audit → triage (critical first) → per-skill remediation → re-check
**Duration**: Variable

### 6. Export Package
**Trigger**: "Package X for sharing"
**Sequence**: registry read → health pre-check → export build → validation
**Duration**: Quick (1-3 minutes)

## Parallelization Rules

- Skills under **different directors** can be scaffolded in parallel
- Skills under the **same director** should be created sequentially (to track naming conflicts)
- **Registry writes** must be serialized (JSON file locking)
- **Health checks** can run in parallel (read-only)
- **Network analysis** must wait for all registry updates to complete
