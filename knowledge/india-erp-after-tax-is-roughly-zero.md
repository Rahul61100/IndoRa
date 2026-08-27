---
title: "The negative ERP is a pre-tax artifact — after tax it is roughly zero, and positive for high earners"
market: india
type: finding
confidence: verified
tags: [india, finding, verified]
updated: 2026-08-27
---

# The negative ERP is a pre-tax artifact — after tax it is roughly zero, and positive for high earners

**Computed 2026-08-27 from `scripts/required_return.py`. Confidence: verified — this is arithmetic
on figures already established, not new research.**

**This materially amends [[CORRECTION-india-erp-is-negative]], which I have quoted repeatedly and
which overstated the case.**

## The error

I have been saying India's equity risk premium is **−1.96%** — earnings yield 4.89% against a
6.85% G-sec — and treating it as decisive.

**That is a pre-tax comparison between two income streams that are taxed completely differently.**

- **G-sec interest is taxed at slab, with the ordinary surcharge ladder** running to 37%
- **Equity LTCG is 12.5%, with surcharge statutorily CAPPED at 15%** regardless of income

For a high earner that is 42.7% against 14.9%. **The asymmetry is large enough to change the sign.**

## The corrected comparison

| Income band | Tax on G-sec | Net G-sec | Tax on LTCG | Equity hurdle | **ERP after tax** |
|---|---|---|---|---|---|
| under ₹50L | 31.2% | 4.71% | 13.0% | 5.42% | **−0.53%** |
| ₹50L-1cr | 34.3% | 4.50% | 14.3% | 5.25% | **−0.36%** |
| ₹1-2cr | 35.9% | 4.39% | 14.9% | 5.16% | **−0.27%** |
| ₹2-5cr | 39.0% | 4.18% | 14.9% | 4.91% | **−0.02%** |
| **over ₹5cr** | **42.7%** | **3.92%** | 14.9% | **4.61%** | **+0.28%** |

**Not −1.96%. Between −0.53% and +0.28% depending on the band, and essentially dead even in the
middle.** The equity market is not being handed a two-point disadvantage; it is roughly at parity.

*(And this understates equity further — the ₹1.25 lakh annual LTCG exemption is not modelled.)*

## What actually has to be true

Decomposing a five-year return as **dividend yield + earnings growth + annualised multiple change**,
against the ₹2-5cr hurdle of 4.91%:

| Multiple path | Δ multiple p.a. | **Required EPS growth** |
|---|---|---|
| unchanged at 20.46x | 0.00% | **3.71%** |
| re-rates to the 10y average 23.33x | +2.66% | **1.05%** |
| de-rates to 18x | −2.53% | 6.24% |
| de-rates to 16x | −4.80% | 8.51% |

**India delivered 3.95% average earnings growth over the last two years — its worst run, nine
straight years of missing consensus.** Testing the pessimistic case at exactly that rate:

| At 3.95% growth | Total return | Verdict |
|---|---|---|
| multiple unchanged | **+5.15%** | **beats the hurdle** |
| re-rates to 23.33x | **+7.81%** | **beats comfortably** |
| de-rates to 18x | +2.62% | misses |
| de-rates to 16x | +0.35% | misses badly |

## The conclusion this forces, and it is not the one I had

**The load-bearing variable is the multiple, not earnings growth.**

Even assuming India keeps delivering at its recent disappointing 3.95%, equities clear the
after-tax hurdle **as long as the multiple holds.** The bear case cannot rest on "the G-sec pays
more" — after tax it barely does. **It has to rest on multiple de-rating**, and the Nifty is
already 12.6% below its own 10-year average, which makes further de-rating a stronger claim than
mere mean reversion.

## What this does NOT rescue

1. **It applies only to LTCG treatment.** Hold under 12 months and STCG at 20% makes the hurdle
   far worse ([[short-horizon-needs-a-10-12-percent-tax-edge]]).
2. **Equal expected return is not equal attractiveness.** A G-sec held to maturity has no price
   risk; the Nifty has a 15%+ annualised standard deviation. Parity in expected return with wildly
   different variance is not parity in a portfolio.
3. **It says nothing to a dollar investor.** In USD the Nifty is −9.9% over one year and −15.0%
   over two ([[india-in-usd-is-the-return-that-matters]]). This analysis is for an INR-earning,
   INR-spending, Indian-resident taxpayer only.
4. **The comparison ignores gold**, which beat the Nifty on all three horizons
   ([[gold-has-beaten-indian-equities-on-every-horizon]]).

## The method lesson

**I quoted a headline ratio for two days without asking whether the two sides of it were
comparable.** Earnings yield and bond yield are not like-for-like in a jurisdiction with
asymmetric taxation — and India's is markedly asymmetric.

**Before quoting any cross-asset comparison, ask: are both sides measured after the same
frictions?** Tax, currency, liquidity and holding period all break comparability, and all four
were unexamined here.
