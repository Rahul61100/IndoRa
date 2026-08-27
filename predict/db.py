"""Schema and connections. Nothing in this file knows about venues or HTTP."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from . import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS propositions (
    id                  INTEGER PRIMARY KEY,
    statement           TEXT NOT NULL,
    topic               TEXT NOT NULL DEFAULT '',
    resolves_by         TEXT,
    resolution_criteria TEXT NOT NULL DEFAULT '',
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    status              TEXT NOT NULL DEFAULT 'open',
    outcome             TEXT,
    resolved_at         TEXT
);

CREATE TABLE IF NOT EXISTS markets (
    id                INTEGER PRIMARY KEY,
    venue             TEXT NOT NULL,
    venue_market_id   TEXT NOT NULL,
    proposition_id    INTEGER REFERENCES propositions(id),
    question          TEXT NOT NULL,
    description       TEXT NOT NULL DEFAULT '',
    resolution_rules  TEXT NOT NULL DEFAULT '',
    end_date          TEXT,
    first_seen        TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen         TEXT NOT NULL DEFAULT (datetime('now')),
    closed            INTEGER NOT NULL DEFAULT 0,
    resolved          INTEGER NOT NULL DEFAULT 0,
    resolved_outcome  TEXT,
    UNIQUE (venue, venue_market_id)
);

CREATE TABLE IF NOT EXISTS odds (
    market_id  INTEGER NOT NULL REFERENCES markets(id),
    ts         TEXT NOT NULL,
    prob_yes   REAL,
    best_bid   REAL,
    best_ask   REAL,
    liquidity  REAL,
    volume     REAL,
    n_traders  INTEGER,
    untradeable INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (market_id, ts)
);

CREATE TABLE IF NOT EXISTS views (
    id             INTEGER PRIMARY KEY,
    proposition_id INTEGER NOT NULL REFERENCES propositions(id),
    created_at     TEXT NOT NULL DEFAULT (datetime('now')),
    our_prob       REAL NOT NULL,
    confidence     TEXT NOT NULL,
    rationale      TEXT NOT NULL DEFAULT '',
    claim_ids      TEXT NOT NULL DEFAULT '',
    proposed_by    TEXT NOT NULL DEFAULT 'human',
    status         TEXT NOT NULL DEFAULT 'proposed',
    reviewed_at    TEXT,
    review_reason  TEXT,
    review_note    TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id                   INTEGER PRIMARY KEY,
    view_id              INTEGER NOT NULL REFERENCES views(id),
    market_id            INTEGER NOT NULL REFERENCES markets(id),
    direction            TEXT NOT NULL,
    entered_at           TEXT NOT NULL DEFAULT (datetime('now')),
    market_prob_at_entry REAL,
    bid_at_entry         REAL,
    ask_at_entry         REAL,
    liquidity_at_entry   REAL,
    edge                 REAL,
    stake_units          INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS resolutions (
    position_id  INTEGER PRIMARY KEY REFERENCES positions(id),
    resolved_at  TEXT,
    outcome      TEXT,
    brier        REAL,
    market_brier REAL,
    beat_market  INTEGER,
    pnl_paper    REAL,
    scored       INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_odds_market_ts ON odds(market_id, ts DESC);
CREATE INDEX IF NOT EXISTS idx_markets_prop   ON markets(proposition_id);
CREATE INDEX IF NOT EXISTS idx_views_status   ON views(status);
"""


def connect(path: Path | None = None) -> sqlite3.Connection:
    p = Path(path) if path else DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    # SQLite defaults FK enforcement OFF. Without this a view can reference a
    # proposition that does not exist and nothing complains until it is read.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()
