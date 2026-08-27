# BUILD — the implementation plan for the research harness

Written 2026-08-27, after three days of running the loop manually. **This supersedes the phase
sketch in `playbooks/roadmap.md`**, which was written on day one before the failure modes were
known.

The point of this document: **the harness must encode the lessons, not merely automate the
collection.** Everything below exists because something went wrong without it.

---

## Target architecture

```
  ┌─ SCHEDULER (cron) ──────────────────────────────────────────────────┐
  │  pre-open 08:45 IST · intraday hourly · post-close 16:00 · 20:00     │
  └──────────────────────────┬──────────────────────────────────────────┘
                             ▼
  ┌─ LAYER 1 · DETERMINISTIC COLLECTION (scripts, never agents) ─────────┐
  │  prices+technicals · flows (cash AND derivatives) · revisions        │
  │  fundamentals · corporate actions · filings · political calendar     │
  │  → every source failure is LOUD; a missing series never reads as zero│
  └──────────────────────────┬──────────────────────────────────────────┘
                             ▼
  ┌─ LAYER 2 · DERIVED STATE (scripts) ──────────────────────────────────┐
  │  regime label · breadth · sector rotation · revision diffusion       │
  │  portfolio risk · required-return model · data-quality gate          │
  └──────────────────────────┬──────────────────────────────────────────┘
                             ▼
  ┌─ LAYER 3 · TRIGGERS (scripts decide what deserves an agent) ─────────┐
  │  thesis invalidation hit · catalyst date passed · revision diffusion │
  │  crossing ±0.4 · governance/regulatory hit on a held name            │
  │  · 52wk break on volume · unexplained anomaly                        │
  └──────────────────────────┬──────────────────────────────────────────┘
                             ▼
  ┌─ LAYER 4 · AGENT FLEET (archetype-diverse, budget-aware) ────────────┐
  │  ≥3 DIFFERENT archetypes per question, never 3 of the same           │
  │  Collector · Falsifier · Steelman · First-Principles · Base-Rate     │
  │  · Second-Order → then VERIFIER, mandatory before any position change│
  └──────────────────────────┬──────────────────────────────────────────┘
                             ▼
  ┌─ LAYER 5 · SYNTHESIS & RECORD ───────────────────────────────────────┐
  │  journal note · knowledge notes (WITH source URLs) · thesis updates  │
  │  · scorecard entry · SESSION-STATE regenerated · vault reindexed     │
  └──────────────────────────────────────────────────────────────────────┘
```

**Layers 1-3 are deterministic and must never be an agent's job.** Agents are for judgement.
Scripts are for facts. Conflating them is how a data error becomes a belief.

---

## What exists today

| Component | Status |
|---|---|
| `fetch_daily.py` — OHLC, technicals, quality gate | ✅ 3 markets, 265 tickers |
| `fetch_flows.py` — India FII/DII, stablecoins, DeFi TVL | ✅ append-only ledgers |
| `fetch_revisions.py` — EPS trend + diffusion + targets | ✅ built today |
| `report_daily.py` — per-market brief, constituent sector rotation | ✅ |
| `regime.py` — regime label, book stress test | ✅ |
| `portfolio_risk.py` — correlation, effective bets, USD-adjusted | ✅ |
| `required_return.py` — after-tax hurdle, EPS decomposition | ✅ built today |
| `sizing.py` — risk contribution, liquidity | ✅ |
| `intraday.py` — volume pace, gaps, level breaks | ✅ |
| `tools/kb.py` — frontmatter, MOC hubs, link integrity | ✅ 83 notes, 0 orphans |
| `tools/session_state.py` — resume brief | ✅ |
| `tools/audit.py` — unsourced-claim detector | ✅ built today |
| `tools/refresh.sh` — one-command full refresh | ✅ |
| Obsidian vault | ✅ |
| **Scheduling** | ❌ manual |
| **Derivatives flows collector** | ❌ niftytrader scrape, not built |
| **Corporate actions / filings watcher** | ❌ |
| **Fundamentals collector** | ❌ hand-captured, ~25 names |
| **Trigger layer** | ❌ |
| **Agent orchestration** | ❌ hand-launched |
| **Verifier gate** | ❌ |
| **Scorecard automation** | ❌ |

---

## Build order

### Phase A — close the collection gaps (highest value per hour)

**A1. Derivatives flows.** FII index-futures net and long-short ratio, PCR, max pain.
niftytrader.in serves NSE data without cookies; NSE's own CSV needs a browser session.
**Why first:** reading FII cash flow without the derivatives book was actively misleading me
([[fii-are-short-the-index-long-the-stocks]]).

**A2. Fundamentals collector.** P/E, P/B, RoE, growth, debt for the full universe, dated, cached.
**Never trust an aggregator ratio after a corporate action** — the Shriram P/B was 3.18x at
screener against ~2.36x recomputed from the filing ([[shriram-finance-mufg-workup]]). Store the
inputs, compute the ratios.

