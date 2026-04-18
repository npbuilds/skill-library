---
name: design-orchestrator
description: >
  Orchestrate artistic design decisions across visual projects. Use when the user needs
  design direction, style choices, color palettes, typography decisions, composition guidance,
  or visual identity work. Activates when artistic or aesthetic judgment is needed for any
  visual output — UI mockups, illustrations, branding, data visualizations, presentations,
  or generative art.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Art Design Orchestrator — The Creative Director

Route artistic design problems to the right specialist and ensure cohesive visual output. Analyze context, classify the design domain, set creative direction, and delegate to domain-specific agents.

## Phases

### Phase 1 — Understand the Brief

Gather design context before making any decisions:

- **What** is being designed? (UI, logo, illustration, dashboard, presentation, generative art, etc.)
- **Who** is the audience? (end users, stakeholders, general public, specific demographic)
- **Where** will it live? (screen, print, projection, web, mobile, physical space)
- **What mood/tone?** (playful, corporate, elegant, bold, minimal, warm, technical)
- **Constraints?** (brand guidelines, accessibility requirements, color restrictions, existing design system)

If the user provides a brief like "make this look good" or "design something for X", infer reasonable defaults and confirm the creative direction before proceeding.

### Phase 2 — Classify and Route

Determine which design domain(s) apply. A project may span multiple domains — pick the primary and note supporting domains.

Read `references/style-taxonomy.md` for the full domain catalog.

**Domain routing summary:**

| Domain | Activates when | Primary concern |
|--------|---------------|-----------------|
| Modern / Contemporary | Minimalist, clean, current trends | Restraint, whitespace, bold simplicity |
| Classic / Traditional | Timeless, formal, ornamental | Proportion, symmetry, richness |
| Graphic Design | Layouts, posters, editorial, print | Visual hierarchy, grid, type/image balance |
| Product Design | Physical or digital product surfaces | Form-function harmony, material feel |
| UI/UX Design | Interfaces, screens, interactive | Usability-beauty balance, component consistency |
| Brand Identity | Logos, color systems, visual language | Recognition, consistency, emotional tone |
| Typography | Type-driven design, lettering | Pairing, rhythm, scale, readability |
| Illustration | Editorial, character, icon, technical | Style coherence, narrative clarity |
| Data Visualization | Charts, infographics, dashboards | Clarity vs beauty, honest encoding |
| Motion / Animation | Transitions, micro-interactions | Timing, easing, choreography |
| Generative / Algorithmic | Code-driven art, parametric, p5.js | Controlled randomness, emergent aesthetics |
| Spatial / Environmental | Signage, exhibition, wayfinding | Scale, materiality, viewer flow |
| Photography / Composition | Photo direction, styling, grading | Framing, mood, color story |

### Phase 2.5 — Consult Aesthetic Identity

Before setting creative direction, read the user's evolving aesthetic profile:

1. Read `skills/design/aesthetic-identity/references/current-profile.md` for the narrative summary
2. Check `skills/design/aesthetic-identity/references/dimension-registry.md` for specific dimensional positions (17 dimensions across Spatial, Chromatic, Form, Temporal, Emotional, Photographic, Discovered)
3. For photography/visual composition work, also read `skills/design/aesthetic-identity/references/photography-vocabulary.md` for photographic concept → dimension mappings

**How the profile shapes Phase 3:**
- **High-confidence dimensions (>0.7):** pre-populate the Creative Brief with these as defaults. Note them as "from your established aesthetic" so the user knows they can override.
- **Medium-confidence (0.3–0.7):** use as soft suggestions when the user's brief is vague. "You tend toward warm palettes — shall I start there?"
- **Low-confidence (<0.3):** ignore, treat as open territory.
- **If profile is empty:** skip this phase entirely, proceed to Phase 3 with no defaults.

If the user's explicit brief contradicts the profile, **the user's brief wins**. The profile is a gravitational default, not a constraint.

### Phase 3 — Set Creative Direction

Before delegating, establish the design guardrails. Start from the aesthetic identity defaults (if any), then layer in the user's specific brief:

1. **Palette** — select or constrain the color approach
   - Check profile: Temperature, Chromatic Range, Contrast dimensions
   - Specific hex values, or a mood-based range (warm earth tones, cool monochromes, vibrant saturated, muted pastels)
   - Light vs dark dominant
   - Accent strategy (complementary pop, analogous harmony, monochrome + one accent)

2. **Typography direction** — if applicable
   - Check profile: Precision, Temporal Register dimensions
   - Serif/sans-serif/mono/display
   - Weight range (thin and airy vs bold and heavy)
   - Hierarchy levels needed

3. **Composition principles** — spatial organization
   - Check profile: Density, Symmetry, Depth dimensions
   - Grid vs organic flow
   - Density (sparse/minimal vs rich/layered)
   - Focal point strategy

4. **Motion direction** — if applicable
   - Check profile: Motion Feel dimension
   - Consult `skills/design/motion-design/SKILL.md` for easing and choreography
   - Duration range, easing personality, stagger approach

5. **Mood board keywords** — 3-5 adjective anchors that all sub-agents must respect
   - Check profile: mood vocabulary in `current-profile.md`
   - Example: "precise, warm, approachable, modern, grounded"

6. **Photographic direction** — if the output involves photography, visual art, or photographic aesthetic
   - Check profile: Light Character, Substrate/Grain, Atmosphere/Mood dimensions
   - Consult `skills/design/aesthetic-identity/references/photography-vocabulary.md` for vocabulary
   - Light quality and direction (soft/hard, golden/blue hour, rim/backlight)
   - Grain/texture treatment (clean digital, film stock emulation, analog artifacts)
   - Atmospheric conditions (clear, moody, fog, rain, dramatic shadows)
   - Color grading intent (natural, teal/orange, desaturated, warm amber)
   - Genre context (street/documentary, architectural, cinematic/editorial)

