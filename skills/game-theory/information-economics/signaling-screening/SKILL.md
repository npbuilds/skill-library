---
name: signaling-screening
description: >
  Classical information economics foundations covering signaling, screening, adverse selection,
  moral hazard, and contract theory. Reference when analyzing how informed parties reveal or
  conceal private information through actions, and how uninformed parties extract information
  through menu design. Use when asymmetric information drives market failure or strategic behavior.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Signaling & Screening — The Classics

The foundational models of information economics. Three Nobel Prizes were awarded for this body of work (Akerlof, Spence, Stiglitz 2001; Mirrlees, Vickrey 1996; Hart, Holmstrom 2016). These models explain why markets fail under asymmetric information and how institutions — education, insurance, contracts, warranties — emerge to mitigate that failure. Grounded primarily in Fudenberg & Tirole (1991 Ch.7-9), Bolton & Dewatripont (2005), and the original Nobel-prize papers.

## The Information Asymmetry Framework

All models in this skill share a common structure:

1. **One party has private information** that the other party cares about
2. **The uninformed party** would make better decisions if they knew the information
3. **The information gap** creates strategic incentives — to reveal, conceal, distort, or extract

| Type | Who Knows | Who Moves First | Examples |
|------|-----------|-----------------|---------|
| **Adverse selection** (hidden type) | Informed party has a fixed private type | Nature → informed → uninformed | Used cars, insurance, hiring |
| **Moral hazard** (hidden action) | Action is chosen after contract | Uninformed → informed → Nature | Employment, insurance after purchase |
| **Signaling** | Informed party | Informed moves first (sends costly signal) | Education, warranties, advertising |
| **Screening** | Informed party | Uninformed moves first (offers a menu) | Insurance menus, airline pricing |

## Adverse Selection — The Lemons Problem

**Akerlof (1970)**: Sellers know car quality; buyers don't. If buyers can't distinguish good from bad cars, they pay an average price. Good-car owners withdraw (price too low), leaving only lemons. The market can collapse entirely.

**The key mechanism**: Asymmetric information creates a **pooling externality** — low-quality types drag down the price for high-quality types, who exit, further lowering average quality (adverse selection spiral).

**Real-world manifestations**:
- **Insurance**: Sick people buy more insurance → premiums rise → healthy people drop out → death spiral
- **Credit markets**: Risky borrowers accept high rates → safe borrowers exit → lenders face worse pool
- **Labor markets**: Unobservable productivity → firms pay average → top performers leave
- **eBay/marketplaces**: Without reputation systems, high-quality sellers can't distinguish themselves

**Solutions to adverse selection**:
- Signaling (costly actions by informed party)
- Screening (menu design by uninformed party)
- Reputation systems and certifications
- Mandatory disclosure or regulation
- Warranties and guarantees

## Signaling — Spence (1973)

The informed party takes a costly action to credibly convey their type.

### The Job Market Signaling Model

Workers have unobservable productivity (high or low). Education is costly but more costly for low-productivity workers. High-productivity workers signal by getting a degree.

**Separating equilibrium**: High types get educated, low types don't. The employer can infer type from education. Education may have zero productive value — it works purely as a signal because the cost differential between types makes it incentive-compatible.

**Pooling equilibrium**: Both types take the same action (both get educated, or neither does). No information is revealed. The employer pays the average.

**Key conditions for signaling to work**:
1. **Single crossing property**: The cost of the signal must differ between types. If everyone could signal cheaply, signals would be uninformative.
2. **Credible commitment**: The signal must be costly or difficult to fake.
3. **Observable**: The receiver must be able to verify the signal.

