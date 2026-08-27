# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas"]
# ///
"""
FX levels, sourced from intraday and never from Yahoo's daily bar.

    uv run scripts/fx.py

This exists because the same instrument produced the same fabricated move twice.

Yahoo's `INR=X` daily bar for 2026-08-26 reads O 93.546 H 95.412 L 93.546 C 93.546. The
intraday series for that session never traded below 95.402. The daily close is wrong by
~1.9%, and any one-day return computed off it the following morning reads +2.1% when the
real move was +0.12%.

The trap is that the bad bar is **internally self-consistent** — its close sits inside its
own high/low, its open equals its low. Every plausible sanity check passes. The first fix
attempted here was a tolerance check and it failed for exactly that reason.

The rule that actually works, and the one this file enforces:
**prefer a source that cannot be wrong over a check that decides whether a source is wrong.**
The last intraday print of a session is the close. Derive it; do not validate it.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
PAIRS = {"INR=X": "USDINR", "EURUSD=X": "EURUSD", "JPY=X": "USDJPY",
         "CNY=X": "USDCNY", "DX-Y.NYB": "DXY"}


def closes_from_intraday(sym: str) -> list[tuple[date, float]]:
    i = yf.download(sym, period="1mo", interval="60m", progress=False, auto_adjust=True)
    if i is None or i.empty:
        return []
    c = i["Close"].squeeze().dropna()
    out = {}
    for ts, v in c.items():
        out[ts.date()] = float(v)   # later bars overwrite earlier: last print wins
    return sorted(out.items())


def main() -> None:
    print("FX — closes derived from the intraday series, not Yahoo's daily bar")
    print("=" * 92)
    snap = {}
    for sym, name in PAIRS.items():
        ser = closes_from_intraday(sym)
        if len(ser) < 2:
            print(f"  {name:<9} no intraday series")
            continue
        (d0, p0), (d1, p1) = ser[-2], ser[-1]
        chg = (p1 / p0 - 1) * 100

        daily = yf.download(sym, period="10d", interval="1d", progress=False, auto_adjust=True)
        note = ""
        if daily is not None and not daily.empty:
            dc = daily["Close"].squeeze().dropna()
            for dd, dv in dc.items():
                m = dict(ser).get(dd.date())
                if m and abs(float(dv) / m - 1) > 0.005:
                    note = (f"   !! Yahoo daily bar for {dd.date()} says {float(dv):.3f}, "
                            f"intraday says {m:.3f} ({(float(dv)/m-1)*100:+.2f}%) — DAILY BAR IS WRONG")
        print(f"  {name:<9}{p1:>10.3f}   {chg:+6.2f}% vs {d0}{note}")
        snap[name] = {"close": round(p1, 4), "date": str(d1), "prev": round(p0, 4),
                      "prev_date": str(d0), "chg_pct": round(chg, 3), "source": "intraday_last_print"}

    p = ROOT / "data" / "fx.json"
    hist = json.loads(p.read_text()) if p.exists() else {}
    hist[str(date.today())] = snap
    p.write_text(json.dumps(hist, indent=1))
    print("=" * 92)
    print(f"-> {p}")


if __name__ == "__main__":
    main()
