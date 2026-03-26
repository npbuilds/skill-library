---
name: design-principles
description: >
  Core visual design principles for evaluating and improving compositions. Use to assess
  layout quality, diagnose why a design feels wrong, establish visual hierarchy, or apply
  foundational rules like Gestalt, contrast, alignment, and proximity.
---

# Design Principles — The Foundation

Universal principles that govern why visual compositions work or fail. These apply across every design domain — UI, print, illustration, environmental, data visualization.

## The Four Pillars

Every effective design demonstrates mastery of these four properties simultaneously.

### 1. Contrast

The difference between elements that creates visual interest and hierarchy.

**Types of contrast:**
- **Size**: large vs small (most powerful hierarchy tool)
- **Weight**: bold vs light (typographic hierarchy)
- **Color**: dark vs light, saturated vs muted, warm vs cool
- **Shape**: geometric vs organic, angular vs curved
- **Density**: packed vs sparse, detailed vs minimal
- **Direction**: horizontal vs vertical, static vs diagonal

**The rule:** If two things are not the same, make them *very* different. Small differences look like mistakes. A heading that's 16px when body is 14px isn't contrast — it's a typo. Make it 24px or 32px.

**Diagnostic:** If a design feels flat or boring, it almost always lacks contrast. Find the most important element and increase its contrast with everything else.

### 2. Alignment

The invisible lines that connect elements and create visual order.

**Types:**
- **Edge alignment**: elements share a left, right, top, or bottom edge
- **Center alignment**: elements share a center axis (use sparingly — weaker than edge)
- **Baseline alignment**: text elements share a typographic baseline
- **Grid alignment**: elements snap to a consistent spatial grid

**The rule:** Every element should have a visual connection to at least one other element. Nothing should be placed arbitrarily. If you can't identify why something is where it is, it's in the wrong place.

**Diagnostic:** Squint at the design. If elements feel scattered or disconnected, draw vertical and horizontal lines through element edges. Misalignment becomes immediately visible.

### 3. Proximity

Related things are close together. Unrelated things are far apart.

**The rule:** The space between elements communicates their relationship. Items in a group should be closer to each other than to anything outside the group. Whitespace between groups should be noticeably larger than whitespace within groups.

**Practical spacing ratios:**
- Within a group: base unit (e.g., 8px)
- Between groups: 2-3× base unit (16-24px)
- Between sections: 4-6× base unit (32-48px)

**Diagnostic:** If a design feels cluttered or confusing, the spacing between unrelated elements is probably too similar to the spacing within groups. Increase the gaps between groups without changing internal spacing.

### 4. Repetition

Consistent visual patterns that create rhythm and unity.

**What to repeat:**
- Colors (use the same palette consistently)
- Typography (same fonts, same size for same-level elements)
- Spacing (consistent margins, padding, gaps)
- Shape language (if buttons are rounded, cards should be too)
- Visual treatments (if one image has a shadow, all images should)

**The rule:** Establish patterns, then follow them relentlessly. Every inconsistency the viewer notices is cognitive load. Repetition is not boring — it's professional.

**Diagnostic:** If a design feels "off" but you can't pinpoint why, look for broken patterns. One element that doesn't match the established rules will feel wrong even to non-designers.

## Gestalt Principles

How the brain organizes visual information into meaningful groups. These are perceptual laws, not style choices — they work on everyone.

### Figure-Ground

The brain separates foreground (figure) from background (ground). Design must make this separation clear.
- Higher contrast = stronger figure
- Smaller area = perceived as figure
- Enclosed area = perceived as figure
- **Problem signal:** if figure and ground compete, the viewer gets confused about what to look at

### Closure

The brain completes incomplete shapes. You can suggest forms with minimal marks.
- Logos use this extensively (negative space logos)
- Dotted lines and partial borders rely on closure
- **Use it:** reduce visual clutter by implying rather than stating

### Continuity

The eye follows smooth paths and lines, even through interruptions.
- Elements along a line or curve are perceived as related
- Reading flow follows continuity (left-to-right, top-to-bottom in Western)
- **Use it:** guide the eye through a composition with implied lines

### Common Fate

Elements moving (or oriented) in the same direction are perceived as grouped.
- Animated elements moving together = one group
- Arrows or chevrons pointing the same way = related items
- **Use it:** in motion design and interactive transitions

### Similarity

Elements that look alike are perceived as grouped, even if spatially separated.
- Same color = related
- Same shape = related
- Same size = related
- **Hierarchy trick:** make the most important thing visually unique (break similarity intentionally)

## Visual Hierarchy

The order in which the eye processes elements. Good hierarchy means the viewer sees the most important thing first without thinking about it.

### Hierarchy Tools (strongest to weakest)

1. **Size** — the largest thing wins
2. **Color/Contrast** — high contrast against surroundings wins
3. **Position** — top-left (Western), center, or isolation
4. **Typography** — bold, uppercase, or different typeface
5. **Imagery** — photos and illustrations beat text
6. **Whitespace** — isolated elements with breathing room feel important
7. **Depth** — shadows, overlaps, z-index create foreground/background

### The Squint Test

Squint until the design blurs. What's still visible? That's your hierarchy. If the wrong thing dominates when blurred, your hierarchy is broken.

### The 3-Second Test

Show someone the design for 3 seconds, then hide it. Ask: "What was that about?" Their answer reveals what your actual hierarchy communicates vs what you intended.

## Compositional Structures

### The Grid

All professional design uses a grid. Not as a prison — as scaffolding.

- **Column grid**: divide the width into equal columns (4, 6, 8, or 12 are standard)
- **Modular grid**: columns + rows create a matrix of modules
- **Baseline grid**: horizontal lines at consistent intervals for text alignment
- **Breaking the grid**: intentional violations create emphasis — but only if the grid is established first

### The Rule of Thirds

Divide the canvas into a 3×3 grid. Place key elements at intersections or along lines. This creates more dynamic compositions than centering everything.

### Visual Weight Distribution

Every element has "weight" based on size, darkness, saturation, and complexity. A balanced composition distributes weight so it doesn't feel like it's tipping to one side.

Asymmetric balance (unequal elements that balance through position and weight) is more dynamic than symmetric balance (mirror image).

## Common Mistakes

1. **Decorating instead of designing** — adding elements to fill space rather than to communicate
2. **Weak hierarchy** — everything at the same visual level, nothing dominates
3. **Inconsistent spacing** — eyeballing instead of using a spacing system
4. **Centering everything** — center alignment is the weakest form; it creates no strong visual edge
5. **Ignoring whitespace** — treating empty space as wasted space rather than a design element
6. **Style without structure** — making things "look nice" without solving the layout problem first
