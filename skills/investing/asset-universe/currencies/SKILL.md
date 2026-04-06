---
name: currencies
description: >
  Currency analysis frameworks — FX valuation, dollar dynamics, carry trades, and how currencies
  affect multi-asset portfolios. Reference when analyzing foreign exchange, hedging currency
  exposure, evaluating the dollar's impact on global markets, or building FX-aware portfolios.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Currencies — The Hidden Variable

Every investment is a currency trade. When you buy a Japanese stock, you are long Japanese equities and long the yen. When you buy a US Treasury bond, you are long US duration and long the dollar. Currency exposure is the most pervasive and least understood risk in most portfolios. This skill covers how to analyze currencies, when to hedge, and how FX movements affect every other asset class.

## FX Analysis Frameworks

No single model reliably predicts currency movements. Instead, use multiple lenses and look for convergence.

### Purchasing Power Parity (PPP)

**The theory**: Exchange rates should adjust so that a basket of goods costs the same in every country. If a basket costs $100 in the US and EUR 90 in Europe, the PPP exchange rate is 1.11 USD/EUR.

**Reality**: PPP is a terrible short-term predictor but a reasonable long-term anchor. Currencies can deviate from PPP by 30-50% for years or decades. But extreme deviations from PPP tend to correct over 5-10 year horizons.

**Practical use**: PPP tells you whether a currency is fundamentally over- or undervalued. The OECD publishes PPP estimates for all major currencies. As of 2025, the US dollar is significantly overvalued against most currencies on a PPP basis (15-25% overvalued vs EUR, 30%+ overvalued vs JPY). This does not mean the dollar will weaken tomorrow — it means the dollar's long-term expected return relative to other currencies is negative.

**The Big Mac Index**: The Economist's informal PPP measure. Entertaining but actually useful as a quick-and-dirty valuation gauge. It captures the same underlying principle as formal PPP models.

### Interest Rate Differentials

**The theory**: According to covered interest rate parity, the forward exchange rate should reflect the interest rate differential between two currencies. In uncovered interest rate parity, high-interest-rate currencies should depreciate to eliminate the yield advantage.

**Reality**: Uncovered interest rate parity fails systematically — high-yielding currencies do not depreciate enough to offset their yield advantage, on average. This is the foundation of the carry trade (see below). But when it fails, it fails spectacularly (carry trade unwinds).

**Practical use**: Interest rate differentials are the most important medium-term driver of currency flows. When the Fed raises rates above other central banks, the dollar strengthens because capital flows into higher-yielding US assets. When rate differentials narrow, the dollar weakens.

**Current dynamics**: The US has maintained a significant interest rate premium over Europe and Japan since 2022. This has been the primary driver of dollar strength. When this differential narrows — because the Fed cuts more than others, or others raise more — it will be the primary catalyst for dollar weakness.

### Capital Flows

**The theory**: Currencies are ultimately determined by supply and demand. Capital flows — investment flows, trade flows, and speculative flows — determine who wants to buy and sell each currency.

**Key flow categories**:
- **Trade flows (current account)**: Countries with trade surpluses (China, Germany, Japan) accumulate foreign currency that must be converted back to their home currency — this should strengthen the surplus country's currency. But this effect is often overwhelmed by capital account flows.
- **Portfolio flows**: Foreign buying of a country's stocks and bonds creates demand for that currency. The US has attracted enormous portfolio inflows due to tech stock outperformance and high yields — this has supported the dollar.
- **FDI flows**: Foreign direct investment (building factories, acquiring companies) creates longer-term currency demand. Less volatile than portfolio flows.
- **Reserve flows**: Central bank reserve management — buying and selling currencies to manage reserves. China and Japan are the largest reserve managers. Their decisions can move markets.
- **Speculative flows**: Hedge fund and CTA positioning. Measured by CFTC Commitments of Traders data. Extreme speculative positioning often precedes reversals.

### Real Effective Exchange Rate (REER)

The REER adjusts the nominal exchange rate for inflation differences between countries. It is the most comprehensive measure of a currency's competitiveness.

**How to use REER**: When a country's REER is at historical highs, its exports become less competitive, its imports become cheaper, and the currency is "expensive" in trade-weighted terms. This creates a gravitational pull toward depreciation, though the timing is uncertain.

