---
name: cultural-voice
description: >
  Translate a culture into how its people talk and think on the page — vocabulary domains,
  idiom source, syntactic rhythm, metaphor reach, and the things characters refuse to explain
  because everyone they know already understands. Use when a culture has been built (via
  `cultures-societies` and `naming-system`) and the user needs characters from that culture
  to *sound* like they belong to it without infodump or accent caricature. Sister skill to
  `world-to-story` and `sensory-translation` — together they form the worldbuilding-to-prose
  bridge.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Cultural Voice — How Characters Carry Their World

A name with the right phonemes is a start. A character whose *thought-shape* matches their culture is the finish. This skill is about the second.

Upstream inputs: `worldbuilding/cultures-societies/` (the seven pillars), `worldbuilding/naming-system/` (phoneme palette), `worldbuilding/world-bible/` (axioms the culture treats as obvious). Output: prose moves that infuse those constraints into vocabulary, idiom, syntax, metaphor, and refusal-to-explain.

## Five Levers

These are five places culture leaves a fingerprint on a character's voice. Reach for one or two per scene, not all five — saturation reads as parody.

### 1. Vocabulary Domains

A culture has many words for what it cares about and few for what it doesn't. The character's vocabulary reveals their culture before any plot does.

| Cultural priority | Lexical expansion |
|---|---|
| Pastoral economy | Specific words for livestock by age, season, condition; one word for "city" |
| Maritime trade | Wind types, sea states, hull parts, rope knots; one word for "forest" |
| Court politics | Honorifics, degrees of indirection, gradations of obligation; few words for manual labor |
| Magic-permeated society | Many words for magical states and adjacent failures; few words for ordinary work |
| Subsistence in scarcity | Specific words for kinds of hunger, kinds of going-without |

Render this by *what your character names precisely* (use the cultural specificity) vs. *what they generalize* (lump into a single word). A herder character will name three kinds of wind and call all of court "the city stuff." A courtier will name three kinds of indirection and call the herder's three winds "wind."

### 2. Idiom Source

Idioms encode what the culture *did with its hands and faced with its body* across generations. The metaphor source domain reveals economic and ecological history.

- Agricultural cultures: *root, graft, fallow, harvest, season, sow, reap, fruit borne*
- Hunting cultures: *track, scent, downwind, kill clean, follow the blood*
- Sailing cultures: *trim, tack, weather, becalmed, hold the line, all hands*
- Smithing cultures: *temper, anneal, fold, ring true, brittle, dross*
- Court cultures: *the gesture, the right hand, the long room, the small voice*

A character idioming from the wrong source feels off-culture. A character idioming from a *neighboring* culture's source can be characterization — they grew up at the border, or they read foreign books, or they spent a year in service to a sailor.

### 3. Syntactic Rhythm

Cultures have prose-rhythm tendencies that survive translation in the hands of a good writer.

| Pattern | Cultural correlate |
|---|---|
| Heavy subordination, long sentences | Hierarchical cultures; legal/scholarly traditions; oral cultures with formal-speech registers |
| Parataxis (short, stacked, *and...and...and*) | Oral-narrative cultures; saga traditions; cultures with high directness norms |
| Hedging, indirection (*perhaps, it may be, if it pleases*) | High-context cultures, court cultures, cultures where bluntness costs |
| Direct, declarative, low-hedge | Low-context cultures, frontier cultures, professional-rough registers |
| Rhetorical repetition / parallel structure | Cultures with strong oral-performance traditions (preaching, oratory, oath-taking) |

This is voice at the syntax level. Same idea, two cultures:

- **Hedging culture:** *It may be — if I do not mistake the season — that we ought to consider, perhaps tomorrow, beginning to think about the journey.*
- **Saga-parataxis culture:** *Tomorrow we ride. The river is high. We ride anyway.*

### 4. Metaphor Reach

When the character needs to describe something abstract, where do they reach for the comparison? Their lived environment leaks into their figurative language.

- A desert-raised character calls a long silence *a salt flat.*
- A coastal character calls a betrayal *a riptide.*
- A miner calls a slow realization *a seam.*
- A courtier calls a sudden alliance *a turned page.*

The metaphor source should be *consistent within a character* and *contrastive across characters*. A scene with two characters from different cultures discussing the same event can carry tremendous worldbuilding weight just through differing metaphor reach.

