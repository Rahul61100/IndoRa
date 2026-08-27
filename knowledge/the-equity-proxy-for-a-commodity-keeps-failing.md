---
title: "Twice today the equity proxy for a commodity failed the same way"
market: general
type: finding
confidence: high
tags: [general, finding, high]
updated: 2026-08-27
---

# Twice today the equity proxy for a commodity failed the same way

The workflow's one new position idea was a gold-loan NBFC — Muthoot or a basket — argued as "the
connector asset: pure domestic book, direct gold-price beta, and gold pays off on both live tail
risks simultaneously." Tested it before accepting it. **The claim does not survive contact with the
data**, and it fails in exactly the way the ONGC oil hedge failed earlier today.

## Muthoot is not a gold proxy

Five years of daily log returns against spot gold:

| | beta to gold | R² | 1y return | 3y return | ann. vol |
|---|---|---|---|---|---|
| Muthoot Finance | **0.232** | **0.020** | +7.2% | +163.0% | **30.1%** |
| Manappuram | 0.188 | 0.009 | +20.1% | +145.2% | 37.2% |
| IIFL Finance | 0.080 | 0.001 | +43.1% | +8.5% | 43.3% |
| Titan (jewellery) | 0.070 | 0.003 | +41.0% | +64.3% | 23.5% |
| **gold itself** | — | — | **+27.4%** | **+149.1%** | — |

Gold explains **2% of Muthoot's daily variance.** Over the last year Muthoot returned **+7.2%
against gold's +27.4%** — about a quarter of the move — while carrying **30.1% annualised
volatility** and full credit and regulatory risk.

The three-year numbers look seductive (+163.0% against gold's +149.1%) and they are the trap. That
is coincidence of magnitude, not transmission: a 0.02 R² says the two did not get there together.

## The tail test is where it actually breaks

Average daily return in gold's **worst** 20 days and **best** 20 days:

| | gold's worst 20d | gold's best 20d | spread |
|---|---|---|---|
| gold itself | −4.06%/day | +3.30%/day | 7.36pp |
| Muthoot | **−1.09%/day** | +1.39%/day | 2.49pp |
| Manappuram | −0.58%/day | +0.56%/day | 1.13pp |
| Nifty | +0.08%/day | +0.42%/day | 0.34pp |

Muthoot captures about a third of gold's tail move — **and it falls when gold falls.** A hedge that
is supposed to pay in a crisis, delivers a third of the payoff, and shares the downside is not a
hedge. It is a lending business whose *collateral* happens to be gold, which is a completely
different thing from an asset whose *value* is gold.

**Rejected.** If the argument is that gold pays off on both tail risks, the instrument is **gold**.

## The pattern, which is the actual finding

This is the second time today:

- **ONGC does not hedge an oil supply shock.** In the four large supply shocks of the last decade,
  ONGC's median return was **+0.55% with a 50% hit rate** — a coin flip — because the windfall levy
  taxes away the gain precisely when it would matter.
- **Muthoot does not hedge a gold move.** R² 0.020, a third of the tail capture, and it falls with
  gold on the bad days.

In both cases the equity looks like the commodity in a pitch and does not behave like it in the
data. The mechanism differs — a tax in one case, a business model in the other — but the error is
identical: **treating a company's exposure to a commodity as equivalent to holding the commodity.**
An operating business sits behind a stack of things that break the transmission: taxes, regulation,
leverage, credit risk, hedging programmes, and its own equity beta.

**Standing rule, now: if the thesis is about a commodity, test the proxy's beta and its tail
capture before accepting it. If the answer is "buy the commodity", buy the commodity.** An equity
proxy needs a positive reason to exist — a genuine operating leverage, an access constraint, a tax
advantage — not just a thematic association.

Two footnotes worth keeping. Indian gold-loan NBFCs additionally carry **RBI LTV and
gold-loan-norm risk**, which has repeatedly hit this specific sub-sector. And this workspace
already records that **gold beat the Nifty over 1, 3 and 5 years in rupees** — so the direct
instrument was already the better trade before any of this.

**Source:** own computation from five years of daily closes; beta, R², tail-day conditional means
all computed here.

Related: [[gold-has-beaten-indian-equities-on-every-horizon]] · [[the-hedge-i-was-planning-is-not-purchasable]] · [[what-the-spreads-say-about-my-own-emphasis]]
