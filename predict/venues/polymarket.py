"""Polymarket adapter.

Two traps verified live on 2026-08-27:
  1. `outcomePrices` is a JSON STRING, not an array. Indexing it gives '['.
  2. The bulk feed caps around 2,100 rows (HTTP 422 beyond) and is
     volume-ordered -- so a market can leave the window while still open.
     Never read absence as resolution.
"""
from __future__ import annotations

import json
import time

import requests

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


GAMMA = "https://gamma-api.polymarket.com/markets"
UA = {"User-Agent": "market-intel/1.0 (research)"}


def fetch_open(session=None, max_pages: int = 21, page_size: int = 100,
               sleep_s: float = 0.25) -> list[RawMarket]:
    """Page the open+active feed, newest-volume first.

    Stops on a short page or a non-200. A 422 is the documented end of the
    window (~2,100 rows) -- it means "no more rows here", never "those
    markets resolved".
    """
    s = session or requests.Session()
    if session is None:
        s.headers.update(UA)
    out, offset = [], 0
    for _ in range(max_pages):
        r = s.get(GAMMA, params={"limit": page_size, "offset": offset,
                                 "closed": "false", "active": "true",
                                 "order": "volumeNum", "ascending": "false"},
                  timeout=40)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        for row in batch:
            m = parse_market(row)
            if m is not None:
                out.append(m)
        offset += page_size
        if len(batch) < page_size:
            break
        if sleep_s:
            time.sleep(sleep_s)
    return out