### 5. Refusal-to-Explain (Dialogue-as-World-Reveal)

This is the most powerful lever. Characters do not explain to each other what they both already know. What your character *doesn't* explain is what their culture treats as obvious — which is exactly what the reader needs to infer.

Two examples of the same exchange:

**Wrong (infodump):**
> "I'll meet you at the Hollow Door, the western gate of the trade quarter where merchants without guild-seal must declare their goods to the customs assessor."
> "Yes, of course, since I am unguilded I will need to declare my five bolts of silk."

**Right (refusal-to-explain):**
> "Hollow Door. Sundown."
> "Five bolts."
> "Declare the silk?"
> "Half."

The reader does not know yet what the Hollow Door is or what "declare half" implies. They know it is real, and they will understand it when the scene needs them to. The opacity is the world — and the world becomes solid in the reader's mind precisely because the characters trust each other to know it already.

Use this when:
- Two characters share a culture: dial *down* explanation, dial *up* shorthand
- A POV character explains things in narration that they would never speak aloud: the gap between their interior fluency and exterior brevity is characterization
- A foreign POV is present: they can ask the dumb question, or fail to ask it and remain confused, both characterizing

## Anti-Patterns

1. **Accent caricature.** Spelling-out a dialect (*"Oi roight, guv'nor"*) is almost always worse than getting vocabulary, idiom, and rhythm right. Sound through structure, not through phonetic spelling.
2. **Pseudo-archaic syntax.** *"Forsooth, methinks the day waxes long."* Unless your culture is explicitly an in-world archaism, this reads as cosplay. Use *real* syntactic differences from the levers above instead.
3. **One-voice-for-the-whole-culture.** Cultures contain class, region, profession, generation. A peasant and a poet from the same culture share core levers but differ at the edges. Show this with a second character.
4. **Code-switch amnesia.** If a character grew up in two cultures, their voice should *carry both* and shift situationally. Forgetting this is a continuity error.
5. **Phoneme name + alien voice mismatch.** A character with a Seran phonetic-palette name should not narrate in a voice indistinguishable from a Karnish character. Phoneme-coherence and voice-coherence must travel together.
6. **Over-italicized "exotic" terms.** Italicize the in-world term once, on first appearance, then let it stand in roman type. Permanent italics signal that the writer thinks the word is foreign — which means the *narrator* is foreign to their own culture.

## Worked Example — One Line, Three Cultures

**Situation:** Character has just realized their oldest friend has been lying to them for years.

**Culture A — Court-Hedging (long subordination, indirection, lexicon of obligation):**
> She understood, then, the way one understands an old debt — slowly, and with a sense that the loan had been long since spent and only the obligation remained, polite and unkind and impossible to repay.

**Culture B — Saga-Parataxis (short, stacked, low hedge, oath-vocabulary):**
> She knew. Years he had lied. Years she had eaten his bread. The bread was poison and she had liked the taste.

**Culture C — Pastoral-Practical (agricultural idiom source, plain syntax, weather metaphors):**
> It came over her the way frost comes — not at once, but by morning everything dead. The friendship was a field of him she had been tending without knowing it had not been hers to keep.

Same realization, three cultures. The phoneme palette of their names, the seven-pillar profile of their society, and their idiom source all *infused* the voice without ever being stated.

## Relationship to Other Skills

**Upstream (worldbuilding inputs):** `cultures-societies` (the seven pillars), `naming-system` (phoneme palette — voice should match name), `world-bible` (what the culture treats as axiomatic), `conlang-craft` (if a constructed language exists, its syntax should leak into characters' prose-syntax).

**Sibling bridge skills:** `world-to-story` (cultural-voice is one of its revelation channels), `sensory-translation` (cultural sensory bias is half the voice; cultural-voice handles the other half — vocabulary, idiom, syntax).

**Downstream (prose craft):** `dialogue` (where refusal-to-explain operates), `character-interiority` (where idiom source and metaphor reach live), `diction` (vocabulary precision and register), `sentence-craft/syntax-patterns` (subordination, parataxis, hedging rhythm).

Learn ─── Voice Is the Most Honest Worldbuilding
A reader can be told a culture is hierarchical and not believe it. They can be told a culture values directness and not feel it. But when a character refuses to explain something to another character because both of them already know — the reader believes the culture exists. The honest worldbuilding is in what people do not say to each other.
