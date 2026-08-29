---
title: "For a rupee-spender, the S&P beat the Nifty in 97% of ten-year windows"
market: india
type: finding
confidence: verified
tags: [india, finding, verified]
updated: 2026-08-29
---

# For a rupee-spender, the S&P beat the Nifty in 97% of ten-year windows

This is the finding that most damages the premise of this workspace, so it gets stated first and
plainly. It is also the most robust: 19 years of monthly data, every sub-period, no endpoint
dependence.

## The base rate

CAGR **in rupees** — the S&P 500 translated at USDINR, which is what an Indian resident actually
receives — against the Nifty:

| rolling window | S&P-in-INR beat Nifty | mean gap | median | worst case |
|---|---|---|---|---|
| 3-year (n=192) | **72%** | +4.79pp | +3.62pp | −14.28pp |
| 5-year (n=168) | **92%** | +4.80pp | +4.07pp | −3.83pp |
| 10-year (n=108) | **97%** | +4.52pp | +4.00pp | **−0.17pp** |

At a ten-year horizon the Nifty won 3 windows out of 108, and its best win was by 17 basis points.

Every calendar period, including the ones people remember as India's good years:

| period | Nifty (INR) | S&P (INR) | gap |
|---|---|---|---|
| 2008–2012 | +2.82% | +7.58% | +4.75pp |
| 2013–2017 | +11.78% | +16.41% | +4.63pp |
| 2018–2022 | +10.42% | +12.02% | +1.60pp |
| 2023–2026 | +8.83% | +24.06% | **+15.23pp** |

## The mechanism is arithmetic, not sentiment

The Nifty compounds at roughly **11%** in rupees. The rupee depreciates at roughly **3.5%** a year.
So the S&P needs only about **7.5%** in dollars to draw level, and it delivered about **13%**.

The half of this I nearly got backwards: for someone who earns and spends in rupees, **rupee
depreciation is not a cost of holding foreign assets — it is a return on them.** The USD
performance table that started this line of work (India −10.9%, Korea +109.3%) is the right frame
for a dollar allocator and the wrong one here. It counts the rupee's fall as India's loss, when for
a rupee-spender it is precisely what makes the foreign asset worth more. Getting this backwards
would have produced the right conclusion for the wrong reason, which does not survive the next
market.

## What it costs an Indian resident to act on this

Being fair to the India case, because the frictions are real:

- **20% TCS** on LRS remittance above the threshold. Creditable against tax liability, so a
  cash-flow cost for the year, not a permanent one.
- **Foreign listed equity is taxed worse**: LTCG needs a **24-month** hold versus 12 months
  domestically, STCG is at **slab rates** (up to 30%+) versus a flat 20%, and there is **no ₹1.25L
  exemption**.
- FX conversion spread, roughly 0.5–1% round trip.
- The LRS annual cap itself.

For a genuine long-term holder both sit at 12.5% LTCG, so the permanent tax wedge narrows to the
lost ₹1.25L exemption and the extra twelve months of holding. **None of that is 4.5pp a year.** The
frictions change the execution, not the conclusion.

## What this does to the work in this repo

It does **not** say "do not invest in India." It says something more uncomfortable and more useful:

1. **The default is a global allocation, and an India-specific book is the thing that needs to
   justify itself** — not the other way round. This workspace has had it backwards since day one,
   because the original question was framed as "pick three Indian stocks" and I never audited the
   frame.
2. **Indian stock-picking carries a ~4.5pp/yr structural headwind** against a passive foreign
   alternative. Any thesis in `positions/theses.json` must beat that, not merely beat the Nifty.
   With 4 theses scored against 30 needed, **there is no evidence yet that it does.**
3. **The real after-tax number is the one that spends.** The Nifty's 10.46% nominal becomes ~5.2%
   real at 5% CPI, and **~3.95% real after LTCG**. That is the actual hurdle. A 3.95% real return
   is not obviously worth the single-country, single-currency concentration risk it carries.
4. **The CPI assumption matters more than the stock picks.** The difference between 4% and 7%
   inflation is 2.98pp of real return — larger than most of the edge this entire research process
   is trying to establish.

## The obvious rebuttal, run — and it fails

The standard objection is that this is a Magnificent-7 artefact: US mega-cap concentration at a
record index share, which will revert. **Tested against the equal-weight S&P, and it is not.**

18.2 years, CAGR in rupees, common window from June 2008:

| index | CAGR in INR | vs Nifty | 5y rolling win rate vs Nifty |
|---|---|---|---|
| **S&P equal-weight** | **+16.39%** | **+6.11pp** | **90%** (mean +5.76pp) |
| S&P cap-weight | +15.27% | +4.99pp | 92% (mean +4.76pp) |
| Total world (VT) | +13.81% | +3.53pp | 77% (mean +2.74pp) |
| MSCI ACWI | +13.61% | +3.33pp | 77% (mean +2.68pp) |
| Developed ex-US | +10.33% | +0.06pp | **38%** (mean −0.98pp) |
| **Nifty** | +10.28% | — | — |
| Emerging markets | +9.01% | −1.27pp | **24%** (mean −3.97pp) |

Equal-weight beat cap-weight, by 1.12pp a year and with a *higher* mean rolling gap. Removing the
mega-caps makes the case against India **stronger**, not weaker. That disposes of the rebuttal.

## But it sharpens what the finding actually is

The table above says something more precise than "India underperforms the world":

- **India beat emerging markets** — EM won only 24% of 5-year windows, mean −3.97pp. India is a
  *good* EM.
- **India roughly tied developed ex-US** — 38% win rate, mean −0.98pp. Europe and Japan are not
  the answer.
- **India lost decisively to the United States, and only to the United States** — 90–92% of
  windows.
- Global cap-weighted indices beat India 77% of the time, but they are ~65% US. The US is doing
  the work.

**So the choice is not India versus foreign. It is India versus the US.** That is a far more
tractable question, and it is the one that should be argued — including the case that US
exceptionalism is itself the thing at a record and due to revert. What cannot be argued any more
is that the gap is a concentration artefact.

## Honest limits

- 19 years is one sample of one historical path. A base rate is not a forecast, and the entire
  window sits inside a single regime of falling and then low global rates.
- Rupee depreciation continuing at 3.5% is an assumption, not a law. If India's external position
  improved durably, the largest single component of the gap shrinks.
- The ETF proxies (RSP, ACWI, EFA, EEM, VT) carry fees and tracking differences the Nifty index
  does not; the comparison is index-to-ETF, which flatters the Nifty slightly, not the reverse.
- 2023–2026's +15.23pp gap is extreme by the standards of the rest of the sample.

## What would change this

The Nifty out-earning the S&P in rupees over a full 5-year rolling window would be the first
evidence in 168 windows that something structural shifted. It last happened in windows ending
around May 2025. Watch that series, not any single year.

**Source:** own computation, `scripts/base_rate_india_vs_world.py` and `scripts/base_rate_challenge.py`, over 228 months of monthly closes from September 2007. Reproducible from this repo; no secondary source involved.

Related: [[the-mean-reversion-steelman-fails-but-cannot-settle-it]] · [[india-vs-north-asia-the-trade-already-happened]] · [[india-aggregate-earnings-are-three-companies]] · [[dixon-profit-is-not-operating]]
