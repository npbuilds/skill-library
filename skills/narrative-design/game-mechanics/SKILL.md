---
name: game-mechanics
description: >
  Design tabletop and mobile game mechanics with structural rigor. Reference when creating core
  loops, balancing risk and reward, designing economic systems, building network/map mechanics,
  writing event cards, or adapting complex games for mobile. Use whenever the user is designing
  game rules, mechanics, player interaction systems, or needs to evaluate whether a mechanic
  will feel good in play. Covers engine building, bubble/crash event design, ethical/corrupt
  dual-track tension, anti-patterns, and mobile constraints. Immediately applicable to any
  hybrid Euro/strategy game — especially Splendor/Catan-style games with economic or
  map-building elements.
---

# Game Mechanics — Design Reference

This skill is a working reference for designing mechanics that feel good in play. The goal is
not simulation fidelity — it's player experience. A mechanic is good when players choose it
willingly, feel its consequences clearly, and understand (in retrospect) why it played out the
way it did.

Read `references/mechanic-patterns.md` for the named pattern library with specific examples.

---

## The Three-Loop Model

Every well-designed game has three nested loops. If any loop is missing, players lose
motivation at that timescale.

| Loop | Timescale | What it does | Failure mode |
|------|-----------|-------------|-------------|
| **Primary** | Per turn | The atomic action — collect, build, spend | Too short: trivial. Too long: exhausting. |
| **Secondary** | Per session | The arc of a match — race to a threshold | Missing: players don't know if they're winning |
| **Tertiary** | Across sessions | Persistence, collection, meta-progression | Missing: no reason to return tomorrow |

**Diagnosing loop problems:**
- If players don't know what to do on their turn → primary loop is unclear
- If players disengage mid-game → secondary loop has no tension inflection
- If Day 7 retention is poor → tertiary loop is too slow or unrewarding

**Strong examples:**
- *Splendor*: collect gems (primary) → buy cards that produce gems (secondary) → race to 15 prestige (session end)
- *Brass: Birmingham*: build industries (primary) → connect via network to activate them (secondary) → era flip resets board state (mid-session inflection)
- *Terraforming Mars*: play cards to terraform (primary) → corporation engine grows (secondary) → generation count drives urgency (tertiary within a session)

---

## Balance Frameworks

### Risk/Reward Calibration
Reward should scale with risk, but the player must be able to *choose* their risk level. Forced
risk (pure randomness) feels punitive. Chosen risk (bet on a bubble, run a scheme) feels
exciting even when it fails, because the player authored the outcome.

The test: after a loss, does the player say "bad luck" or "I should have seen that coming"?
Design for the second response.

### Catch-Up Mechanics
Leaders win more often in games without catch-up — which drives casual players away after one
bad game. But obvious catch-up (rubber-band AI) feels insulting.

Good catch-up is *structural*: trailing players have more options, not better luck.
- *Catan*: robber always targets the leader, which is a player choice with plausible deniability
- *Ticket to Ride*: destination cards give trailing players high-risk/high-reward catches
- *Brass*: the Era flip resets some advantages and lets new leaders emerge

Avoid: giving trailing players free resources. This solves the symptom, not the cause.

### Tempo
Tempo is how fast the game accelerates. A game should feel faster in round 5 than round 1 —
engines are bigger, decisions have more weight. If turns get slower as engines grow, the game
exhausts players before the climax.

Design for tempo acceleration: late-game actions should be fewer but more impactful than
early-game actions.

### The "Feel Bad" Problem
Randomness that punishes a player for good play feels bad. Randomness that punishes a player
for overreach feels like justice.

The difference is *foreshadowing*: if a crash was predictable in retrospect, it's fair. If it
arrived from nowhere, it's frustrating. Use semi-transparent event decks (players see
distribution, not order) to preserve skill while reducing randomness frustration.

### Ethical/Corrupt Dual-Track (Frostpunk Model)
When a game wants to model moral tension, don't make it a binary choice. Make it a
**continuous slider** where every action has a corruption value, and the aggregate position
drifts visibly over time.

