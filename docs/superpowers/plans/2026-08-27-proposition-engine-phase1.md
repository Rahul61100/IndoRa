# Proposition Engine — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A working end-to-end vertical slice — ingest Polymarket markets, map one to a hand-written proposition, record a view, and review it in a browser with live odds and drift — proving the review workflow is usable before any LLM or multi-venue work.

**Architecture:** A `predict/` Python package (SQLite + FastAPI + Jinja/HTMX) driven by two thin PEP-723 runner scripts, matching how the rest of this repo is invoked. Venue adapters normalise to one `RawMarket` shape so Kalshi and Manifold drop in later without touching ingest, storage, or UI.

**Tech Stack:** Python 3.11+, SQLite (stdlib `sqlite3`), FastAPI, Uvicorn, Jinja2, `requests`, pytest. No build step, no CDN, no ORM.

**Spec:** [`docs/superpowers/specs/2026-08-27-prediction-market-engine-design.md`](../specs/2026-08-27-prediction-market-engine-design.md)

## Global Constraints

- **Python `>=3.11`.** Runner scripts carry PEP-723 headers exactly like `scripts/fx.py`.
- **`data/predict.db` is gitignored** (already added). **`data/odds/YYYY-MM.jsonl` IS committed** — historical odds cannot be re-fetched.
- **Raw values land on disk before interpretation.** JSONL append happens even when quality gates reject a row.
- **Never infer resolution from a market's absence** from the bulk feed. Phase 1 does not resolve at all.
- **Snapshot `bid` and `ask` separately, never a mid.** Entry prices are frozen at accept time.
- **`pytest` MUST be scoped to `tests/`.** `scripts/commodity_proxy_test.py` and `scripts/us_exceptionalism_test.py` are *analysis scripts*, not tests, but match pytest's default `*_test.py` pattern; collecting them makes live network calls. Task 1 pins `testpaths`.
- **Polymarket field traps:** `outcomePrices` is a **JSON string**, not an array. Bulk feed caps at ~2,100 rows (HTTP 422 beyond) and is volume-ordered.
- Run tests with: `uv run --quiet --with pytest --with fastapi --with jinja2 --with requests --with httpx python -m pytest tests/ -v`

## File Structure

| File | Responsibility |
|---|---|
| `predict/__init__.py` | Package marker, `DB_PATH` / `ODDS_DIR` constants |
| `predict/db.py` | Schema DDL, `connect()`, `init_schema()` — nothing else |
| `predict/venues/base.py` | `RawMarket` dataclass — the normalised shape every venue produces |
| `predict/venues/polymarket.py` | `parse_market()` (pure) + `fetch_open()` (network) |
| `predict/ingest.py` | Upsert markets, append odds rows, append JSONL |
| `predict/book.py` | Propositions, mappings, views, positions, `edge()` |
| `predict/queries.py` | Read helpers for the UI, incl. drift computation |
| `predict/app.py` | FastAPI routes |
| `predict/templates/*.html` | Jinja templates |
| `scripts/predict_ingest.py` | PEP-723 runner → `predict.ingest.run()` |
| `scripts/predict_serve.py` | PEP-723 runner → uvicorn |
| `tests/*.py` | pytest, no network (adapter tests use recorded fixtures) |

---

### Task 1: Package skeleton, schema, and pinned test scope

**Files:**
- Create: `predict/__init__.py`, `predict/db.py`, `pytest.ini`, `tests/__init__.py`
- Test: `tests/test_db.py`

