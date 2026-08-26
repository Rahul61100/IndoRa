# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas", "numpy"]
# ///
"""
Daily market snapshot for the India research loop.

Pulls OHLCV from Yahoo for every ticker in universe/india.json, derives the
technical state the daily note needs, flags anything that looks like bad data,
and writes:

    data/daily/YYYY-MM-DD.json   full machine-readable snapshot
    data/daily/latest.json       copy of the newest snapshot

Usage:  uv run scripts/fetch_daily.py [--period 3y] [--universe india]

Yahoo's grouped download intermittently drops symbols that fetch fine on their
own, so anything missing from the batch is retried individually before being
reported as genuinely unavailable. Yahoo also carries stale prints on the NSE
sector indices; every derived move is checked against the quality rules in
playbooks/data-quality-rules.md and suspicious rows are flagged rather than
silently trusted.
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "daily"

# A one-day move beyond this on an index is far more likely to be a stale or
# missing prior print than a real session. Cross-check before quoting it.
INDEX_MOVE_SUSPECT_PCT = 4.0
STOCK_MOVE_SUSPECT_PCT = 15.0
STALE_AFTER_DAYS = 5


def rsi(series: pd.Series, window: int = 14) -> float:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / window, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / window, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return float((100 - 100 / (1 + rs)).iloc[-1])


def atr_pct(df: pd.DataFrame, window: int = 14) -> float:
    hl = df["High"] - df["Low"]
    hc = (df["High"] - df["Close"].shift()).abs()
    lc = (df["Low"] - df["Close"].shift()).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return float(tr.ewm(alpha=1 / window, adjust=False).mean().iloc[-1] / df["Close"].iloc[-1] * 100)


def ret(series: pd.Series, days: int) -> float | None:
    if len(series) <= days:
        return None
    return float((series.iloc[-1] / series.iloc[-1 - days] - 1) * 100)


def _r(v):
    return round(v, 2) if v is not None else None


def _trend(last: float, smas: dict) -> str:
    s50, s200 = smas.get("sma50"), smas.get("sma200")
    if not s50 or not s200:
        return "unknown"
    if last > s50 > s200:
        return "uptrend"
    if last < s50 < s200:
        return "downtrend"
    return "above-200dma-choppy" if last > s200 else "below-200dma-choppy"


def analyse(sym: str, df: pd.DataFrame, bench: pd.Series | None) -> dict | None:
    df = df.dropna(subset=["Close"])
    if len(df) < 60:
        return None
    close = df["Close"]
    last = float(close.iloc[-1])
    is_index = sym.startswith("^")

    smas = {f"sma{w}": (float(close.rolling(w).mean().iloc[-1]) if len(close) >= w else None)
            for w in (20, 50, 100, 200)}

    win52 = close.tail(252)
    hi52, lo52 = float(win52.max()), float(win52.min())
    pctile = float((win52 < last).mean() * 100)

    dr = close.pct_change().dropna()
    vol = float(dr.tail(50).std() * np.sqrt(252) * 100) if len(dr) >= 50 else None

    chg1d = ret(close, 1)

    vol_ratio = None
    if "Volume" in df and df["Volume"].tail(60).sum() > 0:
        v20 = float(df["Volume"].tail(21).iloc[:-1].mean())
        if v20 > 0:
            vol_ratio = round(float(df["Volume"].iloc[-1]) / v20, 2)

    flags = []
    last_bar = df.index[-1].to_pydatetime().replace(tzinfo=None)
    if datetime.utcnow() - last_bar > timedelta(days=STALE_AFTER_DAYS):
        flags.append(f"stale:last_bar={last_bar:%Y-%m-%d}")
    limit = INDEX_MOVE_SUSPECT_PCT if is_index else STOCK_MOVE_SUSPECT_PCT
    if chg1d is not None and abs(chg1d) > limit:
        flags.append(f"suspect_1d_move:{chg1d:.1f}pct__verify_against_news")
    gap = (df.index.to_series().diff().dt.days.max())
    if pd.notna(gap) and gap > 10:
        flags.append(f"history_gap_days:{int(gap)}")

    out = {
        "price": round(last, 2),
        "chg_1d_pct": _r(chg1d),
        "returns_pct": {"1w": _r(ret(close, 5)), "1m": _r(ret(close, 21)),
                        "3m": _r(ret(close, 63)), "6m": _r(ret(close, 126)),
                        "1y": _r(ret(close, 252))},
        "sma": {k: (round(v, 2) if v else None) for k, v in smas.items()},
        "vs_sma_pct": {k: (round((last / v - 1) * 100, 2) if v else None) for k, v in smas.items()},
        "rsi14": round(rsi(close), 1),
        "atr14_pct": round(atr_pct(df), 2),
        "vol50_ann_pct": round(vol, 1) if vol else None,
        "volume_vs_20d": vol_ratio,
        "high52": round(hi52, 2),
        "low52": round(lo52, 2),
        "from_high52_pct": round((last / hi52 - 1) * 100, 2),
        "from_low52_pct": round((last / lo52 - 1) * 100, 2),
        "pctile_52w": round(pctile, 1),
        "trend": _trend(last, smas),
        "last_bar": f"{last_bar:%Y-%m-%d}",
        "flags": flags,
    }

    if bench is not None:
        joined = pd.concat([close, bench], axis=1, join="inner").dropna()
        if len(joined) > 63:
            s, b = joined.iloc[:, 0], joined.iloc[:, 1]
            out["rel_strength_vs_nifty_pct"] = {
                lbl: (_r(ret(s, d) - ret(b, d)) if ret(b, d) is not None and ret(s, d) is not None else None)
                for lbl, d in (("3m", 63), ("6m", 126), ("1y", 252))
            }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--period", default="3y")
    ap.add_argument("--universe", default="india")
    args = ap.parse_args()

    universe = json.loads((ROOT / "universe" / f"{args.universe}.json").read_text())
    tickers = [t for group in universe.values() for t in group]

    raw = yf.download(tickers, period=args.period, interval="1d", group_by="ticker",
                      auto_adjust=False, progress=False, threads=True)

    frames: dict[str, pd.DataFrame] = {}
    retried: list[str] = []
    for sym in tickers:
        df = None
        try:
            df = raw[sym].dropna(how="all")
        except Exception:
            df = None
        if df is None or len(df) < 60:
            # Grouped download drops symbols intermittently; a solo fetch usually works.
            try:
                df = yf.Ticker(sym).history(period=args.period, interval="1d", auto_adjust=False)
                retried.append(sym)
            except Exception:
                df = None
        if df is not None and len(df) >= 60:
            frames[sym] = df

    bench = frames["^NSEI"]["Close"].dropna() if "^NSEI" in frames else None

    snapshot: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period": args.period,
        "universe": args.universe,
        "groups": {},
    }
    missing: list[str] = []
    flagged: list[str] = []

    for group, syms in universe.items():
        snapshot["groups"][group] = {}
        for sym in syms:
            if sym not in frames:
                missing.append(sym)
                continue
            res = analyse(sym, frames[sym], bench if sym != "^NSEI" else None)
            if res is None:
                missing.append(sym)
                continue
            if res["flags"]:
                flagged.append(f"{sym}: {'; '.join(res['flags'])}")
            snapshot["groups"][group][sym] = res

    snapshot["missing"] = missing
    snapshot["retried_individually"] = retried
    snapshot["quality_flags"] = flagged

    outdir = OUTDIR / args.universe
    outdir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    payload = json.dumps(snapshot, indent=1)
    (outdir / f"{stamp}.json").write_text(payload)
    (outdir / "latest.json").write_text(payload)

    print(f"wrote {outdir / f'{stamp}.json'}")
    print(f"  ok={len(frames)}/{len(tickers)}  retried={len(retried)}  missing={len(missing)}  flagged={len(flagged)}")
    if missing:
        print("  missing:", ", ".join(missing))
    for f in flagged:
        print("  FLAG:", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
