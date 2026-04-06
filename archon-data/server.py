"""Archon Data — MCP server for live investment intelligence.

Exposes market data, macro indicators, sentiment analysis, and risk metrics
as MCP tools that the Archon skill and React dashboard can consume.
"""

import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

mcp = FastMCP(
    "Archon Data",
    instructions=(
        "Live investment data pipeline for the Archon investment intelligence system. "
        "Provides regime classification, sentiment analysis, market snapshots, "
        "cross-asset performance, insider signals, risk dashboards, and "
        "private markets monitoring (RE, credit, PE/VC exit window). "
        "Data is cached with TTLs to avoid excessive API calls. "
        "FRED data requires FRED_API_KEY environment variable."
    ),
)


@mcp.tool()
def get_regime() -> dict:
    """Get the current macroeconomic regime classification (Dalio's 2x2 quadrant).

    Returns the current regime (goldilocks/reflation/stagflation/deflation),
    confidence score, underlying macro indicators from FRED (GDP, unemployment,
    CPI, PCE, Fed funds, M2), and yield curve analysis. Requires FRED_API_KEY
    env var for full macro data; falls back to yield curve only without it.
    """
    from collectors.fred import get_macro_data
    from collectors.treasury import get_yield_curve
    from processors.regime import classify_regime

    macro = get_macro_data()
    yields = get_yield_curve()
    regime = classify_regime(macro, yields)

    return {
        "regime": regime,
        "macro_indicators": macro,
        "yield_curve": yields,
    }


@mcp.tool()
def get_sentiment() -> dict:
    """Get the current market sentiment dashboard.

    Returns a composite sentiment score (0-100, fear→greed), VIX level and
    term structure, CNN Fear/Greed Index, put/call context, and market breadth
    analysis. All data from free sources (yfinance, CNN).
    """
    from collectors.market import get_market_snapshot
    from collectors.sentiment import get_sentiment_dashboard
    from processors.sentiment_score import compute_sentiment_score

    sentiment = get_sentiment_dashboard()
    market = get_market_snapshot()
    composite = compute_sentiment_score(sentiment, market)

    return {
        "composite": composite,
        "raw_indicators": sentiment,
        "breadth": {
            "divergence": market.get("breadth_divergence"),
            "signal": market.get("breadth_signal"),
        },
    }


@mcp.tool()
def market_snapshot() -> dict:
    """Get current market levels, YTD performance, breadth, and sector rotation.

    Returns S&P 500, Nasdaq, Russell 2000 levels and YTD returns, SPY vs RSP
    breadth analysis, and sector ETF performance with leaders/laggards.
    """
    from collectors.market import get_market_snapshot, get_sector_performance

    return {
        "market": get_market_snapshot(),
        "sectors": get_sector_performance(),
    }


@mcp.tool()
def get_asset_performance() -> dict:
    """Get cross-asset performance table (equities, bonds, gold, oil, BTC, USD).

    Returns current prices, YTD and 1-month returns for major indices,
    treasuries (TLT), high yield (HYG), gold (GLD), oil (USO), Bitcoin,
    and the Dollar Index.
    """
    from collectors.market import get_asset_performance as _perf

    return _perf()


@mcp.tool()
def get_insider_signals() -> dict:
    """Get recent insider buying signals from OpenInsider.

    Returns notable insider purchases (>$100K) from the last 30 days,
    with cluster buy detection (multiple insiders buying the same ticker).
    Cluster buys are among the highest-signal free datasets available.
    """
    from collectors.insider import get_insider_buys

    return get_insider_buys()


@mcp.tool()
def get_risk_dashboard() -> dict:
    """Get the risk dashboard — correlations, VIX regime, yield curve, breadth.

    Returns 30-day rolling correlation matrix for key assets (stocks, bonds,
    gold, oil, dollar, bitcoin), stock-bond correlation regime, VIX term
    structure analysis, yield curve shape, and an overall risk level.
    """
    from collectors.market import get_market_snapshot as _snapshot
    from collectors.sentiment import get_sentiment_dashboard
    from collectors.treasury import get_yield_curve
    from processors.risk import get_risk_dashboard as _risk

    sentiment = get_sentiment_dashboard()
    yields = get_yield_curve()
    market = _snapshot()

    return _risk(sentiment, yields, market)


