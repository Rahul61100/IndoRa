# Proposition engine — design

**Date:** 2026-08-27
**Status:** approved design, not yet implemented
**Repo:** `market-intel` (`IndoRa`, personal GitHub only)
**Supersedes:** the venue-bound first draft of this file (Polymarket-only, markets as the primary entity)

## Why this exists

The knowledge base has a measurement problem it cannot solve alone. `tools/score.py` reads:

> CALIBRATION GATE: 4 scored, 30 needed. Until that gate is passed this workspace has
> NO EVIDENCE OF SKILL.

All four closes were *research corrections*, not market outcomes — they measure the research
process, not the investment process. Equity theses at 2–3 year horizons will not close that gap for
years.

Prediction markets resolve in days-to-weeks, are binary, dated, and settle objectively against a
price that interested parties set with money. **They are the fastest available instrument for
finding out whether this research process has forecasting skill at all.**

Built as a *measurement device first, trading system second*. Real capital is gated on the
measurement, never the reverse.

## The central abstraction: propositions, not markets

The first draft attached predictions to venue markets. That was wrong. **A proposition is a
statement about the world; a market is one venue's contract on it.**

```
claims (sources.json) ──► PROPOSITION ──► our view (prob, date, claim_ids)
                               │
                    ┌──────────┼──────────┐
              Polymarket    Kalshi     Manifold
               market       contract    question
```

"The Fed raises rates at the September 2026 FOMC" is one proposition. Three venues carry it. Our
view attaches to the proposition; venues are rendering targets and execution surfaces.

This buys three things:

1. **Venue independence.** Polymarket has no India markets (verified below). Manifold does. Same
   engine, no redesign.
2. **Cross-venue disagreement**, which is an edge requiring *zero forecasting skill* — see §6.
3. **One view, many scorings.** The same call is scored against every venue carrying it.

## Decisions taken

| Decision | Choice |
|---|---|
| Money | **Paper first.** Real positions logged against live odds, settled on paper. Real capital gated on measured performance. Sidesteps Indian state betting law, FEMA, and 30% crypto tax + 1% TDS with no loss offset. |
| Generation | **System proposes, human approves.** Nothing auto-enters. |
| Scope | **External-sector macro** — Iran/Hormuz/oil, Russia/sanctions, Fed/rates/inflation, China/rare-earth. Plus India via Manifold where it exists. |
| UI | **Local dashboard, single user.** FastAPI + HTMX on localhost. No auth, no hosting. |
| Stack | SQLite + FastAPI + Jinja/HTMX. No build step. |

### Scope was changed by feasibility work, and this is why

The original scope was "India + macro where we have edge". **A scan of all 2,100 open Polymarket
markets found zero on RBI policy, the rupee, the Nifty, Indian CPI or GDP, the monsoon, or Indian
elections.** What exists is novelty (Modi Nobel Peace Prize, $86k) and conflict (India-strikes-
Pakistan, $14k). There is no Polymarket venue for the India thesis.

What *does* exist maps onto the external-sector research this workspace actually did:

| bucket | ≤90d | liquid & ≤180d | our sourced work |
|---|---|---|---|
| Iran / Hormuz / oil | 87 | **118** | SPR reconciliation, supply-vs-demand shock split |
| Russia / sanctions | 52 | **51** | Senate bill 86-11, >50% crude share, discount inversion |
| Fed / rates / inflation | 18 | **30** | rate cycle turned, three dissents wanting a hike |
| China / rare earth | 2 | 11 | the 10 Nov truce |
| tariff / trade | 0 | 1 | — |

**211 candidate markets, $31m combined liquidity.** Verified live 2026-08-27. Manifold separately
carries ~84 open India questions, which is why the proposition layer matters.

## 1. Venue survey (verified 2026-08-27)

| venue | prices public | adapter notes |
|---|---|---|
| **Polymarket** | ✅ | `outcomePrices` is a **JSON string**, not an array. `bestBid`/`bestAsk`. Bulk feed caps ~2,100 rows (HTTP 422), volume-ordered. |
| **Kalshi** | ✅ | Prices live in **`*_dollars` fields** (`yes_ask_dollars`, `no_bid_dollars`, `volume_fp`, `open_interest_fp`) — the unsuffixed names are deprecated and return null. **Blocks python-requests at the TLS layer; works via curl.** Publishes `rules_primary`/`rules_secondary`. |
| **Manifold** | ✅ | Play money (MANA). `probability`, `totalLiquidity`, `uniqueBettorCount`. Timestamps are **epoch milliseconds**. Long India tail. |
| Metaculus | ❌ 403 | Needs auth. Out of scope for v1. |
| PredictIt | ❌ 403 | Out of scope. |

