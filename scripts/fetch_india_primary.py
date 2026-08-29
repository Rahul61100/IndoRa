# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""Indian macro from the primary sources that are actually reachable.

    uv run scripts/fetch_india_primary.py

WHAT IS AND IS NOT BLOCKED — measured 2026-08-29, because the record here was muddled.

Reachable with an ordinary browser User-Agent (all HTTP 200):
    www.rbi.org.in · www.mospi.gov.in · eaindustry.nic.in · www.fbil.org.in
    www.nsdl.co.in · data.rbi.org.in
Genuinely blocked:
    rbidocs.rbi.org.in  -- the DOCUMENT host. Serves an Imperva/TSPD JavaScript
        challenge for every PDF/DOC, so the Bulletin's statistical tables
        (including Table 4A, the forward book) cannot be fetched without a
        browser that executes JS.
    www.cmegroup.com    -- 403.

So both of the competing stories in this repo's history were half right, and the
correction runs BOTH ways:

  - Several agent reports said "MOSPI/PIB/RBI/NSDL/FBIL are unreachable" and
    tiered everything downstream as `reported`. For the HTML pages that was
    wrong -- they answer fine, and this script pulls the live policy corridor
    straight off rbi.org.in.
  - But an agent on 2026-08-27 said specifically that "rbidocs.rbi.org.in is
    behind bot detection (TSPD JS challenge)". That was exactly right, and I
    nearly wrote a note accusing the agents of misdiagnosing it before hitting
    the same challenge myself.

The lesson worth keeping: "the site is blocked" and "this host is blocked" are
different claims, and collapsing them cost a real capability. The policy rates
below were retrievable the whole time.
"""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "india_primary.json"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")
HEADERS = {"User-Agent": UA,
           "Accept": "text/html,application/xhtml+xml,application/json,*/*",
           "Accept-Language": "en-US,en;q=0.9"}


def get(url: str, timeout: int = 30) -> tuple[int, str]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        return r.status_code, r.text
    except requests.RequestException as e:
        return 0, f"__ERROR__ {e}"


def text_of(h: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def policy_rates() -> dict:
    """RBI's own front page carries the live policy corridor."""
    code, h = get("https://www.rbi.org.in/")
    out = {"_status": code}
    if code != 200:
        return out
    t = text_of(h)
    for key, label in [("Policy Repo Rate", "repo"), ("Bank Rate", "bank_rate"),
                       ("CRR", "crr"), ("SLR", "slr"),
                       ("Standing Deposit Facility", "sdf"),
                       ("Marginal Standing Facility", "msf")]:
        m = re.search(rf"{key}\s*[:\-]?\s*([\d.]+)\s*%", t)
        if m:
            out[label] = float(m.group(1))
    return out


def reserves() -> dict:
    """Foreign exchange reserves from the Weekly Statistical Supplement page."""
    code, h = get("https://www.rbi.org.in/Scripts/WSSView.aspx")
    out = {"_status": code}
    if code != 200:
        return out
    t = re.sub(r"\s+", " ", text_of(h))
    # The WSS renders reserves in US$ million alongside a date reference.
    m = re.search(r"[Ff]oreign [Ee]xchange [Rr]eserves.{0,400}?([\d,]{6,})", t)
    if m:
        try:
            out["fx_reserves_usd_mn"] = int(m.group(1).replace(",", ""))
        except ValueError:
            pass
    d = re.search(r"(?:as on|week ended)\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4})", t)
    if d:
        out["as_on"] = d.group(1)
    out["_excerpt"] = t[:300]
    return out


def wpi() -> dict:
    """Wholesale Price Index — Office of the Economic Adviser."""
    code, h = get("https://eaindustry.nic.in/")
    out = {"_status": code}
    if code != 200:
        return out
    t = re.sub(r"\s+", " ", text_of(h))
    m = re.search(r"(?:annual rate of inflation|inflation).{0,120}?([\d.]+)\s*%", t, re.I)
    if m:
        out["headline_pct"] = float(m.group(1))
    d = re.search(r"([A-Z][a-z]+,?\s*20\d\d)", t)
    if d:
        out["period_hint"] = d.group(1)
    out["_excerpt"] = t[:300]
    return out


def mospi() -> dict:
    """MOSPI front page — IIP/CPI release pointers."""
    code, h = get("https://www.mospi.gov.in/")
    out = {"_status": code}
    if code != 200:
        return out
    t = re.sub(r"\s+", " ", text_of(h))
    heads = re.findall(r"(Index of Industrial Production[^|]{0,90}|"
                       r"Consumer Price Index[^|]{0,90})", t)
    out["headlines"] = list(dict.fromkeys(h.strip() for h in heads))[:6]
    return out


def main() -> None:
    today = f"{date.today():%Y-%m-%d}"
    snap = {"date": today,
            "policy_rates": policy_rates(),
            "reserves": reserves(),
            "wpi": wpi(),
            "mospi": mospi()}

    print(f"INDIA PRIMARY SOURCES — {today}")
    print("=" * 74)
    for name, blk in snap.items():
        if name == "date":
            continue
        st = blk.get("_status")
        mark = "ok " if st == 200 else "ERR"
        print(f"\n  [{mark}] {name}   HTTP {st}")
        for k, v in blk.items():
            if k.startswith("_"):
                continue
            print(f"        {k:<22}{v}")
        if st != 200:
            print(f"        NOT REACHABLE — record downstream figures as `reported`, not `verified`.")

    prev = json.loads(OUT.read_text()) if OUT.exists() else {}
    prev[today] = snap
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(prev, indent=1))
    print("\n" + "=" * 74)
    print(f"-> {OUT}")
    print("Anything captured here is PRIMARY and may be tiered `verified`.")


if __name__ == "__main__":
    main()
