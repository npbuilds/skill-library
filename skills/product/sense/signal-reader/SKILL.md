---
name: signal-reader
description: >
  Frameworks for reading external signals through a product lens — market timing, technology
  adoption curves, readiness levels, competitive shifts, and demand indicators. Use when
  evaluating whether a capability is ready for product exposure, whether the market timing
  is right, or how to interpret weak signals about user needs and technology shifts.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Signal Reader — External Intelligence Frameworks

While frontier-antenna reads AI developments and emergence-detector watches internal capability combinations, signal-reader provides the frameworks for interpreting **external** signals: markets, users, technology adoption, and competitive dynamics.

This is the knowledge skill of the Sense director — it teaches how to read signals, not what the signals currently say.

## Signal Categories

### Technology Readiness Signals

When is a capability ready for product exposure?

| Signal | What It Means | Product Implication |
|---|---|---|
| Works in demos, fails in production | Capability is pre-ready | Seed, don't surface. Prototype to understand failure modes. |
| Works reliably but requires expertise | Capability is expert-ready | Surface to power users. Design for progressive disclosure. |
| Works reliably for general users | Capability is market-ready | Surface broadly. Compete on experience, not capability. |
| Multiple competitors offer it | Capability is commoditized | Differentiate on synthesis, not the capability itself. |

**Technology Readiness Levels (adapted for AI products):**

1. **Theoretical** — Research papers suggest it's possible
2. **Demonstrated** — Works in controlled conditions (benchmarks, demos)
3. **Prototype** — Works in your system with effort
4. **Reliable** — Works consistently with minimal intervention
5. **Productized** — Works as a seamless part of a product experience
6. **Commoditized** — Everyone offers it; no competitive advantage

### Market Timing Signals

| Signal | Reading |
|---|---|
| High interest, few products | **Early window** — opportunity to define the category |
| Growing adoption of adjacent products | **Adjacent possible** — market is warming but hasn't arrived yet |
| Established competitors, stable market | **Late entry** — need 10x better or radically different surface |
| Market fatigue, user complaints about existing solutions | **Disruption window** — reframe the problem, not the solution |
| Regulatory uncertainty | **Wait or hedge** — monitor, prototype, but don't bet big |

### Demand Signals (for solo builders)

Without enterprise analytics, read demand through:

- **Watering holes** — Where do potential users gather? What do they complain about?
- **Proxy metrics** — Search volume, GitHub stars on related tools, forum activity
- **Direct conversation** — What do people ask you to build? What do they assume already exists?
- **Behavioral reveals** — What are people using awkward workarounds to accomplish?
- **Adjacent adoption** — When users adopt tool X, what complementary need does it create?

### Competitive Signals

| Signal | Reading |
|---|---|
| New entrant with funding, no product | **Validation** — someone else sees the opportunity. Speed matters. |
| Established player adds the capability | **Commoditization clock started** — differentiate on synthesis |
| Multiple small players, no dominant one | **Category is forming** — opportunity to define it |
| A player pivots away from the space | **Possible warning** — investigate why they left |
| Open-source alternative emerges | **Commoditization accelerating** — move up the value chain |

## Diffusion Curve Awareness

Products don't need to target the mass market. For a solo builder, the relevant question is: **which part of the diffusion curve are my users on?**

| Segment | Characteristics | Product Design Implication |
|---|---|---|
| Innovators (2.5%) | Tolerate rough edges, value novelty | Surface raw capability. Minimal experience layer. |
| Early adopters (13.5%) | Want advantage, tolerate setup effort | Surface with guidance. Clear value proposition. |
| Early majority (34%) | Want proven solutions, low friction | Surface with polish. Experience-first design. |
| Late majority (34%) | Want standards, resist change | Surface within existing workflows. Integration-first. |

Most AI-native products in 2026 are still in innovator/early-adopter territory. Design accordingly.

## Integration with Other Sense Skills

- **frontier-antenna** provides the raw capability signal; **signal-reader** provides the framework for interpreting its product readiness
- **capability-radar** maps what's possible; **signal-reader** assesses whether the market is ready for it
- **emergence-detector** surfaces surprises; **signal-reader** evaluates whether the surprise has external demand
