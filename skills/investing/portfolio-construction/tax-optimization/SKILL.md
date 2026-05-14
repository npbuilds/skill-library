---
name: tax-optimization
description: >
  Tax-efficient portfolio management frameworks — tax-loss harvesting, direct indexing, asset location,
  tax-aware rebalancing, capital gains management, and estate planning considerations for investors.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Tax Optimization — Keeping What You Earn

Taxes are the single largest drag on investment returns for taxable investors. The difference between pre-tax and after-tax returns compounds devastatingly over decades. A portfolio earning 8% pre-tax with a 2% annual tax drag effectively earns 6% — over 30 years, that 2% annual drag reduces terminal wealth by roughly 40%.

Tax optimization is not about tax avoidance — it's about not paying more than legally required. Every dollar saved in taxes compounds for the investor. This skill covers the full spectrum of legal tax optimization strategies available to investors.

---

## Part 1: Tax-Loss Harvesting

### Mechanics

Tax-loss harvesting (TLH) is the practice of selling investments that have declined in value to realize capital losses, which can then be used to offset capital gains (and up to $3,000 of ordinary income per year in the US).

**The process:**

1. Identify holdings with unrealized losses
2. Sell those holdings to realize the loss
3. Immediately replace with a similar (but not "substantially identical") investment to maintain market exposure
4. Use the realized loss to offset realized gains on your tax return
5. Excess losses carry forward indefinitely to offset future gains

**Tax benefit calculation:** The value of a harvested loss is:

```
Tax Savings = Loss Amount x Marginal Tax Rate
```

For a $10,000 loss at a 37% marginal rate: $3,700 in tax savings. Those savings, reinvested, compound over the remaining investment horizon.

**Long-term vs short-term:** Short-term losses are more valuable because they offset short-term gains (taxed at ordinary income rates, up to 37%) before offsetting long-term gains (taxed at 15-20%). Always harvest short-term losses first if available.

### The Wash Sale Rule

The IRS prohibits claiming a loss if you buy a "substantially identical" security within 30 days before or after the sale. This creates a 61-day window (30 days before, sale day, 30 days after).

**What is "substantially identical"?**

- Same stock: selling AAPL and buying AAPL within 30 days = wash sale
- Same fund: selling Vanguard S&P 500 ETF (VOO) and buying Vanguard S&P 500 Index Fund (VFIAX) = likely wash sale (same underlying index)
- Different index, same asset class: selling VOO (S&P 500) and buying ITOT (Total US Market) = NOT a wash sale (different index, different composition)
- Different provider, same index: selling VOO (Vanguard S&P 500) and buying IVV (iShares S&P 500) = grey area, most tax advisors say avoid

**Critical:** The wash sale rule applies across ALL accounts — if you sell a stock for a loss in your taxable account and buy it in your IRA within 30 days, the loss is disallowed AND you don't get the IRA basis adjustment. This is worse than not harvesting at all.

### Harvesting While Maintaining Exposure

The key to effective TLH is replacing the sold position with something similar enough to maintain your intended exposure but different enough to avoid wash sale rules.

**Common swap pairs:**

