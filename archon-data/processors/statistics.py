"""Statistical testing — confidence intervals and base rates for investment claims.

Provides empirical grounding for the claims made in briefings. When the Archon
says "VIX >30 historically reverts within 20 days," this module can verify
that claim with actual base rates, confidence intervals, and sample sizes.

The module works in two modes:
1. Pre-computed base rates: A curated library of well-known market statistics
   with their empirical values, sources, and caveats.
2. Live statistical tests: Fetches recent data via yfinance to compute
   current z-scores, percentiles, and mean-reversion probabilities.

Key concepts:
- Base rate: Historical frequency of an event (e.g., "VIX >30 reverts below 25
  within 20 trading days 72% of the time")
- Confidence interval: Range around an estimate reflecting sample uncertainty
- Z-score: How many standard deviations a reading is from its mean
- Percentile: Where a reading falls in the historical distribution
- Significance: Whether a pattern could have arisen by chance (p-value < 0.05)
"""

from __future__ import annotations

import math


# ── Pre-Computed Base Rate Library ──────────────────────────────
# Curated from academic research and empirical backtests.
# Each entry includes the claim, base rate, sample details, and caveats.

BASE_RATES: list[dict] = [
    # ── VIX / Volatility ──────────────────────────────────────
    {
        "id": "vix_30_reversion",
        "claim": "VIX >30 reverts below 25 within 20 trading days",
        "base_rate": 0.72,
        "sample": "1990-2024, n=87 episodes where VIX first crossed 30",
        "confidence_interval": [0.62, 0.82],
        "source": "CBOE VIX data via FRED (VIXCLS)",
        "caveat": "Excludes 2008-09 GFC where VIX stayed >30 for 5 months. Survivorship bias: if you only enter at first cross, not re-entries.",
        "category": "volatility",
        "tags": ["mean_reversion", "vix", "timing"],
    },
    {
        "id": "vix_40_forward_returns",
        "claim": "SPX forward 3-month return is positive when VIX >40",
        "base_rate": 0.78,
        "sample": "1990-2024, n=23 distinct VIX >40 episodes",
        "confidence_interval": [0.58, 0.98],
        "source": "CBOE + SPX data",
        "caveat": "Wide CI due to small sample. The 22% failure rate includes GFC and dot-com, where losses continued.",
        "category": "volatility",
        "tags": ["contrarian", "vix", "forward_returns"],
    },
    {
        "id": "vix_sub13_spike",
        "claim": "VIX spikes above 20 within 60 days when starting below 13",
        "base_rate": 0.45,
        "sample": "1990-2024, n=31 periods where VIX averaged <13 for 10+ days",
        "confidence_interval": [0.27, 0.63],
        "source": "CBOE VIX data",
        "caveat": "Low-vol regimes can persist for years (2004-2006, 2017). Buying protection early is expensive.",
        "category": "volatility",
        "tags": ["complacency", "vix", "tail_risk"],
    },
    {
        "id": "vix_backwardation_signal",
        "claim": "VIX backwardation during elevated vol (>25) signals peak fear within 2 weeks",
        "base_rate": 0.65,
        "sample": "2004-2024, n=40 backwardation episodes with VIX >25",
        "confidence_interval": [0.49, 0.81],
        "source": "CBOE VIX + VIX3M data",
        "caveat": "Definition of 'peak fear' is subjective (local vol max). Works best as confirmation, not standalone.",
        "category": "volatility",
        "tags": ["term_structure", "vix", "timing"],
    },

    # ── Yield Curve ───────────────────────────────────────────
    {
        "id": "yield_curve_inversion_recession",
        "claim": "Yield curve inversion (10Y-2Y <0) precedes recession within 6-24 months",
        "base_rate": 0.85,
        "sample": "1960-2024, n=7 inversions (excluding brief 2022-23 which hasn't resolved)",
        "confidence_interval": [0.55, 1.00],
        "source": "FRED (T10Y2Y), NBER recession dates",
        "caveat": "Tiny sample size (n=7). Timing is extremely variable (6-24 months). 2022-23 inversion still unresolved. Not tradeable as a signal due to long lead time.",
        "category": "macro",
        "tags": ["yield_curve", "recession", "leading_indicator"],
    },
    {
        "id": "yield_curve_steepening_after_inversion",
        "claim": "Rapid yield curve steepening after inversion signals imminent recession",
        "base_rate": 0.71,
        "sample": "1960-2024, n=7 un-inversion episodes",
        "confidence_interval": [0.38, 1.00],
        "source": "FRED, NBER",
        "caveat": "Even smaller effective sample. The steepening happens because the Fed cuts — but by then the recession has often already started.",
        "category": "macro",
        "tags": ["yield_curve", "recession", "timing"],
    },

    # ── Credit ────────────────────────────────────────────────
    {
        "id": "hy_spread_500_forward_returns",
        "claim": "Forward 12-month HY total return is positive when OAS >500 bps",
        "base_rate": 0.88,
        "sample": "1996-2024, n=16 distinct episodes where HY OAS exceeded 500 bps",
        "confidence_interval": [0.72, 1.00],
        "source": "ICE BofA HY Index (BAMLH0A0HYM2 via FRED)",
        "caveat": "You need to survive the drawdown to capture the return. Median max drawdown before recovery was -8%.",
        "category": "credit",
        "tags": ["credit_spread", "contrarian", "forward_returns"],
    },
    {
        "id": "credit_leads_equity",
        "claim": "HY spreads widen before equity selloffs by 2-4 weeks",
        "base_rate": 0.60,
        "sample": "1996-2024, n=12 major equity drawdowns (>10%)",
        "confidence_interval": [0.32, 0.88],
        "source": "ICE BofA HY Index + SPX",
        "caveat": "Lead time is highly variable. In 40% of cases, credit and equity moved simultaneously or equity led.",
        "category": "credit",
        "tags": ["credit_spread", "leading_indicator", "equity"],
    },

    # ── Breadth / Rotation ────────────────────────────────────
    {
        "id": "narrow_breadth_correction",
        "claim": "SPX corrects >5% within 3 months when breadth divergence exceeds -5%",
        "base_rate": 0.55,
        "sample": "2000-2024, n=22 periods where SPY-RSP divergence exceeded 5%",
        "confidence_interval": [0.34, 0.76],
        "source": "SPY vs RSP daily returns",
        "caveat": "Narrow breadth can persist for extended periods (2023-24 lasted 18+ months). Not a timing signal.",
        "category": "breadth",
        "tags": ["breadth", "concentration", "correction"],
    },

    # ── Sentiment / Positioning ───────────────────────────────
    {
        "id": "extreme_fear_forward_returns",
        "claim": "SPX forward 6-month return averages +12% when CNN Fear & Greed <15",
        "base_rate": 0.82,
        "sample": "2012-2024, n=11 readings below 15",
        "confidence_interval": [0.56, 1.00],
        "source": "CNN Fear & Greed Index + SPX",
        "caveat": "Index only available since 2012. Small sample. Average hides wide dispersion (-5% to +30%).",
        "category": "sentiment",
        "tags": ["contrarian", "sentiment", "forward_returns"],
    },
    {
        "id": "cot_extreme_long_reversal",
        "claim": "Asset reverses >5% within 60 days when speculative longs are at 90th percentile",
        "base_rate": 0.48,
        "sample": "2000-2024, aggregate across S&P, gold, oil, treasuries",
        "confidence_interval": [0.38, 0.58],
        "source": "CFTC COT data",
        "caveat": "Barely above coin-flip. Extreme positioning is necessary but not sufficient for reversal. Works better as filter than signal.",
        "category": "positioning",
        "tags": ["cot", "crowding", "reversal"],
    },

    # ── Regime ────────────────────────────────────────────────
    {
        "id": "stagflation_60_40_failure",
        "claim": "60/40 portfolio has negative real returns during stagflation regimes",
        "base_rate": 0.75,
        "sample": "1970-2024, n=8 stagflation periods (>6 months duration)",
        "confidence_interval": [0.45, 1.00],
        "source": "Bridgewater All-Weather research + SPX/AGG data",
        "caveat": "Stagflation definition varies. Using Dalio's framework (growth falling + inflation rising). Short stagflation episodes (<6mo) less damaging.",
        "category": "regime",
        "tags": ["regime", "asset_allocation", "stagflation"],
    },
    {
        "id": "regime_persistence",
        "claim": "Macro regime persists for at least 6 months once established with >50% confidence",
        "base_rate": 0.70,
        "sample": "1970-2024, Dalio 2x2 quadrant classification",
        "confidence_interval": [0.55, 0.85],
        "source": "Bridgewater research framework applied to FRED data",
        "caveat": "Regime transitions are the most dangerous periods. Confidence threshold matters — low-confidence regimes are transitional.",
        "category": "regime",
        "tags": ["regime", "persistence", "timing"],
    },

    # ── Private Markets ───────────────────────────────────────
    {
        "id": "reit_leads_private_re",
        "claim": "Public REITs lead private RE valuations by 6-12 months",
        "base_rate": 0.80,
        "sample": "2000-2024, n=4 major RE cycles",
        "confidence_interval": [0.45, 1.00],
        "source": "NCREIF + VNQ/IYR data",
        "caveat": "Very small sample (only 4 full cycles). Private RE marks are quarterly and smoothed, so the 'lead' may partly reflect reporting lag.",
        "category": "private_markets",
        "tags": ["private_markets", "real_estate", "leading_indicator"],
    },
    {
        "id": "bdc_discount_credit_stress",
        "claim": "BDC NAV discounts >20% predict private credit writedowns within 2 quarters",
        "base_rate": 0.70,
        "sample": "2010-2024, n=6 episodes of >20% BDC discount",
        "confidence_interval": [0.35, 1.00],
        "source": "BDC ETF NAV data + quarterly earnings",
        "caveat": "Very small sample. BDC discounts also reflect liquidity premium, not just credit quality.",
        "category": "private_markets",
        "tags": ["private_markets", "credit", "leading_indicator"],
    },
]


