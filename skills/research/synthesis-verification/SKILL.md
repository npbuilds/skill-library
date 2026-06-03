---
name: synthesis-verification
description: >
  Route qualified evidence to the synthesis-and-verification skills — confidence-tagged brief
  assembly, active counterfactual disconfirmation, and format translation. Activate during
  spelunker Phases 4–6 (Synthesize → Self-Check → Present) once evidence bundles exist and need
  to become an honest, gap-aware brief. This director owns the "reason from the evidence and
  stress-test the conclusion" half of the research pipeline.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Synthesis & Verification — Director

The second half of the research pipeline — spelunker's Phases 4 through 6. Once
`evidence-gathering` has produced qualified bundles, this director assembles them into a
confidence-tagged brief, then actively tries to break the conclusion before it ships, and
finally translates the brief into whatever format the user needs. Its governing principle is
spelunker's: never present speculation as fact, and name every gap.

## Routing Table

| Child skill | Use when | Output |
|---|---|---|
| `evidence-synthesizer` | Atomic claims have evidence bundles ready to assemble | Structured brief: confidence-tagged findings, evidence map, explicit gaps |
| `counterfactual-prober` | A synthesized brief needs active disconfirmation before delivery | "If the conclusion were false, what would we see?" predictions + searches |
| `synthesis-translator` | The brief must become an exec memo, VC pitch, tweet thread, or decision memo | Reformatted brief with citations and confidence tags preserved |

## Routing Logic

1. `evidence-synthesizer` assembles the brief and runs its Step 5b citation audit. Honor any
   down-tag flags raised by `bias-and-funding-tracer` upstream.
2. Outside `quick` mode, run `counterfactual-prober` *after* the passive adversarial search and
   *before* finalizing tags — disconfirmation can demote a finding.
3. Only when the user requests a non-default format, route the completed brief to
   `synthesis-translator`. It refuses to upgrade confidence tags during compression and surfaces
   what was cut.

## Scope Boundaries

- **In scope:** brief assembly, confidence tagging, counterfactual disconfirmation, format
  translation.
- **Out of scope:** gathering or qualifying evidence (→ `evidence-gathering`).
- **Hand back to `spelunker`** for the Phase 6 pre-flight (CORE-line and citation checks) before
  the brief is delivered.
