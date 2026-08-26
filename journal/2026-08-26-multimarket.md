# 2026-08-26 (second session) — pipeline goes multi-market

Snapshots: `data/daily/{india,us,crypto}/2026-08-26.json`. India 98/100, US 119/119,
crypto 44/46.

## What changed

**Three markets now run on one pipeline.** US (119 tickers) and crypto (46) added alongside
India. Sector baskets written for each. `--universe` and `--market` are the only interface, so
Japan, Europe or commodities are a JSON file away.

**Fixed a bug that was destroying data.** Every market was writing to
`data/daily/<date>.json`, so the US run silently overwrote the India snapshot. Output is now
namespaced per market. Caught it within minutes of adding the second market — worth noting that
the failure was silent and would have been invisible a week later.

**The quality gate caught four stale crypto tickers.** MATIC last printed 2025-03-24 (the POL
migration), SUI 2024-06-04, UNI 2025-04-17, APT 2025-06-24. A dead ticker returns a flat line,
not an error, and a flat line reads as low volatility.

## The finding that justifies the whole multi-market idea

**The AI-kills-software fear already broke and already reversed in the US. India is still
trading it.**

In early February 2026 roughly **$1 trillion of US enterprise software value vanished in a week**
on AI-agent fears. By mid-April, disclosures showed AI was accelerating revenue pipelines. SaaS
multiples went from 3.9x to 4.7x forward revenue during Q2; the group gained 18.9% in the June
quarter against the S&P's 14.9%. Our own basket: **+19.6% over three months, 83% breadth.**

Indian IT is at **+5.9% over three months with 43% breadth**, still 40-50% below its peak, and
Infosys *cut* FY27 guidance at Q1.

Same narrative, roughly four to six months apart. That is a lead-lag, and it is the first thing
this workspace has produced that a single-market view structurally could not see.

**The caveat is load-bearing and written into the knowledge file:** US SaaS is product with
software margins; Indian IT is labour arbitrage. If AI compresses billable headcount, Indian IT
takes a *worse* structural hit than a SaaS vendor who can attach AI to a seat price. What
transfers is the sentiment cycle, not the economics. The India confirmation signal is still a
guidance raise, not a US re-rating.

## The other four things worth knowing

**The rate cycle turned globally, not locally.** Fed funds 3.50-3.75%, held five meetings, with
**three dissents wanting a hike** and nine of eighteen dots favouring at least one. Chair is
Kevin Warsh. 10-year 4.7% near a 20-month high; **30-year 5.2%**. RBI has held four. Neither is
easing. Any India bull case resting on cuts is fighting a global regime.

**"AI exposure" has split into two opposite trades.** Supply-constrained hardware still works —
Micron **+702.9%** with HBM sold out through CY2026 and Goldman calling the worst memory shortage
in 15 years. The debt-funded buildout does not — Oracle -37.2% with a **-$23.7bn** free cash flow
deficit and a $40bn FY27 raise planned; our datacenter-power basket -18.1% over three months;
SMR -73.8%, OKLO -39.6%. With the 30-year at 5.2%, the market stopped paying for AI capex and
started underwriting it.

**US leadership rotated and breadth improved.** Healthcare **+42% over a year with 100% breadth**
(XBI +88.2%, $106bn of M&A across 201 deals, MFN pricing risk narrower than feared), energy +34.5%
at 100%, financials +17.2% over three months. **Russell 2000 +28.7%, leading everything**, on
OBBBA tax provisions effective 1 Jan and expected small-cap earnings growth of 17.1%. Megacap is
+15.5% over a year but **-7.0% over three months.** US breadth 64%; India 56% and split three ways.
The US is a market where an index view is worth having and India is not.

**Crypto is trading as a liquidity asset, not an independent one.** BTC $78,199, -9.2% over a
year and 19.3% below its ~$126k high, but +21.1% in a month with RSI 78. Driver is explicit: spot
BTC ETFs took $517mn on 19 Aug, ~$1.6bn over four days, plus Treasury intervention loosening
conditions and pressuring the dollar. Majors +28.8% over three months at 100% breadth, but
**L1-Alt -38.5% at 22% breadth and L2 -54.8% at 0%.** A majors-and-ETF rally, not alt season.
Regulation: GENIUS and CLARITY passed in 2025, but SEC/CFTC rulemaking runs up to 18 months with
main rules effective **late 2026 into 2027** — the structural case is real and not yet in force.

## What it means for the open book

**No new positions taken in the US or crypto.** Deliberate. Two reasons: the process has not yet
scored a single completed thesis in India, and adding two new markets' worth of positions before
the first scorecard exists is exactly the mistake `roadmap.md` was written to prevent.

One live consequence for the existing book: the **Infosys** thesis now has a named external
signal to watch rather than just "wait for a guidance raise" — the US software basket's
three-month return against Indian IT's. If that gap closes while India's revisions are still
negative, the read-across is sentiment only and the thesis stays on the bench.

## Process

Wrote `playbooks/roadmap.md` — the end goal and five phases with an exit test on each. The
governing rule is **scorecard before automation**: automation multiplies whatever the process
already does, so the process has to be measured first. Phase 3, calibration, is the real gate;
the orchestration harness is Phase 4 and deliberately not sooner. The document also records what
would make this stop, written now while it is still easy to be honest.

## Open questions carried forward

1. **Flows are not collected at all** and have been the most explanatory variable in every market
   examined today — FII/DII in India, ETF creations in crypto, fund flows in the US. Highest-value
   Phase 1 item.
2. **Estimate revisions are not collected either.** The Infosys error was missing a guidance cut,
   not misjudging a multiple. Revision direction has done more work than any valuation metric.
3. Why is Indian capital goods at 100% breadth while Indian infrastructure is flat? Still unknown.
4. Shriram Finance +81.5% on the MUFG stake — full work-up still owed.
5. Does the US healthcare/biotech leadership have an Indian analogue, or is the M&A driver purely
   a US patent-cliff phenomenon? Indian pharma is +1.6% with 67% breadth — nothing like +42%.
6. India Q1 FY27 GDP prints 31 August.
