---
title: "Yahoo's NSE sector indices have multi-week history gaps"
market: india
type: method
confidence: verified
tags: [india, method, verified]
updated: 2026-08-27
---

# Yahoo's NSE sector indices have multi-week history gaps

Verified 2026-08-26. Every `^CNX*` sector index pulled from Yahoo carried a **40-day hole** in
its daily history. The first print after the hole is rendered as a one-day change, producing
fake single-session moves: Nifty Auto appeared +7.0%, Metal +8.9%, Media +5.9%. Business
Standard put Nifty Auto's actual 25 Aug session at **+0.4%**.

`^CNXSC` and `^CNXFIN` fail entirely in a grouped download and only sometimes succeed solo.

**Why it matters:** a fabricated 7% sector move is exactly the kind of thing that looks like a
tradeable signal and generates a whole day of wrong analysis.

**How to apply:** never quote a `^CNX*` one-day or short-window move. Sector rotation comes from
`universe/sectors.json` constituent baskets, median member return. `scripts/fetch_daily.py` flags
history gaps over 10 days automatically. Related: [[corporate-actions-fake-price-history]],
[[verify-prices-from-the-snapshot]].
