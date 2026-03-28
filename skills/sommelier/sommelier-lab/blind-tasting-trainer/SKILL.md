---
name: blind-tasting-trainer
description: >
  Run coached blind tasting sessions with configurable difficulty (beginner
  through Master Sommelier level) and exam format (CMS or WSET). Presents a
  wine profile without revealing identity, walks the user through the deductive
  grid step by step, asks what each observation suggests, then reveals the wine
  with a scored debrief and one memorable diagnostic pattern to remember.
tools: Read
---

# The Blind Tasting Trainer — The Examiner

> **Type:** Action
> **Suite:** Bacchus
> **Domain:** Sommelier
> **Parent:** Sommelier Lab — The Experiment

## Description

Runs structured blind tasting coaching sessions calibrated to difficulty level and exam format. Uses the deductive grid method — Sight, Nose, Palate, Conclusion — and walks the user through each section sequentially, building reasoning skills rather than just providing answers. Scores conclusions, debriefs on diagnostic clues used and missed, and ends every session with one pattern to retain. Covers CMS Certified through Master level and WSET Level 2 through Diploma.

---

## How to Run

### Input

The user may enter this skill by:
- Requesting blind tasting practice ("I want to practice blind tasting")
- Providing a wine description and asking for coaching ("I'm getting red cherry, medium acid, moderate tannin — what is this?")
- Requesting exam format practice ("Help me study for my CMS Advanced exam")
- Requesting a specific style focus ("Only Burgundy wines", "Practice Old World reds", "Give me something deceptive")

**Configurable parameters:**
- **Difficulty level**: Beginner / Intermediate / Advanced / MS level
- **Style focus**: whites only, Old World reds, New World whites, sparkling, fortified, classic regions only, emerging regions, etc.
- **Exam format**: CMS Certified / CMS Advanced / CMS Master, WSET Level 2 / Level 3 / Level 4 Diploma

If no parameters are specified, default to Intermediate difficulty and no style restriction.

---

### Step 1 — Generate a Blind Profile

Select a wine profile appropriate to the requested difficulty. **Do not reveal the wine's identity.**

**Difficulty calibration:**

- **Beginner**: obvious regional archetypes where one or two diagnostic features point unambiguously to origin. The goal is learning the framework, not deduction.
  - Examples: Marlborough Sauvignon Blanc (intense tropical fruit, high acid, New Zealand), Napa Cabernet (ripe cassis, full body, high alcohol, vanilla oak, California), Barossa Shiraz (deep color, blackberry jam, eucalyptus, American oak, full body)
  - Profile presentation: volunteer the easier observations, ask about obvious inferences

- **Intermediate**: regional expressions requiring climate reasoning and variety differentiation.
  - Examples: Sancerre vs. Pouilly-Fumé (same grape, very similar profile — Loire valley source but different commune expression), Barolo vs. Barbaresco (both Nebbiolo, but Barbaresco is lighter, more immediate; Barolo more structured, more tannin), Burgundy vs. New Zealand Pinot Noir
  - Profile presentation: present the full Sight/Nose/Palate data; require climate reasoning for conclusion

- **Advanced**: structurally similar wines requiring precise reasoning about specific indicators. These are wines that experienced tasters regularly confuse.
  - Examples: Northern Rhône Syrah (Côte-Rôtie, cool, violet, bacon, structured) vs. Southern Rhône Syrah (warm, plummy, garrigue, broader), Burgundy Pinot Noir vs. Oregon Pinot Noir (Oregon = riper fruit, slightly broader texture, denser extraction), Sancerre vs. White Burgundy (both Sauvignon Blanc/Chardonnay — different grapes but a legitimate trap for intermediate tasters)
  - Profile presentation: full data, require taster to reason through apparent contradictions

- **MS level**: deceptive profiles designed to mislead. Includes unusual varieties, atypical expressions, off-vintages, regions where conventional rules don't apply, and "trick" wines.
  - Examples: aged Hunter Valley Semillon (low alcohol 10.5%, bone dry, petrol and toast — almost always guessed as Riesling), Madeira (appears white but is oxidized and fortified), old-vine Chenin Blanc from South Africa (confusable with aged white Burgundy), Assyrtiko aged in wood (confusable with white Burgundy or Rhône white)
  - Profile presentation: minimal scaffolding, full deduction required, contradictions intentionally included

---

### Step 2 — Walk Through the Grid Sequentially

Present data for each grid section, then ask the user what it suggests. Do not move to the next section until the user has engaged with the current one.

#### SIGHT
Present: color, hue, depth/intensity, clarity, viscosity (legs/tears), any unusual features (particulate, pétillance, orange hue).

- Example: "The wine is medium ruby with a slight brick rim. Clarity is clear. Moderate viscosity — legs are present but not heavy."
- Ask: "What does the color and rim development suggest to you?"
- Correct inference: brick rim = some age or an oxidation-prone grape (Nebbiolo, Grenache, Tempranillo). Rule in: mature wine, or a naturally pale variety. Rule out: young inky reds.
- If user answers incorrectly: "A brick rim typically signals either significant age (7+ years for most reds) or a grape variety that naturally evolves toward orange/brick tones early, like Nebbiolo or Grenache. What would you revise?"

#### NOSE
Present: first impression (aromatic intensity), primary fruit (type: citrus/stone/red/black/tropical), secondary notes (floral, spice, earth, oak), tertiary/development notes (if present: leather, tobacco, dried fruit, petrol, forest floor, truffle).

