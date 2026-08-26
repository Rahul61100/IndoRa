# CLAUDE.md — market-intel workspace entry point

Research workspace for a **daily equity research loop**. Started with India; built to extend
to other markets later. This file loads on every turn — keep it lean, push depth into the
directories below and retrieve on demand.

> If this file conflicts with the data in `data/daily/latest.json`, **the data wins.** Update
> this file. Every claim here was true when written and decays.

## What this is for

Rahul runs a repeating research cycle: read the market, maintain live theses on a small number
of stocks across three horizons, and score those theses honestly over time. The eventual goal
is an orchestrated harness. Right now it is a manual loop with scripted data collection.

**The three horizons, fixed:**
- **Short** — a few months. Needs a dated catalyst and a stop. Trades, not investments.
- **Medium** — two to three years. Held through an earnings cycle. Staggered entry, no stops.
- **Long** — decades. Structural demand. Entry price still matters; trend does not.

## First move on any research turn

1. **Refresh the data.** `uv run scripts/fetch_daily.py && uv run scripts/report_daily.py --write`
   Never reason about prices from memory — see [`verify-prices-from-the-snapshot`](knowledge/verify-prices-from-the-snapshot.md).
2. **Read the flags.** The fetcher marks stale prints, history gaps and implausible one-day
   moves. Anything flagged is unusable until a second source confirms it.
3. **Score the open theses** in [`positions/open-theses.md`](positions/open-theses.md) before
   forming a new opinion. A thesis that has been wrong for three weeks is information.
4. **Read [`knowledge/INDEX.md`](knowledge/INDEX.md)** — one durable fact per file, the same
   pattern as the gamerun agentic repo. Skim the index, open what is relevant.
5. **Write the day's note** to `journal/YYYY-MM-DD.md`. The data brief is generated beside it
   as `YYYY-MM-DD-data.md`; the narrative note is yours to write and should say what *changed*,
   not restate the table.

## Layout

| Path | Holds |
|---|---|
| `scripts/` | `fetch_daily.py` (OHLC + technicals + quality flags), `report_daily.py` (markdown brief) |
| `universe/india.json` | every ticker fetched, grouped by role |
| `universe/sectors.json` | synthetic sector baskets built from constituents |
| `data/daily/` | one JSON snapshot per day, plus `latest.json` |
| `data/fundamentals/` | valuation and financial snapshots, dated |
| `knowledge/` | one durable fact per file — the load-bearing lessons |
| `playbooks/` | the repeatable procedures |
| `positions/open-theses.md` | live theses, entry logic, invalidation, running scorecard |
| `journal/` | dated notes; `-data.md` is generated, the bare date is written |

## Load-bearing facts (full list in `knowledge/INDEX.md`)

- **Yahoo's NSE sector indices are broken** — 40-day history gaps produce fake one-day moves of
  5-9%. Sector rotation is computed from constituents instead. [`yahoo-nse-sector-indices-have-gaps`](knowledge/yahoo-nse-sector-indices-have-gaps.md)
- **Demerged tickers show fake collapses** — TMPV shows -54% over a year that is a corporate
  action, not a drawdown. [`corporate-actions-fake-price-history`](knowledge/corporate-actions-fake-price-history.md)
- **Value and momentum have split hard in India right now** — nearly every cheap large cap is in
  a confirmed downtrend and nearly every uptrend is in something already expensive. Picking on
  valuation alone has been losing. [`value-and-momentum-are-split`](knowledge/value-and-momentum-are-split.md)
- **India is de-rating while earnings accelerate** — Nifty down on the year with profits up 18%.
  That is a flows and multiple problem, not an earnings problem. [`india-is-derating-not-missing-earnings`](knowledge/india-is-derating-not-missing-earnings.md)
- **The rate-cut cycle is over** — repo has been held four straight meetings and inflation is
  climbing toward a forecast peak. Nothing may be bought on a "cuts are coming" thesis.
  [`rate-cut-cycle-is-over`](knowledge/rate-cut-cycle-is-over.md)
- **Breadth is split down the middle** — roughly half of tracked names above their 200 DMA, an
  even three-way split of uptrend/downtrend/choppy. Index calls are near worthless here; this is
  a selection market. [`breadth-is-split-not-trending`](knowledge/breadth-is-split-not-trending.md)

## Working agreements

- **Never state a price, multiple or return without pulling it in the same session.** Fundamentals
  from `data/fundamentals/` are dated; if the file is older than a week, refresh it.
- **Every thesis carries an invalidation condition before it is entered.** A thesis with no
  falsifier is an opinion.
- **Record what was wrong.** The scorecard is the point. A KB that only logs winning calls
  teaches nothing.
- **Distinguish the trade from the holding.** The same ticker can be a short-horizon trade and a
  decades holding; they need separate entries, separate sizing and separate exit rules.
- This is research, not registered investment advice, and nothing here is a recommendation to
  any third party.
