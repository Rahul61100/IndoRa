---
title: "The spread monitor's first run graded my own research, and one grade is bad"
market: general
type: finding
confidence: high
tags: [general, finding, high]
updated: 2026-08-27
---

# The spread monitor's first run graded my own research, and one grade is bad

First output of `scripts/spreads.py`, built after the monsoon miss. It compares *groups* against
groups rather than ranking names. Five themes:

| theme | 1m | 3m | 6m | verdict |
|---|---|---|---|---|
| monsoon: urban over rural | +5.1pp | +21.2pp | **+20.0pp** | **widening — still working** |
| capex over consumption | +8.0pp | +5.9pp | **+19.8pp** | **widening — still working** |
| momentum over value | +1.0pp | +12.9pp | **+22.5pp** | narrowing — likely finished |
| private over PSU banks | −1.4pp | −0.4pp | +9.5pp | **reversing** |
| **domestic over US/EU-exposed** | **+0.2pp** | **−5.7pp** | **−0.7pp** | **not expressing at all** |

## The bad grade

**The trade-policy thread is not in prices.**

A very large share of this session went into tariffs, Federal Register instruments, the Washington
concentration finding, CBAM, H-1B, the Senate Russia bill. The market's verdict on all of it, over
six months, is a **−0.7pp** spread between domestically-focused names and US/EU-revenue names.
Effectively zero, and the wrong sign for the thesis.

Two readings, and honesty requires holding both:

1. **The market has not priced it** — in which case this is the opportunity, and the research was
   early rather than wrong.
2. **It is not material** — in which case the emphasis was misplaced.

Today's own finding pushes toward (2). The instrument in force is **10%**, roughly **45% of
India's US-bound exports (~$87bn) are exempt**, and the action is a **60-country forced-labour
programme** India was swept into rather than a bilateral squeeze. Generic pharma is at **0% until
August 2028.** Measured against that, a near-zero spread is not the market being asleep. It is the
market correctly pricing a modest, widely-exempted, multi-country tariff.

**Conclusion I do not like but should record: I over-weighted trade policy relative to what it
does to cash flows.** The political-economy layer that found it is still right to exist — it caught
the HAL and HDFC Bank chains, which *did* move prices. But finding a chain is not the same as
finding a priced risk, and I did not run that check.

## What the other four say about the book

- **Capex over consumption, +19.8pp and widening +8.0pp last month** — the second-strongest live
  theme, and **L&T is benched.** The bench was on L&T-specific grounds (European offshore-wind
  contract mix, 5 up / 9 down revision breadth) and those still stand. But the *theme* is working,
  which means the bench needs to be a view on L&T, not on capex. If the thesis is right and the
  vehicle is wrong, find the vehicle.
- **Momentum over value at +22.5pp but only +1.0pp last month.** The split this workspace already
  recorded is **closing**. A 22.5pp spread with no momentum left is a finished trade, and buying
  into it now is buying the top of a rotation.
- **Private over PSU banks reversing** — +9.5pp over six months, −1.4pp over one. The book holds
  **ICICI (private) and SBI (PSU) simultaneously**, so it is flat this spread. That is neutrality
  by accident, not by design, and it should be one or the other deliberately.
- **Monsoon still widening.** See [[the-monsoon-is-the-trade-i-missed]].

## The method note that matters

A wide spread is **not** an entry signal — it is usually the opposite. Three of the five themes here
have six-month spreads above 19pp, and two of those three are narrowing or reversing. The useful
column is the **1m against 6m** comparison, which says whether a theme is still paying, not whether
it has paid.

That distinction is why this file prints the direction rather than the level.

**Source:** own computation, `scripts/spreads.py`, equal-weighted median returns per basket so no
single name can carry a group. Baskets are my own construction and are the obvious place this could
be wrong — a theme is only as good as the names chosen to express it.

Related: [[the-monsoon-is-the-trade-i-missed]] · [[india-us-tariff-the-actual-legal-instruments]] · [[value-and-momentum-are-split]]
