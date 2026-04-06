# Mechanism Design — Quick Reference


## Quick Reference

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Auction formats, bidding, revenue maximization, reserve prices, winner determination | `auction-theory` | Auction-specific theory |
| Revenue equivalence, optimal auctions, Myerson's lemma, FCC spectrum, ad auctions | `auction-theory` | Auction design and analysis |
| Stable matching, Gale-Shapley, school choice, kidney exchange, two-sided markets | `matching-markets` | Matching and market design |
| Assignment problems, housing markets, top trading cycles | `matching-markets` | Allocation mechanisms |
| Voting rules, Arrow's theorem, Gibbard-Satterthwaite, social welfare functions | `social-choice` | Social choice theory |
| Strategy-proofness, manipulation, preference aggregation | `social-choice` | Incentive properties of voting |
| "Design a mechanism for X", "How should I structure incentives?" | `mechanism-designer` | Applied mechanism design |
| Revelation principle, VCG, incentive compatibility, individual rationality | `mechanism-designer` first, then relevant theory skill | Core mechanism design concepts applied |
| DAO governance, token incentives, smart contract mechanism design | `mechanism-designer` | Applied — crypto/decentralized |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Auction theory says "use Vickrey" but the setting has budget constraints | Acknowledge impossibility — VCG may not be efficient under budget constraints; explore alternatives (clinching auctions, adaptive reserves) | Standard results assume quasi-linear utility; violations require specialized mechanisms |
| Matching theory says "use DA for stability" but social choice analysis shows it's manipulable for one side | Present the tradeoff — stability vs. full strategy-proofness. Note that TTC achieves strategy-proofness + efficiency but sacrifices stability | Different desiderata may be incompatible; the designer must choose which to prioritize |
| Revenue maximization (auction) conflicts with efficiency (VCG) | Flag the fundamental tradeoff — Myerson optimal auctions maximize revenue but exclude efficient trades; VCG maximizes efficiency but may sacrifice revenue | This is the Myerson-Satterthwaite impossibility in action; no mechanism achieves both simultaneously |
| Fairness criteria conflict with incentive compatibility | Impossibility results win — if a result says you can't have X and Y simultaneously, don't pretend otherwise | Arrow's theorem and GS theorem are hard constraints, not guidelines |
