"""Archon Data v2 — MCP server for live investment intelligence.

Consolidated from 27 tools to 15: 6 core data tools, 4 utility tools,
and 5 portfolio tools. Every tool response includes _meta health tracking.
"""

import sys
import traceback
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).parent))

mcp = FastMCP(
    "Archon Data",
    instructions=(
        "Archon v2 investment intelligence pipeline. Provides consolidated "
        "market data, regime classification, sentiment/positioning, risk "
        "dashboards, external signals, private markets monitoring, and paper "
        "trading portfolio management. All responses include _meta health info."
    ),
)


# ── Helpers ──────────────────────────────────────────────────


def _safe_collect(name: str, source: str, fn, *args, **kwargs) -> dict:
    """Call a collector function, wrapping result with health _meta.

    Returns the result dict with _meta on success, or an error dict on failure.
    """
    from processors.health import wrap_with_meta

    try:
        result = fn(*args, **kwargs)
        if isinstance(result, dict) and "error" in result:
            return wrap_with_meta(result, source, status="degraded", degraded_reason=str(result["error"]))
        return wrap_with_meta(result if isinstance(result, dict) else {"data": result}, source)
    except Exception as e:
        return wrap_with_meta(
            {"error": str(e)},
            source,
            status="failed",
            degraded_reason=str(e)[:100],
        )


def _parallel_collect(specs: list[tuple], deadline_seconds: float = 22.0) -> dict:
    """Run several _safe_collect calls concurrently, returning {key: result}.

    Each spec is ``(result_key, source_label, fn)``. Collectors fan out across
    threads so total wall-time approaches the slowest single collector rather
    than the sum — the fix for MCP -32001 timeouts when many scraping-dependent
    sources run on a cold cache.

    A collector that misses the shared deadline yields a degraded _meta entry
    instead of stalling the whole tool. Stragglers are left to finish on
    background threads (``shutdown(wait=False)``) so they warm the cache for the
    next call — a missed deadline becomes self-healing.
    """
    from concurrent.futures import ThreadPoolExecutor, wait as _wait

    from processors.health import wrap_with_meta

    ex = ThreadPoolExecutor(max_workers=max(1, len(specs)))
    future_map = {
        ex.submit(_safe_collect, key, source, fn): (key, source)
        for key, source, fn in specs
    }
    done, _ = _wait(future_map.keys(), timeout=deadline_seconds)

    results: dict = {}
    for future, (key, source) in future_map.items():
        if future in done:
            try:
                results[key] = future.result()
            except Exception as e:  # pragma: no cover - defensive
                results[key] = wrap_with_meta(
                    {"error": str(e)}, source, status="failed", degraded_reason=str(e)[:100]
                )
        else:
            results[key] = wrap_with_meta(
                {"error": f"{source} exceeded {deadline_seconds:.0f}s deadline"},
                source,
                status="failed",
                degraded_reason="collector deadline exceeded",
            )

    ex.shutdown(wait=False)  # let stragglers finish in the background (warms cache)
    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CORE DATA TOOLS (6)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
def get_market_data() -> dict:
    """Get consolidated market data: indices, sectors, cross-asset, factors, fund flows.

    Merges market snapshot, asset performance, sector rotation, factor returns,
    and fund flow signals into a single response. All from yfinance (no API key).
    """
    from collectors.market import (
        get_asset_performance,
        get_market_snapshot,
        get_sector_performance,
    )
    from collectors.factors import get_factor_returns
    from collectors.fund_flows import get_fund_flow_proxies

    market = _safe_collect("market", "yfinance", get_market_snapshot)
    sectors = _safe_collect("sectors", "yfinance", get_sector_performance)
    assets = _safe_collect("assets", "yfinance", get_asset_performance)
    factors = _safe_collect("factors", "french_data", get_factor_returns)
    flows = _safe_collect("flows", "yfinance", get_fund_flow_proxies)

    return {
        "market": market,
        "sectors": sectors,
        "assets": assets,
        "factors": factors,
        "fund_flows": flows,
    }


@mcp.tool()
def get_regime_and_macro() -> dict:
    """Get regime classification, macro indicators, yield curve, and Fed game theory.

    Combines FRED macro data, Treasury yield curve, Dalio regime classification,
    and Fed strategic analysis. Requires FRED_API_KEY for full macro data;
    falls back to market-implied signals without it.
    """
    from collectors.fred import get_macro_data
    from collectors.treasury import get_yield_curve
    from processors.regime import classify_regime
    from processors.fed_game import analyze_fed_game

    macro = _safe_collect("macro", "FRED", get_macro_data)
    yields = _safe_collect("yields", "treasury", get_yield_curve)

    # Extract raw data for processors (strip _meta)
    macro_raw = {k: v for k, v in macro.items() if k != "_meta"}
    yields_raw = {k: v for k, v in yields.items() if k != "_meta"}

    regime = _safe_collect("regime", "computed", classify_regime, macro_raw, yields_raw)
    regime_raw = {k: v for k, v in regime.items() if k != "_meta"}

    fed_game = _safe_collect(
        "fed_game", "computed",
        analyze_fed_game, regime=regime_raw, macro=macro_raw, yields=yields_raw,
    )

    return {
        "regime": regime,
        "macro": macro,
        "yield_curve": yields,
        "fed_game": fed_game,
    }


