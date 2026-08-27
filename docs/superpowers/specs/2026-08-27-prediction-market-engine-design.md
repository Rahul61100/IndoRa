# Prediction-market calibration engine — design

**Date:** 2026-08-27
**Status:** approved design, not yet implemented
**Repo:** `market-intel` (`IndoRa`, personal GitHub only)

## Why this exists

The knowledge base has a measurement problem it cannot solve on its own. `tools/score.py` reads:

> CALIBRATION GATE: 4 scored, 30 needed. Until that gate is passed this workspace has
> NO EVIDENCE OF SKILL.

And all four closes were *research corrections*, not market outcomes — they measure the research
process, not the investment process. Equity theses at 2–3 year horizons will not close that gap for
years.

Prediction markets resolve in days-to-weeks, are binary, dated, and settle objectively against a
price that a market of interested parties set. **They are the fastest available instrument for
finding out whether this research process has any forecasting skill at all.**

This system is therefore built as a *measurement device first and a trading system second*. Real
capital is gated on the measurement, not the other way round.

## Decisions taken

| Decision | Choice |
|---|---|
| Money | **Paper first.** Real positions logged against live odds, settled on paper. Real capital gated on measured hit rate. Avoids Indian state betting law, FEMA, and 30% crypto tax + 1% TDS with no loss offset entirely at this stage. |
| Generation | **System proposes, human approves.** Nightly job surfaces candidates; nothing auto-enters. |
| Scope | **External-sector macro** — Iran/Hormuz/oil, Russia/sanctions, Fed/rates/inflation, China/rare-earth. |
| UI | **Local dashboard, single user.** FastAPI + HTMX on localhost. No auth, no hosting. |
| Stack | SQLite + FastAPI + Jinja/HTMX. No build step. |

### Scope was changed by feasibility work, and this is why

The original scope was "India + macro where we have edge". **A scan of all 2,100 open Polymarket
markets found zero markets on RBI policy, the rupee, the Nifty, Indian CPI or GDP, the monsoon, or
Indian elections.** What exists is novelty (Modi Nobel Peace Prize, $86k) and conflict
(India-strikes-Pakistan, $14k). There is no venue for the India thesis.

What *does* exist maps onto the external-sector research this workspace actually did:

| bucket | ≤90d | liquid & ≤180d | our sourced work |
|---|---|---|---|
| Iran / Hormuz / oil | 87 | **118** | SPR reconciliation, supply-vs-demand shock split |
| Russia / sanctions | 52 | **51** | Senate bill 86-11, >50% crude share, discount inversion |
| Fed / rates / inflation | 18 | **30** | rate cycle turned, three dissents wanting a hike |
| China / rare earth | 2 | 11 | the 10 Nov truce |
| tariff / trade | 0 | 1 | — |

**211 candidate markets, $31m combined liquidity.** Verified live, 2026-08-27.

## Architecture

```
Gamma API ──► fetch_markets.py ──► SQLite (predict.db)
                    │                    ▲
                    └──► odds/*.jsonl    │   (committed; DB is derived + gitignored)
                                         │
sources.json ──────────────────────► propose.py ──► review queue
                                         │              │
                                    (LLM, sonnet)    FastAPI + HTMX
                                                        │
                                    resolve.py ◄────────┘
                                         │
                                    scorecard
```

## 1. Data model

SQLite at `data/predict.db`.

```sql
markets          id, platform, condition_id, slug, question, description,
                 outcomes, end_date, resolution_source, resolved_by, neg_risk,
                 event_ticker, first_seen, last_seen,
                 closed, resolved, resolved_outcome, resolved_at, raw_resolution

odds             market_id, ts, prob_yes, best_bid, best_ask,
                 liquidity, volume, one_day_change      PK(market_id, ts)

predictions      id, market_id, created_at, direction,
                 our_prob,
                 market_prob_at_call, best_bid_at_call, best_ask_at_call,
                 liquidity_at_call,
                 edge, confidence, horizon_days, rationale,
                 status, reviewed_at, review_reason, review_note,
                 stake_units, proposed_by

prediction_claims  prediction_id, claim_id, note

resolutions      prediction_id, resolved_at, outcome,
                 brier, market_brier, beat_market, pnl_paper, scored
```

**Snapshot bid and ask, never just the mid.** A sampled market showed bid 0.006 / ask 0.007 — a 17%
spread. Scoring against a mid you could never trade produces a track record you could never have
earned. Same class of error as quoting Indian equity returns in rupees.

**`market_brier` sits beside `brier`.** A Brier of 0.20 alone is meaningless; 0.20 against a market's
0.25 is edge. The market is the benchmark, not truth — the same reasoning that put the S&P-in-INR
hurdle into `tools/score.py`.

