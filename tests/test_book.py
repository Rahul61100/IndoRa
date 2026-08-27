import pytest

from predict.book import (accept_view, create_proposition, create_view, edge,
                          map_market, reject_view)
from predict.db import connect, init_schema
from predict.ingest import append_odds, upsert_markets
from predict.venues.base import RawMarket


def setup(tmp_path, bid=0.29, ask=0.31):
    c = connect(tmp_path / "t.db")
    init_schema(c)
    m = RawMarket(venue="polymarket", venue_market_id="1", question="q",
                  prob_yes=0.30, best_bid=bid, best_ask=ask, liquidity=5000.0)
    upsert_markets(c, [m])
    append_odds(c, [m], "2026-08-27T00:00:00")
    pid = create_proposition(c, "Fed raises in September")
    map_market(c, 1, pid)
    return c, pid


def test_edge_crosses_the_spread_never_uses_the_mid():
    # Mid is 0.30. Using it would report +0.15 for YES; the honest number
    # is against the ask, because that is the price you actually pay.
    assert edge(0.45, 0.29, 0.31, "yes") == pytest.approx(0.14)
    assert edge(0.20, 0.29, 0.31, "no") == pytest.approx(0.09)


def test_edge_is_negative_when_the_market_is_right():
    assert edge(0.30, 0.29, 0.31, "yes") == pytest.approx(-0.01)


def test_edge_rejects_an_unknown_direction():
    with pytest.raises(ValueError):
        edge(0.5, 0.29, 0.31, "maybe")


def test_accept_snapshots_entry_prices_at_accept_time(tmp_path):
    c, pid = setup(tmp_path)
    vid = create_view(c, pid, 0.45, "medium", "because", ["fed-may-hike-next"])
    posid = accept_view(c, vid, 1, "yes")
    row = c.execute("SELECT * FROM positions WHERE id=?", (posid,)).fetchone()
    assert row["bid_at_entry"] == 0.29 and row["ask_at_entry"] == 0.31
    assert row["liquidity_at_entry"] == 5000.0
    assert row["market_prob_at_entry"] == pytest.approx(0.30)
    assert row["edge"] == pytest.approx(0.14)
    assert c.execute("SELECT status FROM views WHERE id=?", (vid,)).fetchone()[0] == "accepted"


def test_accept_raises_when_the_view_does_not_exist(tmp_path):
    c, pid = setup(tmp_path)
    with pytest.raises(ValueError):
        accept_view(c, 9999, 1, "yes")


def test_accept_raises_when_the_market_does_not_exist(tmp_path):
    c, pid = setup(tmp_path)
    vid = create_view(c, pid, 0.45, "medium")
    with pytest.raises(ValueError):
        accept_view(c, vid, 9999, "yes")


def test_accept_raises_when_no_odds_row_exists_for_the_market(tmp_path):
    c, pid = setup(tmp_path)
    m2 = RawMarket(venue="polymarket", venue_market_id="2", question="q2",
                   prob_yes=0.5, best_bid=0.4, best_ask=0.6, liquidity=1000.0)
    upsert_markets(c, [m2])  # no append_odds for this market
    market_id = c.execute(
        "SELECT id FROM markets WHERE venue_market_id=?", ("2",)).fetchone()[0]
    map_market(c, market_id, pid)
    vid = create_view(c, pid, 0.45, "medium")
    with pytest.raises(ValueError):
        accept_view(c, vid, market_id, "yes")


def test_accept_refuses_a_null_bid_or_ask_instead_of_using_a_stale_row(tmp_path):
    c, pid = setup(tmp_path, bid=None, ask=None)
    vid = create_view(c, pid, 0.45, "medium")
    with pytest.raises(ValueError, match="no tradeable price"):
        accept_view(c, vid, 1, "yes")


def test_accepting_a_market_not_mapped_to_the_view_is_refused(tmp_path):
    c, pid = setup(tmp_path)
    other = create_proposition(c, "unrelated")
    vid = create_view(c, other, 0.45, "low")
    with pytest.raises(ValueError, match="not mapped"):
        accept_view(c, vid, 1, "yes")


def test_reject_records_a_categorical_reason(tmp_path):
    c, pid = setup(tmp_path)
    vid = create_view(c, pid, 0.45, "low")
    reject_view(c, vid, "market is right", "spread too wide")
    r = c.execute("SELECT status, review_reason FROM views WHERE id=?", (vid,)).fetchone()
    assert r["status"] == "rejected" and r["review_reason"] == "market is right"


def test_reject_refuses_an_uncategorised_reason(tmp_path):
    c, pid = setup(tmp_path)
    vid = create_view(c, pid, 0.45, "low")
    with pytest.raises(ValueError):
        reject_view(c, vid, "just because")


def test_claim_ids_round_trip(tmp_path):
    c, pid = setup(tmp_path)
    vid = create_view(c, pid, 0.4, "medium", claim_ids=["a", "b"])
    assert c.execute("SELECT claim_ids FROM views WHERE id=?", (vid,)).fetchone()[0] == "a,b"
