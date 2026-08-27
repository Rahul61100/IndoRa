# SESSION STATE — read this first

_Generated 2026-08-27 09:08 UTC by `tools/session_state.py`. Regenerate at the end of every session._

## Start here, in this order

1. `CLAUDE.md` — how this workspace works
2. **This file** — where things stand right now
3. `positions/open-theses.md` — the live book, invalidation conditions, and the
   running scorecard. **Score the open book before forming any new view.**
4. `playbooks/daily-research-loop.md` — the cycle to run
5. `playbooks/political-economy-layer.md` — who is positioned, who holds the levers,
   who benefits, what is on the calendar. Runs daily, second, right after flows.
6. `knowledge/INDEX.md` or the `MOC-*` hub notes — the durable facts

## Refresh the data before reasoning about any price

```bash
cd ~/market-intel
for m in india us crypto; do
  uv run scripts/fetch_daily.py --universe $m --period 3y
  uv run scripts/report_daily.py --market $m --write
done
uv run scripts/fetch_flows.py      # MUST run daily -- NSE serves only the latest session
uv run scripts/regime.py           # regime label per market
uv run scripts/portfolio_risk.py   # correlation, effective bets, USD-adjusted returns
uv run tools/kb.py all             # frontmatter, MOCs, link check
```

## Data freshness

| Series | Last updated | Size | Notes |
|---|---|---|---|
| india | 2026-08-26 | 98 tickers | 11 quality flags |
| us | 2026-08-26 | 119 tickers | 0 quality flags |
| crypto | 2026-08-26 | 46 tickers | 4 quality flags |
| India FII/DII | 2026-08-26 | 1 rows | flows ledger |
| Stablecoin supply | 2026-08-27 | 3194 rows | flows ledger |
| DeFi TVL | 2026-08-27 | 3119 rows | flows ledger |

## Knowledge base: 70 notes

Load-bearing corrections — **these overturn things earlier sessions asserted**:

- `CORRECTION-india-erp-is-negative` — the 6.85% G-sec beats the 4.89% earnings yield.
  "Cheap versus its own history" is not cheap.
- `CORRECTION-india-earnings-growth-was-4-5-percent` — the "+18%" was one quarter and
  60% of it was five stocks. FY26 grew 4.5% against 12-15% expected.
- `CORRECTION-india-did-not-halt-russian-crude` — India was outbid by China, not acting
  on policy. Not reversible by diplomacy.
- `CORRECTION-ieepa-tariffs-were-struck-down` — the Supreme Court voided the authority
  6-3 in February 2026.
- `announced-is-not-disbursed` — approved, awarded and paid are three different things.

## Standing rules that are easy to forget

- **Never state a price, multiple or return without pulling it that session.**
- **Quote Indian returns in BOTH currencies.** INR-only overstates the case badly.
- **Check revision direction before calling anything a de-rating.** Trailing beats and
  forward cuts routinely coexist.
- **Decompose every headline growth number** before using it.
- **Ask: approved, awarded, or paid?**
- **Read the oil curve and crack spreads, not the flat price.**
- Confidence tags: `verified` / `reported` / `degraded` / `not found`. **"Not found"**
  **never means "does not exist."**
- WebSearch is capped at **200 calls per session, shared with all subagents**. Budget it;
  roughly 5-8 deep agents, not 14. Put premises in the *question*, not the framing —
  an agent that inherits a wrong assumption researches around it.
- **Do not publish artifacts without asking** — pass this down to subagents too.

## Scorecard — most recent entries

| Date | Thesis | Status | Note |
|---|---|---|---|
| 2026-08-26 | Dixon | **risk added, capped** | Memory BOM shock + shipment contraction; found via the US universe |
| 2026-08-26 | L&T | thesis sharpened | Capex divergence is execution, not demand — equipment over EPC |
| 2026-08-26 | **Whole India book** | **premise overturned** | ERP negative ~200bp; FY26 EPS grew 4.5% not 18%; EM weight halved |
| 2026-08-26 | HDFC Bank (MEDIUM) | **cut to half, no adds** | Among the largest FY27 downgrades |
| 2026-08-26 | India equities | **new positions frozen** | Until the "why not G-secs at 6.85%" question is answered |
| 2026-08-26 | **HAL** | **cut to half, stop tightened** | Tejas Mk1A 2+ yrs late; MoD reportedly weighing penalties |
| 2026-08-26 | **L&T** | **thesis restated** | Headline wins are European, not Indian NIP; NHAI awards at 7-year low |
| 2026-08-26 | Dixon | second risk logged | Mobile PLI 2.0 cleared 15 Jul, nothing disbursed |
| 2026-08-26 | HDFC Bank | **cut reason narrowed** | −26% was ₹35,000cr of FII selling in one quarter; FIIs returning to financials since 22 Aug |
| 2026-08-26 | Reliance | **conviction raised** | Promoter bought ~₹9,000cr in July, stake to 50.48% |
| 2026-08-26 | Infosys | half the setup in place | FII IT holdings at a 4-year low; revisions still negative |
| 2026-08-26 | ONGC (closed) | **invalidation had already fired** | Windfall levy was reintroduced in March 2026 — I wrote the condition against a false premise |

## Questions carried forward

- (none recorded in the latest journal)

## Repo

Remote: `git@github-personal:Rahul61100/IndoRa.git`

```
03bde90 Add vault Home note and one-command refresh
066f6a1 Fix a fabricated 2% rupee move in the intraday monitor
806d41b Add session continuity, Obsidian vault tooling, and the live market-hours loop
61a85d5 India policy calendar: windfall tax is back, 2026 state elections already done
1208afb US policy map: two shutdowns, a tariff-refund fiscal hole, and a Fed weighing a hike
be68ccc Positioning data partly reverses this morning's HDFC Bank cut
40292f3 Political economy layer hits three open positions
c32d522 US fundamentals: estimates rising 15% while India's were cut 9%
8f804a9 Record the session-wide web search cap and its effect on confidence
89c4348 Add the political economy layer to the daily loop
c998beb Add eight-sector India coverage and the NSE IPO supply event
e89e065 Gold beat the Nifty on every horizon; India's capex is Delhi's and front-loaded
```

Working tree: **UNCOMMITTED CHANGES PRESENT**

## The one thing to hold on to

This workspace has **no evidence of skill yet.** Not a single thesis has been scored
forward to its horizon. Phase 3 of `playbooks/roadmap.md` is the gate, and it needs
~30 scored theses. Any backward-looking number that flatters the book is measuring
hindsight — see `backtests-of-chosen-names-measure-hindsight`.
