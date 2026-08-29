import gzip
import json

import pytest

from predict.db import connect, init_schema
from predict.ingest import append_jsonl, append_odds, run, upsert_markets
from predict.venues.base import RawMarket


def mk(mid="1", **over):
    d = dict(venue="polymarket", venue_market_id=mid, question=f"q{mid}",
             prob_yes=0.30, best_bid=0.29, best_ask=0.31, liquidity=5000.0,
             volume=100.0, raw={"id": mid})
    d.update(over)
    return RawMarket(**d)


def db(tmp_path):
    c = connect(tmp_path / "t.db")
    init_schema(c)
    return c


def test_upsert_inserts_then_updates_without_duplicating(tmp_path):
    c = db(tmp_path)
    assert upsert_markets(c, [mk("1")])["inserted"] == 1
    r = upsert_markets(c, [mk("1", question="renamed")])
    assert r["inserted"] == 0 and r["updated"] == 1
    assert c.execute("SELECT COUNT(*) FROM markets").fetchone()[0] == 1
    assert c.execute("SELECT question FROM markets").fetchone()[0] == "renamed"


def test_upsert_preserves_first_seen_and_proposition_mapping(tmp_path):
    c = db(tmp_path)
    upsert_markets(c, [mk("1")])
    c.execute("INSERT INTO propositions (statement) VALUES ('p')")
    c.execute("UPDATE markets SET proposition_id = 1")
    c.commit()
    first = c.execute("SELECT first_seen FROM markets").fetchone()[0]
    upsert_markets(c, [mk("1", question="again")])
    row = c.execute("SELECT first_seen, proposition_id FROM markets").fetchone()
    assert row[0] == first, "first_seen must survive re-ingest"
    assert row[1] == 1, "a hand-confirmed mapping must never be clobbered"


def test_append_odds_is_idempotent_for_one_timestamp(tmp_path):
    c = db(tmp_path)
    upsert_markets(c, [mk("1")])
    assert append_odds(c, [mk("1")], "2026-08-27T00:00:00") == 1
    append_odds(c, [mk("1")], "2026-08-27T00:00:00")
    assert c.execute("SELECT COUNT(*) FROM odds").fetchone()[0] == 1


def test_untradeable_flag_is_persisted(tmp_path):
    c = db(tmp_path)
    upsert_markets(c, [mk("1", untradeable=True)])
    append_odds(c, [mk("1", untradeable=True)], "2026-08-27T00:00:00")
    assert c.execute("SELECT untradeable FROM odds").fetchone()[0] == 1


def test_jsonl_is_written_before_interpretation(tmp_path):
    # Raw values must reach disk even for rows a gate would reject, so a bad
    # gate can be re-run against history instead of having discarded it.
    # Only identity + raw is written now -- every normalised field is
    # re-derivable from raw via parse_market, so writing both was pure
    # duplication.
    p = append_jsonl([mk("1"), mk("2")], "2026-08-27T00:00:00", tmp_path)
    with gzip.open(p, "rt") as fh:
        lines = fh.read().strip().split("\n")
    assert len(lines) == 2
    row = json.loads(lines[0])
    assert row["raw"]["id"] == "1"
    assert row["venue"] == "polymarket" and row["venue_market_id"] == "1"
    assert row["ts"] == "2026-08-27T00:00:00"
    assert set(row) == {"ts", "venue", "venue_market_id", "raw"}
    assert p.name == "2026-08.jsonl.gz"


def test_jsonl_appends_across_runs(tmp_path):
    # gzip.open("at") appends as a new gzip member -- a stream of
    # concatenated members must still decompress as one stream.
    append_jsonl([mk("1")], "2026-08-27T00:00:00", tmp_path)
    p = append_jsonl([mk("2")], "2026-08-28T00:00:00", tmp_path)
    with gzip.open(p, "rt") as fh:
        lines = fh.read().strip().split("\n")
    assert len(lines) == 2
    assert [json.loads(l)["raw"]["id"] for l in lines] == ["1", "2"]


def test_run_reports_a_summary(tmp_path):
    c = db(tmp_path)
    s = run(c, [mk("1"), mk("2")], tmp_path, ts="2026-08-27T00:00:00")
    assert s["markets"] == 2 and s["odds_rows"] == 2 and s["inserted"] == 2


def test_jsonl_survives_a_database_failure(tmp_path):
    # Tests the actual guarantee -- "raw values reach disk before
    # interpretation" -- rather than the call order. A reorder of
    # append_jsonl/upsert_markets inside run() would not be caught by a
    # test that only checks the order they were invoked in; this one
    # proves the JSONL still holds every row even when the DB write dies.
    class FailingConn:
        def execute(self, *a, **kw):
            raise RuntimeError("db is down")

    with pytest.raises(RuntimeError, match="db is down"):
        run(FailingConn(), [mk("1"), mk("2")], tmp_path, ts="2026-08-27T00:00:00")

    p = tmp_path / "2026-08.jsonl.gz"
    with gzip.open(p, "rt") as fh:
        lines = fh.read().strip().split("\n")
    assert len(lines) == 2
    assert [json.loads(l)["raw"]["id"] for l in lines] == ["1", "2"]
