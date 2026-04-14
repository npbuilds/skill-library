---
name: constraint-sculptor
description: >
  Frameworks for using constraints as creative tools in product design. The right constraints
  channel emergence productively; too many kill it; too few produce chaos. Covers scope
  constraints, interface constraints, behavioral boundaries, safety rails, and the art of
  knowing what to leave open.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep
---

# Constraint Sculptor — The Art of Productive Limitation

Constraints are the most misunderstood element of product design. Traditional PM treats constraints as obstacles — things that limit what you can build. AI-native product design treats constraints as **creative tools** — things that shape what emerges.

A river without banks is a flood. A river with banks is a force.

## The Constraint Spectrum

```
Too few constraints         Edge of chaos           Too many constraints
     CHAOS ←————————————— EMERGENCE ——————————————→ STAGNATION
   (anything goes,          (productive,             (nothing unexpected,
    nothing useful)          surprising)              nothing alive)
```

The sweet spot — Kauffman's "edge of chaos" — is where enough structure exists to channel behavior but enough openness exists for surprise.

## Constraint Types

### Hard Constraints (Non-Negotiable Boundaries)

Things the product must NEVER do. These are safety rails, ethical boundaries, and scope limits.

**Design principle:** Hard constraints should be few, clear, and absolute. If you have more than 5 hard constraints on a seed, you're over-constraining.

Examples:
- "The system must never present speculation as fact" (epistemic boundary)
- "The system must never take irreversible actions without confirmation" (safety rail)
- "This product surface must not exceed 3 interaction steps" (scope boundary)

### Soft Constraints (Preferences That Can Flex)

Things the product SHOULD do, but can override when the situation demands it.

**Design principle:** Soft constraints are where most of the creative shaping happens. They establish defaults and tendencies without eliminating emergence.

Examples:
- "Prefer concise responses unless the user signals they want depth" (behavioral preference)
- "Default to the conversational paradigm unless the task implies a different one" (interaction default)
- "Prioritize familiar patterns for new users, but expose power features progressively" (exposure preference)

### Open Space (Intentional Gaps)

Areas deliberately left unconstrained. This is where emergence happens.

**Design principle:** Open space isn't laziness — it's the most important design decision. Specify what you're intentionally leaving open and why.

Examples:
- "How the system combines writing and design capabilities is left open — we want to see what emerges"
- "The tone the system develops with each user is unconstrained — it should evolve from interaction"
- "The order in which capabilities surface is left to the system's read of user behavior"

## The Constraint Design Process

1. **Start with the thesis** — What behavior do we want to emerge?
2. **Identify the minimum hard constraints** — What would make emergence dangerous or useless?
3. **Add soft constraints for direction** — What tendencies channel toward the thesis?
4. **Explicitly define open space** — What are we intentionally NOT constraining?
5. **Check the ratio** — First seeds: ~20% hard, ~20% soft, ~60% open. Tighten as you learn.

## Constraint Patterns

| Pattern | When to Use | Example |
|---|---|---|
| **Guardrails** | Prevent harm without limiting function | "Never commit financial transactions without explicit confirmation" |
| **Defaults** | Establish baseline that can be overridden | "Start in conversational mode, switch paradigms if user signals" |
| **Boundaries** | Define the edges of the product's world | "This surface handles design questions only — route others to The Loom" |
| **Rhythms** | Establish temporal patterns | "Synthesize weekly, not daily" |
| **Ladders** | Progressive capability exposure | "Show basic capabilities first; unlock advanced after 5 successful interactions" |

## Cross-Domain

- **game-theory/mechanism-design** — Constraints on multi-agent systems need incentive compatibility. A constraint that can be gamed will be gamed.
- **philosophy-orchestrator** — Ethical constraints require philosophical grounding, not just rule lists.
