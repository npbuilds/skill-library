"""Private markets processor — synthesize REIT, BDC, PE, and VC proxy data
into cycle classifications, divergence scores, and exit window assessments."""

from datetime import datetime


def classify_re_cycle(fred_data: dict, proxy_data: dict) -> dict:
    """Classify the real estate cycle using FRED macro + REIT proxy data.

    Combines mortgage rates, housing starts, NAHB index, Case-Shiller,
    and REIT performance to position the RE cycle.
    """
    result = {}

    # Inputs from FRED
    indicators = fred_data.get("indicators", {})
    mortgage = indicators.get("MORTGAGE30US", {}).get("value")
    starts = indicators.get("HOUST", {}).get("value")
    nahb = indicators.get("NAHBHMI", {}).get("value")
    case_shiller_yoy = indicators.get("CSUSHPINSA", {}).get("yoy_change")
    vacancy = indicators.get("RRVRUSQ156N", {}).get("value")

    # Inputs from proxies
    vnq = proxy_data.get("reits", {}).get("Vanguard Real Estate ETF", {})
    vnq_ytd = vnq.get("ytd_pct")
    structural_spread = proxy_data.get("re_structural_spread")

    # Residential cycle score (higher = healthier)
    residential_score = 0
    signals = []

    if nahb is not None:
        if nahb > 50:
            residential_score += 2
            signals.append(f"Builder confidence strong ({nahb})")
        elif nahb > 40:
            residential_score += 1
            signals.append(f"Builder confidence moderate ({nahb})")
        else:
            residential_score -= 1
            signals.append(f"Builder confidence weak ({nahb})")

    if mortgage is not None:
        if mortgage < 5.5:
            residential_score += 2
            signals.append(f"Mortgage rates accommodative ({mortgage}%)")
        elif mortgage < 6.5:
            residential_score += 1
            signals.append(f"Mortgage rates moderate ({mortgage}%)")
        elif mortgage < 7.5:
            residential_score -= 1
            signals.append(f"Mortgage rates elevated ({mortgage}%)")
        else:
            residential_score -= 2
            signals.append(f"Mortgage rates severe ({mortgage}%)")

    if case_shiller_yoy is not None:
        if case_shiller_yoy > 5:
            residential_score += 1
            signals.append(f"Home prices accelerating ({case_shiller_yoy}% YoY)")
        elif case_shiller_yoy > 0:
            signals.append(f"Home prices positive ({case_shiller_yoy}% YoY)")
        else:
            residential_score -= 2
            signals.append(f"Home prices declining ({case_shiller_yoy}% YoY)")

    # Classify
    if residential_score >= 4:
        result["residential_cycle"] = "expansion"
    elif residential_score >= 1:
        result["residential_cycle"] = "recovery"
    elif residential_score >= -1:
        result["residential_cycle"] = "late_cycle"
    else:
        result["residential_cycle"] = "contraction"

    result["residential_score"] = residential_score
    result["residential_signals"] = signals

    # Commercial RE assessment (from REIT subsectors)
    result["structural_spread"] = structural_spread
    result["structural_signal"] = proxy_data.get("re_structural_signal")

    # Overall RE assessment
    result["vnq_ytd"] = vnq_ytd
    if vnq_ytd is not None:
        if vnq_ytd > 10:
            result["reit_market_regime"] = "bull"
        elif vnq_ytd > 0:
            result["reit_market_regime"] = "positive"
        elif vnq_ytd > -10:
            result["reit_market_regime"] = "correction"
        else:
            result["reit_market_regime"] = "bear"

    return result


