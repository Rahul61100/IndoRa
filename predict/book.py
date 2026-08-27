"""Propositions, views, positions.

A VIEW is what we think about a proposition. A POSITION is that view
expressed on one venue at one price. One view can become several positions
across venues at different prices -- and they will score differently, which
is itself the cross-venue signal.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

REJECT_REASONS = {"market is right", "claim too weak", "horizon too long",
                  "illiquid", "don't understand it", "other"}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def edge(our_prob: float, bid: float, ask: float, direction: str) -> float:
    """Edge against the price actually crossed, never the mid.

    A mid you could never trade produces a track record you could never have
    earned -- the same error as quoting Indian equity returns in rupees.
    """
    if direction == "yes":
        return our_prob - ask
    if direction == "no":
        return bid - our_prob
    raise ValueError(f"direction must be 'yes' or 'no', got {direction!r}")


def create_proposition(conn, statement: str, topic: str = "",
                       resolves_by: str | None = None,
                       resolution_criteria: str = "") -> int:
    cur = conn.execute(
        "INSERT INTO propositions (statement, topic, resolves_by, resolution_criteria) "
        "VALUES (?,?,?,?)", (statement, topic, resolves_by, resolution_criteria))
    conn.commit()
    return cur.lastrowid


def map_market(conn, market_id: int, proposition_id: int) -> None:
    """Link a venue market to a proposition. Human-confirmed by design --
    venues publish differing resolution rules, and an unverified mapping
    produces a bet on a technicality nobody read."""
    conn.execute("UPDATE markets SET proposition_id=? WHERE id=?",
                 (proposition_id, market_id))
    conn.commit()


def create_view(conn, proposition_id: int, our_prob: float, confidence: str,
                rationale: str = "", claim_ids=(), proposed_by: str = "human") -> int:
    cur = conn.execute(
        "INSERT INTO views (proposition_id, our_prob, confidence, rationale, "
        "claim_ids, proposed_by, status, created_at) VALUES (?,?,?,?,?,?, 'proposed', ?)",
        (proposition_id, our_prob, confidence, rationale,
         ",".join(claim_ids), proposed_by, _now()))
    conn.commit()
    return cur.lastrowid


def accept_view(conn, view_id: int, market_id: int, direction: str,
                stake_units: int = 1, expected_odds_ts: str | None = None) -> int:
    v = conn.execute("SELECT * FROM views WHERE id=?", (view_id,)).fetchone()
    if v is None:
        raise ValueError(f"no view {view_id}")
    m = conn.execute("SELECT * FROM markets WHERE id=?", (market_id,)).fetchone()
    if m is None:
        raise ValueError(f"no market {market_id}")
    if m["proposition_id"] != v["proposition_id"]:
        raise ValueError("market is not mapped to this view's proposition")

    o = conn.execute("SELECT * FROM odds WHERE market_id=? ORDER BY ts DESC LIMIT 1",
                     (market_id,)).fetchone()
    if o is None:
        raise ValueError("no odds recorded for this market")
    if o["best_bid"] is None or o["best_ask"] is None:
        # Refuse rather than fall back to an older row that happens to have
        # prices -- a position's entry price must be the price actually
        # available at accept time, not a stale one.
        raise ValueError("no tradeable price for this market's latest odds")
    if o["untradeable"]:
        # A spread this wide (>25%) is not a price you could actually cross.
        # Refuse the entry rather than printing a position at a quote the
        # engine itself flagged as not tradeable.
        raise ValueError("this market's latest odds are not tradeable (spread too wide)")
    if expected_odds_ts is not None and expected_odds_ts != o["ts"]:
        # An ingest landed between page render and button click. The
        # reviewer approved the price they SAW, not whatever is now latest.
        raise ValueError("odds moved since this was rendered -- refresh and re-review")

    e = edge(v["our_prob"], o["best_bid"], o["best_ask"], direction)
    cur = conn.execute(
        "INSERT INTO positions (view_id, market_id, direction, entered_at, "
        "market_prob_at_entry, bid_at_entry, ask_at_entry, liquidity_at_entry, "
        "edge, stake_units) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (view_id, market_id, direction, _now(), o["prob_yes"], o["best_bid"],
         o["best_ask"], o["liquidity"], e, stake_units))
    conn.execute("UPDATE views SET status='accepted', reviewed_at=? WHERE id=?",
                 (_now(), view_id))
    conn.commit()
    return cur.lastrowid


def reject_view(conn, view_id: int, reason: str, note: str = "") -> None:
    """Categorical reasons only -- free text cannot be aggregated, and the
    point of recording rejections is to measure the reviewer."""
    if reason not in REJECT_REASONS:
        raise ValueError(f"reason must be one of {sorted(REJECT_REASONS)}")
    conn.execute("UPDATE views SET status='rejected', review_reason=?, "
                 "review_note=?, reviewed_at=? WHERE id=?",
                 (reason, note, _now(), view_id))
    conn.commit()
