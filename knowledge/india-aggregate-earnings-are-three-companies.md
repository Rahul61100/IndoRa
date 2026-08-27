---
title: "India's aggregate earnings number is mostly three companies"
market: india
type: finding
confidence: verified
tags: [india, finding, verified]
updated: 2026-08-27
---

# India's aggregate earnings number is mostly three companies

Ran an earnings-quality screen across 62 large Indian names, latest quarter against the same
quarter a year earlier. The revenue-weighted aggregate says:

> revenue **+20.6%**, operating income **+1.6%**, operating margin **13.13% → 11.06%**, −207 bps

That is a headline that writes itself: *volume growth with no profit growth, a margin collapse
across corporate India.* It is also wrong, and I nearly published it.

Drop **three** names — IOC, BPCL and Tata Motors PV, all of which went operationally
loss-making — and the same 59 companies show:

> revenue **+17.7%**, operating income **+15.4%**, operating margin **15.94% → 15.62%**, −32 bps

The median company grew revenue **+17.9%** and operating income **+20.3%**. Breadth is
**44 of 62 (71%)** growing operating income year on year.

## Why the aggregate lies

Revenue-weighting an Indian large-cap sample hands the answer to the oil marketers, because
they book enormous revenue at near-zero margin:

| | revenue | share of sample | operating margin |
|---|---|---|---|
| Reliance | ₹309,468cr | 15.8% | 10.48% |
| **IOC** | ₹266,407cr | 13.6% | **−0.10%** |
| **BPCL** | ₹151,277cr | 7.7% | **−4.05%** |
| **TMPV** | ₹104,923cr | 5.3% | **−1.31%** |
| Hindalco | ₹84,825cr | 4.3% | 13.72% |
| | | **46.7% cumulative** | |

The three loss-makers are **26.6% of sample revenue** and posted a combined operating loss of
**₹7,776cr**. A revenue-weighted margin is therefore not a statement about Indian corporate
profitability — it is a statement about refining and marketing spreads, wearing the costume of one.

## This is the same error I already made, pointing the other way

Earlier in this workstream I reported "earnings +18%" and later had to correct it: that was one
quarter with **60% of the growth from five stocks**. The bearish aggregate above is the identical
defect with the sign reversed — a handful of names driving a number presented as economy-wide.
Catching it in the bullish direction and then walking into it in the bearish direction would have
meant learning nothing.

**Rule, now standing: never report an Indian aggregate without also reporting the median and the
breadth.** If the three disagree, the aggregate is the one to discard. `scripts/fetch_fundamentals.py`
prints all three.

## What is actually true

Corporate India's *operating* performance in the most recent quarter looks **fine** — median
operating income +20.3%, 71% breadth. The damage is concentrated in **energy marketing and one
auto maker**, and the plausible mechanism is inventory losses on a falling crude price (Brent is
~27% below its high), not demand weakness.

That sits awkwardly against the **FY26 full-year 4.5% growth** figure this workspace relies on, and
the two are not directly comparable: one is a full year of net income on the Nifty, the other is one
quarter of operating income on a 62-name large-cap sample. **Do not net them against each other.**
The honest position is that the quarterly operating trend is better than the annual net trend, and
the gap between those two facts — below-the-line items, interest, tax, and the index-reconstitution
effect — is the thing still unexplained.

## Second-order

If the OMC losses are inventory-driven, they **reverse** when crude stabilises, which means the
aggregate margin recovers without anything improving in the real economy. Anyone reading the next
quarter's aggregate as a recovery signal will be making the mirror error again.

Related: [[dixon-profit-is-not-operating]] · [[india-diversification-concentrated-on-washington]]
