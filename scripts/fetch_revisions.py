# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas", "numpy"]
# ///
"""
Analyst estimate revisions — the gap that cost the Infosys call.

    uv run scripts/fetch_revisions.py [--universe india] [--top 20]

Revision DIRECTION has done more explanatory work in this loop than any valuation
metric. India's FY27 consensus was cut ~9% over twelve months while the index was
called cheap; US CY2026 estimates were revised UP 14.9% over six months. Neither was
visible in a price series, and neither was being collected.

Yahoo exposes two things per ticker that together give the picture:
  eps_trend      the consensus EPS now vs 7/30/60/90 days ago -> revision magnitude
  eps_revisions  count of analysts revising up vs down        -> revision breadth

Writes an append-only ledger to data/revisions/<universe>.json so history accumulates.
Yahoo only ever serves the current snapshot, so **this must run regularly** or the
history simply does not exist.
"""
from __future__ import annotations

import argparse
import json
import warnings
from datetime import date
from pathlib import Path

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "revisions"


def _get(df: pd.DataFrame, row: str, col: str):
    """Yahoo's casing is inconsistent (upLast7days vs downLast7Days). Match loosely."""
    if df is None or not hasattr(df, "index") or row not in df.index:
        return None
    for c in df.columns:
        if c.lower() == col.lower():
            v = df.loc[row, c]
            return None if pd.isna(v) else float(v)
    return None


def pull_one(sym: str) -> dict | None:
    t = yf.Ticker(sym)
    try:
        trend = t.eps_trend
        revs = t.eps_revisions
    except Exception:
        return None
    if trend is None or not hasattr(trend, "index"):
        return None

    rec: dict = {"symbol": sym}
    for period, label in (("0y", "fy0"), ("+1y", "fy1")):
        cur = _get(trend, period, "current")
        if cur is None or cur == 0:
            continue
        for days in (7, 30, 60, 90):
            past = _get(trend, period, f"{days}daysAgo")
            rec[f"{label}_chg_{days}d_pct"] = (
                round((cur / past - 1) * 100, 2) if past else None
            )
        rec[f"{label}_eps"] = round(cur, 2)
        up = _get(revs, period, "upLast30days")
        dn = _get(revs, period, "downLast30days")
        rec[f"{label}_up30"] = int(up) if up is not None else None
        rec[f"{label}_down30"] = int(dn) if dn is not None else None
        if up is not None and dn is not None and (up + dn) > 0:
            # Diffusion: +1 all upgrades, -1 all downgrades, 0 balanced.
            rec[f"{label}_diffusion"] = round((up - dn) / (up + dn), 2)
    try:
        pt = t.analyst_price_targets or {}
        rec["price"] = pt.get("current")
        rec["target_mean"] = pt.get("mean")
        if pt.get("current") and pt.get("mean"):
            rec["target_upside_pct"] = round((pt["mean"] / pt["current"] - 1) * 100, 1)
    except Exception:
        pass
    return rec if len(rec) > 1 else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", default="india")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    uni = json.loads((ROOT / "universe" / f"{args.universe}.json").read_text())
    syms = [s for g in uni.values() for s in g
            if not s.startswith("^") and "=" not in s and not s.startswith("_")]

    rows, failed = [], []
    for s in syms:
        r = pull_one(s)
        (rows if r else failed).append(r if r else s)

    stamp = f"{date.today():%Y-%m-%d}"
    OUT.mkdir(parents=True, exist_ok=True)
    ledger = OUT / f"{args.universe}.json"
    hist = json.loads(ledger.read_text()) if ledger.exists() else {}
    hist[stamp] = rows
    ledger.write_text(json.dumps(hist, indent=1))

    print(f"revisions: {len(rows)}/{len(syms)} pulled, {len(failed)} without estimates")
    if failed:
        print("  no estimate data:", ", ".join(failed[:12]) + ("..." if len(failed) > 12 else ""))
    print(f"  ledger now holds {len(hist)} dated snapshot(s)")

    have = [r for r in rows if r.get("fy1_diffusion") is not None]
    if not have:
        return
    have.sort(key=lambda r: (r["fy1_diffusion"], r.get("fy1_chg_90d_pct") or 0))

    def show(title, sel):
        print(f"\n{title}")
        print(f"  {'symbol':<15}{'FY+1 EPS':>10}{'90d%':>8}{'60d%':>8}{'30d%':>8}"
              f"{'up':>5}{'dn':>5}{'diff':>7}{'tgt up%':>9}")
        for r in sel:
            f = lambda k: (f"{r[k]:>8.2f}" if r.get(k) is not None else f"{'—':>8}")
            print(f"  {r['symbol']:<15}{r.get('fy1_eps', 0):>10.1f}{f('fy1_chg_90d_pct')}"
                  f"{f('fy1_chg_60d_pct')}{f('fy1_chg_30d_pct')}"
                  f"{r.get('fy1_up30', 0):>5}{r.get('fy1_down30', 0):>5}"
                  f"{r['fy1_diffusion']:>7.2f}"
                  f"{(r.get('target_upside_pct') or float('nan')):>9.1f}")

    show(f"WORST revision breadth — next fiscal year (bottom {args.top})", have[:args.top])
    show(f"BEST revision breadth — next fiscal year (top {args.top})", have[-args.top:][::-1])

    ups = sum(1 for r in have if r["fy1_diffusion"] > 0)
    print(f"\n  Universe diffusion: {ups}/{len(have)} names with net UPGRADES "
          f"({ups/len(have)*100:.0f}%). Below ~40% is a market being marked down.")


if __name__ == "__main__":
    main()
