---
name: visual-perception
description: >
  How human vision processes visual information. Reference when making decisions about
  attention flow, readability, visual weight, motion sensitivity, or why a design feels
  wrong despite following rules. Use when agents need perceptual science behind design choices.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Visual Perception — The Eye

How human vision actually works, and what it means for design decisions. These aren't style rules — they're hardware constraints of the human visual system.

## Attention and Eye Movement

### Pre-Attentive Processing

The brain processes these properties *before conscious attention* — in under 200ms. Use them for instant communication:

- **Color hue** — a red dot among blue dots pops out instantly
- **Size** — one large element among small ones
- **Orientation** — a tilted line among vertical lines
- **Motion** — anything that moves when surroundings are static
- **Enclosure** — a bounded region stands out from unbounded

**Design implication:** If you need something noticed *immediately* (errors, alerts, primary CTA), change a pre-attentive property. Don't rely on reading or spatial position alone.

### What the eye cannot do:**

- **Track more than 4-5 distinct items** in working visual memory (why dashboards with 20 KPIs fail)
- **Compare colors accurately from memory** — colors must be adjacent to compare (why legends far from data points fail)
- **Judge absolute values** — only relative differences (why unlabeled charts fail)
- **Process two focal points simultaneously** — the eye alternates, creating fatigue

### Saccades and Fixations

The eye doesn't scan smoothly — it jumps (saccades) and pauses (fixations). Each fixation captures about 2° of sharp focus (roughly a thumbnail at arm's length). Everything else is peripheral blur.

**Design implication:** Create clear "landing pads" for fixations. Don't spread critical information across the full field — cluster it where the eye naturally fixates (headings, first words of lines, images, high-contrast elements).

## Readability

### Optimal Reading Conditions

- **Line length (measure):** 45-75 characters per line (66 is ideal). Shorter = too choppy. Longer = the eye loses its place on return.
- **Line height (leading):** 1.4-1.6× font size for body text. Tighter for headings (1.1-1.2×). Looser for small text or wide columns.
- **Font size:** 16px minimum for body text on screen. 14px absolute minimum with good contrast.
- **Paragraph spacing:** 0.5-1.0× line height between paragraphs.

### Why ALL CAPS is Harder to Read

Lowercase text has ascenders (b, d, h) and descenders (g, p, y) that create a unique word shape. The brain recognizes word shapes, not individual letters. ALL CAPS removes this shape variation, forcing letter-by-letter processing.

**Use ALL CAPS only for:** very short labels (2-3 words), navigation items, button text. Never for paragraphs.

### Contrast Sensitivity

The eye is far more sensitive to **lightness contrast** than to **hue contrast**. Two different colors with the same lightness are nearly invisible to distinguish at speed.

**Test:** Convert to greyscale. If elements merge, your design has a lightness contrast problem regardless of how colorful it is.

## Visual Weight

Every element has perceived "weight" that affects compositional balance.

### What Makes Things Heavy

| Property | Heavier | Lighter |
|----------|---------|---------|
| Size | Larger | Smaller |
| Color | Darker, more saturated | Lighter, desaturated |
| Texture | Complex, detailed | Smooth, minimal |
| Shape | Irregular, complex | Regular, simple |
| Position | Lower on page | Higher on page |
| Density | Packed, filled | Open, spacious |
| Isolation | Surrounded by whitespace | In a group |

**The isolation effect:** A small element with generous whitespace around it feels heavier than a large element crammed against other elements. This is why a single word centered on a white page feels powerful.

### Balance Types

- **Symmetric:** Equal weight on both sides of center. Feels formal, stable, static. Use for serious/institutional design.
- **Asymmetric:** Unequal elements balanced through position/weight compensation. Feels dynamic, modern, interesting. Use for most design.
- **Radial:** Weight distributed around a center point. Feels focused, contained. Use for medallions, logos, hero sections.

## Color Perception

### Simultaneous Contrast

A color looks different depending on what surrounds it:
- Grey on black looks lighter than grey on white (same grey)
- A color next to its complement looks more saturated
- A warm color next to cool looks warmer (and vice versa)

**Design implication:** Never evaluate a color in isolation. Always test it in context — on its actual background, next to its actual neighbors.

### Color Constancy

The brain compensates for lighting — a white shirt looks "white" in warm indoor light and cool outdoor light, even though the actual reflected wavelengths are very different.

**Design implication:** Colors on screen don't have this benefit — `#FFFFFF` always looks the same. But printed colors shift dramatically under different lighting. Always specify viewing conditions for print work.

### Chromatic Adaptation

Staring at one color for 30+ seconds shifts perception. After staring at red, white looks greenish. After staring at a saturated screen, muted colors look grey.

**Design implication:** Intense color should be used in bursts, not as persistent backgrounds. Users adapt to it and stop seeing it as special.

## Motion Perception

### What Motion Communicates

- **Entry/exit:** Element appearing or disappearing (should have a source/destination)
- **Emphasis:** Drawing attention to a change (pulse, scale, glow)
- **Connection:** Showing that two things are related (shared motion path)
- **Feedback:** Confirming an action happened (button press, form submit)
- **Continuity:** Maintaining spatial context during transitions (slide, morph)

### Motion Thresholds

- **< 100ms:** Perceived as instant. Good for hover states, micro-feedback.
- **100-300ms:** Perceived as responsive. Good for most UI transitions.
- **300-500ms:** Perceived as animated. Good for meaningful transitions (page changes, modals).
- **> 500ms:** Perceived as slow. Only for dramatic/narrative purpose.
- **> 1000ms:** Perceived as broken unless clearly a deliberate animation.

### Motion Sickness and Accessibility

- **Parallax scrolling** triggers motion sickness in ~12% of users
- **Auto-playing animations** cause issues for vestibular disorder sufferers
- **Respect `prefers-reduced-motion`** — always provide a fallback with minimal/no animation
- **Flashing content** (>3 flashes per second) can trigger photosensitive seizures — never do this

## Common Perceptual Traps

1. **The Mona Lisa effect** — centering a face/focal point makes it feel like it's staring at the viewer regardless of position. Use intentionally or avoid.
2. **Banner blindness** — users have learned to ignore anything that looks like an ad (top banners, sidebars, certain sizes/positions). Critical content must not resemble ads.
3. **Change blindness** — users fail to notice changes that happen during a visual interruption (page load, modal open). Don't rely on users noticing that something changed — animate the change or call it out.
4. **Inattentional blindness** — when focused on a task, users literally don't see unrelated elements. Warning messages must interrupt the task flow to be seen.
5. **The Von Restorff effect** — the item that stands out from a group is remembered best. Make the most important thing the most visually distinct.
