# Delegation Rules — Agent Selection Logic

## Single-Domain Routing

When the project clearly maps to one domain, launch that domain's agent directly.

**Signal → Agent mapping:**

| User signal | Route to |
|-------------|----------|
| "dashboard", "app", "screen", "interface", "component", "layout" | UI Design Agent |
| "logo", "brand", "identity", "color system", "style guide" | Brand Agent |
| "font", "type", "heading", "text styling", "lettering" | Typography Agent |
| "illustration", "icon", "character", "drawing", "editorial art" | Illustration Agent |
| "chart", "graph", "infographic", "data", "visualization", "metrics" | DataViz Agent |
| "generative", "algorithmic", "p5", "parametric", "procedural" | Generative Art Agent |

## Multi-Domain Routing

Many projects span domains. Launch agents in dependency order:

### Typical sequences:

**Brand project:** Brand Agent → Typography Agent → Illustration Agent
- Brand sets palette and personality → Type reinforces it → Illustration extends it

**Dashboard project:** DataViz Agent → UI Design Agent → Typography Agent
- Data encoding comes first → UI wraps it → Type polishes hierarchy

**Website/App:** Brand Agent → Typography Agent → UI Design Agent → Illustration Agent
- Brand foundation → Type system → Component design → Visual assets

**Presentation:** Graphic Design (via orchestrator) → DataViz Agent → Typography Agent
- Layout grid → Chart styling → Type hierarchy

**Generative art project:** Generative Art Agent (standalone, may consult Typography Agent for overlays)

## When NOT to Delegate

Handle directly in the orchestrator (no sub-agent needed) when:
- The user needs a quick palette suggestion (just provide 5-6 hex values with rationale)
- The decision is purely about mood/direction and doesn't require detailed specification
- The user is exploring options and needs a conversation, not a deliverable

## Context Threading

When launching sequential agents, pass a **Creative Context Block** to each:

```
CREATIVE CONTEXT
────────────────
Brief: [1-2 sentence project summary]
Palette: [hex values or mood description]
Typography: [font choices or direction, if established]
Mood anchors: [3-5 adjectives]
Anti-patterns: [what to avoid]
Prior decisions: [summary of what earlier agents established]
```

This ensures each agent inherits the creative decisions of prior agents.

## Escalation

If a sub-agent's output conflicts with the creative brief:
1. Identify the specific mismatch (color? tone? density?)
2. Re-launch with the constraint explicitly tightened
3. If conflict persists after re-launch, present both options to the user and let them decide
