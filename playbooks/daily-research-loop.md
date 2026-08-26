# Playbook — the daily research loop

The cycle to run every trading day. Roughly 30-45 minutes of work; the scripted parts are
seconds. Steps are ordered so that data comes before opinion, and scoring comes before
new ideas.

## 1. Collect (scripted)

```bash
cd ~/market-intel
uv run scripts/fetch_daily.py --period 3y
uv run scripts/report_daily.py --write
```

Writes `data/daily/YYYY-MM-DD.json` and `journal/YYYY-MM-DD-data.md`.

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

1. **Macro** — crude, USDINR, US 10-year, gold and silver, dollar index. These set the regime.
2. **Breadth** — % above 200 DMA and the uptrend/downtrend/choppy split. This decides whether
   an index view is worth having at all.
3. **Sector rotation** — the median-member table. Look for a sector where the *median* member
   is moving, not one where a single megacap is dragging the average.
4. **Extremes** — new highs, new lows, RSI below 35 and above 70. These are where the questions
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
