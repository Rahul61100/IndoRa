# Playbook — the daily research loop

The cycle to run every trading day. Roughly 30-45 minutes of work; the scripted parts are
seconds. Steps are ordered so that data comes before opinion, and scoring comes before
new ideas.

## 1. Collect (scripted)

```bash
cd ~/market-intel
for m in india us crypto; do
  uv run scripts/fetch_daily.py --universe $m --period 3y
  uv run scripts/report_daily.py --market $m --write
done
uv run scripts/fetch_flows.py
```

Writes `data/daily/<market>/YYYY-MM-DD.json`, `journal/YYYY-MM-DD-<market>-data.md`, and appends
to the ledgers in `data/flows/`.

**Run `fetch_flows.py` every single day without exception.** NSE serves only the latest session,
so a skipped day is a permanently missing row — the history cannot be backfilled. The stablecoin
and TVL series backfill themselves; the India FII/DII series does not.

Read the quality-flag block at the bottom of the brief first. Anything flagged is unusable
until confirmed elsewhere — see `data-quality-rules.md`.

## 2. Score the open book (before forming any new view)

Open `positions/open-theses.md`. For each live thesis ask only these:

- Has the **invalidation condition** triggered? If yes, it is closed. Not "watched", closed.
- Has the **catalyst date** passed without the catalyst? If yes, the thesis has decayed —
  either restate it with a new catalyst or close it.
- Is the **relative strength vs Nifty** worse than when the thesis was opened? If it has been
  worse for three consecutive weekly checks, the market disagrees and the burden of proof
  shifts back to the thesis.

Write the answer in the scorecard even when nothing changed. Especially when nothing changed.

## 3. Read the market

In this order, because each frames the next:

1. **Flows** — India FII/DII net, stablecoin supply, DeFi TVL. Read these *first*. Flows have
   explained more of what happened in all three markets than any valuation metric.
2. **The political economy layer** — promoter pledging and stake changes, bulk and block deals,
   regulatory or judicial actions on held names, policy and appointment news, and the next dated
   political catalyst. See `political-economy-layer.md`. In India this moves stocks harder and
   faster than earnings, and it is invisible in every price series and every financial statement.
3. **Macro** — crude (**curve shape and crack spreads, not just flat price**), USDINR, **USDJPY
   and BOJ policy**, US 10-year and 30-year, gold and silver, dollar index. These set the regime.
4. **Breadth** — % above 200 DMA and the uptrend/downtrend/choppy split. This decides whether
   an index view is worth having at all.
5. **Sector rotation** — the median-member table. Look for a sector where the *median* member
   is moving, not one where a single megacap is dragging the average.
6. **Extremes** — new highs, new lows, RSI below 35 and above 70. These are where the questions
   are, not where the answers are.

## 4. Explain the anomalies

Anything the data shows that the current knowledge base does not explain is the day's real work.
Search for the cause. Three outcomes:

- It is a **data artifact** → add a rule to `data-quality-rules.md` and fix the fetcher.
- It is **noise** → note it and move on.
- It is **new information** → write a knowledge file and, if it touches an open thesis, update
  the scorecard.

## 5. Write the note

`journal/YYYY-MM-DD.md`, structured as:

```
## What changed
## What it means for the open book
## New or revised theses
## Open questions carried to tomorrow
```

Say what changed. The generated data brief already holds the table; do not restate it.

## 6. Promote durable lessons

If something learned today will still be true in six months, it belongs in `knowledge/` as its
own file, one fact per file, and gets a line in `knowledge/INDEX.md`. If it is only true this
week, it stays in the journal.

## Weekly (Sunday)

- Refresh `data/fundamentals/` for everything in the position groups.
- Re-read the last five journal notes end to end and look for a thesis being quietly restated
  each day without progress. That pattern is how a losing position survives.
- Check whether any knowledge file has been contradicted by the data since it was written.

## Extending to other markets

`fetch_daily.py --universe <name>` already takes a universe file. To add a market, write
`universe/<name>.json` and `universe/<name>-sectors.json` in the same shape. Nothing else in
the pipeline is India-specific except the benchmark symbol used for relative strength, which
is read from the `benchmarks` group.
