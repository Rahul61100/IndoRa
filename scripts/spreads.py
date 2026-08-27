# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance","pandas","numpy"]
# ///
"""
Cross-sectional theme spreads — what a security-level process cannot see.

    uv run scripts/spreads.py
    uv run scripts/spreads.py --window 126

Built the day the monsoon trade was found, months late. Rural-exposed names had underperformed
urban ones by **21.4pp over six months** — the largest persistent divergence in the Indian
market — and nothing in this workspace noticed, because every screen here looks at individual
securities. A dominant spread between two *groups* is structurally invisible to a process that
ranks names.

Each theme is a pair of baskets that should diverge if the theme is real. The output is the
spread and, more usefully, whether it is *widening or narrowing* — a spread already at its
extreme is a finished trade, which is the mistake this file exists to stop repeating.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import numpy as np
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent

THEMES = {
    "monsoon / rural vs urban": {
        "long": {"TRENT.NS": "Trent", "TITAN.NS": "Titan", "JUBLFOOD.NS": "Jubilant",
                 "DMART.NS": "DMart", "INDIGO.NS": "IndiGo"},
        "short": {"DABUR.NS": "Dabur", "HINDUNILVR.NS": "HUL", "ITC.NS": "ITC",
                  "BRITANNIA.NS": "Britannia", "COROMANDEL.NS": "Coromandel",
                  "ESCORTS.NS": "Escorts", "UPL.NS": "UPL"},
        "reads": "urban premium consumption over rural/agri exposure",
    },
    "exporters vs domestic": {
        "long": {"DMART.NS": "DMart", "TRENT.NS": "Trent", "NTPC.NS": "NTPC",
                 "POWERGRID.NS": "Power Grid", "SBIN.NS": "SBI"},
        "short": {"INFY.NS": "Infosys", "TCS.NS": "TCS", "SUNPHARMA.NS": "Sun Pharma",
                  "CIPLA.NS": "Cipla", "TATASTEEL.NS": "Tata Steel"},
        "reads": "domestic revenue over US/EU-exposed revenue (tariffs, H-1B, CBAM)",
    },
    "value vs momentum": {
        "long": {"TITAN.NS": "Titan", "TRENT.NS": "Trent", "BHARTIARTL.NS": "Bharti",
                 "M&M.NS": "M&M"},
        "short": {"IOC.NS": "IOC", "BPCL.NS": "BPCL", "COALINDIA.NS": "Coal India",
                  "ONGC.NS": "ONGC", "HINDUNILVR.NS": "HUL"},
        "reads": "expensive-and-trending over cheap-and-falling",
    },
    "private vs PSU banks": {
        "long": {"ICICIBANK.NS": "ICICI", "HDFCBANK.NS": "HDFC Bank", "KOTAKBANK.NS": "Kotak",
                 "AXISBANK.NS": "Axis"},
        "short": {"SBIN.NS": "SBI", "BANKBARODA.NS": "BoB", "CANBK.NS": "Canara",
                  "PNB.NS": "PNB"},
        "reads": "private banks over public sector banks",
    },
    "capex vs consumption": {
        "long": {"LT.NS": "L&T", "SIEMENS.NS": "Siemens", "ABB.NS": "ABB",
                 "CUMMINSIND.NS": "Cummins"},
        "short": {"HINDUNILVR.NS": "HUL", "NESTLEIND.NS": "Nestle", "MARICO.NS": "Marico",
                  "DABUR.NS": "Dabur"},
        "reads": "industrial capex over consumer staples",
    },
}


def basket(px, syms, k: int) -> float | None:
    """Equal-weighted median return over k sessions — median, not mean, so one name cannot carry it."""
    rets = []
    for s in syms:
        if s not in px:
            continue
        c = px[s].dropna()
        if len(c) <= k:
            continue
        rets.append((float(c.iloc[-1]) / float(c.iloc[-k]) - 1) * 100)
    return float(np.median(rets)) if rets else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=126)
    args = ap.parse_args()

    syms = sorted({s for t in THEMES.values() for side in ("long", "short") for s in t[side]})
    px = yf.download(syms, period="1y", interval="1d", progress=False, auto_adjust=True)["Close"].ffill()

    print("CROSS-SECTIONAL THEME SPREADS — group against group, not name against name")
    print("=" * 94)
    out = {}
    for name, t in THEMES.items():
        spreads = {}
        for lbl, k in [("1m", 22), ("3m", 66), ("6m", 126)]:
            a, b = basket(px, t["long"], k), basket(px, t["short"], k)
            spreads[lbl] = (a - b) if (a is not None and b is not None) else None
        s1, s3, s6 = spreads["1m"], spreads["3m"], spreads["6m"]
        print(f"\n  {name}")
        print(f"    {t['reads']}")
        row = "    "
        for lbl in ("1m", "3m", "6m"):
            v = spreads[lbl]
            row += f"{lbl} {v:+7.1f}pp   " if v is not None else f"{lbl}    n/a   "
        print(row)
        if s1 is not None and s6 is not None:
            # Is the theme still working, or is it a finished trade?
            if abs(s6) < 3:
                verdict = "no meaningful spread — theme is not expressing"
            elif (s6 > 0) == (s1 > 0) and abs(s1) > abs(s6) / 6:
                verdict = "WIDENING — theme still working"
            elif (s6 > 0) != (s1 > 0):
                verdict = "*** REVERSING — the last month runs against the six-month spread ***"
            else:
                verdict = "narrowing — the trade may be finished; a wide spread is not an entry"
            print(f"    -> {verdict}")
        out[name] = spreads

    print("\n" + "=" * 94)
    biggest = max((v for v in out.values() if v["6m"] is not None),
                  key=lambda v: abs(v["6m"]), default=None)
    if biggest:
        nm = [k for k, v in out.items() if v is biggest][0]
        print(f"WIDEST 6m SPREAD: {nm} at {biggest['6m']:+.1f}pp")
        print("A spread this size is the market's dominant view. Holding no position on either")
        print("side of it is a choice, and it should be a deliberate one.")

    p = ROOT / "data" / "spreads.json"
    hist = json.loads(p.read_text()) if p.exists() else {}
    hist[str(date.today())] = {k: {kk: (round(vv, 2) if vv is not None else None)
                                   for kk, vv in v.items()} for k, v in out.items()}
    p.write_text(json.dumps(hist, indent=1))
    print(f"\n-> {p}")


if __name__ == "__main__":
    main()