**Indian platforms (Probo, MPL Opinio) are deliberately excluded** — legally grey, active
regulatory pressure and state-level bans, regardless of technical feasibility.

## 2. Data model

SQLite at `data/predict.db`.

```sql
propositions     id, statement, topic, resolves_by, resolution_criteria,
                 created_at, status            -- open | resolved | void
                 outcome, resolved_at

markets          id, venue, venue_market_id, proposition_id,     -- nullable until mapped
                 question, description, resolution_source, resolution_rules,
                 outcomes, end_date, neg_risk,
                 first_seen, last_seen, closed, resolved,
                 resolved_outcome, resolved_at, raw_resolution

odds             market_id, ts, prob_yes, best_bid, best_ask,
                 liquidity, volume, n_traders       PK(market_id, ts)

views            id, proposition_id, created_at, our_prob, confidence,
                 rationale, claim_ids, proposed_by, status,
                 reviewed_at, review_reason, review_note

positions        id, view_id, market_id,           -- a view executed on ONE venue
                 direction, entered_at,
                 market_prob_at_entry, bid_at_entry, ask_at_entry,
                 liquidity_at_entry, edge, stake_units

resolutions      position_id, resolved_at, outcome,
                 brier, market_brier, beat_market, pnl_paper, scored
```

**The split that matters:** a `view` is what we think about a proposition. A `position` is that view
expressed on a specific venue at a specific price. One view can produce three positions across three
venues at three different prices — and they will score differently, which is itself the
cross-venue signal.

**Snapshot bid and ask, never the mid.** A sampled market showed bid 0.006 / ask 0.007 — a 17%
spread. Scoring against a price you could never trade produces a track record you could never have
earned. Same class of error as quoting Indian equity returns in rupees.

**`market_brier` sits beside `brier`.** A Brier of 0.20 alone is meaningless; 0.20 against a market's
0.25 is edge. The market is the benchmark, not truth — same reasoning that put the S&P-in-INR hurdle
into `tools/score.py`.

**`claim_ids` links every view to `sources.json`.** Every call is auditable, and it enables the real
feedback loop: *do `reported` claims produce worse forecasts than `verified` ones?* If so, that
changes how the knowledge base gets built.

**`review_reason` is categorical.** A rejected proposal is data about the reviewer.

### Persistence split

- `sources.json` / `theses.json` remain the git-tracked, human-editable source of truth. One-way
  sync into SQLite for joins.
- **`data/predict.db` is gitignored** — derived and rebuildable.
- Ingestion appends to **`data/odds/YYYY-MM.jsonl`, which is committed.** Historical odds cannot be
  re-fetched. If the DB is the only copy, one `rm` destroys the irreplaceable half of the asset.

## 3. Ingestion — venue adapters

`scripts/venues/{polymarket,kalshi,manifold}.py`, each exposing one function:

```python
def fetch_open() -> list[RawMarket]   # normalises to a common shape
```

Deterministic, no model in the loop — the repo rule that layers 1–3 are never an agent's job.
`scripts/fetch_markets.py` runs every adapter, upserts, appends odds, appends JSONL, reconciles.

### Traps found while probing, now design constraints

**Absence is not resolution.** Polymarket's bulk feed caps at ~2,100 rows and is volume-ordered. A
market can leave that window while still open — this happened during design, when a 500-row scan
concluded India had one market. **Never infer resolution from disappearance.** Any market with an
open position is polled individually by id.

**Field names are not guessable.** Polymarket's `outcomePrices` is a JSON string; Kalshi's real
prices are `*_dollars` and the obvious names return null; Manifold's timestamps are epoch ms. Every
adapter needs a field-mapping test that fails loudly when a venue renames something.

**Keyword matching is dangerous.** During design, `india` matched **Indiana Pacers** and `rbi`
matched baseball **Runs Batted In** — on two separate venues. Negative filters are mandatory:
`india` NOT `indiana|indianapolis`; `rbi` only as a standalone token, never adjacent to
`lead|mlb|season`. Kalshi's first 1,000 rows are zero-volume sports parlays.

### Quality gates

- Binary outcome probabilities sum to ~1.0 (±0.02).
- `bid ≤ last ≤ ask`; reject a crossed book.
- Volume is cumulative; a decrease is a data error or restructure, never real.
- Spread > 25% marks the row **untradeable** rather than dropping it — keep the history, don't price
  off it.

None of these catch an internally-consistent bad value, which is exactly how the corrupt USDINR
daily bar got through. The real protection is the **JSONL append**: raw values land on disk before
interpretation, so a bad gate can be re-run against history rather than having silently discarded it.

### Cadence

- **Nightly sweep** — full universe across all venues, builds odds history.
- **On-demand refresh** — re-pull the shortlist immediately before proposing, so entry prices are
  honest.

