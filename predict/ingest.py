"""Fetch -> disk. Deterministic; no model ever runs in this path."""
from __future__ import annotations

import gzip
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .venues.base import RawMarket


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def upsert_markets(conn: sqlite3.Connection, markets: list[RawMarket]) -> dict:
    ins = upd = 0
    for m in markets:
        cur = conn.execute(
            "UPDATE markets SET question=?, description=?, resolution_rules=?, "
            "end_date=?, last_seen=?, closed=?, resolved=?, resolved_outcome=? "
            "WHERE venue=? AND venue_market_id=?",
            (m.question, m.description, m.resolution_rules, m.end_date, _now(),
             int(m.closed), int(m.resolved), m.resolved_outcome,
             m.venue, m.venue_market_id))
        if cur.rowcount:
            upd += 1
            continue
        conn.execute(
            "INSERT INTO markets (venue, venue_market_id, question, description, "
            "resolution_rules, end_date, first_seen, last_seen, closed, resolved, "
            "resolved_outcome) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (m.venue, m.venue_market_id, m.question, m.description,
             m.resolution_rules, m.end_date, _now(), _now(),
             int(m.closed), int(m.resolved), m.resolved_outcome))
        ins += 1
    conn.commit()
    return {"inserted": ins, "updated": upd}


def append_odds(conn: sqlite3.Connection, markets: list[RawMarket], ts: str) -> int:
    n = 0
    for m in markets:
        row = conn.execute(
            "SELECT id FROM markets WHERE venue=? AND venue_market_id=?",
            (m.venue, m.venue_market_id)).fetchone()
        if row is None:
            continue
        cur = conn.execute(
            "INSERT OR IGNORE INTO odds (market_id, ts, prob_yes, best_bid, "
            "best_ask, liquidity, volume, n_traders, untradeable) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (row["id"], ts, m.prob_yes, m.best_bid, m.best_ask, m.liquidity,
             m.volume, m.n_traders, int(m.untradeable)))
        n += cur.rowcount
    conn.commit()
    return n


def append_jsonl(markets: list[RawMarket], ts: str, odds_dir: Path) -> Path:
    """Raw values to disk BEFORE interpretation.

    No quality gate catches an internally-consistent bad value -- that is
    exactly how a corrupt USDINR daily bar got through elsewhere in this repo.
    Keeping the raw line means a bad gate can be re-run against history rather
    than having silently discarded it.

    Only the identity (venue, venue_market_id) and the raw API payload are
    written -- every normalised field is re-derivable by re-running
    parse_market on raw, so writing both was pure duplication: 19MB/run for
    2,100 markets, ~570MB/month nightly. Gzipped, appending as a new gzip
    member -- gzip.open("at") appends bytes as a separate member, and a
    stream of concatenated members decompresses correctly as one stream.
    """
    odds_dir = Path(odds_dir)
    odds_dir.mkdir(parents=True, exist_ok=True)
    path = odds_dir / f"{ts[:7]}.jsonl.gz"
    with gzip.open(path, "at") as fh:
        for m in markets:
            d = {"ts": ts, "venue": m.venue, "venue_market_id": m.venue_market_id,
                 "raw": m.raw}
            fh.write(json.dumps(d, default=str) + "\n")
    return path


def run(conn: sqlite3.Connection, markets: list[RawMarket], odds_dir: Path,
        ts: str | None = None) -> dict:
    ts = ts or _now()
    append_jsonl(markets, ts, odds_dir)      # disk first, always
    counts = upsert_markets(conn, markets)
    return {"markets": len(markets), "odds_rows": append_odds(conn, markets, ts),
            "ts": ts, **counts}