**Interfaces:**
- Consumes: nothing
- Produces: `predict.DB_PATH: Path`, `predict.ODDS_DIR: Path`, `predict.db.connect(path: Path | None = None) -> sqlite3.Connection`, `predict.db.init_schema(conn: sqlite3.Connection) -> None`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_db.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --quiet --with pytest python -m pytest tests/test_db.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'predict'`

- [ ] **Step 3: Write minimal implementation**

```python
# predict/__init__.py
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "predict.db"
ODDS_DIR = ROOT / "data" / "odds"
```

```python
# predict/db.py
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
```

```ini
; pytest.ini
[pytest]
; MUST stay scoped. scripts/*_test.py are analysis scripts, not tests --
; collecting them fires live network calls.
testpaths = tests
python_files = test_*.py
```

```python
# tests/__init__.py
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run --quiet --with pytest python -m pytest tests/test_db.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add predict/ tests/ pytest.ini
git commit -m "feat(predict): schema, connection, pinned test scope

FK enforcement is explicitly ON -- SQLite defaults it off, which would let
a view reference a proposition that does not exist and stay silent until read.

pytest.ini pins testpaths to tests/ because scripts/commodity_proxy_test.py
and scripts/us_exceptionalism_test.py match the default *_test.py pattern and
are analysis scripts that hit the network."
```

---

### Task 2: `RawMarket` and Polymarket parsing (pure, no network)

**Files:**
- Create: `predict/venues/__init__.py`, `predict/venues/base.py`, `predict/venues/polymarket.py`
- Create: `tests/fixtures/polymarket_market.json`
- Test: `tests/test_polymarket_parse.py`

**Interfaces:**
- Consumes: nothing
- Produces: `predict.venues.base.RawMarket` (frozen dataclass, fields below), `predict.venues.polymarket.parse_market(raw: dict) -> RawMarket | None`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_polymarket_parse.py
import json
from pathlib import Path

from predict.venues.polymarket import parse_market

FIX = Path(__file__).parent / "fixtures" / "polymarket_market.json"


def raw(**over):
    d = json.loads(FIX.read_text())
    d.update(over)
    return d


def test_outcome_prices_is_a_json_string_not_a_list():
    # The single most likely parsing bug: outcomePrices arrives as
    # '["0.0065", "0.9935"]' -- a STRING. Indexing it yields '['.
    m = parse_market(raw())
    assert m is not None
    assert isinstance(m.prob_yes, float)
    assert abs(m.prob_yes - 0.0065) < 1e-9


def test_bid_ask_are_kept_separate():
    m = parse_market(raw())
    assert m.best_bid == 0.006
    assert m.best_ask == 0.007
    assert m.best_bid < m.best_ask


def test_crossed_book_is_rejected():
    assert parse_market(raw(bestBid=0.9, bestAsk=0.1)) is None


def test_probabilities_must_sum_to_one():
    assert parse_market(raw(outcomePrices='["0.20", "0.20"]')) is None


def test_probabilities_within_tolerance_are_accepted():
    m = parse_market(raw(outcomePrices='["0.30", "0.69"]'))
    assert m is not None and abs(m.prob_yes - 0.30) < 1e-9


def test_wide_spread_is_flagged_untradeable_not_dropped():
    # 25%+ spread: keep the history, never price off it.
    m = parse_market(raw(bestBid=0.10, bestAsk=0.50))
    assert m is not None
    assert m.untradeable is True


def test_missing_price_fields_do_not_crash():
    d = raw()
    for k in ("bestBid", "bestAsk", "outcomePrices"):
        d.pop(k, None)
    m = parse_market(d)
    assert m is None or m.prob_yes is None


def test_malformed_outcome_prices_returns_none():
    assert parse_market(raw(outcomePrices="not json")) is None


def test_identity_and_rules_are_captured():
    m = parse_market(raw())
    assert m.venue == "polymarket"
    assert m.venue_market_id == "2063134"
    assert m.end_date == "2026-06-01"
    assert "raw" not in m.__dataclass_fields__ or isinstance(m.raw, dict)
```

```json
// tests/fixtures/polymarket_market.json
{
  "id": 2063134,
  "question": "Will Adanech Abiebie be the next Prime Minister of Ethiopia?",
  "description": "General elections are scheduled to be held in Ethiopia on June 1, 2026.",
  "outcomes": "[\"Yes\", \"No\"]",
  "outcomePrices": "[\"0.0065\", \"0.9935\"]",
  "bestBid": 0.006,
  "bestAsk": 0.007,
  "lastTradePrice": 0.005,
  "liquidityNum": 20502.15364,
  "volumeNum": 51234.5,
  "endDateIso": "2026-06-01",
  "closed": false,
  "resolutionSource": "",
  "negRisk": true
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --quiet --with pytest python -m pytest tests/test_polymarket_parse.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'predict.venues'`

- [ ] **Step 3: Write minimal implementation**

```python
# predict/venues/__init__.py
```

```python
# predict/venues/base.py
"""The normalised shape every venue adapter produces.

Adding Kalshi or Manifold later means writing one more module that returns
these -- ingest, storage and the UI never learn a venue's field names.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RawMarket:
    venue: str
    venue_market_id: str
    question: str
    description: str = ""
    resolution_rules: str = ""
    end_date: str | None = None
    prob_yes: float | None = None
    best_bid: float | None = None
    best_ask: float | None = None
    liquidity: float = 0.0
    volume: float = 0.0
    n_traders: int | None = None
    closed: bool = False
    resolved: bool = False
    resolved_outcome: str | None = None
    untradeable: bool = False
    raw: dict = field(default_factory=dict, repr=False, compare=False)
```

```python
# predict/venues/polymarket.py
"""Polymarket adapter.

Two traps verified live on 2026-08-27:
  1. `outcomePrices` is a JSON STRING, not an array. Indexing it gives '['.
  2. The bulk feed caps around 2,100 rows (HTTP 422 beyond) and is
     volume-ordered -- so a market can leave the window while still open.
     Never read absence as resolution.
"""
from __future__ import annotations

import json

from .base import RawMarket

VENUE = "polymarket"
PROB_SUM_TOLERANCE = 0.02
WIDE_SPREAD = 0.25


def _f(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def parse_market(raw: dict) -> RawMarket | None:
    """Normalise one Gamma market. Returns None when the row is unusable."""
    mid = raw.get("id")
    if mid is None or not raw.get("question"):
        return None

    prob = None
    prices_field = raw.get("outcomePrices")
    if prices_field is not None:
        try:
            prices = json.loads(prices_field) if isinstance(prices_field, str) else prices_field
            vals = [float(p) for p in prices]
        except (json.JSONDecodeError, TypeError, ValueError):
            return None
        if len(vals) == 2 and abs(sum(vals) - 1.0) > PROB_SUM_TOLERANCE:
            return None            # the two legs disagree: the row is wrong
        prob = vals[0] if vals else None

    bid, ask = _f(raw.get("bestBid")), _f(raw.get("bestAsk"))
    if bid is not None and ask is not None and bid > ask:
        return None                # crossed book

    untradeable = False
    if bid is not None and ask is not None:
        mid_px = (bid + ask) / 2
        if mid_px > 0 and (ask - bid) / mid_px > WIDE_SPREAD:
            untradeable = True     # keep the history, do not price off it

    return RawMarket(
        venue=VENUE,
        venue_market_id=str(mid),
        question=raw.get("question") or "",
        description=raw.get("description") or "",
        resolution_rules=raw.get("resolutionSource") or "",
        end_date=(raw.get("endDateIso") or None),
        prob_yes=prob,
        best_bid=bid,
        best_ask=ask,
        liquidity=_f(raw.get("liquidityNum")) or 0.0,
        volume=_f(raw.get("volumeNum")) or 0.0,
        n_traders=None,
        closed=bool(raw.get("closed")),
        resolved=bool(raw.get("resolved")),
        resolved_outcome=raw.get("resolvedOutcome"),
        untradeable=untradeable,
        raw=raw,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run --quiet --with pytest python -m pytest tests/test_polymarket_parse.py -v`
Expected: 9 passed

- [ ] **Step 5: Commit**

```bash
git add predict/venues/ tests/test_polymarket_parse.py tests/fixtures/
git commit -m "feat(predict): RawMarket shape and Polymarket parsing

outcomePrices is a JSON string, not an array -- indexing it yields '['.
Verified live 2026-08-27 and covered by a test that fails loudly if the
venue changes shape.

A wide spread flags untradeable rather than dropping the row: we still
want the odds history, we just must not price a call off it."
```

---

### Task 3: Polymarket fetch (network, paginated)

**Files:**
- Modify: `predict/venues/polymarket.py`
- Test: `tests/test_polymarket_fetch.py`

**Interfaces:**
- Consumes: `parse_market`, `RawMarket`
- Produces: `predict.venues.polymarket.fetch_open(session=None, max_pages: int = 21, page_size: int = 100, sleep_s: float = 0.25) -> list[RawMarket]`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_polymarket_fetch.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --quiet --with pytest --with requests python -m pytest tests/test_polymarket_fetch.py -v`
Expected: FAIL — `ImportError: cannot import name 'fetch_open'`

- [ ] **Step 3: Write minimal implementation**

Append to `predict/venues/polymarket.py`:

```python
import time

import requests

GAMMA = "https://gamma-api.polymarket.com/markets"
UA = {"User-Agent": "market-intel/1.0 (research)"}


def fetch_open(session=None, max_pages: int = 21, page_size: int = 100,
               sleep_s: float = 0.25) -> list[RawMarket]:
    """Page the open+active feed, newest-volume first.

    Stops on a short page or a non-200. A 422 is the documented end of the
    window (~2,100 rows) -- it means "no more rows here", never "those
    markets resolved".
    """
    s = session or requests.Session()
    if session is None:
        s.headers.update(UA)
    out, offset = [], 0
    for _ in range(max_pages):
        r = s.get(GAMMA, params={"limit": page_size, "offset": offset,
                                 "closed": "false", "active": "true",
                                 "order": "volumeNum", "ascending": "false"},
                  timeout=40)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        for row in batch:
            m = parse_market(row)
            if m is not None:
                out.append(m)
        offset += page_size
        if len(batch) < page_size:
            break
        if sleep_s:
            time.sleep(sleep_s)
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run --quiet --with pytest --with requests python -m pytest tests/test_polymarket_fetch.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add predict/venues/polymarket.py tests/test_polymarket_fetch.py
git commit -m "feat(predict): paginated Polymarket fetch

A 422 past the window end is a stop signal, not a crash, and never
evidence that the remaining markets resolved. Tests inject a fake session
so no test touches the network."
```

---

### Task 4: Ingest — upsert, odds, JSONL

**Files:**
- Create: `predict/ingest.py`, `scripts/predict_ingest.py`
- Test: `tests/test_ingest.py`

**Interfaces:**
- Consumes: `RawMarket`, `connect`, `init_schema`
- Produces: `predict.ingest.upsert_markets(conn, markets) -> dict`, `predict.ingest.append_odds(conn, markets, ts: str) -> int`, `predict.ingest.append_jsonl(markets, ts: str, odds_dir: Path) -> Path`, `predict.ingest.run(conn, markets, odds_dir: Path, ts: str | None = None) -> dict`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_ingest.py
import json

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
    p = append_jsonl([mk("1"), mk("2")], "2026-08-27T00:00:00", tmp_path)
    lines = p.read_text().strip().split("\n")
    assert len(lines) == 2
    assert json.loads(lines[0])["raw"]["id"] == "1"
    assert p.name == "2026-08.jsonl"


def test_jsonl_appends_across_runs(tmp_path):
    append_jsonl([mk("1")], "2026-08-27T00:00:00", tmp_path)
    p = append_jsonl([mk("2")], "2026-08-28T00:00:00", tmp_path)
    assert len(p.read_text().strip().split("\n")) == 2


def test_run_reports_a_summary(tmp_path):
    c = db(tmp_path)
    s = run(c, [mk("1"), mk("2")], tmp_path, ts="2026-08-27T00:00:00")
    assert s["markets"] == 2 and s["odds_rows"] == 2 and s["inserted"] == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --quiet --with pytest python -m pytest tests/test_ingest.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'predict.ingest'`

- [ ] **Step 3: Write minimal implementation**

```python
# predict/ingest.py
"""Fetch -> disk. Deterministic; no model ever runs in this path."""
from __future__ import annotations

import dataclasses
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
    """
    odds_dir = Path(odds_dir)
    odds_dir.mkdir(parents=True, exist_ok=True)
    path = odds_dir / f"{ts[:7]}.jsonl"
    with path.open("a") as fh:
        for m in markets:
            d = dataclasses.asdict(m)
            d["ts"] = ts
            fh.write(json.dumps(d, default=str) + "\n")
    return path


def run(conn: sqlite3.Connection, markets: list[RawMarket], odds_dir: Path,
        ts: str | None = None) -> dict:
    ts = ts or _now()
    append_jsonl(markets, ts, odds_dir)      # disk first, always
    counts = upsert_markets(conn, markets)
    return {"markets": len(markets), "odds_rows": append_odds(conn, markets, ts),
            "ts": ts, **counts}
```

```python
# scripts/predict_ingest.py
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""Nightly ingest.

    uv run scripts/predict_ingest.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from predict import ODDS_DIR
from predict.db import connect, init_schema
from predict.ingest import run
from predict.venues import polymarket


def main() -> None:
    conn = connect()
    init_schema(conn)
    markets = polymarket.fetch_open()
    print(f"polymarket: {len(markets)} parsed")
    print(run(conn, markets, ODDS_DIR))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run --quiet --with pytest python -m pytest tests/test_ingest.py -v`
Expected: 7 passed

Then run it for real: `uv run scripts/predict_ingest.py`
Expected: roughly 2,000 markets parsed, a summary dict, and `data/odds/2026-08.jsonl` created.

- [ ] **Step 5: Commit**

```bash
git add predict/ingest.py scripts/predict_ingest.py tests/test_ingest.py
git commit -m "feat(predict): ingest with JSONL-before-interpretation

Raw values reach disk before any gate runs. No quality gate catches an
internally-consistent bad value -- that is how a corrupt USDINR daily bar
got through elsewhere in this repo -- so the raw line is the real
protection and a bad gate can be re-run against history.

Upsert preserves first_seen and never clobbers a hand-confirmed
proposition mapping."
```

---

### Task 5: Propositions, mappings, views, positions, and `edge()`

**Files:**
- Create: `predict/book.py`
- Test: `tests/test_book.py`

**Interfaces:**
- Consumes: `connect`, `init_schema`
- Produces: `predict.book.edge(our_prob, bid, ask, direction) -> float`, `create_proposition(conn, statement, topic="", resolves_by=None, resolution_criteria="") -> int`, `map_market(conn, market_id, proposition_id) -> None`, `create_view(conn, proposition_id, our_prob, confidence, rationale="", claim_ids=(), proposed_by="human") -> int`, `accept_view(conn, view_id, market_id, direction, stake_units=1) -> int`, `reject_view(conn, view_id, reason, note="") -> None`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_book.py
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
    assert row["edge"] == pytest.approx(0.14)
    assert c.execute("SELECT status FROM views WHERE id=?", (vid,)).fetchone()[0] == "accepted"


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --quiet --with pytest python -m pytest tests/test_book.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'predict.book'`

- [ ] **Step 3: Write minimal implementation**

```python
# predict/book.py
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
                stake_units: int = 1) -> int:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run --quiet --with pytest python -m pytest tests/test_book.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add predict/book.py tests/test_book.py
git commit -m "feat(predict): views, positions, and spread-crossing edge

edge() uses the ask for YES and the bid for NO, never the mid. A mid you
could never trade produces a track record you could never have earned.

Accepting a view snapshots bid, ask and liquidity at accept time, and
refuses a market that is not mapped to the view's proposition. Rejections
take a categorical reason because the point of recording them is to
measure the reviewer, and free text cannot be aggregated."
```

---

### Task 6: Queries with drift, and the review-queue UI

**Files:**
- Create: `predict/queries.py`, `predict/app.py`, `predict/templates/base.html`, `predict/templates/queue.html`, `scripts/predict_serve.py`
- Test: `tests/test_queries.py`, `tests/test_app.py`

**Interfaces:**
- Consumes: everything above
- Produces: `predict.queries.queue_rows(conn) -> list[dict]`, `predict.queries.drift(entry_prob, live_prob) -> float | None`, `predict.app.create_app(db_path=None) -> FastAPI`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_queries.py
from predict.book import create_proposition, create_view, map_market
from predict.db import connect, init_schema
from predict.ingest import append_odds, upsert_markets
from predict.queries import drift, queue_rows
from predict.venues.base import RawMarket


def mkt(bid, ask, prob):
    return RawMarket(venue="polymarket", venue_market_id="1", question="Fed raises?",
                     prob_yes=prob, best_bid=bid, best_ask=ask, liquidity=368000.0)


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
    assert r["claim_ids"] == ["fed-may-hike-next"]
    assert round(r["drift"], 3) == 0.010


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
```

```python
# tests/test_app.py
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
    # machine with better CSS. The claim id must be on the page.
    client = TestClient(create_app(seeded(tmp_path)))
    assert "fed-may-hike-next" in client.get("/").text


def test_accept_creates_a_position_and_clears_the_queue(tmp_path):
    client = TestClient(create_app(seeded(tmp_path)))
    r = client.post("/views/1/accept", data={"market_id": "1", "direction": "yes"})
    assert r.status_code == 200
    assert "Fed raises in September" not in client.get("/").text


def test_reject_requires_a_known_reason(tmp_path):
    client = TestClient(create_app(seeded(tmp_path)))
    assert client.post("/views/1/reject", data={"reason": "nonsense"}).status_code == 400
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --quiet --with pytest --with fastapi --with jinja2 --with httpx python -m pytest tests/test_queries.py tests/test_app.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'predict.queries'`

- [ ] **Step 3: Write minimal implementation**

```python
# predict/queries.py
"""Read helpers for the UI. No writes here."""
from __future__ import annotations

import sqlite3

from .book import edge


def drift(entry_prob: float | None, live_prob: float | None) -> float | None:
    if entry_prob is None or live_prob is None:
        return None
    return live_prob - entry_prob


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
        d = dict(r)
        d.update(
            best_bid=o["best_bid"], best_ask=o["best_ask"],
            prob_yes=o["prob_yes"], liquidity=o["liquidity"],
            untradeable=bool(o["untradeable"]),
            claim_ids=[c for c in (r["claim_ids"] or "").split(",") if c],
            edge_yes=edge(r["our_prob"], o["best_bid"], o["best_ask"], "yes"),
            edge_no=edge(r["our_prob"], o["best_bid"], o["best_ask"], "no"),
            drift=drift(first["prob_yes"] if first else None, o["prob_yes"]),
        )
        out.append(d)
    return out
```

```python
# predict/app.py
"""Local review dashboard. Single user, no auth, localhost only."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .book import accept_view, reject_view
from .db import connect, init_schema
from .queries import queue_rows

TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def create_app(db_path=None) -> FastAPI:
    app = FastAPI(title="proposition engine")

    def db():
        c = connect(db_path)
        init_schema(c)
        return c

    @app.get("/", response_class=HTMLResponse)
    def queue(request: Request):
        conn = db()
        try:
            return TEMPLATES.TemplateResponse(
                request, "queue.html", {"rows": queue_rows(conn)})
        finally:
            conn.close()

    @app.post("/views/{view_id}/accept")
    def accept(view_id: int, market_id: int = Form(...), direction: str = Form(...)):
        conn = db()
        try:
            accept_view(conn, view_id, market_id, direction)
        except ValueError as e:
            return HTMLResponse(str(e), status_code=400)
        finally:
            conn.close()
        return RedirectResponse("/", status_code=303)

    @app.post("/views/{view_id}/reject")
    def reject(view_id: int, reason: str = Form(...), note: str = Form("")):
        conn = db()
        try:
            reject_view(conn, view_id, reason, note)
        except ValueError as e:
            return HTMLResponse(str(e), status_code=400)
        finally:
            conn.close()
        return RedirectResponse("/", status_code=303)

    return app
```

```html
<!-- predict/templates/base.html -->
<!doctype html>
<html><head><meta charset="utf-8"><title>proposition engine</title>
<style>
 body{font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;max-width:900px;
      margin:2rem auto;padding:0 1rem;background:#fbfbfa;color:#1a1a1a}
 .card{border:1px solid #ddd;border-radius:6px;padding:1rem;margin:1rem 0;background:#fff}
 .stmt{font-size:16px;font-weight:600;margin-bottom:.5rem}
 .venue{display:flex;gap:1rem;padding:.35rem 0;border-bottom:1px solid #f0f0f0}
 .edge{font-weight:600}.pos{color:#0a7}.neg{color:#c33}
 .claim{font-size:12px;padding:.15rem .4rem;border-radius:3px;margin-right:.4rem}
 .reported{background:#fff4d6;border:1px solid #e8c86a}
 .verified{background:#e3f6e8;border:1px solid #7bc48a}
 .warn{background:#fff0f0;border:1px solid #e5a0a0;padding:.5rem;border-radius:4px;margin:.5rem 0}
 .muted{color:#888;font-size:12px}
 button{font:inherit;padding:.3rem .8rem;margin-right:.4rem;cursor:pointer}
</style></head><body>
<h1>review queue</h1>
{% block content %}{% endblock %}
</body></html>
```

```html
<!-- predict/templates/queue.html -->
{% extends "base.html" %}
{% block content %}
{% if not rows %}<p class="muted">Nothing awaiting review.</p>{% endif %}
{% for r in rows %}
<div class="card">
  <div class="stmt">{{ r.statement }}</div>
  <div class="muted">{{ r.topic }}{% if r.resolves_by %} · resolves by {{ r.resolves_by }}{% endif %}</div>

  <div class="venue">
    <span>{{ r.venue }}</span>
    <span>bid {{ '%.3f'|format(r.best_bid) }} / ask {{ '%.3f'|format(r.best_ask) }}</span>
    <span>${{ '{:,.0f}'.format(r.liquidity) }}</span>
    <span class="edge {{ 'pos' if r.edge_yes > 0 else 'neg' }}">
      YES {{ '%+.1f'|format(r.edge_yes * 100) }}pts</span>
    <span class="edge {{ 'pos' if r.edge_no > 0 else 'neg' }}">
      NO {{ '%+.1f'|format(r.edge_no * 100) }}pts</span>
    {% if r.untradeable %}<span class="neg">UNTRADEABLE (wide spread)</span>{% endif %}
  </div>

  <p>our view <b>{{ '%.2f'|format(r.our_prob) }}</b> · confidence {{ r.confidence }}</p>
  {% if r.rationale %}<p class="muted">{{ r.rationale }}</p>{% endif %}

  <p>{% for c in r.claim_ids %}<span class="claim reported">{{ c }}</span>{% endfor %}
     {% if not r.claim_ids %}<span class="muted">no claims attached</span>{% endif %}</p>

  {% if r.drift is not none and r.drift|abs > 0.005 %}
  <div class="warn">odds moved {{ '%+.3f'|format(r.drift) }} since this view was formed.</div>
  {% endif %}

  <form method="post" action="/views/{{ r.view_id }}/accept" style="display:inline">
    <input type="hidden" name="market_id" value="{{ r.market_id }}">
    <input type="hidden" name="direction" value="yes">
    <button type="submit">accept YES</button>
  </form>
  <form method="post" action="/views/{{ r.view_id }}/reject" style="display:inline">
    <select name="reason">
      <option>market is right</option><option>claim too weak</option>
      <option>horizon too long</option><option>illiquid</option>
      <option>don't understand it</option><option>other</option>
    </select>
    <button type="submit">reject</button>
  </form>
</div>
{% endfor %}
{% endblock %}
```

```python
# scripts/predict_serve.py
# /// script
# requires-python = ">=3.11"
# dependencies = ["fastapi", "uvicorn", "jinja2", "python-multipart"]
# ///
"""Local review dashboard.

    uv run scripts/predict_serve.py     # http://127.0.0.1:8848
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import uvicorn

from predict.app import create_app

if __name__ == "__main__":
    uvicorn.run(create_app(), host="127.0.0.1", port=8848)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run --quiet --with pytest --with fastapi --with jinja2 --with httpx --with python-multipart python -m pytest tests/ -v`
Expected: all tests pass (32 total across the six files)

Then verify end to end:
```bash
uv run scripts/predict_ingest.py
uv run scripts/predict_serve.py     # visit http://127.0.0.1:8848
```

- [ ] **Step 5: Commit**

```bash
git add predict/queries.py predict/app.py predict/templates/ \
        scripts/predict_serve.py tests/test_queries.py tests/test_app.py
git commit -m "feat(predict): review queue with render-time drift

Drift is computed at render and never stored: a price from four hours ago
is not the price you would get, and the card must say so.

Claim ids render as tinted chips so a reported claim looks visibly weaker
than a verified one. This repo was found stamping 85 of 92 notes verified
against a ledger that said otherwise -- a review screen that hides tiers
is that same confidence-laundering machine with better CSS."
```

---

## Manual smoke test (after Task 6)

```bash
uv run scripts/predict_ingest.py
uv run --quiet --with fastapi python - <<'EOF'
import sys; sys.path.insert(0, ".")
from predict.db import connect
from predict.book import create_proposition, map_market, create_view
c = connect()
mid, q = c.execute(
    "SELECT id, question FROM markets WHERE question LIKE '%Fed%' "
    "ORDER BY id LIMIT 1").fetchone()
pid = create_proposition(c, "The Fed raises rates at the September 2026 FOMC",
                         topic="fed", resolves_by="2026-09-17")
map_market(c, mid, pid)
create_view(c, pid, 0.45, "medium",
            "Fed held five meetings with three dissents wanting a hike",
            ["fed-may-hike-next", "rate-cut-cycle-is-over"])
print("mapped:", q)
EOF
uv run scripts/predict_serve.py
```

Expect the card to render with live bid/ask, both edges, two claim chips, and working accept/reject.

## Self-review notes

**Spec coverage (Phase 1 scope only).** §1 venue survey → Task 2/3. §2 data model → Task 1 (all six tables created now, `resolutions` unused until Phase 2). §3 ingestion + traps → Tasks 2–4. §4 proposition mapping → Task 5 (`map_market`, human-only by design). §5 edge and spread-crossing → Task 5. §8 review UI → Task 6.

**Deliberately deferred to Phase 2:** LLM proposal generation (§5), cross-venue disagreement (§6), the two daily alerts (§7), resolver and scorecard (§9), Kalshi and Manifold adapters. The `venue` column and `RawMarket` shape exist now so those land without migration.

**Known deviation from repo convention:** this is a package, not a standalone PEP-723 script, because a web app spans files. The two `scripts/predict_*.py` runners keep the `uv run scripts/...` invocation identical to everything else; both insert the repo root on `sys.path` (verified working).
