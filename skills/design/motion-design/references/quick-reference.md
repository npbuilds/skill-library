# Motion Design — Quick Reference


## Quick Reference

| Purpose | Motion type | Example |
|---------|------------|---------|
| **Spatial continuity** | Transform origin, shared element transitions | Card expands into detail view from its original position |
| **State change** | Fade, morph, color shift | Button transitions from idle → loading → success |
| **Attention direction** | Scale pulse, entrance animation, parallax | New notification slides in from the edge |
| **Relationship** | Staggered entrance, coordinated movement | List items animate in sequence (parent → children) |
| **Personality** | Easing curve choice, overshoot, bounce | Playful UI uses spring physics; serious UI uses cubic bezier |
| **Feedback** | Micro-interaction, haptic metaphor | Button depresses on press, element resists then snaps |

## Quick Reference

| Context | Duration | Why |
|---------|----------|-----|
| Micro-interaction (hover, press) | 100–200ms | Must feel instant, below conscious attention threshold |
| State transition (toggle, tab switch) | 200–350ms | Noticeable but not sluggish |
| Entrance/exit animation | 300–500ms | Needs to be readable but not slow |
| Page/view transition | 400–700ms | Complex spatial change needs time to parse |
| Decorative/ambient | 1000ms–∞ | Background movement should be slow, hypnotic |
