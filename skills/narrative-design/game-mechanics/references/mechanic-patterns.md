# Mechanic Pattern Library

Named, reusable mechanic structures with landmark examples. Each pattern has a name,
what problem it solves, how it works, and where it's been used well.

---

## Resource Mechanics

### TIERED ENGINE
**Problem:** Resource collection feels flat — all resources feel the same.
**Solution:** Resources exist in 2-3 tiers. Lower-tier resources are common and enable
purchase of cards that *produce* higher-tier resources. Each tier feels qualitatively
different in play.
**Implementation:** Tier 1 (abundant, gathered) → Tier 2 (produced by engine, spent on
upgrades) → Tier 3 (rare, unlocks special abilities only).
**Examples:** Splendor (gems → gem-producing cards → noble tiles), Terraforming Mars
(basic resources → production tracks → milestone/award scoring).
**Watch out for:** Tiers that are quantitatively different but not qualitatively — if Tier 2
is just "more Tier 1," the distinction collapses. Give each tier a different *action type*
it unlocks, not just a higher cost.

### DUAL RESOURCE
**Problem:** One resource type creates a single axis of competition; everything reduces to
"who has more."
**Solution:** Two resource types with different acquisition methods, different uses, and
non-fungibility. Players must manage both.
**Implementation:** Common resource (abundant, tradeable) + Rare resource (scarce,
non-tradeable, activates special abilities). The rare resource should feel categorically
different — like electricity vs. fuel, not gold vs. silver.
**Examples:** Brass (money + cards as two distinct inputs), Power Grid (electro vs. fuel
mix), "This Time Is Different" design (Stock vs. Flux).
**Watch out for:** Making rare resource just a higher-cost common resource. Non-fungibility
is essential — if you can trade rare for common, the distinction collapses.

### CONVERSION CHAIN
**Problem:** Players passively accumulate resources with no interesting choices.
**Solution:** Resources must be actively converted through a chain with decision points at
each step. The chain creates meaningful choices at each stage.
**Implementation:** Raw input → processing step (costs time or secondary resource) →
refined output → final product. Each step is a player choice, not automatic.
**Examples:** Container (manufacturing → shipping → market), Wingspan (eggs → birds →
abilities), Puerto Rico (plantation → production → shipping).
**Watch out for:** Chains that are always optimal to complete — if you always process
everything, there's no decision. Add costs or alternatives at each step.

---

## Market & Economic Patterns

### COLLECTIVE BUBBLE
**Problem:** Bubble mechanics feel arbitrary — one player inflates, another deflates.
**Solution:** No single player "owns" the bubble. All players contribute to inflation
through normal play because the short-term math is correct for everyone. Collapse is shared.
**Implementation:** One commodity's price rises as a function of total player buying.
Each player buying is individually rational. A trigger (Crash card, threshold) collapses it.
Post-collapse loss is distributed across all holders.
**Examples:** The Estates (building inflation), Container (oversupply crashes), tulip mania
as historical model.
**Watch out for:** One player being able to single-handedly trigger a crash on others.
The mechanic should feel like a systemic failure, not a player attack.

### PUMP AND DUMP
**Problem:** Market manipulation is morally interesting but mechanically hard to model.
**Solution:** Give players the explicit ability to inflate an asset they control, then exit
before collapse. Make it a legal first-class strategy, not a rules violation.
**Implementation:** Player can "support" a company (withhold dividends to inflate) or
"dump" it (sell at peak, exit before collapse). Other players can observe signals but not
the intent. The company (or commodity) eventually collapses without support.
**Examples:** 1830/18xx series (company stock manipulation), Offworld Trading Company
(market cornering), Ponzi Scheme (the game).
**Watch out for:** It being always optimal to dump. Add timing uncertainty — the collapse
trigger should be semi-random so dumping too early leaves value on the table.

### OBLIGATION CHAIN
**Problem:** Economic overextension is interesting but hard to make legible and fun.
**Solution:** Actions create future obligations (debts, promises, maintenance costs).
When obligations exceed capacity, cascade failure — but with one last pivot opportunity.
**Implementation:** Every major purchase creates a recurring obligation. Each round,
obligations must be paid before new actions. Failure to pay triggers a cascade: forced
sale of assets at reduced price, which may trigger further obligations.
**Examples:** Ponzi Scheme (the game), Power Grid (plant maintenance), Agricola
(feeding your family).
**Watch out for:** Silent cascade — the player doesn't see it coming. Foreshadow: show
upcoming obligations clearly. The fun is the attempt to escape, not the sudden death.

### SEMI-TRANSPARENT DECK
**Problem:** Random event cards feel arbitrary and punitive.
**Solution:** Show players the *distribution* of remaining events (e.g., "3 Mania, 1 Crash")
without revealing order. Players can reason about probability and position accordingly.
**Implementation:** Event deck has a visible "deck state" display. Shuffle events into
a deck; show type counts, not positions. Skilled players track what's been drawn.
**Examples:** No mainstream game does this cleanly — it's an identified design opportunity.
Pandemic shows the infection deck partially. Dominion shows draw probability implicitly.
**Watch out for:** Making the deck state too legible — if players always know the next
event, it's not a deck, it's a queue. Distribution knowledge preserves uncertainty while
enabling skill.

