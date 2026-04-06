# Clarity Engine — Quick Reference


## Quick Reference

| Technical Concept | Analogy | Shared Structure |
|------------------|---------|-----------------|
| Attention mechanism in transformers | A spotlight that the model can aim at different parts of the input | Both select what to focus on from a large field; intensity varies |
| Overfitting | Memorizing the answers to a practice test instead of learning the subject | Both produce great performance on known data and terrible performance on new data |
| Embeddings | A map where similar cities are placed near each other | Both encode meaning as position in space; distance = relatedness |
| Loss function | A score in a game where lower is better | Both measure "how wrong are you" and guide improvement |
| Tokenization | Chopping a sentence into LEGO bricks before building with them | Both decompose complex wholes into standard reusable units |

## Quick Reference

| Concept | Before | After | Why It Matters |
|---------|--------|-------|---------------|
| Attention | Models read left-to-right, forgetting early words | Models see all words simultaneously | Long-range relationships finally work |
| Fine-tuning | One model for everything, mediocre at all | General model + targeted training = specialist | Good enough became great at specific tasks |
| RLHF | Models generated technically correct but unhelpful text | Models learned what humans actually find useful | The "it's technically right but useless" problem got solved |

## Formula / Pseudocode

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

## Formula / Pseudocode

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

## Formula / Pseudocode

```
What people think: [Common wrong mental model]
What's actually happening: [Corrected mental model]
Why the confusion: [What makes the wrong model feel right]
The key difference: [One sentence that separates right from wrong]
```

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
