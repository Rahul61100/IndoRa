from predict.book import create_proposition, create_view, map_market
from predict.db import connect, init_schema
from predict.ingest import append_odds, upsert_markets
from predict.queries import claim_tiers, drift, queue_rows
from predict.venues.base import RawMarket


def mkt(bid, ask, prob, untradeable=False):
    return RawMarket(venue="polymarket", venue_market_id="1", question="Fed raises?",
                     prob_yes=prob, best_bid=bid, best_ask=ask, liquidity=368000.0,
                     untradeable=untradeable)


def test_drift_is_none_without_a_prior_price():
    assert drift(None, 0.31) is None


def test_drift_reports_the_move():
    assert round(drift(0.285, 0.310), 3) == 0.025


def test_queue_row_carries_live_odds_edge_and_claims(tmp_path):
    c = connect(tmp_path / "t.db")
    init_schema(c)
    upsert_markets(c, [mkt(0.29, 0.31, 0.30)])
    append_odds(c, [mkt(0.285, 0.295, 0.29)], "2026-08-27T00:00:00")
    append_odds(c, [mkt(0.29, 0.31, 0.30)], "2026-08-27T04:00:00")   # latest
    pid = create_proposition(c, "Fed raises in September", topic="fed")
    map_market(c, 1, pid)
    vid = create_view(c, pid, 0.45, "medium", "three dissents", ["fed-may-hike-next"])
    # Pin created_at BETWEEN the two odds rows, so "the price when this view
    # was formed" is the 00:00 row and drift is a real measurement. Without
    # this, create_view stamps a real now() that is after both fixture rows,
    # the baseline resolves to the latest row, and drift is trivially 0.0.
    c.execute("UPDATE views SET created_at='2026-08-27T02:00:00' WHERE id=?", (vid,))
    c.commit()

    rows = queue_rows(c)
    assert len(rows) == 1
    r = rows[0]
    assert r["statement"] == "Fed raises in September"
    assert r["best_ask"] == 0.31 and r["best_bid"] == 0.29
    assert round(r["edge_yes"], 3) == 0.14
    # "fed-may-hike-next" is not in the real data/sources.json -- an
    # unlooked-up claim must resolve to "unknown", never a fixed tier.
    assert r["claim_ids"] == [{"id": "fed-may-hike-next", "tier": "unknown"}]
    assert round(r["drift"], 3) == 0.010


def test_gate_line_states_the_gate_while_unproven(tmp_path):
    from predict.queries import gate_line
    c = connect(tmp_path / "t.db")
    init_schema(c)
    line = gate_line(c)
    assert "0 resolved" in line and "50 needed" in line
    assert "measures nothing" in line


def test_reviewed_views_leave_the_queue(tmp_path):
    c = connect(tmp_path / "t.db")
    init_schema(c)
    upsert_markets(c, [mkt(0.29, 0.31, 0.30)])
    append_odds(c, [mkt(0.29, 0.31, 0.30)], "2026-08-27T00:00:00")
    pid = create_proposition(c, "p")
    map_market(c, 1, pid)
    vid = create_view(c, pid, 0.45, "low")
    assert len(queue_rows(c)) == 1
    c.execute("UPDATE views SET status='accepted' WHERE id=?", (vid,))
    c.commit()
    assert queue_rows(c) == []


def test_rows_without_a_tradeable_price_are_skipped(tmp_path):
    c = connect(tmp_path / "t.db")
    init_schema(c)
    upsert_markets(c, [mkt(None, None, 0.30)])
    append_odds(c, [mkt(None, None, 0.30)], "2026-08-27T00:00:00")
    pid = create_proposition(c, "Untradeable market")
    map_market(c, 1, pid)
    create_view(c, pid, 0.45, "low")
    assert queue_rows(c) == []


def test_untradeable_rows_are_shown_but_not_acceptable(tmp_path):
    # A card must not print "spread too wide to price" directly above a
    # working Accept button. Keep the row (it is still information -- the
    # history matters) but flag it as not acceptable.
    c = connect(tmp_path / "t.db")
    init_schema(c)
    upsert_markets(c, [mkt(0.006, 0.007, 0.30, untradeable=True)])
    append_odds(c, [mkt(0.006, 0.007, 0.30, untradeable=True)], "2026-08-27T00:00:00")
    pid = create_proposition(c, "Untradeable but shown")
    map_market(c, 1, pid)
    create_view(c, pid, 0.45, "low")

    rows = queue_rows(c)
    assert len(rows) == 1
    assert rows[0]["untradeable"] is True
    assert rows[0]["acceptable"] is False


def test_claim_tier_is_looked_up_not_assumed(tmp_path):
    # The screen must assert a tier it actually looked up, not one it
    # hardcoded. Cite one real claim id from data/sources.json (whatever its
    # true status is) alongside a fabricated one, and prove they diverge.
    tiers = claim_tiers()
    assert tiers, "data/sources.json must have at least one claim for this test to mean anything"
    real_id, real_status = next(iter(tiers.items()))
    fake_id = "definitely-not-a-real-claim-id"
    assert fake_id not in tiers

    c = connect(tmp_path / "t.db")
    init_schema(c)
    upsert_markets(c, [mkt(0.29, 0.31, 0.30)])
    append_odds(c, [mkt(0.29, 0.31, 0.30)], "2026-08-27T00:00:00")
    pid = create_proposition(c, "p")
    map_market(c, 1, pid)
    create_view(c, pid, 0.45, "low", claim_ids=[real_id, fake_id])

    rows = queue_rows(c)
    by_id = {claim["id"]: claim["tier"] for claim in rows[0]["claim_ids"]}
    assert by_id[real_id] == real_status
    assert by_id[fake_id] == "unknown"
