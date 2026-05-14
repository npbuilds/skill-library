---
name: sentiment-signals
description: >
  Modern quantitative sentiment measurement using options-derived data, flow analysis, NLP-based
  text analysis, and alternative data sources. Covers GEX/DEX, 0DTE dynamics, CFTC positioning,
  social media sentiment, FinBERT, and frameworks for building composite sentiment indicators.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Sentiment Signals — The Quantitative Measurement Layer

How to measure market sentiment using modern data sources: options-derived metrics, flow data, natural language processing, and alternative data. Moving beyond surveys and vibes to quantified positioning and behavioral signals.

## Social Media Sentiment Analysis

### Twitter/X Financial Community

The financial community on X has evolved into a real-time sentiment barometer with distinct participant tiers:

**Key account categories**:
- **Macro strategists**: Accounts with institutional-quality macro analysis. Their thesis shifts often precede institutional positioning changes by days to weeks.
- **Options flow accounts**: Real-time reporting of large options transactions. Valuable for reading institutional hedging and speculative bets.
- **Quantitative analysts**: Share research findings, factor performance, and systematic signals. Less sentiment, more information.
- **Retail opinion leaders**: High-follower accounts that influence retail positioning. Their consensus IS the retail sentiment reading.

**Engagement metrics as sentiment signals**:
- Viral bearish threads in a bull market: often marks intermediate bottoms (maximum attention to risk = maximum hedging = maximum contrarian signal)
- Viral bullish threads with massive engagement: Phase 4 marker — the crowd is celebrating
- Ratio of bearish to bullish engagement: sustained shifts in this ratio precede market turns by days
- Account creation spikes in brokerage affiliate links: retail mania indicator

**Limitations**: Survivorship bias in who gets amplified. The loudest voices are not necessarily the most representative. Algorithmic amplification creates artificial consensus that may not reflect actual positioning. Bot activity can distort sentiment readings.

### Reddit — Retail Sentiment and Flows

**WallStreetBets (WSB)**: The most influential retail trading community. Key patterns:
- **Ticker mention frequency**: The rate at which a ticker appears in WSB posts and comments correlates with retail options activity in that name. Spikes in mention frequency precede spikes in options volume.
- **Sentiment polarity of mentions**: Not just frequency but direction — are mentions bullish ("to the moon") or bearish ("puts printing")? NLP classifiers trained on WSB-specific language can quantify this.
- **YOLO post frequency**: Posts showing concentrated single-stock positions signal peak retail conviction in specific names.
- **Loss porn emergence**: Posts celebrating losses signal that the cycle has turned and the community is shifting from greed to coping humor. This is a bottoming indicator for retail-driven names.

**r/investing and r/stocks**: More moderate, longer-term oriented retail communities. Their consensus provides a proxy for the average retail investor's sentiment, distinct from the more speculative WSB population.

**Translating Reddit sentiment to flows**: Retail sentiment on Reddit translates to real market impact through:
- Call option buying on popular tickers → dealer delta hedging → stock buying pressure
- Coordinated buying campaigns (rare but impactful when they occur)
- Retail fund flows into thematic ETFs aligned with popular Reddit narratives

### StockTwits — Quantified Sentiment

**Platform structure**: Designed specifically for stock market discussion. Users tag messages as bullish or bearish when posting about specific tickers.

**Quantified metrics**:
- **Bullish/bearish ratio by ticker**: Direct self-reported sentiment. A ratio > 80% bullish is a contrarian concern; < 30% bullish is contrarian opportunity.
- **Message volume**: Spikes in volume correlate with attention and positioning changes. Volume spikes precede large moves in either direction.
- **Trending tickers**: The top-trending tickers on StockTwits overlap significantly with retail options activity.

**Limitations**: Self-selection bias (users who post are more engaged/extreme than the average investor). The bullish/bearish tagging is voluntary and may not reflect the user's actual position.

### NLP Models for Financial Text

**FinBERT**: A BERT model fine-tuned on financial text for sentiment classification. Pre-trained on financial news, earnings call transcripts, and analyst reports.

**How FinBERT improves over general sentiment models**:
- Understands financial-specific language: "missed estimates" is negative, "beat expectations" is positive — general NLP models may not catch these
- Handles hedging language: "We remain cautious but optimistic" — FinBERT parses the net sentiment; general models may fixate on "cautious" or "optimistic" depending on order
- Domain-specific negation: "No concerns about credit quality" — correctly identifies this as positive, whereas naive models flag "concerns" and "credit quality" as negative

