# Visual Vocabulary — Reusable Concept Shapes

A library of structural metaphors for explaining technical concepts. Each shape maps to a category of concept. When explaining something new, find the shape first — then dress it in the specifics.

## The Core Shapes

### 1. The Funnel
**Structure**: Wide input → progressive narrowing → focused output
**Use for**: Filtering processes, search, attention, classification
**Examples**:
- How search engines work (billions of pages → indexed → ranked → top 10)
- How attention mechanisms work (all tokens → relevance scoring → focused subset)
- How decision trees split data (full dataset → branch → branch → leaf)

```
    ████████████████
     ██████████████
      ████████████
       ██████████
        ████████
         ██████
          ████
           ██
```

### 2. The Layer Cake
**Structure**: Stacked levels where each builds on the one below
**Use for**: Abstraction hierarchies, neural network architectures, protocol stacks
**Examples**:
- How deep learning works (pixels → edges → shapes → objects → scenes)
- How language models process text (characters → tokens → embeddings → meaning)
- How web technology stacks (hardware → OS → server → application → UI)

```
  ┌─────────────────────────┐  High-level (abstract)
  ├─────────────────────────┤
  ├─────────────────────────┤
  ├─────────────────────────┤
  └─────────────────────────┘  Low-level (concrete)
```

### 3. The Feedback Loop
**Structure**: Output feeds back as input, creating self-reinforcing cycles
**Use for**: Reinforcement learning, market reflexivity, iterative improvement, compounding
**Examples**:
- How RLHF works (generate → rate → adjust → generate better)
- How market bubbles form (price rises → attracts buyers → price rises more)
- How skills compound (practice → improvement → harder challenges → more practice)

```
  ──────► Process ──────►
  ▲                      │
  │       Feedback       │
  └──────────────────────┘
```

### 4. The Map/Territory
**Structure**: A simplified representation of something complex; the map is not the territory
**Use for**: Models, embeddings, abstractions, representations, simulations
**Examples**:
- What embeddings are (words placed on a map where proximity = similarity)
- What a trained model is (a compressed, approximate map of patterns in data)
- What a simulation is (a simplified map of a complex system)

### 5. The Dial (Spectrum)
**Structure**: A continuous range between two extremes
**Use for**: Trade-offs, hyperparameters, bias-variance, precision-recall
**Examples**:
- Bias-variance trade-off (underfitting ←——→ overfitting)
- Precision-recall trade-off (miss nothing ←——→ no false alarms)
- Exploration-exploitation trade-off (try new things ←——→ use what works)

```
  Conservative ◄━━━━━━━━━━━●━━━━━━━━━━━► Aggressive
                        current
```

### 6. The Fork in the Road
**Structure**: A decision point where different paths lead to different outcomes
**Use for**: Decision trees, conditional logic, branching strategies, if/then
**Examples**:
- How classification works (is it X? → yes path / no path)
- How routing in orchestrators works (what type of question? → different specialist)
- How A/B testing works (randomly assign → path A or path B → compare outcomes)

```
              ┌──── Path A ────► Outcome 1
  ── Decision ┤
              └──── Path B ────► Outcome 2
```

### 7. The Sieve (Progressive Filtering)
**Structure**: Multiple filters in sequence, each removing different things
**Use for**: Data pipelines, validation chains, multi-stage processing
**Examples**:
- How data cleaning works (remove nulls → fix types → handle outliers → validate)
- How immune systems work (skin → inflammation → antibodies → memory cells)
- How code review works (linting → tests → peer review → merge checks)

### 8. The Constellation
**Structure**: Points in space with meaningful connections between some of them
**Use for**: Knowledge graphs, skill networks, concept relationships, social networks
**Examples**:
- How the skill library is structured (skills as stars, edges as connections)
- How knowledge graphs work (entities as nodes, relationships as edges)
- How neural network weights form meaningful clusters

### 9. The Ratchet
**Structure**: Forward progress that can't slide backward
**Use for**: Checkpoints, irreversible processes, one-way functions, progressive commitment
**Examples**:
- How training checkpoints work (save progress, can always resume from last good state)
- How hashing works (easy to compute forward, impossible to reverse)
- How skill building works (each skill learned makes the next one easier)

### 10. The Lens
**Structure**: Same input, different view depending on which lens you use
**Use for**: Multi-framework analysis, perspectives, feature extraction, different metrics on same data
**Examples**:
- How ethics analysis works (same situation viewed through utilitarian, deontological, virtue lenses)
- How feature engineering works (same data → different features depending on what you're looking for)
- How the same market event looks different to a value investor vs. a momentum trader

## Combining Shapes

Complex concepts often combine 2-3 shapes:

| Concept | Shapes Combined | Description |
|---------|----------------|-------------|
| Training a neural network | Layer cake + feedback loop | Layered architecture that improves through repeated feedback |
| RAG (retrieval-augmented generation) | Funnel + layer cake | Filter relevant documents (funnel), then process through model layers (cake) |
| Multi-agent systems | Constellation + feedback loop | Connected agents (constellation) that influence each other (feedback) |
| Skill library growth | Ratchet + constellation | Each new skill (ratchet) adds a node and edges (constellation) |

## Quick Reference: Concept → Shape

| When the concept involves... | Reach for... |
|-----------------------------|-------------|
| Narrowing, selecting, focusing | Funnel |
| Hierarchy, levels, abstraction | Layer cake |
| Self-reinforcement, iteration, cycles | Feedback loop |
| Representation, approximation, compression | Map/territory |
| Trade-offs, continua, tuning | Dial |
| Choices, branching, conditions | Fork |
| Sequential processing, cleaning | Sieve |
| Relationships, networks, connections | Constellation |
| One-way progress, checkpoints | Ratchet |
| Multiple perspectives on same thing | Lens |
