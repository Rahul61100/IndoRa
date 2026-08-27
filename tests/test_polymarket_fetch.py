import json
from pathlib import Path

from predict.venues.polymarket import fetch_open

FIX = json.loads((Path(__file__).parent / "fixtures" / "polymarket_market.json").read_text())


class FakeResp:
    def __init__(self, status, payload):
        self.status_code, self._p = status, payload

    def json(self):
        return self._p


class FakeSession:
    """Records calls; returns two full pages then a 422, like the real API."""
    def __init__(self, pages):
        self.pages, self.calls = pages, []

    def get(self, url, params=None, timeout=None):
        self.calls.append(params)
        i = len(self.calls) - 1
        return self.pages[i] if i < len(self.pages) else FakeResp(422, [])


def market(i):
    d = dict(FIX)
    d["id"] = 1000 + i
    return d


def test_paginates_until_short_page():
    pages = [FakeResp(200, [market(i) for i in range(100)]),
             FakeResp(200, [market(100 + i) for i in range(30)])]
    s = FakeSession(pages)
    out = fetch_open(session=s, sleep_s=0)
    assert len(out) == 130
    assert s.calls[0]["offset"] == 0
    assert s.calls[1]["offset"] == 100


def test_http_422_stops_cleanly_and_keeps_what_it_has():
    # The real feed 422s past ~2,100 rows. That is a stop signal, not a crash,
    # and absolutely not evidence that the remaining markets closed.
    pages = [FakeResp(200, [market(i) for i in range(100)]), FakeResp(422, [])]
    out = fetch_open(session=FakeSession(pages), sleep_s=0)
    assert len(out) == 100


def test_unparseable_rows_are_skipped_not_fatal():
    good, bad = market(1), market(2)
    bad["outcomePrices"] = "not json"
    out = fetch_open(session=FakeSession([FakeResp(200, [good, bad])]), sleep_s=0)
    assert len(out) == 1


def test_max_pages_is_respected():
    pages = [FakeResp(200, [market(i) for i in range(100)]) for _ in range(5)]
    out = fetch_open(session=FakeSession(pages), max_pages=2, sleep_s=0)
    assert len(out) == 200
