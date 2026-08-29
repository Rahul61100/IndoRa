# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""What moved in the prediction-market book between two snapshots.

    uv run scripts/odds_moves.py
    uv run scripts/odds_moves.py --min-liquidity 100000 --top 25

The odds log only becomes useful once it has more than one point in it. This is
the first thing that reads it as a SERIES rather than a snapshot.

Why this exists as its own script: a market that reprices sharply on a topic this
workspace has a sourced view on is Alert B from the spec -- the market telling us
we are missing something. That is a research-agenda generator, and it is worth
more than the opportunity alert, because the process cannot find its own blind
spots by looking harder at what it already tracks.
"""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "predict.db"

# Topics this workspace holds sourced claims on. A big move inside one of these
# is a research prompt; a big move outside them is noise we have no view on.
WATCHED = {
    "iran": ["iran", "hormuz", "strait"],
    "russia": ["russia", "putin", "ukraine", "sanction"],
    "fed/rates": ["fed ", "fomc", "interest rate", "rate hike", "rate cut", "inflation", "cpi"],
    "china": ["china", "taiwan", "rare earth", "xi jinping"],
    "oil": ["oil", "crude", "brent", "opec", "gasoline"],
    "india": ["india", "modi", "rupee", "rbi"],
}
# india->indiana and rbi->runs-batted-in have both bitten this workspace already.
NEGATIVE = ["indiana", "indianapolis", "rbis", "mlb", "nba", "nfl", "wnba",
            "premier league", "ballon", "esports"]


def topic_of(q: str) -> str | None:
    low = q.lower()
    if any(n in low for n in NEGATIVE):
        return None
    for t, keys in WATCHED.items():
        if any(k in low for k in keys):
            return t
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-liquidity", type=float, default=50_000)
    ap.add_argument("--min-move", type=float, default=0.02)
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    if not DB.exists():
        print("no data/predict.db -- run scripts/predict_ingest.py first")
        return
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    snaps = [r[0] for r in conn.execute("SELECT DISTINCT ts FROM odds ORDER BY ts")]
    if len(snaps) < 2:
        print(f"only {len(snaps)} snapshot(s) in the odds log -- nothing to compare yet.")
        print("Run scripts/predict_ingest.py again tomorrow; two points make a series.")
        return

    prev, curr = snaps[-2], snaps[-1]
    print(f"ODDS MOVES  {prev}  ->  {curr}")
    print("=" * 92)

    rows = conn.execute("""
        SELECT m.question, m.end_date,
               a.prob_yes AS p0, b.prob_yes AS p1,
               b.liquidity AS liq, b.untradeable AS ut
        FROM odds a
        JOIN odds b ON b.market_id = a.market_id
        JOIN markets m ON m.id = a.market_id
        WHERE a.ts = ? AND b.ts = ?
          AND a.prob_yes IS NOT NULL AND b.prob_yes IS NOT NULL
          AND b.liquidity >= ?
    """, (prev, curr, args.min_liquidity)).fetchall()

    moves = []
    for r in rows:
        d = r["p1"] - r["p0"]
        if abs(d) >= args.min_move:
            moves.append((abs(d), d, r, topic_of(r["question"] or "")))
    moves.sort(reverse=True, key=lambda x: x[0])

    watched = [m for m in moves if m[3]]
    print(f"\n{len(rows)} liquid markets compared · {len(moves)} moved >= "
          f"{args.min_move*100:.0f}pts · {len(watched)} of those on a WATCHED topic\n")

    if watched:
        print("ON A TOPIC WE HOLD A VIEW ON  — a sharp move here with no claim explaining it")
        print("is a research gap, not an opportunity:\n")
        for _, d, r, t in watched[: args.top]:
            print(f"  {d*100:+6.1f}pts  {r['p0']:.3f}->{r['p1']:.3f}  [{t:<10}] "
                  f"${r['liq']:>9,.0f}  {(r['question'] or '')[:52]}")
    else:
        print("Nothing on a watched topic moved materially. That is a real answer.")

    other = [m for m in moves if not m[3]]
    if other:
        print(f"\nLARGEST MOVES ELSEWHERE (no view held — context only):\n")
        for _, d, r, _ in other[:8]:
            print(f"  {d*100:+6.1f}pts  {r['p0']:.3f}->{r['p1']:.3f}  "
                  f"${r['liq']:>9,.0f}  {(r['question'] or '')[:52]}")

    print("\n" + "=" * 92)
    print(f"snapshots in log: {len(snaps)}  ({snaps[0]} .. {snaps[-1]})")


if __name__ == "__main__":
    main()