**Applications beyond education**:
- **Warranties**: Only high-quality firms offer generous warranties (costly for low-quality)
- **Advertising**: Spending on advertising signals product quality (would be wasted money for a bad product that won't get repeat purchases)
- **Dividends**: Companies pay dividends to signal financial health (bad companies can't sustain payouts)
- **IPO underpricing**: High-quality firms underprice IPOs to signal confidence in future earnings
- **Courtship displays**: Peacock tails, expensive gifts — costly signals of genetic fitness or commitment

## Screening — Rothschild & Stiglitz (1976)

The uninformed party offers a **menu of contracts** designed so that different types self-select into different options, revealing their private information.

### The Insurance Screening Model

Insurers can't observe risk type (high/low risk). They offer two policies:
- **High coverage, high premium**: Attractive to high-risk types (who expect to claim)
- **Low coverage, low premium**: Attractive to low-risk types (who rarely claim)

**Key result**: In competitive markets with two risk types, the separating equilibrium offers:
- High-risk types: full insurance at actuarially fair price for their risk
- Low-risk types: partial insurance (a distortion) to prevent high-risk types from mimicking them

**The distortion is borne by the "good" types**: Low-risk consumers get less coverage than they would under symmetric information. This is the informational rent — the cost of incentive compatibility.

**No-pooling result**: Under competitive conditions, pooling equilibria may not exist. But separating equilibria may not exist either when the proportion of high-risk types is small (Rothschild-Stiglitz non-existence). This was a foundational puzzle that motivated much subsequent work.

**Real-world screening**:
- **Airline pricing**: Business class vs. economy with deliberate discomfort (screening willingness-to-pay)
- **Insurance deductibles**: High deductible = lower premium (self-selection by risk type)
- **Coupon-clipping**: Time-insensitive consumers clip coupons; time-sensitive ones pay full price (screening price sensitivity)
- **Product versioning**: Software with feature restrictions (lite vs. pro) screens willingness-to-pay

## Moral Hazard

The informed party's **action** (not type) is unobservable. The classic principal-agent problem.

### The Principal-Agent Model

A principal (employer) hires an agent (worker) whose effort is unobservable. Output depends on effort + randomness. The principal wants high effort; the agent prefers low effort.

**The tradeoff**: Insurance vs. incentives
- **Full insurance** (fixed salary): Agent bears no risk but has no incentive to work hard
- **Full incentive** (pay = output): Agent works hard but bears all output risk
- **Optimal contract**: Balances risk-sharing and incentive provision. Second-best — strictly worse than the first-best (which would be achievable with observable effort)

**Key results** (Holmstrom 1979):
- Optimal pay depends on a **sufficient statistic** for effort — include any informative performance measure, exclude uninformative ones
- **Informativeness principle**: Additional signals of effort improve the contract even if they don't directly affect output
- Team problems: When multiple agents contribute to joint output, budget-breaking (paying more or less than total output) is needed for incentive compatibility (Holmstrom 1982)

**Applications**:
- Executive compensation (stock options as incentive)
- Insurance (deductibles to encourage care)
- Sharecropping (dividing harvest between landlord and tenant)
- Regulation (regulated firm's costs are private)

## Sources

Read `references/sources.md` for the full bibliography — Nobel-prize papers, primary texts, and key surveys.

## When This Applies

- Markets with quality uncertainty (insurance, credit, used goods)
- Any situation where one party has private information that affects the other's decision
- Contract design under hidden information or hidden action
- Understanding why institutions like education, warranties, or insurance menus exist
- Platform design (reputation systems, certification, quality assurance)

## Cross-Domain Connections

- **Investing/special-situations/insider-signals**: Insider buying is a signaling game — insiders use costly transactions (regulatory filing, capital at risk) to credibly signal private information about firm quality. The Spence signaling framework directly explains why insider purchases are more informative than insider sales.
- **Investing/reflexivity-sentiment/sentiment-signals**: Corporate guidance, earnings surprises, and disclosure timing are information design problems. Companies strategically reveal information to manage market expectations — screening by institutional vs. retail audience.
- **Investing/value-quality**: Adverse selection explains why cheap stocks are often cheap for a reason — the "market for lemons" dynamic in equity markets. Screening by quality metrics (ROIC, balance sheet strength) is the investor's response to asymmetric information.
