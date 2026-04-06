---
name: information-economics
description: >
  Direct the information economics subdomain — route questions about signaling, screening,
  adverse selection, moral hazard, Bayesian persuasion, information design, cheap talk,
  and strategic communication to the right specialist skill. Use when asymmetric information
  drives the strategic interaction.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Information Economics Director — The Cryptographer

The department head for information economics within the game-theory domain. Information economics studies what happens when different players know different things — and how they strategically acquire, reveal, withhold, or distort information. Routes questions to the right specialist, defines the learning order, and resolves conflicts between information paradigms.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

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

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:

1. `signaling-screening` — establish the information asymmetry structure
2. `bayesian-persuasion` — analyze how information can be optimally revealed or concealed
3. `info-designer` — apply to the specific design problem

This order ensures the fundamental asymmetry is understood before the communication/design layer.

**Example multi-skill question**: "Should a startup reveal its financials to investors?"
1. `signaling-screening` → Understand the signaling game: high-quality startups want to separate from low-quality; revealing financials is costly for weak startups
2. `bayesian-persuasion` → Analyze what partial disclosure is optimal — reveal some metrics but not others
3. `info-designer` → Produce a concrete disclosure strategy with commitment analysis

## Curriculum Order

For learning or progressive loading:

1. **Signaling & Screening** (foundation) — The classical paradigm. Spence signaling, Rothschild-Stiglitz screening, the lemons problem, and moral hazard. These models established that information asymmetry fundamentally changes market outcomes.

2. **Bayesian Persuasion** (modern theory) — The revolution. Kamenica & Gentzkow (2011) showed that information itself can be designed as a strategic instrument. Extends from cheap talk through verifiable disclosure to full Bayesian persuasion.

3. **Info Designer** (application) — Apply the theory: design disclosure policies, rating systems, recommendation algorithms, and information revelation strategies.

### Level Progression
- **Foundational**: Signaling & Screening
- **Intermediate**: Bayesian Persuasion, Cheap Talk
- **Advanced**: (future) Dynamic Information Design, Information Design in Networks, Robust Information Design

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Signaling model says "reveal quality" but persuasion analysis says "conceal" | Distinguish the commitment structure — signaling has no commitment power (sender acts first), persuasion assumes commitment to a signal structure. Different models apply to different real-world settings | The key question is: can the sender commit to an information policy ex ante? |
| Cheap talk says "no information can be transmitted" but screening says "information can be extracted" | Cheap talk assumes costless, unverifiable messages. Screening uses self-selection through costly menus. If the designer can impose costs or make messages verifiable, screening works even when cheap talk fails | The instrument set determines what's achievable |
| Unraveling theorem says "full disclosure" but practice shows partial disclosure | The unraveling result assumes verifiable disclosure, common priors, and that non-disclosure is interpreted as worst-case. Real-world friction (disclosure costs, uncertainty about what others know) breaks unraveling | Unraveling is a benchmark; deviations from its assumptions explain observed partial disclosure |
| Full Bayesian persuasion optimal but infeasible to implement | Simplify — binary signals or finite partitions are often near-optimal and much simpler to implement. Present the theoretical optimum alongside practical approximations | Perfect is the enemy of good in information design |

**General rule**: The commitment assumption is the master switch. With commitment → persuasion framework. Without commitment → signaling/cheap talk framework. Always identify the commitment structure first.

## Scope Boundaries

**This director handles**: All questions where asymmetric information is the central strategic element — signaling, screening, adverse selection, moral hazard, persuasion, disclosure, cheap talk, and information design.

**Escalate to the orchestrator when**:
- The question is about strategic interaction with complete information → Strategic Foundations
- The question is about designing allocation rules (not information rules) → Mechanism Design
- The question involves evolving populations, not informed agents → Evolutionary Dynamics
- The question is about computational complexity of information processing → Computational Strategy

## Cross-Domain Connections

- **Investing/reflexivity-sentiment**: Corporate disclosure, earnings guidance, and sell-side research are information design problems. Companies and analysts strategically reveal information to influence market beliefs — the commitment structure determines whether it's persuasion (binding guidance) or cheap talk (non-binding forecasts).
- **Investing/special-situations/insider-signals**: Insider transactions are costly signals in a Spence signaling framework. Filing requirements make the signal verifiable; capital at risk makes it costly. Information economics provides the theoretical foundation for reading insider behavior.
- **Investing/value-quality/second-level-thinking**: Adverse selection in equity markets — cheap stocks may be "lemons." Second-level thinking asks whether the market's discount reflects genuine information asymmetry or mispricing.
