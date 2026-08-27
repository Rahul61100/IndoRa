from fastapi.testclient import TestClient

from predict.app import create_app
from predict.book import create_proposition, create_view, map_market
from predict.db import connect, init_schema
from predict.ingest import append_odds, upsert_markets
from predict.venues.base import RawMarket


def seeded(tmp_path):
    p = tmp_path / "t.db"
    c = connect(p)
    init_schema(c)
    m = RawMarket(venue="polymarket", venue_market_id="1", question="Fed raises?",
                  prob_yes=0.30, best_bid=0.29, best_ask=0.31, liquidity=368000.0)
    upsert_markets(c, [m])
    append_odds(c, [m], "2026-08-27T00:00:00")
    pid = create_proposition(c, "Fed raises in September", topic="fed")
    map_market(c, 1, pid)
    create_view(c, pid, 0.45, "medium", "three dissents", ["fed-may-hike-next"])
    c.close()
    return p


def test_queue_page_renders_the_view(tmp_path):
    client = TestClient(create_app(seeded(tmp_path)))
    r = client.get("/")
    assert r.status_code == 200
    assert "Fed raises in September" in r.text


def test_queue_page_shows_claim_provenance(tmp_path):
    # A review screen that hides claim tiers is a confidence-laundering
    # machine with better CSS. The claim id must be on the page, and its
    # tier must be looked up -- "fed-may-hike-next" is not in the real
    # data/sources.json, so it must render as "unknown", never "reported".
    client = TestClient(create_app(seeded(tmp_path)))
    text = client.get("/").text
    assert "fed-may-hike-next" in text
    # Assert the rendered CHIP, not the document -- the stylesheet in this
    # page legitimately names every tier, so a bare substring check would
    # pass on CSS and prove nothing about what was rendered.
    assert '<span class="chip chip--unknown">fed-may-hike-next' in text
    assert '<span class="chip chip--reported">fed-may-hike-next' not in text


def test_accept_creates_a_position_and_clears_the_queue(tmp_path):
    db_path = seeded(tmp_path)
    client = TestClient(create_app(db_path))
    r = client.post("/views/1/accept", data={"market_id": "1", "direction": "yes"})
    assert r.status_code == 200
    assert "Fed raises in September" not in client.get("/").text
    # The queue clears on the status flip alone -- it would also empty if
    # the position INSERT silently vanished. Prove the position was
    # actually written, not just that the view left 'proposed' status.
    c = connect(db_path)
    assert c.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 1
    c.close()


def test_reject_requires_a_known_reason(tmp_path):
    client = TestClient(create_app(seeded(tmp_path)))
    assert client.post("/views/1/reject", data={"reason": "nonsense"}).status_code == 400