Polymarket and Manifold need no auth; Kalshi needs curl-based transport. 250ms between pages,
exponential backoff on 429/5xx, resumable.

## 4. Proposition mapping

Two distinct joins, and conflating them is the main failure mode.

**Market → proposition.** Does this venue contract express a proposition we already track? Runs as:
deterministic prefilter (topic keywords with negative filters, liquidity, horizon) → LLM on the
shortlist → **human confirms any new market-to-proposition link before it is used for cross-venue
comparison.**

That human step is not ceremony. Kalshi publishes `rules_primary` *because resolution criteria
differ between venues*. Two contracts that read identically can settle differently — different data
source, cutoff, or rounding. An unverified mapping doesn't produce arbitrage; it produces a bet on a
technicality nobody read.

**Claim → proposition.** Which sourced claims bear on this statement? A proposition with no matching
claim gets **no view** — it stays tracked (so §6 can still flag price moves on it) but we do not
forecast it. No sourced view, no call.

## 5. Forming a view — `scripts/propose.py`

LLM on the shortlist only, sonnet, forced structured output: `our_prob`, `confidence`, `claim_ids[]`,
`rationale`, and **`no_view` as a first-class allowed answer.** A model asked to find edge in 40
propositions will find 40 edges unless abstaining is explicitly cheap.

### Edge is per venue, not per view

Edge is **not** `our_prob − mid`. You cross the spread, and the spread differs by venue:

```
YES: edge = our_prob − ask
NO:  edge = bid − our_prob
```

One view can be tradeable on one venue and not another. That is the point of the split.

**Threshold: 10 percentage points minimum.** Prediction markets are well-calibrated in aggregate;
the honest prior is that the market is right. With zero measured forecasting skill, the threshold
starts punitive and comes down only if Brier scores earn it.

### The favorite-longshot trap

Most of the candidate board sits at p = 0.001–0.07. Prediction markets have a documented
favorite-longshot bias, so a naive engine will repeatedly "discover" it should sell longshots. That
trade wins 99 times and returns everything on the hundredth, while producing **a beautiful hit rate
that means nothing.** Proposals below p<0.05 or above p>0.95 are flagged and require explicit
override, and the scorecard reports Brier and P&L, **never hit rate alone**.

### Sizing

`stake_units` 1–5 from edge × confidence, **quarter-Kelly capped at 5% of bankroll**. Full Kelly
assumes your probabilities are correct; ours are unvalidated, and Kelly's failure mode under
overconfidence is ruin, not underperformance.

## 6. Cross-venue disagreement — the day-one signal

When two venues carry the same **confirmed** proposition at materially different prices, that gap is
information *before we have any forecasting skill at all*. It is the only component of this system
that can work immediately.

**Gate it on all four, or it is noise:**

1. **Mapping is human-confirmed** (§4).
2. **Resolution rules materially match** — surfaced side by side for reading, never auto-approved.
3. **Liquidity floor on BOTH sides.** A live example found during design: Polymarket priced Fed-raise
   at ~0.309 with $368k liquidity while Manifold priced it 0.2205 — an 8.7-point gap. But that
   Manifold market had **5 unique bettors and 100 total liquidity.** The gap was thinness, not
   disagreement. Without a two-sided floor this signal is a thin-market detector.
4. **Play money is not price discovery.** Manifold gaps are logged and never sized on.

## 7. The daily loop — two alerts, and the second is the better one

The knowledge base updates daily. The valuable daily output is not *what we know* but **what
changed, and which live propositions it bears on.**

**Alert A — opportunity.** A claim changed → a proposition depends on it → the market has not moved.

**Alert B — research gap.** A market moved sharply → we have **no claim explaining it.**

Alert B is the one that closes the loop. The market becomes a *gap detector for the knowledge base*,
pointing the next day's research at exactly what we are missing. This workspace missed a 21.4pp
rural-versus-urban monsoon spread for months because every screen ranked securities and nothing
watched groups; Alert B is the same correction applied to propositions.

Output lands in `journal/` alongside the existing daily notes, and feeds the review queue.

## 8. Review UI

FastAPI + HTMX, localhost, four screens.

### Review queue

```
PROPOSITION  Fed raises rates at the September 2026 FOMC          20d

  Polymarket   bid 0.300 / ask 0.310   $368k     edge +14.0pts   [3 units]
  Manifold     p 0.2205                 5 traders  — play money, not sized
  Kalshi       (no confirmed mapping)                  [map it ▸]

OUR VIEW  0.45   confidence medium
WHY  ▸ fed-may-hike-next          reported   2026-08-26   ← 1 day old
     ▸ rate-cut-cycle-is-over     reported   2026-08-25

⚠ odds moved 0.285 → 0.310 since proposal (4h). Edge was +16.5, now +14.0.

[ accept ]  [ adjust prob ]  [ reject ▾ ]
```