### PRICE DISCOVERY
**Problem:** Prices set by the game feel arbitrary; players optimize against a fixed system.
**Solution:** Prices emerge from collective player buying and selling behavior. Players
optimize against each other, not the system.
**Implementation:** Commodity prices rise when players buy (demand up) and fall when
players sell or don't buy (supply glut). Track total purchases per commodity per round.
Price resets each round based on last round's demand.
**Examples:** Container (pure player-driven pricing), Navegador (column depletion model),
Power Grid (fuel market depletion).
**Watch out for:** AI breaking the economy. Price discovery only works well when players
are human or AI is trained to respond to price signals, not optimal paths.

---

## Network & Spatial Patterns

### CONNECTION ACTIVATION
**Problem:** Network building feels abstract — roads to nowhere.
**Solution:** Built industries/nodes are inactive until connected to the network. Connection
is a second action layer that creates a two-axis decision space (what to build, where to
connect). Activation is visible on the board.
**Implementation:** Industry tiles placed face-down (inactive). When a network connection
reaches them, they flip face-up (active) and score/produce. Players can build without
connecting — but nothing activates.
**Examples:** Brass: Birmingham (core mechanic), Power Grid (plant activation via city
network).
**Watch out for:** Connection being trivially easy or trivially hard. The interesting
moment is when a connection activates multiple industries at once — design the map to
create those moments.

### CHOKEPOINT DESIGN
**Problem:** Player interaction requires direct conflict (attacking, blocking), which casual
players dislike.
**Solution:** Map geography creates natural chokepoints — single routes between key nodes
that multiple players need. Controlling a chokepoint generates passive toll income without
aggressive play.
**Implementation:** Map has 2-3 key routes that all optimal paths pass through. First
player to claim these routes extracts tolls from all others (or forces a detour). The
interaction is positional, not aggressive.
**Examples:** Ticket to Ride (key routes on popular paths), Catan (port placement,
robber on key hexes), Brass (canal/rail route competition).
**Watch out for:** Chokepoints that are too decisive — if controlling one route wins the
game, players will fight too hard for it. Multiple viable chokepoints are healthier than
one dominant one.

