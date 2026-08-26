# CLAUDE.md — market-intel workspace entry point

Research workspace for a **daily multi-market research loop**. Three markets live: **India, US,
crypto.** This file loads on every turn — keep it lean, push depth into the directories below
and retrieve on demand.

**The end goal and the staged path to it are in [`playbooks/roadmap.md`](playbooks/roadmap.md).
Read that before proposing to build anything.** The governing principle is *scorecard before
automation*: the process must prove it produces calibrated theses before it gets industrialised.

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

## Resuming after a context reset

**Read [`SESSION-STATE.md`](SESSION-STATE.md) first.** It is generated mechanically by
`tools/session_state.py` from what is on disk — open theses, the scorecard, data freshness,
carried-forward questions, recent commits — so nothing in it depends on the previous session
having remembered to summarise itself. **Regenerate it at the end of every session** and after
any material change to the book.

**Live market sessions run 09:00-14:00 IST** while the Indian market is open — see
[`playbooks/market-hours.md`](playbooks/market-hours.md). That is a different rhythm from the
end-of-day loop: watch volume pace and gaps, which the daily bar destroys.

**This directory is also an Obsidian vault.** Open `~/market-intel` as the vault root. Notes in
`knowledge/` carry frontmatter (`market`, `type`, `confidence`) that colours the graph, and the
`MOC-*` hub notes are the entry points. Run `uv run tools/kb.py all` after adding notes — it
stamps frontmatter, regenerates the hubs and reports broken links and orphans.

## First move on any research turn

1. **Refresh the data**, per market:
   ```bash
   for m in india us crypto; do
     uv run scripts/fetch_daily.py --universe $m
     uv run scripts/report_daily.py --market $m --write
   done
   ```
   Never reason about prices from memory — see [`verify-prices-from-the-snapshot`](knowledge/verify-prices-from-the-snapshot.md).
2. **Read the flags.** The fetcher marks stale prints, history gaps and implausible one-day
   moves. Anything flagged is unusable until a second source confirms it.
3. **Score the open theses** in [`positions/open-theses.md`](positions/open-theses.md) before
   forming a new opinion. A thesis that has been wrong for three weeks is information.
4. **Run the political economy layer** — [`playbooks/political-economy-layer.md`](playbooks/political-economy-layer.md).
   Who is positioned where, who holds the levers, who benefits from what the state is doing, and
   what is next on the political calendar. **This is not optional and it is not colour.** Two of
   the largest findings in this workspace are political-economy facts that no price series or
   financial statement contained.
5. **Read [`knowledge/INDEX.md`](knowledge/INDEX.md)** — one durable fact per file, the same
   pattern as the gamerun agentic repo. Skim the index, open what is relevant.
6. **Write the day's note** to `journal/YYYY-MM-DD.md`. The data brief is generated beside it
   as `YYYY-MM-DD-data.md`; the narrative note is yours to write and should say what *changed*,
   not restate the table.

## Layout

| Path | Holds |
|---|---|
| `scripts/` | `fetch_daily.py` (OHLC + technicals + quality flags), `report_daily.py` (markdown brief) |
| `universe/<market>.json` | every ticker fetched, grouped by role — `india`, `us`, `crypto` |
| `universe/<market>-sectors.json` | synthetic sector baskets built from constituents (India's is `sectors.json`) |
| `data/daily/<market>/` | one JSON snapshot per market per day, plus `latest.json` |
| `data/fundamentals/` | valuation and financial snapshots, dated |
| `knowledge/` | one durable fact per file — the load-bearing lessons |
| `playbooks/` | the repeatable procedures |
| `positions/open-theses.md` | live theses, entry logic, invalidation, running scorecard |
| `journal/` | dated notes; `<date>-<market>-data.md` is generated, `<date>.md` is written |
| `playbooks/roadmap.md` | the end goal and the phase gates to reach it |

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
- **Proximity to power is a pricing factor, especially in India** — who wins the licence, order,
  subsidy or forbearance is knowable from the public record and is absent from every financial
  statement. [`political-economy-layer`](playbooks/political-economy-layer.md)
- **India's ERP is NEGATIVE** — the 6.85% G-sec beats the 4.89% earnings yield. "Cheap versus its
  own history" is not the same as cheap. [`CORRECTION-india-erp-is-negative`](knowledge/CORRECTION-india-erp-is-negative.md)
- **Gold beat the Nifty over 1, 3 and 5 years in rupees** — the honest comparison set for any India
  equity thesis. [`gold-has-beaten-indian-equities-on-every-horizon`](knowledge/gold-has-beaten-indian-equities-on-every-horizon.md)
- **The rate-cut cycle is over** — repo has been held four straight meetings and inflation is
  climbing toward a forecast peak. Nothing may be bought on a "cuts are coming" thesis.
  [`rate-cut-cycle-is-over`](knowledge/rate-cut-cycle-is-over.md)
- **Breadth is split down the middle in India** — roughly half of tracked names above their 200
  DMA, an even three-way split of uptrend/downtrend/choppy. Index calls are near worthless there.
  The US at 64% and broadening is the opposite. [`breadth-is-split-not-trending`](knowledge/breadth-is-split-not-trending.md)
- **Cross-market lead-lag is the edge, not diversification** — the same narrative hits different
  markets months apart, and the first market is a preview of the second.
  [`cross-market-lead-lag-is-the-edge`](knowledge/cross-market-lead-lag-is-the-edge.md)
- **US SaaS already bottomed on the AI fear; Indian IT has not** — the clearest live example of
  the above. [`us-saas-already-bottomed-india-it-has-not`](knowledge/us-saas-already-bottomed-india-it-has-not.md)
- **The rate cycle turned globally** — the Fed has held five meetings with three dissents wanting
  a *hike*, and the 30-year is at 5.2%. [`fed-may-hike-next`](knowledge/fed-may-hike-next.md)
- **"AI exposure" is two opposite trades now** — supply-constrained chips still work; the
  debt-funded buildout is priced as credit. [`ai-capex-is-now-a-credit-story`](knowledge/ai-capex-is-now-a-credit-story.md)

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
