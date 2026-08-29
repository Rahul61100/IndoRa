---
title: "Capital stayed in crypto while prices fell by half"
market: crypto
type: flows
confidence: high
tags: [crypto, flows, high]
updated: 2026-08-29
---

# Capital stayed in crypto while prices fell by half

Pulled directly from public APIs, so these are **verified** rather than reported — a rare thing in
this base.

| | value | 1-month | YTD | YoY |
|---|---|---|---|---|
| BTC | $77,949 | +22.0% | **−11.0%** | −28% |
| ETH | $2,444.50 | +27.3% | **−17.7%** | −44% |
| **Stablecoin supply** | **$311.3bn** | +1% | **+1.3%** | **+10.3%** |
| DeFi TVL | — | +17.7% | — | −42.5% |

Between October 2025 and June 2026, **BTC fell 53% and ETH fell 67% peak-to-trough.** Across that
entire crash, **stablecoin supply grew monotonically.** It never contracted.

BTC's 52-week range is $58,566 (1 Jul 2026) to $124,740 (7 Oct 2025) — it currently sits **37% below
that high** while capital in the system sits at an all-time high.

## What that separates

This base has treated stablecoin supply as **the cleanest proxy for real capital entering the
system, as distinct from price speculation.** The claim was asserted without evidence. It now has
some: the two series decoupled completely across a 53–67% drawdown, which is exactly the condition
under which a genuine flow measure and a price measure should diverge.

**The drawdown was a de-rating, not capital flight.** Money stayed; it stopped paying as much for
the same tokens.

## And it kills a metric I might have reached for

**DeFi TVL is not a flow signal.** It fell 42.5% YoY and rose 17.7% in a month, moving in lockstep
with price — because TVL is denominated in the assets it holds. It is a **mark-to-market quantity
wearing the costume of a flow measure**, and using it to infer capital movement would double-count
price.

That distinction generalises well beyond crypto and is the reason this note exists: *any* metric
denominated in the thing it is supposed to be measuring will confirm whatever price already did.

## Two live signals worth watching

- **ETF flows are diverging.** BTC's 9-day, >$3bn inflow streak broke (−$202m on 29 Aug) in the same
  week ETH's extended to 12 days (+$1.42bn). A rotation, if it holds. [reported]
- **BTC is now >50% correlated with GOLD on a 90-day basis**, having decoupled from tech equity.
  [reported] That reframes it as a macro/store-of-value trade rather than a Nasdaq proxy — and it
  changes any hedge-ratio assumption that treated crypto as high-beta equity.

## For an Indian resident specifically

**Budget 2026 gave no relief.** 30% tax and 1% TDS retained, and a **new ₹50,000 non-disclosure
penalty added.** India remains the most punitive of the three major regimes (US moving toward "most
crypto isn't a security"; EU MiCA live and enforcing) with **no reform signal.** [reported —
indiabudget.gov.in and pib.gov.in both 403'd, so this rests on secondary media.]

Practical read: crypto stays close to uninvestable for a rupee taxpayer regardless of the setup.

**Source:** CoinGecko `/simple/price` and `market_chart`, and DefiLlama's stablecoin and TVL
endpoints, fetched directly — **verified**. ETF flows, the gold correlation, and the Budget
provisions are **reported**.

Related: [[not-found-is-not-the-same-as-false]] · [[the-india-premise-fails-its-own-base-rate]]
