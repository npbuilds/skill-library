# Signal Catalog

Extended reference for mapping user behaviors to dimensional updates. The SKILL.md contains the core inference protocol; this reference expands on edge cases and compound signals.

## Compound Signals

Some behaviors affect multiple dimensions simultaneously:

| Behavior | Dimensions | Interpretation |
|----------|-----------|----------------|
| "Make it more elegant" | Density → Sparse, Precision → Mechanical, Emotional Register → Serious | Elegance = restraint + precision + dignity |
| "More energy" | Motion Feel → Kinetic, Contrast → Bold, Density → Rich | Energy = movement + impact + abundance |
| "Cleaner" | Density → Sparse, Precision → Mechanical, Depth → Flat | Clean = less stuff + crisp edges + no shadows |
| "More organic/natural" | Geometry → Organic, Precision → Expressive, Depth → Dimensional | Natural = curves + imperfection + layering |
| "More modern" | Temporal Register → Futuristic, Geometry → Geometric, Density → Sparse | Modern = contemporary + geometric + minimal |
| "Cozy/warm" | Temperature → Warm, Contrast → Muted, Emotional Register → Playful | Cozy = warm palette + soft contrast + approachable |
| "Professional" | Emotional Register → Serious, Precision → Mechanical, Symmetry → Symmetric | Professional = restrained + precise + balanced |

## Silence as Signal

When the user accepts output without comment, the signal interpretation depends on context:

- **First output in a new direction**: weak positive (they didn't reject it, but may be reserving judgment)
- **Output aligned with profile**: moderate positive (confirms existing preferences)
- **Output that deviated from profile**: strong positive (they accepted something outside their comfort zone — potential drift)

## Revision Specificity

The specificity of a revision request indicates how confident the user is about what they want:

- **Vague**: "I don't love it" → weak negative on all dimensions, wait for clarification
- **Directional**: "Make it warmer" → clear signal on Temperature dimension
- **Precise**: "Change the accent to #E87040 and increase the letter-spacing" → very strong signal, high confidence update

## Reference Signals

When the user references external work:

1. Capture the reference in `influences.md`
2. Analyze which aesthetic qualities they're pointing at
3. Map those qualities to dimensions
4. Weight: references carry moderate signal (the user may like some qualities but not all)

## Anti-Pattern Detection

Watch for signals that the user is fighting the profile:

- Consistently overriding the same dimension's default → profile may be wrong, investigate
- Requesting opposite directions in consecutive outputs → dimension may be context-dependent, not a fixed preference
- "I usually like X but not here" → project-specific override, don't update the global profile
