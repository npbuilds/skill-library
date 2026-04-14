---
name: learning-loops
description: >
  Frameworks for designing self-improving systems. How does the product get better without
  manual intervention? Reinforcement from use, capability compounding, knowledge accumulation,
  behavioral refinement. The meta-skill of making intelligence products that learn.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep
---

# Learning Loops — Self-Improving Intelligence

The ultimate goal of an intelligence product is to learn from use without manual intervention. Not just feedback loops (which react) but **learning loops** (which develop new capabilities or deepen existing ones).

A product with good learning loops gets better every day. A product without them is frozen at the quality of its initial design.

## Types of Learning

### Behavioral Refinement

The system gets better at doing what it already does.

**Mechanism:** Each interaction provides signal about what works. The system adapts its defaults, its tone, its depth, its timing.

**Example:** A writing surface that gradually learns the user's voice preferences — not through settings, but through observing which outputs the user accepts, edits, or rejects.

**Design requirement:** A clear quality signal. If you can't tell good output from bad output, the system can't learn the difference either.

### Capability Compounding

Capabilities combine to create new capabilities that weren't designed.

**Mechanism:** As more domains are engaged and more cross-domain patterns are observed, new capability combinations become available — not because anyone built them, but because the connections existed latently and use revealed them.

**Example:** The skill library itself. Each new domain doesn't just add knowledge — it creates new cross-domain combinations with every existing domain.

**Design requirement:** Rich cross-domain connections. Isolated capabilities don't compound.

### Knowledge Accumulation

The system knows more over time because interactions deposit knowledge.

**Mechanism:** Each use case, each question answered, each problem solved adds to the system's working knowledge. Not just data — understanding.

**Example:** A product research surface that accumulates institutional knowledge about the builder's products, users, market — knowledge that makes every future analysis richer.

**Design requirement:** Persistent memory architecture. Knowledge must survive across sessions.

### Pattern Recognition Deepening

The system gets better at seeing patterns across disparate signals.

**Mechanism:** With enough observations, the system begins to see connections between signals that humans miss — because it has a broader view across time and domains.

**Example:** The Loom's pattern-weaver getting better at predicting which capability combinations will produce valuable emergence, based on accumulated experience with past seeds.

**Design requirement:** Cross-signal visibility. The system must be able to observe multiple data streams simultaneously.

## Designing for Learning

### The Learning Budget

Not everything should be learned automatically. Some things should remain under human control.

| Learn Automatically | Learn with Permission | Never Learn |
|---|---|---|
| Tone and style preferences | Strategic direction changes | Ethical boundaries |
| Interaction pacing | Exposure decisions | Safety constraints |
| Capability selection for tasks | Value/pricing adjustments | Kill criteria |
| Response depth calibration | New capability development | Core thesis changes |

### The Learning Rate

How fast should the system adapt?

| Too Slow | Just Right | Too Fast |
|---|---|---|
| User feels unheard. Repeats preferences. | System adapts naturally. User notices improvement. | System is unstable. Overreacts to single signals. |

**Rule of thumb:** Require 3+ consistent signals before adapting a default. Single signals are noise; repeated signals are learning.

### The Forgetting Function

Learning without forgetting leads to stale intelligence. The system must also unlearn:

- Preferences that were relevant 6 months ago but aren't now
- Patterns from a context that no longer exists
- Optimizations for a user behavior that has changed

**Design:** Time-decay on learned behaviors. Recent signals weighted more than old ones. Periodic review of accumulated learning.

## Cross-Domain

- **data-science-orchestrator** — For quantitative modeling of learning dynamics. "Is the system actually getting better, or does it just feel like it?"
- **game-theory-orchestrator** — Learning in games. When the user adapts to the system AND the system adapts to the user, you need game-theoretic analysis to understand the equilibrium.