**A3. Filings and corporate-actions watcher.** NSE bulk/block CSVs (confirmed free), pledge
changes, board meetings, rating actions, exchange announcements for held names.
**Why:** a governance event closed two positions this week and neither appeared in any price series.

**A4. Political-economy calendar.** Elections, budget, RBI dates, expiry calendar, IPO dates,
Supreme Court listings on held names, regulatory deadlines.

**Exit test:** a full week with zero unexplained quality flags, and every held name's fundamentals
under seven days old.

### Phase B — scheduling and triggers

**B1. Cron.** Pre-open 08:45 IST, intraday hourly during the session, post-close 16:00, evening
20:00 for the US. **`fetch_flows.py` must run daily without exception** — NSE serves only the
latest session and a skipped day is permanently lost.

**B2. The trigger engine.** A script that reads the day's state and emits a ranked list of *what
deserves human or agent attention*, rather than a dashboard to be scanned. Triggers:
- a written invalidation condition met
- a catalyst date passed without the catalyst
- revision diffusion crossing ±0.4
- a governance, regulatory or legal hit on a held name
- a 52-week break on >1.5x volume
- a move the knowledge base cannot explain

**Exit test:** the trigger list, unread by me, would have caught HDFC Bank's breakdown and HAL's
governance chain.

### Phase C — agent orchestration

**C1. Archetype library as code.** The seven briefs in `playbooks/multi-agent-research.md` as
parameterised templates. A question plus a set of archetypes yields a fleet.

**C2. Budget-aware dispatch.** 200 WebSearch calls per session, shared. That is 5-8 deep agents.
The dispatcher must **track the rejected launches as open tasks** — five were silently dropped on
2026-08-26 and one was the governance screen whose absence closed HDFC Bank
([[i-never-ran-governance-on-my-own-book]]).

**C3. The Verifier gate.** **No position change without an independent verification pass.**
Mandatory, not optional.

**C4. Source enforcement.** `tools/audit.py` found **1,197 numeric claims and 0 source URLs**
across the base. Every agent brief must demand URLs, and the synthesis step must reject a note
that carries numbers without them.

**Exit test:** a fleet launched from one command, with archetype diversity enforced and rejected
launches queued rather than lost.

### Phase D — the scorecard, which is the real gate

**D1. Automated thesis scoring.** Every open thesis carries an invalidation condition and a
horizon. A script checks them daily against the data and writes the outcome.

**D2. Calibration.** Hit rate by horizon, market, archetype and thesis type. **When this process
says 70%, is it right 70% of the time?**

**D3. Benchmark honestly** — against the index, and against the naive alternative of owning the
leading sector basket.

**D4. Error taxonomy.** This week produced a clear one: *anchoring on a metric without checking
its forecasting record* (the ERP, R² 0.5%), and *keeping numerical work while dropping judgement
work under capacity pressure* (the governance screen). **Patterns are fixable; individual losses
are not.**

**Exit test — and this is the gate on everything above:** **30 theses scored forward to their
horizon.** Until then this workspace has **no evidence of skill**, and any backward-looking number
that flatters it is measuring hindsight ([[backtests-of-chosen-names-measure-hindsight]]).

### Phase E — extension

More markets (`--universe <name>` is already the whole interface), more asset classes, longer
horizons. Cheap once A-D hold. **Deliberately last.**

---

## Failure modes the harness must prevent

Each one has already happened.

| Failure | What it cost | The control |
|---|---|---|
| **Silent data degradation** | Yahoo's NSE sector indices had 40-day gaps rendering as fake 5-9% moves; a bad USDINR bar manufactured a 2% rupee move | Quality gate; prefer a source that cannot be wrong over a check that decides whether a source is wrong |
| **Rejected agent = lost task** | The governance screen never ran; HDFC Bank closed two days later on a governance event | Dispatcher queues rejections |
| **Collection crowds out judgement** | Under the search cap I kept the Collectors and dropped the governance work — exactly backwards | Budget rule: cut Collectors first, keep Falsifiers and Verifiers |
| **Aggregator ratios after corporate actions** | Shriram P/B 3.18x vs ~2.36x recomputed | Store inputs, compute ratios |
| **Unsourced claims** | 1,197 numbers, 0 URLs | Audit gate in the synthesis step |
| **My framing embedded in briefs** | Two false premises survived until an agent challenged them by luck | Premises go in the question, never the framing |
| **A metric with no forecasting record** | Two days on an ERP frame with R² 0.5% | Before building on a metric, establish its record |

---

## What would make this stop

Written now, while it is still easy to be honest:

- The calibration curve at Phase D shows no edge over owning the leading sector basket
- The daily loop becomes a ritual that restates yesterday instead of changing a conclusion
- The scorecard starts recording only wins

Any of those, and the correct answer is index funds and a much shorter loop.
