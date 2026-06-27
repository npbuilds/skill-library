# Anti-Pattern Detectors — Operationalized

`micro-tension` ships an anti-pattern table. This file converts it into **concrete, scannable failure-detectors**: surface signatures the critic can find verbatim in the text, each mapped to the dimension it fails and the fix to hand `prose-editor`. This is half the critic — most quality failures are one of these.

Each detector is a **find-the-line** test. When you find the signature, quote it (the evidence-anchor cap requires a verbatim cite), then run the steelman test before failing.

> **A detector hit is a prompt to test for earned intent — not an automatic FAIL.** Before failing, apply SKILL.md Step 2e: is the pattern *intentional, consistent across the passage, and achieving a nameable effect the conventional move couldn't*? An even tone that *enacts* numbness, a flat affect that *enacts* dread — these are choices, and they PASS. Only an **unearned** signature (a slip, achieving nothing) is a deficiency. Detectors find *suspects*, not verdicts.

---

## Told-emotion detectors → FAIL **Interiority**

| Signature to find | Why it fails | Fix for prose-editor |
|---|---|---|
| An emotion **named** as a state: "she was sad/angry/afraid/nervous" | Naming the emotion prevents the reader feeling it | Delete the label; keep the evidence (the specific perception/action that *is* the feeling) |
| Cliché somatic beats: "her heart pounded," "his stomach dropped," "a chill ran down" | Generic body-cliché stands in for specific feeling | Find the somatic detail specific to *this* character in *this* moment |
| "...he felt [X]" / "...she realized [Y]" filter verbs stacking | Distances via reportage instead of rendering | Cut the filter verb; render the perception directly (FID) |

## Even-tone / neutral-prose detectors → FAIL **Micro-tension**

| Signature to find | Why it fails | Fix |
|---|---|---|
| Every sentence carries the **same emotional weight** across a paragraph | No peaks/valleys → no charge | Create variation; let one beat spike |
| Description/exposition with **no emotional filter** — neutral inventory of a room/landscape | Neutral prose has no pulse | Pass each detail through the character's inner state as *friction* |
| A contradiction **surfaces then instantly resolves** in the same beat | Resolution kills the tension it raised | Let the contradiction sit unresolved on the page |
| The character feels **exactly what the situation predicts** (grief at a funeral, joy at a wedding) | Predictable = inert | Find the third-level emotion (the one they won't acknowledge) |

## On-the-nose detectors → FAIL **Dialogue subtext**

| Signature to find | Why it fails | Fix |
|---|---|---|
| A line **states the speaker's exact feeling/intent**: "I'm angry that you left me" | No gap between line and intent = no subtext | Code it: what they'd actually say to *protect* the feeling ("Fine. Do what you want.") |
| Characters **answer every question directly**, no dodges/deflections | Frictionless talk is dead talk | Add a dodge, a subject-change, an evasion that reveals what's guarded |
| Dialogue that exists to **convey information to the reader** ("As you know, Bob...") | Exposition wearing a dialogue costume | Re-route the info; let the scene need drive the talk |

## Info-dump / travelogue detectors → FAIL **Show vs. tell**

| Signature to find | Why it fails | Fix |
|---|---|---|
| A **block of world/backstory** delivered outside any character's immediate need | Lore for its own sake stalls the scene | Apply the iceberg test (`world-to-story`): does a character need this *now*? If not, cut to a stub |
| Abstract summary of events ("Years of war had hardened them") with **no scene-level enactment** | Telling the conclusion robs the reader of the experience | Dramatize one concrete instance instead |
| Sensory-free passage — **no specific, picturable detail** | Generic = invisible | Add one concrete, perception-filtered detail |

## Static-scene detectors → FAIL **Scene turns**

| Signature to find | Why it fails | Fix |
|---|---|---|
| The scene's **value-state is identical** at start and end (same emotional/situational charge) | A scene that doesn't turn has no reason to exist | Find the turn — what *changes*? If nothing, cut or merge the scene |
| Scene ends on **arrival/setup** with no shift | Throat-clearing | Start later, end on the turn |

## Voice-drift detectors → FAIL **Voice consistency**

| Signature to find | Why it fails | Fix |
|---|---|---|
| An **unmotivated register break** — a colloquial line in formal narration, or vice versa | Breaks the voice contract | Restore the established register (or motivate the break) |
| **Narrative distance** lurches (deep POV → sudden omniscient aside) | Distance whiplash | Hold the established distance |

---

## Important: detectors find FAILs, not PASSes

These detect *failure*. A passage with none of these signatures is not automatically a PASS — the evidence-anchor cap still applies: to PASS a dimension you must **quote the line that earns it** (the actual unresolved contradiction, the actual turn, the actual subtext). Absence of failure + absence of grounding evidence = auto-FAIL, not PASS. This asymmetry is the anti-style guard: hollow prose triggers no detector *and* offers no line to cite, so it cannot pass.
