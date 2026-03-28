---
name: motion-design
description: >
  Knowledge skill for animation principles, timing, easing, choreography, and motion
  language in digital artifacts. Covers micro-interactions, page transitions, loading
  states, scroll-driven animation, and performance-aware motion patterns. Consult when
  any artifact or design needs movement — from a single hover effect to a fully
  choreographed experience.
---

# Motion Design — The Grammar of Movement

Motion is not decoration. It communicates relationships (this came from there), state (this is loading), hierarchy (look here first), and personality (this feels playful vs. precise). Bad motion is worse than no motion — it creates cognitive noise. Good motion is invisible until you remove it.

## Core Principles

### 1. Motion Has Meaning

Every animation must answer: **what is this movement saying?**

| Purpose | Motion type | Example |
|---------|------------|---------|
| **Spatial continuity** | Transform origin, shared element transitions | Card expands into detail view from its original position |
| **State change** | Fade, morph, color shift | Button transitions from idle → loading → success |
| **Attention direction** | Scale pulse, entrance animation, parallax | New notification slides in from the edge |
| **Relationship** | Staggered entrance, coordinated movement | List items animate in sequence (parent → children) |
| **Personality** | Easing curve choice, overshoot, bounce | Playful UI uses spring physics; serious UI uses cubic bezier |
| **Feedback** | Micro-interaction, haptic metaphor | Button depresses on press, element resists then snaps |

If you can't articulate what a motion communicates, remove it.

### 2. Timing Is Everything

**Duration guidelines:**

| Context | Duration | Why |
|---------|----------|-----|
| Micro-interaction (hover, press) | 100–200ms | Must feel instant, below conscious attention threshold |
| State transition (toggle, tab switch) | 200–350ms | Noticeable but not sluggish |
| Entrance/exit animation | 300–500ms | Needs to be readable but not slow |
| Page/view transition | 400–700ms | Complex spatial change needs time to parse |
| Decorative/ambient | 1000ms–∞ | Background movement should be slow, hypnotic |

**The critical window:** 200–500ms is where most UI animation lives. Below 150ms, motion is subliminal. Above 700ms, motion feels sluggish. Ambient motion is the exception — it operates on a different perceptual channel.

### 3. Easing Is Character

The easing curve defines personality more than any other motion property.

**Core curves:**

- **ease-out** (decelerate) — the workhorse. Elements arrive with energy and settle. Feels natural for entrances. `cubic-bezier(0, 0, 0.2, 1)`
- **ease-in** (accelerate) — for exits. Elements gather speed as they leave. Rarely used alone. `cubic-bezier(0.4, 0, 1, 1)`
- **ease-in-out** (S-curve) — for position changes where start and end are both visible. `cubic-bezier(0.4, 0, 0.2, 1)`
- **linear** — mechanical, robotic. Use for progress bars, loading indicators, continuous rotation. Never for UI transitions.
- **spring** — organic, alive. Overshoots and settles. Playful personality. `spring(mass, stiffness, damping)`

**Advanced curves:**

- **Anticipation** — small reverse movement before the main action (pull back before launching)
- **Follow-through** — elements continue slightly past their target then settle back
- **Overshoot** — intentional overshooting for energetic, bouncy feel

Read `references/easing-recipes.md` for specific curve values mapped to personality types.

## Choreography

### Staggering

When multiple elements animate, stagger their timing to create visual rhythm:

- **Cascade stagger** — fixed delay between each element (40–80ms). Creates a waterfall effect. Good for lists.
- **Distance stagger** — delay proportional to distance from a focal point. Creates a ripple. Good for grids.
- **Group stagger** — groups of elements animate together, with delays between groups. Creates sections.

**Rule:** Total stagger duration should not exceed the individual animation duration. If each item takes 300ms and you have 10 items, stagger by 30ms (not 300ms) to keep the total under 600ms.

### Orchestration

Complex transitions coordinate multiple movements:

1. **Exit first, enter second** — remove old content before introducing new (prevents visual collision)
2. **Shared elements bridge** — if an element exists in both states, it morphs continuously (doesn't exit/enter)
3. **Container first** — animate the container, then its contents (establishes spatial context)
4. **Focal element leads** — the most important element moves first, supporting elements follow

### Scroll-Driven Motion

Read `references/scroll-animation-patterns.md` for scroll-linked animation techniques.

**Key principle:** Scroll-driven motion should feel like the user is *revealing* content, not *triggering* it. Elements should move in response to scroll position, not play canned animations when they enter the viewport.

## Performance

### The 60fps Contract

Motion must maintain 60fps. Dropped frames destroy the illusion of fluidity.

**GPU-accelerated properties (safe to animate):**
- `transform` (translate, scale, rotate)
- `opacity`
- `filter` (blur, brightness — with caution on mobile)

**Layout-triggering properties (expensive, avoid animating):**
- `width`, `height`, `top`, `left`, `margin`, `padding`
- `font-size`, `border-width`

**Compositing properties (use sparingly):**
- `will-change` — declare before animation starts, remove after
- `contain` — limit paint/layout scope

### Reduced Motion

Always respect `prefers-reduced-motion`:
- Replace motion with instant state changes or simple fades
- Never remove information that was communicated through motion — find a static alternative
- Ambient/decorative motion should stop entirely

## When to Consult This Skill

- Choosing animation for an artifact's entrance, transitions, or interactions
- Deciding between CSS transitions, CSS animations, WAAPI, or JS animation
- Setting timing and easing for any motion
- Choreographing multi-element sequences
- Optimizing animation performance
- Building scroll-driven experiences
