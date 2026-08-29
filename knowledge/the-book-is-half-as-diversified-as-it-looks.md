---
title: "Ten positions, 5.4 effective bets — and I never checked before opening them"
market: general
type: position
confidence: reported
tags: [general, position, reported]
updated: 2026-08-29
---

# Ten positions, 5.4 effective bets — and I never checked before opening them

**Computed 2026-08-26** by `scripts/portfolio_risk.py`, from two years of daily returns.

- positions in the book: **10**
- average pairwise correlation: **0.28**
- **effective number of bets: 5.41** (participation ratio of the correlation-matrix eigenvalues —
  equals N when holdings are independent, 1 when they are a single factor)

So the book carries roughly **half the diversification the position count implies**. Not a
disaster, but the count was never the right measure and I had not looked.

Per-holding risk against the Nifty:

| Holding | Beta | Ann vol % | Max DD % | Corr | 2y ann return % |
|---|---|---|---|---|---|
| ICICI Bank | 0.99 | 18.1 | -18.4 | 0.66 | +9.5 |
| Bharti Airtel | 0.89 | 20.9 | -18.8 | 0.51 | +13.4 |
| HAL | 1.03 | **29.8** | **-36.0** | 0.41 | +1.7 |
| SBI | 0.97 | 20.3 | -22.1 | 0.57 | +15.9 |
| **Dixon** | **1.46** | **39.1** | **-48.9** | 0.45 | +5.0 |
| HDFC Bank | 1.01 | 17.5 | -27.8 | 0.69 | **-4.4** |
| NTPC | 0.81 | 21.2 | -32.3 | 0.46 | **-8.4** |
| Reliance | 1.01 | 18.9 | -23.9 | 0.64 | **-7.0** |
| L&T | 1.30 | 23.8 | -24.3 | 0.65 | +6.3 |
| Infosys | 0.95 | 27.7 | **-48.2** | 0.42 | **-20.4** |

**Three things fall out that the thesis notes never mentioned:**

1. **The entire LONG bucket has lost money over two years** — NTPC -8.4% and Reliance -7.0%
   annualised, with HDFC Bank at -4.4%. Every one is a "cheap, structural, decades" thesis. They
   are cheap because they have been falling for two years, which is the honest version of the
   entry case.
2. **Dixon is not a half position on valuation grounds, it is a half position on volatility
   grounds** — 39.1% annualised vol and a 48.9% historical drawdown, beta 1.46. Sizing it like a
   normal holding would have made it the dominant contributor to book risk. It is now capped for
   a *different* reason too ([[memory-shortage-is-a-tax-on-device-makers]]).
3. **HAL carries 29.8% vol and a 36% drawdown**, which is a lot for a position entered on trend
   with a stop. The stop distance has to respect the volatility, not a round number.

**How to apply:** run `portfolio_risk.py` before opening or sizing anything, not after. Size on
**risk contribution**, not on rupees. And if the effective-bets number falls much below half the
position count, the book has quietly become one macro wager wearing many tickers — most likely
"domestic Indian cyclical recovery", which is exactly what three banks plus capital goods plus
telecom is.
