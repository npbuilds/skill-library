# Lore Writer — Quick Reference


## Quick Reference

| Voice | Character | Inspired By | Best For |
|-------|-----------|------------|----------|
| **Epistolary** | Intimate, urgent, personal — letters and messages between individuals | This Is How You Lose the Time War | Personal communications, intercepted messages, correspondence |
| **Uncanny** | Clinical precision masking something deeply wrong — the observer can't quite process what they're seeing | Southern Reach, Vandermeer | Phenomena that resist understanding, anomalous locations, things that shouldn't exist |
| **Mythic** | Archetypal, resonant, told from the deep time of a culture — stories that explain how the world works | The Sandman, Tolkien's Silmarillion | Origin stories, religious texts, cultural myths, prophecies |
| **Atmospheric** | Mood over information — what's unsaid matters as much as what's said, fragments and impressions | Cowboy Bebop, fragments | Mood pieces, place descriptions, sensory documents, memories |
| **Clinical** | Detached, analytical, precisely structured — the voice of someone studying the world as a system | Foundation, Death Note, academic papers | Intelligence briefings, scholarly analysis, system documentation, autopsies |
| **Chronicle** | Historical weight, the voice of someone recording events for posterity — shaped by what the chronicler values | Game of Thrones, historical epics | War records, era summaries, political histories, biographical accounts |
| **Visceral** | Felt before understood — the body's knowledge of power, violence, or the supernatural | Jujutsu Kaisen, Attack on Titan | Combat accounts, encounters with the fantasy system, moments of physical extremity |

## Artifact Types

| Type | What It Is | Directory |
|------|-----------|-----------|
| **Region profile** | A place described from inside the world | `artifacts/regions/` |
| **Civilization profile** | A people, their systems, their character | `artifacts/civilizations/` |
| **Historical account** | An event or era as recorded by someone in the world | `artifacts/histories/` |
| **Lore document** | Myths, sacred texts, folk knowledge, oral traditions | `artifacts/lore/` |
| **Intercepted document** | Something not meant for the reader — letters, reports, stolen intelligence | `artifacts/intercepted/` |

## Formula / Pseudocode

```
---
subject: [what this artifact is about]
voice: [which voice register]
perspective: [who in the world wrote/told this]
layer: [0-3, which revelation layer this artifact operates at]
related_axioms: [which world-bible axioms this must be consistent with]
created: [date]
---
```