**Application pipeline**:
1. Ingest text sources (news feeds, earnings transcripts, social media, SEC filings)
2. Pre-process: segment into sentences, remove boilerplate
3. Run FinBERT classification: positive, negative, neutral for each segment
4. Aggregate: weighted average by source importance, recency, and relevance
5. Track the time series of aggregate sentiment — level and rate of change

**Beyond FinBERT**: Newer models (GPT-based, domain-specific LLMs) can perform more nuanced analysis including aspect-based sentiment (bullish on revenue, bearish on margins), tone detection (confident vs hedging), and forward-looking vs backward-looking statement classification.

## Options-Derived Sentiment

Options markets contain richer sentiment information than equity markets because options prices embed expectations about the distribution of future returns, not just the point estimate.

### GEX (Gamma Exposure)

**Sentiment reading**: GEX tells you whether the market's structural posture is complacent or fragile. High positive GEX signals a calm, range-bound environment where dealers dampen moves — consistent with complacent sentiment. Negative GEX signals a fragile, amplification-prone environment where dealer hedging exacerbates moves — consistent with fearful or unstable sentiment. The gamma flip level acts as a structural sentiment boundary: above it, calm prevails; below it, fear feeds on itself.

### DEX (Delta Exposure)

**Sentiment reading**: DEX reveals the options market's aggregate directional bet. High positive DEX (heavy call ownership, put selling) signals bullish positioning with fragility underneath. High negative DEX (heavy put ownership) signals bearish positioning with short-squeeze potential. A rapid shift in DEX from positive to negative signals institutional hedging activity and often precedes or accompanies market declines.

### 0DTE (Zero Days to Expiration) Options

**Sentiment reading**: 0DTE activity is a real-time gauge of intraday speculative conviction. Heavy 0DTE call buying signals retail/speculative bullishness and momentum-chasing. Heavy 0DTE put buying signals fear-driven hedging or speculative bearishness. Extreme total 0DTE volume days (> 2x average) signal high engagement and emotional trading — a marker of sentiment extremes in either direction.

For the full mechanical explanation of GEX, dealer hedging dynamics, 0DTE gamma effects, and the gamma flip level, consult the `options-mechanics` knowledge skill in the Market Microstructure subdomain.

### Put/Call Open Interest Ratios

Beyond volume ratios (which measure daily flow), open interest ratios reveal accumulated positioning.

**Term structure of fear**: Examining put/call open interest across expirations reveals the time horizon of hedging:
- Elevated near-term put/call OI: acute fear, hedging against an imminent event (earnings, FOMC, data release)
- Elevated far-term put/call OI: structural hedging, portfolio protection against tail risk
- Elevated across all expirations: pervasive fear — the strongest contrarian buy signal from options data

**Strike distribution analysis**: Where the open interest is concentrated tells you about expectations:
- Concentrated put OI at a specific strike creates a "floor" — dealers who sold those puts will buy shares at that level to hedge
- Concentrated call OI at a specific strike creates a "ceiling" — dealers who sold those calls will sell shares at that level
- These dealer hedging levels become self-reinforcing support and resistance

### Volatility Risk Premium

**Definition**: The spread between implied volatility (what options price) and realized volatility (what actually happens). Implied vol systematically exceeds realized vol because investors pay a premium for hedging (insurance is priced above expected loss).