| Sold (Harvest Loss) | Replace With | Why It Works |
|---------------------|-------------|--------------|
| VOO (S&P 500) | ITOT (Total US Market) or SCHX (Large Cap) | Different index, similar exposure |
| VTI (Total US Market) | SCHB (Broad Market) or SPTM (SPDR Total Market) | Different provider, different index methodology |
| VXUS (Int'l ex-US) | IXUS (iShares Int'l) or SPDW (SPDR Int'l) | Different provider, slightly different composition |
| BND (Total Bond) | AGG (iShares Aggregate) or SCHZ (Schwab Aggregate) | Different provider |
| Individual stock (e.g., AAPL) | Sector ETF (e.g., XLK) or competitor stock | Different security, similar factor exposure |

After 31 days, you can swap back to the original position if desired (resetting the cost basis).

### Quantified Benefit

Academic and industry research consistently shows TLH adds approximately 1-2% annually to after-tax returns for taxable investors, declining over time as the portfolio's unrealized gains grow.

**Early years (years 1-5):** Highest harvesting opportunity. New positions haven't appreciated much, and market volatility creates frequent loss opportunities. Benefit: 1.5-2.5% annually.

**Middle years (years 5-15):** Moderate harvesting opportunity. Some positions have large embedded gains. Benefit: 0.75-1.5% annually.

**Later years (years 15+):** Reduced harvesting opportunity. Most positions have large embedded gains. New contributions are a smaller share of the portfolio. Benefit: 0.25-0.75% annually.

**Lifetime benefit (compounded):** Over a 30-year horizon, consistent TLH adds roughly 15-25% to terminal portfolio value for a high-tax-rate investor. This is one of the most reliable sources of excess return available.

---

## Part 2: Direct Indexing

### What Is Direct Indexing?

Instead of buying an index ETF (which owns all stocks in the index as a single security), direct indexing buys the individual stocks that comprise the index separately. This allows tax-loss harvesting at the individual stock level rather than the ETF level.

**Why this matters:** An ETF can only be harvested when the entire ETF is down. But within the ETF, individual stocks are constantly rising and falling. On any given day, even in a rising market, 40-50% of index constituents may be down for the month or quarter. Direct indexing captures these individual-stock losses that are invisible inside an ETF.

### The Harvesting Advantage

Direct indexing harvests dramatically more losses than ETF-based strategies:

**ETF-only harvesting:** Average annual harvest of roughly $5,000-$8,000 per $1M portfolio. Limited to periods when the entire market or sector is down.

**Direct indexing:** Average annual harvest of roughly $18,000-$30,000 per $1M portfolio. Individual stocks provide constant harvesting opportunities.

**The multiplier:** Direct indexing typically harvests 3-5x more losses than ETF-only strategies. On a $1M portfolio, the additional tax savings at a 37% marginal rate are roughly $4,000-$8,000 per year. This compounds.

### Major Platforms

| Platform | Owner | Minimum | Annual Fee | Key Feature |
|----------|-------|---------|------------|-------------|
| Aperio | BlackRock | $100K | 0.20-0.45% | Institutional-grade, deep customization |
| Parametric | Morgan Stanley | $250K | 0.20-0.40% | Largest platform, strong tax management |
| Wealthfront | Wealthfront | $100K | 0.25% (included) | Automated, consumer-friendly |
| Frec | Frec | $20K | 0.10% | Lowest cost, newer entrant |
| Fidelity | Fidelity | $5K | 0.40% | Integrated with Fidelity accounts |
| Schwab | Charles Schwab | $100K | Varies | Personalized indexing |

### When Direct Indexing Makes Sense

**Strong candidates:**
- Taxable portfolios above $100K (below this, the fee drag outweighs the tax benefit)
- High marginal tax rates (32%+ federal)
- Portfolios with significant realized gains elsewhere (concentrated stock sales, real estate sales)
- Investors who want ESG customization (exclude specific companies or sectors)
- Investors who want factor tilts built into the index (value, quality, etc.)

**Weak candidates:**
- Portfolios primarily in tax-advantaged accounts (no tax benefit)
- Low marginal tax rates (tax savings don't justify the fee)
- Very small portfolios (transaction costs and fees dominate)
- Investors who want extreme simplicity (direct indexing requires more positions and complexity)

### Customization Benefits Beyond Tax

Direct indexing allows customization that ETFs cannot:

- **ESG exclusions:** Remove fossil fuel companies, weapons manufacturers, etc. without selling the whole ETF
- **Factor tilts:** Overweight value, quality, or momentum within the index construction
- **Concentration management:** Reduce exposure to stocks you already own elsewhere (employer stock, concentrated positions)
- **Sector constraints:** Limit or eliminate exposure to sectors where you have other exposure (e.g., tech workers excluding tech)
- **Transition management:** Gradually harvest losses on a legacy portfolio while building toward a target allocation

---

## Part 3: Asset Location

### The Principle

Different account types have different tax treatments. Matching the right investments to the right account type can add 0.25-0.75% annually to after-tax returns.

**Account types and their tax treatment:**

| Account Type | Contributions | Growth | Withdrawals |
|-------------|--------------|--------|-------------|
| Taxable (brokerage) | After-tax | Taxed annually (dividends, gains) | Capital gains tax on sale |
| Tax-deferred (401k, Traditional IRA) | Pre-tax (deductible) | Tax-free | Taxed as ordinary income |
| Tax-free (Roth IRA, Roth 401k) | After-tax (not deductible) | Tax-free | Tax-free |

### Asset Location Rules

**Taxable accounts — hold tax-efficient assets:**
- Broad market index ETFs (low turnover, minimal distributions)
- Municipal bonds (tax-exempt interest for in-state residents)
- Long-term holdings (defer gains, pay lower long-term rate)
- Tax-managed funds (explicitly minimize taxable distributions)
- Individual stocks you plan to hold for 1+ year

**Tax-deferred accounts (401k, Traditional IRA) — hold tax-inefficient assets:**
- Bonds (interest taxed as ordinary income — shelter it in tax-deferred)
- REITs (dividends taxed as ordinary income)
- High-turnover strategies (active funds, factor strategies with frequent rebalancing)
- Treasury Inflation-Protected Securities (TIPS — phantom income problem in taxable accounts)

**Tax-free accounts (Roth) — hold highest expected return assets:**
- Small-cap equities (highest expected return, shelter the growth)
- Emerging market equities (same logic)
- High-growth strategies
- Assets you expect to appreciate the most (maximize the value of tax-free growth)

### The "Fill the Buckets" Framework

Rank your investments from most tax-inefficient to most tax-efficient. Rank your accounts from most tax-advantaged to least. Fill from the top:

```
Most tax-inefficient → Most tax-advantaged account
                    ↓
Least tax-inefficient → Least tax-advantaged account

Example:
1. REITs, bond funds, high-turnover active → Tax-deferred (401k/IRA)
2. Small-cap growth, EM equities → Tax-free (Roth)
3. Broad market index ETFs, muni bonds → Taxable
```

### Asset Location Considerations

**Total portfolio view:** Asset location must be evaluated across ALL accounts simultaneously, not account by account. Your allocation targets apply to the total portfolio — individual accounts will have different compositions to optimize tax efficiency.

**Rebalancing across accounts:** When rebalancing, make changes in tax-advantaged accounts first (no tax impact). Only rebalance in taxable accounts when necessary, and combine with tax-loss harvesting.

**Withdrawal sequencing (retirement):** In retirement, the order of account withdrawals matters enormously. Generally: taxable first (lowest tax cost), then tax-deferred (ordinary income), then Roth (tax-free, let it compound longest). But this interacts with tax bracket management, RMDs, and Social Security taxation.

---

## Part 4: Tax-Aware Rebalancing

### The Problem

Standard rebalancing advice says "rebalance quarterly" or "rebalance when drift exceeds 5%." But in taxable accounts, every rebalancing trade that involves selling an appreciated asset triggers a capital gain. The tax cost of rebalancing can exceed the benefit.

### Tax-Aware Rebalancing Methods

**Method 1 — Rebalance with new contributions (preferred):**
Direct all new cash (savings, dividends, interest) to the underweight asset class. No selling required, no tax impact. This is the cleanest method.

- Dividend reinvestment: direct dividends to the underweight asset class rather than reinvesting in the same fund
- New contributions: always contribute to the most underweight allocation
- This alone handles most drift for portfolios in the accumulation phase

**Method 2 — Sell highest basis lots first:**
When selling is necessary, sell the tax lots with the highest cost basis. These have the smallest (or no) embedded gain, minimizing the tax impact.

- Use specific lot identification (not average cost) for all taxable accounts
- Track cost basis by lot at purchase
- Always sell the highest-basis lot first when reducing a position

**Method 3 — Rebalance in tax-advantaged accounts:**
If the asset is held in both taxable and tax-advantaged accounts, rebalance within the tax-advantaged account. Zero tax impact.

**Method 4 — Combine with tax-loss harvesting:**
If a position is overweight AND has losses, harvest the loss while rebalancing. You get the tax benefit AND return to target allocation. This is the ideal scenario — actively look for it.

**Method 5 — Synthetic rebalancing:**
Use options or futures to adjust effective exposure without selling. For example, if equities are overweight, sell equity futures (short) to reduce effective equity exposure without triggering gains on the underlying stock positions. This is more complex but can be powerful for large portfolios.

### Rebalancing Priority Order

When the portfolio needs rebalancing:

1. Direct new contributions to underweight assets (no tax)
2. Rebalance within tax-advantaged accounts (no tax)
3. Tax-loss harvest overweight positions that are at a loss (negative tax — you get a benefit)
4. Sell highest-basis lots of overweight positions (minimal tax)
5. Sell long-term gain lots of overweight positions (reduced rate)
6. Last resort: sell short-term gain lots (highest tax cost — avoid if possible)

---

## Part 5: Capital Gains Management

### Short-Term vs Long-Term: The Rate Gap

The difference in tax rates between short-term and long-term capital gains is enormous:

| Income Level (Single, 2024) | Short-Term Rate | Long-Term Rate | Gap |
|---------------------------|-----------------|----------------|-----|
| Under $47,025 | 10-12% | 0% | 10-12% |
| $47,025 - $100,525 | 22% | 15% | 7% |
| $100,525 - $191,950 | 24% | 15% | 9% |
| $191,950 - $243,725 | 32% | 15% | 17% |
| $243,725 - $609,350 | 35% | 20% | 15% |
| Over $609,350 | 37% | 20% | 17% |

Plus the 3.8% Net Investment Income Tax (NIIT) applies to both short-term and long-term gains for high earners, making the effective top rates 40.8% and 23.8% respectively. The gap at the top: 17 percentage points. On a $100,000 gain, that's $17,000 in additional taxes for selling one day too early.

### Holding Period Management

**The 366-day rule:** Hold all positions for at least one year and one day to qualify for long-term capital gains treatment. This single rule is worth more than most active trading strategies.

**Near-threshold positions:** If a position is approaching the 1-year holding period and you want to sell:
- If it's within 30 days of the 1-year mark: WAIT. The tax savings from long-term treatment almost always exceed any expected price decline over 30 days.
- If it's more than 30 days away: Evaluate whether the expected return over the waiting period justifies the holding period. If the thesis is broken, sell (a short-term gain is better than a larger short-term gain after further appreciation, or a loss after a decline).

**Tax lot management:** When you own multiple lots of the same security purchased at different times, always specify which lot you are selling. Sell the lot that:
1. Has a loss (harvest it)
2. Has the highest cost basis (minimize gain)
3. Qualifies for long-term treatment (lower rate)

In that priority order.

### Charitable Giving of Appreciated Securities

One of the most powerful tax strategies available. Instead of selling appreciated stock, paying capital gains tax, and donating the cash:

1. Donate the appreciated stock directly to a charity or donor-advised fund (DAF)
2. Receive a tax deduction for the full fair market value (no capital gains tax)
3. The charity sells the stock tax-free

**The double benefit:**
- You avoid the capital gains tax (up to 23.8%)
- You receive the charitable deduction (up to 37% marginal rate)
- Combined tax benefit: up to 60.8% of the donated amount

**Requirements:** Must hold the security for more than one year. Deduction limited to 30% of AGI for appreciated property (vs 60% for cash donations). Excess carries forward for 5 years.

**Practical tip:** Use a donor-advised fund (DAF) as an intermediary. Donate appreciated stock to the DAF (immediate deduction), then distribute grants to charities over time. This decouples the tax benefit timing from the charitable giving timing.

### Qualified Opportunity Zones (QOZs)

A mechanism to defer and reduce capital gains by investing in designated opportunity zones:

**Step 1:** Realize a capital gain from any source (stock sale, real estate, business sale)
**Step 2:** Within 180 days, invest the gain amount in a Qualified Opportunity Fund (QOF)
**Step 3:** Defer the original gain until the earlier of: (a) sale of the QOF investment, or (b) December 31, 2026

**Benefits:**
- Deferral of the original gain
- If held 10+ years: NO tax on the appreciation of the QOF investment itself (this is the powerful part)
- The basis step-up for 5/7-year holdings was available for investments made before 2020 but is no longer available for new investments

**Risks:** QOZ investments are typically illiquid real estate developments in economically distressed areas. The investment risk is real — tax benefits don't help if the underlying investment loses money.

**When it makes sense:** Large capital gains ($500K+) from a concentrated stock sale or business exit, AND access to a well-managed QOF with strong real estate fundamentals.

---

## Part 6: Estate Planning Considerations

### Step-Up in Basis at Death

The single most powerful tax planning rule in the US tax code. When an investor dies, all unrealized capital gains in their estate receive a "step-up" in cost basis to the fair market value on the date of death. The unrealized gains disappear — they are never taxed.

**Implication:** If you hold highly appreciated stock, the optimal tax strategy may be to NEVER sell it during your lifetime. The gains vanish at death, and your heirs receive the stock with a basis equal to the date-of-death value.

**This creates the "buy, borrow, die" strategy used by the ultra-wealthy:**
1. Buy appreciating assets (stocks, real estate)
2. Borrow against them for spending (interest on loans is lower than capital gains tax rates)
3. Die with the appreciated assets (step-up eliminates the gains)
4. Heirs sell at stepped-up basis (no tax) and repay the loans

**Practical application for regular investors:**
- Avoid selling highly appreciated long-term holdings if possible
- Harvest losses aggressively (they offset gains now and preserve the step-up benefit)
- Hold your most appreciated assets in taxable accounts (not Roth, where the step-up is irrelevant since growth is already tax-free)
- If choosing between selling a large gain or borrowing against it, borrowing may be more tax-efficient at current rates

### Gift vs Bequest

**Gifting during lifetime:** The recipient takes the donor's cost basis (carryover basis). No step-up. The embedded gain transfers with the gift. This is tax-inefficient for appreciated assets.

**Bequest at death:** The recipient receives the step-up in basis. All embedded gains disappear. This is tax-efficient for appreciated assets.

**Strategic implication:**
- Gift LOSING positions (the recipient gets your high basis and can harvest the loss)
- Gift cash or low-appreciation assets
- Bequeath highly appreciated assets (let the step-up eliminate the gain)

**Annual gift exclusion (2024):** $18,000 per recipient per year without using lifetime exemption. Useful for transferring wealth to the next generation, especially combined with the gifting strategy above.

**Lifetime exemption (2024):** $13.61 million per person ($27.22 million per couple). Amounts above the annual exclusion eat into this lifetime cap. The exemption is scheduled to be reduced by roughly half after 2025 unless Congress acts.

---

## Part 7: Practical Framework — Tax Optimization Checklist

### Before Any Trade

Ask these questions before executing any trade in a taxable account:

1. **Is there a loss to harvest?** If the position is at a loss, harvesting is almost always correct. Replace with a non-identical substitute.
2. **Is the gain short-term or long-term?** If short-term, can you wait to convert to long-term? The rate difference is 10-17 percentage points.
3. **Can this trade happen in a tax-advantaged account instead?** If you hold the same asset class in both taxable and tax-advantaged, rebalance in the tax-advantaged account.
4. **What is the cost basis?** If selling, use specific lot identification to sell the highest-basis lot.
5. **Are there offsetting losses available?** If you have harvested losses in the current year, they can offset this gain. Check before deferring the trade.
6. **Is this a charitable giving candidate?** If the gain is large and you plan to donate to charity anyway, donate the appreciated stock instead of selling.

### Monthly Tax Review

- Scan portfolio for new loss-harvesting opportunities (positions down 5%+ from purchase)
- Check for positions approaching the 1-year holding period mark
- Review recent dividends and distributions for tax impact
- Verify wash sale compliance (no identical purchases within 30 days of harvests)

### Annual Tax Optimization Checklist

**Q1 (January-March):**
- Review prior year's capital gain/loss carryforward
- Set tax-loss harvesting targets for the year
- Review asset location — are new contributions going to the right accounts?

**Q2-Q3 (April-September):**
- Harvest losses opportunistically through market volatility
- Review holding periods of positions you may want to sell
- Evaluate Roth conversion opportunities (especially in down market years)

**Q4 (October-December):**
- Final tax-loss harvesting sweep before year-end
- Estimate annual capital gains distributions from mutual funds (they distribute in December)
- Make charitable contributions of appreciated stock before year-end
- Review whether to accelerate or defer income/gains across the year boundary
- Evaluate qualified opportunity zone investments for large realized gains
- Confirm all wash sale windows are clear before year-end harvests

### The Anti-Checklist: What NOT to Do

- Do not let taxes drive investment decisions — tax optimization is a secondary filter, not the primary investment thesis
- Do not harvest losses and then violate the wash sale rule by buying back within 30 days
- Do not assume your accountant will catch harvesting opportunities — proactive management is required
- Do not hold losing positions solely because "they'll come back" — harvest the loss, buy something similar, and maintain the exposure
- Do not ignore state taxes — state capital gains rates vary from 0% (no income tax states) to 13.3% (California) and significantly impact the optimization math
- Do not sell highly appreciated positions near death — the step-up in basis eliminates the gain for free
- Do not put tax-inefficient assets in taxable accounts when tax-advantaged space is available
- Do not over-optimize at the expense of portfolio quality — owning a slightly inferior investment for tax reasons can cost more than the tax saved

## Related Skills

- **rebalancing-logic** — Rebalancing is a primary source of taxable events. Inputs from rebalancing-logic (target drift, rebalance triggers) determine when tax-optimization decisions become live.
