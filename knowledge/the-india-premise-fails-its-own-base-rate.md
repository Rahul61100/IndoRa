---
market: india
type: finding
confidence: high
date: 2026-08-27
tags: [allocation, base-rate, currency, tax, premise-check]
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

## Honest limits

- The 2023–2026 gap of +15.23pp is extreme and driven by US mega-cap concentration at a record
  share of the index. Reversion there would compress the gap materially.
- 19 years is one sample of one historical path. A base rate is not a forecast.
- Rupee depreciation continuing at 3.5% is an assumption, not a law. If India's external position
  improved durably, the largest single component of the gap shrinks.
- Nothing here is tested against an *equal-weight* or *ex-mega-cap* S&P, which is the obvious
  first challenge to it and has not been run.

## What would change this

The Nifty out-earning the S&P in rupees over a full 5-year rolling window would be the first
evidence in 168 windows that something structural shifted. It last happened in windows ending
around May 2025. Watch that series, not any single year.

Related: [[india-vs-north-asia-the-trade-already-happened]] · [[india-aggregate-earnings-are-three-companies]] · [[dixon-profit-is-not-operating]]