@mcp.tool()
def get_sentiment_and_positioning() -> dict:
    """Get sentiment, CFTC positioning, Google Trends, and contrarian scorecard.

    Combines sentiment dashboard, COT institutional positioning, behavioral
    signals from Google Trends, and the computed contrarian scorecard.
    """
    from collectors.cot import get_cot_positioning
    from collectors.google_trends import get_trend_signals
    from collectors.market import (
        get_asset_performance,
        get_market_snapshot,
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

    sentiment_raw = _safe_collect("sentiment", "CNN/yfinance", get_sentiment_dashboard)
    cot = _safe_collect("cot", "CFTC", get_cot_positioning)
    trends = _safe_collect("trends", "google_trends", get_trend_signals)

    # Compute composite sentiment
    try:
        market = get_market_snapshot()
    except Exception:
        market = {}
    sent_data = {k: v for k, v in sentiment_raw.items() if k != "_meta"}
    composite = compute_sentiment_score(sent_data, market)

    # Compute contrarian scorecard
    try:
        macro = get_macro_data()
        yields = get_yield_curve()
        regime = classify_regime(macro, yields)
        assets = get_asset_performance()
        sectors = get_sector_performance()
        fred_pm = get_private_market_macro()
        proxies = get_private_market_proxies()
        pm = get_private_markets_dashboard(fred_pm, proxies)

        sentiment_bundle = {"composite": composite, "raw": sent_data}
        cot_raw = {k: v for k, v in cot.items() if k != "_meta"}
        trends_raw = {k: v for k, v in trends.items() if k != "_meta"}

        contrarian = compute_contrarian_scorecard(
            sentiment=sentiment_bundle, cot=cot_raw, trends=trends_raw,
            market=market, regime=regime, risk={},
            private_markets=pm, assets=assets, sectors=sectors,
        )
    except Exception as e:
        contrarian = {"error": str(e), "_meta": {"status": "failed", "source": "computed"}}

    return {
        "sentiment": {**sentiment_raw, "composite": composite},
        "cot_positioning": cot,
        "trends": trends,
        "contrarian": contrarian,
    }


@mcp.tool()
def get_risk_dashboard() -> dict:
    """Get risk dashboard: correlations, VIX regime, yield curve, overall risk level.

    Returns 30-day rolling correlations, stock-bond correlation regime,
    VIX term structure, and an overall risk assessment.
    """
    from collectors.market import get_market_snapshot
    from collectors.sentiment import get_sentiment_dashboard
    from collectors.treasury import get_yield_curve
    from processors.risk import get_risk_dashboard as _risk

    sentiment = _safe_collect("sentiment", "CNN/yfinance", get_sentiment_dashboard)
    yields = _safe_collect("yields", "treasury", get_yield_curve)
    market = _safe_collect("market", "yfinance", get_market_snapshot)

    sent_raw = {k: v for k, v in sentiment.items() if k != "_meta"}
    yields_raw = {k: v for k, v in yields.items() if k != "_meta"}
    market_raw = {k: v for k, v in market.items() if k != "_meta"}

    risk = _safe_collect("risk", "computed", _risk, sent_raw, yields_raw, market_raw)

    return risk


@mcp.tool()
def get_external_signals() -> dict:
    """Get external signals: insider buys, SEC filings, geopolitical, crypto, calendars.

    Consolidates fragile/scraping-dependent data sources. Tolerates partial
    failures — each source is independently collected and health-tracked.
    """
    from collectors.coingecko import get_crypto_dashboard
    from collectors.earnings import get_earnings_calendar
    from collectors.econ_calendar import get_economic_calendar
    from collectors.gdelt import get_geopolitical_monitor
    from collectors.insider import get_insider_buys
    from collectors.sec_edgar import get_special_situation_filings, get_recent_13f_filings

    return _parallel_collect([
        ("insider", "OpenInsider", get_insider_buys),
        ("special_situations", "SEC_EDGAR", get_special_situation_filings),
        ("filings_13f", "SEC_EDGAR", get_recent_13f_filings),
        ("geopolitical", "GDELT", get_geopolitical_monitor),
        ("crypto", "CoinGecko", get_crypto_dashboard),
        ("earnings", "yfinance", get_earnings_calendar),
        ("economic_calendar", "FRED", get_economic_calendar),
    ])


@mcp.tool()
def get_private_markets() -> dict:
    """Get private markets monitor: RE cycle, credit cycle, PE/VC exit window.

    Synthesizes FRED macro + public market proxies (REITs, BDCs, PE GP stocks)
    to classify private market cycles and detect public-private divergence.
    """
    from collectors.fred import get_private_market_macro
    from collectors.market import get_private_market_proxies
    from processors.private_markets import get_private_markets_dashboard

    fred_data = _safe_collect("fred_pm", "FRED", get_private_market_macro)
    proxy_data = _safe_collect("proxies", "yfinance", get_private_market_proxies)

    fred_raw = {k: v for k, v in fred_data.items() if k != "_meta"}
    proxy_raw = {k: v for k, v in proxy_data.items() if k != "_meta"}

    dashboard = _safe_collect("private_markets", "computed", get_private_markets_dashboard, fred_raw, proxy_raw)

    return dashboard


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UTILITY TOOLS (4)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
def generate_briefing() -> dict:
    """Generate a complete Archon v2 briefing data package.

    Calls all 6 core data tools and assembles the full data package with
    health tracking. Returns a _health dict summarizing data source status.
    """
    from processors.health import collect_health

    results = {}
    tool_health = {}

    # Call all core tools
    for name, fn in [
        ("market_data", get_market_data),
        ("regime_macro", get_regime_and_macro),
        ("sentiment_positioning", get_sentiment_and_positioning),
        ("risk", get_risk_dashboard),
        ("external", get_external_signals),
        ("private_markets", get_private_markets),
    ]:
        try:
            result = fn()
            results[name] = result
            # Extract health from _meta (top-level or nested)
            if isinstance(result, dict):
                if "_meta" in result:
                    tool_health[name] = result
                for k, v in result.items():
                    if isinstance(v, dict) and "_meta" in v:
                        tool_health[f"{name}.{k}"] = v
        except Exception as e:
            results[name] = {"error": str(e)}
            tool_health[name] = {"_meta": {"status": "failed", "source": name}}

    # Aggregate health
    health = collect_health(tool_health)

    return {
        **results,
        "_health": health,
    }


@mcp.tool()
def get_pipeline_health() -> dict:
    """Quick health check — returns data source status without full briefing.

    Useful for diagnostics. Tests connectivity to each major data source
    and reports status, freshness, and any errors.
    """
    from processors.health import collect_health

    checks = {}

    # Test each source independently
    test_sources = [
        ("yfinance", "collectors.market", "get_market_snapshot"),
        ("FRED", "collectors.fred", "get_macro_data"),
        ("treasury", "collectors.treasury", "get_yield_curve"),
        ("sentiment", "collectors.sentiment", "get_sentiment_dashboard"),
        ("CFTC", "collectors.cot", "get_cot_positioning"),
        ("CoinGecko", "collectors.coingecko", "get_crypto_dashboard"),
        ("GDELT", "collectors.gdelt", "get_geopolitical_monitor"),
        ("OpenInsider", "collectors.insider", "get_insider_buys"),
    ]

    for name, module_path, fn_name in test_sources:
        try:
            module = __import__(module_path, fromlist=[fn_name])
            fn = getattr(module, fn_name)
            result = fn()
            if isinstance(result, dict) and "error" in result:
                checks[name] = {"_meta": {"status": "degraded", "source": name, "degraded_reason": str(result["error"])[:80]}}
            else:
                checks[name] = {"_meta": {"status": "ok", "source": name, "cache_age_seconds": 0}}
        except Exception as e:
            checks[name] = {"_meta": {"status": "failed", "source": name, "degraded_reason": str(e)[:80]}}

    return collect_health(checks)


@mcp.tool()
def save_snapshot(for_date: str = "") -> dict:
    """Save today's briefing data as a permanent daily snapshot.

    Persists to archon-data/snapshots/YYYY-MM-DD.json for delta computation.

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
    }


@mcp.tool()
def get_delta() -> dict:
    """Get the Delta Block — what changed since the last saved snapshot.

    Generates a fresh briefing, diffs it against the most recent snapshot,
    and returns structured deltas: market moves, regime changes, threshold
    crossings, leadership changes, and summary bullets.
    """
    from processors.persistence import compute_delta, get_prior_snapshot

    current = generate_briefing()
    prior = get_prior_snapshot()

    if prior is None:
        return {
            "status": "no_prior_snapshot",
            "message": "No prior snapshot. Run save_snapshot to establish a baseline.",
            "current_briefing": current,
        }

    delta = compute_delta({"data": current}, prior)
    return {
        "status": "ok",
        "delta": delta,
        "current_briefing": current,
    }


@mcp.tool()
def get_alerts() -> dict:
    """Get the alert feed — threshold-based signals across all data.

    Scans for regime shifts, VIX extremes, credit stress, crowded positioning,
    breadth divergences, and correlation regime changes. Each alert has severity
    (critical/warning/watch) and actionability note.
    """
    from processors.alerts import generate_alerts

    briefing = generate_briefing()
    return generate_alerts(briefing)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PORTFOLIO TOOLS (5)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
def open_position(
    symbol: str,
    direction: str,
    size_pct: float,
    entry_price: float,
    thesis_source: str,
    thesis_text: str,
    confidence: str,
    regime_context: str = "",
    stop_loss_pct: float = 0.0,
    target_pct: float = 0.0,
) -> dict:
    """Open a paper trade in Archon's portfolio.

    Args:
        symbol: Ticker (e.g., "XLE", "GLD", "QQQ")
        direction: "long" or "short"
        size_pct: Position size as % of capital (e.g., 10.0)
        entry_price: Entry price per share
        thesis_source: What analysis drove this (contrarian_scorecard, regime_shift, alert, etc.)
        thesis_text: The specific thesis statement
        confidence: "H", "M", or "L"
        regime_context: Active regime when opened
        stop_loss_pct: Stop-loss % from entry (negative, e.g., -5.0). 0 = use default.
        target_pct: Profit target % from entry (positive). 0 = no target.
    """
    from processors.portfolio import open_position as _open

    return _open(
        symbol=symbol, direction=direction, size_pct=size_pct,
        entry_price=entry_price, thesis_source=thesis_source,
        thesis_text=thesis_text, confidence=confidence,
        regime_context=regime_context,
        stop_loss_pct=stop_loss_pct or None,
        target_pct=target_pct or None,
    )


@mcp.tool()
def close_position(
    trade_id: str,
    exit_price: float,
    exit_reason: str,
    resolution_notes: str = "",
    thesis_outcome: str = "correct",
) -> dict:
    """Close an open paper trade.

    Args:
        trade_id: Position's unique ID (8-char hex)
        exit_price: Exit price per share
        exit_reason: target_hit, stop_hit, thesis_broken, regime_change, rebalance
        resolution_notes: Explanation
        thesis_outcome: correct, wrong, stopped_out, invalidated
    """
    from processors.portfolio import close_position as _close

    result = _close(trade_id, exit_price, exit_reason, resolution_notes, thesis_outcome)
    if result is None:
        return {"error": f"Position {trade_id} not found"}
    return result


@mcp.tool()
def update_positions() -> dict:
    """Mark-to-market all open positions using live prices.

    Fetches current prices from yfinance and updates unrealized P&L,
    high water marks, and daily equity snapshot.
    """
    from processors.portfolio import update_positions as _update

    return _update()


@mcp.tool()
def get_portfolio() -> dict:
    """Get the full portfolio state: positions, trades, metrics, rules."""
    from processors.portfolio import get_portfolio as _get

    return _get()


@mcp.tool()
def get_portfolio_performance() -> dict:
    """Get detailed performance breakdown by regime, thesis source, and timeframe."""
    from processors.portfolio import get_portfolio_performance as _perf

    return _perf()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PREDICTION TRACKING (3 — kept from v1)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


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
    """Log a falsifiable prediction for calibration scoring.

    Args:
        claim: Specific prediction (e.g., "VIX below 25 by April 15")
        probability: Assigned probability (0.0 to 1.0)
        framework: Source framework (Marks, Soros, Tudor Jones, etc.)
        category: Domain (regime, credit, equity, vol, rotation, fed)
        resolve_by: Deadline (YYYY-MM-DD)
        regime_context: Active regime when prediction was made
        evidence: Supporting evidence points
        tags: Optional tags
    """
    from processors.calibration import log_prediction as _log

    return _log(
        claim=claim, probability=probability, framework=framework,
        category=category, resolve_by=resolve_by,
        regime_context=regime_context or None,
        evidence=evidence, tags=tags,
    )


@mcp.tool()
def resolve_prediction(prediction_id: str, outcome: bool, notes: str = "") -> dict:
    """Resolve a prediction (True = happened, False = didn't).

    Args:
        prediction_id: The prediction's 8-char ID
        outcome: Whether the predicted event occurred
        notes: Resolution notes
    """
    from processors.calibration import resolve_prediction as _resolve

    result = _resolve(prediction_id, outcome, notes=notes or None)
    if result is None:
        return {"error": f"Prediction {prediction_id} not found"}
    return {"status": "resolved", "prediction": result}


@mcp.tool()
def get_calibration_report(framework: str = "", category: str = "") -> dict:
    """Get calibration report: Brier scores, accuracy, breakdowns.

    Args:
        framework: Filter by investor framework (optional)
        category: Filter by category (optional)
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
    report["open_predictions"] = get_open_predictions()
    report["overdue_predictions"] = get_overdue_predictions()

    return report


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    mcp.run()
