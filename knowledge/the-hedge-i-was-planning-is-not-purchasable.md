---
title: "The hedge for the 10 November catalyst does not exist at the tenor it needs"
market: general
type: finding
confidence: high
tags: [general, finding, high]
updated: 2026-08-29
---

# The hedge for the 10 November catalyst does not exist at the tenor it needs

India VIX at **10.94** (52-week range 8.72–28.91, so roughly the bottom decile) says protection is
cheap. It is — at tenors nobody needs. Live NSE option-chain data, 27 August 2026, Nifty spot
**24,090.85**:

| expiry | horizon | 10%-OTM put | price | IV | open interest | volume |
|---|---|---|---|---|---|---|
| 01-Sep-2026 | ~5 days | 22,000 | ₹0.80 | 29.05% | 53,884 | 64,558 |
| 29-Sep-2026 | ~1 month | 21,700 | ₹9.70 | 18.53% | **971** | **179** |
| 23-Nov-2026 | ~3 months | **not listed** | — | — | — | — |

**At the three-month expiry the exchange does not list a strike anywhere near 10% out of the
money.** The 10%-OTM level would be 21,682. The lowest strike listed at all is **22,450** — only
6.8% OTM — and it shows **zero open interest, zero volume, zero last-traded price, bid ₹0 against
ask ₹76.** That is not a wide market. That is no market.

## Why this specifically matters

The largest dated risk in the book is the **US–China rare-earth truce expiry on 10 November**,
**75 days out**. That lands squarely inside the dead zone: past the liquid weeklies, past the
thin monthly, at a tenor where the strike is not listed and the nearest one has no bid.

So the plan I was assembling — buy three-month index puts into a low-VIX window ahead of a dated
catalyst — **is not executable.** Not expensive: unavailable.

## What the alternatives actually cost

- **Weekly puts, rolled.** The only genuinely liquid instrument (OI 53,884, volume 64,558). But a
  five-day 10%-OTM put at ₹0.80 with 29% IV is a lottery ticket — the index has to fall 10% inside
  five days for it to pay anything. Covering 10 November means **eleven consecutive rolls**, each
  with its own spread, and eleven chances to be un-hedged on the week that matters. Cheap per unit,
  expensive as a programme, and it does not hedge a gap that happens between two of the rolls.
- **The one-month put.** ₹9.70 on a 24,100 index is 0.04% of notional — genuinely cheap. But OI of
  **971 contracts** means it cannot be sized for a real book, and exiting is a negotiation, not a
  trade.
- **Bank Nifty has no weekly options at all** — monthly only, since November 2024. The alternative
  index does not solve the tenor problem.

## The honest conclusion

**Low VIX is not the same as available protection.** A cheap option you cannot buy in size, at a
strike that is not listed, for the date you actually care about, is not a hedge — and quoting VIX
at 10.9 as evidence that hedging is cheap conflates the price of protection with its existence.

That reframes the problem. If index protection is not purchasable at the needed tenor, the
remaining ways to carry a dated catalyst risk are:

1. **Size down before the date** — the only method that always works and needs no counterparty.
   Unglamorous and reliable.
2. **Reduce the specific exposure** rather than hedging the index. The 10 November risk runs through
   magnet- and China-input-dependent names. That exposure was already reduced when Dixon closed
   today, which means the book is substantially less exposed to that date than it was this morning
   — by accident rather than design, but reduced nonetheless.
3. **Accept it and write it down.** A risk that cannot be hedged and will not be sized down is a
   risk being taken deliberately, and it should say so in the thesis rather than being implied.

**Do not put "buy Nifty puts before 10 November" in a plan.** It reads as prudence and it cannot be
executed.

## What to check before relying on this

Strike listings extend as expiries approach — the November chain may well list lower strikes by
October, and NSE adds strikes as spot moves. So this is a statement about **today's** chain, not a
permanent property. **Re-check the November chain in early October.** If liquid 10%-OTM protection
appears by then, the plan becomes available again at a VIX that may no longer be 10.9.

**Source:** live NSE option chain via agent research, 2026-08-27. Nifty spot and India VIX
independently consistent with own pulls (24,090.85 matches exactly). Strike listings and open
interest are **reported** from a single retrieval and are the sort of thing worth confirming
directly before trading.

Related: [[the-monsoon-is-the-trade-i-missed]] · [[dixon-profit-is-not-operating]] · [[what-the-spreads-say-about-my-own-emphasis]]