@mcp.tool()
def get_cot_positioning() -> dict:
    """Get CFTC Commitments of Traders data — institutional futures positioning.

    Returns net speculative positioning for key contracts (S&P 500, Treasuries,
    gold, oil, euro, yen, bitcoin, VIX), with extreme readings flagged.
    Updated weekly. Crowded longs/shorts are among the highest-signal
    contrarian indicators available for free.
    """
    from collectors.cot import get_cot_positioning as _cot

    return _cot()


@mcp.tool()
def get_factor_returns() -> dict:
    """Get academic factor returns from Kenneth French Data Library.

    Returns daily Mkt-RF, SMB (size), HML (value), and UMD (momentum)
    factor returns with 5-day and 30-day cumulative performance,
    plus a factor regime assessment (value rotation, momentum crash, etc.).
    """
    from collectors.factors import get_factor_returns as _factors

    return _factors()


@mcp.tool()
def get_geopolitical_monitor() -> dict:
    """Get real-time geopolitical event monitoring from GDELT Project.

    Tracks article volume and sentiment tone across key hotspots:
    Iran conflict, China-Taiwan, Russia-Ukraine, US-China trade,
    Middle East, and AI regulation. Flags surging coverage as alerts
    with affected market mapping.
    """
    from collectors.gdelt import get_geopolitical_monitor as _geo

    return _geo()


@mcp.tool()
def get_special_situations() -> dict:
    """Get special situation filings from SEC EDGAR.

    Returns recent SC 13D filings (activist stakes >5%), S-1 filings
    (IPOs/spinoffs), and DEFA14A filings (proxy/M&A). Identifies
    potential special situation opportunities per Greenblatt's framework.
    """
    from collectors.sec_edgar import get_special_situation_filings

    return get_special_situation_filings()


@mcp.tool()
def get_13f_filings() -> dict:
    """Get recent 13F-HR institutional holdings filings from SEC EDGAR.

    Returns the most recent institutional holdings disclosures, showing
    which major institutions have filed updated portfolio positions.
    """
    from collectors.sec_edgar import get_recent_13f_filings

    return get_recent_13f_filings()


@mcp.tool()
def get_google_trends() -> dict:
    """Get Google Trends data for investment-relevant search terms.

    Tracks search interest for fear-related terms (recession, crash),
    greed-related terms (buy stocks, best stocks), inflation, crypto,
    housing, and geopolitical themes. Spikes in fear terms are
    historically contrarian bullish at extremes.
    """
    from collectors.google_trends import get_trend_signals

    return get_trend_signals()


@mcp.tool()
def get_crypto_dashboard() -> dict:
    """Get comprehensive crypto market data from CoinGecko.

    Returns total market cap, BTC/ETH dominance, top coin prices and
    changes (24h/7d/30d), trending coins, crypto Fear & Greed Index,
    DeFi stats, and a crypto regime classification.
    """
    from collectors.coingecko import get_crypto_dashboard as _crypto

    return _crypto()


@mcp.tool()
def get_earnings_calendar() -> dict:
    """Get upcoming earnings dates for major companies (6-week lookahead).

    Tracks Magnificent 7, major financials, healthcare, energy, consumer,
    and semiconductor companies. Groups by week and identifies
    catalyst-dense periods where multiple large-caps report.
    """
    from collectors.earnings import get_earnings_calendar as _earnings

    return _earnings()


@mcp.tool()
def get_fed_game() -> dict:
    """Get the Fed game theory analysis — strategic interaction modeling.

    Models the Fed-Market-Fiscal interaction as a multi-player game.
    Returns the Fed's strategic position and constraints, what the bond
    market is pricing, where market expectations diverge from game equilibrium,
    probability-weighted Fed action scenarios, the dominant strategy, and
    fiscal dominance assessment. Powers the Fed-focused commentary in §7
    and the predictions section §15.
    """
    from collectors.fred import get_macro_data
    from collectors.treasury import get_yield_curve
    from processors.regime import classify_regime
    from processors.fed_game import analyze_fed_game

    macro = get_macro_data()
    yields = get_yield_curve()
    regime = classify_regime(macro, yields)

    return analyze_fed_game(regime=regime, macro=macro, yields=yields)