The BIS publishes REER data for all major currencies. Persistent REER overvaluation (2+ standard deviations above average) historically precedes significant currency weakness, though the lead time can be years.

## The Dollar Wrecking Ball

The US dollar is not just another currency — it is the global reserve currency, the primary funding currency for international trade, and the denomination for most commodity pricing. Dollar movements have outsized effects on global markets.

### How Dollar Strength Affects Asset Classes

**Equities**:
- US large caps: Mixed. Strong dollar reduces the value of overseas earnings when translated back to USD (negative for ~40% of S&P 500 revenue that comes from abroad). But strong dollar reflects US economic strength (positive for domestic earnings).
- US small caps: Neutral to positive. Small caps are domestically focused, so dollar strength does not hurt earnings translation.
- International developed equities: Negative. Strong dollar reduces returns for US-based investors in two ways — local equity returns may suffer due to tighter global financial conditions, and currency translation losses reduce dollar returns.
- Emerging market equities: Very negative. Dollar strength tightens EM financial conditions (dollar-denominated debt becomes more expensive to service), triggers capital outflows from EM, and depresses commodity prices (which many EM economies depend on).

**Fixed income**:
- US Treasuries: Neutral to positive. Dollar strength can attract foreign capital into Treasuries (supporting prices). But strong dollar often accompanies higher US rates, which is negative for existing bond positions.
- EM debt: Very negative. Dollar strength is the single biggest risk factor for EM debt — it increases the real burden of dollar-denominated debt and triggers sell-offs.
- Credit: Moderate negative. Dollar strength tightens global financial conditions, which widens credit spreads.

**Commodities**: Negative. Most commodities are priced in dollars. A stronger dollar makes commodities more expensive for non-dollar buyers, reducing demand and depressing prices. The inverse is equally powerful — a weakening dollar is one of the most reliable tailwinds for commodity prices.

### The Dollar Smile Theory

The dollar tends to strengthen in two very different environments, creating a "smile" shape:

**Left side of the smile (risk-off)**: During global crises, the dollar strengthens as a safe haven. Despite being the reserve currency of the country that may have caused the crisis (2008), the dollar rallies because:
- Dollar-denominated debts must be serviced, creating dollar demand.
- Flight to the most liquid asset in the world (US Treasuries, which require dollars).
- Unwinding of dollar-funded carry trades creates dollar buying pressure.

**Right side of the smile (US outperformance)**: When the US economy is growing faster than the rest of the world, the dollar strengthens because:
- Higher US rates attract capital flows.
- Stronger US growth attracts equity investment.
- US exceptionalism narrative drives speculative flows.

**Bottom of the smile (benign global growth)**: When global growth is synchronized and positive, the dollar weakens because:
- Investors move out on the risk curve, selling safe-haven dollars for higher-returning assets.
- Carry trades are funded in dollars and invested in higher-yielding currencies.
- Commodity prices rise, benefiting commodity-exporting currencies at the dollar's expense.

## Carry Trade Mechanics

### How Carry Trades Work

Borrow in a low-interest-rate currency (the "funding currency"), convert to a high-interest-rate currency (the "carry currency"), invest in high-yielding assets. Earn the interest rate differential.

**Classic carry pairs**: Borrow JPY (near-zero rates) or CHF (low rates), invest in AUD, NZD, MXN, BRL, or ZAR (high rates).

**Expected return**: The interest rate differential, minus any currency depreciation of the carry currency.

### Why Carry Works (Most of the Time)

The carry trade has historically generated positive returns because uncovered interest rate parity fails — high-yielding currencies do not depreciate enough to offset their yield advantage. This creates a persistent "carry premium." Explanations include:
- **Risk premium**: High-yielding currencies are riskier (more volatile, less liquid, in countries with weaker institutions). Carry returns are compensation for bearing this risk.
- **Peso problem**: Carry currencies occasionally crash (the name comes from the Mexican peso crises). The slow accumulation of carry returns is periodically wiped out by sudden devaluations. Investors earn a premium for accepting this negative skew.
- **Central bank behavior**: Central banks in high-yield countries often intervene to prevent depreciation, providing a floor under the carry currency.

### When Carry Fails

Carry trade unwinds are among the most violent events in financial markets:

