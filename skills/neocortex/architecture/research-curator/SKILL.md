---
name: research-curator
description: >
  Build and maintain living research collections on topics relevant to the skill library.
  Use when building a curated knowledge base on a subject, gathering authoritative sources
  for a domain, creating reading lists, or when the same topic keeps requiring fresh
  research across multiple conversations.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep WebSearch WebFetch
---

# Research Curator — The Archivist

Builds living collections of curated research on topics that matter to the skill library. Not a one-off investigator (that's spelunker) — a long-term collector who maintains organized, up-to-date reference shelves that anyone in the library can draw from.

The difference between a researcher and a curator: a researcher answers a specific question once. A curator builds a collection that answers a class of questions repeatedly. Spelunker investigates; the archivist catalogs.

## Core Function

Create and maintain curated research collections organized by topic, assessed for quality, and designed for reuse. Every collection answers:

1. **What are the authoritative sources?** — Not comprehensive, but vetted
2. **What's the consensus?** — Where do sources agree
3. **What's contested?** — Where they disagree and why
4. **What's the frontier?** — The newest, least-settled findings
5. **When was this last updated?** — Currency matters; stale research is dangerous

## Collection Types

### Domain Primer
A curated introduction to a field the skill library is entering or expanding.

**Use when**: Building a new domain and need foundational research before writing skills.

| Component | Purpose |
|-----------|---------|
| **Canonical texts** | The 3-5 works everyone in the field knows |
| **Key concepts** | The vocabulary and mental models that define the field |
| **Active debates** | Where practitioners disagree — reveals the field's live edges |
| **Adjacent fields** | What neighboring domains connect to this one |

### Topic Deep-Shelf
An ongoing collection on a specific topic (e.g., "AI alignment research", "behavioral economics critiques").

**Use when**: A topic keeps coming up across conversations and the same research keeps being re-done.

| Component | Purpose |
|-----------|---------|
| **Source registry** | Annotated list of sources with quality assessments |
| **Finding summary** | Key findings organized by theme, not by source |
| **Contradictions log** | Where sources disagree, with the strongest argument on each side |
| **Currency marker** | When each finding was last verified |

### Reading List
A focused, prioritized list of sources for the user to engage with.

**Use when**: The user wants to learn about a topic and needs guidance on what to read and in what order.

| Component | Purpose |
|-----------|---------|
| **Sequence** | Ordered from foundational to advanced |
| **Time estimates** | How long each source takes to engage with |
| **Key takeaway** | What each source uniquely contributes |
| **Skip conditions** | "Skip this if you already understand X" |

## Curation Process

### Step 1 — Scope the Collection
Define what's in and out. A collection on "machine learning" is too broad; "transformer architecture evolution 2017-2026" is focused enough to curate well.

| Scoping Question | Purpose |
|-----------------|---------|
| What question does this collection answer? | Defines the core purpose |
| Who will use it? | Determines depth and assumed knowledge |
| What's the time horizon? | Determines how far back to look |
| What quality bar applies? | Peer-reviewed only? Industry reports? Blog posts? |

### Step 2 — Gather Sources
Cast a wide net, then filter aggressively.

| Source Type | When to Include | Quality Check |
|------------|----------------|---------------|
| Academic papers | When rigor matters | Peer-reviewed, cited by others |
| Books / textbooks | For foundational understanding | Standard references in the field |
| Industry reports | For current practice | Source credibility, methodology transparency |
| Technical blogs | For cutting-edge developments | Author credibility, reproducibility |
| Primary data | When claims need verification | Methodology, sample size, recency |

### Step 3 — Assess and Annotate
For each source:

| Assessment | What to Record |
|-----------|---------------|
| **Reliability** | How trustworthy is this source? (high/medium/low) |
| **Relevance** | How directly does it address the collection's question? |
| **Recency** | When was it published? Is it still current? |
| **Unique contribution** | What does this source add that others don't? |
| **Limitations** | Known biases, gaps, or methodological issues |

### Step 4 — Synthesize
Organize findings by theme, not by source. The collection should be more useful than the sum of its parts.

### Step 5 — Maintain
Set a review cadence. Research goes stale.

| Collection Type | Review Cadence | Trigger for Update |
|----------------|---------------|-------------------|
| Domain Primer | Every 6 months | New domain build planned |
| Topic Deep-Shelf | Every 3 months | New major publication in the area |
| Reading List | Every 3 months | User completes the list and wants next steps |

## Output Format

```
RESEARCH COLLECTION — [Topic]
Type: [Domain Primer / Topic Deep-Shelf / Reading List]
Last Updated: [Date]
Currency Status: [current / aging / stale]

Scope:
  Question: [What this collection answers]
  Time Horizon: [period covered]
  Quality Bar: [source types included]

Sources: [N total, M high-reliability]

Key Findings:
  1. [Theme]: [synthesis across sources]
  2. [Theme]: [synthesis across sources]

Active Debates:
  - [Debate]: [Side A] vs. [Side B] — [current evidence leans toward...]

Frontier (newest/least-settled):
  - [Finding]: [source, date, confidence]

Recommended Reading Order:
  1. [Source] — [why first, time estimate]
  2. [Source] — [builds on #1, time estimate]
  ...
```

## What This Skill Does NOT Do

- **Investigate** — One-off research questions go to spelunker. The curator builds lasting collections, not answers.
- **Evaluate evidence philosophically** — Evidence quality assessment at the philosophical level is epistemology/evidence-evaluator. The curator applies practical quality checks (peer review, methodology, recency).
- **Store the sources themselves** — The curator creates organized references and syntheses, not a document repository.

## Cross-Domain Connections

- **Research/spelunker**: Spelunker does deep-dive investigations; curator catalogs findings for long-term reuse
- **Research/evidence-synthesizer**: Synthesizer assembles evidence for a specific claim; curator maintains broad topic collections
- **Research/source-triangulator**: Triangulator verifies individual sources; curator uses triangulation as part of quality assessment
- **Neocortex/foresight/frontier-scanner**: Scanner identifies developments; curator builds lasting reference collections on the topics scanner surfaces
- **Neocortex/architecture/growth-architect**: Domain primers directly support new domain planning
- **Philosophy/epistemology/evidence-evaluator**: Epistemological evidence assessment provides the philosophical foundation for the curator's practical quality checks
