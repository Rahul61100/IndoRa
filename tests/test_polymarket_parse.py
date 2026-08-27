import json
from pathlib import Path

from predict.venues.polymarket import parse_market

FIX = Path(__file__).parent / "fixtures" / "polymarket_market.json"


def raw(**over):
    d = json.loads(FIX.read_text())
    d.update(over)
    return d


def test_outcome_prices_is_a_json_string_not_a_list():
    # The single most likely parsing bug: outcomePrices arrives as
    # '["0.0065", "0.9935"]' -- a STRING. Indexing it yields '['.
    m = parse_market(raw())
    assert m is not None
    assert isinstance(m.prob_yes, float)
    assert abs(m.prob_yes - 0.0065) < 1e-9


def test_bid_ask_are_kept_separate():
    m = parse_market(raw())
    assert m.best_bid == 0.006
    assert m.best_ask == 0.007
    assert m.best_bid < m.best_ask


def test_crossed_book_is_rejected():
    assert parse_market(raw(bestBid=0.9, bestAsk=0.1)) is None


def test_probabilities_must_sum_to_one():
    assert parse_market(raw(outcomePrices='["0.20", "0.20"]')) is None


def test_probabilities_within_tolerance_are_accepted():
    m = parse_market(raw(outcomePrices='["0.30", "0.69"]'))
    assert m is not None and abs(m.prob_yes - 0.30) < 1e-9


def test_wide_spread_is_flagged_untradeable_not_dropped():
    # 25%+ spread: keep the history, never price off it.
    m = parse_market(raw(bestBid=0.10, bestAsk=0.50))
    assert m is not None
    assert m.untradeable is True


def test_missing_price_fields_do_not_crash():
    d = raw()
    for k in ("bestBid", "bestAsk", "outcomePrices"):
        d.pop(k, None)
    m = parse_market(d)
    assert m is None or m.prob_yes is None


def test_malformed_outcome_prices_returns_none():
    assert parse_market(raw(outcomePrices="not json")) is None


def test_identity_and_rules_are_captured():
    m = parse_market(raw())
    assert m.venue == "polymarket"
    assert m.venue_market_id == "2063134"
    assert m.end_date == "2026-06-01"
    assert "raw" not in m.__dataclass_fields__ or isinstance(m.raw, dict)
