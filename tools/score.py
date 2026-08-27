# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas"]
# ///
"""
Score the open book against its own written invalidation conditions.

    uv run tools/score.py            # today's check
    uv run tools/score.py --history  # the running scorecard

This is Phase D of BUILD.md — the gate on everything else. Until roughly 30 theses have
been scored FORWARD to their horizon, this workspace has no evidence of skill, and any
backward-looking number that flatters it is measuring hindsight.

The design rule that makes it work: **a thesis whose invalidation cannot be mechanised is
a thesis whose invalidation will never actually be checked.** Conditions that genuinely
need judgement are typed `manual` and surfaced for review rather than silently decided —
but they are surfaced every single day, which is the part a human memory fails at.

Reads positions/theses.json and the latest data/daily and data/revisions snapshots.
Appends to data/scorecard.json.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(p: Path, default=None):
    return json.loads(p.read_text()) if p.exists() else default


def benchmarks() -> dict:
    """Nifty and the alternative, so a position is scored against what else the money could do.

    Added 2026-08-27 after establishing that S&P-in-INR beat the Nifty in 97% of rolling
    ten-year windows. Absolute P&L on an India book is the wrong yardstick when the passive
    alternative compounds ~4.5pp a year faster in the same currency."""
    import yfinance as yf
    out = {}
    try:
        px = yf.download(["^NSEI", "^GSPC", "INR=X"], period="6mo", interval="1d",
                         progress=False, auto_adjust=True)["Close"].ffill().dropna()
        out["nifty"] = px["^NSEI"]
        out["spx_inr"] = px["^GSPC"] * px["INR=X"]
    except Exception:
        pass
    return out


def bench_return(series, since: str) -> float | None:
    if series is None or len(series) == 0:
        return None
    s = series[series.index >= since]
    if len(s) < 2:
        return None
    return (float(s.iloc[-1]) / float(s.iloc[0]) - 1) * 100


def market_state() -> tuple[dict, dict]:
    snap = load_json(ROOT / "data" / "daily" / "india" / "latest.json", {}) or {}
    px = {s: r for g in snap.get("groups", {}).values() for s, r in g.items()}
    revs_hist = load_json(ROOT / "data" / "revisions" / "india.json", {}) or {}
    latest = list(revs_hist.values())[-1] if revs_hist else []
    revs = {r["symbol"]: r for r in latest}
    return px, revs


def evaluate(th: dict, px: dict, revs: dict, fund: dict) -> list[dict]:
    sym = th["symbol"]
    p, rv = px.get(sym), revs.get(sym)
    out = []
    for cond in th.get("invalidation", []):
        c, res, detail = cond["check"], "no_data", ""
        if c in ("price_below", "price_above") and p:
            hit = p["price"] < cond["level"] if c == "price_below" else p["price"] > cond["level"]
            res, detail = ("TRIGGERED" if hit else "ok"), f"{p['price']:,.1f} vs {cond['level']:,.1f}"
        elif c == "below_sma" and p:
            sma = p["vs_sma_pct"].get(f"sma{cond['sma']}")
            if sma is not None:
                res, detail = ("TRIGGERED" if sma < 0 else "ok"), f"{sma:+.1f}% vs {cond['sma']}DMA"
        elif c in ("diffusion_below", "diffusion_above") and rv:
            d = rv.get("fy1_diffusion")
            if d is not None:
                hit = d < cond["level"] if c == "diffusion_below" else d > cond["level"]
                res, detail = ("TRIGGERED" if hit else "ok"), f"diffusion {d:+.2f} vs {cond['level']:+.2f}"
        elif c == "date_passed":
            hit = f"{date.today():%Y-%m-%d}" > cond["date"]
            res, detail = ("TRIGGERED" if hit else "ok"), f"deadline {cond['date']}"
        elif c == "margin_below" and (fd := fund.get(sym)):
            m = fd.get("operating_margin_pct")
            if m is not None:
                res, detail = ("TRIGGERED" if m < cond["level"] else "ok"), f"op margin {m:.2f}% vs {cond['level']:.2f}%"
        elif c == "manual":
            res, detail = "REVIEW", "needs judgement"
        out.append({"check": c, "result": res, "detail": detail, "note": cond.get("note", "")})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", action="store_true")
    args = ap.parse_args()

    reg = load_json(ROOT / "positions" / "theses.json")
    px, revs = market_state()
    fund = load_json(ROOT / "data" / "fundamentals" / "india.json", {}) or {}
    today = f"{date.today():%Y-%m-%d}"

    bm = benchmarks()

    print("=" * 88)
    print(f"BOOK SCORECARD — {today}")
    print("=" * 88)

    entry = {"date": today, "positions": []}
    triggered, review = [], []

    for th in reg["theses"]:
        sym, p = th["symbol"], px.get(th["symbol"])
        pnl = ((p["price"] / th["entry_price"] - 1) * 100) if p and th.get("entry_price") else None
        conds = evaluate(th, px, revs, fund)
        trig = [c for c in conds if c["result"] == "TRIGGERED"]
        man = [c for c in conds if c["result"] == "REVIEW"]
        flag = "  *** INVALIDATION TRIGGERED ***" if trig else ""
        nb = bench_return(bm.get("nifty"), th["opened"])
        sb = bench_return(bm.get("spx_inr"), th["opened"])
        alpha = ""
        if pnl is not None and nb is not None and sb is not None:
            alpha = (f"   vs Nifty {pnl-nb:+.1f}pp   vs S&P-in-INR {pnl-sb:+.1f}pp")
        print(f"\n{th['id']:<24}{th['horizon']:<8}{th['status']:<18}"
              f"{(f'{pnl:+.1f}%' if pnl is not None else '—'):>9} since entry{flag}")
        if alpha:
            print(f"{'':24}{alpha}")
        for c in conds:
            mark = {"TRIGGERED": "!!", "REVIEW": "??", "ok": "  ", "no_data": " ?"}[c["result"]]
            print(f"    {mark} {c['result']:<10}{c['detail']:<28}{c['note'][:44]}")
        if trig:
            triggered.append(th["id"])
        if man:
            review.append((th["id"], [c["note"] for c in man]))
        entry["positions"].append({"id": th["id"], "pnl_pct": round(pnl, 2) if pnl is not None else None,
                                   "status": th["status"], "triggered": [c["note"] for c in trig]})

    print("\n" + "=" * 88)
    if triggered:
        print(f"ACT: {len(triggered)} thesis/theses have hit a written invalidation — {', '.join(triggered)}")
    else:
        print("No written invalidation triggered today.")
    print(f"\nMANUAL REVIEW REQUIRED ({len(review)}) — these do not decide themselves:")
    for tid, notes in review:
        for n in notes:
            print(f"  ?? {tid}: {n}")

    closed = reg.get("closed", [])
    print("\n" + "=" * 88)
    print(f"CLOSED: {len(closed)} — the only honest evidence this process produces")
    for c in closed:
        move = ((c["exit_price"] / c["entry_price"] - 1) * 100) if c.get("exit_price") else 0
        held = (date.fromisoformat(c["closed"]) - date.fromisoformat(c["opened"])).days
        print(f"  {c['id']:<20}{move:+6.1f}%  held {held}d   {c['reason'][:52]}")
        print(f"  {'':20}LESSON: {c['lesson'][:70]}")

    n_open, n_closed = len(reg["theses"]), len(closed)
    print("\n" + "=" * 88)
    print(f"CALIBRATION GATE: {n_closed} scored, 30 needed. "
          f"{n_open} open, none yet held to horizon.")
    print("Until that gate is passed this workspace has NO EVIDENCE OF SKILL.")
    print("Every close so far was a research correction, not a market outcome — which measures")
    print("the research process, not the investment process. Those are different things.")
    if bm.get("nifty") is not None and bm.get("spx_inr") is not None:
        opened = min((t["opened"] for t in reg["theses"]), default=None)
        if opened:
            nb, sb = bench_return(bm["nifty"], opened), bench_return(bm["spx_inr"], opened)
            if nb is not None and sb is not None:
                print(f"\nSince the book opened ({opened}): Nifty {nb:+.2f}%, "
                      f"S&P-in-INR {sb:+.2f}%.")
                print("The second number is the hurdle. Beating the Nifty is not the job —")
                print("the passive alternative beat it in 97% of rolling ten-year windows.")

    ledger_p = ROOT / "data" / "scorecard.json"
    ledger = load_json(ledger_p, []) or []
    ledger = [e for e in ledger if e["date"] != today] + [entry]
    ledger_p.write_text(json.dumps(sorted(ledger, key=lambda e: e["date"]), indent=1))

    if args.history and len(ledger) > 1:
        print("\n" + "=" * 88)
        print("HISTORY")
        for e in ledger[-15:]:
            hits = sum(len(p["triggered"]) for p in e["positions"])
            print(f"  {e['date']}  {len(e['positions'])} positions, {hits} invalidations triggered")


if __name__ == "__main__":
    main()
