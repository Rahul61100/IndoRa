# The process, and the end goal it is built toward

Written 2026-08-26, after the first three-market pull.

## The end goal, stated plainly

**A research process that compounds, and that can prove whether it is any good.**

Concretely: a daily, multi-market research loop that produces a small number of scored,
falsifiable theses; keeps an honest record of which ones worked; and only then gets automated
into an orchestrated harness. Coverage across India, the US, crypto and whatever comes next.

The thing being built is **not** a stock picker. It is a **calibration machine**. A process that
produces ten confident calls a day and never checks them is worth less than one that produces one
call a week and knows its own hit rate.

## The one principle everything else follows from

**Scorecard before automation.**

Automation multiplies whatever the process already does. If the process is wrong, automation
produces wrong answers faster and with more conviction. So the ordering is fixed: prove the
manual loop generates calibrated theses first, then scale it. Any pressure to jump straight to
the harness is pressure to industrialise an unmeasured process.

Corollary: **every phase below has an exit test, and the phase does not end until the test
passes.**

---

## Phase 0 — Foundation ✅ done 2026-08-26

Collection is scripted, the knowledge base exists, and theses are written with invalidation
conditions attached.

- `fetch_daily.py` — OHLC, derived technicals, relative strength, **automated data-quality gate**
- `report_daily.py` — per-market brief with constituent-based sector rotation and breadth
- Three markets live: India (100 tickers), US (119), crypto (46)
- `knowledge/` — 20 durable facts, one per file
- `positions/open-theses.md` — live book with invalidation conditions and a revision log
- Daily journal

**What it already caught:** Yahoo's NSE sector indices have 40-day history holes producing fake
5-9% single-day moves; four crypto tickers stale on rebrands and migrations; three of nine open
Indian theses invalidated on first contact with price data.

**Exit test — passed:** the loop ran end to end and changed a conclusion.

---

## Phase 1 — Coverage and reliability

Make the data trustworthy and complete enough that a wrong conclusion is a *reasoning* error,
not a data error.

- **Fundamentals automation.** Today ~25 hand-captured names. Needs a fetcher with a dated cache
  and a staleness gate, covering valuation, growth, margins, balance sheet and estimate revisions.
- **Estimate revisions specifically.** The Infosys mistake was missing that guidance was being
  *cut*. Revision direction has done more work in this loop than any valuation metric.
- **Corporate-action handling.** Demergers, bonuses and renames silently corrupt long-window
  returns. Needs a per-ticker action log so the fetcher can flag or splice.
- **Flows.** ✅ *partially done 2026-08-26* — `fetch_flows.py` collects India FII/DII (NSE),
  stablecoin supply and DeFi TVL (DefiLlama), all public and unauthenticated, into append-only
  ledgers. It immediately produced a finding no search had: stablecoin supply peaked at $320.9bn
  in May 2026 and is **down 3.2% over 90 days** while BTC rallied 28% on ETF creations
  ([[stablecoin-supply-peaked-in-may]]).
  **Still missing: US fund flows and crypto ETF creations** — no free daily source found yet.
  Do not let a missing series read as zero flow.
- **Scheduled runs**, so the snapshot exists before the session starts rather than during it.
- **More universes:** Japan, Europe, commodities, FX, India small/mid as its own file.

**Exit test:** a full week of daily runs with zero unexplained data-quality flags, and every open
thesis carrying current fundamentals no older than seven days.

---

## Phase 2 — Signal layer

Turn the data into ranked candidates. Still human-decided; the machine proposes, it does not
choose.

- **Regime classifier.** Breadth, volatility, rate direction and credit spreads reduced to a
  labelled state per market. This matters because the correct strategy is regime-dependent — at
  India's current 56% breadth and three-way trend split, an index view is worthless, while the
  US at 64% and broadening supports one.
- **Screens with explicit logic.** Value-with-trend, breakout-with-earnings, oversold-quality,
  revision-momentum. Each screen writes its output dated, so its own hit rate can be measured
  later.
- **Cross-market lead-lag monitor.** The highest-value thing found so far
  ([[cross-market-lead-lag-is-the-edge]]). Automate the comparison of paired baskets across
  markets and surface widening or closing gaps.
- **Position sizing framework.** Currently ad hoc. Needs to be a function of conviction,
  volatility and correlation to what is already held.

**Exit test:** every thesis entered for a month traces to a named screen or a named lead-lag,
not to a hunch.

---

## Phase 3 — Scoring and calibration ← the real gate

The phase that determines whether any of this is worth automating.

- **Every thesis scored at its horizon**, and at fixed checkpoints before it. Outcome recorded
  against the invalidation condition written at entry — not against a story invented afterwards.
- **Hit rate by category:** by horizon, by market, by screen, by thesis type (value / momentum /
  event / macro). Expect these to differ a lot, and expect some to be negative.
- **Calibration curve.** When this process says it is 70% confident, is it right 70% of the time?
  This is the number that matters and nobody keeps it.
- **Benchmark honestly.** Against the index, and against the naive alternative of buying the
  strongest sector basket. If the process cannot beat "own the leading sector", it is
  entertainment.
- **Error taxonomy.** Today's three failures were all one type: anchoring on valuation without
  checking trend or revision direction. That is a *pattern*, and patterns are fixable. Log the
  type, not just the loss.

**Exit test:** at least 30 scored theses, a measured hit rate per category, and one documented
process change made because the scorecard demanded it.

---

## Phase 4 — Orchestration harness

Only after Phase 3. Shape, roughly:

```
scheduled collectors  →  per-market analyst agents  →  adversarial verifier
                                                              ↓
                                     cross-market synthesiser → daily brief
                                                              ↓
                                              scorecard updater (automatic)
```

- **Collectors** are scripts, not agents. Deterministic work stays deterministic.
- **One analyst per market**, each holding only its own market's context.
- **An adversarial verifier that tries to refute every proposed thesis** — this is the piece that
  would have killed the ONGC call on day one, by asking what the driver was actually doing rather
  than what its level was.
- **A synthesiser** whose only job is cross-market lead-lag, because no single-market analyst can
  see it.
- **Automatic scorecard updates**, so the record cannot quietly stop being kept when it gets
  uncomfortable.

**Exit test:** the harness reproduces a week of manual conclusions, and its disagreements with the
manual loop are examined one by one rather than assumed to be improvements.

---

## Phase 5 — Extension

More markets, more asset classes, longer horizons. Cheap once Phases 1-4 hold, because the
pipeline is already market-agnostic — `--universe <name>` is the whole interface.

---

## What would make this stop

Written down now, while it is still easy to be honest:

- The calibration curve at Phase 3 shows no edge over the naive sector-basket benchmark
- The daily loop becomes a ritual that restates yesterday instead of changing a conclusion
- The scorecard starts recording only wins

Any of those means the correct answer is index funds and a much shorter loop.