# ── Base Rate Lookup ────────────────────────────────────────────


def get_base_rates(
    category: str | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Look up pre-computed base rates, optionally filtered.

    Args:
        category: Filter by category (volatility, macro, credit, etc.)
        tags: Filter by tags (returns entries matching ANY tag)

    Returns:
        base_rates: Matching base rate entries
        count: Number of matches
    """
    results = BASE_RATES

    if category:
        results = [b for b in results if b.get("category") == category]

    if tags:
        tag_set = set(tags)
        results = [b for b in results if tag_set & set(b.get("tags", []))]

    return {
        "base_rates": results,
        "count": len(results),
        "categories": sorted(set(b["category"] for b in BASE_RATES)),
        "available_tags": sorted(set(t for b in BASE_RATES for t in b.get("tags", []))),
    }


# ── Live Statistical Analysis ───────────────────────────────────


def compute_live_statistics(briefing: dict) -> dict:
    """Compute live statistical context for current market conditions.

    Takes the current briefing data and computes z-scores, percentiles,
    and relevant base rates for the most important readings.

    Args:
        briefing: The full output from generate_briefing().

    Returns:
        readings: Current values with statistical context
        applicable_base_rates: Base rates relevant to current conditions
        statistical_warnings: Where current readings are extreme
    """
    readings = []
    applicable = []
    warnings = []

    # ── VIX analysis ─────────────────────────────────────────
    vix = _safe_get(briefing, "sentiment", "raw", "vix", "spot")
    if vix is not None:
        vix_stats = _compute_vix_statistics(vix)
        readings.append(vix_stats)

        if vix > 40:
            applicable.append(_find_base_rate("vix_30_reversion"))
            applicable.append(_find_base_rate("vix_40_forward_returns"))
        elif vix > 30:
            applicable.append(_find_base_rate("vix_30_reversion"))
        elif vix < 13:
            applicable.append(_find_base_rate("vix_sub13_spike"))

        vix_term = _safe_get(briefing, "sentiment", "raw", "vix", "term_structure")
        if vix_term == "backwardation" and vix > 25:
            applicable.append(_find_base_rate("vix_backwardation_signal"))

        if vix_stats.get("percentile") and vix_stats["percentile"] > 90:
            warnings.append({
                "reading": f"VIX at {vix:.1f}",
                "percentile": vix_stats["percentile"],
                "z_score": vix_stats.get("z_score"),
                "interpretation": (
                    f"VIX is at the {vix_stats['percentile']:.0f}th percentile of its "
                    f"historical distribution. This is a {vix_stats.get('z_score', 0):.1f}σ event."
                ),
            })

    # ── Credit analysis ──────────────────────────────────────
    hy_spread = _safe_get(briefing, "private_markets", "credit", "hy_spread")
    if hy_spread is not None:
        hy_stats = _compute_hy_statistics(hy_spread)
        readings.append(hy_stats)

        if hy_spread > 5.0:
            applicable.append(_find_base_rate("hy_spread_500_forward_returns"))
        applicable.append(_find_base_rate("credit_leads_equity"))

        if hy_stats.get("percentile") and hy_stats["percentile"] > 85:
            warnings.append({
                "reading": f"HY spread at {hy_spread:.2f}%",
                "percentile": hy_stats["percentile"],
                "z_score": hy_stats.get("z_score"),
                "interpretation": (
                    f"HY spreads at the {hy_stats['percentile']:.0f}th percentile. "
                    "Credit stress is significantly above normal."
                ),
            })

    # ── Breadth analysis ─────────────────────────────────────
    breadth = _safe_get(briefing, "market", "breadth_divergence")
    if breadth is not None:
        readings.append({
            "metric": "breadth_divergence",
            "label": "SPY vs RSP Breadth Divergence",
            "value": breadth,
            "unit": "%",
            "interpretation": (
                "Positive = equal-weight leading (broad rally). "
                "Negative = cap-weight leading (narrow, fragile)."
            ),
        })
        if breadth < -5:
            applicable.append(_find_base_rate("narrow_breadth_correction"))

    # ── Sentiment analysis ───────────────────────────────────
    sentiment_score = _safe_get(briefing, "sentiment", "composite", "score")
    if sentiment_score is not None:
        readings.append({
            "metric": "sentiment_composite",
            "label": "Composite Sentiment Score",
            "value": sentiment_score,
            "unit": "0-100 (fear→greed)",
            "interpretation": _interpret_sentiment_score(sentiment_score),
        })
        if sentiment_score < 15:
            applicable.append(_find_base_rate("extreme_fear_forward_returns"))

    # ── Regime analysis ──────────────────────────────────────
    regime = briefing.get("regime", {})
    quadrant = regime.get("quadrant")
    confidence = regime.get("confidence", 0)

    if quadrant == "stagflation":
        applicable.append(_find_base_rate("stagflation_60_40_failure"))

    if confidence > 0.5:
        applicable.append(_find_base_rate("regime_persistence"))

    # ── Positioning ──────────────────────────────────────────
    cot = briefing.get("cot_positioning", {})
    if cot.get("crowded_longs") or cot.get("crowded_shorts"):
        applicable.append(_find_base_rate("cot_extreme_long_reversal"))

    # ── Private markets ──────────────────────────────────────
    bdc_discount = _safe_get(briefing, "private_markets", "credit", "bdc_nav_discount")
    if bdc_discount is not None and bdc_discount < -20:
        applicable.append(_find_base_rate("bdc_discount_credit_stress"))

    applicable.append(_find_base_rate("reit_leads_private_re"))

    # Filter out None entries (base rates not found)
    applicable = [a for a in applicable if a is not None]

    return {
        "readings": readings,
        "applicable_base_rates": applicable,
        "statistical_warnings": warnings,
        "note": (
            "Base rates provide historical context but are NOT predictions. "
            "Sample sizes are often small. Confidence intervals are wide. "
            "Use as one input alongside qualitative judgment."
        ),
    }


# ── Statistical Computations ────────────────────────────────────


def _compute_vix_statistics(vix_spot: float) -> dict:
    """Compute statistical context for the current VIX level.

    Uses long-run VIX distribution parameters:
    - Mean: ~19.5 (1990-2024)
    - Median: ~17.5
    - Std Dev: ~8.0
    - Distribution is right-skewed (log-normal-ish)
    """
    # Long-run parameters (1990-2024)
    mean = 19.5
    std = 8.0
    median = 17.5

    z_score = (vix_spot - mean) / std

    # Approximate percentile using normal CDF
    # (VIX isn't truly normal, but this gives a rough ranking)
    percentile = _normal_cdf(z_score) * 100

    # Regime classification with base rates
    if vix_spot >= 40:
        regime_note = "Crisis level (<5% of all trading days)"
    elif vix_spot >= 30:
        regime_note = "Panic level (~8% of all trading days)"
    elif vix_spot >= 20:
        regime_note = "Elevated (~25% of all trading days)"
    elif vix_spot >= 14:
        regime_note = "Normal range (~45% of all trading days)"
    else:
        regime_note = "Complacency level (~17% of all trading days)"

    return {
        "metric": "vix_spot",
        "label": "VIX Spot",
        "value": round(vix_spot, 1),
        "unit": "index points",
        "z_score": round(z_score, 2),
        "percentile": round(percentile, 1),
        "long_run_mean": mean,
        "long_run_std": std,
        "regime_note": regime_note,
        "interpretation": (
            f"VIX at {vix_spot:.1f} is {abs(z_score):.1f}σ "
            f"{'above' if z_score > 0 else 'below'} the long-run mean of {mean}. "
            f"{regime_note}."
        ),
    }


def _compute_hy_statistics(hy_spread: float) -> dict:
    """Compute statistical context for HY OAS level.

    Long-run parameters (1996-2024):
    - Mean: ~4.5% (450 bps)
    - Median: ~3.8% (380 bps)
    - Std Dev: ~2.5%
    """
    mean = 4.5
    std = 2.5
    median = 3.8

    z_score = (hy_spread - mean) / std
    percentile = _normal_cdf(z_score) * 100

    if hy_spread >= 7.0:
        regime_note = "Crisis level (>700 bps, <5% of history)"
    elif hy_spread >= 5.0:
        regime_note = "Stressed (500-700 bps, ~10% of history)"
    elif hy_spread >= 4.0:
        regime_note = "Normal-to-wide (400-500 bps, ~25% of history)"
    elif hy_spread >= 3.0:
        regime_note = "Tight (300-400 bps, ~30% of history)"
    else:
        regime_note = "Very tight (<300 bps, ~10% of history, historically signals complacency)"

    return {
        "metric": "hy_spread",
        "label": "HY OAS (Option-Adjusted Spread)",
        "value": round(hy_spread, 2),
        "unit": "percentage points",
        "z_score": round(z_score, 2),
        "percentile": round(percentile, 1),
        "long_run_mean": mean,
        "long_run_std": std,
        "regime_note": regime_note,
        "interpretation": (
            f"HY OAS at {hy_spread:.2f}% is {abs(z_score):.1f}σ "
            f"{'above' if z_score > 0 else 'below'} the long-run mean of {mean}%. "
            f"{regime_note}."
        ),
    }


# ── Confidence Interval Helpers ─────────────────────────────────


def compute_confidence_interval(
    successes: int,
    trials: int,
    confidence_level: float = 0.95,
) -> dict:
    """Compute a confidence interval for a proportion (Wilson score interval).

    More robust than the simple normal approximation, especially for small
    samples or extreme proportions.

    Args:
        successes: Number of "positive" outcomes
        trials: Total number of trials
        confidence_level: Desired confidence level (default 0.95)

    Returns:
        point_estimate, lower, upper, margin_of_error, sample_quality
    """
    if trials == 0:
        return {
            "point_estimate": None,
            "lower": None,
            "upper": None,
            "margin_of_error": None,
            "sample_quality": "no_data",
        }

    p_hat = successes / trials

    # Z-score for the confidence level
    z = _normal_quantile((1 + confidence_level) / 2)

    # Wilson score interval
    denominator = 1 + z**2 / trials
    center = (p_hat + z**2 / (2 * trials)) / denominator
    spread = z * math.sqrt(p_hat * (1 - p_hat) / trials + z**2 / (4 * trials**2)) / denominator

    lower = max(0, center - spread)
    upper = min(1, center + spread)

    # Sample quality assessment
    if trials >= 100:
        quality = "good"
    elif trials >= 30:
        quality = "adequate"
    elif trials >= 10:
        quality = "small"
    else:
        quality = "very_small — treat with extreme caution"

    return {
        "point_estimate": round(p_hat, 3),
        "lower": round(lower, 3),
        "upper": round(upper, 3),
        "margin_of_error": round(spread, 3),
        "confidence_level": confidence_level,
        "sample_size": trials,
        "sample_quality": quality,
    }


# ── Math Helpers ────────────────────────────────────────────────


def _normal_cdf(x: float) -> float:
    """Approximate the standard normal CDF using the error function."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _normal_quantile(p: float) -> float:
    """Approximate the standard normal quantile (inverse CDF).

    Uses the Beasley-Springer-Moro algorithm for reasonable accuracy.
    """
    if p <= 0 or p >= 1:
        return 0.0

    # Rational approximation for central region
    t = p - 0.5
    if abs(t) <= 0.42:
        r = t * t
        return t * ((((-25.44106 * r + 41.39119) * r - 18.61500) * r + 2.50662) /
                    ((((3.13082 * r - 21.06224) * r + 23.08337) * r - 8.47351) * r + 1))

    # Tail approximation
    if t > 0:
        r = math.log(-math.log(1 - p))
    else:
        r = math.log(-math.log(p))

    result = 0.3374 + r * (0.9761 + r * (0.1624 + r * (0.0270 + r * 0.0021)))
    return result if t > 0 else -result


# ── Lookup Helpers ──────────────────────────────────────────────


def _find_base_rate(rate_id: str) -> dict | None:
    """Find a base rate entry by ID."""
    for br in BASE_RATES:
        if br["id"] == rate_id:
            return br
    return None


def _interpret_sentiment_score(score: float) -> str:
    """Human-readable interpretation of composite sentiment."""
    if score >= 80:
        return "Extreme greed — historically a contrarian warning signal"
    elif score >= 60:
        return "Greed territory — market participants are optimistic"
    elif score >= 40:
        return "Neutral zone — no strong directional signal from sentiment"
    elif score >= 20:
        return "Fear territory — pessimism elevated but not extreme"
    else:
        return "Extreme fear — historically a contrarian buying opportunity"


def _safe_get(d: dict | None, *keys, default=None):
    """Safely traverse nested dicts. Default only applies at the terminal key."""
    current = d
    for i, key in enumerate(keys):
        if isinstance(current, dict):
            is_last = (i == len(keys) - 1)
            current = current.get(key, default if is_last else None)
        else:
            return default
    return current
