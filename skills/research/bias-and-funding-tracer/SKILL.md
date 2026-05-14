---
name: bias-and-funding-tracer
description: >
  Trace funding sources, author conflicts of interest, and institutional incentives behind a
  set of sources. Use when source quality alone is insufficient — when "10 sources agree" might
  mean "10 sources funded by the same company agree." Especially load-bearing for biotech
  (industry-funded trials), markets (sell-side analyst incentives), and politically charged
  topics. Plugged into Phase 3 of Spelunker after source-triangulator completes its sweep.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write WebSearch WebFetch
---

# Bias and Funding Tracer — The Provenance Auditor

Source-triangulator confirms whether sources agree. This skill asks the harder question: are they truly independent of the entity that benefits from the agreement? A high-tier source funded by the company whose product it evaluates is not the same as one with no stake in the answer.

## Guiding Principles

1. **Funding is not the same as truth.** Industry-funded research can be correct. But it has a higher prior on motivated conclusions and deserves an independence discount.
2. **Independence is a spectrum, not a binary.** Score it; don't just label it.
3. **Absence of disclosure is itself a signal.** Sources that don't disclose funding get the lowest independence score regardless of what they say.
4. **Trace upstream.** A think-tank report citing a study citing another study — find the original funder.

## How to Run

### Input

A list of sources from `source-triangulator`'s evidence bundle, plus the claim being verified. For each source:
- Title, URL/DOI
- Authors (if known)
- Publishing organization
- Source type (peer-reviewed / institutional / news / blog / etc.)

### Steps

#### Step 1 — Resolve Funding for Each Source

For each source, search for and record:

1. **Direct funding disclosure.** Most peer-reviewed papers have a "Funding" or "Acknowledgments" section. News articles may have a sponsorship or "in partnership with" line. Reports often list funders on the cover page.
2. **Institutional funding.** If the publishing org is a think-tank, university lab, or NGO, identify its top 3 funders (annual report, "Supporters" page, IRS Form 990 for US nonprofits).
3. **Author affiliations.** Each author's primary employer, board seats, consulting relationships, and stock holdings if disclosed.

If funding cannot be found after a reasonable search, mark `funding: undisclosed` — do not assume it's none.

#### Step 2 — Map Stake Relationships

For each funder/affiliation found, ask: does this entity have a financial, regulatory, or reputational stake in the claim being true?

- **Direct stake** — funder makes/sells the thing being evaluated, or directly profits from the outcome
- **Indirect stake** — funder is in the same industry, or competes with an alternative the claim disfavors
- **Regulatory stake** — funder is regulated by an agency the claim affects, or vice versa
- **No identifiable stake** — funding exists but doesn't bear on this specific claim (e.g., a general operating grant)

#### Step 3 — Compute Independence Score (0–10)

Per source:

| Signal | Score adjustment |
|--------|------------------|
| Funding fully disclosed, no stake | +4 baseline |
| Funding fully disclosed, indirect stake | +2 baseline |
| Funding fully disclosed, direct stake | -2 baseline |
| Funding undisclosed | 0 baseline (and tag as such) |
| Authors have personal financial interest in outcome (stock, paid consulting) | -2 |
| Authors are independent academics with no industry ties | +2 |
| Source is a registered preregistration / preregistered analysis | +2 |
| Source is post-publication peer-reviewed (e.g., systematic review of the claim) | +1 |
| Source is a press release, marketing, or sponsored content | -3 |
| Source is from an org with documented prior advocacy on this claim | -1 |

Clip to [0, 10]. Document the calculation per source.

#### Step 4 — Cross-Source Independence Check

After scoring individual sources, examine the SET of sources for the claim:

- Do multiple "independent" sources share a common funder? (e.g., 3 different think-tanks all funded by the same foundation)
- Do they share authors or co-authors on prior work?
- Did they emerge from the same conference, working group, or industry consortium?

If yes, treat the affected sources as effectively ONE source for confidence-tier purposes (per the Confidence Framework's independence definition), and feed this back to evidence-synthesizer for re-tagging.

### Output

An augmented evidence bundle with one entry per source:

```
SOURCE: [title]
  funding: [organization] | undisclosed
  primary_stake: direct | indirect | regulatory | none | unknown
  author_affiliations: [list]
  coi_disclosed: yes | no | partial
  independence_score: [0-10]
  reasoning: [1-2 sentences explaining the score]

CROSS-SOURCE FLAGS:
  shared_funders: [list, if any] — affects: [source IDs]
  shared_authors: [list, if any] — affects: [source IDs]
  effectively_independent_count: [N] (may be lower than total source count)
```

If cross-source flags reduce the effectively-independent count below the threshold for the preliminary confidence tier (3 for Confirmed, 2 for Likely), recommend a downgrade with explicit reasoning.

## Error Handling

**No funding info available for any source:** Tag the entire claim's evidence as `independence: undetermined` and recommend evidence-synthesizer downgrade by one tier.

**Funder structure is opaque (shell orgs, dark money):** Document what you found and what you couldn't trace. Treat as `undisclosed` for scoring.

**Source is too informal to have funding (random blog, social media):** Independence score = 0 by default; rely on source-triangulator's tier rating instead.

## Scope Boundaries

**Does NOT:** Allege wrongdoing or fraud. The skill reports stakes; it does not adjudicate intent.
**Does NOT:** Replace methodological review. A poorly-designed independent study is still poorly-designed.
**Does NOT:** Apply uniform skepticism. Industry funding ≠ wrong; this is a calibration tool, not a dismissal tool.
