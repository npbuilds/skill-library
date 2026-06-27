# Rubric Profiles — Swappable by Medium

The critic core is fixed (evidence-anchored, floor-gated, reason-first). The **rubric is a profile**, parameterized by medium. Several dimensions *invert* by medium — what is a virtue in literary fiction is a defect in a children's picture book. Load exactly one profile per run.

Each dimension is **boolean** with a **pass-test** and a **floor**. The floor sets how the dimension gates:
- `required` — must PASS for the gate to pass.
- `advisory` — scored and reported, but does **not** gate (used when a medium genuinely tolerates the dimension being absent).
- `required-if-present` — **conditional**: required only when its precondition holds (e.g. dialogue exists in the passage); when the precondition is absent it is scored **N/A** and excluded from the gate — never an auto-FAIL. See SKILL.md Step 2f.

A dimension **cannot PASS without a cited verbatim sentence** that grounds the pass (the evidence-anchor cap). This is profile-independent.

**Test function, not form.** Each pass-test below names a *function* the prose must achieve; the conventional device in the description is the **default evidence**, not the only path. A deliberately flat, hypnotic passage that achieves the function by other means passes — the critic judges *aliveness*, never *conventionality*. Before failing any dimension on a broken convention, apply the **earned-transgression test** (SKILL.md Step 2e): a rule-break that is patterned and achieves a nameable effect is a *choice*, not a deficiency, and passes. See "Earned transgression vs. deficiency" below.

---

## Profile: `literary-fiction` (default)

The canonical profile. Tuned for adult literary/upmarket fiction where interiority and unresolved tension are the engine.

| Dimension | Source skill | Pass-test — *function* (device = default evidence) | Floor | Catches |
|---|---|---|---|---|
| **Micro-tension** | `micro-tension` | **The page is alive** — it compels attention through an unresolved emotional contradiction *or* by other means (obsessive specificity, dread, momentum). A static scene can pass. | required | Flat, even-toned, lifeless prose |
| **Scene turns** | `scene-craft` | The scene ends in a *different value-state* than it began (a turn) | required | Static, purposeless scenes |
| **Interiority** | `character-interiority` | Feeling is *rendered through perception/somatic specificity*, not labeled | required | Told emotion ("she was sad") |
| **Dialogue subtext** | `dialogue` | *If dialogue is present*, at least one exchange means *more than it says* (line ≠ intent); **N/A** on narration-only passages | required-if-present | On-the-nose talk |
| **Show vs. tell** | `concrete-detail` / `world-to-story` | The world is *enacted through specific detail*, not info-dumped | required | Travelogue / exposition |
| **Originality / surprise** | `style-analyzer` / `narrative-geometry` | At least one beat *subverts the expected* — a third-level emotion, an unpredictable turn, a fresh image — rather than the seen-a-thousand-times default. Cite the surprising line. | required | **Competent but generic** — predictable, cliché, dead-on-arrival |
| **Arc shape** (`draft` level only) | `narrative-arc` / `narrative-geometry` | The whole has a *discernible shape* — escalation, reversal, or convergence | required at `draft` | Shapeless drift |
| **Voice consistency** | `style-analyzer` | Register is *controlled* — it holds, **or breaks in a patterned, earned way**. Unmotivated drift fails; a deliberate, effect-bearing clash passes. | required | Accidental voice drift (not deliberate clash) |

---

## Profile: `genre` (plot-forward commercial fiction)

