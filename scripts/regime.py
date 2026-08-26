# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas", "numpy"]
# ///
"""
Regime classifier and book stress test.

Two jobs:

1. REGIME — reduce each market to a labelled state from breadth, trend, volatility and
   momentum. The correct strategy is regime-dependent: at India's split breadth an index
   view is worthless, while the US at broadening breadth supports one. Labelling it stops
   that judgement being re-made from scratch and inconsistently every day.

2. STRESS — take the worst historical days for each market over the sample and ask what
   the current book would have done. Not a VaR model; a "this actually happened" test.

    uv run scripts/regime.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
BOOK = ["ICICIBANK.NS", "BHARTIARTL.NS", "HAL.NS", "SBIN.NS", "DIXON.NS",
        "HDFCBANK.NS", "NTPC.NS", "RELIANCE.NS"]


def load_snapshot(market: str) -> dict | None:
    p = ROOT / "data" / "daily" / market / "latest.json"
    return json.loads(p.read_text()) if p.exists() else None


def breadth(snap: dict) -> dict:
    rows = [r for g in snap["groups"].values() for k, r in g.items()
            if not k.startswith("^") and "=" not in k]
    if not rows:
        return {}
    n = len(rows)
    return {
        "n": n,
        "above200": sum(1 for r in rows if (r["vs_sma_pct"]["sma200"] or -1) > 0) / n * 100,
        "above50": sum(1 for r in rows if (r["vs_sma_pct"]["sma50"] or -1) > 0) / n * 100,
        "up": sum(1 for r in rows if r["trend"] == "uptrend"),
        "down": sum(1 for r in rows if r["trend"] == "downtrend"),
        "median_rsi": float(np.median([r["rsi14"] for r in rows])),
        "median_1y": float(np.median([r["returns_pct"]["1y"] for r in rows
                                      if r["returns_pct"]["1y"] is not None])),
    }


def classify(b: dict, bench: dict | None) -> tuple[str, list[str]]:
    """Label the regime. Thresholds are deliberately coarse -- this is a state label,
    not a signal, and false precision would invite over-reading."""
    if not b:
        return "unknown", []
    a200, a50 = b["above200"], b["above50"]
    why = [f"{a200:.0f}% above 200 DMA", f"{a50:.0f}% above 50 DMA",
           f"{b['up']} up / {b['down']} down of {b['n']}"]
    bench_trend = bench["trend"] if bench else "unknown"
    why.append(f"benchmark {bench_trend}")

    if a200 >= 70 and a50 >= 60:
        label = "broad uptrend — index view works, own the market"
    elif a200 >= 60 and a50 >= 45:
        label = "broadening — index view works, leadership rotating"
    elif a200 <= 30:
        label = "broad downtrend — capital preservation, index view works and is negative"
    elif 40 <= a200 <= 65 and abs(b["up"] - b["down"]) <= max(3, 0.1 * b["n"]):
        label = "SPLIT — index view near worthless, selection market"
    elif a200 < 45:
        label = "deteriorating — narrowing leadership"
    else:
        label = "mixed"
    return label, why


def main() -> None:
    print("=" * 80)
    print("REGIME")
    print("=" * 80)
    for market, bench_sym in (("india", "^NSEI"), ("us", "^GSPC"), ("crypto", "BTC-USD")):
        snap = load_snapshot(market)
        if not snap:
            print(f"{market}: no snapshot")
            continue
        b = breadth(snap)
        bench = None
        for g in snap["groups"].values():
            if bench_sym in g:
                bench = g[bench_sym]
        label, why = classify(b, bench)
        vix = None
        for g in snap["groups"].values():
            for k in ("^INDIAVIX", "^VIX"):
                if k in g:
                    vix = g[k]["price"]
        print(f"\n  {market.upper():8} {label}")
        print(f"           {' · '.join(why)}")
        print(f"           median member 1y {b['median_1y']:+.1f}%, median RSI {b['median_rsi']:.0f}"
              + (f", VIX {vix}" if vix else ""))

    print("\n" + "=" * 80)
    print("BOOK STRESS TEST — worst actual days, 2y")
    print("=" * 80)
    px = yf.download(BOOK + ["^NSEI"], period="2y", interval="1d", group_by="ticker",
                     auto_adjust=True, progress=False, threads=True)
    cols = {}
    for t in BOOK + ["^NSEI"]:
        try:
            s = px[t]["Close"].dropna()
            if len(s) > 200:
                cols[t] = s
        except Exception:
            pass
    df = pd.DataFrame(cols)
    rets = df.pct_change().dropna()
    held = [t for t in BOOK if t in rets.columns]

    # Equal-weighted book, rebalanced daily. Crude, but it isolates selection from sizing.
    book = rets[held].mean(axis=1)
    nifty = rets["^NSEI"]

    worst = nifty.nsmallest(10)
    print(f"\n  {'date':<12}{'Nifty%':>9}{'book%':>9}{'excess':>9}")
    for d, v in worst.items():
        if d in book.index:
            print(f"  {d:%Y-%m-%d}  {v*100:>8.2f} {book.loc[d]*100:>8.2f} {(book.loc[d]-v)*100:>8.2f}")

    dd_book = float((( 1 + book).cumprod() / (1 + book).cumprod().cummax() - 1).min() * 100)
    dd_nifty = float(((1 + nifty).cumprod() / (1 + nifty).cumprod().cummax() - 1).min() * 100)
    down = nifty < 0
    print(f"\n  max drawdown        book {dd_book:>7.1f}%   Nifty {dd_nifty:>7.1f}%")
    print(f"  ann vol             book {book.std()*np.sqrt(252)*100:>7.1f}%   "
          f"Nifty {nifty.std()*np.sqrt(252)*100:>7.1f}%")
    print(f"  downside capture    {book[down].mean()/nifty[down].mean()*100:>7.0f}%  "
          f"(<100 = book falls less than the index on down days)")
    print(f"  upside capture      {book[~down].mean()/nifty[~down].mean()*100:>7.0f}%")
    print(f"  2y cumulative       book {((1+book).prod()-1)*100:>7.1f}%   "
          f"Nifty {((1+nifty).prod()-1)*100:>7.1f}%")
    print("\n  Equal-weighted and daily-rebalanced -- isolates selection, ignores sizing and costs.")
    print("  !! The cumulative return line is NOT evidence of skill. These names were chosen")
    print("     today with full knowledge of their two-year history, so the backtest measures")
    print("     hindsight, not process. Only the volatility, drawdown and capture ratios are")
    print("     meaningful -- those describe co-movement rather than selection.")


if __name__ == "__main__":
    main()
