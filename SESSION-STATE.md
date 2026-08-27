# SESSION STATE — read this first

_Generated 2026-08-27 09:58 UTC by `tools/session_state.py`. Regenerate at the end of every session._

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
| india | 2026-08-27 | 88 tickers | 0 quality flags |
| us | 2026-08-27 | 119 tickers | 0 quality flags |
| crypto | 2026-08-27 | 46 tickers | 4 quality flags |
| India FII/DII | 2026-08-26 | 1 rows | flows ledger |
| Stablecoin supply | 2026-08-27 | 3194 rows | flows ledger |
| DeFi TVL | 2026-08-27 | 3119 rows | flows ledger |

## Knowledge base: 78 notes

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
| 2026-08-27 | **Reliance** | **tension flagged** | Promoter bought ~₹9,000cr in July; FY+1 EPS cut 5.23% in 30 days |
| 2026-08-27 | **SHORT bucket** | **hurdle raised** | Needs 10-12% gross edge over a long hold, after tax — never applied before |
| 2026-08-27 | Buyback names | stale note corrected | Budget 2026 restored capital-gains treatment for non-promoters |
| 2026-08-27 | **SBI, NTPC** | **short build-up flagged** | Both showing F&O short build-up; SBI flipped from long in a day — tentative |
| 2026-08-27 | Flow reading | **method corrected** | FIIs net cash buyers while ~1:8.25 short index futures — cash alone was misleading |
| 2026-08-27 | **HAL** | **CLOSED** | 199 forged test certificates, fatal crash, fleet grounding, zero Mk-1A delivered |
| 2026-08-27 | **ICICI Bank** | **capped, CEO thread tracked** | 6 GST notices >₹1,350cr; reappointment contested to RBI, escalated 24 Aug |
| 2026-08-27 | Bharti | exit confirmed independently | Mittal + Singtel sold >$4bn across 2025 |
| 2026-08-27 | Dixon | **data conflict — resolve** | Screen says PAT −36% YoY; our pull says TTM +119% |
| 2026-08-27 | SBI | false positive avoided | RCom fraud headlines are SBI *detecting* fraud, not committing it |
| 2026-08-27 | SBI | supply fact logged | Largest selling shareholder in the NSE IPO |
| 2026-08-26 | ONGC (closed) | **invalidation had already fired** | Windfall levy was reintroduced in March 2026 — I wrote the condition against a false premise |

## Questions carried forward

- (none recorded in the latest journal)

## Repo

Remote: `git@github-personal:Rahul61100/IndoRa.git`

```
8f96702 FIIs are short the index and long single stocks -- cash flow alone was misleading me
69b8e45 Short-horizon trades now need a 10-12% tax edge to earn their place
734dd90 Shriram Finance work-up, owed three times, now done against primary filings
90679fa Build the estimate-revisions collector -- the gap that cost the Infosys call
2882f30 Close HDFC Bank: the driver was governance, not NIM
94babf9 Q1 FY27 GDP preview, and flag a figure I have been quoting wrong
03bde90 Add vault Home note and one-command refresh
066f6a1 Fix a fabricated 2% rupee move in the intraday monitor
806d41b Add session continuity, Obsidian vault tooling, and the live market-hours loop
61a85d5 India policy calendar: windfall tax is back, 2026 state elections already done
1208afb US policy map: two shutdowns, a tariff-refund fiscal hole, and a Fed weighing a hike
be68ccc Positioning data partly reverses this morning's HDFC Bank cut
```

Working tree: **UNCOMMITTED CHANGES PRESENT**

## The one thing to hold on to

This workspace has **no evidence of skill yet.** Not a single thesis has been scored
forward to its horizon. Phase 3 of `playbooks/roadmap.md` is the gate, and it needs
~30 scored theses. Any backward-looking number that flatters the book is measuring
hindsight — see `backtests-of-chosen-names-measure-hindsight`.
