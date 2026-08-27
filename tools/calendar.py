# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
The catalyst calendar — Phase A4 of BUILD.md.

    uv run tools/calendar.py              # what is coming, and what it changes
    uv run tools/calendar.py --horizon 90

The user's instruction that produced this: "think about news, mogels, people at the top,
politicians... where are they positioned". A calendar is how that stops being a thing I
remember in a good session and becomes a thing the system checks in every session.

Two rules enforced here, both of which caught a real error on the first run:

1. **Every event needs a `so_what` naming what it changes in the book.** An event with no
   so_what is news, not a catalyst.
2. **A past date is a bug, not an entry.** The first version of data/calendar.json dated
   the STT hike Feb 2026 as an upcoming friction change. It is 207 days in the past and
   already in force, which means every hedge cost quoted in this workspace is already the
   post-hike cost. Prose never catches that. Arithmetic does, immediately.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizon", type=int, default=180)
    args = ap.parse_args()

    d = json.loads((ROOT / "data" / "calendar.json").read_text())
    today = date.today()
    theses = json.loads((ROOT / "positions" / "theses.json").read_text())
    open_syms = {t["symbol"] for t in theses["theses"]}

    past, upcoming = [], []
    for e in d["events"]:
        days = (date.fromisoformat(e["date"]) - today).days
        (past if days < 0 else upcoming).append((days, e))

    if past:
        print("!! STALE ENTRIES — a past date in a forward calendar is a bug, not an entry:")
        for days, e in sorted(past, key=lambda x: x[0]):
            print(f"   T{days:+d}  {e['date']}  {e['title']}")
            print(f"        This has ALREADY HAPPENED. Anything in the book still treating it")
            print(f"        as forward-looking is wrong today.")
        print()

    print("=" * 78)
    print(f"CATALYST CALENDAR — next {args.horizon} days from {today}")
    print("=" * 78)

    for days, e in sorted(upcoming, key=lambda x: x[0]):
        if days > args.horizon:
            continue
        hit = [a for a in e.get("affects", []) if a in open_syms]
        mark = "  <-- LIVE POSITION" if hit else ""
        print(f"\nT+{days:<4d} {e['date']}  [{e['type']}] {e['title']}{mark}")
        print(f"       {e['so_what']}")
        if hit:
            print(f"       positions: {', '.join(hit)}")

    print("\n" + "=" * 78)
    print(f"UNDATED WATCH ({len(d['watching_undated'])}) — no date means no trigger, which is")
    print("exactly why these are the dangerous ones:")
    for w in d["watching_undated"]:
        print(f"\n  [{w['type']}] {w['title']}")
        print(f"       {w['so_what']}")

    nxt = min(upcoming, key=lambda x: x[0], default=None)
    if nxt:
        print("\n" + "=" * 78)
        print(f"NEXT: {nxt[1]['title']} in {nxt[0]} days")


if __name__ == "__main__":
    main()