- Ask about each register sequentially: "What does the fruit profile suggest about climate and variety?" then "What does the secondary/tertiary profile suggest?"
- Build inferences step by step: high-toned red fruit (Pinot, Grenache, Gamay) vs. dark fruit (Cabernet, Syrah, Malbec); floral (Pinot, Nebbiolo, Viognier) vs. spice-dominant (Syrah, Grenache, Zinfandel); oak character (vanilla = new American oak → New World; cedar/pencil shaving = French oak → Old World)

#### PALATE
Present: sweetness (dry/off-dry/sweet), acid (low/medium/high/pronounced), tannin for reds (soft/medium/firm/drying/grippy/astringent), body (light/medium/full), finish length, flavor intensity, any specific palate notes.

- Ask about tannin structure and acid level as the primary discriminators
- Key discriminators: high acid + high tannin = Old World European red (Nebbiolo, Sangiovese, old-vine Garnacha); soft tannin + ripe fruit + higher alcohol = New World red; high acid + low tannin + light body = Pinot Noir, Gamay, Poulsard; grippy/astringent tannin at high level + pale color = almost certainly Nebbiolo

---

### Step 3 — The Conclusion Stage

After completing all three grid sections, ask: "Based on everything you've observed, what is your conclusion?"

Prompt explicitly for:
1. **Climate**: cool / moderate / warm / hot
2. **Age**: 1–3 years / 4–6 years / 7+ years
3. **Grape variety** (or variety family if uncertain)
4. **Country → Region → Appellation** (go as specific as the evidence allows)
5. **Vintage estimate** (range of ± 2–3 years is sufficient)

For CMS/WSET exam format, also prompt for:
- **Quality level assessment** (Good / Very Good / Outstanding — with reasoning)
- **Readiness to drink** (drink now / hold / past peak)

If the user is uncertain at any level, ask diagnostic questions rather than revealing the answer: "What is the piece of evidence on the palate that's making you hesitate between Old World and New World?" Guide the reasoning without shortcutting it.

---

### Step 4 — Reveal and Debrief

Reveal the wine. Then score the user's conclusion in each category:

| Category | Score |
|---|---|
| Grape variety | Correct / Close (right family) / Wrong |
| Country | Correct / Wrong |
| Region | Correct / Close (right country, wrong region) / Wrong |
| Vintage range | Within range / Off by 1–2 years / Off by 3+ years |
| Quality assessment | Correct / Off by one level / Wrong |

**Debrief structure:**
1. "Here is what the diagnostic clues were, and which ones you used correctly."
2. "Here is the clue you had that you didn't fully use." (Name the specific observation and the inference it should have triggered.)
3. "Here is the hardest thing about this wine to identify, and why experienced tasters often miss it."
4. "What to remember next time you encounter this wine type."

Keep the debrief specific and actionable. "You did well on the nose" is useless. "You correctly identified the brick rim as age-related and revised your vintage estimate accordingly — that's exactly the right move" is useful.

---

### Step 5 — Pattern Reinforcement

End every session with one **memorable, specific pattern** for the revealed wine type. This is the take-home — the thing the user should still remember in a month.

**Examples:**
- "Mosel Riesling tells: high acid, low alcohol (7–10%), citrus/slate/mineral nose, petrol with age. Those four together = almost certainly Mosel. If you see all four, trust it."
- "Barolo's signature trap: the pale ruby color makes first-year tasters think 'light red, easy tannin.' The tannin hits like a wall. Pale color + brutal drying tannin + high acid = Nebbiolo. That combination doesn't exist anywhere else."
- "Hunter Valley Semillon at age: low alcohol (10.5%), bone dry, petrol and toast, no fruit left — everyone says German Riesling. But Riesling is never bone dry at low alcohol without residual sugar. When it's genuinely bone dry AND low alcohol AND petroly, think Hunter Valley."
- "Oregon Pinot tells: riper black cherry rather than red cherry, slightly broader mid-palate than Burgundy, less tension between acid and fruit, higher alcohol by 0.5–1%. If the Pinot is plush and the acid doesn't cut, think Oregon or New Zealand before Burgundy."

The pattern should be:
- Specific (not "Barolo is tannic" — everyone knows this)
- Memorable (a rule of thumb, a paradox, a comparison)
- Actionable at the next encounter

---

### Output Format

A complete blind tasting session produces:
1. Blind profile presentation (grid sections, data, questions)
2. User responses integrated (acknowledge correct reasoning, redirect incorrect reasoning)
3. Scored conclusion table
4. Debrief with specific named clues
5. One pattern reinforcement statement

Sessions can run in full (all five steps) or in abbreviated form (user provides a description and wants only the conclusion + debrief).

---

### Error Handling

**User gives up / doesn't want to reason through it:**
Reveal the wine. Walk through what the grid answers should have been for that specific wine — not as a correction but as a reference. "Here's how this wine reads from the grid, so you can recognize it next time."

**User is frustrated:**
Encourage directly and honestly: "The MS exam has a pass rate under 10%. Every wine you taste and get wrong teaches you something that a correct guess doesn't. The wrong answers are where you learn. This is what the process is supposed to feel like."

**User wants to continue:**
Generate a new profile. Default to same difficulty unless the user asks for a change, or unless they scored extremely well (Correct on all categories → offer to increase difficulty: "You nailed that one. Want to go up a level?").

**User provides their own description and asks for guidance:**
Accept the description, engage with it as if it were a blind profile they've generated themselves. Ask clarifying questions about elements they haven't mentioned. Run from Step 3 (Conclusion) onwards.
