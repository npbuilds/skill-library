---
name: pattern-synthesizer
description: >
  Detect recurring patterns across domains in the skill library — shared structures,
  parallel architectures, common abstractions, and missing connections. Use when noticing
  similarities between domains, looking for deeper organizing principles, or identifying
  structural opportunities the library isn't exploiting.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep
---

# Pattern Synthesizer — The Weaver

Finds the threads that run through multiple domains but nobody named yet. Every skill library develops emergent patterns as it grows — the synthesizer makes them visible.

Think of it like looking at a city from a helicopter. At street level, you see individual buildings. From the air, you see that three different neighborhoods independently built the same kind of town square. That's not coincidence — it's an unnamed pattern that wants to be recognized.

## Core Function

Scan the skill library for recurring structures, parallel architectures, and unnamed abstractions that span multiple domains. Every pattern found is either:

1. **A connection opportunity** — Two domains doing the same thing independently should know about each other
2. **An abstraction opportunity** — A pattern that appears 3+ times might deserve its own skill
3. **An architectural insight** — The pattern reveals something about how knowledge is structured

## Pattern Types

### 1. Structural Parallels
Same architecture, different content.

| Pattern | Example | What It Suggests |
|---------|---------|-----------------|
| Parallel skill trees | Ethics has dilemma-analyzer; decision-theory has decision-architect. Both apply multiple frameworks in parallel and compare results | Shared "multi-framework analysis" pattern — could share methodology |
| Mirror directors | Investing and game-theory both have "strategy + psychology" subdivisions | Domain-independent "strategy/psychology" structure |
| Repeated reference patterns | Multiple domains have "taxonomy" reference files | Common need for classification infrastructure |

### 2. Cross-Domain Isomorphisms
Different domains that are secretly the same problem.

| Domain A | Domain B | Shared Structure |
|----------|----------|-----------------|
| Ethics/stakeholder-mapper | Investing/risk-architecture | Both map affected parties and assess impact — stakeholders vs. risk factors |
| Philosophy/belief-auditor | Investing/reflexivity-sentiment | Both check whether beliefs are coherent and well-calibrated |
| Worldbuilding/magic-systems | Game-theory/mechanism-design | Both design rule systems with emergent consequences |
| Writing/narrative-arc | Investing/macro-cycles | Both model phase transitions (setup → rising action → climax maps to expansion → peak → contraction) |

### 3. Missing Abstractions
A concept that appears in multiple domains but has no home.

| Unnamed Pattern | Where It Appears | Candidate Abstraction |
|----------------|-----------------|----------------------|
| "Apply N frameworks, compare results" | Ethics, decision-theory, epistemology, investing | Multi-framework analysis engine |
| "Map hidden assumptions" | Logic/assumption-excavator, ethics/values-excavator, epistemology/belief-auditor | General excavation methodology |
| "Evaluate quality on multiple dimensions" | Evidence-evaluator, methodology-critic, model-evaluation | Multi-dimensional quality assessment |
| "Route based on question type" | Every director skill | Routing is itself a pattern worth studying |

### 4. Edge Patterns
Patterns in how domains connect (or fail to).

| Pattern | Signal | Meaning |
|---------|--------|---------|
| **Hub domain** | One domain connects to 5+ others | This domain contains general infrastructure knowledge |
| **Island domain** | Domain has 0-1 external connections | Either self-contained or under-connected |
| **Bridge skill** | One skill connects two otherwise separate domains | High-value — losing this skill disconnects the graph |
| **Parallel edges** | Multiple skills in Domain A connect to Domain B | Strong relationship — consider a dedicated interface |

## Synthesis Process

### Quick Pattern Scan
1. Read the registry for domain and edge data
2. Look for structural parallels in skill tree shapes
3. Identify the top 3 unnamed patterns

### Deep Synthesis
1. **Structural survey** — Map every domain's architecture (types, depths, shapes)
2. **Isomorphism detection** — For each domain pair, check: "Are any skills doing the same thing in different language?"
3. **Abstraction mining** — Find concepts that appear 3+ times across domains without their own skill
4. **Edge analysis** — Map the full connection graph, identify hubs/islands/bridges
5. **Pattern naming** — Give each discovered pattern a clear name and description
6. **Recommendation** — For each pattern: connect, abstract, or just note?

## Output Format

```
PATTERN SYNTHESIS — [Date]
Domains Analyzed: [list]

Patterns Found:

1. [Pattern Name]
   Type: [structural parallel / isomorphism / missing abstraction / edge pattern]
   Appears in: [Domain A, Domain B, ...]
   Description: [What the pattern is, in plain language]
   Analogy: [A visual/intuitive way to understand it]
   Recommendation: [Connect / Abstract into new skill / Note for future / No action]

2. ...

Highest-Impact Pattern:
  [Name] — [Why this one matters most and what to do about it]

Structural Observations:
  - [Insight about the library's overall shape]
  - ...
```

## Cross-Domain Connections

- **Neocortex/skill-cartographer**: Cartographer finds gaps; synthesizer explains *why* the gaps exist (structural patterns creating blind spots)
- **Neocortex/growth-architect**: Patterns inform build priorities — if a pattern appears 5 times, the underlying abstraction is high-value
- **Infrastructure/skill-network**: Network provides the raw connection graph; synthesizer interprets the patterns within it
- **Philosophy/logic/assumption-excavator**: Meta-connection — the synthesizer does for the library what assumption-excavator does for arguments (surfaces what's implicit)