### FOG OF WAR (MAP)
**Problem:** Perfect information on a map eliminates exploration tension.
**Solution:** Map reveals progressively — tiles, routes, or node values are face-down
until a player reaches or trades for information about them.
**Implementation:** Nodes have face-down values. Players can explore (reveal a node's
value to themselves) or spy (peek at another's revealed tiles). Information is an asset.
**Examples:** Archipelago (hidden island resources), various war games, app-native hidden
information (trivial to implement on mobile).
**Watch out for:** Hidden information that's asymmetric and unrecoverable — if one player
gets lucky early reveals, they compound the advantage. Give all players ways to catch up
on information.

---

## Event & Chaos Patterns

### MANIA CARD
**Problem:** Bubble formation should emerge from player behavior, but needs an external
trigger to ensure it happens in a finite session.
**Solution:** An event card inflates one commodity's value dramatically for 2-3 rounds,
creating a FOMO window. Players who position before the Mania profit; those who enter late
absorb the crash.
**Implementation:** Mania card names a commodity. Its value multiplies (2x-3x) for N
rounds. A Crash card (in the same deck, revealed later) collapses it. The gap between
Mania and Crash is the risk window.
**Examples:** No single game implements this cleanly — it's an original design opportunity
synthesized from historical tulip mania and The Estates' bubble mechanic.
**Watch out for:** Mania targeting a commodity no one holds (nobody cares) or one player
holds exclusively (feels targeted). Mania should hit a contested commodity to create tension.

### SCANDAL TRIGGER
**Problem:** Corrupt play needs consequences that are mechanically interesting, not just
"you lose points."
**Solution:** Corruption accumulates silently. At a threshold, a Scandal event fires —
visible to all players — triggering immediate mechanical consequences (routes close,
investors flee, a player loses turns to "investigation").
**Implementation:** Each corrupt action adds to a hidden Scandal meter. Other players can
see the meter value but not the source actions. At threshold, the event fires automatically.
**Examples:** Frostpunk (law system threshold events), various social deduction games
(reveal mechanics).
**Watch out for:** Scandal being the dominant outcome for corrupt players (no one
plays corrupt) or never firing (no consequence). Calibrate threshold so Scandal fires
roughly 30-40% of corrupt game-arcs.

### PANIC CASCADE
**Problem:** Bank run / market panic mechanics often feel sudden and arbitrary.
**Solution:** Panic is a two-stage event. Stage 1: a visible warning sign (a Mania card
crashed, a player over-leveraged). Stage 2: triggered by a second condition (player
action or deck event), the cascade fires — multiple nodes lose value simultaneously.
**Implementation:** Stage 1 creates a "Fragile Market" token on the board (visible to
all). While Fragile, certain player actions can trigger Stage 2. Stage 2: all Fragile
commodities drop; players must liquidate.
**Examples:** Container (oversupply crash), 2008 financial crisis as design model.
**Watch out for:** Stage 2 being triggered by one player to punish another specifically
(feels targeted). Cascade should be systemic — everyone suffers together.

---

## Tension & Pacing Patterns

### ERA FLIP
**Problem:** Long games lose tension midway — the leader feels insurmountable.
**Solution:** A mid-game inflection point (Era flip, Season change, Market reset) partially
resets board state. Leaders lose some advantages; new paths open for trailing players.
**Implementation:** At a trigger point (round count, deck exhaustion), a visible reset
occurs. Some assets carry over; others reset. The reset is announced in advance so players
can position for it.
**Examples:** Brass: Birmingham (canal era → rail era), Through the Ages (age transitions),
"This Time Is Different" (Season end with Fleet/Scandal carry-over).
**Watch out for:** Reset that's too complete — players lose everything they built, which
feels punitive. Reset should feel like a new chapter, not a new game.

### RACE THRESHOLD
**Problem:** Players need a clear win condition that creates urgency.
**Solution:** The game ends when the first player reaches a visible threshold (prestige,
fame, points). This creates a race dynamic in the final third — everyone can see the
leader approaching the threshold and must respond.
**Implementation:** Threshold is visible to all players at all times. As one player
approaches it, others have 2-3 rounds to catch up or block. The game ends immediately
when the threshold is hit.
**Examples:** Splendor (15 prestige), Dominion (Province pile depletion), Race for the
Galaxy (12 card tableau).
**Watch out for:** Race being solvable too early (leader reaches threshold in round 5
of 15). Calibrate threshold so the decisive moment comes in the final 20-30% of the
session.

### HUBRIS ARC
**Problem:** Corrupt or aggressive play styles are one-dimensional (always risky, always
punished).
**Solution:** Design a narrative arc where corrupt play is clearly winning in the middle,
then collapses in a legible way. The arc has three acts: setup (corrupt play is working),
peak (player looks unbeatable), collapse (consequences arrive).
**Implementation:** Corrupt actions have compounding short-term benefits (each one makes
the next one more effective). But a threshold triggers consequences that compound in the
opposite direction. The peak is visible — other players should see it coming even when
the corrupt player doesn't.
**Examples:** 1830 (pump-and-dump arcs), Offworld Trading Company (market corner
collapse), Papers Please (complicity escalation).
**Watch out for:** Collapse being invisible until it fires. Other players watching the
arc is half the entertainment — make the Scandal meter or debt pile visible.

---

## Mobile Adaptation Patterns

### VISUAL STATE MACHINE
**Problem:** Complex game states are hard to represent on a small screen.
**Solution:** Every game object has exactly two or three visible states with a clear
visual difference. State transitions are animated (brief, legible). Players always know
the current state of every object at a glance.
**Implementation:** Design states first (inactive / active / exhausted), then design
the visual for each. Never let an object have an ambiguous state. Use color + icon +
position (three independent channels) to communicate state.
**Examples:** Brass Digital (industry tile flip), Splendor mobile (gem count badges),
Ticket to Ride mobile (route color claim).
**Watch out for:** State communicated only by color (colorblind players) or only by
small icons (phone screen legibility). Always use multiple visual channels.

### ASYNC CORE LOOP
**Problem:** Multiplayer strategy games require all players present simultaneously,
limiting mobile play.
**Solution:** Design the core loop so each player's turn is independent and can be
taken at any time within a window. Notification triggers bring players back to the
game.
**Implementation:** Each turn is a complete unit — player sees current state, makes
decision, submits. Next player is notified. No real-time dependency. Session length
becomes irrelevant — the game completes over hours or days.
**Examples:** Chess.com, Through the Ages Digital, Words With Friends.
**Watch out for:** Mechanics that require simultaneous action or real-time negotiation
(these break async). Redesign such mechanics as sequential offers and counter-offers.

### THUMB RADIUS DENSITY
**Problem:** Mechanics that require comparing two distant areas of the screen simultaneously
fail on mobile.
**Solution:** Design information groupings so all the information needed for a single
decision fits within thumb radius of the action button.
**Implementation:** Audit each decision: what information does the player need? Can
they see it without scrolling or navigating away? If not, either surface it in a panel
near the action, or eliminate the comparison (simplify the decision).
**Examples:** Splendor mobile (gem costs shown directly on card), Ticket to Ride
(route cost shown on tap), Brass Digital (connection preview on hover/tap).
**Watch out for:** Information density that requires the player to hold a mental model
of off-screen state. Mobile UI must externalize memory.
