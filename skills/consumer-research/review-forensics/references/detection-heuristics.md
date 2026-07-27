# Fake-Review Detection Heuristics

Ensemble thresholds for review-forensics. Evidence base: `research/consumer-research-landscape-2026.md` §1.2-1.3 (hybrid ensembles reach ~93% accuracy vs ~55% human; Fakespot dead July 2025, ReviewMeta unmaintained; successor tools RateBud/SureVett early-stage — RateBud has documented self-astroturfing, so treat third-party scores as one signal, never the verdict).

**Cardinal rule: no single heuristic suffices.** Velocity alone false-positives on legitimately viral products; language alone false-positives on non-native speakers.

## Signal Thresholds

### 1. Review velocity
- **Flag:** >50% of all reviews posted within the most recent 2 weeks of the corpus's lifetime, or a discrete spike (≥10x baseline weekly rate) not explained by launch/holiday/price-drop.
- **Strong flag:** spike composed mostly of 5-star, unverified, short reviews.

### 2. Verified-purchase ratio
- **Flag:** <70% verified among recent reviews (where the platform exposes it).
- **Unchecked:** platform doesn't display verification — do not assume.

### 3. Rating distribution shape
- Genuine corpora trend toward a J-curve (many 5s, some 1s, thin middle).
- **Flag:** manufactured peaks — near-zero 1-2★ on a high-volume product, or a 5★ wall with uniform short texts.
- **Flag:** bimodal split where 5★ are clustered in one date band and 1★ in another (review-bombing or seeding).

### 4. Reviewer-account patterns
- **Flag:** recent accounts (<6 months) dominating; single-review accounts; profiles whose history is all 5★ across unrelated categories on the same dates.
- **Strong flag:** documented seller participation in review brokers / FTC enforcement history (rule effective 2024-10-21).

### 5. Cross-product / template repetition
- **Flag:** same reviewer set across the seller's other products; same-day batches; near-identical phrasing across products ("template" reviews).
- Linguistic AI cues (supporting evidence only, never standalone): hyper-coherent, emotionally flat prose; spec recitation matching the listing copy; absence of concrete usage detail. Do NOT use generic "AI detector" tool verdicts — false-positive rates are too high.

## Verdict Rubric

| Checked signals | Flags | Verdict |
|---|---|---|
| ≥3 | 0 | clean |
| ≥3 | 1 | mixed |
| any | ≥2, or 1 strong flag | suspect |
| <3 | — | unverifiable |

## Consequences for the caller

- `clean` — crowd ratings usable as supporting (never primary) evidence.
- `mixed` — usable directionally; cite the flag in the brief.
- `suspect` — exclude crowd ratings from scoring; note in VERIFICATION & AUTHENTICITY; consider whether the finalist survives on Tier 1-2 evidence alone.
- `unverifiable` — crowd ratings carry zero weight; the product is evaluated on independent testing only.
