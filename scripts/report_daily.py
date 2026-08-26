# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy"]
# ///
"""
Turn the newest data/daily snapshot into the markdown brief the daily loop reads.

    uv run scripts/report_daily.py [--date YYYY-MM-DD] [--write]

Without --write it prints to stdout. With --write it saves to
journal/YYYY-MM-DD-data.md so the narrative note can link to it.

Sector rotation is computed from constituent baskets in universe/sectors.json
using the equal-weighted MEDIAN member return. Median rather than mean because
one 40% mover should not make a sector look broadly strong -- what matters for
rotation is whether the typical member is participating.
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(market: str, date: str | None) -> dict:
    p = ROOT / "data" / "daily" / market / (f"{date}.json" if date else "latest.json")
    return json.loads(p.read_text())


def flat(snap: dict) -> dict[str, dict]:
    out = {}
    for group, members in snap["groups"].items():
        for sym, rec in members.items():
            rec = dict(rec)
            rec["_group"] = group
            out[sym] = rec
    return out


def fmt(v, width=7, dp=1, suffix=""):
    if v is None:
        return " " * (width - 1) + "-"
    return f"{v:>{width}.{dp}f}{suffix}"


def line(sym: str, r: dict, label_w: int = 15) -> str:
    ret = r["returns_pct"]
    rs = (r.get("rel_strength_vs_nifty_pct") or {}).get("1y")
    warn = " !" if r.get("flags") else "  "
    return (f"{sym:<{label_w}}{r['price']:>10,.1f}{fmt(r['chg_1d_pct'])}"
            f"{fmt(ret['1m'])}{fmt(ret['3m'])}{fmt(ret['6m'])}{fmt(ret['1y'])}"
            f"{r['rsi14']:>6.0f}{fmt(r['vs_sma_pct']['sma200'])}"
            f"{fmt(r['from_high52_pct'])}{fmt(rs)}  {r['trend']}{warn}")


HEAD = (f"{'symbol':<15}{'price':>10}{'1d%':>7}{'1m%':>7}{'3m%':>7}{'6m%':>7}"
        f"{'1y%':>7}{'RSI':>6}{'v200%':>7}{'frHi%':>7}{'RS1y%':>7}  trend")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--market", default="india")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    snap = load(args.market, args.date)
    rows = flat(snap)
    sec_file = "sectors.json" if args.market == "india" else f"{args.market}-sectors.json"
    sectors = json.loads((ROOT / "universe" / sec_file).read_text())
    stamp = snap["generated_at"][:10]

    L: list[str] = []
    add = L.append

    add(f"# {args.market.upper()} data brief — {stamp}")
    add("")
    add(f"_Generated from `data/daily/{args.market}/{stamp}.json`. Every number is a close-to-close "
        f"derivation from Yahoo OHLC. Read `playbooks/data-quality-rules.md` before "
        f"quoting any single-day move._")
    add("")

    add("## Benchmarks and macro")
    add("```")
    add(HEAD)
    for g in ("benchmarks", "macro"):
        for sym, r in snap["groups"].get(g, {}).items():
            add(line(sym, r))
    add("```")
    add("")

    add("## Sector rotation (median member return, equal weighted)")
    add("```")
    add(f"{'sector':<22}{'n':>3}{'1m%':>8}{'3m%':>8}{'6m%':>8}{'1y%':>8}{'medRSI':>8}   %members>200dma")
    scored = []
    for name, members in sectors.items():
        if name.startswith("_"):
            continue
        have = [rows[m] for m in members if m in rows]
        if not have:
            continue

        def med(key):
            vals = [h["returns_pct"][key] for h in have if h["returns_pct"][key] is not None]
            return statistics.median(vals) if vals else None

        above = sum(1 for h in have if (h["vs_sma_pct"]["sma200"] or -1) > 0) / len(have) * 100
        scored.append((name, len(have), med("1m"), med("3m"), med("6m"), med("1y"),
                       statistics.median([h["rsi14"] for h in have]), above))
    for name, n, m1, m3, m6, y1, r14, above in sorted(scored, key=lambda x: -(x[5] or -999)):
        add(f"{name:<22}{n:>3}{fmt(m1,8)}{fmt(m3,8)}{fmt(m6,8)}{fmt(y1,8)}{fmt(r14,8)}{above:>16.0f}%")
    add("```")
    add("")

    add("## Open positions")
    add("```")
    add(HEAD)
    for g in ("positions_short", "positions_medium", "positions_long"):
        add(f"-- {g.replace('positions_', '').upper()} " + "-" * 40)
        for sym, r in snap["groups"].get(g, {}).items():
            add(line(sym, r))
    add("```")
    add("")

    stocks = {s: r for s, r in rows.items() if not s.startswith("^") and "=" not in s}
    if not stocks:
        stocks = dict(rows)
    by1y = sorted(stocks.items(), key=lambda kv: -(kv[1]["returns_pct"]["1y"] or -999))

    add("## Leaders (top 12 by 1y)")
    add("```")
    add(HEAD)
    for sym, r in by1y[:12]:
        add(line(sym, r))
    add("```")
    add("")
    add("## Laggards (bottom 12 by 1y)")
    add("```")
    add(HEAD)
    for sym, r in by1y[-12:]:
        add(line(sym, r))
    add("```")
    add("")

    os = [(s, r) for s, r in stocks.items() if r["rsi14"] < 35]
    ob = [(s, r) for s, r in stocks.items() if r["rsi14"] > 70]
    add("## Extremes")
    add(f"- Oversold, RSI<35: " + (", ".join(f"{s} ({r['rsi14']:.0f})" for s, r in sorted(os, key=lambda kv: kv[1]['rsi14'])) or "none"))
    add(f"- Overbought, RSI>70: " + (", ".join(f"{s} ({r['rsi14']:.0f})" for s, r in sorted(ob, key=lambda kv: -kv[1]['rsi14'])) or "none"))
    nh = [s for s, r in stocks.items() if r["from_high52_pct"] > -2]
    nl = [s for s, r in stocks.items() if r["from_low52_pct"] < 3]
    add(f"- Within 2% of 52w high: " + (", ".join(nh) or "none"))
    add(f"- Within 3% of 52w low: " + (", ".join(nl) or "none"))
    add("")

    breadth_200 = sum(1 for r in stocks.values() if (r["vs_sma_pct"]["sma200"] or -1) > 0) / len(stocks) * 100
    breadth_50 = sum(1 for r in stocks.values() if (r["vs_sma_pct"]["sma50"] or -1) > 0) / len(stocks) * 100
    add("## Breadth")
    add(f"- {breadth_200:.0f}% of tracked stocks above their 200 DMA")
    add(f"- {breadth_50:.0f}% above their 50 DMA")
    add(f"- uptrend: {sum(1 for r in stocks.values() if r['trend']=='uptrend')} / "
        f"downtrend: {sum(1 for r in stocks.values() if r['trend']=='downtrend')} / "
        f"choppy: {sum(1 for r in stocks.values() if 'choppy' in r['trend'])}")
    add("")

    if snap.get("quality_flags"):
        add("## Data quality flags — do not quote these without a second source")
        for f in snap["quality_flags"]:
            add(f"- {f}")
        add("")
    if snap.get("missing"):
        add(f"Missing tickers: {', '.join(snap['missing'])}")

    text = "\n".join(L)
    if args.write:
        out = ROOT / "journal" / f"{stamp}-{args.market}-data.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(f"wrote {out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
