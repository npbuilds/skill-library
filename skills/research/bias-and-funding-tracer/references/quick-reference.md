# Bias And Funding Tracer — Quick Reference


## Quick Reference

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

## Formula / Pseudocode

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
