"""Paper trading portfolio — tracks Archon's conviction trades against real prices.

Follows the same persistence pattern as calibration.py (single JSON file,
log/resolve lifecycle), but adds mark-to-market, P&L computation, and
performance metrics. Archon sets its own rules and can evolve them over time.

Key concepts:
- Position: an open trade with entry price, thesis, and stop-loss
- Trade: a closed position with exit price, P&L, and thesis outcome
- Equity curve: daily snapshots of total portfolio value
- Thesis tracking: did the stated reason for the trade actually play out?
"""

from __future__ import annotations

import json
import uuid
from datetime import date, datetime
from pathlib import Path

PORTFOLIO_FILE = Path(__file__).parent.parent / "snapshots" / "portfolio.json"


# ── Portfolio I/O ───────────────────────────────────────────


def _load_portfolio() -> dict:
    """Load or initialize the portfolio."""
    if PORTFOLIO_FILE.exists():
        with open(PORTFOLIO_FILE) as f:
            return json.load(f)
    return _init_portfolio()


def _save_portfolio(portfolio: dict) -> None:
    """Atomically save portfolio state."""
    PORTFOLIO_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = PORTFOLIO_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(portfolio, f, indent=2, default=str)
    tmp.rename(PORTFOLIO_FILE)


def _init_portfolio() -> dict:
    """Create an empty portfolio with default rules."""
    portfolio = {
        "rules": {
            "initial_capital": 1_000_000,
            "current_capital": 1_000_000,
            "max_position_pct": 15,
            "max_positions": 8,
            "stop_loss_default_pct": -5.0,
            "conviction_sizing": True,
            "rules_history": [
                {
                    "date": date.today().isoformat(),
                    "change": "initial rules set",
                    "rationale": (
                        "$1M notional, max 15% per position, max 8 positions, "
                        "default 5% stop-loss, conviction-based sizing enabled. "
                        "Archon may evolve these rules over time."
                    ),
                }
            ],
        },
        "positions": [],
        "closed_trades": [],
        "daily_equity": [],
        "metrics": _empty_metrics(),
    }
    _save_portfolio(portfolio)
    return portfolio


def _empty_metrics() -> dict:
    return {
        "total_return_pct": 0.0,
        "sharpe_ratio": None,
        "sortino_ratio": None,
        "max_drawdown_pct": 0.0,
        "win_rate": None,
        "profit_factor": None,
        "avg_holding_days": None,
        "avg_winner_pct": None,
        "avg_loser_pct": None,
        "by_regime": {},
        "by_thesis_source": {},
    }


# ── Position Management ─────────────────────────────────────


def open_position(
    symbol: str,
    direction: str,
    size_pct: float,
    entry_price: float,
    thesis_source: str,
    thesis_text: str,
    confidence: str,
    regime_context: str = "",
    stop_loss_pct: float | None = None,
    target_pct: float | None = None,
) -> dict:
    """Open a new paper trade.

    Args:
        symbol: Ticker symbol (e.g., "XLE", "GLD", "QQQ")
        direction: "long" or "short"
        size_pct: Position size as % of portfolio (e.g., 10.0 = 10%)
        entry_price: Entry price per share
        thesis_source: What briefing analysis drove this (e.g., "contrarian_scorecard", "regime_shift", "alert")
        thesis_text: Specific thesis statement
        confidence: "H", "M", or "L"
        regime_context: Active regime when trade was opened
        stop_loss_pct: Stop-loss as % from entry (negative, e.g., -5.0). Defaults to portfolio rule.
        target_pct: Profit target as % from entry (positive, e.g., 10.0). Optional.

    Returns:
        The opened position record.
    """
    portfolio = _load_portfolio()
    rules = portfolio["rules"]

    # Enforce rules
    if len(portfolio["positions"]) >= rules["max_positions"]:
        return {"error": f"Max positions ({rules['max_positions']}) reached. Close a position first."}

    if size_pct > rules["max_position_pct"]:
        return {"error": f"Size {size_pct}% exceeds max {rules['max_position_pct']}%"}

    capital = rules["current_capital"]
    notional = capital * (size_pct / 100.0)
    quantity = int(notional / entry_price) if entry_price > 0 else 0

    position = {
        "id": str(uuid.uuid4())[:8],
        "symbol": symbol,
        "direction": direction.lower(),
        "entry_price": entry_price,
        "quantity": quantity,
        "size_pct": size_pct,
        "notional": round(quantity * entry_price, 2),
        "entry_date": date.today().isoformat(),
        "thesis_source": thesis_source,
        "thesis_text": thesis_text,
        "confidence": confidence.upper(),
        "regime_context": regime_context,
        "stop_loss_pct": stop_loss_pct if stop_loss_pct is not None else rules["stop_loss_default_pct"],
        "target_pct": target_pct,
        "current_price": entry_price,
        "unrealized_pnl": 0.0,
        "unrealized_pnl_pct": 0.0,
        "high_water_mark": entry_price,
        "max_adverse_excursion": 0.0,
        "status": "open",
    }

    portfolio["positions"].append(position)
    _save_portfolio(portfolio)
    return position


