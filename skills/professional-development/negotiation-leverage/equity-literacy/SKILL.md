---
name: equity-literacy
description: >
  Understand and negotiate equity grants — options vs RSUs vs PSUs, strike price, vesting,
  cliff, refresh, acceleration, dilution, secondary, 409A. Reference when evaluating an
  equity grant, modeling expected value across scenarios, or negotiating equity terms.
  Most senior comp upside lives in equity; getting equity wrong dwarfs getting base wrong.
  Equity literacy is the foundation of every senior negotiation.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Equity Literacy — Where the Real Money Lives

For a senior role at a venture-backed company, the equity grant is often worth more in expected value than the base salary over the role's tenure. Senior MDs frequently under-negotiate equity because they don't understand the components, the levers, or the magnitudes. This skill is the foundational literacy: what each equity instrument is, how to evaluate a grant, what's negotiable, and how dilution works over time.

## Key Concepts

### The Three Main Instruments

| Instrument | What It Is | When You Pay | Typical Use |
|---|---|---|---|
| **ISO (Incentive Stock Option)** | Right to buy shares at strike price | At exercise; tax on spread vs FMV (potentially AMT) | Early-stage startups; tax-favored if held long enough |
| **NSO (Non-Qualified Stock Option)** | Right to buy shares at strike price | At exercise; ordinary income tax on spread | Larger grants beyond ISO limit; non-employee grants |
| **RSU (Restricted Stock Unit)** | Promise of shares (no cost) | At vesting; ordinary income tax | Public companies and many late-stage privates |
| **PSU (Performance Stock Unit)** | RSU contingent on performance metrics | At vesting (if metrics hit) | Senior executive comp at public companies |
| **Restricted Stock** | Actual shares with restrictions | At grant; tax depends on 83(b) election | Founder grants; very early grants |

### Vesting Mechanics

Standard equity vesting at venture-backed companies:

- **Total vesting**: 4 years
- **Cliff**: 1 year (no vesting until 1 year; then 25% vests at the cliff)
- **After cliff**: monthly or quarterly vesting for remaining 3 years
- **Refresh**: At 2.5–3 years tenure, a refresh grant typically vests over a new 4-year schedule

### Acceleration

Acceleration provisions matter when the company is acquired or when the user is involuntarily terminated:

| Type | Definition | When It Triggers |
|---|---|---|
| **Single-trigger** | Vests on a single event | Usually acquisition alone |
| **Double-trigger** | Vests when two events occur | Acquisition AND termination within 12 months |
| **No acceleration** | Default; nothing accelerates | Most standard grants for ICs |

For senior roles, double-trigger acceleration is often negotiable and high-value. Single-trigger is rare except at executive level.

### Strike Price and 409A

For options, the strike price is set by the company's most recent 409A valuation — an independent appraisal of common stock fair market value. Strike-price implications:

- **Lower strike** = less to pay at exercise = more upside per share
- **Strike rises** as the company's valuation grows; later employees get higher strikes
- **Underwater options** = strike higher than current FMV = effectively worthless until growth

When evaluating an offer, ask for the current 409A and the most recent preferred-share price; the gap (often 4–10x) is the upside on day 1.

### Dilution

Equity is denominated in shares; the meaningful number is *percentage of fully-diluted shares*. Dilution happens when the company:

- Raises a new round (issues new preferred shares)
- Adds an option pool refresh
- Issues shares for acquisitions
- Goes public (typical IPO dilution)

A grant of 100,000 shares means nothing without knowing the fully-diluted share count. Always ask: "What's the fully-diluted percentage of this grant?"

For a senior role at a Series B biotech:

| Role | Typical Range (% fully-diluted) |
|---|---|
| Director / Senior Manager | 0.05–0.15% |
| VP / Senior Director | 0.15–0.4% |
| SVP / Head-of | 0.4–1.0% |
| C-suite (CMO, CTO, CFO) | 0.5–2% |
| CEO (non-founder) | 2–5%+ |

These ranges vary by stage, company maturity, and company-specific economics. They are starting points, not benchmarks.

### Expected-Value Modeling

For a senior offer, model expected equity value across scenarios:

| Scenario | Probability (rough) | Outcome |
|---|---|---|
| Company fails | 30–60% (stage-dependent) | Equity worth $0 |
| Modest exit (1–3x post-money) | 20–40% | Equity worth $X |
| Strong exit (5–10x) | 5–15% | Equity worth $5X–$10X |
| Outlier (10x+) | 1–5% | Equity worth $20X+ |