Thriller / mystery / SFF / romance where forward drive and payoff matter more than submerged interiority. Micro-tension stays required (page-turning is the genre's promise) but interiority relaxes; momentum is added.

| Dimension | Pass-test | Floor | Note vs. literary |
|---|---|---|---|
| **Micro-tension** | Unresolved tension *or* a live story question on the page | required | Story-question counts, not only emotional contradiction |
| **Forward drive** (`pacing`) | The passage *raises or escalates* a question/stake | required | **Added** — genre must pull |
| **Scene turns** | Scene ends in a changed state | required | same |
| **Show vs. tell** | World/clues enacted, not summarized | required | same |
| **Interiority** | Feeling rendered, not labeled | **advisory** | Relaxed — genre tolerates lighter interiority |
| **Dialogue subtext** | Lines carry intent beyond content | advisory | Relaxed |
| **Voice consistency** | Register holds | required | same |
| **Arc shape** (`draft`) | Discernible escalation/payoff structure | required | Payoff-weighted |

---

## Profile: `rpg-playability` (tabletop / interactive world material)

Judged for *playability and prompting power*, not finished prose. The reader is a GM/player who must act on it.

| Dimension | Pass-test | Floor | Note |
|---|---|---|---|
| **Actionable hooks** | The passage offers ≥1 thing a player can *do* or *pursue* | required | Replaces "scene turns" |
| **Evocative specificity** | Concrete, usable sensory/world detail (not abstract lore) | required | `concrete-detail` / `sensory-worldbuilding` |
| **Open-endedness** | Leaves *deliberate gaps* for player agency (not over-determined) | required | Inversion: total resolution is a defect here |
| **Faction/tension seeds** | Names a live conflict or pressure a GM can escalate | required | `faction-design` |
| **Micro-tension** | — | **advisory** | Not the point of reference material |
| **Voice consistency** | Tone holds across the entry | required | same |

---

## Profile: `childrens` (picture book / early reader)

**The clearest inversion.** Micro-tension's "unresolved contradiction" is *wrong* here — young children need emotional *clarity*. New dimensions (read-aloud rhythm, refrain, vocabulary ceiling, one-beat-per-spread) dominate. Parked as out-of-scope for v1 of the narrative system, included for completeness.

| Dimension | Pass-test | Floor | Note |
|---|---|---|---|
| **Emotional clarity** | The feeling is *legible and single* in each beat | required | **Inverts** micro-tension |
| **Read-aloud rhythm** | Lines scan aloud — meter/stress is regular and speakable | required | `prose-rhythm` |
| **Refrain / repetition** | A repeated structure a child can anticipate | required | Inversion: repetition is a virtue |
| **Vocabulary ceiling** | Diction stays within the age band | required | `diction` |
| **One beat per spread** | Each unit advances exactly one idea | required | `pacing` |
| **Show vs. tell** | Concrete and picturable | required | same |

---

## Profile: `experimental` (form-breaking / transgressive literary work)

For work whose whole point is to break form — modernist flat affect, stream-of-consciousness, fractured structure, deliberate register-collision. The danger here is **the critic acting as a conformity engine**, so this profile maximally protects earned risk. The critic core is unchanged; the floors shift toward function and the surprise dimension becomes the spine.

| Dimension | Pass-test | Floor | Note vs. literary |
|---|---|---|---|
| **Aliveness** | The page compels attention by *any* means | required | Micro-tension, fully de-conventionalized |
| **Originality / surprise** | The work subverts the expected; it is *not* the default move | required | Promoted to the spine — the reason this profile exists |
| **Earned intent** | Every formal break is *patterned* and achieves a *nameable effect* (the steelman test passes) | required | The guard against pretension-as-art |
| **Scene turns** | Some shift occurs (may be tonal/perceptual, not plot) | advisory | Relaxed — form-breaking work may refuse the turn |
| **Voice consistency** | — | advisory | Relaxed — deliberate register-collision is the medium |
| **Show vs. tell** | — | advisory | Relaxed — abstraction may be intentional |

> The `experimental` profile **never** judges bold-vs-safe direction (the writer's fork). It only enforces that the boldness is *earned* — alive, surprising, and effect-bearing — not hollow. Pretension fails `Earned intent`; it cannot cite the effect its breaks buy.

---

## Earned transgression vs. deficiency

The hardest judgment the critic makes, and the one that decides whether it protects creativity or crushes it. A broken convention is one of two things:

- **Deficiency** — *unearned*. The writer didn't mean it; it achieves nothing; it's a one-off slip. → FAIL.
- **Earned transgression** — *intentional, patterned, effect-bearing*. The writer broke the rule because the conventional move couldn't do what this does. → PASS (often an excellence).

The test that separates them is the same evidence-anchor that catches hollow-polish: **cite the line and name the effect it buys.**

| Signature | Deficiency (FAIL) | Earned transgression (PASS) |
|---|---|---|
| Flat affect | Numb, undifferentiated, achieves nothing | McCarthy — flatness *enacts* moral exhaustion / dread |
| Run-on / no punctuation | Confused, accidental, unreadable | Saramago — the rush *enacts* breathless inevitability |
| Static scene | Inert, nothing accrues | Robinson — stillness *accrues* philosophical weight |
| Register clash | Unmotivated wobble | Deliberate collision that *lands* a tonal effect |

If you cannot name the effect, it is not transgression — it is **pretension**, which is hollowness in transgression's clothes, and it FAILs the same way purple prose does.

---

## Adding a profile

1. List dimensions, each with a boolean pass-test, a source skill, and a floor (`required` | `advisory`).
2. Note any **inversions** — dimensions whose virtue flips vs. literary-fiction (these are the dangerous ones to miss).
3. The critic core does not change. Only this table swaps.
