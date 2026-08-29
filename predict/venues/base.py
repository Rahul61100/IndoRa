"""The normalised shape every venue adapter produces.

Adding Kalshi or Manifold later means writing one more module that returns
these -- ingest, storage and the UI never learn a venue's field names.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RawMarket:
    venue: str
    venue_market_id: str
    question: str
    description: str = ""
    resolution_rules: str = ""
    end_date: str | None = None
    prob_yes: float | None = None
    best_bid: float | None = None
    best_ask: float | None = None
    liquidity: float = 0.0
    volume: float = 0.0
    n_traders: int | None = None
    closed: bool = False
    resolved: bool = False
    resolved_outcome: str | None = None
    untradeable: bool = False
    raw: dict = field(default_factory=dict, repr=False, compare=False)
