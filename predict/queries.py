"""Read helpers over the collected data. No writes here.

The web review UI was removed on 2026-08-29; this module survives it
because claim_tiers() and drift() are collection-layer facts, and
queue_rows() is the shape any future report or CLI would want.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from . import ROOT
from .book import edge


def drift(entry_prob: float | None, live_prob: float | None) -> float | None:
    if entry_prob is None or live_prob is None:
        return None
    return live_prob - entry_prob


def claim_tiers(root: Path | None = None) -> dict[str, str]:
    """Claim id -> status, read from data/sources.json.

    The review screen must show a confidence tier it actually looked up --
    not one it assumed. Missing file is not an error here: a fresh checkout
    with no sources.json yet should render 'unknown' chips, not crash.
    """
    path = (root if root is not None else ROOT) / "data" / "sources.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return {c["id"]: c["status"] for c in data.get("claims", [])}


def gate_line(conn: sqlite3.Connection) -> str:
    """The honest headline, permanently in the header.

    Until enough calls have RESOLVED, this system measures nothing -- and the
    surest way to forget that is to leave it off the screen.
    """
    resolved = conn.execute(
        "SELECT COUNT(*) FROM resolutions WHERE scored = 1").fetchone()[0]
    open_pos = conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
    if resolved < 50:
        return (f"Calibration gate: {resolved} resolved, 50 needed for a directional "
                f"read (200 for a confident one). {open_pos} open. "
                f"Until then this measures nothing.")
    return f"{resolved} resolved, {open_pos} open."


def queue_rows(conn: sqlite3.Connection) -> list[dict]:
    """Views awaiting review, with the LATEST odds and the move since the
    view was formed. Drift is computed at render, never stored -- a price
    from four hours ago is not the price you would get."""
    rows = conn.execute("""
        SELECT v.id AS view_id, v.our_prob, v.confidence, v.rationale,
               v.claim_ids, v.created_at,
               p.id AS proposition_id, p.statement, p.topic, p.resolves_by,
               m.id AS market_id, m.venue, m.question
        FROM views v
        JOIN propositions p ON p.id = v.proposition_id
        JOIN markets m      ON m.proposition_id = p.id
        WHERE v.status = 'proposed'
        ORDER BY v.created_at DESC
    """).fetchall()

    tiers = claim_tiers()
    out = []
    for r in rows:
        o = conn.execute(
            "SELECT * FROM odds WHERE market_id=? ORDER BY ts DESC LIMIT 1",
            (r["market_id"],)).fetchone()
        first = conn.execute(
            "SELECT prob_yes FROM odds WHERE market_id=? AND ts <= ? "
            "ORDER BY ts DESC LIMIT 1", (r["market_id"], r["created_at"])).fetchone()
        if o is None:
            continue
        # 224 of 2,100 real markets (10.7%) have a NULL best_bid or best_ask.
        # A view with no tradeable price cannot be acted on -- accept_view
        # already refuses it -- so it does not belong in a review queue.
        if o["best_bid"] is None or o["best_ask"] is None:
            continue
        ids = [c for c in (r["claim_ids"] or "").split(",") if c]
        untradeable = bool(o["untradeable"])
        d = dict(r)
        d.update(
            best_bid=o["best_bid"], best_ask=o["best_ask"],
            prob_yes=o["prob_yes"], liquidity=o["liquidity"],
            odds_ts=o["ts"],
            untradeable=untradeable,
            # A spread >25% is not one accept_view will let through -- keep
            # the row visible (it is still information) but tell the
            # template not to offer an Accept it will only bounce.
            acceptable=not untradeable,
            claim_ids=[{"id": cid, "tier": tiers.get(cid, "unknown")} for cid in ids],
            edge_yes=edge(r["our_prob"], o["best_bid"], o["best_ask"], "yes"),
            edge_no=edge(r["our_prob"], o["best_bid"], o["best_ask"], "no"),
            drift=drift(first["prob_yes"] if first else None, o["prob_yes"]),
        )
        out.append(d)
    return out