@mcp.tool()
def get_fund_flows() -> dict:
    """Get ETF-based fund flow proxy signals.

    Analyzes volume patterns across 17 key ETFs (equities, fixed income,
    alternatives, sectors) to detect institutional capital rotation.
    Returns per-ETF flow signals (accumulation/distribution/capitulation/
    squeeze), asset class aggregates, rotation patterns, and an overall
    risk appetite score (0=extreme risk-off, 100=extreme risk-on).
    """
    from collectors.fund_flows import get_fund_flow_proxies

    return get_fund_flow_proxies()


@mcp.tool()
def get_alerts() -> dict:
    """Get the alert feed — threshold-based signals across all data sources.

    Scans the full briefing data for conditions that warrant attention:
    regime shifts, VIX extremes, credit stress, crowded positioning,
    breadth divergences, private market signals, upcoming catalysts,
    and correlation regime changes. Each alert has a severity level
    (critical/warning/watch), investor framework mapping, and an
    actionability note.
    """
    from processors.alerts import generate_alerts

    briefing = generate_briefing()
    return generate_alerts(briefing)


@mcp.tool()
def get_economic_calendar() -> dict:
    """Get upcoming economic data releases and Fed speaker context.

    Returns a 3-week lookahead of high-impact economic releases (CPI, NFP,
    GDP, FOMC, retail sales, ISM) with impact levels and days until release,
    catalyst-dense week identification, and Fed official roster with hawk/dove
    classifications. Uses FRED release calendar API if FRED_API_KEY is set,
    otherwise falls back to a static estimated calendar.
    """
    from collectors.econ_calendar import get_economic_calendar as _cal

    return _cal()


@mcp.tool()
def get_contrarian_scorecard() -> dict:
    """Get the contrarian scorecard — consensus beliefs vs. second-level thinking.

    Synthesizes COT positioning, sentiment, Google trends, market breadth,
    and private markets data into a structured matrix of where consensus is
    likely wrong. Returns Marks's pendulum position (fear↔greed), specific
    contrarian views with evidence chains, crowding alerts, and confidence
    tags. Powers §2 Consensus vs. Contrarian in the briefing protocol.
    """
    from collectors.cot import get_cot_positioning as _cot
    from collectors.google_trends import get_trend_signals
    from collectors.market import (
        get_asset_performance as _assets,
        get_market_snapshot as _snapshot,
        get_private_market_proxies,
        get_sector_performance,
    )
    from collectors.fred import get_macro_data, get_private_market_macro
    from collectors.sentiment import get_sentiment_dashboard
    from collectors.treasury import get_yield_curve
    from processors.contrarian import compute_contrarian_scorecard
    from processors.private_markets import get_private_markets_dashboard
    from processors.regime import classify_regime
    from processors.sentiment_score import compute_sentiment_score

    # Collect
    sentiment_raw = get_sentiment_dashboard()
    market = _snapshot()
    composite = compute_sentiment_score(sentiment_raw, market)
    sentiment = {"composite": composite, "raw": sentiment_raw}
    cot = _cot()
    trends = get_trend_signals()
    assets = _assets()
    sectors = get_sector_performance()

    macro = get_macro_data()
    yields = get_yield_curve()
    regime = classify_regime(macro, yields)

    fred_pm = get_private_market_macro()
    proxies = get_private_market_proxies()
    pm = get_private_markets_dashboard(fred_pm, proxies)

    return compute_contrarian_scorecard(
        sentiment=sentiment,
        cot=cot,
        trends=trends,
        market=market,
        regime=regime,
        risk={},  # Risk dashboard not needed for contrarian scoring
        private_markets=pm,
        assets=assets,
        sectors=sectors,
    )


@mcp.tool()
def get_private_markets() -> dict:
    """Get the private markets monitor — real estate cycle, credit cycle, PE/VC exit window.

    Synthesizes FRED macro data (mortgage rates, housing starts, credit spreads,
    lending standards) with public market proxy data (REITs, BDCs, PE GP stocks,
    VC proxy ETFs) to classify private market cycles and detect public-private
    valuation divergence. Divergence signals future write-downs in private marks.
    """
    from collectors.fred import get_private_market_macro
    from collectors.market import get_private_market_proxies
    from processors.private_markets import get_private_markets_dashboard

    fred_data = get_private_market_macro()
    proxy_data = get_private_market_proxies()

    return get_private_markets_dashboard(fred_data, proxy_data)


