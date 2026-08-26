---
title: "Regime labels: India SPLIT, US BROADENING, crypto SPLIT"
market: india
type: regime
confidence: verified
tags: [india, regime, verified]
updated: 2026-08-26
---

# Regime labels: India SPLIT, US BROADENING, crypto SPLIT

Produced by `scripts/regime.py`, 2026-08-26. The point of labelling is that **the correct
strategy is regime-dependent**, and re-deriving that judgement from scratch each day produces
inconsistent answers.

| Market | Label | Above 200 DMA | Above 50 DMA | Trend split | Median member 1y | Vol index |
|---|---|---|---|---|---|---|
| **India** | **SPLIT — index view near worthless, selection market** | 57% | 49% | 24 up / 23 down of 72 | **+1.6%** | VIX 10.56 |
| **US** | **BROADENING — index view works, leadership rotating** | 64% | 58% | 36 up / 17 down of 101 | **+9.6%** | VIX 15.49 |
| **Crypto** | **SPLIT — index view near worthless, selection market** | 58% | **74%** | 10 up / 6 down of 43 | **-22.0%** | — |

**What each label means for how to act:**

- **India SPLIT.** Half the market works and half does not, separated by sector rather than by
  size or valuation. Index targets are close to useless here; the return comes from sector and
  stock selection. **Stop leading notes with a Nifty level.**
- **US BROADENING.** Breadth is improving while the two-year leaders stall — the healthy version
  of a rotation, not a distribution top. An index view is worth holding, and the leadership
  question ("what is taking over from megacap AI") is the productive one.
- **Crypto SPLIT, and note the specific shape.** 74% above the 50 DMA but only 58% above the 200,
  with a **median member down 22% over a year**. That is a young recovery inside an unrepaired
  downtrend — short-term strength, no structural repair. Consistent with the rally being funded
  by imported ETF liquidity rather than native on-chain capital
  ([[stablecoin-supply-peaked-in-may]]).

**Also note India VIX at 10.56 against a 52-week range of 8.72-28.90.** A split, trendless market
priced for near-zero volatility. Hedges are cheap; nothing is being paid to compensate for the
lack of direction.

**How to apply:** run `regime.py` at the start of each loop and let the label set the frame before
looking at any individual name. Re-check the thresholds if a market sits at a boundary — they are
deliberately coarse, because false precision in a state label invites over-reading.
Related: [[breadth-is-split-not-trending]], [[us-leadership-rotated-to-value-health-smallcap]].
