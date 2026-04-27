# Child Skill Routing

Decision tree and sequencing rules for the Scriptorium's 5 child skills.

## Decision Tree

```
User question arrives
        │
        ▼
Does the user have a specific source in hand?
        │
        ├── YES ──► source-evaluator
        │              │
        │              └─ load source-criticism for principles
        │
        └── NO
              │
              ▼
        What is the question really asking?
              │
              ├── "How do we know?" / evidence-based ──► source-criticism
              │
              ├── "How should I approach?" / cognitive-method ──► historical-thinking
              │
              ├── "Why do historians disagree?" / interpretation ──► schools-of-thought
              │
              ├── "Is this argument valid?" / claim-evaluation ──► historical-argument
              │
              └── "What caused X?" / causation ──► historical-argument (with thematic wing for content)
```

## When to Load Multiple Children

The Scriptorium teaches a *craft*, and craft is composed. Most non-trivial questions need 2+ children loaded in sequence.

### Sequence: Foundation → Method → Synthesis → Tradition

| Step | Skill | Purpose |
|---|---|---|
| 1. Foundation | historical-thinking | Establish the cognitive frame (sourcing, contextualization, corroboration, perspective-taking) |
| 2. Method | source-criticism | Evaluate the specific evidence at hand |
| 3. Synthesis | historical-argument | Build or critique the claim being made |
| 4. Tradition | schools-of-thought | Situate the argument in interpretive lineage |

Most questions need only 2–3 of these steps. A full curriculum sequence is for when the user asks "teach me to think like a historian."

## Worked Examples

### Example 1: "How do we actually know the Battle of Thermopylae happened?"

- **Question shape:** evidence-based, specific event.
- **Load:** source-criticism → historical-argument.
- **Why this order:** First establish what sources exist for Thermopylae (Herodotus, archaeological remains, later Roman writers), then assess how those sources are marshaled into the historical claim.
- **Do NOT load:** schools-of-thought (no major school dispute about whether the battle occurred); source-evaluator (user has no specific source in hand).

### Example 2: "Why do Marxist and liberal historians disagree about the Industrial Revolution?"

- **Question shape:** interpretation-contested, schools-of-thought primary.
- **Load:** schools-of-thought → historical-argument.
- **Why this order:** First explain the two traditions (their commitments, what they treat as evidence, what they ignore). Then show how each constructs a different argument from the *same* evidence about wages, life expectancy, and social mobility.
- **Add:** Defer to economic-history wing for content; the Scriptorium teaches the *meta-disagreement*.

### Example 3: "Teach me to think like a historian."

- **Question shape:** full curriculum request.
- **Load (sequenced):** historical-thinking → source-criticism → historical-argument → (later) schools-of-thought.
- **Why this order:** Cognitive scaffolding before evidentiary methods before claim-construction before interpretive sophistication.

### Example 4: "Here's a 19th-century pamphlet about temperance. What do you make of it?"

- **Question shape:** specific source in hand.
- **Load:** source-evaluator → source-criticism.
- **Why this order:** Run the structured evaluation template (date, author, audience, purpose, biases), then explain *why* each evaluation step matters by referencing source-criticism principles.

### Example 5: "What caused World War I?"

- **Question shape:** causation, with thematic content.
- **Load:** historical-argument (for the meta-question of how causation claims work) + escalate to wan-shi-tong for political-history (immediate causes), military-history (alliance system), economic-history (imperial competition), intellectual-history (nationalism).
- **Pattern:** Historiography handles *how* to make the causation argument; wan-shi-tong's thematic wings handle *what* the evidence is.

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Source says X, tradition interprets as Y | source-criticism wins | Evidence trumps tradition — but name the tradition's reasoning so the user sees the move |
| Two valid frameworks disagree | Present both, name stakes | The Scriptorium teaches the debate, not the verdict |
| General heuristic vs. content-specific knowledge | Content-specific wins for that case | General heuristics are defaults; expertise overrides when warranted |
| User wants "the answer," but the question is genuinely contested | Refuse the false certainty; teach the contestation | Method before conclusion |

## Boundary Conditions — Escalate Out

| Trigger | Route to |
|---|---|
| Question is about a specific historical event (not the methodology) | wan-shi-tong → relevant thematic wing |
| Question applies history to a present-day decision | wan-shi-tong → applied-history |
| Question requires deep regional expertise | wan-shi-tong → regional-atlas |
| Question is about epistemology in general (not historical epistemology) | philosophy-orchestrator → epistemology |
| Question is about source triangulation as a generic skill (not historical) | research/spelunker |

## Default Behavior

If a question is ambiguous and could route to either historical-thinking or source-criticism, prefer **historical-thinking** — it's the foundation, and starting there avoids skipping the cognitive scaffolding.

If a question is ambiguous and could route to historical-argument or schools-of-thought, prefer **historical-argument** — it's the synthesis layer, and traditions become useful only after the user can evaluate a claim on its own terms.
