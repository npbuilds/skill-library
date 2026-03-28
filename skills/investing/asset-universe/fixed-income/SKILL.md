---
name: fixed-income
description: >
  Fixed income investing frameworks — yield curve analysis, credit evaluation, duration
  management, and bond market structure. Reference when analyzing bonds, managing interest
  rate risk, evaluating credit, or understanding what the bond market signals about the economy.
---

# Fixed Income — The Lending Side

Fixed income is a contract: you lend money, you get it back with interest. Every bond question reduces to three risks — will they pay me back (credit risk), what happens to rates before they do (interest rate risk), and can I sell if I need to (liquidity risk). The bond market is bigger than the stock market, more informative about the economy, and less understood by most investors.

## Yield Curve Analysis

The yield curve is the single most important chart in finance. It plots the interest rate (yield) against the time to maturity for government bonds. Its shape, slope, and level each tell you something different about the economy.

### Shape: What the Curve Tells You

**Normal (upward sloping)**: Short-term rates are lower than long-term rates. This is the default state. It means:
- The market expects growth and/or inflation to be higher in the future.
- Lenders demand more compensation for locking up money for longer periods (term premium).
- Banks can profit by borrowing short and lending long (positive carry), which supports credit creation and economic growth.

**Flat**: Short-term and long-term rates are approximately equal. This signals:
- The market expects growth to slow.
- The Fed has raised short-term rates to a level that the bond market thinks is restrictive.
- Banks' net interest margins are compressed, which reduces lending and slows the economy.
- A transition state — the curve is either on its way to inverting or steepening.

**Inverted (downward sloping)**: Short-term rates are higher than long-term rates. This is the most powerful recession signal in finance:
- The market expects the Fed to cut rates in the future — because a recession will force it to.
- Banks lose money on new loans (borrow short at high rates, lend long at low rates), which chokes credit.
- The inversion itself contributes to the recession by tightening financial conditions.

### The Inverted Curve as Recession Predictor

**Track record**: The 2-year/10-year Treasury spread has inverted before every US recession since 1955. It has produced two arguable false positives (1966 and 1998), though both were periods of significant economic slowdown.

**Lead time**: The median lead time from initial inversion to recession onset is approximately 15-18 months, but the range is wide (6-24 months). The recession typically begins after the curve has un-inverted (steepened), not during the inversion itself.

**The 3-month/10-year spread**: Some researchers (notably the New York Fed) prefer this measure. It has a slightly better track record but inverts later than the 2-10 spread, giving less lead time.

**Why it works**: The yield curve reflects the collective expectation of every bond market participant about future interest rates, growth, and inflation. When the curve inverts, the bond market is saying: "The Fed has overtightened, the economy will weaken, and rates will have to come back down." The bond market is not always right, but it has a better forecasting record than any economic model.

**Caveats**: Quantitative easing distorted the signal by compressing term premium, potentially causing inversions that are less recessionary. Foreign central bank demand for US Treasuries also depresses long-term yields, making the curve more prone to inversion independent of recession risk.

### Curve Movements: The Four Regimes

Yield curves do not just steepen and flatten — how they steepen or flatten matters enormously.

**Bear Steepener (short rates stable or rising, long rates rising faster)**:
- What it means: Inflation expectations rising, term premium expanding, bond market losing confidence in fiscal sustainability or inflation control.
- When it happens: Rising government deficits, commodity price shocks, central bank losing credibility.
- Impact: Negative for both stocks and bonds. Rising long rates increase discount rates and tighten financial conditions. This is the most dangerous curve regime for portfolios.
- Historical example: October 2023 bear steepener — 10-year yields surging above 5%, driven by fiscal concerns and Treasury supply.

**Bull Steepener (short rates falling, long rates stable or falling slower)**:
- What it means: The Fed is cutting rates because the economy is weakening. The front end falls as the Fed eases, but the long end holds because the market expects the easing to eventually reflate the economy.
- When it happens: Early stages of Fed easing cycles, initial recession response.
- Impact: Positive for bonds (price gains on the front end), cautious for equities (the reason for cuts matters — is it an insurance cut or a recession response?).
- Historical example: September 2024 onward — Fed beginning to cut rates with long-end yields sticky.

**Bear Flattener (short rates rising faster than long rates, or long rates falling)**:
- What it means: The Fed is tightening, and the bond market believes the tightening will slow the economy (long rates stop rising or fall because growth expectations decline).
- When it happens: Mid to late stages of Fed hiking cycles.
- Impact: The bond market is telling the Fed it is making a policy mistake by overtightening. Often precedes curve inversion.
- Historical example: 2022 — Fed aggressively hiking, long rates rose but less than short rates.