**`prediction_claims` links every call to `sources.json` ids.** Every call is auditable, and it
enables the real feedback loop: *do `reported` claims produce worse predictions than `verified`
ones?* If they do, that changes how the knowledge base gets built.

**`review_reason` is categorical.** A rejected proposal is data about the reviewer.

### Persistence split

- `sources.json` / `theses.json` remain the git-tracked, human-editable source of truth. One-way
  sync into SQLite for joins.
- **`data/predict.db` is gitignored** — derived and rebuildable.
- Ingestion also appends to **`data/odds/YYYY-MM.jsonl`, which is committed.** Historical odds
  cannot be re-fetched. If the DB is the only copy, one `rm` destroys the irreplaceable half of the
  asset.

## 2. Ingestion — `scripts/fetch_markets.py`

Deterministic, no model in the loop, matching the repo rule that layers 1–3 are never an agent's job.

Flow: paginate Gamma → upsert `markets` → append `odds` row per market → append JSONL → reconcile
resolutions.

### Two traps found during probing, now design constraints

**Absence is not resolution.** The bulk feed caps at ~2,100 rows (HTTP 422 beyond) and is *ordered by
volume*. A market can leave that window while still open — this actually happened during design, when
a 500-row scan concluded India had one market. **Never infer resolution from disappearance.** Any
market with an open prediction is polled individually by id.

**`outcomePrices` is a JSON string, not an array** — `"[\"0.0065\", \"0.9935\"]"`. Parse it.

### Quality gates

- Binary outcome probabilities sum to ~1.0 (±0.02).
- `bestBid ≤ lastTradePrice ≤ bestAsk`; reject a crossed book.
- Volume is cumulative; a decrease is a data error or restructure, never real.
- Spread > 25% marks the row **untradeable** rather than dropping it — keep the history, don't price
  off it.

None of these catch an internally-consistent bad value, which is exactly how the corrupt USDINR daily
bar got through. The real protection is the **JSONL append**: raw values land on disk before
interpretation, so a bad gate can be re-run against history instead of having silently discarded it.

### Cadence

- **Nightly sweep** — full universe, builds odds history.
- **On-demand refresh** — re-pull the shortlist immediately before proposing, so
  `market_prob_at_call` is honest.

No auth required (verified: all endpoints return 200 unauthenticated). 250ms between pages,
exponential backoff on 429/5xx, resumable by offset.

## 3. Matching and proposal — `scripts/propose.py`

Three stages; only the third uses a model.

**Stage 1 — deterministic prefilter.** 2,100 → ~40. Liquidity > $50k, horizon ≤ 180d, no open
position, spread < 25%, topic keywords **with negative filters**.

> Negative filters are not optional. The design scan matched `india` → **Indiana Pacers** and `rbi`
> → baseball **Runs Batted In**. `india` NOT `indiana|indianapolis`; `rbi` only as a standalone
> token, never adjacent to `lead|mlb|season`.

**Stage 2 — claim join.** Pull candidate claims from `sources.json` by topic. **A market with no
matching claim is dropped, not guessed at.** No sourced view, no proposal.

**Stage 3 — LLM on the shortlist**, sonnet, forced structured output: `our_prob`, `direction`,
`claim_ids[]`, `rationale`, `confidence`, and **`no_view` as a first-class allowed answer.** A model
asked to find edge in 40 markets will find 40 edges unless abstaining is explicitly cheap.

### Edge calculation

Edge is **not** `our_prob − mid`. You cross the spread:

```
YES: edge = our_prob − ask
NO:  edge = bid − our_prob
```

**Threshold: 10 percentage points minimum.** Prediction markets are well-calibrated in aggregate;
the honest prior is that the market is right. With zero measured forecasting skill, the threshold
starts punitive and comes down only if Brier scores earn it.

### The favorite-longshot trap

Most of the candidate board sits at p = 0.001–0.07. Prediction markets have a documented
favorite-longshot bias — longshots are overpriced — so a naive engine will repeatedly "discover"
that it should sell longshots. That trade wins 99 times and returns everything on the hundredth,
while producing a **beautiful hit rate that means nothing**.

Therefore: proposals below p<0.05 or above p>0.95 are flagged and require explicit override, and the
scorecard reports Brier and P&L, **never hit rate alone**.

### Sizing

`stake_units` 1–5 from edge × confidence, **quarter-Kelly capped at 5% of bankroll**. Full Kelly
assumes your probabilities are correct; ours are unvalidated, and Kelly's failure mode under
overconfidence is ruin, not underperformance.

Nothing auto-enters. Everything lands as `proposed`.

## 4. Review UI

FastAPI + HTMX, localhost, four screens.

