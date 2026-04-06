---
name: dialectical-tools
description: >
  Direct the dialectical methods subdomain — route meta-methodological requests to Socratic
  questioning, steel-manning, thought experiments, or structured dialectic. Use when the user
  wants to challenge reasoning, stress-test a position, play devil's advocate, think through
  a problem more carefully, or run a structured debate.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Dialectical Tools Director

The department head for meta-methods of philosophical inquiry. These skills don't analyze content directly — they provide *procedures for thinking* that can be applied to any subject matter.

Dialectical tools are unique in the library: they are designed to operate as **companions** to other skills. After any primary analysis (ethical, logical, epistemic), dialectical tools can interrogate the output. They are the quality assurance layer for reasoning itself.

## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| socratic-examiner | `socratic-examiner/SKILL.md` | Action | Systematic questioning to surface assumptions, contradictions, and deeper understanding |
| steel-man-forge | `steel-man-forge/SKILL.md` | Action | Construct the strongest possible version of an opposing argument |
| thought-experiment-lab | `thought-experiment-lab/SKILL.md` | Action | Construct, analyze, and vary thought experiments to test intuitions |
| dialectic-engine | `dialectic-engine/SKILL.md` | Action | Run structured thesis/antithesis/synthesis dialogues |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Challenge this", "What's wrong with my thinking?", "Push back on this" | socratic-examiner | Questioning reveals weaknesses from within |
| "Play devil's advocate", "What would the other side say?", "Argue against this" | steel-man-forge | Builds the strongest opposing case |
| "What if...", "Imagine a world where...", "Suppose X were true" | thought-experiment-lab | Structured hypothetical reasoning |
| "Debate both sides", "Give me thesis and antithesis", "Help me see all angles" | dialectic-engine | Multi-perspective structured dialogue |
| "Help me think through this", "I'm stuck on this problem" (unspecified method) | Assess and recommend — see below | Match method to the thinking block |

### Method Selection for Unspecified Requests

When the user says "help me think" without specifying a method, assess what kind of block they're experiencing:

| Block Type | Signal | Recommended Method |
|-----------|--------|-------------------|
| **Stuck on assumptions** | "I keep going in circles", "something feels off" | socratic-examiner — questioning will surface the hidden constraint |
| **Can't see the other side** | "I know I'm biased", "what am I missing?" | steel-man-forge — building the opposition reveals blind spots |
| **Can't test the idea** | "I don't know if this would work", "is this principle consistent?" | thought-experiment-lab — hypotheticals test intuitions safely |
| **Overwhelmed by complexity** | "There are too many angles", "I can't organize my thoughts" | dialectic-engine — structured dialogue creates order from chaos |

### Companion Mode

When invoked as a companion to another skill's output (e.g., "challenge this ethical analysis"):

1. Receive the primary analysis output
2. Select the appropriate dialectical method based on what would most usefully stress-test the analysis
3. Apply the method to the analysis, not to the original question
4. Return the dialectical output alongside the primary analysis — let the user see both

Default companion pairings:
- Ethics analysis → steel-man-forge (build the strongest opposing moral argument)
- Logic analysis → socratic-examiner (question the premises and inferential steps)
- Epistemology analysis → socratic-examiner (question what counts as evidence and why)
- Decision analysis → thought-experiment-lab (vary the scenario to test robustness)

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Socratic questioning reveals a fatal flaw; steel-man of the original position is still strong | Present both — the flaw is real AND the position has genuine strength. The user needs to weigh them | Dialectical tools illuminate; they don't resolve |
| User wants devil's advocacy but the position is actually indefensible | Steel-man the best *partial* version — find what's right about the wrong position. Even broken arguments often contain a legitimate concern | Pure devil's advocacy serves no one; finding the grain of truth is more valuable |
| Dialectical tools undermine the primary analysis | This is working as intended. Present the challenge to the user alongside the original analysis | The whole point of dialectical tools is to stress-test — finding weakness is success, not failure |

## Scope Boundaries

**This director handles**: Meta-methods for thinking — questioning, opposition-building, hypothetical reasoning, structured multi-perspective analysis.

**Escalate to the orchestrator when**:
- The user needs substantive analysis of content, not a method for thinking about it (route to logic, ethics, epistemology, etc.)
- The user wants to evaluate evidence quality specifically (Epistemology)
- The user wants to analyze argument structure specifically (Logic)
- The dialectical process reveals a need for domain-specific knowledge beyond philosophy
