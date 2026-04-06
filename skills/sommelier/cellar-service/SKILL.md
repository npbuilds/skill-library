---
name: cellar-service
description: >
  Route wine service and cellar management questions to the correct specialist
  knowledge. Use when the user wants to know how to serve, decant, or store a
  wine correctly, understand professional service protocol, assess whether a
  wine is ready to drink, or manage a wine collection with appropriate storage
  conditions and drinking windows.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Cellar & Service — The Butler

**Type:** Director
**Suite:** Bacchus

## Description
Orchestrates everything that happens to a wine after it leaves the producer and before it reaches the glass. Routes between service execution (temperature, decanting, glassware, opening technique, formal protocol) and cellar stewardship (storage conditions, drinking windows, collection management, provenance). Ensures wine is served in the condition that honors both the producer's intention and the guest's investment.

## Routing Table

| Trigger | Route To | Notes |
|---|---|---|
| Serving temperature, decanting decisions, glassware selection, opening technique, formal restaurant protocol | service-protocol | The execution layer — what to do and how to do it |
| Storage conditions, drinking windows, cellar organization, buying strategy, provenance | cellar-management | The stewardship layer — how to protect and plan |
| Any question about wine condition, faults, or whether a wine is still good | Escalate to tasting-evaluation | Out of scope — requires sensory assessment |
| "Is this wine ready to drink?" | cellar-management (primary) + tasting-evaluation if bottle is in hand | cellar-management handles the window; tasting-evaluation handles the actual bottle |

## Multi-Skill Scenarios

### "How should I serve this 1996 Barolo?"
Both skills activate in sequence:
1. **cellar-management** first: assess the drinking window. A 1996 Barolo is approximately 30 years old — is it within its window, past it, or still developing? Drinking window for Barolo of this era from quality producers: typically 15-30+ years, putting 1996 in a mature, possibly late-window position. Confirm the wine is not over the hill before advising on service.
2. **service-protocol** second: once cellar-management confirms the wine is serviceable, generate service advice — stand the bottle 24 hours minimum, use an Ah-So or Durand for a potentially fragile cork, candle-decant to separate sediment (do NOT aerate aggressively — old Barolo falls apart with too much air), serve at 17-18°C, large-bowled Burgundy-style glass to concentrate the delicate tertiary aromatics.

### "What temperature should I serve Champagne?"
- **service-protocol** handles solo: NV Brut at 6-9°C (sacrifices nothing), Vintage/Prestige cuvées at 9-11°C (the additional 2-3°C unlocks complexity that over-chilling destroys). No cellar-management needed — straightforward service question.

### "I have a case of 2018 Brunello — when should I open the first bottle?"
- **cellar-management** handles solo: drinking window analysis for Brunello di Montalcino 2018 vintage (a strong vintage), peak window estimation, first bottle recommendation vs. peak window recommendation, storage guidance for the remaining case.

## Curriculum Order
1. **service-protocol** first: immediate practical value. Most users need to know how to serve a wine tonight before they need to know how to build a 10-year cellar.
2. **cellar-management** second: the longer view. Once service fundamentals are in place, learning how to steward a collection across time.

## Conflict Resolution
**When a wine needs decanting but the host or guest is impatient:**
- Always prioritize the wine's integrity over convenience — but offer alternatives rather than simply refusing.
- **Option 1:** Coravin one glass directly and let the rest continue to evolve in the sealed bottle. The first glass may be slightly reductive; subsequent glasses over 30-60 minutes will open.
- **Option 2:** Brief splash decant into a warmed decanter (10-15 minutes) rather than full extended aeration. Not ideal, but meaningfully better than serving directly from the bottle with no air.
- **Option 3:** Pour one taste glass now, let it sit in the glass for 10-15 minutes while beginning the meal. The glass itself provides sufficient aeration for an initial taste.
- Never tell a host "just wait" without offering a practical alternative. The wine's needs and the host's practical constraints must be reconciled, not resolved by fiat.

## Scope Boundaries
- **In scope:** everything from cork removal to decanting to temperature management to cellar organization and acquisition
- **Escalate to tasting-evaluation if:** the question is "is this wine good?", "does this wine have a fault?", or "has this wine peaked?" — these require sensory judgment that goes beyond service and storage protocol
- **Does not cover:** food pairing (route to food-pairing suite), identifying grape varieties (route to deductive-method)