def classify_credit_cycle(fred_data: dict, proxy_data: dict) -> dict:
    """Classify the private credit cycle using spreads, BDC data, and lending standards."""
    result = {}

    indicators = fred_data.get("indicators", {})
    hy_oas = indicators.get("BAMLH0A0HYM2", {}).get("value")
    bbb_oas = indicators.get("BAMLC0A4CBBB", {}).get("value")
    aaa_oas = indicators.get("BAMLC0A1CAAA", {}).get("value")
    lending_std = indicators.get("DRTSCILM", {}).get("value")
    real_yield = indicators.get("DFII10", {}).get("value")

    bdc_discount = proxy_data.get("bdc_avg_nav_discount")
    bdc_signal = proxy_data.get("bdc_signal")

    credit_score = 0
    signals = []

    # HY spread (FRED returns percentage points, e.g. 3.21 = 321 bps)
    if hy_oas is not None:
        result["hy_spread"] = hy_oas
        if hy_oas < 3.0:
            credit_score += 2
            signals.append(f"HY spreads tight ({hy_oas:.2f}%, {hy_oas*100:.0f} bps) — easy credit")
        elif hy_oas < 4.0:
            credit_score += 1
            signals.append(f"HY spreads normal ({hy_oas:.2f}%, {hy_oas*100:.0f} bps)")
        elif hy_oas < 5.5:
            credit_score -= 1
            signals.append(f"HY spreads elevated ({hy_oas:.2f}%, {hy_oas*100:.0f} bps) — caution")
        else:
            credit_score -= 2
            signals.append(f"HY spreads stressed ({hy_oas:.2f}%, {hy_oas*100:.0f} bps) — distress risk")

    # Quality spread (BBB-AAA, percentage points)
    if bbb_oas is not None and aaa_oas is not None:
        quality_spread = bbb_oas - aaa_oas
        result["quality_spread"] = round(quality_spread, 2)
        if quality_spread > 1.5:
            credit_score -= 1
            signals.append(
                f"Quality spread wide ({quality_spread:.2f}%, {quality_spread*100:.0f} bps) — credit differentiation"
            )

    # BDC NAV discount
    if bdc_discount is not None:
        result["bdc_nav_discount"] = bdc_discount
        if bdc_discount < -8:
            credit_score -= 2
            signals.append(
                f"BDCs at {bdc_discount:.1f}% NAV discount — market pricing credit losses"
            )
        elif bdc_discount < -3:
            credit_score -= 1
            signals.append(f"BDCs at {bdc_discount:.1f}% NAV discount — cautious")
        else:
            credit_score += 1
            signals.append(f"BDCs near/above NAV — confidence in credit quality")

    # Lending standards
    if lending_std is not None:
        result["lending_standards"] = lending_std
        if lending_std > 20:
            credit_score -= 1
            signals.append("Banks tightening lending significantly")
        elif lending_std < -10:
            credit_score += 1
            signals.append("Banks easing lending standards")

    # Classify
    if credit_score >= 3:
        result["credit_cycle"] = "expansion"
    elif credit_score >= 1:
        result["credit_cycle"] = "mid_cycle"
    elif credit_score >= -1:
        result["credit_cycle"] = "late_cycle"
    else:
        result["credit_cycle"] = "stress"

    result["credit_score"] = credit_score
    result["credit_signals"] = signals
    result["real_yield"] = real_yield

    return result


def assess_exit_window(proxy_data: dict) -> dict:
    """Assess the PE/VC exit window health using IPO ETF and GP stock performance."""
    result = {}
    signals = []

    # IPO ETF as exit window proxy
    ipo_etf = proxy_data.get("vc_proxies", {}).get("Renaissance IPO ETF", {})
    ipo_ytd = ipo_etf.get("ytd_pct")

    # PE GP stock performance = market's view on fee/carry revenue
    gp_avg_ytd = proxy_data.get("pe_gp_avg_ytd")

    # VC proxy composite
    vc_avg_ytd = proxy_data.get("vc_proxy_avg_ytd")

    # ARKK as growth multiple proxy
    arkk = proxy_data.get("vc_proxies", {}).get("ARK Innovation (VC proxy)", {})
    arkk_ytd = arkk.get("ytd_pct")

    exit_score = 0

    if ipo_ytd is not None:
        result["ipo_etf_ytd"] = ipo_ytd
        if ipo_ytd > 10:
            exit_score += 2
            signals.append(f"IPO market strong ({ipo_ytd:+.1f}% YTD)")
        elif ipo_ytd > 0:
            exit_score += 1
            signals.append(f"IPO market positive ({ipo_ytd:+.1f}% YTD)")
        elif ipo_ytd > -15:
            exit_score -= 1
            signals.append(f"IPO market weak ({ipo_ytd:+.1f}% YTD) — exit window narrowing")
        else:
            exit_score -= 2
            signals.append(f"IPO market collapsed ({ipo_ytd:+.1f}% YTD) — exit window frozen")

    if gp_avg_ytd is not None:
        result["gp_avg_ytd"] = gp_avg_ytd
        if gp_avg_ytd > 10:
            exit_score += 1
            signals.append(f"PE GP stocks strong ({gp_avg_ytd:+.1f}%) — fundraising healthy")
        elif gp_avg_ytd < -10:
            exit_score -= 1
            signals.append(
                f"PE GP stocks weak ({gp_avg_ytd:+.1f}%) — market doubts exit/fundraising"
            )

    if arkk_ytd is not None:
        result["arkk_ytd"] = arkk_ytd
        if arkk_ytd < -20:
            exit_score -= 1
            signals.append(
                f"Growth multiples compressing ({arkk_ytd:+.1f}%) — VC marks at risk"
            )
        elif arkk_ytd > 15:
            exit_score += 1
            signals.append(
                f"Growth multiples expanding ({arkk_ytd:+.1f}%) — VC marks improving"
            )

    # Classify exit window
    if exit_score >= 3:
        result["exit_window"] = "wide_open"
    elif exit_score >= 1:
        result["exit_window"] = "open"
    elif exit_score >= -1:
        result["exit_window"] = "narrowing"
    else:
        result["exit_window"] = "frozen"

    result["exit_score"] = exit_score
    result["exit_signals"] = signals
    result["vc_proxy_avg_ytd"] = vc_avg_ytd

    return result


