---
title: "A backtest of names you already picked measures hindsight, not process"
market: general
type: method
confidence: verified
tags: [general, method, verified]
updated: 2026-08-27
---

# A backtest of names you already picked measures hindsight, not process

Method rule, written 2026-08-26 the moment the stress test produced a flattering number.

`scripts/regime.py` reports that the current eight-name Indian book, equal-weighted and
daily-rebalanced, would have returned **+11.8% over two years against the Nifty's -1.9%.**

**That number is worthless as evidence and must never be quoted as a result.** The names were
selected on 2026-08-25 and 2026-08-26 with full visibility of their two-year price history. The
"backtest" is measuring my knowledge of the past, not the quality of the process. Any set of
names chosen today will look good against the index over a window that ended today.

**What in that output IS meaningful**, because it describes co-movement rather than selection:

| Measure | Book | Nifty |
|---|---|---|
| Max drawdown | -15.1% | -15.8% |
| Annualised vol | **15.8%** | 13.1% |
| Downside capture | **104%** | — |
| Upside capture | **113%** | — |

The book is higher-beta in both directions — it falls slightly more than the index on down days
and rises more on up days. That is a genuine property of what is held and is worth knowing.

**How to apply:** the only honest test of this process is **forward** — theses scored from the
date they were opened, which is what `positions/open-theses.md` exists for and what Phase 3 of
[`roadmap`](../playbooks/roadmap.md) gates on. Until roughly 30 theses have been scored forward,
this workspace has **no evidence of skill at all**, and any backward-looking number that suggests
otherwise is a trap. Related: [[verify-prices-from-the-snapshot]].