def close_position(
    trade_id: str,
    exit_price: float,
    exit_reason: str,
    resolution_notes: str = "",
    thesis_outcome: str = "correct",
) -> dict | None:
    """Close an open position.

    Args:
        trade_id: The position's unique ID
        exit_price: Exit price per share
        exit_reason: Why closing (target_hit, stop_hit, thesis_broken, regime_change, rebalance)
        resolution_notes: Explanation of the outcome
        thesis_outcome: "correct" (thesis played out), "wrong" (thesis broken but profitable),
                       "stopped_out" (right thesis, bad timing), "invalidated" (thesis no longer relevant)

    Returns:
        The closed trade record, or None if not found.
    """
    portfolio = _load_portfolio()

    for i, pos in enumerate(portfolio["positions"]):
        if pos["id"] == trade_id:
            # Compute P&L
            if pos["direction"] == "long":
                pnl_per_share = exit_price - pos["entry_price"]
            else:
                pnl_per_share = pos["entry_price"] - exit_price

            pnl = round(pnl_per_share * pos["quantity"], 2)
            pnl_pct = round((pnl_per_share / pos["entry_price"]) * 100, 2) if pos["entry_price"] else 0.0

            entry_date = date.fromisoformat(pos["entry_date"])
            holding_days = (date.today() - entry_date).days

            trade = {
                **pos,
                "exit_price": exit_price,
                "exit_date": date.today().isoformat(),
                "exit_reason": exit_reason,
                "resolution_notes": resolution_notes,
                "thesis_outcome": thesis_outcome,
                "realized_pnl": pnl,
                "realized_pnl_pct": pnl_pct,
                "holding_days": holding_days,
                "status": "closed",
            }

            # Move from positions to closed_trades
            portfolio["positions"].pop(i)
            portfolio["closed_trades"].append(trade)

            # Update capital
            portfolio["rules"]["current_capital"] += pnl

            # Recompute metrics
            portfolio["metrics"] = _compute_metrics(portfolio)
            _save_portfolio(portfolio)
            return trade

    return None


