---
title: "Estimate revisions are now collected — and they settle three open calls"
market: general
type: regime
confidence: reported
tags: [general, regime, reported]
updated: 2026-08-29
---

# Estimate revisions are now collected — and they settle three open calls

Built 2026-08-27. **Confidence: verified** — derived from Yahoo's own analyst-estimate
endpoints, pulled this session.

This was the gap that cost the Infosys call and the "earnings +18%" error. Revision
**direction** has done more explanatory work in this loop than any valuation metric, and it was
not being collected at all. `scripts/fetch_revisions.py` now pulls, per ticker:

- **eps_trend** — consensus EPS now against 7, 30, 60 and 90 days ago → revision *magnitude*
- **eps_revisions** — analysts revising up vs down over 30 days → revision *breadth*
- a **diffusion index**: `(up − down) / (up + down)`, so +1 is all upgrades and −1 all downgrades
- consensus price target and implied upside

Yahoo serves only the current snapshot, so the ledger at `data/revisions/india.json` is
append-only and **the history only exists if this runs regularly.**

## The book, 27 August 2026

| Name | FY+1 EPS | 90d % | 30d % | up | dn | **diffusion** | target upside |
|---|---|---|---|---|---|---|---|
| Divi's Labs | 150.3 | +4.77 | +6.77 | 24 | **0** | **+1.00** | −8.4% |
| ICICI Bank | 94.0 | — | — | 28 | 4 | **+0.75** | **+20.0%** |
| Dixon | 281.6 | **+10.07** | +3.39 | 21 | 3 | **+0.75** | −1.2% |
| Shriram Finance | 71.8 | **+9.37** | +1.96 | 18 | 8 | +0.38 | +8.6% |
| HAL | 172.0 | +3.04 | +2.77 | 2 | 1 | +0.33 | +11.6% |
| NTPC | 24.9 | +1.41 | −0.95 | 5 | 3 | +0.25 | +31.7% |
| Bharti Airtel | 82.2 | −1.46 | +0.05 | 10 | 7 | +0.18 | +23.0% |
| TCS | 162.5 | −1.77 | +0.18 | 11 | 18 | −0.24 | +9.3% |
| L&T | 125.9 | +0.72 | +0.72 | 5 | 9 | −0.29 | +11.4% |
| **Reliance** | 28.1 | +2.55 | **−5.23** | 6 | 13 | **−0.37** | +29.7% |
| **HDFC Bank** | 62.6 | −4.35 | −2.42 | 7 | **23** | **−0.53** | **+41.9%** |
| **Infosys** | 79.9 | −2.51 | −0.03 | 4 | **30** | **−0.76** | +8.5% |

*(SBI returns no EPS estimate data from this source — a genuine collection gap.)*

## What it settles

**Infosys — bench confirmed, decisively.** 4 upgrades against **30 downgrades**, FY+1 EPS cut
2.51% over 90 days. I had been saying "revisions are still negative" from narrative. Now it is a
number, and it is worse than I implied. The entry condition remains a **turn in this figure**, not
a cheap multiple.

**HDFC Bank — the close is confirmed, and the signature is textbook.** 7 up against **23 down**,
EPS cut 4.35% over 90 days — **while the consensus target sits 41.9% above the price.** Falling
estimates plus a stale, far-above-market target is the classic value-trap signature, and it is
exactly what the separate governance research found independently
([[hdfc-bank-msrdc-governance-overhang]]).

**ICICI Bank — the short-horizon pick is fully corroborated.** 28 up against 4 down, and a
consensus target 20% above the price. Estimates and price agree, which is the opposite of HDFC
Bank.

## What it flags that I had not seen

**Reliance: FY+1 EPS cut 5.23% in thirty days, 6 upgrades against 13 downgrades.** That sits
directly against the promoter buying ~₹8,500-9,000 crore in July and lifting the stake to 50.48%
([[who-is-actually-buying-india]]).

**Insider buying and falling estimates at the same time is a genuine tension, not a confirmation.**
Either the promoter sees value the analysts do not, or the analysts are seeing near-term earnings
deterioration the promoter is choosing to look through. **Both readings are live and I cannot yet
distinguish them.** Open question, logged.

**Dixon and Divi's both have strong upgrade breadth but the price is already above the consensus
target** (−1.2% and −8.4% implied upside). Estimates rising into a price that has already run.
That is a better problem than the reverse, but it caps near-term upside.

## The universe reading

**39 of 67 names carry net upgrades — 58%.** Below ~40% would be a market being marked down;
58% is a market with a mildly positive revision cycle.

**That matters, because the index-level story was the opposite.** FY27 Nifty consensus EPS was cut
~9% over twelve months ([[CORRECTION-india-earnings-growth-was-4-5-percent]]), yet stock-level
breadth is now positive. It corroborates the separate finding that the upgrade/downgrade ratio
turned to 1.5x post-Q1, the strongest in 22 quarters.

**The revision cycle has turned at the stock level. It has not yet shown up in the index estimate.**
Watching whether that gap closes upward is now a tracked series rather than a guess.

## How to apply

Run it daily alongside flows. **A thesis on a name whose diffusion is below about −0.4 needs an
explicit reason why the analysts are wrong** — and "it is cheap" is not one, because a falling
numerator makes it cheaper on the way down.
