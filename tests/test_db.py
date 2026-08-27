import sqlite3
from predict.db import connect, init_schema

TABLES = {"propositions", "markets", "odds", "views", "positions", "resolutions"}


def test_init_schema_creates_all_tables(tmp_path):
    conn = connect(tmp_path / "t.db")
    init_schema(conn)
    got = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    assert TABLES <= got


def test_init_schema_is_idempotent(tmp_path):
    conn = connect(tmp_path / "t.db")
    init_schema(conn)
    init_schema(conn)          # must not raise
    assert conn.execute("SELECT COUNT(*) FROM markets").fetchone()[0] == 0


def test_market_is_unique_per_venue(tmp_path):
    conn = connect(tmp_path / "t.db")
    init_schema(conn)
    conn.execute("INSERT INTO markets (venue, venue_market_id, question) "
                 "VALUES ('polymarket', 'abc', 'q')")
    conn.commit()
    try:
        conn.execute("INSERT INTO markets (venue, venue_market_id, question) "
                     "VALUES ('polymarket', 'abc', 'dup')")
        conn.commit()
        raised = False
    except sqlite3.IntegrityError:
        raised = True
    assert raised, "same venue+id must be rejected; upsert relies on this"


def test_foreign_keys_are_enforced(tmp_path):
    conn = connect(tmp_path / "t.db")
    init_schema(conn)
    try:
        conn.execute("INSERT INTO views (proposition_id, our_prob, confidence, "
                     "rationale, proposed_by, status, created_at) "
                     "VALUES (999, 0.5, 'low', 'r', 'human', 'proposed', 'now')")
        conn.commit()
        raised = False
    except sqlite3.IntegrityError:
        raised = True
    assert raised, "FK enforcement must be ON, not SQLite's default OFF"