Probability-weighted expected value is the right frame. Don't optimize for the headline number; optimize for the expected value, weighted by what you can stomach if the company fails.

### Secondary Sales

For pre-IPO companies that have grown significantly, "secondary" transactions allow employees to sell some vested equity privately (often during a tender offer organized by the company). For senior employees with significant vested equity, secondary becomes a real liquidity source 4–6+ years in.

### 83(b) Election

When given restricted stock or early-exercising options, an 83(b) election (filed within 30 days) elects to pay ordinary-income tax on the grant value upfront rather than at vesting. For early-stage grants where the FMV is very low, this is usually a no-brainer; for later-stage grants, the calculus is different.

This is genuinely tax advice; consult a CPA familiar with startup equity for any actual decision.

### Common Failure Modes

| Failure | Looks Like | Fix |
|---|---|---|
| Negotiating shares without %-of-fully-diluted | Asking for "more shares" without context | Always ask for and negotiate on % |
| Ignoring strike price | Accepting offer without 409A awareness | Ask for current 409A and recent preferred price |
| No acceleration ask | Accepting standard "no acceleration" terms | At senior levels, double-trigger is often negotiable |
| Ignoring refresh | One-time grant, no refresh discussion | At 2.5+ years tenure, refresh grants matter |
| Optimistic scenario weighting | Modeling assuming success | Weight by realistic failure probability |
| Skipping the CPA conversation | Making 83(b) or exercise decisions without tax advice | Get a startup-equity CPA |

## Self-Coaching Track

**For your situation (MD → biotech VC/operator):**

1. **Build the basic model.** For any equity offer, capture: instrument type, share count, strike (if options), fully-diluted percentage, vesting schedule, acceleration provisions, refresh policy.

2. **Calculate expected value across scenarios.** Even rough numbers — fail / modest / strong / outlier — illuminate whether the equity is meaningful. The headline number alone misleads.

3. **Always ask for the 409A and recent preferred price.** This data is requestable and is critical for evaluating options grants.

4. **Negotiate acceleration explicitly.** At senior levels, double-trigger acceleration is often negotiable. The downside-protection value is real.

5. **Understand dilution dynamics for the company's stage.** A Series B biotech will likely raise 1–2 more rounds before exit; each will dilute. Model the dilution into expected value.

6. **Consult a CPA for any actual exercise / 83(b) decisions.** This is genuinely complex and tax-consequential. Don't DIY.

7. **Cross-load with `investing/archon`** for cap-table mechanics if the equity is at a startup with complex preferred-stock structures.

## Teach / Mentor-Others Track

**When coaching a junior or peer through equity literacy:**

1. **Force the %-of-fully-diluted reframe.** Many mentees evaluate grants in absolute share counts. Reframe: shares are meaningless without the denominator.

2. **The expected-value model is high-leverage.** Mentees often think about equity in optimistic-scenario terms. Coach the probability-weighted model.

3. **Acceleration negotiation is undertaught.** Many mentees don't know to ask. Walk through single vs double trigger; have them ask in their next offer.

4. **The 409A conversation matters.** Coach mentees to request 409A and recent preferred-share price for every options grant.

5. **Coach against DIY tax decisions.** Mentees sometimes try to figure out 83(b), AMT, exercise timing themselves. Refer to a CPA; the cost of bad advice is high.

6. **Dilution awareness changes negotiation strategy.** Mentees often anchor on current grant size; coach them to model dilution forward to estimate end-of-tenure share value.

## When This Applies

- Evaluating an equity offer
- Modeling expected value of a startup grant
- Negotiating equity terms (size, acceleration, vesting)
- Considering an exercise or 83(b) decision
- Building basic literacy before any senior negotiation

## Cross-Domain Connections

- **negotiation-leverage/offer-negotiation** — Equity is the negotiation's highest-leverage component
- **negotiation-leverage/exit-and-transition** — Vesting acceleration and post-exit equity matter at exit
- **investing/archon** — Cap-table mechanics, preferred-share economics, dilution modeling
- **biotech-venture/asclepius/asset-valuation** — Asset-stage valuation informs equity expected value
- **trajectory-design/optionality-architecture** — Equity decisions have option-set consequences