**Claim provenance is inline and unmissable** — tier, date, age, rendered so a `reported` claim looks
visibly weaker than a `verified` one. On 2026-08-27 this repo was found stamping 85 of 92 notes
`verified` against a ledger that said otherwise; a review screen that hides tiers is that same
confidence-laundering machine with better CSS.

**Odds drift is computed at render.** If drift takes edge below threshold, the card **auto-demotes to
`expired`** rather than allowing acceptance on a stale price.

**Rejection is categorical**: `market is right` / `claim too weak` / `horizon too long` / `illiquid` /
`don't understand it` / `other`. Countable, so that in six months *"you reject 60% for 'claim too
weak' and those resolve in your favour 55% of the time"* is answerable.

### Open book
Entry vs live odds per venue, unrealised paper P&L, days to resolution, underpinning claims. **Any
position whose claim has since been contradicted is flagged** — the Dixon lesson, where a written
invalidation had already triggered two quarters before anything looked.

### Scorecard
Brier vs market Brier, and a **calibration plot** bucketing calls by stated probability, predicted
against actual, **with n shown per bucket**. A bucket with 3 calls is decoration.

### Proposition browser
Search, filter, manual view entry, and the mapping queue. Manual views get `proposed_by='human'` and
score separately. If the engine is worse than the human, that needs to surface early.

**Stack:** server-rendered Jinja + HTMX, ~6 endpoints, inline SVG charts, no CDN.

## 9. Resolver and scorecard — `scripts/resolve.py`

Nightly, after ingestion. Polls **by market id** for every open position.

### Two questions, two numbers

```
Was I more accurate?   Brier vs market Brier — both use the MID at entry
Did I make money?      paper P&L — uses the ASK or BID actually crossed
```

Scoring *accuracy* against the mid is right — the mid is the market's honest forecast. Scoring *P&L*
against the mid is wrong — you never traded there. Keeping both lets a call be **more accurate than
the market and still lose money on the spread**, the case that says the edge is real but the venue
eats it.

```
brier        = (our_prob − outcome)²
market_brier = (mid_at_entry − outcome)²
beat_market  = brier < market_brier
pnl_paper    = YES: outcome − ask_at_entry        per unit staked
               NO:  bid_at_entry − outcome
```

### Resolution is not always clean

Polymarket settles via UMA oracle and outcomes get disputed. Store the raw payload, mark disputed
markets `pending_dispute`, and **never score a disputed resolution until it settles.** A market that
resolves against us and flips on appeal must not sit in the record as a loss — and must not be
quietly deleted either.

Markets expiring unresolved get `void`, excluded from Brier, logged separately. Voids clustering on
one venue or topic is a problem worth surfacing.

**A proposition resolves once**, even if three venues resolve it at different times. Venue-level
disagreement on the *outcome* is a loud alarm, not an average: it means the mapping was wrong.

### The gate

```
CALIBRATION GATE: 0 resolved, 50 needed for a directional read
                                200 for a confident one
Until then this measures nothing.
```

The arithmetic is unforgiving: distinguishing a Brier of 0.23 from a market's 0.25 needs hundreds of
resolved calls. At a 126-day median horizon this is plausibly **a year** to a real answer. Better
written on the screen now than discovered at call 40. Multi-venue helps sample size somewhat, but
correlated positions on one proposition are **not** independent observations and must not be counted
as such.

### The assumed result

**The base case is that we lose to the market**, which aggregates money from people doing this full
time. `beat_market` is reported as a **rate with a confidence interval**, never a count, and when the
interval spans 50% the scorecard prints *"indistinguishable from chance"* rather than a number that
invites a story.

**Real-money unlock requires all three:** ≥50 resolved, `beat_market` interval entirely above 50%,
and positive paper P&L after spread.

## Out of scope

- Real-money execution, wallets, crypto rails.
- Public hosting, auth, or selling insight as a product — that is gated on the same calibration
  evidence as real money. Selling a forecast before measuring it is the same error as publishing an
  unearned hit rate.
- Metaculus and PredictIt (403 unauthenticated).
- Indian prediction platforms (legally grey).
- Automated entry without human approval.

## Open questions for implementation

1. LLM cost per nightly run at ~40 propositions — measure before scaling the shortlist.
2. Whether `sources.json` needs an explicit `topics[]` field for the claim→proposition join.
3. Bankroll notional for paper sizing, to make `stake_units` meaningful.
4. Whether resolution-rule comparison can be assisted by a model or must stay fully manual. Start
   manual; revisit only with evidence.
