---
name: intellectual-history
description: >
  Route questions about the history of ideas, scientific revolutions, political thought, and
  knowledge systems. Activate when users ask how ideas emerged, spread, and transformed
  societies, from the Axial Age through the Scientific Revolution, the Enlightenment, and
  the digital age, or when examining how knowledge is produced and contested.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Intellectual History — The Hall of Minds

The Hall of Minds traces the history of *ideas* — not just what people did, but what they *thought*, why they thought it, and how those thoughts changed the world. Intellectual history is not philosophy (which evaluates whether ideas are true) but the study of how ideas emerge from specific historical contexts, spread across networks, and produce consequences their originators never imagined.

This wing is the strongest bridge between Wan Shi Tong and the philosophy domain. Intellectual history provides the *historical context* for ideas that philosophy evaluates *analytically*.

## Child Skills

| Skill | Type | Handles |
|---|---|---|
| `scientific-revolutions` | knowledge | Kuhn's paradigm shifts; how scientific knowledge changes through upheavals |
| `political-thought` | knowledge | The great conversation from Plato through Rawls; genealogy of political concepts |
| `knowledge-systems` | knowledge | How civilizations organize, preserve, and transmit knowledge; infrastructure of knowing |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| Science, discovery, paradigm, scientific method, Copernicus, Darwin, Einstein | `scientific-revolutions` | Questions about how scientific knowledge changes |
| Political philosophy, liberty, equality, sovereignty, rights, justice, Plato, Marx, Locke | `political-thought` | Questions about political ideas and their history |
| Library, university, writing, printing press, oral tradition, knowledge, education, curriculum | `knowledge-systems` | Questions about knowledge infrastructure |
| "How did people think about X in the past," "history of the idea of" | Context-dependent routing | Use the specific idea to determine which child skill |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "How did the Enlightenment change the world?" | knowledge-systems → political-thought → scientific-revolutions | Start with the infrastructure (salons, print), then the ideas (liberty, reason), then the scientific dimension |
| "How did Darwin's ideas affect politics?" | scientific-revolutions → political-thought | Scientific idea first, then its political appropriation (Social Darwinism) |
| "Why was the printing press so important?" | knowledge-systems → (escalate to wan-shi-tong for multi-wing routing) | The printing press affected everything — intellectual history leads but economic, cultural, and political dimensions are needed |

## Curriculum Order

1. **`knowledge-systems`** (foundation) — How knowledge is produced and transmitted; the infrastructure that makes intellectual history possible
2. **`scientific-revolutions`** (paradigm) — How the most powerful form of knowledge changes
3. **`political-thought`** (application) — How ideas about human organization evolve; the most politically consequential branch of intellectual history

### Level Progression
- **Foundational**: knowledge-systems
- **Intermediate**: scientific-revolutions
- **Advanced**: political-thought

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| "Great thinker" vs. social/material explanation of ideas | Present both; lean toward contextualism | Ideas don't emerge in vacuums — but individual genius does sometimes produce genuine novelty |
| Internal (philosophical) vs. external (historical) reading of a text | Intellectual history favors external reading | Philosophy evaluates truth; intellectual history explains why this truth emerged here and now |
| Western vs. non-Western intellectual traditions | Present both; flag when one dominates | The Hall of Minds covers all civilizations, not just the Western canon |

**General rule**: Ideas have histories. Always ask: *Who thought this? When? Why then? What were the alternatives?* An idea stripped of its context is philosophy, not intellectual history.

## Scope Boundaries

**This director handles**: All questions about how ideas emerge, spread, and transform societies.

**Escalate to wan-shi-tong when**:
- The question is about evaluating ideas philosophically rather than historically (route to philosophy-orchestrator)
- The question is about political *events* driven by ideas (route to political-history)
- The question is about technological *applications* of scientific knowledge (route to world-systems)
