---
name: polya-method
description: >
  Reference Polya's How to Solve It heuristic catalog and four-step problem-solving method
  (understand / plan / execute / look back). Use when binding-vow's reframing or decomposition
  skills need to apply restatement, relation-finding, reduction, working-backwards,
  decomposition, analogy, or verification heuristics. Foundational reference for
  problem-statement work.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Polya Method — How to Solve It

George Pólya's *How to Solve It* (1945) is the spine of problem-statement work. The four-step method tells you *when* you are; the heuristic dictionary (~67 entries) tells you *what to try*. Pólya's most important contribution was insisting that Step 1 (Understand the problem) is not trivial — it is where most failures originate.

## The Four Steps

1. **Understand the problem.** What is the unknown? What are the data? What is the condition? Restate in your own words. Draw a figure. Introduce suitable notation. Most problems are misstated until Step 1 is taken seriously.
2. **Devise a plan.** Find the connection between the data and the unknown. Search for a related problem with the same unknown. This is the creative step — heuristics live here.
3. **Carry out the plan.** Execute, checking each step.
4. **Look back.** Examine the result. Can you check it? Can you derive it differently? Can you use the result, or the method, on another problem?

## The Seven Heuristic Families

The dictionary collapses into seven families. Pick the family by where you're stuck.

| Family | Example heuristics | When to invoke |
|---|---|---|
| **Restatement** | Have you stated it correctly? Express in different words. Define the terms. | Step 1 — before any solving work |
| **Relation-finding** | Have you seen the same problem in a different form? Is there a related problem with the same unknown? | Step 2 — when no plan suggests itself |
| **Reduction** | Solve a simpler / more general / related problem first. Specialize the problem. Generalize the problem. | Step 2 — when the problem is too hard as stated |
| **Working backwards** | Start from the desired conclusion. Ask what would suffice. Trace backwards to the data. | Search problems, proof problems, design problems |
| **Decomposition** | Break the problem into sub-problems. Vary the problem. Drop conditions; add them back. | Step 2 — for compound or multi-step problems |
| **Analogy** | Find an auxiliary problem you've solved before with similar structure. | Cross-domain or transfer cases |
| **Verification** | Can you check the result? Can you check the argument? Use it for another problem? | Step 4 — never skip |

## Diagnostic Cues

| Symptom | Family to try |
|---|---|
| "I don't understand what's being asked" | Restatement |
| "I have no idea where to start" | Relation-finding, then Analogy |
| "This problem is too big" | Decomposition or Reduction (specialize) |
| "I can't find a path forward" | Working backwards |
| "I have an answer but I'm not sure it's right" | Verification |
| "I solved one case but the general result eludes me" | Reduction (generalize) |

## How binding-vow uses Polya

Polya's Step 1 maps directly onto `six-eyes`'s Phase 1 (Intake) — the "restate the dump in precise terms" instruction is Polya's "Understand the problem" verbatim. The heuristic families in the table above are the operations `frame-rotator` (Phase 4) executes:

- Restatement → trivial in Phase 1; deep in `frame-rotator`
- Reduction (specialize / generalize) → `frame-rotator`'s level-shifting moves (folded in per v2)
- Working backwards → reframing technique when forward-chaining fails
- Decomposition → calls `claim-decomposer` (cross-domain — research)
- Analogy → suggested by `frame-rotator`; can call `domain-translator` (neocortex) for cross-domain analogies
- Verification → Phase 6 audit (every audit skill is a flavor of Polya verification)

The dictionary itself (the ~67 numbered entries in *How to Solve It*) is reference material; future skills should cite it by entry rather than re-implementing.

## Common Mistakes

- Skipping Step 1 because "I obviously understand the problem" — Reiter-Palmon's automaticity finding shows you usually don't.
- Treating heuristics as solutions — they generate candidate plans, not answers.
- Stopping at Step 3. Step 4 (look back) is where transfer happens; without it, every new problem starts from scratch.
- Confusing Reduction with Decomposition. Reduction simplifies (one easier problem); Decomposition splits (several simpler problems).
- Treating Analogy as proof. An analogous problem suggests an approach; it does not guarantee the approach works.

## Connections

- `six-eyes` — Phase 1 maps onto Polya Step 1; Phase 4 implements heuristic families
- `frame-rotator` (binding-vow) — uses Restatement, Reduction, Working Backwards
- `claim-decomposer` (research) — implements Decomposition family
- `domain-translator` (neocortex) — implements Analogy family across domains
- Vault note: `skill-lab/polya-heuristics-catalog.md`

## Sources

- Pólya, G. (1945). *How to Solve It: A New Aspect of Mathematical Method*. Princeton University Press / John Wiley & Sons.
- Pólya, G. (1954). *Mathematics and Plausible Reasoning* (vol. I & II). Princeton University Press.
- Schoenfeld, A. H. (1985). *Mathematical Problem Solving*. Academic Press. (Expansion of Pólya's framework with empirical testing.)
