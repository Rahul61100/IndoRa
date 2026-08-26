# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas", "numpy"]
# ///
"""
Live intraday monitor for the Indian session (09:15-15:30 IST).

    uv run scripts/intraday.py                 # one snapshot
    uv run scripts/intraday.py --log           # also append to journal/<date>-intraday.md
    uv run scripts/intraday.py --market us

Built for watching flow rather than reading a close. It reports what a close cannot:
where the day opened relative to the prior close, whether volume is running ahead of
or behind normal pace at this point in the session, which way breadth is leaning
intraday, and whether any held position has broken a level that matters.

Volume pace is the point. A stock down 1% on double the normal pace is a different
event from one down 1% on half of it, and the daily bar cannot tell them apart.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
IST = timezone(timedelta(hours=5, minutes=30))

WATCH = {
    "india": {
        "indices": ["^NSEI", "^NSEBANK", "^NSEMDCP50", "^INDIAVIX"],
        "macro": ["USDINR=X", "BZ=F", "GC=F"],
        "book": ["ICICIBANK.NS", "BHARTIARTL.NS", "HAL.NS", "SBIN.NS",
                 "DIXON.NS", "HDFCBANK.NS", "NTPC.NS", "RELIANCE.NS"],
        "open": (9, 15), "close": (15, 30),
    },
    "us": {
        "indices": ["^GSPC", "^IXIC", "^RUT", "^VIX"],
        "macro": ["^TNX", "DX-Y.NYB", "BZ=F", "GC=F"],
        "book": [],
        "open": (9, 30), "close": (16, 0),
    },
}


def session_progress(cfg: dict, now_local: datetime) -> float:
    o = now_local.replace(hour=cfg["open"][0], minute=cfg["open"][1], second=0, microsecond=0)
    c = now_local.replace(hour=cfg["close"][0], minute=cfg["close"][1], second=0, microsecond=0)
    if now_local <= o:
        return 0.0
    if now_local >= c:
        return 1.0
    return (now_local - o).total_seconds() / (c - o).total_seconds()


def pull(tickers: list[str]) -> dict[str, dict]:
    """5-minute bars for today plus daily bars for the reference levels."""
    intr = yf.download(tickers, period="2d", interval="5m", group_by="ticker",
                       auto_adjust=False, progress=False, threads=True)
    daily = yf.download(tickers, period="3mo", interval="1d", group_by="ticker",
                        auto_adjust=False, progress=False, threads=True)
    out: dict[str, dict] = {}
    for t in tickers:
        try:
            i = intr[t].dropna(subset=["Close"])
            d = daily[t].dropna(subset=["Close"])
        except Exception:
            continue
        if len(i) < 2 or len(d) < 21:
            continue
        last_day = i.index[-1].date()
        today = i[i.index.map(lambda x: x.date() == last_day)]
        if today.empty:
            continue
        prev_close = float(d["Close"].iloc[-2]) if d.index[-1].date() == last_day else float(d["Close"].iloc[-1])
        cur = float(today["Close"].iloc[-1])
        out[t] = {
            "price": cur,
            "prev_close": prev_close,
            "chg_pct": (cur / prev_close - 1) * 100,
            "open": float(today["Open"].iloc[0]),
            "gap_pct": (float(today["Open"].iloc[0]) / prev_close - 1) * 100,
            "high": float(today["High"].max()),
            "low": float(today["Low"].min()),
            "vol_today": float(today["Volume"].sum()),
            "vol_20d": float(d["Volume"].tail(21).iloc[:-1].mean()),
            "sma20": float(d["Close"].rolling(20).mean().iloc[-1]),
            "sma50": float(d["Close"].rolling(50).mean().iloc[-1]) if len(d) >= 50 else None,
            "bars": len(today),
            "asof": today.index[-1],
        }
    return out


def fmt(rows: dict[str, dict], progress: float, label: str) -> list[str]:
    L = [f"### {label}", "```",
         f"{'symbol':<15}{'price':>11}{'chg%':>8}{'gap%':>8}{'range%':>8}"
         f"{'vol pace':>10}{'vs20d%':>9}  level"]
    for t, r in rows.items():
        rng = (r["high"] - r["low"]) / r["prev_close"] * 100
        # Volume pace is only meaningful for cash equities. Yahoo reports no volume for
        # Indian indices, and futures volume spans contracts, so both give nonsense.
        cash_equity = not (t.startswith("^") or "=" in t)
        expected = r["vol_20d"] * max(progress, 0.02)
        pace = (r["vol_today"] / expected) if (cash_equity and expected > 0) else None
        v20 = (r["price"] / r["sma20"] - 1) * 100
        note = []
        if pace is not None:
            if pace > 1.6:
                note.append("HEAVY VOL")
            elif pace < 0.5:
                note.append("thin")
        if abs(r["gap_pct"]) > 1.0:
            note.append(f"gap {r['gap_pct']:+.1f}%")
        if r["sma50"]:
            crossed = (r["prev_close"] - r["sma50"]) * (r["price"] - r["sma50"]) < 0
            if crossed:
                side = "above" if r["price"] > r["sma50"] else "below"
                note.append(f"**50DMA cross {side}**")
        pace_s = f"{pace:>10.2f}" if pace is not None else f"{'—':>10}"
        L.append(f"{t:<15}{r['price']:>11,.2f}{r['chg_pct']:>8.2f}{r['gap_pct']:>8.2f}"
                 f"{rng:>8.2f}{pace_s}{v20:>9.1f}  {' '.join(note)}")
    L.append("```")
    return L


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", default="india", choices=list(WATCH))
    ap.add_argument("--log", action="store_true")
    args = ap.parse_args()
    cfg = WATCH[args.market]

    tz = IST if args.market == "india" else timezone(timedelta(hours=-4))
    now_local = datetime.now(tz)
    progress = session_progress(cfg, now_local)
    state = ("PRE-OPEN" if progress == 0 else
             "CLOSED" if progress == 1 else f"{progress*100:.0f}% through session")

    all_t = cfg["indices"] + cfg["macro"] + cfg["book"]
    rows = pull(all_t)
    if not rows:
        print("no intraday data returned — market may be closed with no recent bars")
        return

    L = [f"# Intraday — {args.market.upper()} — {now_local:%Y-%m-%d %H:%M} "
         f"{'IST' if args.market=='india' else 'ET'}  ({state})", ""]
    for group, label in (("indices", "Indices"), ("macro", "Macro"), ("book", "Open book")):
        sub = {t: rows[t] for t in cfg[group] if t in rows}
        if sub:
            L += fmt(sub, progress, label) + [""]

    book = {t: rows[t] for t in cfg["book"] if t in rows}
    if book:
        up = sum(1 for r in book.values() if r["chg_pct"] > 0)
        heavy = [t for t, r in book.items()
                 if not (t.startswith("^") or "=" in t)
                 and r["vol_today"] / max(r["vol_20d"] * max(progress, 0.02), 1) > 1.6]
        L += ["### Read", "",
              f"- Book breadth: **{up}/{len(book)} up**",
              f"- Running heavy volume: {', '.join(heavy) if heavy else 'none'}",
              "- Volume pace is the signal. Same price move on double pace versus half pace",
              "  are different events, and a daily bar cannot separate them.", ""]

    text = "\n".join(L)
    print(text)
    if args.log:
        out = ROOT / "journal" / f"{now_local:%Y-%m-%d}-intraday.md"
        with out.open("a") as f:
            f.write(text + "\n\n---\n\n")
        print(f"\nappended to {out}")


if __name__ == "__main__":
    main()
