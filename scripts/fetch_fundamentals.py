# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas"]
# ///
"""
Earnings-quality collector — Phase A2 of BUILD.md.

    uv run scripts/fetch_fundamentals.py --universe india
    uv run scripts/fetch_fundamentals.py --book        # just the open positions

Built the day the Dixon position closed, and it is the generalisation of that catch. Dixon
reported revenue +21.1% with operating income −8.6% and net income +194.8% — profit at 1.86×
operating income, i.e. from below the line. No price or revision screen sees that. Four
flags, each of which would have caught it independently:

  BELOW_THE_LINE    net income far above operating income -- profit is not from the business
  OPERATING_DELEVERAGE  revenue growing while operating income shrinks
  MARGIN_SLIDE      operating margin down across consecutive quarters
  CONSENSUS_DECLINE forward P/E above trailing P/E -- the market expects EPS to fall

Writes data/fundamentals/<market>.json, which tools/score.py reads for the `margin_below`
check type.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
CR = 1e7  # yfinance reports INR; 1 crore = 1e7


def series(fin, row):
    if fin is None or fin.empty or row not in fin.index:
        return []
    s = fin.loc[row].dropna()
    return [(c.date().isoformat(), float(v) / CR) for c, v in s.items()]


def pull(sym: str) -> dict | None:
    t = yf.Ticker(sym)
    try:
        q, info = t.quarterly_financials, t.info
    except Exception as e:
        return {"symbol": sym, "error": str(e)[:120]}

    rev, op, ni = series(q, "Total Revenue"), series(q, "Operating Income"), series(q, "Net Income")
    if not rev or not op:
        return {"symbol": sym, "error": "no quarterly income statement"}

    opm = [(d, o / r * 100) for (d, r), (_, o) in zip(rev, op) if r]
    out = {
        "symbol": sym,
        "quarters": [d for d, _ in rev][:6],
        "revenue_cr": [round(v, 1) for _, v in rev][:6],
        "operating_income_cr": [round(v, 1) for _, v in op][:6],
        "net_income_cr": [round(v, 1) for _, v in ni][:6],
        "operating_margin_pct_series": [round(v, 2) for _, v in opm][:6],
        "operating_margin_pct": round(opm[0][1], 2) if opm else None,
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "flags": [],
    }

    # BELOW_THE_LINE: profit that is not coming from operations
    if ni and op and op[0][1] > 0:
        ratio = ni[0][1] / op[0][1]
        out["net_to_operating"] = round(ratio, 2)
        if ratio > 1.4:
            out["flags"].append(f"BELOW_THE_LINE net income {ratio:.2f}x operating income")

    # Year-on-year, like for like -- index 4 is the same quarter a year earlier
    if len(rev) >= 5 and len(op) >= 5 and rev[4][1] and op[4][1]:
        rg, og = (rev[0][1] / rev[4][1] - 1) * 100, (op[0][1] / op[4][1] - 1) * 100
        out["revenue_yoy_pct"], out["operating_income_yoy_pct"] = round(rg, 1), round(og, 1)
        if rg > 5 and og < 0:
            out["flags"].append(f"OPERATING_DELEVERAGE revenue {rg:+.1f}% but operating income {og:+.1f}%")

    # MARGIN_SLIDE: three consecutive declines
    m = [v for _, v in opm][:4]
    if len(m) >= 4 and m[0] < m[1] < m[2] < m[3]:
        out["flags"].append(f"MARGIN_SLIDE {m[3]:.2f}% -> {m[0]:.2f}% over four quarters")

    # CONSENSUS_DECLINE: forward multiple above trailing
    tp, fp = out["trailing_pe"], out["forward_pe"]
    if tp and fp and fp > tp * 1.05:
        out["flags"].append(f"CONSENSUS_DECLINE forward PE {fp:.1f} > trailing {tp:.1f}, "
                            f"implies EPS {(tp/fp - 1)*100:+.0f}%")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", default="india")
    ap.add_argument("--book", action="store_true")
    ap.add_argument("--groups", default="watchlist")
    args = ap.parse_args()

    if args.book:
        reg = json.loads((ROOT / "positions" / "theses.json").read_text())
        syms = sorted({t["symbol"] for t in reg["theses"]})
        label = "OPEN BOOK"
    else:
        uni = json.loads((ROOT / "universe" / f"{args.universe}.json").read_text())
        groups = args.groups.split(",") if args.groups else list(uni)
        syms = sorted({s for k in groups for s in uni.get(k, [])})
        label = args.universe.upper()

    print(f"EARNINGS QUALITY — {label} ({len(syms)} names)\n" + "=" * 78)
    results, flagged = {}, 0
    for s in syms:
        r = pull(s)
        if not r or r.get("error"):
            print(f"  {s:<18} -- {r.get('error','no data') if r else 'no data'}")
            continue
        results[s] = r
        if r["flags"]:
            flagged += 1
            print(f"\n  {s:<18} op margin {r['operating_margin_pct']:>6.2f}%")
            for f in r["flags"]:
                print(f"      !! {f}")
        else:
            print(f"  {s:<18} op margin {r['operating_margin_pct']:>6.2f}%   clean")

    outp = ROOT / "data" / "fundamentals" / f"{args.universe}.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    prev = json.loads(outp.read_text()) if outp.exists() else {}
    prev.update(results)
    prev["_updated"] = f"{date.today():%Y-%m-%d}"
    outp.write_text(json.dumps(prev, indent=1))
    print("\n" + "=" * 78)
    print(f"{flagged}/{len(results)} carry at least one earnings-quality flag -> {outp}")


if __name__ == "__main__":
    main()
