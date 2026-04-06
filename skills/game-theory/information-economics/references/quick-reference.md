# Information Economics — Quick Reference


## Quick Reference

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Signaling, education as signal, Spence model, costly signals, separating/pooling equilibria | `signaling-screening` | Classical signaling theory |
| Screening, self-selection, menu design, insurance markets, adverse selection | `signaling-screening` | Screening and adverse selection |
| Principal-agent, moral hazard, incentive contracts, hidden action | `signaling-screening` | Contract theory foundations |
| Lemons problem, market for lemons, quality uncertainty | `signaling-screening` | Adverse selection applications |
| Bayesian persuasion, information design, sender-receiver, optimal signal structure | `bayesian-persuasion` | Modern information design |
| Cheap talk, Crawford-Sobel, strategic communication without commitment | `bayesian-persuasion` | Strategic communication |
| Verifiable disclosure, unraveling, voluntary disclosure | `bayesian-persuasion` | Disclosure theory |
| "Design an information policy for X", "What should the platform reveal?" | `info-designer` | Applied information design |
| Experiment design, A/B testing as information acquisition, value of information | `bayesian-persuasion` + `info-designer` | Information acquisition |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Signaling model says "reveal quality" but persuasion analysis says "conceal" | Distinguish the commitment structure — signaling has no commitment power (sender acts first), persuasion assumes commitment to a signal structure. Different models apply to different real-world settings | The key question is: can the sender commit to an information policy ex ante? |
| Cheap talk says "no information can be transmitted" but screening says "information can be extracted" | Cheap talk assumes costless, unverifiable messages. Screening uses self-selection through costly menus. If the designer can impose costs or make messages verifiable, screening works even when cheap talk fails | The instrument set determines what's achievable |
| Unraveling theorem says "full disclosure" but practice shows partial disclosure | The unraveling result assumes verifiable disclosure, common priors, and that non-disclosure is interpreted as worst-case. Real-world friction (disclosure costs, uncertainty about what others know) breaks unraveling | Unraveling is a benchmark; deviations from its assumptions explain observed partial disclosure |
| Full Bayesian persuasion optimal but infeasible to implement | Simplify — binary signals or finite partitions are often near-optimal and much simpler to implement. Present the theoretical optimum alongside practical approximations | Perfect is the enemy of good in information design |