**Interpreting the VRP**:
- **Wide VRP** (implied >> realized): Market is paying a premium for protection. Fear exceeds actual risk. Selling volatility is profitable in this environment. This is the normal state.
- **Narrow or negative VRP** (implied <= realized): Extremely unusual. Means realized moves are exceeding what the market expected. This occurs during true crisis events (options were underpriced for the actual risk). The collapse of VRP is an acute crisis indicator.
- **VRP trend**: A widening VRP from normal levels signals growing fear/hedging demand. A collapsing VRP from elevated levels signals that fear is resolving (either the feared event didn't materialize or positions are being unwound).

## Flow Data

### CFTC Commitment of Traders (COT)

**What it is**: Weekly report (released Friday for data through Tuesday) showing the aggregate positioning of three trader categories in US futures markets: commercials (hedgers), non-commercials (speculators), and non-reportable (small traders).

**How to read it**:

**Commercials** (hedgers): Companies hedging their core business. In commodity markets, this is producers and consumers. In financial futures, these are institutions hedging exposures.
- Commercials are considered "smart money" because they have informational advantages about supply/demand in their core markets
- When commercials are net long at extremes, it's bullish: the people who KNOW the market best are buying
- When commercials are net short at extremes, it's bearish

**Non-commercials** (large speculators): Hedge funds, CTAs, and large speculative accounts.
- Speculative positioning at extremes is a contrarian indicator: when speculators are max long, the trade is crowded and vulnerable
- The rate of change in speculative positioning is more informative than the level — rapid position-building signals conviction that may be ahead of fundamentals
- Speculative positioning in currency and bond futures is particularly informative for macro regime shifts

**Non-reportable** (small speculators): Retail and small accounts below reporting thresholds.
- Traditionally the "dumb money" — extreme positioning by small specs is the strongest contrarian signal
- However, this category has become less informative as trading has shifted from futures to options and CFDs

**Key COT signals by market**:
- **S&P 500 futures**: Large speculator net positioning extremes are 60-70% accurate as contrarian signals over 1-3 month horizons
- **Treasury futures**: Large speculator positioning extremes in 10-year note futures are among the best signals for bond market turning points
- **Gold futures**: Commercial hedger positioning (gold miners) at extremes is a reliable signal for gold's medium-term direction
- **Currency futures**: Non-commercial positioning extremes in major currency pairs (EUR, JPY, GBP) reliably signal crowded trades

### ETF Fund Flows

**What it measures**: Net creations and redemptions of ETF shares. When money flows into an ETF, the authorized participant creates shares (buys the underlying); when money flows out, shares are redeemed (sells the underlying).

**Signal interpretation**:
- **Extreme inflows**: Peak enthusiasm. Retail and institutional investors are adding exposure aggressively. Historically coincides with intermediate to major peaks (buying the top).
- **Extreme outflows**: Capitulation. Investors are liquidating regardless of price. Historically coincides with intermediate to major bottoms.
- **Flow-price divergence**: Rising prices + declining flows = smart money distributing. Falling prices + rising flows = value buyers accumulating.

**Specific ETF categories to monitor**:
- **SPY/VOO/IVV** (S&P 500 ETFs): The broadest equity flow signal. Extreme inflows after multi-month rallies are late-cycle indicators.
- **HYG/JNK** (high-yield bond ETFs): Credit risk appetite proxy. Outflows from HY ETFs often precede equity market weakness because credit deteriorates before equity.
- **TLT/IEF** (Treasury ETFs): Safe-haven demand proxy. Inflows during equity weakness confirm risk-off; outflows during equity weakness signal something different (rising rates, inflation fear, not equity fear).
- **GLD/IAU** (gold ETFs): Gold ETF flows correlate with real interest rate expectations and fear of monetary debasement. Extreme inflows often mark gold peaks; extreme outflows mark gold troughs.
- **Sector ETFs**: Rotation between offensive (XLK, XLY) and defensive (XLU, XLP) sectors reveals real-time risk appetite shifts.

### 13F Filings

**What it is**: Quarterly SEC filing required of institutional investment managers with > $100M in AUM. Shows equity holdings as of the end of each quarter. Filed within 45 days of quarter end.

**Value despite the lag**:
- **Identifying crowded positions**: When many top funds hold the same name at large sizes, the position is crowded. Crowded positions are vulnerable to correlated selling.
- **Tracking position changes**: Quarter-over-quarter changes reveal institutional conviction shifts. A position that grows from 3% to 8% of a top fund's portfolio signals high conviction.
- **New position initiation**: When a respected investor initiates a new position, it provides both an analytical signal and a sentiment shift (other investors follow).
- **Complete exits**: When a long-term holder completely exits a position, it signals either a fundamental change in thesis or a valuation extreme.

**Limitations**: 45-day lag means the data is stale. Managers can change positions between quarter-ends. The filing shows long equity holdings only — no shorts, no options, no credit positions. Managers with concentrated portfolios can shift materially within the reporting delay.

### Dark Pool Activity

**What dark pools reveal**: Off-exchange trading venues where large institutional orders execute without displaying to the public order book. Dark pool data reveals institutional behavior that is intentionally hidden from the lit market.

**Sentiment signals from dark pool data**:
- **Dark pool short volume ratio**: The percentage of dark pool volume that is short-sold. Elevated ratios (> 50%) suggest institutional selling pressure; depressed ratios (< 40%) suggest institutional buying.
- **Block trade frequency**: Spikes in large block trades (> 10,000 shares) indicate institutional urgency — either aggressive accumulation or distribution.
- **Dark pool prints above/below midpoint**: Trades executing above the NBBO midpoint suggest buyer urgency; below midpoint suggests seller urgency.

## Alternative Sentiment Sources

### Google Trends — Search Interest as Leading Indicator

**How it works**: Google Trends provides an index (0-100) of search interest for any term over time. In finance, search interest reveals attention allocation — what the public is thinking about.

**Proven applications**:
- **"Stock market crash" searches**: Spikes in this search term have historically coincided with or slightly lagged market drawdowns. However, the spike itself is a contrarian buy signal — by the time the public is searching for "crash," the worst of the selling is usually over.
- **Ticker-specific searches**: Surges in search interest for individual stock tickers precede retail buying activity. This can be exploited for short-term momentum or used as a contrarian fade when search interest reaches extreme levels.
- **"How to invest" or "how to buy stocks"**: Secular spikes in beginner investment searches signal new retail money entering the market — a late-cycle indicator when it reaches extreme levels.
- **Economic anxiety searches**: "Recession," "layoffs," "unemployment benefits" — these searches reflect real economic anxiety and often lead consumer sentiment surveys by 2-4 weeks.

**Methodology**: Always use relative terms. A spike in "bitcoin" searches to 100 means maximum search interest for bitcoin relative to its own history, not that bitcoin is the most searched term overall. Compare the search index to price: when search interest lags price (price is rising but nobody is searching yet), it's Phase 1-2. When search interest leads price (searches spike before price moves), it's retail FOMO in Phase 4.

### Job Postings as Sentiment Proxy

**The signal**: Company-level hiring activity reveals management's confidence in future growth before it shows up in financial statements.

- **Accelerating job postings**: Management is investing in growth — bullish for revenue trajectory
- **Decelerating or freezing postings**: Management is pulling back — bearish signal, often 1-2 quarters before it shows up in earnings
- **Mass layoff announcements**: Can be bullish (cost-cutting that improves profitability) or bearish (demand collapse) — context matters
- **Hiring in specific functions**: What functions are being hired for reveals strategic direction. Hiring sales reps = expecting demand growth. Hiring restructuring specialists = expecting trouble.

**Data sources**: LinkedIn job postings data, Indeed Hiring Lab, Glassdoor, company careers pages (trackable via web scraping), and platforms like Revelio Labs and LinkUp that aggregate and analyze hiring data.

### Earnings Call NLP — Tone Analysis

**What it measures**: Applying NLP to earnings call transcripts to extract sentiment, confidence, and forward-looking guidance beyond the numbers.

**Key dimensions to analyze**:

**Tone analysis**: Is management's language becoming more positive or negative over time? Track the trend, not the absolute level (some CEOs are naturally optimistic, others cautious).

**Hedging language detection**: Words and phrases like "uncertain," "challenging environment," "cautious optimism," "subject to," and "depending on conditions" signal management anxiety that may not be reflected in the reported numbers. An increase in hedging language quarter-over-quarter is a leading indicator of disappointing future results.

**Forward guidance confidence**: Distinguish between:
- High confidence guidance: specific numbers, narrow ranges, clear timelines — "We expect revenue of $2.3-2.4B"
- Low confidence guidance: vague language, wide ranges, conditional statements — "We believe we are well-positioned for growth depending on macro conditions"
- Declining confidence in guidance over sequential quarters is bearish even if the numbers are still meeting expectations

**Q&A section analysis**: The Q&A portion of earnings calls is more informative than the prepared remarks because management cannot fully control the narrative. Key signals:
- Evasive answers to direct questions (topic-switching, answering a different question)
- Increased frequency of "I'll let [CFO] address that" deferrals
- Changes in which executives answer which types of questions
- Tone shifts between prepared remarks (scripted, optimistic) and Q&A (defensive, hedging)

### News Sentiment Aggregators

**How headlines map to price action**: Academic research consistently finds that news sentiment has predictive power for subsequent returns, but the relationship is nonlinear.

**Key findings**:
- **Extreme negative news sentiment** (> 2 standard deviations below average) precedes above-average returns over 1-5 day horizons — consistent with overreaction and contrarian reversal
- **Moderate negative sentiment** has weak or no predictive power — the market digests moderate bad news efficiently
- **Extreme positive sentiment** has weak predictive power for subsequent returns — the market is approximately efficient at pricing good news
- **News sentiment momentum**: A sustained shift in news sentiment (positive to negative or vice versa over weeks) is more informative than single-day extremes

**Aggregation sources**: RavenPack, Bloomberg News Sentiment, Refinitiv MarketPsych, Alexandria Technology (now part of S&P Global). These services ingest thousands of news sources, apply NLP classification, and produce real-time sentiment scores by asset, sector, and topic.

**News vs social media sentiment divergence**: When professional news sentiment diverges from social media sentiment, it often signals:
- News negative + social positive: retail hasn't absorbed the implications yet → bearish
- News positive + social negative: retail is still shell-shocked from recent losses → bullish (retail sentiment is the lagging indicator)

## Building a Modern Sentiment Composite

### Design Principles

1. **Multiple independent sources**: A composite should blend survey-based, flow-based, options-derived, and text-based signals. The power comes from independence — when independently derived signals agree, the confidence is high.

2. **Normalize everything**: Each component operates on different scales. Z-score normalize each component relative to its own history (1-year rolling or 3-year rolling) to make them comparable.

3. **Weight by reliability**: Not all signals are equally informative. Empirically, options-derived signals (GEX, skew, VRP) and flow data (COT, ETF flows) tend to have higher hit rates than survey-based or social media signals. Weight accordingly:
   - Options-derived signals: 30-35% weight
   - Flow data (COT, ETF, 13F): 25-30% weight
   - Survey data (AAII, fund manager): 15-20% weight
   - Social/alternative data (NLP, search, social media): 15-20% weight

4. **Track level and rate of change**: Both the current reading and the direction of change matter. A composite at -1.5 standard deviations (bearish) that is getting MORE bearish is different from one at -1.5 that is starting to recover.

5. **Time horizon matching**: Short-term signals (0DTE flows, intraday GEX) should not be blended with long-term signals (13F filings, monthly COT) in the same composite. Build separate composites for:
   - **Tactical** (1-5 day horizon): 0DTE flows, intraday GEX, put/call ratio, social media momentum
   - **Intermediate** (1-3 month horizon): COT positioning, ETF flows, VIX term structure, AAII, fund manager surveys
   - **Strategic** (3-12 month horizon): Margin debt, 13F positioning changes, earnings call NLP trends, credit flow data

### Composite Construction

**Step 1**: Select components (4-8 per time horizon)

**Step 2**: Normalize each to z-scores using rolling window appropriate to the time horizon
- Tactical: 20-day rolling z-score
- Intermediate: 63-day (1-quarter) rolling z-score
- Strategic: 252-day (1-year) rolling z-score

**Step 3**: Apply weights based on empirical reliability and theoretical independence

**Step 4**: Sum weighted z-scores to produce composite reading

**Step 5**: Interpret:
- Composite > +1.5 sigma: Extreme bullish sentiment. Contrarian bearish setup.
- Composite +0.5 to +1.5: Moderately bullish. No strong contrarian signal.
- Composite -0.5 to +0.5: Neutral. No sentiment signal.
- Composite -0.5 to -1.5: Moderately bearish. No strong contrarian signal.
- Composite < -1.5 sigma: Extreme bearish sentiment. Contrarian bullish setup.

**Step 6**: Validate: Backtest the composite against subsequent returns over the relevant time horizon. A good composite should show:
- Positive subsequent returns following extreme bearish readings
- Negative subsequent returns following extreme bullish readings
- Monotonic relationship between composite quintile and subsequent return

### Common Pitfalls

- **Overfitting**: Adding more signals doesn't always improve the composite. If two signals are highly correlated (e.g., VIX level and put/call ratio), including both adds noise, not information. Test incremental value before adding.
- **Look-ahead bias**: Ensure all data was available at the time of the signal. COT data has a 3-day lag; 13F has a 45-day lag. Backtest with these realistic lags.
- **Survivorship of signals**: Some sentiment signals that worked historically may stop working as they become widely known and traded against. The most crowded signals are the most at risk of degradation.
- **Regime dependence**: Sentiment signals work differently in different macro regimes. In a secular bull market, extreme bullish sentiment readings are less reliable as sell signals. In a bear market, extreme bearish readings may mark intermediate bottoms but not THE bottom.
- **Confusing sentiment with positioning**: Sentiment (what people believe) and positioning (what people have done) can diverge. Someone who is bearish but fully invested is different from someone who is bearish and 100% cash. Always prefer positioning data over opinion data when both are available.

## Cross-Domain Connections

- **Data-science/data-wrangling/feature-engineering**: Building a sentiment composite is multi-source feature engineering — normalizing heterogeneous signals (VIX, put/call ratios, AAII surveys, NLP scores) into a unified feature space with appropriate weighting and temporal alignment.
- **Data-science/ml-engineering/drift-detection**: Sentiment signals degrade as they become crowded. Monitoring signal efficacy over time (does extreme fear still predict above-average forward returns?) is drift detection applied to sentiment factors.



## Related Skills

- **alt-data-monitoring** — Many sentiment signals are built on alternative data feeds. Pair with alt-data-monitoring when the sentiment construction depends on non-traditional inputs (text scrapes, transaction data, satellite).
- **market-psychology** — Market-psychology provides the qualitative theory that sentiment-signals quantify. Read market-psychology to understand WHY a sentiment regime persists or breaks.
