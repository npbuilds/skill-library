---
name: experience-weaver
description: >
  Design the experience layer — how surfaced capabilities feel in use. The emotional and
  aesthetic quality of interacting with intelligence. Creates experience briefs that get
  handed to design and writing domains for execution. Use when capabilities are being
  surfaced and need an experience design, not just a function.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Experience Weaver — How Intelligence Feels

A capability without experience design is a raw function. Experience weaving adds the emotional, aesthetic, and narrative layer that transforms "the system can do X" into "interacting with this intelligence feels like Y."

This skill doesn't design interfaces — that's the design domain's job. It designs the **experience intent** that interfaces should embody.

## The Experience Dimensions

### 1. Emotional Tone

What emotion should the interaction evoke?

| Tone | When | Anti-Tone |
|---|---|---|
| **Confidence** | High-stakes decisions, expert advice | Not arrogance — confidence with humility about uncertainty |
| **Curiosity** | Exploration, discovery, research | Not confusion — guided curiosity, not lost-in-the-woods |
| **Calm** | Monitoring, ambient intelligence, background processing | Not boring — calm presence, not absence |
| **Delight** | Creative work, unexpected capability reveals | Not gimmicky — genuine surprise, not party tricks |
| **Urgency** | Alerts, time-sensitive opportunities, warnings | Not anxiety — actionable urgency, not fear |

### 2. Pacing

How does the interaction unfold over time?

| Pace | Character | When |
|---|---|---|
| **Immediate** | Instant response, zero wait | Simple lookups, status checks, reactive surfaces |
| **Considered** | Brief pause, then thoughtful response | Analysis, synthesis, anything where thinking time signals quality |
| **Unfolding** | Progressive revelation over time | Complex analysis, storytelling, investigation |
| **Ambient** | Continuous low-level presence, occasional surfacing | Monitoring, background intelligence |

### 3. Depth Calibration

How deep should interactions go by default?

| Level | Character | Default When |
|---|---|---|
| **Headline** | One sentence. The answer. | First interaction, mobile, high-confidence questions |
| **Brief** | 2-3 key points. Enough to act on. | Most interactions. The sweet spot. |
| **Deep** | Full analysis, evidence, alternatives. | Expert mode, high-stakes, "tell me more" |
| **Exhaustive** | Everything the system knows. | Research mode, audit, deep investigation |

**Adaptive rule:** Start at Brief. Escalate to Deep when the user signals interest. Never start at Exhaustive unless explicitly asked.

### 4. Voice Character

What personality does the intelligence have in this surface?

This is defined in collaboration with `prose-orchestrator` but specified here at the experience level:

- **Authority level** — Expert? Peer? Student learning alongside you?
- **Warmth** — Clinical precision or warm guidance?
- **Initiative** — Waits to be asked or proactively offers?
- **Humor** — Never? Occasionally? Frequently?
- **Formality** — Casual? Professional? Context-adaptive?

## The Experience Brief

For each surface, produce an experience brief that gets handed to design-orchestrator and prose-orchestrator:

```markdown
# Experience Brief: {surface name}

## Emotional Tone
Primary: {emotion}
Secondary: {emotion}
Never: {emotion to avoid}

## Pacing
Default pace: {immediate/considered/unfolding/ambient}
Escalation pattern: {how pace changes with depth}

## Depth
Default level: {headline/brief/deep}
Escalation trigger: {what causes deeper engagement}

## Voice Character
Authority: {expert/peer/student}
Warmth: {scale}
Initiative: {reactive/proactive/balanced}
Formality: {casual/professional/adaptive}

## Key Moments
First interaction: {what should the user feel?}
Repeated use: {how does the experience deepen?}
Surprise moment: {when does the intelligence reveal unexpected capability?}
Failure: {how does the intelligence handle mistakes gracefully?}

## Anti-Patterns
{Specific things this experience must NEVER feel like}
```

## Cross-Domain Handoffs

- **design-orchestrator** — Receives the experience brief for visual/interaction execution. "Here's what it should feel like. You design what it looks like."
- **prose-orchestrator** — Receives voice character and tone for language execution. "Here's the personality. You craft the words."