### Review queue

```
Fed +25bp after September FOMC          20d    $368k liq
market  bid 0.300 / ask 0.310      ours  0.45      edge +14.0pts
                                   stake 3 units (quarter-Kelly)

WHY  ▸ fed-may-hike-next          reported   2026-08-26   ← 1 day old
     ▸ rate-cut-cycle-is-over     reported   2026-08-25

⚠ odds moved 0.285 → 0.310 since proposal (4h). Edge was +16.5, now +14.0.

[ accept ]  [ adjust prob ]  [ reject ▾ ]
```

**Claim provenance is inline and unmissable** — tier, date, age, rendered so a `reported` claim looks
visibly weaker than a `verified` one. On 2026-08-27 this repo was found stamping 85 of 92 notes
`verified` against a ledger that said otherwise; a review screen that hides tiers is that same
confidence-laundering machine with better CSS.

**Odds drift is computed at render**, not at proposal. If drift takes edge below threshold the card
**auto-demotes to `expired`** rather than allowing acceptance on a stale price.

**Rejection is categorical**: `market is right` / `claim too weak` / `horizon too long` / `illiquid` /
`don't understand it` / `other`. Countable, so that in six months *"you reject 60% for 'claim too
weak' and those resolve in your favour 55% of the time"* is answerable. Free text cannot be
aggregated.

### Open book
Entry vs live odds, unrealised paper P&L, days to resolution, underpinning claims. **Any position
whose claim has since been contradicted is flagged** — the Dixon lesson, where a written invalidation
had already triggered two quarters before anything looked.

### Scorecard
Brier vs market Brier, plus a **calibration plot** bucketing calls by stated probability, predicted
against actual, **with n shown per bucket**. A bucket with 3 calls is decoration.

### Market browser
Search, filter, manual entry. Manual calls get `proposed_by='human'` and score separately from
engine calls. If the engine is worse than the human, that needs to surface early.

**Stack:** server-rendered Jinja + HTMX, ~4 endpoints, inline SVG charts, no CDN.

## 5. Resolver and scorecard — `scripts/resolve.py`

Nightly, after ingestion. Polls **by market id** for every open prediction.

### Two questions, two numbers

```
Was I more accurate?   Brier vs market Brier — both use the MID at call time
Did I make money?      paper P&L — uses the ASK or BID actually crossed
```

Scoring *accuracy* against the mid is right — the mid is the market's honest forecast. Scoring *P&L*
against the mid is wrong — you never traded there. Keeping both lets a call be **more accurate than
the market and still lose money on the spread**, which is the case that says the edge is real but the
venue eats it.

```
brier        = (our_prob − outcome)²
market_brier = (mid_at_call − outcome)²
beat_market  = brier < market_brier
pnl_paper    = YES: outcome − ask_at_call        per unit staked
               NO:  bid_at_call − outcome
```

### Resolution is not always clean

Polymarket settles via UMA oracle and outcomes get disputed. Store the raw resolution payload, mark
disputed markets `pending_dispute`, and **never score a disputed resolution until it settles.** A
market that resolves against us and flips on appeal must not sit in the record as a loss, and must
not be quietly deleted either.

Markets expiring unresolved get `void`, excluded from Brier, logged separately. Voids clustering on
one topic is a venue problem worth surfacing.

### The gate

```
CALIBRATION GATE: 0 resolved, 50 needed for a directional read
                                200 for a confident one
Until then this measures nothing.
```

The arithmetic is unforgiving: distinguishing a Brier of 0.23 from a market's 0.25 needs hundreds of
resolved calls. At a 126-day median horizon this is plausibly **a year** to a real answer. Better
written on the screen now than discovered at call 40.

### The assumed result

**The base case is that we lose to the market**, which aggregates money from people who do this full
time. `beat_market` is therefore reported as a **rate with a confidence interval**, not a count, and
when the interval spans 50% the scorecard prints *"indistinguishable from chance"* rather than a
number that invites a story.

**Real-money unlock requires all three:** ≥50 resolved, `beat_market` interval entirely above 50%,
and positive paper P&L after spread.

## Out of scope

- Real-money execution, wallets, crypto rails.
- Public hosting and auth.
- Manifold / Metaculus ingestion (Metaculus returned 403 unauthenticated; Manifold is viable later
  for the India questions Polymarket lacks).
- Automated entry without human approval.

## Open questions for implementation

1. LLM proposal cost per nightly run at ~40 markets — measure before scaling the shortlist.
2. Whether `sources.json` topic tagging is rich enough for the Stage-2 join, or needs an explicit
   `topics[]` field added.
3. Bankroll notional for paper sizing — needs a number to make `stake_units` meaningful.
