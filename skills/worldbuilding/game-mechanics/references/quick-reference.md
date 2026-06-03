# Game Mechanics — Quick Reference


## Quick Reference

| Loop | Timescale | What it does | Failure mode |
|------|-----------|-------------|-------------|
| **Primary** | Per turn | The atomic action — collect, build, spend | Too short: trivial. Too long: exhausting. |
| **Secondary** | Per session | The arc of a match — race to a threshold | Missing: players don't know if they're winning |
| **Tertiary** | Across sessions | Persistence, collection, meta-progression | Missing: no reason to return tomorrow |

## Mobile-Specific Constraints

| Audience Tier | Session Length | Complexity Budget | Async Support |
|--------------|---------------|-------------------|---------------|
| Casual | 5-15 min | Low — one core loop | Optional |
| Mid-core | 20-35 min | Medium — 2-3 systems | Important |
| Hardcore | 45-90 min | High — full Euro complexity | Essential |

## Anti-Patterns (Red Flags)

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Kingmaking** | Eliminated player determines winner | Remove elimination; use point-loss instead |
| **Runaway Leader** | Leader wins from round 3 | Add structural catch-up (more options for trailing players) |
| **Feel-Bad Randomness** | Players blame luck, not choices | Semi-transparent decks; foreshadow random events |
| **Negotiation Dependency** | Game is boring with AI | Make markets systemic, not social |
| **Complexity Creep** | Sessions exceed target length | Audit every rule for primary-loop contribution |
| **Simulation Trap** | Game is realistic but slow | Abstract ruthlessly; fun over fidelity |
| **Crash as Punishment** | Crash events end player agency | Crashes must be recoverable; never eliminate |
| **Obvious Corruption** | Corrupt track is always optimal | Calibrate so honest play is viable long-term |
