---
name: agentic-researcher
description: >
  Generate, test, and iteratively refine candidate solutions to open-ended research questions
  using an evolutionary loop with automated evaluation. Use when the question is generative
  rather than investigative — "what's the best approach to X?" rather than "is X true?" — and
  when candidates can be evaluated against definable criteria. Produces ranked recommendations
  with confidence-tagged reasoning and explicit trade-off maps.
metadata:
  author: nirav
  version: "1.0"
  inspired_by: "AlphaEvolve (DeepMind, 2025) — evolutionary coding agent with automated evaluators"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash WebSearch WebFetch
---

# Agentic Researcher — The Evolver

Generate candidate answers to open-ended questions, evaluate them against criteria, keep the best, mutate, and iterate. Where the spelunker's other tools verify claims (is X true?), this skill creates and refines solutions (what's the best X?).

Inspired by the generate → evaluate → select → mutate loop that AlphaEvolve uses for algorithm discovery, adapted for general research questions where multiple valid answers exist.

## When to Use (vs. Standard Spelunker Pipeline)

| Question Shape | Route To |
|---------------|----------|
| "Is X true?" / "What caused X?" | claim-decomposer → source-triangulator |
| "What's the best approach to X?" / "How should we design X?" | **agentic-researcher** |
| "What are the options for X?" / "Optimize X" | **agentic-researcher** |

**Key signal:** If the answer must be *constructed* rather than *found*, use this skill.

## Guiding Principles

1. **Never present one option as if it's the only option.** Show the landscape.
2. **Every recommendation needs a trade-off map.** "Best" is relative to criteria.
3. **Evaluate before you advocate.** Generate candidates first, then evaluate. Don't start with a conclusion.
4. **Use the confidence framework.** Recommendations carry confidence tags per `../spelunker/references/confidence-framework.md`.
5. **Iterate only when it improves signal.** Stop when additional rounds produce marginal gains.

## How to Run

### Input

From the spelunker orchestrator:
- The generative question (restated)
- The detected domain
- Depth mode (quick / standard / deep)
- User constraints (budget, timeline, technology, values)

### Phase 1 — Frame the Solution Space

Define what "good" means before generating candidates:

1. **Extract evaluation criteria** from the question and constraints. Every generative question implies criteria even if unstated.
2. **Weight the criteria.** Hard requirements (must-have, pass/fail) vs. soft preferences (weighted).
3. **Define the evaluation method** per criterion: measurable (numeric), comparable (ordinal), or judgmental (reasoned assessment).
4. **Map the candidate space** dimensions to ensure diversity in Phase 2.

See `references/evaluation-methods.md` for scoring scales, weighting defaults, and trade-off visualization formats.

### Phase 2 — Generate Initial Candidates

Create 3-5 diverse candidates spanning the solution space. Use generation strategies: established options, analogical transfer, constraint inversion, extreme positions, and hybrids. See `references/evaluation-methods.md` for strategy details.

For each candidate, produce:
- A clear description (1-3 sentences)
- Which solution space dimensions it occupies
- Hypothesized strengths and weaknesses
- What evidence would confirm or undermine it

**Research grounding:** Quick-search each candidate to verify it's real. Use source-triangulator at `quick` depth if needed. Flag or replace candidates based on nonexistent technology or debunked approaches.

### Phase 3 — Evaluate Candidates

Score each candidate against the rubric from Phase 1:

1. **Evidence gathering** — For each candidate × criterion, search for evidence using source-triangulator standards. Tag evidence quality: Strong / Weak / None.
2. **Scoring** — Measurable (data + citation), comparable (relative rank + evidence), judgmental (reasoned + flagged as judgment).
3. **Build the evaluation matrix** — candidates as rows, weighted criteria as columns.
4. **Identify trade-offs** — Where does each candidate excel vs. sacrifice?

### Phase 4 — Select and Mutate (Evolutionary Loop)

**Skip in `quick` mode.** Quick mode stops after Phase 3.

1. **Select** top 2-3 candidates.
2. **Mutate** — Generate 1-2 variants per selected candidate: repair weaknesses, import strengths from others, tighten constraints. See `references/evaluation-methods.md` for mutation operators and convergence detection.
3. **Re-evaluate** mutated candidates with the same rubric.
4. **Convergence check** — Stop when scores stabilize or iteration budget exhausted.

| Mode | Initial Candidates | Iterations | Max Evaluated |
|------|-------------------|------------|---------------|
| quick | 3 | 0 | 3 |
| standard | 4 | 1 | 8 |
| deep | 5 | 2-3 | 15 |

### Phase 5 — Synthesize Recommendation

1. **Ranked recommendation** with confidence tag and reasoning.
2. **Trade-off map** — what the user gains and sacrifices with each viable option.
3. **Sensitivity analysis** — would shifting criteria weights change the recommendation?
4. **Evidence quality assessment** — gaps that could change the ranking.
5. **Next steps** — what to validate before committing.

### Output Format

```
AGENTIC RESEARCH BRIEF
══════════════════════
Question: [restated question]
Mode: [quick / standard / deep] | Iterations: [N]

RECOMMENDATION
──────────────
[Top candidate] — Confidence: [tag]
[2-3 sentence summary]

TRADE-OFF MAP
─────────────
[Candidate 1]: Best at [X], sacrifices [Y]
[Candidate 2]: Best at [Z], sacrifices [W]

EVALUATION MATRIX
─────────────────
[Weighted scoring matrix]

SENSITIVITY
───────────
[Decisive criteria; what would flip the recommendation]

EVIDENCE QUALITY
────────────────
[Confidence tags per candidate; evidence gaps that could change ranking]

NEXT STEPS
──────────
[What to verify before committing]
```

## Error Handling

| Failure | Response |
|---------|----------|
| Can't define evaluation criteria | Ask user: "What does 'good' mean here? What are you optimizing for?" |
| All candidates score equally | Criteria aren't discriminating. Suggest more specific criteria. |
| No evidence for any candidate | Tag entire brief as Speculative. Note what would help. |
| User constraints are contradictory | Surface the contradiction. Ask which constraint to relax. |
| Solution space too large | Ask user to constrain scope. Suggest 2-3 scoping options. |
| Single candidate dominates | Adversarial check: search for "[candidate] problems". Flag lack of trade-offs as suspicious if it survives. |

## Cross-Domain Connections

- **Spelunker orchestrator** — Routes generative questions here; returns structured brief.
- **Confidence framework** — Shared with all spelunker children via `../spelunker/references/confidence-framework.md`.
- **Source-triangulator** — Called during Phase 2 (grounding) and Phase 3 (evidence) at reduced depth.
- **Game theory / mechanism-design** — Evaluation matrices share structure with payoff matrices.
- **Data science / statistical-analysis** — Sensitivity analysis parallels parameter sensitivity testing.
