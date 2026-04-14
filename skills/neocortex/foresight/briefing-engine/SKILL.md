---
name: briefing-engine
description: >
  Synthesize intelligence from all Neocortex skills into strategic briefings for the user.
  Use when the user wants the big picture on library strategy, needs a status update on
  what's changed, wants to understand where things stand and what comes next, or asks
  to be briefed on the state of the brain.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep bash
---

# Briefing Engine — The Herald

Gathers intelligence from every corner of Neocortex and distills it into a clear, actionable strategic briefing. The herald doesn't generate new analysis — it synthesizes what the other skills have found into a coherent picture the user can act on.

Think of the other Neocortex skills as field agents: the scanner watches the frontier, the cartographer maps the territory, the synthesizer finds patterns, the evolutionist checks the troops. The herald collects all their reports and delivers the briefing to command.

## Core Function

Produce strategic briefings that answer the user's implicit question: **"What do I need to know about my skill library and the AI landscape right now?"**

Every briefing synthesizes up to 5 intelligence streams:

| Stream | Source Skill | What It Provides |
|--------|-------------|-----------------|
| **Frontier** | frontier-scanner | What's new or changing in AI capabilities |
| **Coverage** | skill-cartographer | Library gaps, underdeveloped areas, structural issues |
| **Patterns** | pattern-synthesizer | Cross-domain connections, unnamed abstractions |
| **Evolution** | skill-evolutionist | Stale skills, upgrade opportunities, maturity status |
| **Strategy** | growth-architect | Build priorities, sequence recommendations |
| **Scenarios** | scenario-planner | Future states, robust vs. contingent moves |

Not every briefing needs all streams. Match the briefing scope to the user's question.

## Briefing Types

### Quick Pulse (1-minute read)
When the user asks "what's going on?" or "anything I should know?"

```
NEOCORTEX PULSE — [Date]

Headline: [One sentence — the most important thing right now]

Key Changes Since Last Briefing:
  - [Change 1]
  - [Change 2]
  - [Change 3]

Action Items:
  - [Most urgent thing to do]

Library Vital Signs:
  Total Skills: [N] | Domains: [M] | Health: [overall status]
```

### Strategic Briefing (5-minute read)
When the user asks "brief me" or "what's the strategy?"

```
NEOCORTEX STRATEGIC BRIEFING — [Date]

═══ EXECUTIVE SUMMARY ═══
[2-3 sentences: the state of play and the recommended direction]

═══ AI LANDSCAPE ═══
[Frontier-scanner findings]
Key Developments: [what changed]
Capability Trajectory: [what's improving, plateauing, emerging]
Implications for Library: [what this means for us]

═══ LIBRARY STATE ═══
[Cartographer + evolutionist findings]
Coverage: [strong areas, weak areas, gaps]
Health: [skills needing attention, staleness flags]
Structure: [hub/orphan/bridge patterns]

═══ PATTERNS & CONNECTIONS ═══
[Pattern-synthesizer findings]
Cross-Domain Patterns: [what threads run through multiple domains]
Missing Abstractions: [patterns that deserve their own skill]
Connection Opportunities: [edges that should exist but don't]

═══ STRATEGIC DIRECTION ═══
[Growth-architect + scenario-planner findings]
Build Priorities: [what to build next, with rationale]
Scenario Robustness: [does the plan hold across futures?]
Recommended Sequence: [wave plan]

═══ ACTION ITEMS ═══
  Priority 1: [most important action]
  Priority 2: [second]
  Priority 3: [third]

═══ SIGNPOSTS TO WATCH ═══
[From scenario-planner: what to monitor]
```

### Domain Focus Briefing
When the user asks about a specific domain: "Brief me on the state of investing skills"

```
DOMAIN BRIEFING — [Domain Name]

Domain Snapshot:
  Skills: [N] | Directors: [M] | Health: [status]
  Last Major Change: [date and what changed]

Coverage Assessment:
  Strong: [well-covered areas]
  Thin: [areas with shallow coverage]
  Missing: [gaps relative to comprehensive treatment]

Evolution Status:
  [List of skills with maturity stage and any staleness flags]

Cross-Domain Connections:
  Active: [existing edges to other domains]
  Missing: [connections that should exist]

Recommendations:
  - [Specific action for this domain]
```

## Briefing Principles

1. **Headline first** — The single most important thing goes at the top. If the user reads nothing else, they get the headline.
2. **Delta over state** — Emphasize what *changed* since the last briefing, not just what *is*. Static snapshots are less useful than change detection.
3. **Action-oriented** — Every briefing ends with concrete action items. Intelligence without action is trivia.
4. **Confidence-tagged** — When synthesizing from multiple streams, note confidence levels. "Cartographer is confident about gap X; scenario-planner rates it medium probability."
5. **Visual framing** — Use clarity-engine's approach: lead with the picture, ground in evidence, connect to what the user knows. Briefings should be intuitive, not walls of text.
6. **Honest about gaps** — If a stream has no data (e.g., no frontier scan has been run recently), say so rather than guessing.

## Briefing Process

1. **Scope** — What type of briefing? (Pulse / Strategic / Domain Focus)
2. **Gather** — Collect the latest from relevant source skills
3. **Synthesize** — Look for connections, contradictions, and convergence across streams
4. **Prioritize** — Rank findings by impact and urgency
5. **Frame** — Apply clarity-engine principles (headline, picture, evidence, recommendation)
6. **Deliver** — Present in the appropriate template

## What This Skill Does NOT Do

- **Generate primary analysis** — Briefing-engine synthesizes other skills' findings. It doesn't do its own frontier scans, gap analyses, or pattern detection.
- **Replace archon** — Archon produces investment-specific briefings with a different structure, voice, and purpose. Briefing-engine handles library strategy briefings.
- **Make decisions** — Briefings inform the user's decisions. The user decides what to build.

## Cross-Domain Connections

- **All Neocortex skills**: Briefing-engine is the output layer that synthesizes everything Neocortex produces
- **Neocortex/foresight/frontier-scanner**: Primary source for AI landscape section
- **Neocortex/foresight/scenario-planner**: Primary source for strategic direction and robustness assessment
- **Neocortex/architecture/skill-cartographer**: Primary source for library state section
- **Neocortex/architecture/skill-evolutionist**: Primary source for health and maturity assessment
- **Neocortex/architecture/growth-architect**: Primary source for build priorities
- **Neocortex/architecture/clarity-engine**: Briefing style should follow clarity-engine principles
- **Investing/archon**: Parallel pattern — archon is to investing what briefing-engine is to the library. Different domain, similar role.