@mcp.tool()
def generate_briefing() -> dict:
    """Generate a complete Archon investment intelligence briefing.

    Assembles the full data package for the briefing protocol by calling
    all data collectors and processors: regime, sentiment, market snapshot,
    sectors, cross-asset, COT, factors, geopolitical, crypto, trends,
    special situations, insider signals, earnings, private markets,
    economic calendar, fund flows, contrarian scorecard, and Fed game
    theory analysis.
    """
    from collectors.coingecko import get_crypto_dashboard as _crypto
    from collectors.cot import get_cot_positioning as _cot
    from collectors.earnings import get_earnings_calendar as _earnings
    from collectors.econ_calendar import get_economic_calendar as _calendar
    from collectors.factors import get_factor_returns as _factors
    from collectors.fred import get_macro_data, get_private_market_macro
    from collectors.fund_flows import get_fund_flow_proxies as _flows
    from collectors.gdelt import get_geopolitical_monitor as _geo
    from collectors.google_trends import get_trend_signals
    from collectors.insider import get_insider_buys
    from collectors.market import (
        get_asset_performance as _assets,
        get_market_snapshot as _snapshot,
        get_private_market_proxies,
        get_sector_performance,
    )
    from collectors.sec_edgar import (
        get_recent_13f_filings,
        get_special_situation_filings,
    )
    from collectors.sentiment import get_sentiment_dashboard
    from collectors.treasury import get_yield_curve
    from processors.private_markets import get_private_markets_dashboard
    from processors.regime import classify_regime
    from processors.risk import get_risk_dashboard as _risk
    from processors.sentiment_score import compute_sentiment_score

    # ── Core market data ──────────────────────────────────────
    macro = get_macro_data()
    yields = get_yield_curve()
    market = _snapshot()
    sectors = get_sector_performance()
    assets = _assets()
    sentiment = get_sentiment_dashboard()
    insiders = get_insider_buys()

    # ── Extended data sources ─────────────────────────────────
    cot = _cot()
    factors = _factors()
    geo = _geo()
    crypto = _crypto()
    trends = get_trend_signals()
    special_situations = get_special_situation_filings()
    filings_13f = get_recent_13f_filings()
    earnings = _earnings()
    fund_flows = _flows()

    # ── Private markets ───────────────────────────────────────
    fred_private = get_private_market_macro()
    proxies = get_private_market_proxies()

    # ── Process ───────────────────────────────────────────────
    regime = classify_regime(macro, yields)
    composite_sentiment = compute_sentiment_score(sentiment, market)
    sentiment_bundle = {"composite": composite_sentiment, "raw": sentiment}
    risk = _risk(sentiment, yields, market)
    private_markets = get_private_markets_dashboard(fred_private, proxies)

    # ── Economic calendar ──────────────────────────────────────
    calendar = _calendar()

    # ── Fed game theory (§7, §15) ────────────────────────────
    from processors.fed_game import analyze_fed_game

    fed_game = analyze_fed_game(regime=regime, macro=macro, yields=yields)

    # ── Contrarian scorecard (§2) ────────────────────────────
    from processors.contrarian import compute_contrarian_scorecard

    contrarian = compute_contrarian_scorecard(
        sentiment=sentiment_bundle,
        cot=cot,
        trends=trends,
        market=market,
        regime=regime,
        risk=risk,
        private_markets=private_markets,
        assets=assets,
        sectors=sectors,
    )

    return {
        # §1 Regime + §7 Macro
        "regime": regime,
        "macro": macro,
        "yield_curve": yields,
        # §2 Consensus vs. Contrarian
        "contrarian": contrarian,
        # §3 Vitals
        "sentiment": sentiment_bundle,
        # §4 Equities + §5 Sectors + §6 Cross-Asset
        "market": market,
        "sectors": sectors,
        "assets": assets,
        # §8 Risk
        "risk": risk,
        # §9 Factors
        "factors": factors,
        # §10 CFTC Positioning
        "cot_positioning": cot,
        # §11 Special Situations + Insider Signals
        "insiders": insiders,
        "special_situations": special_situations,
        "filings_13f": filings_13f,
        # §11.5 Private Markets
        "private_markets": private_markets,
        # §12 Geopolitical
        "geopolitical": geo,
        # §13 Crypto
        "crypto": crypto,
        # §14 Behavioral / Google Trends
        "trends": trends,
        # §17 Earnings Calendar
        "earnings": earnings,
        # Catalyst calendar
        "calendar": calendar,
        # Fund flows
        "fund_flows": fund_flows,
        # Fed game theory
        "fed_game": fed_game,
    }


