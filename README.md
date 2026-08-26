# market-intel

A daily equity research loop. India first; the pipeline is market-agnostic and other markets
get added as new universe files.

## Quick start

```bash
cd ~/market-intel
uv run scripts/fetch_daily.py --period 3y     # pull OHLC, derive technicals, flag bad data
uv run scripts/report_daily.py --write        # generate journal/YYYY-MM-DD-data.md
```

No API keys and no paid data. `uv` resolves the script dependencies inline from the PEP 723
header in each script — nothing needs installing.

## Read these in order

1. `CLAUDE.md` — what this workspace is and how to work in it
2. `playbooks/daily-research-loop.md` — the cycle to run each day
3. `positions/open-theses.md` — what is live and how each thesis dies
4. `knowledge/INDEX.md` — the durable lessons

## Structure

```
scripts/     fetch_daily.py, report_daily.py
universe/    india.json (tickers by role), sectors.json (constituent baskets)
data/daily/  one JSON snapshot per day + latest.json
data/fundamentals/  dated valuation snapshots
knowledge/   one durable fact per file
playbooks/   repeatable procedures
positions/   live theses + running scorecard
journal/     YYYY-MM-DD.md written, YYYY-MM-DD-data.md generated
```

## Adding a market

Write `universe/<market>.json` in the same shape and run
`uv run scripts/fetch_daily.py --universe <market>`. Relative strength uses the first entry of
the `benchmarks` group, so put the local index there.

## Not investment advice

This is a personal research log. Nothing in it is a recommendation, and every figure is a
point-in-time capture that starts decaying the moment it is written.
