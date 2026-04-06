"""Daily snapshot persistence and delta computation.

Stores complete briefing outputs as date-keyed JSON files in the snapshots/
directory. Provides delta computation between consecutive days to power the
Delta Block (§0) in the briefing protocol.

Design decisions:
- One file per day (YYYY-MM-DD.json), not a single growing database.
  Keeps each snapshot independent, easy to inspect, easy to archive.
- Delta computation is structural, not just numeric — it detects regime
  changes, leadership flips, new alerts, and threshold crossings, not
  just "VIX went up 2 points."
- NaN-safe JSON encoding inherited from cache.py pattern.
"""

import json
import math
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

SNAPSHOT_DIR = Path(__file__).parent.parent / "snapshots"


# ── JSON encoding ────────────────────────────────────────────


class _NaNSafeEncoder(json.JSONEncoder):
    """JSON encoder that converts NaN/Infinity to None and datetimes to ISO.

    Also handles numpy numeric types (float64, int64) which yfinance and
    fredapi return — these aren't caught by isinstance(o, float).
    """

    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        # Handle numpy types that aren't plain Python scalars
        try:
            f = float(o)
            if math.isnan(f) or math.isinf(f):
                return None
            return f
        except (TypeError, ValueError):
            pass
        return str(o)

    def encode(self, o):
        return super().encode(self._clean(o))

    def _clean(self, o):
        if isinstance(o, float):
            if math.isnan(o) or math.isinf(o):
                return None
            return o
        # Catch numpy float64/int64 and similar
        if hasattr(o, '__float__') and not isinstance(o, (int, bool, str)):
            try:
                f = float(o)
                if math.isnan(f) or math.isinf(f):
                    return None
                return f
            except (TypeError, ValueError):
                pass
        if isinstance(o, dict):
            return {k: self._clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [self._clean(v) for v in o]
        return o


# ── Snapshot I/O ─────────────────────────────────────────────


def save_daily_snapshot(briefing_data: dict, for_date: str | None = None) -> str:
    """Save a complete briefing as a daily snapshot.

    Args:
        briefing_data: The full output from generate_briefing().
        for_date: Optional date string (YYYY-MM-DD). Defaults to today.

    Returns:
        The file path of the saved snapshot.
    """
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_date = for_date or date.today().isoformat()
    path = SNAPSHOT_DIR / f"{snapshot_date}.json"

    snapshot = {
        "_snapshot_date": snapshot_date,
        "_saved_at": datetime.now().isoformat(),
        "data": briefing_data,
    }

    path.write_text(json.dumps(snapshot, cls=_NaNSafeEncoder, indent=2))
    return str(path)


def load_snapshot(for_date: str) -> dict | None:
    """Load a specific day's snapshot. Returns None if not found."""
    path = SNAPSHOT_DIR / f"{for_date}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def get_prior_snapshot(before_date: str | None = None, max_lookback: int = 30) -> dict | None:
    """Find the most recent snapshot before the given date.

    Scans the snapshots directory for the most recent file with a date
    earlier than `before_date`. Limits search to `max_lookback` most
    recent candidates to avoid unbounded directory scans over time.
    Returns None if no prior snapshot exists.
    """
    ref = (date.fromisoformat(before_date) if before_date else date.today()).isoformat()
    if not SNAPSHOT_DIR.exists():
        return None
    # Scan recent snapshots, find the most recent one before ref date
    candidates = sorted(
        (p for p in SNAPSHOT_DIR.glob("*.json") if p.stem < ref),
        reverse=True,
    )
    for path in candidates[:max_lookback]:
        snapshot = load_snapshot(path.stem)
        if snapshot:
            return snapshot
    return None


def list_snapshots() -> list[dict]:
    """List all available snapshots with dates and file sizes."""
    if not SNAPSHOT_DIR.exists():
        return []
    snapshots = []
    for path in sorted(SNAPSHOT_DIR.glob("*.json")):
        snapshots.append({
            "date": path.stem,
            "path": str(path),
            "size_kb": round(path.stat().st_size / 1024, 1),
        })
    return snapshots


# ── Delta Computation ────────────────────────────────────────


def _safe_get(d: dict, *keys, default=None) -> Any:
    """Safely traverse nested dicts. Default only applies at the terminal key."""
    current = d
    for i, key in enumerate(keys):
        if isinstance(current, dict):
            is_last = (i == len(keys) - 1)
            current = current.get(key, default if is_last else None)
        else:
            return default
    return current


def _pct_change(new: float | None, old: float | None) -> float | None:
    """Compute percentage change, handling None/zero."""
    if new is None or old is None or old == 0:
        return None
    return round(((new - old) / abs(old)) * 100, 2)


def _level_change(new: float | None, old: float | None) -> float | None:
    """Compute absolute level change."""
    if new is None or old is None:
        return None
    return round(new - old, 4)


def compute_delta(current: dict, prior: dict) -> dict:
    """Compute the Delta Block — what changed between two briefings.

    Returns a structured delta with:
    - market_moves: significant price/level changes
    - regime_changes: any regime or cycle classification changes
    - threshold_crossings: signals that crossed important thresholds
    - new_alerts: alerts present now but not in prior
    - leadership_changes: sector or asset leadership flips
    - summary_bullets: human-readable 3-5 bullet summary for §0

    This is NOT a generic diff — it's an opinionated extraction of
    what actually matters for investment decisions.
    """
    cur = current.get("data", current)
    pri = prior.get("data", prior)

    delta = {
        "prior_date": prior.get("_snapshot_date", "unknown"),
        "market_moves": _compute_market_moves(cur, pri),
        "regime_changes": _compute_regime_changes(cur, pri),
        "threshold_crossings": _compute_threshold_crossings(cur, pri),
        "leadership_changes": _compute_leadership_changes(cur, pri),
        "private_market_shifts": _compute_private_market_shifts(cur, pri),
    }

    delta["summary_bullets"] = _generate_summary_bullets(delta, cur)
    return delta


def _compute_market_moves(cur: dict, pri: dict) -> list[dict]:
    """Extract significant market level changes."""
    moves = []

    # Index moves
    for name in ["S&P 500", "Nasdaq", "Russell 2000"]:
        cur_price = _safe_get(cur, "market", "indices", name, "price")
        pri_price = _safe_get(pri, "market", "indices", name, "price")
        pct = _pct_change(cur_price, pri_price)
        if pct is not None and abs(pct) >= 0.3:  # >0.3% move is notable
            moves.append({
                "asset": name,
                "current": cur_price,
                "prior": pri_price,
                "change_pct": pct,
                "direction": "▲" if pct > 0 else "▼",
            })

    # VIX
    cur_vix = _safe_get(cur, "sentiment", "raw", "vix", "spot")
    pri_vix = _safe_get(pri, "sentiment", "raw", "vix", "spot")
    vix_change = _level_change(cur_vix, pri_vix)
    if vix_change is not None and abs(vix_change) >= 1.0:
        moves.append({
            "asset": "VIX",
            "current": cur_vix,
            "prior": pri_vix,
            "change_abs": vix_change,
            "direction": "▲" if vix_change > 0 else "▼",
            "note": "crossed panic threshold" if cur_vix >= 30 and pri_vix < 30
                    else "exited panic" if cur_vix < 30 and pri_vix >= 30
                    else None,
        })

    # Key assets: oil, gold, bitcoin, dollar, 10Y yield
    asset_checks = [
        ("Oil (USO)", "assets", "assets", "Oil (USO)", "price"),
        ("Gold (GLD)", "assets", "assets", "Gold (GLD)", "price"),
        ("Bitcoin", "assets", "assets", "Bitcoin", "price"),
        ("Dollar (DXY)", "assets", "assets", "Dollar (DXY)", "price"),
        ("10Y Yield", "yield_curve", "yields", "10Y", "value"),
    ]
    for label, *path in asset_checks:
        cur_val = _safe_get(cur, *path)
        pri_val = _safe_get(pri, *path)
        pct = _pct_change(cur_val, pri_val)
        if pct is not None and abs(pct) >= 0.5:
            moves.append({
                "asset": label,
                "current": cur_val,
                "prior": pri_val,
                "change_pct": pct,
                "direction": "▲" if pct > 0 else "▼",
            })

    # Sort by magnitude of move
    moves.sort(key=lambda m: abs(m.get("change_pct", 0) or m.get("change_abs", 0)), reverse=True)
    return moves


def _compute_regime_changes(cur: dict, pri: dict) -> list[dict]:
    """Detect changes in regime classifications."""
    changes = []

    # Macro regime
    cur_regime = _safe_get(cur, "regime", "quadrant")
    pri_regime = _safe_get(pri, "regime", "quadrant")
    if cur_regime and pri_regime and cur_regime != pri_regime:
        changes.append({
            "type": "macro_regime",
            "from": pri_regime,
            "to": cur_regime,
            "significance": "high",
            "note": f"Regime shift: {pri_regime} → {cur_regime}",
        })

    # VIX regime
    cur_vix_regime = _safe_get(cur, "sentiment", "raw", "vix", "regime")
    pri_vix_regime = _safe_get(pri, "sentiment", "raw", "vix", "regime")
    if cur_vix_regime and pri_vix_regime and cur_vix_regime != pri_vix_regime:
        changes.append({
            "type": "vix_regime",
            "from": pri_vix_regime,
            "to": cur_vix_regime,
            "significance": "high" if "panic" in (cur_vix_regime, pri_vix_regime) else "medium",
        })

    # Yield curve shape
    cur_curve = _safe_get(cur, "yield_curve", "curve_shape")
    pri_curve = _safe_get(pri, "yield_curve", "curve_shape")
    if cur_curve and pri_curve and cur_curve != pri_curve:
        changes.append({
            "type": "yield_curve",
            "from": pri_curve,
            "to": cur_curve,
            "significance": "high",
            "note": f"Yield curve shifted: {pri_curve} → {cur_curve}",
        })

    # Sentiment label
    cur_sent = _safe_get(cur, "sentiment", "composite", "label")
    pri_sent = _safe_get(pri, "sentiment", "composite", "label")
    if cur_sent and pri_sent and cur_sent != pri_sent:
        changes.append({
            "type": "sentiment",
            "from": pri_sent,
            "to": cur_sent,
            "significance": "medium",
        })

    # Risk level
    cur_risk = _safe_get(cur, "risk", "overall_risk")
    pri_risk = _safe_get(pri, "risk", "overall_risk")
    if cur_risk and pri_risk and cur_risk != pri_risk:
        changes.append({
            "type": "risk_level",
            "from": pri_risk,
            "to": cur_risk,
            "significance": "high" if cur_risk == "extreme" else "medium",
        })

    return changes


def _compute_threshold_crossings(cur: dict, pri: dict) -> list[dict]:
    """Detect when metrics cross important thresholds."""
    crossings = []

    # VIX thresholds: 20 (elevated), 30 (panic), 40 (crisis)
    cur_vix = _safe_get(cur, "sentiment", "raw", "vix", "spot")
    pri_vix = _safe_get(pri, "sentiment", "raw", "vix", "spot")
    if cur_vix is not None and pri_vix is not None:
        for threshold, label in [(20, "elevated"), (30, "panic"), (40, "crisis")]:
            if pri_vix < threshold <= cur_vix:
                crossings.append({
                    "metric": "VIX",
                    "threshold": threshold,
                    "label": label,
                    "direction": "crossed_above",
                    "value": cur_vix,
                })
            elif cur_vix < threshold <= pri_vix:
                crossings.append({
                    "metric": "VIX",
                    "threshold": threshold,
                    "label": label,
                    "direction": "crossed_below",
                    "value": cur_vix,
                })

    # Sentiment score thresholds: 25 (extreme fear), 75 (extreme greed)
    cur_score = _safe_get(cur, "sentiment", "composite", "score")
    pri_score = _safe_get(pri, "sentiment", "composite", "score")
    if cur_score is not None and pri_score is not None:
        if pri_score >= 25 > cur_score:
            crossings.append({
                "metric": "sentiment_score",
                "threshold": 25,
                "label": "extreme_fear",
                "direction": "crossed_below",
                "value": cur_score,
            })
        elif pri_score <= 75 < cur_score:
            crossings.append({
                "metric": "sentiment_score",
                "threshold": 75,
                "label": "extreme_greed",
                "direction": "crossed_above",
                "value": cur_score,
            })

    # 10Y-2Y spread: 0 (inversion threshold)
    cur_spread = _safe_get(cur, "yield_curve", "spread_10y2y")
    pri_spread = _safe_get(pri, "yield_curve", "spread_10y2y")
    if cur_spread is not None and pri_spread is not None:
        if pri_spread >= 0 > cur_spread:
            crossings.append({
                "metric": "10Y-2Y_spread",
                "threshold": 0,
                "label": "inversion",
                "direction": "inverted",
                "value": cur_spread,
            })
        elif pri_spread < 0 <= cur_spread:
            crossings.append({
                "metric": "10Y-2Y_spread",
                "threshold": 0,
                "label": "un-inversion",
                "direction": "normalized",
                "value": cur_spread,
            })

    # Breadth divergence: ±3% is notable
    cur_breadth = _safe_get(cur, "market", "breadth_divergence")
    pri_breadth = _safe_get(pri, "market", "breadth_divergence")
    if cur_breadth is not None and pri_breadth is not None:
        if abs(cur_breadth) >= 3 and abs(pri_breadth) < 3:
            crossings.append({
                "metric": "breadth_divergence",
                "threshold": 3,
                "label": "significant_divergence",
                "direction": "widened",
                "value": cur_breadth,
            })

    # HY spread thresholds: 4% (watch), 5% (stress), 7% (crisis)
    cur_hy = _safe_get(cur, "private_markets", "credit", "hy_spread")
    pri_hy = _safe_get(pri, "private_markets", "credit", "hy_spread")
    if cur_hy is not None and pri_hy is not None:
        for threshold, label in [(4.0, "watch"), (5.0, "stress"), (7.0, "crisis")]:
            if pri_hy < threshold <= cur_hy:
                crossings.append({
                    "metric": "HY_spread",
                    "threshold": threshold,
                    "label": label,
                    "direction": "crossed_above",
                    "value": cur_hy,
                })

    return crossings


def _compute_leadership_changes(cur: dict, pri: dict) -> list[dict]:
    """Detect sector and asset leadership flips."""
    changes = []

    cur_leaders = _safe_get(cur, "sectors", "leaders", default=[])
    pri_leaders = _safe_get(pri, "sectors", "leaders", default=[])
    cur_laggards = _safe_get(cur, "sectors", "laggards", default=[])
    pri_laggards = _safe_get(pri, "sectors", "laggards", default=[])

    # Sectors that moved from laggard to leader (or vice versa)
    if cur_leaders and pri_laggards:
        laggard_to_leader = set(cur_leaders) & set(pri_laggards)
        for sector in laggard_to_leader:
            changes.append({
                "type": "sector_flip",
                "sector": sector,
                "from": "laggard",
                "to": "leader",
                "significance": "high",
            })

    if cur_laggards and pri_leaders:
        leader_to_laggard = set(cur_laggards) & set(pri_leaders)
        for sector in leader_to_laggard:
            changes.append({
                "type": "sector_flip",
                "sector": sector,
                "from": "leader",
                "to": "laggard",
                "significance": "high",
            })

    # New sector leaders not in prior top 3
    if cur_leaders and pri_leaders:
        new_leaders = set(cur_leaders) - set(pri_leaders)
        for sector in new_leaders:
            changes.append({
                "type": "new_leader",
                "sector": sector,
                "significance": "medium",
            })

    return changes


def _compute_private_market_shifts(cur: dict, pri: dict) -> list[dict]:
    """Detect changes in private market cycle classifications."""
    shifts = []

    cycle_keys = [
        ("real_estate", "residential_cycle", "RE cycle"),
        ("credit", "credit_cycle", "Credit cycle"),
        ("exit_window", "exit_window", "Exit window"),
    ]

    for section, key, label in cycle_keys:
        cur_val = _safe_get(cur, "private_markets", section, key)
        pri_val = _safe_get(pri, "private_markets", section, key)
        if cur_val and pri_val and cur_val != pri_val:
            shifts.append({
                "type": label,
                "from": pri_val,
                "to": cur_val,
                "significance": "high",
            })

    # Divergence level changes
    cur_div = _safe_get(cur, "private_markets", "divergence", "overall_divergence")
    pri_div = _safe_get(pri, "private_markets", "divergence", "overall_divergence")
    if cur_div and pri_div and cur_div != pri_div:
        shifts.append({
            "type": "Public-private divergence",
            "from": pri_div,
            "to": cur_div,
            "significance": "high" if cur_div == "severe" else "medium",
        })

    return shifts


def _generate_summary_bullets(delta: dict, cur: dict) -> list[str]:
    """Generate 3-5 human-readable summary bullets for §0 Delta Block.

    Prioritizes: regime changes > threshold crossings > big moves >
    leadership changes > private market shifts.
    """
    bullets = []

    # Regime changes are always top-priority
    for change in delta.get("regime_changes", []):
        if change.get("significance") == "high":
            if change["type"] == "macro_regime":
                bullets.append(
                    f"⚡ REGIME SHIFT: {change['from']} → {change['to']}"
                )
            elif change["type"] == "vix_regime":
                bullets.append(
                    f"⚡ VIX regime: {change['from']} → {change['to']}"
                )
            elif change["type"] == "risk_level":
                bullets.append(
                    f"⚡ Risk level: {change['from']} → {change['to']}"
                )

    # Threshold crossings
    for crossing in delta.get("threshold_crossings", []):
        metric = crossing["metric"]
        label = crossing["label"]
        val = crossing["value"]
        direction = crossing["direction"]
        if metric == "VIX":
            arrow = "▲" if "above" in direction else "▼"
            bullets.append(f"{arrow} VIX: {val} — {direction} {label} threshold ({crossing['threshold']})")
        elif metric == "HY_spread":
            bullets.append(f"▲ HY spread: {val}% — entered {label} zone")
        elif metric == "10Y-2Y_spread":
            bullets.append(f"⚡ Yield curve {label}: 10Y-2Y at {val}%")

    # Top 3 market moves by magnitude
    for move in delta.get("market_moves", [])[:3]:
        asset = move["asset"]
        direction = move["direction"]
        if "change_pct" in move:
            bullets.append(
                f"{direction} {asset}: {move['current']:,.2f} ({move['change_pct']:+.1f}%)"
                + (f" — {move['note']}" if move.get("note") else "")
            )
        elif "change_abs" in move:
            bullets.append(
                f"{direction} {asset}: {move['current']:.1f} ({move['change_abs']:+.1f})"
                + (f" — {move['note']}" if move.get("note") else "")
            )

    # Private market shifts
    for shift in delta.get("private_market_shifts", []):
        if shift.get("significance") == "high":
            bullets.append(
                f"⚡ {shift['type']}: {shift['from']} → {shift['to']}"
            )

    # Leadership flips
    for change in delta.get("leadership_changes", []):
        if change["type"] == "sector_flip":
            bullets.append(
                f"🔄 {change['sector']}: {change['from']} → {change['to']}"
            )

    # Cap at 5 bullets, prioritized by insertion order (regime > thresholds > moves > shifts > flips)
    return bullets[:5] if bullets else ["─ No significant changes since last briefing"]