- Honest track: slower, more stable, builds reputation that unlocks civic bonuses
- Corrupt track: faster short-term gains, accumulates a Scandal meter with threshold consequences
- Other players can *see* your track position but not your specific actions (hidden information maintained)

The player should never feel forced into corruption — it's always a choice with clear tradeoffs.

---

## Economic Mechanics

### Engine Building (Splendor Model)
The tiered resource conversion chain: common resources → buy cards → cards produce better
resources → buy better cards. Three design rules:
1. Every tier should feel qualitatively different, not just quantitatively
2. The engine should be legible: players can see what others are building
3. Late engine should feel like a machine running itself, not constant micromanagement

### Market Dynamics
Prices driven by collective player behaviour create emergent strategy. The more players
buy a commodity, the higher it rises — until it doesn't.

Key design question: who sets prices? If the system sets them, players optimise against the
system. If players collectively set them (Container model), players optimise against each other.
The second is more interesting but harder to balance with AI.

### Bubble/Crash Event Design
The cleanest bubble mechanic (*The Estates* model): no single player is "the bubble" — all
players collectively inflate it because the short-term math is correct. When it pops, the
blame is shared. This is historically accurate and psychologically satisfying.

Implementation:
- A **Mania card** inflates one commodity 2-3x for 2-3 rounds; creates FOMO
- A **Crash card** collapses that commodity; players holding it absorb the loss
- Semi-transparent deck: show distribution ("3 Mania cards remain, 1 Crash"), not order
- Crashes must be *recoverable* — not a death sentence

### Dual-Resource Systems
When a game has two resource tiers (common + rare), they create natural economy layers:
- Common resource: abundant, tradeable, used for standard actions
- Rare resource: scarce, non-tradeable, used to activate special abilities

The rare resource should feel categorically different — not "more common resource" but
"the thing that makes your engine do something extraordinary."

### Obligation Chains (Ponzi Model)
New investors pay old obligations. When obligations exceed capacity, cascade failure. Design
for: the moment of recognition (player sees collapse coming), the last-ditch pivot (one more
action to escape), and the collapse itself (spectacular, legible, not elimination).

---

## Network & Map Mechanics

### Route Claiming (Ticket to Ride / Brass Model)
Visual networks on maps are natively mobile-friendly — one of the strongest UI patterns in
strategy gaming. Route claiming should:
- Be spatially intuitive: connections should look like connections
- Create natural chokepoints: key routes that multiple players want
- Produce legible state: glancing at the map tells you who's winning

### Connection-Activation (Brass Model)
The most elegant map mechanic in recent Euro design: building an industry is not enough —
it must be *connected* to a market to activate. This creates two decision axes
(what to build, where to connect) without requiring complex rules.

The visual metaphor: industry tiles are face-down until a network connection flips them active.
This is extremely legible on mobile.

### Chokepoints Without Combat
Natural player interaction without attacking: if one player controls the only route between
two key nodes, all others must negotiate or build around them. The interaction is *positional*,
not aggressive — lower friction for casual players, same strategic depth.

---

## Card Mechanics

### Semi-Transparent Decks
Players see the *distribution* of upcoming events (e.g., "3 Mania cards, 1 Crash card remain")
but not the *order*. This preserves skill (read the risk window, position accordingly) while
reducing randomness frustration (no crash came from nowhere).

### Asymmetric Player Identity
Each player has a unique starting ability that changes *how* they play, not *what* they can
access. Good asymmetry:
- Changes strategic priority ("The Alchemist wants Flux; The Navigator wants Lanes")
- Creates readable player identity ("they always hoard routes — they must be the Navigator")
- Does not block options: asymmetry is a bonus, not a restriction

### Event Cards that Respond to Game State
Static event cards (fixed effects) are random. Dynamic event cards (effects scale with
current game state) are strategic. Design events that reward players who read the board:
"All players holding more than 3 Tulip Stock lose half" is more interesting when Tulips
are already inflated by player choice.

