---
name: type-pairing
description: >
  Typeface pairing methodology — how to combine fonts for harmony, contrast, and hierarchy.
  Covers the contrast principle, superfamily strategy, mood matching, and common pairing
  patterns. Use when selecting fonts for a project that needs more than one typeface.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Type Pairing — Combining Typefaces

The methodology for combining typefaces so they feel intentional, not accidental. Good pairing creates visual hierarchy and personality; bad pairing creates noise.

## The Core Principle: Contrast, Not Conflict

Two typefaces work together when they are **different enough to create contrast** but **share enough DNA to feel harmonious**.

- **Too similar** = no hierarchy, reader can't tell which is heading vs body (e.g., Arial + Helvetica)
- **Too different** = visual clash, feels random (e.g., Bodoni + Comic Sans)
- **Just right** = clear roles, shared visual rhythm (e.g., Playfair Display + Source Sans Pro)

## Pairing Strategies

### Strategy 1: Serif + Sans-Serif (Most Reliable)
The classic approach. Works because the two categories are inherently different yet can share proportions.

**Rules:**
- Match x-heights (most important single factor)
- Serif for headings + sans for body, OR sans for headings + serif for body
- Both should share a similar "era" feel (don't pair a medieval blackletter with a geometric sans)

**Reliable combinations:**
| Heading | Body | Mood |
|---------|------|------|
| Playfair Display (serif) | Source Sans Pro (sans) | Editorial, elegant |
| Montserrat (sans) | Merriweather (serif) | Modern, readable |
| Lora (serif) | Roboto (sans) | Warm, professional |
| Oswald (sans) | EB Garamond (serif) | Bold, literary |

### Strategy 2: Superfamily (Safest)
Use faces from the same type family that includes both serif and sans-serif variants. They're designed to work together.

**Reliable superfamilies:**
- Roboto + Roboto Slab
- Noto Sans + Noto Serif
- IBM Plex Sans + IBM Plex Serif + IBM Plex Mono
- Source Sans Pro + Source Serif Pro + Source Code Pro
- PT Sans + PT Serif + PT Mono

**When to use:** When you want guaranteed harmony, or when the project needs serif, sans, and mono variants (documentation, code + prose).

### Strategy 3: Weight Contrast Within One Family
Use a single typeface but vary weight dramatically for hierarchy.

**Rules:**
- Heading: Bold/Black (700-900)
- Subheading: Medium/SemiBold (500-600)
- Body: Regular (400)
- Caption: Light or Regular at smaller size

**Best for:** Minimal design, brand consistency, when you want the type to recede behind the content.

### Strategy 4: Mood Matching
Choose faces that evoke the same emotional register but express it differently.

| Mood | Heading option | Body option | Why it works |
|------|---------------|-------------|-------------|
| Luxury | Didot (high contrast serif) | Futura (geometric sans) | Both are refined, one ornate and one minimal |
| Friendly | Poppins (rounded sans) | Lora (soft serif) | Both are warm, one geometric and one organic |
| Technical | Space Grotesk (geometric) | JetBrains Mono (mono) | Both are precise, different rhythm |
| Editorial | Playfair Display (display serif) | Inter (neutral sans) | Drama in headings, clarity in body |

## Hierarchy Rules

A well-paired system needs clear roles:

### The Hierarchy Stack
1. **Display** (optional) — Hero headlines, 36px+. Can be expressive.
2. **Heading** — Section titles, 20-32px. Creates structure.
3. **Body** — Main content, 16-20px. Optimized for reading.
4. **Caption/UI** — Labels, metadata, 12-14px. Functional, not decorative.

**Rule of thumb:** You need at most 2 typefaces. One for headings, one for body. Everything else is weight/size variation within those two.

### Size Ratios
Use a typographic scale for consistency:
- **Major Third (1.25)**: 16 → 20 → 25 → 31 → 39
- **Perfect Fourth (1.333)**: 16 → 21 → 28 → 37 → 50
- **Golden Ratio (1.618)**: 16 → 26 → 42 → 67

Pick one scale and stick to it. Don't mix ratios.

## Testing Your Pairing

Before committing, run these checks:

1. **Squint test** — Squint at the layout. Can you still see the hierarchy? If heading and body blur together, contrast is too low.
2. **x-height alignment** — Set both faces at the same pixel size. Do the lowercase letters sit at the same visual height? If not, the pairing will feel mismatched.
3. **Paragraph test** — Set a full paragraph in the body face. Is it comfortable to read for 60+ seconds? If not, switch the body face.
4. **Headline test** — Does the heading face work at both 24px and 48px? Some faces only shine at one specific range.
5. **Brand alignment** — Does the pairing match the project's personality? A law firm shouldn't use the same pairing as a children's app.

## Anti-Patterns

- **Two faces from the same sub-category** — e.g., Helvetica + Arial (no contrast)
- **Display face for body** — decorative types break at small sizes
- **More than 2 families** — unless you're using a superfamily with serif+sans+mono
- **Ignoring x-height mismatch** — the #1 cause of pairings that "feel off"
- **Choosing by name recognition** — "I've heard of Futura so I'll use it" without checking if it fits
- **Pairing two "loud" faces** — one face should be quiet (body) so the other can be expressive (heading)
