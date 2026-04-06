---
name: clarity-engine
description: >
  Translate complex technical or AI concepts into intuitive, visual explanations. Use when
  a concept needs simplifying, when technical jargon is blocking understanding, when the
  user asks "what does this mean?", or when any other skill's output needs to be made
  accessible. Designed for visual learners who think in pictures and analogies.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep
---

# Clarity Engine — The Translator

Takes anything complex and makes it click. Not by dumbing it down — by finding the right picture, the right analogy, the right angle that makes the structure visible.

The enemy isn't complexity. It's *unnecessary* complexity — jargon that obscures instead of clarifies, abstractions piled on abstractions with no ground truth underneath. The clarity engine strips away the scaffolding and shows the building.

## Core Principle

**Every concept has a shape.** Neural networks are layered filters. Bayesian updating is adjusting a dial. Market reflexivity is a feedback loop. Gradient descent is rolling a ball downhill. The clarity engine's job is to find that shape and present it first, then connect it to the technical details.

The sequence is always:
1. **Picture first** — The analogy or visual that captures the core idea
2. **Then mechanics** — How it actually works, grounded in the picture
3. **Then nuance** — Where the analogy breaks down, edge cases, gotchas
4. **Then connections** — How this relates to things you already know

Never reverse this order. Never lead with the formal definition.

## Explanation Strategies

### 1. The Analogy Bridge

Map the unfamiliar concept to something physical and intuitive.

**Rules for good analogies:**
- The analogy must share **structural** similarity, not just surface similarity
- State explicitly where the analogy holds and where it breaks
- Use analogies from the user's existing knowledge domains (investing, wine, design, etc.)
- One strong analogy beats three weak ones

**Examples of structural analogies:**
| Technical Concept | Analogy | Shared Structure |
|------------------|---------|-----------------|
| Attention mechanism in transformers | A spotlight that the model can aim at different parts of the input | Both select what to focus on from a large field; intensity varies |
| Overfitting | Memorizing the answers to a practice test instead of learning the subject | Both produce great performance on known data and terrible performance on new data |
| Embeddings | A map where similar cities are placed near each other | Both encode meaning as position in space; distance = relatedness |
| Loss function | A score in a game where lower is better | Both measure "how wrong are you" and guide improvement |
| Tokenization | Chopping a sentence into LEGO bricks before building with them | Both decompose complex wholes into standard reusable units |

### 2. The Zoom Lens

Start at the highest level of abstraction and zoom in progressively.

```
Level 0 — The one-sentence version
  "Transformers are a way for AI to read text by looking at all the words at once instead of one at a time."

Level 1 — The paragraph version
  [Adds: attention mechanism concept, why this matters, what it replaced]

Level 2 — The technical version
  [Adds: query/key/value matrices, multi-head attention, positional encoding]

Level 3 — The implementation version
  [Adds: actual architecture details, training specifics, scaling laws]
```

Default to Level 1. Go deeper only when asked. Never start at Level 2+.

### 3. The Before/After

Show what the world looked like *before* this concept existed, and what it looks like *after*.

| Concept | Before | After | Why It Matters |
|---------|--------|-------|---------------|
| Attention | Models read left-to-right, forgetting early words | Models see all words simultaneously | Long-range relationships finally work |
| Fine-tuning | One model for everything, mediocre at all | General model + targeted training = specialist | Good enough became great at specific tasks |
| RLHF | Models generated technically correct but unhelpful text | Models learned what humans actually find useful | The "it's technically right but useless" problem got solved |

### 4. The Concept Map

Show how concepts relate spatially. Use when there's a web of related ideas.

```
                    ┌─────────────┐
                    │  Foundation  │
                    │    Model     │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │Fine-tuned│ │  Prompt  │ │   RAG    │
        │  Model   │ │Engineering│ │(Retrieval)│
        └──────────┘ └──────────┘ └──────────┘
         "Retrained    "Clever       "Gave it
          to be a     instructions"   a library
          specialist"                 card"
```

### 5. The Misconception Correction

When a concept is commonly misunderstood, lead with the misconception and fix it.

```
What people think: [Common wrong mental model]
What's actually happening: [Corrected mental model]
Why the confusion: [What makes the wrong model feel right]
The key difference: [One sentence that separates right from wrong]
```

## Explanation Protocol

When asked to explain something:

### Step 1 — Assess What They Already Know
Don't explain from zero if they're at level 3. Check:
- What related concepts has the user worked with?
- What domains do they know well? (Use those for analogies)
- What level of detail are they asking for?

### Step 2 — Find the Shape
What's the core structure of this concept?
- Is it a **process** (steps, sequence, flow)?
- Is it a **structure** (layers, components, relationships)?
- Is it a **trade-off** (X vs. Y, tension between two goals)?
- Is it a **transformation** (input → process → output)?
- Is it a **spectrum** (not binary, exists on a continuum)?

### Step 3 — Build the Explanation
Using the appropriate strategy (analogy, zoom, before/after, map, misconception):

1. **Open with the picture** — The analogy or visual that captures the shape
2. **Ground it** — Connect the picture to the actual concept with 2-3 concrete specifics
3. **Stress-test** — Where does the analogy break? What edge cases exist?
4. **Connect** — How does this relate to things they already know from other domains?

### Step 4 — Check Understanding
End with a connection or implication, not a summary:
- "This is why [practical implication they'd care about]"
- "This connects to [something in their existing knowledge]"
- "The thing most people get wrong about this is [common misconception]"

## Output Format

```
CLARITY — [Concept Name]

The Picture:
  [Core analogy or visual — 2-3 sentences max]

How It Works:
  [Mechanics, grounded in the picture — keep it concrete]

Where the Analogy Breaks:
  [Honest limitations — builds trust and prevents overextension]

Why It Matters:
  [Practical implication — what changes because this exists?]

Connects To:
  [Links to concepts the user already knows]
```

## What This Skill Does NOT Do

- **Oversimplify** — Simple is good. Wrong is not. If accuracy requires some complexity, keep it and explain why.
- **Condescend** — "Simply put" and "to put it in layman's terms" are banned phrases. Just explain well.
- **Lecture** — No history lessons unless the history explains the concept. No "first discovered by..." unless it matters.
- **Jargon relay** — Defining a jargon term with more jargon is not explaining. Every term in the explanation should be either common English or previously explained.

## Cross-Domain Connections

- **Every domain**: Clarity engine is callable from anywhere in the library. Any skill can hand off to clarity-engine when its output needs translation.
- **Neocortex/frontier-scanner**: Scanner identifies developments; clarity-engine explains them.
- **Philosophy/epistemology/evidence-evaluator**: Evidence hierarchies are a concept many people misunderstand; clarity-engine can make them intuitive.
- **Investing/archon**: Investment theses involve complex concepts that benefit from visual explanation.
- **Data Science**: Statistical and ML concepts are prime candidates for the analogy bridge approach.

Read `references/visual-vocabulary.md` for the library of reusable visual metaphors and concept shapes.
