---
name: conflict-design
description: >
  Design a conflict — war, insurgency, revolution, cold or economic conflict, feud —
  as a system: why it starts, how it escalates, what equilibrium holds it, how it ends,
  and how it corrupts its participants. Reference when building the central conflict of a
  world or story, a war between factions, a rebellion, or a rivalry. Covers the five
  conflict axes (each a stated/felt dual), conflict as a metastable game tipped by
  emotional variance, and the strategist who manages the variance gradient.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Conflict Design — The Game Between the Players

A conflict is not a fight scene, and it is not a villain. It's a *system*: two or more parties who cannot get what they want by bargaining, locked in a structure that escalates, holds, and eventually breaks. Faction-design gives you the players; this gives you the game between them; narrative-craft narrates the match.

The single most useful fact in the scholarship: **war is always ex-post inefficient** — both sides pay costs they could have avoided with an ex-ante deal. So the first design question is never "who fights?" but **"why did the bargain fail?"** Rational actors have exactly three reasons (Fearon): private information they can't credibly reveal, a commitment neither can credibly make, or a stake that can't be divided. Every designed conflict starts by naming which one.

But a purely rational conflict is a *solved* game — you could read its ending off the payoffs, and a solved game has no drama. What makes it unsolved is **emotion**: the humiliation that makes a divisible stake indivisible, the grievance that makes people pay costs no calculation would justify, the rage that makes an incredible threat credible. Emotion is not noise on the model. It is the variance that decides when the system tips. Design the rational skeleton first; then layer the emotional variance that brings it alive.

## The Five Axes

Every conflict answers five questions. Each has a **stated (rational) face** and a **felt (emotional) driver**, and *the gap between them is where the drama and the instability live*. This stated/felt split is the skill's core tool — run it on every axis.

| Axis | Stated (rational) | Felt (emotional) — the real driver |
|---|---|---|
| **Stakes** | territory, resource, succession, power | honor, humiliation, existential fear — *honor is what makes a divisible stake indivisible* |
| **Cost** | can each side afford the blood/treasure? | what grievance makes people pay a price no cost-benefit would justify |
| **Lifecycle** | the escalation ladder; the equilibrium that holds | which ratchet dominates — rational escalation self-corrects; the cycle of hatred self-amplifies |
| **Legitimacy** | the legal/strategic justification | the mobilizer — identity, grievance, hope, hatred (propaganda is emotional engineering) |
| **Termination** | the deal both sides would prefer to fighting | the block that seals the off-ramp — can't accept humiliation; revenge unpaid; grief demands more |

Read `references/the-five-axes.md` for each axis in full, worked in three layers (a craft question, a case, and the theory underneath).

## Conflict as a Metastable Game

A conflict worth writing is neither dead-stable (nothing happens) nor chaotic (nothing means anything). It sits in a **metastable equilibrium** — an order held in place by deterrence, dependency, or exhaustion, that looks permanent until it isn't. The interesting question is what tips it.

**Emotion is the tipping variance.** A stable order breaks not when the math changes but when someone's *felt* assessment crosses a threshold. Two things make this a design tool, not a hand-wave:

1. **The variance is biased, not random.** Loss-aversion, revenge, and honor are *predictable* deviations. So a cool head can model other actors' emotional volatility while capping its own — the **strategist operation**: suppress your own variance, weaponize theirs. The "principle" a great strategist is bound by is the self-imposed cap on their own volatility, and it's exactly what lets them exploit everyone who lacks one.
2. **Rising variance is the warning sign.** In complex systems, a variable's volatility *rises* as it nears a tipping point ("critical slowing down"). The dramatized version: the doom clock starts ticking when the felt volatility in the system starts climbing — the reprisals get hotter, the rhetoric less hedged, the moderates quieter.

**The calibration rule (which is also a failure mode):** variance must stay *coupled to stakes*. Bounded unpredictability is drama; unbounded is chaos that reads as the author flailing. Turn the emotion knob up only as far as the stakes can absorb.

Read `references/emotion-and-variance.md` for the strategist operation, commitment devices, and the tipping model in full; `references/insurgency-and-revolution.md` for how rebellions build and corrupt (the principal-agent gap); `references/case-study-library.md` for worked conflicts on the five axes; `references/failure-modes.md` for the evidenced ways this goes wrong.

## Design Workflow

1. **Name the bargaining failure** — private information, commitment problem, or indivisibility. This is the conflict's rational spine.
2. **Run the stated/felt split** on all five axes. The gaps are your drama.
3. **Set the equilibrium** — what holds the conflict in place, and what it would take to tip it.
4. **Assign the variance** — which actors are volatile, whether their volatility is exploitable, and by whom.
5. **Design the ending backward** — the deal both sides would prefer, then the emotional block that keeps them from taking it. (Ending is the three bargaining failures in reverse.)
6. **Keep the cost on the page** — or the whole system reads as a bloodless strategy game.

## Common Mistakes

Worked, evidenced versions of these are in `references/failure-modes.md`.

1. **The monolithic-evil conflict.** One rootable side against one villainous side. The scholarship and the craft agree: every camp needs a real virtue and a real crime; the "wrong" side gets a legitimate grievance (the villain is the hero of their own story).
2. **The bloodless strategy game.** Conflict as a chess problem with no human price. If no character carries an assigned cost of the war, the stakes are notional.
3. **Uncoupled variance.** Emotion cranked past what the stakes can hold — escalation without payoff. Volatility must stay tied to something real.
4. **Deus ex machina resolution.** An ending imposed from outside rather than earned by the characters and the stakes established. Turning points must come from choice.
5. **The rational-only conflict.** A solved game: correct, legible, and inert. If you can read the ending off the payoff matrix, you have a model, not a story.

## Related Skills

Conflict-design consumes and extends several skills — cross-link, don't restate.

- `faction-design` — the players this operates on (the Four Essentials feed the Stakes and Legitimacy axes).
- `classical-games` — the formal engine for deterrence, brinkmanship (Chicken), credible commitment, and the folk-theorem stability that holds a metastable order.
- `cooperative-games` — bargaining range, BATNA, and coalition stability (the Core) for Stakes and Termination.
- `behavioral-game-theory` — prospect theory and framing: the biased, exploitable variance at the center of this skill.
- `revolutions-and-regime-change` — Brinton's stages, Skocpol's structural conditions, and the "revolution devours its own" dynamic feeding the insurgency lifecycle.
- `empires-and-states` — Weber's legitimacy typology and the legitimacy-coercion trade-off for the Legitimacy axis.
- `magic-system-design` — the sibling method: its First Law (don't resolve conflict with a force the reader doesn't understand) generalizes to *all* conflict resolution.
- `world-bible` — the source of truth this builds on; conflict-design's output populates its `references/faction-conflict-web.md`.
