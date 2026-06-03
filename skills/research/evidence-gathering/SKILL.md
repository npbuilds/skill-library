---
name: evidence-gathering
description: >
  Route a research question to the evidence-acquisition skills — claim decomposition, source
  triangulation, funding/COI tracing, paywall strategy, and the generative agentic-researcher.
  Activate during spelunker Phases 2–3 (Decompose → Investigate) when a question needs to be
  broken into claims and each claim backed by independent sources. This director owns the
  "find and qualify the evidence" half of the research pipeline.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Evidence Gathering — Director

Research splits cleanly into two halves: acquiring evidence and reasoning from it. This director
owns the first half — spelunker's Phases 2 and 3. It decomposes the question into atomic claims,
triangulates independent sources for each, traces who funded them, works around paywalls before
declaring anything unverifiable, and — for generative questions — hands off to the evolutionary
agentic-researcher. The output is qualified evidence bundles ready for synthesis.

## Routing Table

| Child skill | Use when | Output |
|---|---|---|
| `claim-decomposer` | The question bundles multiple assertions, hidden assumptions, or compound predictions | Atomic claims with a dependency graph and priority tiers |
| `source-triangulator` | An atomic claim needs evidence from multiple independent sources | Per-claim evidence bundle + independence verification |
| `bias-and-funding-tracer` | Source quality alone is insufficient — you need funding, COI, and cross-source independence | Sources enriched with funder/COI + independence flags |
| `paywall-strategist` | A critical claim's source is paywalled or inaccessible | Open-access mirrors / abstracts, or a `truly_unverifiable` verdict |
| `agentic-researcher` | The question is generative ("what's the best X?", "how should we design X?") | Ranked candidate solutions via an evolutionary loop |

## Routing Logic

1. `claim-decomposer` first — everything downstream operates per-claim.
2. For each claim, `source-triangulator`. Enrich every **critical** claim's bundle with
   `bias-and-funding-tracer`; if effective independence drops below the confidence tier's
   threshold, flag it for the synthesizer to down-tag.
3. If a critical claim's source is paywalled, run `paywall-strategist` *before* tagging it
   Unverifiable.
4. If the question is generative rather than investigative, route to `agentic-researcher` instead
   of the claim pipeline and present its brief in spelunker's Phase 6 format.

## Scope Boundaries

- **In scope:** decomposition, source acquisition, source qualification, paywall handling,
  generative candidate construction.
- **Out of scope:** assembling the brief, adversarial disconfirmation, format translation — all
  owned by `synthesis-verification`.
- **Hand back to `spelunker`** with the qualified evidence bundles; the orchestrator drives the
  Phase 4 synthesis.
