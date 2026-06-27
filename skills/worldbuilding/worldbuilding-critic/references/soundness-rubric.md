# Soundness Rubric — invented systems

The Layer-2 rubric for `worldbuilding-critic`. Each dimension is **boolean**, names a **function**, cites a **source** (the offending axiom/consequence), and carries a **floor**. The `_shared/critic-core` loop and guards apply verbatim — including the **steelman** (a deliberate genre choice is not a deficiency) and the **evidence-anchor cap** (no cited axiom/consequence → auto-FAIL).

> **Judge soundness, not taste.** Soft vs hard magic, grim vs bright, sparse vs baroque — author's call (bounded authority). The rubric asks only whether the system is *costed, limited, accessed, propagated, plausible, generative, and bounded.*

## Core dimensions (apply across system types)

| Dimension | Source | Pass-test (function) | Floor | Catches |
|---|---|---|---|---|
| **Cost is real** | `magic-system-design` / `economic-systems` | Every use of the system carries a real, legible cost or trade-off — nothing is free | required | Consequence-less power; magic/tech with no price |
| **Limits > powers** | Sanderson's 2nd Law | The system is defined more by what it *can't* do than what it can; the limits are explicit and generative | required | God-powers; "anything is possible"; unbounded systems |
| **Access is defined** | `cultures-societies` / `magic-system-design` | Who may use it, and why (bloodline / capital / training / license), is specified — and the access rule shapes society | required | Undefined gating; a power with no social footprint |
| **Propagation (Rule of Consequence)** | `extrapolation-engine` | Each axiom *ripples* through economy, war, culture, tech — it isn't decoration | required | Axioms that don't propagate; a system bolted on, not woven in |
| **Plausibility / explanatory power** | academic worldbuilding eval | Internal cause→effect coherence; no convenient contradictions; the system *explains* the world's shape | required | Ad hoc exceptions; "it works because the plot needs it" |
| **Bright-line on escalation** | `extrapolation-engine` | The powers that *could* escalate to omnipotence have explicit bright lines (e.g. can it edit minds? raise the dead? print money?) | required | One-inference-from-a-god-power; an unruled capability |
| **Generativity** | `faction-design` / `magic-system-design` | The system *generates* conflict, society, and story rather than merely existing | required | Inert systems; a consistent world with no engine |

## Soft-system note (Sanderson's 1st Law)

A deliberately **soft** system (numinous, unexplained — Tolkien's magic) is *valid*, not a failure of "Cost/Limits." The steelman applies: if the softness is **owned** and the narrative **does not use the system to resolve its conflicts**, "Cost is real" and "Limits > powers" relax to **advisory**. The dimension that stays **required** for soft systems is **Bright-line on escalation** — even an unexplained power must not become a plot-solving deus ex machina. (First Law: reader-understanding gates conflict-resolution.)

## Per-type emphasis (the dimensions shift weight by system)

- **Magic system** — Cost, Limits, Bright-line are the spine (the Sanderson core).
- **Economy** — Cost (scarcity source), Propagation (does the money-rule ripple?), Plausibility (sources/sinks balance) dominate; "Limits" reads as *what the economy structurally can't do*.
- **Society / factions** — Access, Propagation, Generativity dominate; add the **coercion stress-test** (`stress-tests.md`): who holds the monopoly on violence?
- **Technology** — Cost, Propagation, Plausibility; add the **suppression/advancement stress-test**: why is the tech level *stable* given the incentives to change it?

## Adding a system type

List the dimensions, mark which are the **spine** for that type, note any that relax to advisory, and name the stress-tests (`stress-tests.md`) most likely to bite. The critic core does not change; only this table does.
