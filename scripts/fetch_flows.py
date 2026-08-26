# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "pandas"]
# ///
"""
Flow collection — the variable that has explained more than any valuation metric.

Sources, all public and unauthenticated:
  India   NSE fiidiiTradeReact  -> daily FII/FPI and DII cash-segment net, in INR crore
  Crypto  DefiLlama stablecoins -> total stablecoin circulating supply, daily
  Crypto  DefiLlama TVL         -> total DeFi TVL, daily

Writes an append-only ledger per source under data/flows/ so history accumulates even
though NSE only ever serves the latest two rows.

    uv run scripts/fetch_flows.py

US fund flows are NOT covered -- no free daily source found. Logged in the roadmap as an
open Phase 1 item; do not silently treat US flows as zero.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
FLOWDIR = ROOT / "data" / "flows"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def _merge(path: Path, rows: list[dict], key: str) -> int:
    """Append-only merge keyed on `key`. Returns count of genuinely new rows."""
    existing = json.loads(path.read_text()) if path.exists() else []
    seen = {r[key] for r in existing}
    fresh = [r for r in rows if r[key] not in seen]
    if fresh:
        combined = sorted(existing + fresh, key=lambda r: r[key])
        path.write_text(json.dumps(combined, indent=1))
    return len(fresh)


def india_fii_dii() -> int:
    """NSE serves only the latest session, so this must run daily to build history."""
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "application/json"})
    try:
        s.get("https://www.nseindia.com", timeout=15)  # cookie handshake
    except requests.RequestException:
        pass
    r = s.get("https://www.nseindia.com/api/fiidiiTradeReact", timeout=20)
    r.raise_for_status()
    data = r.json()

    by_date: dict[str, dict] = {}
    for row in data:
        d = datetime.strptime(row["date"], "%d-%b-%Y").strftime("%Y-%m-%d")
        rec = by_date.setdefault(d, {"date": d, "unit": "INR_crore"})
        tag = "fii" if "FII" in row["category"].upper() else "dii"
        rec[f"{tag}_buy"] = float(row["buyValue"])
        rec[f"{tag}_sell"] = float(row["sellValue"])
        rec[f"{tag}_net"] = float(row["netValue"])
    return _merge(FLOWDIR / "india_fii_dii.json", list(by_date.values()), "date")


def stablecoin_supply() -> int:
    r = requests.get("https://stablecoins.llama.fi/stablecoincharts/all", timeout=45)
    r.raise_for_status()
    rows = []
    for pt in r.json():
        usd = (pt.get("totalCirculatingUSD") or {}).get("peggedUSD")
        if usd is None:
            continue
        rows.append({
            "date": datetime.fromtimestamp(int(pt["date"]), tz=timezone.utc).strftime("%Y-%m-%d"),
            # DefiLlama serves raw USD; store millions so the series is readable.
            "total_supply_usd_mn": round(float(usd) / 1e6, 1),
        })
    return _merge(FLOWDIR / "stablecoin_supply.json", rows, "date")


def defi_tvl() -> int:
    r = requests.get("https://api.llama.fi/v2/historicalChainTvl", timeout=45)
    r.raise_for_status()
    rows = [{
        "date": datetime.fromtimestamp(int(pt["date"]), tz=timezone.utc).strftime("%Y-%m-%d"),
        "tvl_usd_mn": round(float(pt["tvl"]) / 1e6, 1),
    } for pt in r.json() if pt.get("tvl")]
    return _merge(FLOWDIR / "defi_tvl.json", rows, "date")


def summarise() -> None:
    """Print the read that matters: recent net flow and its rolling context."""
    p = FLOWDIR / "india_fii_dii.json"
    if p.exists():
        rows = json.loads(p.read_text())[-10:]
        print("\nIndia cash-segment net, INR crore (positive = buying):")
        print(f"  {'date':<12}{'FII':>12}{'DII':>12}{'combined':>12}")
        for r in rows:
            f, d = r.get("fii_net"), r.get("dii_net")
            if f is None or d is None:
                continue
            print(f"  {r['date']:<12}{f:>12,.0f}{d:>12,.0f}{f + d:>12,.0f}")

    for name, field, label in (("stablecoin_supply.json", "total_supply_usd_mn", "Stablecoin supply"),
                               ("defi_tvl.json", "tvl_usd_mn", "DeFi TVL")):
        p = FLOWDIR / name
        if not p.exists():
            continue
        rows = json.loads(p.read_text())
        if len(rows) < 200:
            continue
        cur = rows[-1][field]
        d30 = (cur / rows[-31][field] - 1) * 100
        d90 = (cur / rows[-91][field] - 1) * 100
        d365 = (cur / rows[-366][field] - 1) * 100 if len(rows) > 366 else float("nan")
        print(f"\n{label}: ${cur/1e3:,.1f}bn   30d {d30:+.1f}%   90d {d90:+.1f}%   1y {d365:+.1f}%")


def main() -> int:
    FLOWDIR.mkdir(parents=True, exist_ok=True)
    for label, fn in (("india_fii_dii", india_fii_dii),
                      ("stablecoin_supply", stablecoin_supply),
                      ("defi_tvl", defi_tvl)):
        try:
            n = fn()
            print(f"{label}: +{n} new rows")
        except Exception as e:
            # A failed source must be loud. A silently missing flow series reads as zero flow.
            print(f"{label}: FAILED — {type(e).__name__}: {e}")
    summarise()
    return 0


if __name__ == "__main__":
    sys.exit(main())