@mcp.tool()
def save_snapshot(for_date: str = "") -> dict:
    """Save today's briefing data as a permanent daily snapshot.

    Generates a full briefing and persists it to archon-data/snapshots/YYYY-MM-DD.json.
    This enables the Delta Block (§0) which diffs today vs prior day.
    Call this after reviewing a briefing to persist it for future comparison.

    Args:
        for_date: Optional date (YYYY-MM-DD). Defaults to today.
    """
    from processors.persistence import save_daily_snapshot

    briefing = generate_briefing()
    path = save_daily_snapshot(briefing, for_date=for_date or None)

    return {
        "status": "saved",
        "path": path,
        "date": for_date or __import__("datetime").date.today().isoformat(),
        "sections": list(briefing.keys()),
    }


@mcp.tool()
def get_delta() -> dict:
    """Get the Delta Block — what changed since the last saved briefing.

    Generates a fresh briefing, compares it to the most recent saved snapshot,
    and returns structured deltas: market moves, regime changes, threshold
    crossings, leadership changes, private market shifts, and a 3-5 bullet
    summary for §0 of the briefing protocol.
    """
    from processors.persistence import compute_delta, get_prior_snapshot

    current_briefing = generate_briefing()
    prior = get_prior_snapshot()

    if prior is None:
        return {
            "status": "no_prior_snapshot",
            "message": "No prior snapshot found. Run save_snapshot first to establish a baseline.",
            "current_briefing": current_briefing,
        }

    delta = compute_delta({"data": current_briefing}, prior)
    return {
        "status": "ok",
        "delta": delta,
        "current_briefing": current_briefing,
    }


@mcp.tool()
def get_statistical_context(category: str = "", tags: str = "") -> dict:
    """Get statistical base rates and live z-scores for current market conditions.

    Provides empirical grounding for briefing claims. When the Archon says
    "VIX >30 historically reverts within 20 days," this endpoint verifies it
    with actual base rates, confidence intervals, sample sizes, and caveats.

    Returns current readings with z-scores and percentiles, applicable base
    rates for today's conditions, and statistical warnings for extreme readings.

    Args:
        category: Filter base rates by category (volatility, macro, credit, etc.)
        tags: Comma-separated tags to filter by (e.g., "contrarian,vix")
    """
    from processors.statistics import compute_live_statistics, get_base_rates

    briefing = generate_briefing()
    live = compute_live_statistics(briefing)

    # Also include filtered base rate library if requested
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else None
    library = get_base_rates(
        category=category or None,
        tags=tag_list,
    )

    return {
        "live_statistics": live,
        "base_rate_library": library if (category or tags) else {"note": "Pass category or tags to browse the full base rate library"},
    }


@mcp.tool()
def run_stress_test(scenario: str = "") -> dict:
    """Run a scenario stress test — "if X happens, what breaks?"

    Takes a trigger shock and traces the transmission cascade through asset
    classes, sectors, and risk factors. Returns impact estimates adjusted
    for current market vulnerability, portfolio impact across allocation
    types, and framework-specific hedging suggestions.

    Available scenarios: oil_spike, vix_spike, credit_blowout, rate_shock,
    dollar_crash, china_shock, ai_bubble_pop. Call with no scenario to list all.

    Args:
        scenario: Scenario ID from the library (e.g., "oil_spike"). Empty to list all.
    """
    from processors.stress_test import run_stress_test as _stress, list_scenarios

    if not scenario:
        return list_scenarios()

    briefing = generate_briefing()
    return _stress(scenario_id=scenario, briefing=briefing)


@mcp.tool()
def get_historical_analogs() -> dict:
    """Find historical periods most similar to current market conditions.

    Compares the current macro/sentiment/vol/positioning fingerprint against
    a curated library of 12 historical reference periods (COVID crash, GFC,
    2022 stagflation, Volcker, 2017 low-vol, etc.) and any saved Archon
    snapshots older than 30 days. Returns ranked matches with similarity
    scores, forward outcomes from each analog, divergences from today,
    and a composite outlook weighted by similarity. Powers the "what
    rhymes with today?" analysis in §16 of the briefing protocol.
    """
    from processors.analogs import find_analogs

    briefing = generate_briefing()
    return find_analogs(briefing)