**Bull Flattener (long rates falling faster than short rates, or short rates stable)**:
- What it means: Flight to quality — investors buying long-term bonds as a safe haven. Growth expectations collapsing.
- When it happens: Acute economic fears, geopolitical crises, deflationary scares.
- Impact: Very negative for equities, very positive for long-duration bonds. Classic risk-off regime.
- Historical example: March 2020 COVID crash — massive flight to quality in long-duration Treasuries.

### Term Premium

Term premium is the extra yield investors demand for holding a long-term bond instead of rolling a series of short-term bonds. It is unobservable — it must be estimated using models.

**Key models**:
- **ACM (Adrian, Crump, Mohanty)**: Published by the New York Fed. Estimates term premium using a statistical model of the yield curve. Widely followed.
- **Kim-Wright**: Published by the Federal Reserve Board. Similar approach, different assumptions. Generally produces higher estimates than ACM.

**Why term premium matters**:
- When term premium is low or negative (as it was from 2015-2023), long-term bonds are not compensating investors for duration risk. This makes long-duration bonds asymmetrically risky — you have all the downside of duration with no premium to compensate.
- When term premium is high and rising (2023-2025 trend), long-term bonds become more attractive on a risk-adjusted basis. But rising term premium also means rising long-term rates, which tightens financial conditions.
- The trend in term premium is as important as the level. Rising term premium from negative to zero is very different from rising from 1% to 2%.

**What drives term premium**:
- Supply: More Treasury issuance increases the term premium investors demand. Fiscal deficits matter.
- Demand: Foreign central bank purchases, pension fund demand, and QE all compress term premium. Quantitative tightening (QT) does the opposite.
- Inflation uncertainty: Higher uncertainty about future inflation increases term premium. Investors need more compensation when the range of possible outcomes is wider.

## Credit Analysis

### The Credit Spectrum

| Category | Yield Spread Over Treasuries (typical range) | Default Rate (annual average) | Characteristics |
|----------|----------------------------------------------|-------------------------------|-----------------|
| AAA-AA (high grade) | 20-60 bps | <0.1% | Government-like credit quality. Minimal default risk. Yield driven by duration and liquidity. |
| A-BBB (investment grade) | 60-200 bps | 0.1-0.5% | Corporate stalwarts. Manageable leverage, stable cash flows. The BBB tier is the largest and most important — fallen angel risk if downgraded to junk. |
| BB-B (high yield / junk) | 200-600 bps | 1-4% | Higher leverage, cyclical businesses, leveraged buyouts. Credit selection matters enormously. |
| CCC and below (distressed) | 600-2000+ bps | 10-30% | Companies in or near financial distress. Equity-like risk with bond-like upside — not a bond investment, it is a distressed turnaround bet. |
| Leveraged loans | 200-500 bps over SOFR | 1-3% | Floating rate, senior secured, covenant-lite since 2020. Lower loss-given-default than bonds due to seniority, but weaker covenant protection. |

### Credit Spreads as Economic Indicators

Credit spreads are the difference in yield between corporate bonds and Treasuries of similar maturity. They are among the most reliable real-time economic indicators.

**What widening spreads tell you**:
- Economic growth expectations are deteriorating.
- Default risk is rising.
- Liquidity in credit markets is declining.
- Risk aversion is increasing.

**What tightening spreads tell you**:
- Economic confidence is improving.
- Default risk is declining.
- Liquidity is abundant.
- Investors are reaching for yield (which can indicate complacency).

**Spread levels and what they signal** (investment grade OAS):
- Below 80 bps: Extremely tight. Complacency. Little compensation for credit risk. Historically precedes widening.
- 80-130 bps: Normal range. Adequate compensation for average default losses.
- 130-200 bps: Elevated concern. Economic slowdown being priced.
- 200-300 bps: Recession pricing. Significant widening from normal.
- 300+ bps: Crisis levels. Distress in credit markets. Historically, buying at these levels has produced strong forward returns.

**High yield spread levels**:
- Below 300 bps: Extremely tight. Historically rare and unsustainable.
- 300-450 bps: Normal range.
- 450-700 bps: Recessionary concern.
- 700-1000 bps: Recession priced. Historically excellent entry point.
- 1000+ bps: Full crisis (2008, March 2020). Generational buying opportunity if you can stomach the volatility.

### Default Cycle Dynamics

Defaults are cyclical, not random. Understanding the default cycle helps with credit timing.