---

## Mobile-Specific Constraints

| Audience Tier | Session Length | Complexity Budget | Async Support |
|--------------|---------------|-------------------|---------------|
| Casual | 5-15 min | Low — one core loop | Optional |
| Mid-core | 20-35 min | Medium — 2-3 systems | Important |
| Hardcore | 45-90 min | High — full Euro complexity | Essential |

**AI opponent design** is the critical failure mode for economic games on mobile. An AI that
doesn't inflate the bubble makes the bubble mechanic feel hollow. An AI that doesn't respond
to market prices makes the market mechanic feel pointless. Build AI behaviour around market
signals, not optimised paths.

**Tutorial design:** never a rulebook. The first session *is* the tutorial — introduce one
system per match for the first 3 matches. Players learn by playing, not by reading.

**One-thumb legibility:** if a mechanic requires comparing two non-adjacent areas of the
screen simultaneously, it will fail on mobile. Design for thumb-radius information density.

---

## Player Psychology

**Complicity (Papers Please model):** Satire lands when the player *performs* the absurdity,
not observes it. Don't show the player a Ponzi scheme — let them run one. The moral weight
arrives through mechanical action.

**FOMO:** Time-limited opportunities (a Venture that closes next round; a commodity about to
crash) create urgency without requiring timers. Use sparingly — chronic FOMO exhausts players.

**Schadenfreude:** Other players' collapses are fun to watch when the collapse was *their
fault*. Design for legible hubris arcs: the pump-and-dump that worked until it didn't.

**Loss Aversion:** Players feel losses ~2.5x more intensely than equivalent gains (Kahneman).
Design crash events to feel *smaller* than their mathematical size: spread the loss over time,
give one pivot action, make the post-crash state recoverable.

---

## Anti-Patterns (Red Flags)

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Kingmaking** | Eliminated player determines winner | Remove elimination; use point-loss instead |
| **Runaway Leader** | Leader wins from round 3 | Add structural catch-up (more options for trailing players) |
| **Feel-Bad Randomness** | Players blame luck, not choices | Semi-transparent decks; foreshadow random events |
| **Negotiation Dependency** | Game is boring with AI | Make markets systemic, not social |
| **Complexity Creep** | Sessions exceed target length | Audit every rule for primary-loop contribution |
| **Simulation Trap** | Game is realistic but slow | Abstract ruthlessly; fun over fidelity |
| **Crash as Punishment** | Crash events end player agency | Crashes must be recoverable; never eliminate |
| **Obvious Corruption** | Corrupt track is always optimal | Calibrate so honest play is viable long-term |

---

## Playtesting Framework

**Test order:** core loop first (can players take turns fluently?) → economic balance (does
anyone run away?) → event cards (do crashes feel fair?) → full game (does it hold together?).
Never test event cards before the core loop is stable.

**The 5-Session Rule:** mechanics that feel good on session 1 but bad on session 5 are
novelty, not design. Mechanics that feel awkward on session 1 but reveal depth on session 5
are worth keeping. Test at session 5, not session 1.

**Balance signals:**
- If one strategy wins >60% of the time, it's dominant — nerf or buff alternatives
- If no strategy wins consistently, the game is too random — add more player agency
- If players consistently make the same first move, the opening is solved — add variance

**Corruption calibration:** run 10 sessions where one player always plays corrupt, one always
honest. If corrupt wins >70%, rebalance threshold consequences. If honest wins >70%, reduce
corrupt rewards.

---

## Pattern Library

Read `references/mechanic-patterns.md` for the named pattern catalogue — reusable mechanic
structures (like software design patterns) with landmark game examples and implementation
notes. Organised by:
- Resource Mechanics
- Market & Economic Patterns
- Network & Spatial Patterns
- Event & Chaos Patterns
- Tension & Pacing Patterns
- Mobile Adaptation Patterns