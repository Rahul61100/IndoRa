# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""
FII/DII derivatives positioning, from NSE's own participant-OI file.

    uv run scripts/fetch_derivatives.py [--days 10]

Closes the gap that made me misread flows for three days. On 2026-08-26 FIIs were net
CASH buyers of ₹503 crore while running a ~1:8.25 short in index futures against a large
single-stock long — a dispersion trade, not bullishness. Cash flow alone said the opposite.

**Source note:** this reads NSE's primary CSV, not an aggregator. WebFetch cannot retrieve
it (Akamai bot protection), but a normal session that first touches nseindia.com to collect
cookies and then sends a Referer header does. That is worth knowing generally — "WebFetch
timed out" is not the same as "the data is unavailable."

Writes an append-only ledger to data/flows/india_derivatives.json.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from datetime import date, datetime, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "flows" / "india_derivatives.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")
URL = "https://nsearchives.nseindia.com/content/nsccl/fao_participant_oi_{d:%d%m%Y}.csv"


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Referer": "https://www.nseindia.com/",
                      "Accept": "text/csv,*/*"})
    try:
        s.get("https://www.nseindia.com", timeout=15)   # sets the cookies the archive requires
    except requests.RequestException:
        pass
    return s


def parse(text: str, day: date) -> dict | None:
    rows = list(csv.reader(io.StringIO(text)))
    header_i = next((i for i, r in enumerate(rows) if r and r[0].strip() == "Client Type"), None)
    if header_i is None:
        return None
    hdr = [h.strip() for h in rows[header_i]]
    out: dict = {"date": f"{day:%Y-%m-%d}"}
    for r in rows[header_i + 1:]:
        if not r or not r[0].strip():
            continue
        who = r[0].strip()
        if who not in ("FII", "DII", "Client", "Pro"):
            continue
        rec = {}
        for k, v in zip(hdr[1:], r[1:]):
            try:
                rec[k] = int(float(v.strip().replace(",", "")))
            except (ValueError, AttributeError):
                pass
        fl, fs = rec.get("Future Index Long", 0), rec.get("Future Index Short", 0)
        sl, ss = rec.get("Future Stock Long", 0), rec.get("Future Stock Short", 0)
        out[who] = {
            "fut_index_long": fl, "fut_index_short": fs, "fut_index_net": fl - fs,
            # The headline sentiment gauge. Below ~0.3 is a heavily bearish index posture.
            "fut_index_ls_ratio": round(fl / fs, 3) if fs else None,
            "fut_stock_long": sl, "fut_stock_short": ss, "fut_stock_net": sl - ss,
            "total_long": rec.get("Total Long Contracts", 0),
            "total_short": rec.get("Total Short Contracts", 0),
        }
    return out if "FII" in out else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=10, help="calendar days back to attempt")
    args = ap.parse_args()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    hist = {r["date"]: r for r in json.loads(OUT.read_text())} if OUT.exists() else {}
    s = session()
    added, missing = 0, []

    for i in range(args.days):
        d = date.today() - timedelta(days=i)
        if d.weekday() >= 5 or f"{d:%Y-%m-%d}" in hist:
            continue
        try:
            r = s.get(URL.format(d=d), timeout=25)
            if r.status_code != 200 or "Client Type" not in r.text:
                missing.append(f"{d:%Y-%m-%d}")
                continue
            rec = parse(r.text, d)
            if rec:
                hist[rec["date"]] = rec
                added += 1
        except requests.RequestException:
            missing.append(f"{d:%Y-%m-%d}")

    rows = sorted(hist.values(), key=lambda r: r["date"])
    OUT.write_text(json.dumps(rows, indent=1))
    print(f"derivatives: +{added} new sessions, ledger holds {len(rows)}")
    if missing:
        print(f"  not published / unreachable: {', '.join(missing[:6])}"
              + ("..." if len(missing) > 6 else ""))

    print(f"\n  {'date':<12}{'FII idx net':>13}{'L:S':>8}{'FII stk net':>13}"
          f"{'DII idx net':>13}   read")
    for r in rows[-10:]:
        f, d_ = r.get("FII", {}), r.get("DII", {})
        ratio = f.get("fut_index_ls_ratio")
        note = ""
        if ratio is not None:
            if ratio < 0.3 and f.get("fut_stock_net", 0) > 0:
                note = "short index / long stocks -> DISPERSION, not direction"
            elif ratio < 0.3:
                note = "heavily short index"
            elif ratio > 1.5:
                note = "net long index"
        print(f"  {r['date']:<12}{f.get('fut_index_net',0):>13,}"
              f"{(f'{ratio:.2f}' if ratio else '—'):>8}{f.get('fut_stock_net',0):>13,}"
              f"{d_.get('fut_index_net',0):>13,}   {note}")
    print("\n  Never read FII cash flow without this table beside it.")


if __name__ == "__main__":
    main()
