---
name: prediction-market-oracle-research
description: Use a prediction market as a research signal — market-implied probability, its quality, and what it is evidence of. Use when reading a Polymarket or other venue price into a thesis, a dashboard, or the review queue, and when deciding whether a market is usable at all.
---

# Prediction markets as a signal

Adapted from ECC's `prediction-market-oracle-research` skill (MIT).

## Guardrails

- **A market price is not a probability of truth.** It is the price at which two people stopped
  disagreeing, under that venue's rules, fee structure and participant mix.
- **No investment advice**, here or in anything this workspace emits.
- Keep venue mechanics, liquidity, incentives and resolution rules **separate** from the implied
  number. A clean 0.62 on a market that resolves ambiguously is not a 62% chance of anything.
- Name manipulation risk, thin books, stale markets, and ambiguous resolution explicitly. They are
  the finding as often as the price is.

## This workspace's own rules apply first

- **Never reason about a price from memory.** Same rule as equities: refresh, then read. The
  ingested row in `predict/db.py` with its timestamp is the source, not recall.
- **A flagged row is unusable until a second source confirms it.** Stale prints and implausible
  moves are as real on a prediction venue as on an exchange — more so, because the book is thinner.
- **Scorecard before automation.** A signal earns its way into the loop by being scored over time,
  not by being interesting once.
- **A cap is a claim too.** Calling a market "too thin to use" is an assertion that needs the same
  evidence as using it would.

## Workflow

1. **Name the decision the signal is meant to inform.** If there isn't one, stop — this is
   entertainment, not research.
2. **Find the markets.** `predict/venues/polymarket.py` is the live ingester; `predict/ingest.py`
   normalizes into the store. One venue today, so **every conclusion is single-venue** until a
   second is wired — say so rather than implying consensus.
3. **Record the implied probability with its timestamp and source link.** Undated is unusable.
4. **Score the signal quality** before using the number:
   - liquidity and depth, not just volume
   - bid-ask spread — a wide spread means there is no single implied probability, there is a range
   - market age and time to resolution
   - trader concentration, where visible
   - **the resolution rule and who adjudicates it** — the most common defect, and the one that
     silently makes a number mean something other than what the title says
   - geography and account restrictions on the venue
5. **Compare against non-market sources** — filings, the political-economy layer, news, internal
   data. A market that merely echoes a headline adds nothing.
6. **Give a verdict: usable, weak, or unsuitable** for the stated decision. Not a shrug.

## What it is evidence of

The useful move is rarely "the market says 62%". It is one of:

- **Divergence** — the market disagrees with a thesis in `positions/open-theses.md`. Which one is
  carrying information the other lacks?
- **Repricing** — the number moved, and the move is dated. What happened between the two prints?
- **Base rate** — the market has priced this class of event repeatedly; the history is a base rate,
  and this workspace's standing rule is that **a claim must clear its base rate.**

## Integration patterns

Research context for a human · a dated signal beside internal metrics · a stored, retrievable
time-stamped observation · a threshold alert on probability, spread, or liquidity · scenario
comparison across outcomes. **Never automated execution.**

## Output

1. decision context · 2. market sources with timestamps · 3. signal quality · 4. comparison
sources · 5. verdict and integration recommendation · 6. caveats

End with:

```text
Prediction-market signals are informational inputs, not investment advice.
```
