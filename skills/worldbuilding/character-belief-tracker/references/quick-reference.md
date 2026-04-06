# Character Belief Tracker — Quick Reference


## Quick Reference

| Field | Description |
|-------|-------------|
| `layer` | 0-3, which revelation layer this character has reached for this subject |
| `belief` | What the character actually thinks is true (may be wrong) |
| `confidence` | How certain they are: high, medium, low, doubting |
| `source` | How they came to believe this (observation, told by X, read in Y, deduced) |

## The Confidence Spectrum

```
CERTAIN ─── CONFIDENT ─── UNCERTAIN ─── DOUBTING ─── QUESTIONING
   │              │            │              │             │
   │              │            │              │             │
"I know this"  "I believe"  "I think"    "Something's   "What if
                                          off"           everything
                                                         I know is
                                                         wrong?"
```

## Formula / Pseudocode

```
voss.beliefs.about(kerrigan).about(origin_of_magic) = Layer 0
  → "Voss thinks Kerrigan believes the official story"

kerrigan.beliefs.about(origin_of_magic) = Layer 2
  → "But Kerrigan actually knows the hidden truth"

This creates dramatic irony:
  → Voss trusts Kerrigan because he thinks they share beliefs
  → Kerrigan is operating with deeper knowledge, unseen by Voss
```