- **Risk-off events**: When global risk appetite collapses, carry trades unwind simultaneously. Everyone tries to buy back the funding currency (JPY, CHF) at the same time, causing massive spikes. The JPY carry trade unwind in August 2024 caused a 10%+ JPY appreciation in days.
- **Sudden policy changes**: When a central bank in a carry destination unexpectedly cuts rates or imposes capital controls, the carry currency can collapse.
- **Volatility spikes**: Carry trades are implicitly short volatility. When FX volatility spikes (measured by CVIX or JPY implied volatility), carry trades produce losses.

**Risk management for carry**: Size positions based on potential drawdown, not yield. Use stop losses. Diversify across multiple carry pairs. Reduce carry exposure when volatility is low (complacency signal) or when speculative positioning is extreme.

## Major Currency Dynamics

### US Dollar (USD)

The global reserve currency. Its strength or weakness sets the tone for all other asset classes. Key drivers: Fed policy relative to other central banks, US economic growth relative to rest of world, geopolitical risk (safe-haven demand), fiscal position (long-term).

### Euro (EUR)

The second most important currency. Driven by ECB policy, European economic growth (Germany is the bellwether), political stability (Italian spreads, French fiscal concerns, EU cohesion), and current account surplus/deficit dynamics. The euro tends to appreciate when global growth is synchronized (bottom of the dollar smile).

### Japanese Yen (JPY)

The classic safe-haven and funding currency. Driven by Bank of Japan policy (rate differentials with the US), Japanese institutional investor behavior (GPIF, lifers, banks), and global risk appetite (yen strengthens in risk-off). The yen's extreme weakness since 2022 is driven by the massive rate differential with the US. When this differential narrows, the yen is likely to appreciate significantly.

### British Pound (GBP)

A hybrid — carries higher yield than EUR/JPY but has safe-haven characteristics as a G7 currency. Vulnerable to UK-specific political risk and fiscal concerns. The UK's persistent current account deficit is a structural headwind.

### Swiss Franc (CHF)

The ultimate safe-haven currency. The Swiss National Bank has historically intervened to prevent excessive appreciation. CHF strengthens during European political crises, global risk-off events, and periods of banking system stress.

### Australian Dollar (AUD)

A commodity currency closely tied to Chinese economic activity and commodity prices (iron ore, copper, coal). AUD is a pure play on the global growth and China cycle. Also a popular carry destination due to historically higher interest rates.

### Canadian Dollar (CAD)

