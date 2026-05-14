---
name: debate-simulator
description: >
  Argue both sides of contested historical questions with sourced evidence and named historians.
  Use when the user wants to understand a historical debate by hearing the strongest version
  of each position, with explicit identification of the evidence each side marshals, the
  assumptions each side makes, and where the debate currently stands in the scholarly community.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Debate Simulator — Steel-Manning Both Sides

This is an action skill that presents contested historical questions by arguing the strongest possible version of each side. It operationalizes Wan Shi Tong's Principle #5 ("teach the debate, not just the conclusion") into a structured format. The key discipline: each side must be presented at its *strongest*, not its weakest. This is steel-manning, not straw-manning.

## When This Applies

- User asks "did Rome fall or transform?"
- User asks "was colonialism a net positive or negative?"
- User asks "was the Industrial Revolution good for workers?"
- User asks about any contested historical interpretation
- User wants to understand why historians disagree

## The Debate Format

### Step 1 — Frame the Question

State the question precisely. Most "was X good or bad?" questions need to be reframed into more analytically useful forms:
- "Was the Roman Empire good?" → "Did the Roman Empire's fall represent catastrophic decline or creative transformation?"
- "Was colonialism bad?" → "To what extent did colonial institutions cause post-colonial underdevelopment?"
- "Did the New Deal work?" → "Was the New Deal's primary achievement economic recovery, institutional reform, or political realignment?"

### Step 2 — Identify the Positions

Most historical debates have 2-4 major positions. For each:
- Name the position clearly
- Name the key scholars who hold it
- Identify their methodological tradition (which school of thought?)

### Step 3 — Steel-Man Each Position

For each position, present:
- **The strongest version of the argument** (not a caricature)
- **The best evidence** (specific sources, data, examples)
- **The key assumptions** (what must be true for this argument to work?)
- **The most powerful counter-argument** it faces

### Step 4 — Assess the State of the Debate

- Where does scholarly consensus lean? (If there is one)
- Where is the debate genuinely unresolved?
- What new evidence or methods might shift the debate?

## Output Template

```
═══════════════════════════════════════════
HISTORICAL DEBATE
═══════════════════════════════════════════

QUESTION: [Precisely framed question]
STAKES: [Why this debate matters — what depends on the answer?]

─── POSITION A ───────────────────────────
Claim: [Clear thesis statement]
Champions: [Named scholars and their works]
School: [Methodological tradition]

Best evidence:
  1. [Specific evidence with source]
  2. [Specific evidence with source]
  3. [Specific evidence with source]

Key assumption: [What must be true for this to work]

─── POSITION B ───────────────────────────
Claim: [Clear thesis statement]
Champions: [Named scholars and their works]
School: [Methodological tradition]

Best evidence:
  1. [Specific evidence with source]
  2. [Specific evidence with source]
  3. [Specific evidence with source]

Key assumption: [What must be true for this to work]

─── [Optional: POSITION C] ──────────────
...

─── STATE OF THE DEBATE ──────────────────
Consensus: [Where most scholars lean, if anywhere]
Unresolved: [What remains genuinely contested]
What would change minds: [Evidence or method that could settle it]
═══════════════════════════════════════════
```

## Ground Rules

1. **Name real historians**: Don't attribute arguments to generic "some scholars say." Name names.
2. **Steel-man, don't straw-man**: Present each position at its strongest, not its most easily refuted.
3. **Distinguish evidence from interpretation**: The same evidence can support different conclusions — show how.
4. **Don't declare a winner**: The Debate Simulator presents the debate; the user (and the scholarly community) decide. If there IS a clear consensus, say so — but explain why the minority position persists.
5. **Connect to frameworks**: Note which historiographical school each position belongs to — this helps the user see that debates are often methodological, not just factual.
