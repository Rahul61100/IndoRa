"""Polymarket adapter.

Two traps verified live on 2026-08-27:
  1. `outcomePrices` is a JSON STRING, not an array. Indexing it gives '['.
  2. The bulk feed caps around 2,100 rows (HTTP 422 beyond) and is
     volume-ordered -- so a market can leave the window while still open.
     Never read absence as resolution.
"""
from __future__ import annotations

import json

from .base import RawMarket

VENUE = "polymarket"
PROB_SUM_TOLERANCE = 0.02
WIDE_SPREAD = 0.25


def _f(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def parse_market(raw: dict) -> RawMarket | None:
    """Normalise one Gamma market. Returns None when the row is unusable."""
    mid = raw.get("id")
    if mid is None or not raw.get("question"):
        return None

    prob = None
    prices_field = raw.get("outcomePrices")
    if prices_field is not None:
        try:
            prices = json.loads(prices_field) if isinstance(prices_field, str) else prices_field
            vals = [float(p) for p in prices]
        except (json.JSONDecodeError, TypeError, ValueError):
            return None
        if len(vals) == 2 and abs(sum(vals) - 1.0) > PROB_SUM_TOLERANCE:
            return None            # the two legs disagree: the row is wrong
        prob = vals[0] if vals else None

    bid, ask = _f(raw.get("bestBid")), _f(raw.get("bestAsk"))
    if bid is not None and ask is not None and bid > ask:
        return None                # crossed book

    untradeable = False
    if bid is not None and ask is not None:
        mid_px = (bid + ask) / 2
        if mid_px > 0 and (ask - bid) / mid_px > WIDE_SPREAD:
            untradeable = True     # keep the history, do not price off it

    return RawMarket(
        venue=VENUE,
        venue_market_id=str(mid),
        question=raw.get("question") or "",
        description=raw.get("description") or "",
        resolution_rules=raw.get("resolutionSource") or "",
        end_date=(raw.get("endDateIso") or None),
        prob_yes=prob,
        best_bid=bid,
        best_ask=ask,
        liquidity=_f(raw.get("liquidityNum")) or 0.0,
        volume=_f(raw.get("volumeNum")) or 0.0,
        n_traders=None,
        closed=bool(raw.get("closed")),
        resolved=bool(raw.get("resolved")),
        resolved_outcome=raw.get("resolvedOutcome"),
        untradeable=untradeable,
        raw=raw,
    )