An energy currency closely tied to oil prices and US economic activity (Canada's largest trading partner). CAD tends to move with oil prices and the US business cycle.

## Emerging Market Currencies

### Key Concepts

**Risk premium**: EM currencies carry a risk premium — higher interest rates compensate for higher political risk, weaker institutions, and lower liquidity. This premium is earned slowly (through carry) and lost quickly (during crises).

**Intervention**: Many EM central banks actively intervene in FX markets to manage volatility and prevent excessive appreciation or depreciation. Intervention can be direct (buying/selling FX reserves) or indirect (adjusting interest rates, imposing capital controls, implementing macroprudential measures).

**Capital controls**: Some countries restrict the free flow of capital in and out. China's capital controls are the most significant — the RMB is managed within a band by the PBOC, and foreign investor access is limited. Capital controls reduce volatility but also reduce liquidity and can trap capital during crises.

**Dollarization risk**: Countries with high dollar-denominated debt and inadequate FX reserves face dollarization risk — if the currency weakens significantly, the real burden of dollar debt increases, causing further economic stress and further currency weakness, in a vicious spiral.

### Key EM Currencies

- **Chinese Yuan (CNY/CNH)**: Managed by the PBOC. The onshore (CNY) and offshore (CNH) rates can diverge during stress. China's massive reserves provide buffer, but capital flow pressures from property crisis and growth slowdown create depreciation pressure.
- **Indian Rupee (INR)**: Managed float with active RBI intervention. Structural depreciation trend (2-3% per year) driven by India's current account deficit and inflation differential. But India's strong growth and reform trajectory make it a favored EM investment destination.
- **Mexican Peso (MXN)**: The most liquid EM currency. Popular carry trade target due to high interest rates. Near-shoring tailwind as supply chains diversify from China. But political risk and US trade policy create episodic volatility.
- **Brazilian Real (BRL)**: High-yielding, volatile, commodity-linked. Brazil's commodity exports provide natural FX support, but fiscal concerns and political uncertainty create persistent volatility. One of the highest real interest rates in the world.

## Currency as an Asset Class

### Strategic FX Positions

Currencies can be held as standalone positions, not just as a byproduct of equity or bond investments:

**Trend following in FX**: FX markets exhibit persistent trends due to central bank policy cycles, capital flow persistence, and behavioral biases. Systematic trend-following strategies in FX have generated positive returns with low correlation to traditional assets. The key: trends in FX are driven by fundamental factors (rate differentials, growth differentials) that persist for months or years.

**Carry strategies**: Systematically long high-yield currencies, short low-yield currencies. Historically the most profitable FX strategy in normal times, with the caveat of periodic crash risk.

**Value strategies**: Buy undervalued currencies (below PPP), sell overvalued currencies. Long-term positive returns but requires patience — deviations from fair value can persist for years.

**The optimal combination**: Academic research suggests that combining carry, trend, and value signals in FX produces returns with higher Sharpe ratios than any single strategy. The diversification benefit comes from the strategies performing well in different environments — carry in calm markets, trend in trending markets, value over long horizons.

## Central Bank Intervention and Reserves Management

### Why Central Banks Intervene

- **Prevent excessive volatility**: Rapid currency movements disrupt trade, create inflationary pressure, and stress dollar-denominated debtors.
- **Competitive devaluation**: Keeping the currency weak to support exports (Japan 2013-2015, China historically).
- **Defend a peg or band**: Some currencies are pegged to the dollar (Hong Kong, Gulf states) or managed within a band (China, Singapore). The central bank must intervene to maintain the peg.
- **Accumulate reserves**: EM central banks build FX reserves as insurance against crises. This typically involves buying dollars (selling local currency), which keeps the local currency weaker than it would otherwise be.

### Reserves as a Buffer

Global FX reserves exceed $12 trillion. China holds approximately $3.2 trillion, Japan approximately $1.2 trillion. Adequate reserves are measured by:
- **Months of import cover**: Below 3 months is dangerously low.
- **Short-term debt cover**: Reserves should exceed short-term external debt (the Greenspan-Guidotti rule).
- **ARA metric (IMF)**: A composite measure that accounts for imports, short-term debt, money supply, and portfolio liabilities. Below 100% of ARA is a warning sign.

## Practical Framework: FX Implications for Portfolio Positioning

### Step 1: Assess Dollar Direction

This is the single most impactful FX call. Use the dollar smile framework:
- Risk-off environment → dollar strengthens → reduce EM, reduce commodities, increase US assets.
- US outperformance → dollar strengthens → same positioning but for different reasons.
- Synchronized global growth → dollar weakens → increase international equities, increase EM, increase commodities.

### Step 2: Determine Hedging Policy

**Equity exposure**: The academic consensus is that currency hedging adds little value for equity portfolios over the long term because equity volatility dominates FX volatility. Practical recommendation: hedge 0-50% of developed market equity FX exposure, depending on conviction about dollar direction. Do not hedge EM equity FX — the cost is too high and the EM equity premium partially compensates for FX risk.

**Fixed income exposure**: Always hedge. Bond returns are small relative to FX volatility, so unhedged foreign bonds are primarily a currency bet, not a bond investment. The exception is EM local-currency debt, where the FX risk is the point (you are earning a risk premium for taking it).

**Alternative assets**: Typically unhedged. Private equity, real estate, and infrastructure are long-duration, illiquid assets where FX hedging is impractical and costly.

### Step 3: Consider Tactical FX Positions

If you have a strong view on a specific currency:
- Express it through the asset class that benefits most (e.g., if you are bullish on a weak yen, buy Japanese exporters rather than shorting JPY directly — you get equity returns plus FX benefits).
- Use FX forwards or options for pure FX views. Options provide defined risk.
- Size FX positions modestly — currency moves are notoriously difficult to predict, and leverage in FX amplifies mistakes.

### Step 4: Monitor FX Volatility

Low FX volatility is a precondition for carry trades and risk-taking. When FX volatility spikes (watch CVIX, JPY implied vol, EM FX implied vol):
- Reduce carry trade exposure.
- Increase hedging ratios.
- Reduce EM and international exposure if not hedged.
- Consider increasing dollar exposure as a safe haven.