def update_positions(market_prices: dict[str, float] | None = None) -> dict:
    """Mark-to-market all open positions.

    Args:
        market_prices: Dict of symbol → current price. If None, fetches from yfinance.

    Returns:
        Updated portfolio summary.
    """
    portfolio = _load_portfolio()

    if not portfolio["positions"]:
        return {"status": "no_positions", "positions": []}

    # Fetch prices if not provided
    if market_prices is None:
        market_prices = _fetch_current_prices(
            [p["symbol"] for p in portfolio["positions"]]
        )

    total_unrealized = 0.0

    for pos in portfolio["positions"]:
        price = market_prices.get(pos["symbol"])
        if price is None:
            continue

        pos["current_price"] = price

        if pos["direction"] == "long":
            pnl_per_share = price - pos["entry_price"]
        else:
            pnl_per_share = pos["entry_price"] - price

        pos["unrealized_pnl"] = round(pnl_per_share * pos["quantity"], 2)
        pos["unrealized_pnl_pct"] = round(
            (pnl_per_share / pos["entry_price"]) * 100, 2
        ) if pos["entry_price"] else 0.0

        # Track high water mark and max adverse excursion
        if pos["direction"] == "long":
            pos["high_water_mark"] = max(pos.get("high_water_mark", price), price)
            pos["max_adverse_excursion"] = min(
                pos.get("max_adverse_excursion", 0.0), pos["unrealized_pnl_pct"]
            )
        else:
            pos["high_water_mark"] = min(pos.get("high_water_mark", price), price)
            pos["max_adverse_excursion"] = min(
                pos.get("max_adverse_excursion", 0.0), pos["unrealized_pnl_pct"]
            )

        total_unrealized += pos["unrealized_pnl"]

    # Record daily equity snapshot
    capital = portfolio["rules"]["current_capital"]
    realized_cumulative = capital - portfolio["rules"]["initial_capital"]
    deployed = sum(p["notional"] for p in portfolio["positions"])
    deployed_pct = round((deployed / capital) * 100, 1) if capital else 0.0

    equity_entry = {
        "date": date.today().isoformat(),
        "equity": round(capital + total_unrealized, 2),
        "capital": capital,
        "deployed": round(deployed, 2),
        "deployed_pct": deployed_pct,
        "realized_pnl_cumulative": round(realized_cumulative, 2),
        "unrealized_pnl": round(total_unrealized, 2),
        "positions_open": len(portfolio["positions"]),
    }

    # Replace today's entry if exists, otherwise append
    today_iso = date.today().isoformat()
    portfolio["daily_equity"] = [
        e for e in portfolio["daily_equity"] if e["date"] != today_iso
    ]
    portfolio["daily_equity"].append(equity_entry)

    portfolio["metrics"] = _compute_metrics(portfolio)
    _save_portfolio(portfolio)

    return {
        "status": "ok",
        "equity": equity_entry,
        "positions": portfolio["positions"],
    }


def get_portfolio() -> dict:
    """Get the full portfolio state."""
    return _load_portfolio()


def get_portfolio_performance() -> dict:
    """Get detailed performance breakdown."""
    portfolio = _load_portfolio()
    metrics = portfolio["metrics"]

    return {
        "summary": {
            "total_return_pct": metrics["total_return_pct"],
            "sharpe_ratio": metrics["sharpe_ratio"],
            "sortino_ratio": metrics["sortino_ratio"],
            "max_drawdown_pct": metrics["max_drawdown_pct"],
            "win_rate": metrics["win_rate"],
            "profit_factor": metrics["profit_factor"],
            "avg_holding_days": metrics["avg_holding_days"],
        },
        "by_regime": metrics["by_regime"],
        "by_thesis_source": metrics["by_thesis_source"],
        "equity_curve": portfolio["daily_equity"][-30:],  # Last 30 entries
        "total_trades": len(portfolio["closed_trades"]),
        "open_positions": len(portfolio["positions"]),
    }


def adjust_portfolio_rules(rules_update: dict, rationale: str) -> dict:
    """Adjust portfolio rules. Archon can evolve its own risk parameters.

    Args:
        rules_update: Dict of rule keys to update (e.g., {"max_position_pct": 20})
        rationale: Why the rules are changing

    Returns:
        Updated rules.
    """
    portfolio = _load_portfolio()
    rules = portfolio["rules"]

    allowed_keys = {
        "max_position_pct", "max_positions", "stop_loss_default_pct",
        "conviction_sizing",
    }

    changes = []
    for key, value in rules_update.items():
        if key in allowed_keys:
            old_val = rules.get(key)
            rules[key] = value
            changes.append(f"{key}: {old_val} → {value}")

    if changes:
        rules["rules_history"].append({
            "date": date.today().isoformat(),
            "change": "; ".join(changes),
            "rationale": rationale,
        })

    _save_portfolio(portfolio)
    return rules


# ── Metrics Computation ──────────────────────────────────────


