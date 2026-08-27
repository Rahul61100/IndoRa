---
title: "The first-principles agent caught four errors I made — and it never searched once"
market: general
type: finding
confidence: verified
tags: [general, finding, verified]
updated: 2026-08-27
---

# The first-principles agent caught four errors I made — and it never searched once

**Computed and verified 2026-08-27.** The Falsifier archetype has not reported yet; this is the
**First-Principles Reasoner**, deliberately forbidden from searching. It used **zero tools** and
reasoned only from facts supplied. It was more rigorous than I was.

## 1. Duration mismatch — I used the wrong risk-free rate

I benchmarked a **five-year** equity horizon against the **ten-year** G-sec at 6.85%. The correct
comparator is the five-year yield.

| Benchmark | After-tax hurdle (₹2-5cr band) | ERP after tax |
|---|---|---|
| 10y at 6.85% — what I used | 4.91% | **−0.02%** |
| **5y at 6.65% — duration-matched** | **4.77%** | **+0.12%** |

**Duration-matched, the after-tax equity risk premium is positive at the ₹2-5cr band, not
break-even.** Small, but it moves the sign again — the second time in one day that a framing error,
not new information, changed the answer.

*(The 5y figure of 6.65% is from May 2026 and stale — flagged.)*

## 2. I have been double-counting the domestic bid

I have repeatedly cited **SIP inflows of ~₹31,961 crore a month** and a **25-month DII buying
streak worth ₹11.4 trillion** as though they were two separate supports.

**SIP flows go into mutual funds. Mutual funds are a DII subcategory. The SIP number is almost
certainly already inside the DII number.**

| | Annualised |
|---|---|
| SIP | ₹3.84 lakh crore |
| **DII (the encompassing figure)** | **₹5.47 lakh crore** |
| Named visible supply | ₹11.78 lakh crore |

**Absorption at the DII run-rate: 2.15 years.** Had I added SIP and DII together — which my framing
implied — I would have computed 1.27 years and **understated the supply problem by 40%.**

**And the deeper point the agent made: this is a stock-flow problem at each moment, not a
cumulative one.** If the ₹4.72 trillion pipeline and the $32bn PE overhang land front-loaded rather
than spread across two years, price concessions are required regardless of the eventual total.
**Pacing is unknown and the conclusion is acutely sensitive to it.**

## 3. My FII futures reading is weaker than I stated

I wrote that FIIs being short the index and long single stocks is "a dispersion trade, not a
directional view" and treated it as established
([[fii-are-short-the-index-long-the-stocks]]).

**The agent correctly flags this as the weakest inference in the chain.** A short index future may
equally be a **beta hedge over a large unstated cash-equity long book** — "long stocks,
beta-neutral overall" rather than "bearish India." **Derivatives positioning alone cannot
distinguish these.** Resolving it needs the FII net cash-equity position for the same period, which
I do not have.

The balance of evidence still leans my way — FII ownership at a 14-year low and the worst outflows
since 1993 suggest genuine beta reduction — **but that is two facts stacked into an inference, not
a proof, and I presented it as more certain than it is.**

## 4. The index-versus-breadth puzzle has two explanations and I assumed one

Index FY27 EPS was cut ~9% over twelve months while **58% of stocks carry net upgrades today**.
Both are true, which requires that revisions are **not uniformly distributed**. Two mechanisms:

**(a) Weight, not count.** A few heavy-weight names carry large downgrades while many smaller names
carry upgrades. Strongly supported by two facts already in the base: **60% of Q1 FY27's incremental
profit came from five companies**, and **the Nifty 50's share of Nifty 500 profit fell from 87% in
FY18 to 51% in FY26.**

**(b) Timing.** The −9% is a trailing twelve-month cumulative; the 58% is today's snapshot. The
index estimate was also revised **up 0.6%** after Q1 — so the aggregate may simply be lagging a
turn the breadth reading has already caught.

**I assumed (b), the optimistic reading, without noting (a) exists.** They cannot be distinguished
without **a time series of breadth**, which is precisely why `fetch_revisions.py` must run daily —
today's snapshot is one point; the answer needs the series.

## The load-bearing conclusion, restated properly

At the only defensible earnings assumption — **the realised ~4%, not the 12-15% that has missed
nine years running** — clearing the hurdle requires **either** earnings breaking a nine-year
pattern **or** the multiple re-rating without earnings accelerating.

**Multiple expansion historically follows delivered growth rather than substituting for its
absence.** So the bull case asks for a re-rating on faith. That is possible — the Nifty trades
12.6% below its own ten-year average — but it is a distinct and separately fragile assumption from
"earnings deliver," and I had been treating the two as one.

## Why this archetype earned its place

**Search returns what has been written. First-principles reasoning returns what follows.** Four
corrections, three of them to arithmetic or framing I had already committed to, from an agent that
consumed no search budget at all.

**It should run on every question that matters, and it costs nothing.**
Related: [[india-erp-after-tax-is-roughly-zero]], [[multi-agent-research]] in `playbooks/`.
