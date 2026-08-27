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

**Read the first two first — they reframe everything below them.**

- **The India premise fails its own base rate** — for a *rupee-spender*, the S&P-in-INR beat the
  Nifty in **97% of rolling 10-year windows** (92% of 5-year, 72% of 3-year), mean gap ~4.5pp/yr,
  across every calendar sub-period since 2008. Equal-weight S&P does *better* than cap-weight, so
  it is not a Magnificent-7 artefact. Nuance that matters: India **beat** EM and roughly tied
  developed-ex-US — **it lost only to the US.** The default is a global allocation and an India
  book is what must justify itself; this workspace had that backwards because the framing of the
  original question was never audited. [`the-india-premise-fails-its-own-base-rate`](knowledge/the-india-premise-fails-its-own-base-rate.md)
- **Rupee depreciation is a RETURN on foreign assets, not a cost** — for someone who earns and
  spends in rupees. A USD performance table counts the rupee's fall as India's loss when it is
  exactly what makes the foreign asset worth more. Real after-tax Nifty return is **~3.95%**
  (10.46% nominal, 5% CPI, LTCG) — and the 4%-vs-7% CPI assumption is worth 2.98pp, more than most
  of the stock-picking edge this process is trying to establish. `scripts/real_return.py`
- **Never report an Indian aggregate without its median and breadth** — revenue-weighted, Q1 FY27
  reads as an economy-wide margin collapse (operating income +1.6%, −207bps). Excluding three
  operationally negative names it reads +15.4% and −32bps, median company +20.3%, breadth 71%.
  Those three are 26.6% of sample revenue. [`india-aggregate-earnings-are-three-companies`](knowledge/india-aggregate-earnings-are-three-companies.md)
- **Yahoo's FX daily bars are wrong often enough to be unusable** — three pairs affected. USDINR
  2026-08-26 closed at 93.546 on a session that never traded below 95.402, rendering the next day
  as +2.1% when it was +0.12%. The bad bar is *internally self-consistent*, so both a tolerance
  check and an OHLC check pass on it. **Prefer a source that cannot be wrong over a check that
  decides whether a source is wrong.** `scripts/fx.py` derives closes from intraday prints.
  [`yahoo-fx-daily-bars-are-unreliable`](knowledge/yahoo-fx-daily-bars-are-unreliable.md)
- **Profit is not the same as operating profit** — Dixon reported revenue +21.1% with operating
  income −8.6% and net income +194.8%, at 1.86× operating income. Four flags now screen for it
  (`scripts/fetch_fundamentals.py`). And: a thesis that needs **three caps** has already been
  falsified and is being kept alive with qualifiers. [`dixon-profit-is-not-operating`](knowledge/dixon-profit-is-not-operating.md)
- **Korea is real and that is why it is dangerous** — SK Hynix's 76% operating margin is confirmed
  from five quarters of income statement, monotonic from 42.2%. It trades at a **forward P/E of
  3.7**. Peak earnings at a trough multiple is a cyclical top, not cheapness. KOSPI is 24% off its
  high with three days above +10% in two years. **The trade already happened.**
  [`india-vs-north-asia-the-trade-already-happened`](knowledge/india-vs-north-asia-the-trade-already-happened.md)
- **An oil shock is only bad for India if it is a SUPPLY shock** — unconditionally, Indian equities
  *rise* with oil (6-month beta +0.17), because oil proxies global demand. Split by copper: in
  demand-driven oil-up months the Nifty averages +1.98%, in supply-driven ones −0.16%. In the four
  large supply shocks in ten years the Nifty fell **every time** (mean −3.91%, worst −12.0%) and
  IndiGo averaged −8.5%. **ONGC does not reliably hedge it** — 50% hit rate, median +0.55%, because
  the windfall levy taxes away the gain precisely when it would matter. `scripts/oil_india.py`
- **Yahoo's NSE sector indices are broken** — 40-day history gaps produce fake one-day moves of
  5-9%. Sector rotation is computed from constituents instead. Related trap: one all-NaN column
  turns `dropna(how="any")` into an empty frame and prints a *blank table* rather than erroring.
  [`yahoo-nse-sector-indices-have-gaps`](knowledge/yahoo-nse-sector-indices-have-gaps.md)
- **Demerged tickers show fake collapses** — TMPV shows -54% over a year that is a corporate
  action, not a drawdown. [`corporate-actions-fake-price-history`](knowledge/corporate-actions-fake-price-history.md)
- **Value and momentum have split hard in India right now** — nearly every cheap large cap is in
  a confirmed downtrend and nearly every uptrend is in something already expensive. Picking on
  valuation alone has been losing. [`value-and-momentum-are-split`](knowledge/value-and-momentum-are-split.md)
- ~~**India is de-rating while earnings accelerate** — profits up 18%~~ **RETRACTED.** The 18% was
  one quarter with 60% of the growth from five stocks. **FY26 actually grew 4.5%** against 12–15%
  expected, the ninth straight year of misses, and index reconstitution flatters even that (4.5%
  actual vs 6.9% reconstituted). It is an earnings problem as well as a multiple problem.
  [`india-is-derating-not-missing-earnings`](knowledge/india-is-derating-not-missing-earnings.md)
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