def _compute_metrics(portfolio: dict) -> dict:
    """Recompute all performance metrics from closed trades and equity curve."""
    closed = portfolio["closed_trades"]
    equity = portfolio["daily_equity"]
    initial = portfolio["rules"]["initial_capital"]

    metrics = _empty_metrics()

    if not closed:
        return metrics

    # Basic trade stats
    winners = [t for t in closed if t["realized_pnl"] > 0]
    losers = [t for t in closed if t["realized_pnl"] <= 0]

    metrics["win_rate"] = round(len(winners) / len(closed), 3) if closed else None

    if winners:
        metrics["avg_winner_pct"] = round(
            sum(t["realized_pnl_pct"] for t in winners) / len(winners), 2
        )
    if losers:
        metrics["avg_loser_pct"] = round(
            sum(t["realized_pnl_pct"] for t in losers) / len(losers), 2
        )

    # Profit factor
    gross_profit = sum(t["realized_pnl"] for t in winners) if winners else 0
    gross_loss = abs(sum(t["realized_pnl"] for t in losers)) if losers else 0
    metrics["profit_factor"] = round(gross_profit / gross_loss, 2) if gross_loss > 0 else None

    # Average holding days
    metrics["avg_holding_days"] = round(
        sum(t["holding_days"] for t in closed) / len(closed), 1
    )

    # Total return
    current_capital = portfolio["rules"]["current_capital"]
    unrealized = sum(p.get("unrealized_pnl", 0) for p in portfolio["positions"])
    total_value = current_capital + unrealized
    metrics["total_return_pct"] = round(((total_value - initial) / initial) * 100, 2)

    # Sharpe and Sortino from equity curve
    if len(equity) >= 5:
        returns = []
        for i in range(1, len(equity)):
            prev_eq = equity[i - 1]["equity"]
            curr_eq = equity[i]["equity"]
            if prev_eq > 0:
                returns.append((curr_eq - prev_eq) / prev_eq)

        if returns:
            import statistics

            avg_ret = statistics.mean(returns)
            std_ret = statistics.stdev(returns) if len(returns) > 1 else 0.001

            # Annualize (assume ~252 trading days)
            metrics["sharpe_ratio"] = round(
                (avg_ret / std_ret) * (252 ** 0.5), 2
            ) if std_ret > 0 else None

            # Sortino: only downside deviation
            downside = [r for r in returns if r < 0]
            if len(downside) > 1:
                down_std = statistics.stdev(downside)
                if down_std > 0:
                    metrics["sortino_ratio"] = round(
                        (avg_ret / down_std) * (252 ** 0.5), 2
                    )

    # Max drawdown from equity curve
    if equity:
        peak = equity[0]["equity"]
        max_dd = 0.0
        for e in equity:
            peak = max(peak, e["equity"])
            dd = ((e["equity"] - peak) / peak) * 100 if peak > 0 else 0
            max_dd = min(max_dd, dd)
        metrics["max_drawdown_pct"] = round(max_dd, 2)

    # Breakdowns by regime and thesis source
    for key_field, metric_key in [("regime_context", "by_regime"), ("thesis_source", "by_thesis_source")]:
        breakdown = {}
        for t in closed:
            bucket = t.get(key_field, "unknown") or "unknown"
            if bucket not in breakdown:
                breakdown[bucket] = {"count": 0, "winners": 0, "total_pnl": 0.0}
            breakdown[bucket]["count"] += 1
            breakdown[bucket]["total_pnl"] += t["realized_pnl"]
            if t["realized_pnl"] > 0:
                breakdown[bucket]["winners"] += 1

        for bucket in breakdown:
            b = breakdown[bucket]
            b["win_rate"] = round(b["winners"] / b["count"], 3) if b["count"] else 0
            b["total_pnl"] = round(b["total_pnl"], 2)

        metrics[metric_key] = breakdown

    return metrics


# ── Helpers ──────────────────────────────────────────────────


def _fetch_current_prices(symbols: list[str]) -> dict[str, float]:
    """Fetch current prices from yfinance."""
    try:
        import yfinance as yf

        prices = {}
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.fast_info
                price = getattr(info, "last_price", None)
                if price and price > 0:
                    prices[symbol] = round(float(price), 2)
            except Exception:
                continue
        return prices
    except ImportError:
        return {}
