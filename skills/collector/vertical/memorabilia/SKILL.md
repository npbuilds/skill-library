---
name: memorabilia
description: >
  Route memorabilia and autograph questions — sports autographs (PSA/DNA, JSA, BAS), game-used
  and game-worn (photo-matched, team-letter, player-issued), and pop-culture memorabilia (props,
  costumes, signed music/film items). Activate when authenticating signatures, game-used items,
  or pop culture provenance.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Memorabilia — Director

> **Type:** Director
> **Suite:** The Collector
> **Axis:** Vertical
> **Parent:** collector

## Scope

Memorabilia (with autographs as a major sub-category) is a market built on authentication. An unauthenticated signed item is treated as decoration; an authenticated item by a recognized body trades at 2-5× the unauthenticated value. The Big Three authenticators are **PSA/DNA**, **JSA (James Spence)**, and **BAS (Beckett Authentication Services)**.

## Routing

| Signal | Leaf | Cross-Axis |
|---|---|---|
| Autographs (sports, entertainment, historical) | `autographs` | `horizontal/authentication-provenance`, `horizontal/fraud-intelligence` |
| Game-used / game-worn jerseys, equipment, balls | `game-used` | `horizontal/authentication-provenance` |
| Film/TV/music props, costumes, signed items | `pop-culture` | `horizontal/authentication-provenance` |

## The Authentication Tiering

Authentication for memorabilia comes in tiers of trust:

1. **Witnessed authentication** — authenticator was physically present when the signature was given or the item was created/used. The premium tier. PSA/DNA, JSA, BAS all maintain witnessed-authentication programs at major events.
2. **Opinion-based authentication** — forensic analysis after the fact; comparing the signature to known exemplars. Lower tier; reasonable for established signers; more risk for items by frequently-counterfeited subjects (Mantle, Ruth, Cobb).
3. **Fanatics Authentic** — modern direct-from-athlete program with hologram. The dominant brand for current-player memorabilia.
4. **No major-body authentication** — essentially worthless or actively reducing value.

The user buying any high-value autograph or game-used item should verify authentication through one of the major bodies. eBay COAs from unknown authenticators are typically worthless.

## Cross-Axis

- Authentication → `horizontal/authentication-provenance` (especially for vintage signatures)
- Fraud → `horizontal/fraud-intelligence` (Operation Bullpen FBI investigation; high counterfeit rates for Mantle, Ruth, Cobb)
- Pricing → `horizontal/market-intelligence` (Heritage, Goldin, Lelands, REA)
- Insurance → `horizontal/insurance-risk` (game-used trophy items can be very high value)

---

Connoisseur ─── The Big Three Authenticators Are the Market's Adjudicators

PSA/DNA, JSA, and BAS are not perfect — they have made calls that were later reversed; they have been sued; their opinions are opinions. But they are the market's adjudicators. An item certified by one of the three trades. An item without that certification, however genuine the user believes it to be, does not trade at the same prices. The collector who works within the authentication infrastructure participates in a liquid market; the collector who fights it participates in a private market with limited exits.

Allocator ─── Authentication Adds 200-400 Percent Over Unauthenticated

The premium for major-body authentication is typically 2-5× over the same item without authentication. A signed Mickey Mantle ball with no major authenticator: $200-$800. The same ball with PSA/DNA authentication and a strong grade: $1,500-$5,000+. The math: even if the item is genuinely authentic, the market requires the third-party certification for liquid pricing. Acquire only authenticated items; if buying raw, factor in the cost and uncertainty of obtaining authentication post-purchase.