@mcp.tool()
def log_prediction(
    claim: str,
    probability: float,
    framework: str,
    category: str,
    resolve_by: str,
    regime_context: str = "",
    evidence: list[str] | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Log a falsifiable prediction for future calibration scoring.

    Records a specific, time-bounded prediction with its assigned probability,
    the investor framework that generated it, and supporting evidence.
    Predictions are stored in snapshots/predictions.json and scored against
    outcomes using Brier scores once resolved.

    Args:
        claim: Specific, falsifiable prediction (e.g., "VIX below 25 by April 15")
        probability: Assigned probability (0.0 to 1.0)
        framework: Investor framework source (e.g., "Marks", "Soros", "Tudor Jones")
        category: Domain (regime, credit, equity, vol, rotation, fed, etc.)
        resolve_by: Resolution deadline (YYYY-MM-DD)
        regime_context: What regime was active when prediction was made
        evidence: Supporting evidence points
        tags: Optional tags for filtering
    """
    from processors.calibration import log_prediction as _log

    return _log(
        claim=claim,
        probability=probability,
        framework=framework,
        category=category,
        resolve_by=resolve_by,
        regime_context=regime_context or None,
        evidence=evidence,
        tags=tags,
    )


@mcp.tool()
def resolve_prediction(prediction_id: str, outcome: bool, notes: str = "") -> dict:
    """Resolve a prediction with its actual outcome (True = happened, False = didn't).

    Marks a prediction as resolved and records whether the predicted event occurred.
    Once enough predictions are resolved, calibration metrics become meaningful.

    Args:
        prediction_id: The prediction's unique ID (8-char hex string)
        outcome: True if the predicted event occurred, False if not
        notes: Optional resolution notes explaining the outcome
    """
    from processors.calibration import resolve_prediction as _resolve

    result = _resolve(prediction_id, outcome, notes=notes or None)
    if result is None:
        return {"status": "not_found", "prediction_id": prediction_id}
    return {"status": "resolved", "prediction": result}


@mcp.tool()
def get_calibration_report(framework: str = "", category: str = "") -> dict:
    """Get the calibration report — Brier scores, calibration curve, accuracy.

    Computes calibration metrics for all resolved predictions (or filtered
    by framework/category). Returns Brier score (0=perfect, 1=worst),
    calibration curve (predicted vs actual frequency in 5 buckets),
    sharpness (decisiveness), accuracy, and breakdowns by framework,
    category, and regime. Requires at least 5 resolved predictions.

    Args:
        framework: Filter to a specific investor framework (optional)
        category: Filter to a specific category (optional)
    """
    from processors.calibration import (
        compute_calibration_report,
        get_open_predictions,
        get_overdue_predictions,
    )

    report = compute_calibration_report(
        framework=framework or None,
        category=category or None,
    )

    # Always include open/overdue for visibility
    if report.get("status") == "ok" or report.get("status") == "insufficient_data":
        report["open_predictions"] = get_open_predictions()
        report["overdue_predictions"] = get_overdue_predictions()

    return report


@mcp.tool()
def extract_predictions() -> dict:
    """Auto-extract falsifiable predictions from the current briefing data.

    Scans regime classification, VIX levels, contrarian views, credit cycle,
    and Fed game scenarios for claims that can be logged as predictions.
    Returns candidates — call log_prediction to persist the ones you want.
    Does NOT auto-log; the Archon reviews and selects which to persist.
    """
    from processors.calibration import extract_predictions_from_briefing

    briefing = generate_briefing()
    candidates = extract_predictions_from_briefing(briefing)

    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "note": "These are candidates. Call log_prediction for each one you want to track.",
    }


@mcp.tool()
def list_snapshots() -> dict:
    """List all saved daily briefing snapshots.

    Returns dates, file paths, and sizes for all persisted snapshots.
    Use this to see what historical data is available for delta computation
    and trend analysis.
    """
    from processors.persistence import list_snapshots as _list

    snapshots = _list()
    return {
        "count": len(snapshots),
        "snapshots": snapshots,
    }


if __name__ == "__main__":
    mcp.run()
