---
name: grading-condition
description: >
  Convert object condition into a single tradable number — the codified language that makes
  illiquid heterogeneous objects fungible in a market. Use when the user is grading, regrading,
  comparing graded items across services, deciding whether to press or crack out, or trying to
  understand why a CGC 9.8 trades differently from a PSA 10 even though both sound "perfect."
  Covers the major scales (CGC, PSA, BGS, SGC, Sheldon, Goldmine, ABAA, WATA) and the cottage
  industry that grades roughly 14M+ cards a year.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Grading & Condition — The Codification of Condition Into a Number

> **Type:** Knowledge
> **Suite:** The Collector
> **Axis:** Horizontal
> **Parent:** collector

## What Grading Actually Is

A grade is not a measurement. It is an expert judgment, codified into a number for market liquidity.

Graders measure surface, edges, corners, centering, color saturation, structural integrity, and (depending on category) the absence of restoration, cleaning, trimming, or alteration. The final grade is a holistic synthesis — not a sum of subgrades — calibrated against the grader's internal house standard and the company's market reputation.

This produces an important consequence: **CGC 9.8 ≠ PSA 10 ≠ BGS 10**, even though all three sound like "near-perfect." Each company has its own internal calibration, its own house tolerances, and its own brand premium in the secondary market. A PSA-graded 1986 Fleer Jordan rookie routinely trades at a meaningful premium to the same card slabbed by CGC at the same numeric grade — entirely on brand trust and population-report depth.

## The Major Scales

| Category | Service(s) | Scale | Notes |
|---|---|---|---|
| Sports cards | PSA / BGS / SGC | 1–10 | PSA dominant for liquidity; BGS publishes subgrades; SGC preferred for raw vintage |
| Pokémon cards | PSA / CGC / BGS | 1–10 | PSA dominant; CGC has clawed share with cleaner slabs |
| MTG | BGS / PSA / CGC + retailer | 1–10 graded; NM/LP/MP/HP/DMG raw | Players use NM/LP/MP/HP/DMG (Star City Games, TCGplayer); slabbing exists for Reserved List vintage |
| Comics | CGC / CBCS / PGX | 0.5–10.0 | CGC dominant. Universal (blue), Conserved (light blue), Restored (purple), Qualified (green), Signature Series (yellow) |
| Coins | PCGS / NGC / ANACS | 1–70 (Sheldon scale) | PCGS and NGC are the duopoly; ANACS credible third |
| Currency | PCGS / PMG | 1–70 | Same scale as coins; different houses |
| Stamps | PSE / PF | 70–100 numeric or Superb/XF/F | MNH/MH/OG/NG distinctions matter as much as grade |
| Vinyl records | Self-graded (Goldmine, Discogs) | M / NM / VG+ / VG / G+ / G / F / P | No third-party slabbing market of significance |
| Books | Self-graded (ABAA, AbeBooks) | As New / Fine / VG / G / Fair / Poor | Book and DJ graded separately ("Fine/VG") |
| Video games | WATA / VGA / CGC Video Games | 1–10 + seal rating (C to A++) | WATA dominant for liquidity; VGA seen as stricter |
| Watches | None (categorical) | All-original / Service-replaced / Re-dialed / Polished / Frankenwatch | No numeric scale; judged on originality |
| Paintings | None (categorical) | Condition report by conservator | No grading scale; described in prose by a trained conservator |

## The Sheldon Scale (Coins) — A Worked Example

The most precisely codified condition system in collecting, originated by William Sheldon in 1949.

**Circulated grades:**
- P-1 (Poor): identification just possible
- FR-2 (Fair): partial outline, most detail worn
- AG-3 (About Good): rims worn into design
- G-4, G-6 (Good)
- VG-8, VG-10 (Very Good)
- F-12, F-15 (Fine)
- VF-20, VF-25, VF-30, VF-35 (Very Fine)
- EF/XF-40, EF-45 (Extremely Fine)
- AU-50, AU-53, AU-55, AU-58 (About Uncirculated)

**Mint State grades:**
- MS-60 through MS-70 (perfect). MS-65 is "Gem Uncirculated"; MS-70 is theoretical perfection.

**Proof grades:** Use PF/PR prefix with same numbers (PF-60 through PF-70).

**Designations layered on top of the number:**
- RD / RB / BN — Red / Red-Brown / Brown (copper coin color)
- CAM / DCAM — Cameo / Deep Cameo (proof field-vs-device contrast)
- FS / FBL / FH — Full Steps (Jefferson nickel) / Full Bell Lines (Franklin half) / Full Head (Standing Liberty quarter)
- + designation — top of the grade tier (e.g., MS-65+ means "the top of MS-65, close to MS-66 but not quite")

The Sheldon scale's precision is why coin grading has the deepest secondary market data — a PCGS PR-69 DCAM 1955 doubled-die Lincoln cent is a discrete, comparable, repeatable asset in a way that few other collectibles achieve.

