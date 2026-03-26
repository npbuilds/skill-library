# Graph Rendering Rules

## Characters

| Char | Meaning |
|------|---------|
| `─` | Horizontal edge |
| `│` | Vertical edge |
| `┌` | Top-left corner |
| `┐` | Top-right corner |
| `└` | Bottom-left corner |
| `┘` | Bottom-right corner |
| `├` | Left tee (branch) |
| `┤` | Right tee |
| `┬` | Top tee |
| `┼` | Cross |
| `▼` | Arrow down (depends_on direction) |
| `▶` | Arrow right |
| `◄` | Back-reference (already visited) |

## Layout Algorithm

1. **Find roots**: Skills with empty `depends_on` — these go at the top
2. **Assign levels**: BFS from roots. Each skill's level = max(parent levels) + 1
3. **Order within level**: Sort by number of dependents (most connected first)
4. **Draw edges**: Vertical lines from parent to child, with branch characters
5. **Cycle detection**: If a node is visited twice during BFS, mark with `◄ (cycle!)`

## Formatting

- Skill names left-aligned within their level
- Composite scores shown in parentheses after name: `skill-name (97)`
- Health status shown as prefix when unhealthy: `⚠ skill-name (45)`
- Max width: 80 characters (wrap or abbreviate if needed)
- Use `━` for section borders, `─` for internal separators

## Compact Mode

For networks with 10+ skills, use a compact adjacency list instead of the full graph:

```
skill-registry     → (none)                    ← health, dashboard, scaffold, test, analyze
skill-health       → registry, dashboard       ← scaffold
skill-dashboard    → registry                  ← health, scaffold
skill-scaffold     → registry, health, dash    ← (none)
```