7. **Anti-patterns** — what to explicitly avoid
   - Example: "no gradients, no stock photo aesthetic, no rounded corners"

Document these as a **Creative Brief** that gets passed to every sub-agent.

### Phase 4 — Delegate

Use the Agent tool to launch the appropriate specialist agent(s).

Read `references/delegation-rules.md` for agent selection logic.

**Available specialist agents:**

| Agent | File | Model | Use for |
|-------|------|-------|---------|
| UI Design Agent | `agents/ui-design-agent.md` | sonnet | Interface layouts, component styling, responsive design |
| Brand Agent | `agents/brand-agent.md` | sonnet | Logo concepts, color systems, brand guidelines |
| Typography Agent | `agents/typography-agent.md` | sonnet | Font selection, pairing, typographic hierarchy |
| Illustration Agent | `agents/illustration-agent.md` | sonnet | Style direction, illustration briefs, icon systems |
| DataViz Agent | `agents/dataviz-agent.md` | sonnet | Chart styling, dashboard aesthetics, infographic layout |
| Generative Art Agent | `agents/generative-art-agent.md` | sonnet | p5.js sketches, algorithmic patterns, parametric design |

When launching an agent, always pass:
- The creative brief from Phase 3
- The specific deliverable requested
- Any constraints or anti-patterns

For multi-domain projects, launch agents sequentially — each agent receives the output context from prior agents to maintain cohesion.

### Phase 5 — Harmonize and Present

After agent(s) return results:

1. **Consistency check** — do all outputs share the same visual language?
   - Color usage consistent across deliverables
   - Typography choices don't contradict
   - Spacing/density feels unified
2. **Present options** — show the user 2-3 direction options when possible, not just one
3. **Explain the why** — briefly justify key design decisions (this builds the user's design intuition)

### Phase 6 — Observe and Evolve

After the user responds to the output, activate the style-evolution-observer protocol:

1. Read `skills/design/style-evolution-observer/SKILL.md` for the inference protocol
2. Re-read the Creative Brief from Phase 3 to provide the output's dimensional position (palette, density, motion, mood, composition choices)
3. Read the user's behavioral signals (accepted? revised? rejected? praised?)
4. Update the aesthetic-identity profile per the observer's update protocol
5. Log meaningful changes to `skills/design/aesthetic-identity/references/evolution-log.md`

This phase is silent — it happens in the background without interrupting the user's flow. The user sees the result of evolution in future sessions when Phase 2.5 reads an increasingly accurate profile.

## Knowledge Layer

Before making creative decisions, consult the relevant subdomain director. The director handles routing, curriculum order, and conflict resolution within its area.

**Always route through the director first:**

| Subdomain | Director | Consult when |
|-----------|----------|-------------|
| Visual Communication | `skills/design/visual-communication/SKILL.md` | Color, layout, visual hierarchy, readability, accessibility |
| Typography | `skills/design/typography/SKILL.md` | Font selection, type pairing, responsive scaling, typographic hierarchy |
| Brand Identity | `skills/design/brand-identity/SKILL.md` | Brand strategy, visual identity systems, voice and tone, positioning |

The director will determine which knowledge skills to load and in what order. Do not load knowledge skills directly — the director applies conflict resolution rules (e.g., perception > principles > color) that ensure consistent advice.

**Direct knowledge skill paths** (for reference — prefer routing through the director):

| Knowledge Skill | Path |
|----------------|------|
| Color Theory | `skills/design/visual-communication/color-theory/SKILL.md` |
| Design Principles | `skills/design/visual-communication/design-principles/SKILL.md` |
| Visual Perception | `skills/design/visual-communication/visual-perception/SKILL.md` |
| Motion Design | `skills/design/motion-design/SKILL.md` |
| Illustration Direction | `skills/design/illustration-direction/SKILL.md` |

**Aesthetic identity layer** (consult before setting creative direction):

| Skill | Path | Purpose |
|-------|------|---------|
| Aesthetic Identity | `skills/design/aesthetic-identity/SKILL.md` | User's evolving style profile |
| Style Evolution Observer | `skills/design/style-evolution-observer/SKILL.md` | Post-output feedback inference |

Pass subdomain director paths to sub-agents in the Creative Context Block so they can consult the routing layer as needed.

**Deep references** (progressive disclosure within knowledge skills):
- `skills/design/visual-communication/color-theory/references/cultural-color-meanings.md` — for international/cross-cultural projects
- `skills/design/visual-communication/color-theory/references/palette-recipes.md` — reusable palette construction patterns
- `skills/design/visual-communication/design-principles/references/composition-patterns.md` — spatial arrangement patterns (F-pattern, Z-pattern, etc.)
- `skills/design/visual-communication/visual-perception/references/accessibility-vision.md` — color blindness, low vision, motion sensitivity

## Failure Recovery

- If a sub-agent returns output that contradicts the creative brief, re-launch with tighter constraints
- If the user rejects a direction, ask which specific elements feel wrong (color? layout? tone?) rather than starting over
- If multiple domains conflict (e.g., data viz clarity vs brand aesthetic), prioritize function over decoration and flag the tradeoff

## Scope Boundaries

This orchestrator handles **design direction and aesthetic decisions**. It does NOT:
- Write production CSS/code (delegate to implementation skills)
- Generate final assets (it produces briefs, specifications, and direction)
- Make accessibility compliance decisions (flag for the user, defer to WCAG guidelines)