**The default cycle**:
1. **Late cycle**: Companies that over-levered during the expansion begin to struggle as growth slows and rates rise. Defaults begin ticking up from trough levels. CCC-rated issuers go first.
2. **Recession**: Default rates spike. The average high-yield default rate during recessions is 8-12%. Recovery rates (how much you get back in default) fall to 30-40 cents on the dollar, down from 50-60 cents in normal times.
3. **Early recovery**: Defaults peak and begin to fall. The weakest companies have already defaulted. Survivors are leaner and more creditworthy. This is the best time to buy credit.
4. **Mid expansion**: Defaults at trough levels (1-2%). Credit quality deteriorating at the margin as new issuance increases and lending standards loosen, but the overall default rate stays low.

**Leading indicators of rising defaults**:
- Distress ratio: Percentage of high-yield bonds trading at spreads above 1000 bps. Rising distress ratio precedes rising defaults by 6-12 months.
- Leverage ratios: Aggregate corporate debt/EBITDA. Rising leverage in a maturing economic cycle is a warning.
- Interest coverage: EBITDA/interest expense. Declining coverage means companies are less able to service debt.
- Maturity wall: The amount of debt maturing in the next 2-3 years. If companies cannot refinance, defaults rise.

### Credit Selection Tools

**Altman Z-Score**: A discriminant analysis model that predicts bankruptcy probability. Uses five financial ratios weighted together. Z > 2.99 = safe zone. Z < 1.81 = distress zone. Between = gray zone. Developed for manufacturing companies — less applicable to financial firms and service companies.

