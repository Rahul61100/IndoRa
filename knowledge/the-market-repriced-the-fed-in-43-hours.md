---
title: "Six Fed contracts repriced the same way in 43 hours"
market: us
type: finding
confidence: high
tags: [us, finding, high]
updated: 2026-08-29
---

# Six Fed contracts repriced the same way in 43 hours

First read of the prediction-market odds log as a **series** rather than a snapshot, comparing
2026-08-27 17:53 against 2026-08-29 12:23 across 1,016 liquid markets. It immediately produced
something the news-based collection could not.

## The Fed is being repriced toward a hike, coherently

| contract | 27 Aug | 29 Aug | move | liquidity |
|---|---|---|---|---|
| Fed rate hike by **October** meeting | 0.445 | **0.595** | **+15.0** | $62k |
| Fed rate hike by **September** meeting | 0.305 | **0.445** | **+14.0** | $78k |
| **No change** after September | 0.675 | **0.545** | **−13.0** | $370k |
| Fed **+25bp** after September | 0.305 | **0.435** | **+13.0** | $372k |
| Fed **+25bp** (second contract) | 0.355 | **0.470** | **+11.5** | $81k |
| Fed rate hike **in 2026** | 0.565 | **0.665** | **+10.0** | $106k |

**Six independent contracts, all moving the same direction, inside 43 hours.** The two largest by
liquidity ($370k and $372k) move in exact opposition to each other, which is what internal
consistency looks like. This is not noise.

## It settles yesterday's contradiction

The 28 August collection surfaced two irreconcilable readings: a CME FedWatch snapshot showing
**0% probability of a hike**, against press framing of Warsh's Jackson Hole speech as hawkish enough
to sell gold off more than 3%.

The odds log resolves it. **The market is at ~44.5% for a September hike, up from 30.5%.** The
hawkishness is in the price. The "0% priced" reading was wrong, stale, or misread — and the way to
find that out was not to search harder, it was to **hold the price series ourselves.**

That is the argument for collecting rather than querying: a number someone reports to you is a
claim, and a number you recorded twice is a measurement.

## It confirms a held view, which is rarer than a correction

This base holds that [[rate-cut-cycle-is-over|the rate-cut cycle is over]] and that the next Fed
move is as likely to be a hike as a cut — a contrarian read grounded in five holds and three
dissents wanting a *hike*. The market has now moved decisively toward it.

Recording this deliberately: almost every finding in this workspace has been a correction against
itself. This one is confirmation, and confirmation deserves the same scepticism — **a view that
gets confirmed by price is still only a view that has not been tested by an outcome.** The
September FOMC is the test.

## Second cluster: the Iran blockade is being priced to last

Every "blockade ends by X" contract fell, across every tenor:

**Sep 7:** 0.115 → 0.045 · **Sep 14:** 0.195 → 0.095 · **Sep 21:** 0.245 → 0.150
**Sep 30:** 0.300 → 0.235 · **Oct 31:** 0.510 → 0.415 · **Dec 31:** 0.706 → 0.664

Hormuz-normalisation odds fell with them. The market is pricing the disruption as **more
persistent**, not less.

That matters here specifically. This base established that Indian equities *rise* with oil
unconditionally and that **only supply shocks hurt** — the Nifty fell in all four large supply
shocks of the last decade. A lengthening blockade is a supply story.

**And it sits against the price:** WTI *fell* 3.95% last week. Rising blockade-persistence odds
alongside falling crude is a genuine tension, not a confirmation. Either the market thinks the
blockade no longer constrains supply, or one of the two is wrong. **Unresolved, and worth chasing.**

## Third: Russia-Ukraine peace odds fell

Peace talks by 31 December: **0.615 → 0.495 (−12pts).** Peace receding keeps the Senate sanctions
bill — 100% tariffs on buyers of Russian energy, India named, Russia >50% of India's crude — live
rather than fading.

## Method note

`scripts/odds_moves.py` filters to topics this base holds sourced claims on, with negative filters,
because `india`→*Indiana* and `rbi`→*runs batted in* have both bitten this workspace already. Of 89
markets that moved ≥2 points, **39 were on a watched topic** — the rest are noise we hold no view on
and should not narrate.

**Source:** own computation from two Polymarket snapshots recorded by `scripts/predict_ingest.py`.
Prices are **verified** in the sense that they are what the venue published and we stored; the
*interpretation* is reasoned.

Related: [[rate-cut-cycle-is-over]] · [[the-hedge-i-was-planning-is-not-purchasable]] · [[not-found-is-not-the-same-as-false]]