def compute_public_private_divergence(proxy_data: dict) -> dict:
    """Score how much public proxies diverge from where private marks likely sit.

    Public market prices lead private valuations by 6-12 months. When public
    proxies are down significantly but private marks haven't adjusted, the
    divergence signals future write-downs.
    """
    result = {"divergences": []}

    # REIT vs private RE (public REITs lead private by 6-12 months)
    vnq = proxy_data.get("reits", {}).get("Vanguard Real Estate ETF", {})
    vnq_ytd = vnq.get("ytd_pct")
    if vnq_ytd is not None:
        if vnq_ytd < -15:
            result["divergences"].append({
                "asset_class": "Real Estate",
                "public_proxy": f"VNQ {vnq_ytd:+.1f}% YTD",
                "private_lag": "Private RE marks likely 6-12 months behind",
                "signal": "write_down_risk",
                "severity": "high",
            })
        elif vnq_ytd < -5:
            result["divergences"].append({
                "asset_class": "Real Estate",
                "public_proxy": f"VNQ {vnq_ytd:+.1f}% YTD",
                "private_lag": "Moderate gap — watch for next appraisal cycle",
                "signal": "monitoring",
                "severity": "medium",
            })

    # BDC NAV discount → private credit divergence
    bdc_discount = proxy_data.get("bdc_avg_nav_discount")
    if bdc_discount is not None and bdc_discount < -8:
        result["divergences"].append({
            "asset_class": "Private Credit",
            "public_proxy": f"BDC index at {bdc_discount:.1f}% NAV discount",
            "private_lag": "Private credit funds haven't marked down yet",
            "signal": "write_down_risk",
            "severity": "high",
        })

    # ARKK vs VC marks
    arkk = proxy_data.get("vc_proxies", {}).get("ARK Innovation (VC proxy)", {})
    arkk_ytd = arkk.get("ytd_pct")
    if arkk_ytd is not None and arkk_ytd < -20:
        result["divergences"].append({
            "asset_class": "Venture Capital",
            "public_proxy": f"ARKK {arkk_ytd:+.1f}% YTD",
            "private_lag": "VC marks lag public comps by 2-4 quarters",
            "signal": "down_round_risk",
            "severity": "high",
        })

    # Overall divergence score
    high_count = sum(
        1 for d in result["divergences"] if d.get("severity") == "high"
    )
    if high_count >= 2:
        result["overall_divergence"] = "severe"
        result["divergence_note"] = (
            "Multiple private asset classes showing significant public-private "
            "valuation gaps. Expect write-downs in upcoming quarterly marks."
        )
    elif high_count == 1:
        result["overall_divergence"] = "elevated"
        result["divergence_note"] = (
            "One private asset class showing meaningful divergence from public proxies."
        )
    else:
        result["overall_divergence"] = "normal"
        result["divergence_note"] = "Public and private valuations roughly aligned."

    return result


def get_private_markets_dashboard(fred_data: dict, proxy_data: dict) -> dict:
    """Master function: assemble the complete private markets monitor."""
    result = {
        "real_estate": classify_re_cycle(fred_data, proxy_data),
        "credit": classify_credit_cycle(fred_data, proxy_data),
        "exit_window": assess_exit_window(proxy_data),
        "divergence": compute_public_private_divergence(proxy_data),
        "raw_proxies": {
            "reit_subsectors": proxy_data.get("reit_subsectors", {}),
            "pe_gps": proxy_data.get("pe_gps", {}),
            "bdcs": proxy_data.get("bdcs", {}),
            "vc_proxies": proxy_data.get("vc_proxies", {}),
        },
        "timestamp": datetime.now().isoformat(),
    }

    # Top-level summary
    re_cycle = result["real_estate"].get("residential_cycle", "unknown")
    credit_cycle = result["credit"].get("credit_cycle", "unknown")
    exit_win = result["exit_window"].get("exit_window", "unknown")
    divergence = result["divergence"].get("overall_divergence", "unknown")

    result["summary"] = {
        "real_estate_cycle": re_cycle,
        "credit_cycle": credit_cycle,
        "exit_window": exit_win,
        "public_private_divergence": divergence,
        "headline": (
            f"RE: {re_cycle} | Credit: {credit_cycle} | "
            f"Exits: {exit_win} | Divergence: {divergence}"
        ),
    }

    return result
