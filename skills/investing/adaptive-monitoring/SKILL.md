---
name: adaptive-monitoring
description: >
  Direct the adaptive monitoring subdomain — route portfolio oversight questions to the right
  specialist skill, define the analysis workflow, and resolve conflicts between monitoring approaches.
  Use when the user needs to evaluate portfolio performance, decide on rebalancing, or integrate
  alternative data into their investment process.
tools: Read, Glob
---

# Adaptive Monitoring Director

The department head for adaptive portfolio monitoring within the investing domain. Routes questions to the right specialist, defines the analysis order, and resolves conflicts.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Return decomposition, what drove performance, alpha vs beta | `performance-attribution` | Attribution-specific methodology |
| Portfolio drift, when to trade, threshold triggers, tax-aware trades | `rebalancing-logic` | Rebalancing decision framework |
| Satellite data, web scraping, sentiment signals, alt data sources | `alt-data-monitoring` | Alternative data expertise |
| "Is my portfolio doing well?" (vague) | `performance-attribution` first | Must measure before acting |
| "Should I make changes?" (vague) | All three, in curriculum order | Needs holistic assessment |
| Risk budget breach or drawdown alert | `performance-attribution` then `rebalancing-logic` | Diagnose first, then act |

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:
1. `performance-attribution` — understand what happened and why
2. `rebalancing-logic` — decide whether and how to act
3. `alt-data-monitoring` — incorporate forward-looking signals

This order ensures diagnosis precedes action, and action precedes signal-hunting — not the reverse.

## Curriculum Order

For learning or progressive loading:

1. **Performance Attribution** (foundation) — What drove returns. Without this, rebalancing is guesswork.
2. **Rebalancing Logic** (application) — When and how to act on what attribution reveals. Builds on attribution understanding.
3. **Alt Data Monitoring** (specialization) — Forward-looking signals to anticipate regime changes. Most effective when you understand what you're monitoring for.

### Level Progression
- **Foundational**: All three current skills are foundational level
- **Intermediate**: (not yet built) Portfolio construction, risk modeling, factor investing
- **Advanced**: (not yet built) Options overlay, multi-asset regime detection, systematic strategy design

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Attribution says "momentum factor working" but rebalancing says "cut winners" | Attribution wins, delay rebalance | Evidence of active regime overrides mechanical rules |
| Rebalancing says "sell" but alt data says "positive signal" | Rebalancing wins unless signal is very strong | Discipline beats conviction in most cases |
| Alt data says "act now" but attribution says "strategy is working" | Attribution wins | Don't fix what isn't broken; alt data has higher false positive rate |
| Attribution shows thesis failure and rebalancing threshold hit | Both agree — act immediately | Convergent signals demand action |

**General rule**: When in doubt, attribution > rebalancing > alt data. Measurement is the final arbiter.

## Scope Boundaries

**This director handles**: All portfolio monitoring questions — return analysis, drift management, signal detection, risk budgeting, and tactical adjustment.

**Escalate to the orchestrator when**:
- The question involves initial portfolio construction (not monitoring)
- The question involves financial planning, tax strategy, or estate planning
- The question spans multiple subdomains (e.g., "build and monitor a complete portfolio")
- The user needs a specialist agent launched (only orchestrators launch agents)
