---
name: sensory-translation
description: >
  Translate a worldbuilding sensory palette into prose technique. Use when a built region exists
  (via `sensory-worldbuilding`) and the user needs to render it on the page without sensory-dump
  paragraphs. Covers detail-selection, POV attention bias, sensory-as-characterization, and
  diction-by-region. Sister skill to `world-to-story` and `cultural-voice` — together they form
  the worldbuilding-to-prose bridge.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Sensory Translation — From Palette to Page

A sensory palette is design. Prose is selection. The bridge between them is the question every line must answer: **what would *this* character notice in *this* moment, and why?**

Upstream input: `skills/worldbuilding/physical-world/sensory-worldbuilding/` defines the 5 channels (sound, smell, touch, taste, proprioception) and a sensory signature per region. This skill turns that palette into prose moves.

## The Detail-Selection Filter

You do not render the sensory signature. You render the *one detail* from it that the POV character would notice given their goal, mood, and history. The signature is the well; the line is the cup.

| Step | Question | Output |
|------|----------|--------|
| 1. Pull palette | What is the regional sensory signature? | 2–3 channel-specific anchors |
| 2. Filter by POV | What does *this* character notice about this place? | A subset of 1, weighted by character |
| 3. Filter by scene goal | What detail does the scene's tension want foregrounded? | Usually 1 detail, sometimes 2 |
| 4. Render | Encode that detail in diction, syntax, and metaphor that match POV voice | One or two sentences, not a paragraph |

## POV Attention Bias

A character's noticing pattern is characterization. What they see first reveals where they came from.

- **Born-here:** registers what is *absent* or *off* — the silence of usually-busy bells, the wrong cardamom, the unfamiliar smell of fear in the courtyard
- **New-arrival:** registers what is *abundant* and *strange* — the cardamom, the bells, the sand
- **Returning-after-exile:** registers what is *unchanged* and *grief-tinged* — same bells, same cardamom, same sand, none of it for them anymore
- **Trauma-bound:** registers what *resembles the original event* — the bells become church bells become the bells before the raid

The same room, three POVs, three different detail-sets pulled from the same palette.

## Sensory-Bias-As-Characterization

A character's *channel preference* — which of the five they reach for first — reveals their formative environment. Show this through their narration, not by telling.

| Background | First channel reached for | Why |
|------------|---------------------------|-----|
| Sailor | Smell, proprioception (deck pitch) | Visibility unreliable; nose and body kept them alive |
| Forager | Sight + smell layered | Pattern-matching food and predator at once |
| Musician | Sound; sound metaphors for non-sound things | Trained perceptual mode bleeds across senses |
| Soldier in built terrain | Sound (footfalls, breath, metal) + proprioception | Survival cued to sub-visual signals |
| Cook | Smell + taste, even out of context | Kitchen as primary sensorium |
| Lifelong courtier | Sight + the politics of who-is-looking-at-whom | Visual surveillance as default mode |

When a character of one background narrates a scene set in another's environment, the *gap* is the interest. A musician in a battlefield will reach for sound first — and what they reach for tells you everything.

## Diction-By-Region

A region's sensory palette infiltrates how prose set there *sounds*. This is not a heavy-handed move — it operates one or two word choices per paragraph.

- Desert prose reaches for *grit, sift, snap, parched, sere, glare*
- Coastal prose reaches for *brine, drift, hush, swell, rope-burn, gull-quarrel*
- Highland prose reaches for *bite, cleft, scree, ringing, sparse*
- Underground prose reaches for *echo, settle, drip, mineral, vault*

Match the region's signature, then push *against* it sparingly when you want defamiliarization (a coastal character feeling claustrophobic in a desert — let the desert words press in).

## Anti-Patterns

1. **The sensory dump.** "She smelled the cardamom, the camel dung, the fabric, the sand, the salt of distant sea, the…" Selection over inventory. Always.
2. **Generic descriptors.** *Fragrant, beautiful, harsh, vivid.* These are placeholders; replace each one with a specific anchor from the palette.
3. **Paragraph-as-photograph.** Sensory details work as punctuation between action and thought, not as static description blocks.
4. **POV-neutral sensing.** If your sensory line could come from any character, it's not doing characterization. Bias it.
5. **All-five-channels-per-scene.** Two channels per scene, three at most. The brain doesn't perceive in five-track stereo; neither should prose.
6. **Decorative sensory.** Every sensory detail should be earning its keep — characterization, tension, foreshadowing, mood. Pretty is not enough.

## Worked Example — Same Room, Two POVs

**Setting palette** (from sensory-worldbuilding): A desert trading city at dawn. Signature: cardamom + camel dung, fabric snapping in wind, sand in everything.

**POV A — Sara, born here, returning after seven years of exile:**

> The cardamom was wrong. Yusra's mother had always ground it too fine, the way her own grandmother had taught her — but the steam off the brass pot smelled like every other house's pot, store-bought and sharp, and Sara understood before she sat down that the grandmother had died while she was gone.

POV-A details: cardamom (not the dung, not the wind), filtered through *absence* (the missing fineness of the grind), encoding grief without naming it.

**POV B — Tomás, foreign envoy, day three in the city:**

> Tomás had stopped sneezing on the second day. The sand was a fact now, like the cardamom-and-something-else smell that thickened every doorway, like the way fabric in this place did not hang but *snapped*, awnings and robes and tent walls all clapping in the small wind at once. He sat where the host gestured.

POV-B details: sand (foregrounded as adjustment), cardamom-and-something-else (he can't name the second note — the dung), and the *snap* of fabric (the kinesthetic anchor a born-here narrator wouldn't bother naming).

Same palette, same room. Different attention. The reader learns the world *and* the characters in one move.

## Relationship to Other Skills

**Upstream (worldbuilding inputs):** `sensory-worldbuilding` (the palette), `geography-ecology` (climate baseline), `cultures-societies` (built environment that produces the palette).

**Sibling bridge skills:** `world-to-story` (the iceberg methodology — sensory detail is the primary vehicle), `cultural-voice` (when sensory bias meets cultural diction).

**Downstream (prose craft):** `concrete-detail` (the underlying technique), `character-interiority` (the perception filter), `figurative-language` (when sensory anchors become metaphors), `narrative-craft/scene-craft` (where sensory details sit in scene architecture).

Learn ─── Selection Is the Craft
A palette is everything that could be noticed. Prose is the one thing this character notices, now. Beginners describe rooms. Working writers describe what their characters cannot stop seeing.