**Merton Model (Structural Credit Model)**: Treats equity as a call option on the firm's assets. When asset value falls below the debt's face value, the firm defaults. Key inputs: asset value, asset volatility, debt level, and time to maturity. The distance-to-default metric derived from this model is widely used by banks and rating agencies (Moody's KMV is a commercial implementation).

**Covenant Analysis**: Bond covenants are contractual protections for lenders. Key covenants to analyze:
- Leverage covenants: Maximum debt/EBITDA ratio.
- Interest coverage: Minimum EBITDA/interest.
- Restricted payments: Limits on dividends and share buybacks.
- Change of control: Put option if the company is acquired.
- Limitation on liens: Prevents the company from pledging assets to other creditors ahead of you.

Since 2020, covenant quality has deteriorated significantly ("covenant-lite" structures). This means lenders have less protection, and default recoveries will likely be lower in the next cycle.

## Duration Management

Duration measures a bond's sensitivity to interest rate changes. A bond with a duration of 5 years will lose approximately 5% of its value for every 1% increase in interest rates (and gain 5% for every 1% decrease).

### When to Be Long Duration (duration > benchmark)

- The Fed is cutting or expected to cut rates.
- Economic growth is decelerating.
- Inflation is falling.
- Credit conditions are tightening (flight to quality benefits long-duration Treasuries).
- Term premium is high (you are being paid to own duration).
- Portfolio needs a recession hedge (long-duration bonds are the best hedge against equity drawdowns — when they work).

### When to Be Short Duration (duration < benchmark)

- The Fed is hiking or expected to hike.
- Inflation is rising or sticky.
- Fiscal deficits are expanding (more supply of long-duration bonds).
- Term premium is low or negative (you are not being paid for duration risk).
- The stock-bond correlation has flipped positive (both stocks and bonds selling off together, as in 2022 — duration is no longer a hedge, it is adding risk).

### Key Duration Concept: Convexity

Convexity is the curvature of the price-yield relationship. Positive convexity means a bond's price rises more when yields fall than it declines when yields rise by the same amount. Long-duration Treasury bonds have high positive convexity — they are asymmetric bets that pay off more in a rally than they lose in a selloff. This makes them valuable as portfolio hedges even when the expected return is modest.

## TIPS and Inflation-Linked Bonds

### Breakeven Analysis

The breakeven inflation rate is the difference between the nominal Treasury yield and the TIPS yield of the same maturity. It represents the inflation rate at which a TIPS investor and a nominal Treasury investor would earn the same return.

**How to use breakevens**:
- If you expect inflation to be higher than the breakeven rate, buy TIPS (they will outperform nominal Treasuries).
- If you expect inflation to be lower than the breakeven rate, buy nominal Treasuries.
- The 5-year, 5-year forward breakeven (the market's expected inflation 5-10 years from now) is the best measure of long-term inflation expectations. When this moves significantly, it signals a shift in the inflation regime.

**Real vs nominal yields**: The real yield (TIPS yield) is the true return after inflation. When real yields are negative, bondholders are guaranteed to lose purchasing power — they are paying the government for the privilege of lending. When real yields are significantly positive (above 2%), bonds become attractive as an asset class on an absolute basis, not just relative to other assets.

## Treasury Market Structure

### Auction Cycle

The Treasury issues debt on a regular schedule. Understanding this schedule matters because supply affects pricing:
- **Bills** (< 1 year): Auctioned weekly. Huge market, highly liquid, low volatility.
- **Notes** (2, 3, 5, 7, 10 year): Auctioned monthly. The core of the Treasury market.
- **Bonds** (20, 30 year): Auctioned monthly. The long end of the curve. Most volatile.
- **TIPS**: Auctioned less frequently. Smaller market, lower liquidity.

**Auction dynamics**: Weak auctions (low bid-to-cover ratio, high tail — meaning the yield is higher than expected) signal insufficient demand for Treasuries. This matters because the US is issuing record amounts of debt, and demand is not guaranteed. Watch for weak auctions as a leading indicator of rising term premium.

### On-the-Run vs Off-the-Run

On-the-run Treasuries are the most recently issued securities at each maturity — they are the benchmark issues. Off-the-run Treasuries are older issues. On-the-runs trade at a premium (lower yield) because of superior liquidity. The on-the-run/off-the-run spread widens during periods of market stress, making off-the-runs attractive for investors who do not need daily liquidity.

## Municipal Bonds

### Tax-Equivalent Yield

Municipal bond interest is exempt from federal income tax (and often state and local tax for residents of the issuing state). The tax-equivalent yield formula:

Tax-equivalent yield = Municipal yield / (1 - marginal tax rate)

For an investor in the 37% federal bracket, a 3.5% municipal yield is equivalent to a 5.56% taxable yield. This makes munis attractive for high-income investors.

### Credit Quality Tiers

- **General obligation (GO)**: Backed by the full taxing power of the issuer. Highest quality for a given issuer.
- **Revenue bonds**: Backed by a specific revenue stream (tolls, water fees, hospital revenue). Quality depends on the revenue source's stability and essentiality.
- **Essential service revenue bonds**: Water, sewer, electric — very stable. Near-GO quality.
- **Non-essential revenue bonds**: Convention centers, stadiums, speculative development — higher risk.

Municipal defaults are rare (0.1% annually for investment grade) but not zero. Detroit (2013), Puerto Rico (2017), and various hospital and retirement community bonds demonstrate that munis are not risk-free.

## Global Fixed Income

### Sovereign Spreads

Non-US government bonds trade at a spread to US Treasuries (or German Bunds in Europe). These spreads reflect:
- Credit risk of the sovereign (fiscal position, institutional quality, rule of law).
- Currency risk (embedded in the yield differential if unhedged).
- Liquidity premium (US Treasuries are the most liquid bonds in the world).

### Currency Hedging Costs

For US-based investors, owning foreign bonds introduces currency risk. Hedging this risk using FX forwards or swaps costs approximately the interest rate differential between the two countries. When US rates are significantly higher than foreign rates (as they have been since 2022), hedging costs can eliminate or exceed the yield advantage of foreign bonds. This is why global bond allocations are less attractive to US investors when rate differentials are wide — you pay the full hedging cost, and the remaining yield is often below what US bonds offer.

**When to leave FX unhedged in fixed income**: Almost never. Unlike equities, where currency exposure can provide diversification, in fixed income the currency volatility typically overwhelms the modest yield. Unhedged foreign bonds are primarily a currency bet, not a bond investment. The exception is when you have a strong view on currency direction and want to express it through the bond market.

## Practical Framework: Fixed Income Portfolio Construction

### Step 1: Set the Duration Target

Based on the rate outlook and regime analysis. In uncertainty, stay neutral (match the benchmark).

### Step 2: Determine the Credit Allocation

How much credit risk do you want? More credit = more yield but more correlation with equities (defeating the purpose of bonds as a diversifier). A core allocation to Treasuries for diversification, plus a satellite allocation to credit for yield, is the standard approach.

### Step 3: Choose the Credit Quality

Investment grade for stability. High yield for income (but recognize it is a hybrid between bonds and equities). Leveraged loans for floating-rate exposure (protects against rising rates but not recession).

### Step 4: Add Tax-Advantaged Positions Where Appropriate

Municipal bonds for taxable accounts of high-income investors. The after-tax yield advantage is substantial and persistent.

### Step 5: Consider TIPS for Inflation Protection

When breakeven inflation is below your expected inflation, TIPS are cheap. When real yields are positive, TIPS offer genuine real return — something rare in fixed income history.

### Step 6: Monitor the Signals

The bond market tells you what is coming. Watch the yield curve shape, credit spreads, term premium, and auction results. When the bond market and the stock market disagree, bet on the bond market — it has a better track record.