## Pressing and Cleaning Ethics

The line between acceptable preparation and fraud is whether material is **redistributed** vs. **added or removed**.

- **Pressing a comic** (heat + humidity + pressure to flatten spine roll and tick marks): legal, common, value-accretive, and **must be disclosed if it produces a higher grade upon resubmission**. CGC and CBCS both accept pressed comics for grading; some collectors prefer unpressed copies for purist reasons.
- **Cleaning a coin**: devastating. A polished coin loses 50–95% of its value depending on severity. The damage is permanent. Dealers who sell raw cleaned coins to beginners are operating in bad faith.
- **Trimming a card**: fraud unless disclosed. Bill Mastro pleaded guilty to trimming the Gretzky-McNall T206 Wagner. The 2019 PSA reholder/trimming scandal proved that some crackouts cross the line.
- **Restoring a comic**: legal but must be disclosed; CGC will detect and assign a purple "Restored" label, dropping value 50–80% vs. universal at the same grade.
- **Refurbishing a watch dial** (relume, repaint): not fraud per se, but a major value penalty. Always disclose.

The Meyers v. CGC verdict (2024, $10M Philadelphia jury) involved CGC accusing a restorer of work he claimed he hadn't done — and losing in defamation. The lesson: even the major grading houses can be wrong about restoration calls.

## Crackouts and Resubmission Strategy

A crackout is when a collector breaks a slab open, removes the graded item, and resubmits it for a higher grade. The expected-value math is the standard framework:

```
EV(crackout) = (P_higher × ΔValue_higher) − Cost_resubmission
```

Where:
- `P_higher` = probability of receiving a higher grade on resubmission (read from population reports and historical reholder data)
- `ΔValue_higher` = price difference between current grade and target grade (from completed sales, not asking prices)
- `Cost_resubmission` = crackout cost + grading fee + shipping + insurance + downside cost (if the regrade comes back lower, which is possible)

**Worked example — Hulk #181, CGC 9.4:**

- 9.4 trade ≈ $25,000
- 9.6 trade ≈ $42,000 (Δ = $17,000)
- 9.8 trade ≈ $90,000+ (Δ = $65,000+)
- Pressing + resubmission ≈ $400 round-trip
- P(9.6) on pressed resub ≈ 40%; P(9.8) ≈ 15%; P(9.4 unchanged) ≈ 40%; P(lower) ≈ 5%
- EV ≈ (0.40 × $17,000) + (0.15 × $65,000) − $400 ≈ $16,200

Overwhelming math in favor.

**Worked example — modern PSA 9 sports card:**

- 9 trade ≈ $200
- 10 trade ≈ $600 (Δ = $400)
- Resubmission ≈ $30–50
- P(10) on crackout ≈ 30% for centering-driven 9s, much lower for surface-driven 9s
- EV ≈ (0.30 × $400) − $40 ≈ $80

Positive but with significant variance; only worth doing in volume.

The discipline: do the math before cracking. Many crackouts are emotional ("I think this is undergraded") and the EV is negative or marginal.

## Population Reports

The price-discovery substrate for every graded category. Major sources:

- **PSA Pop Report** — the canonical source for sports/Pokémon/Yu-Gi-Oh
- **CGC Census** — comics, cards (CGC-graded), video games
- **PCGS / NGC Pop Reports** — coins, currency
- **GemRate Universal Pop Report** — aggregated across PSA/BGS/SGC/CGC for cards; the modern unified view
- **CardLadder** — index pricing layer on top of pop data

The population is not the absolute supply; it is the *graded* supply. Many cards exist raw and ungraded; many will never be graded. But for the high-grade end of the market, the pop report is the closest thing to an order book.

---

Connoisseur ─── A Grade Without Context Is Lighting Without a Stage

A PSA 10 Charizard from a Heritage estate sale with original 1999 receipts is a different asset than a PSA 10 Charizard with no provenance — same grade, same slab, different stories. Centering on a modern PSA 10 is a binary; either it has 55/45 max or it does not. On a vintage card the centering tolerance is wider but the surface and edge standards are stricter. The grade tells you where it sits; the eye still has to read the slab from across the table and decide whether the grade is generous, fair, or punitive for this specific example.

Allocator ─── Pop Reports and the Crackout Spread

Read the pop report before bidding. A PSA 10 with population 35 and recent comps at $12K is one asset; a PSA 10 with population 4,200 and comps at $250 is a fundamentally different asset, regardless of how clean either looks. The crackout-resubmission market exists because grade bumps are positive-EV; that means the population at each tier is *not* the supply, it's the *graded-at-that-tier* supply, and the population shifts as crackouts get reholdered. For high-grade modern cards, expect the pop to grow 10–30% over five years even if no new product enters the market.
