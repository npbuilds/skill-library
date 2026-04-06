---
name: frontier-scanner
description: >
  Scan the AI frontier for emerging capabilities, model developments, tool patterns, and
  paradigm shifts. Use when tracking what's new in AI, understanding capability jumps,
  evaluating whether a new development changes what's possible, or providing context for
  skill library planning.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep WebSearch WebFetch
---

# Frontier Scanner — The Telescope

Watches the AI horizon and translates what's happening into actionable intelligence for the skill library. Not a news aggregator — a capability analyst. The question isn't "what launched?" but "what's now *possible* that wasn't before?"

## Core Function

Track developments across the AI landscape and assess their implications for the skill library's architecture and growth. Every scan answers three questions:

1. **What changed?** — New models, tools, techniques, paradigms
2. **What does it enable?** — Capabilities that didn't exist or weren't practical before
3. **What does it mean for us?** — How should the skill library respond?

## Scan Categories

### 1. Model Capabilities
What can AI models do now that they couldn't before?

| Dimension | What to Track | Why It Matters |
|-----------|--------------|----------------|
| Reasoning depth | Chain-of-thought improvements, multi-step problem solving | Determines which skills can be more ambitious |
| Context window | Token limits, long-context performance | Affects how much reference material skills can load |
| Multimodal | Vision, audio, code execution, tool use | Opens entirely new skill categories |
| Agentic behavior | Planning, tool chaining, autonomous operation | Changes what "a skill" can even be |
| Speed/cost | Latency improvements, pricing changes | Makes some approaches practical that weren't before |

### 2. Tool Ecosystem
What new tools, frameworks, and integrations exist?

| Dimension | What to Track | Why It Matters |
|-----------|--------------|----------------|
| MCP servers | New Model Context Protocol integrations | Directly extends what skills can access |
| IDE integration | Editor plugins, workflow tools | Changes how skills are invoked |
| Agent frameworks | New agent SDKs, orchestration patterns | May suggest new skill architecture patterns |
| Data access | New APIs, databases, knowledge sources | Expands what skills can know about |

### 3. Paradigm Shifts
What fundamental assumptions about AI are changing?

| Signal | Example | Implication |
|--------|---------|-------------|
| New interaction pattern | Conversational → agentic → ambient | Skill invocation models may need rethinking |
| Capability plateau | A previously fast-improving area levels off | Shift investment to areas still improving |
| Unexpected emergence | Models suddenly good at something nobody predicted | New skill category opportunity |
| Commoditization | Something that was cutting-edge becomes table stakes | Existing skills may need less sophistication, new skills become possible |

## Source Intelligence

All scans draw from the curated source registry: `references/source-registry.md`

Sources are tiered by signal density:
- **Tier 1** (every scan): Model lab blogs, tool ecosystem changelogs, MCP/SDK repos
- **Tier 2** (weekly): Practitioner analysis blogs, arXiv/HuggingFace research feeds
- **Tier 3** (when relevant): Domain-specific AI applications mapped to library domains

Anti-sources (hype aggregators, listicles, LinkedIn thought leadership) are explicitly excluded.

## Scan Process

### Quick Scan (weekly scheduled task)
1. Hit Tier 1 primary sources for new announcements
2. Skim Tier 2 practitioner blogs for pattern synthesis
3. Cross-reference against library domains using Tier 3
4. Flag anything that changes what's possible

### Deep Scan (on-demand, triggered by [ACTION NEEDED] or user request)
Uses `research/spelunker` methodology for epistemic rigor:

1. **Survey** — Map the current state of AI capabilities across all dimensions
2. **Delta** — What changed since last scan? What's trending?
3. **Decompose** — Break each development into atomic claims (spelunker Phase 2)
4. **Triangulate** — Verify claims across multiple independent sources (spelunker Phase 3)
5. **Adversarial pass** — For every significant claim, actively search for counterevidence, limitations, and what the announcement does NOT say (spelunker Phase 5). Tag confidence: Confirmed / Likely / Speculative / Contested
6. **Implication analysis** — For each verified change:
   - What skill categories does this enable?
   - What existing skills does this make more/less valuable?
   - What architectural assumptions does this challenge?
7. **Opportunity ranking** — Prioritize implications by impact × urgency
8. **Briefing** — Present findings using clarity-engine framing (headline → picture → evidence → recommendation)

## Output Format

```
FRONTIER SCAN — [Date]
Scan Type: [Quick / Deep]

Headline: [One sentence — the most important thing]

Key Developments:
  1. [Development] → enables [capability] → suggests [library action]
  2. [Development] → enables [capability] → suggests [library action]
  3. ...

Capability Shifts:
  Expanding: [areas where AI is getting notably better]
  Plateauing: [areas where improvement has slowed]
  Emerging: [new capabilities appearing]

Library Implications:
  Build: [new skills/domains this suggests]
  Evolve: [existing skills that should be updated]
  Retire: [skills that may become less relevant]
  Connect: [new cross-domain edges this creates]

Confidence: [High / Medium / Low — how certain are these assessments?]
```

## What This Skill Does NOT Do

- **Predict specific timelines** — "AGI by 2027" is not a useful output. Capability trajectories are; dates are noise.
- **Hype relay** — Every AI announcement claims to be revolutionary. This skill filters signal from marketing.
- **Technical deep dives** — If the user wants to *understand* a development in depth, hand off to clarity-engine. Frontier-scanner identifies and assesses; clarity-engine explains.

## Cross-Domain Connections

- **Research/spelunker**: Deep scan mode borrows spelunker's full methodology — claim decomposition, source triangulation, adversarial pass, confidence tagging. For deep dives into specific developments frontier-scanner surfaces
- **Neocortex/clarity-engine**: To explain findings in plain language with visual framing
- **Neocortex/growth-architect**: Frontier findings feed directly into build prioritization
- **Infrastructure/skill-registry**: To check current library state when assessing implications
