---
title: "Yahoo's FX daily bars are wrong often enough to be unusable"
market: general
type: method
confidence: verified
tags: [general, method, verified]
updated: 2026-08-27
---

# Yahoo's FX daily bars are wrong often enough to be unusable

Third occurrence, now across three different pairs. **Any FX number in this workspace that was
taken from a Yahoo daily bar is suspect and should be re-derived.**

| pair | date | Yahoo daily close | intraday actual | error |
|---|---|---|---|---|
| USDINR | 2026-08-26 | 93.546 | 95.402 | **−1.95%** |
| EURUSD | 2026-08-19 | 1.158 | 1.168 | −0.87% |
| USDJPY | 2026-08-19 | 159.550 | 158.172 | +0.87% |

The USDINR bar reads `O 93.546  H 95.412  L 93.546  C 93.546`. The session never traded below
95.402. Computing a one-day return off it the next morning produces **+2.1%** when the real move
was **+0.12%** — a fabricated 2% currency move, which is a macro event that did not happen.

## Why every check I tried failed

The bad bar is **internally self-consistent**. Its close sits inside its own high/low. Its open
equals its low. There is no arithmetic relationship inside the bar that is violated.

- A tolerance check on the size of the move failed — the first version used 8%, and the corruption
  was only 1.95%.
- An OHLC self-consistency check passes cleanly. It was run explicitly against this bar and
  returned `bar is self-consistent`.

A check can only catch a source being wrong in a way the check anticipated. This one was wrong in
a way that looks exactly like a real market move.

## The rule

**Prefer a source that cannot be wrong over a check that decides whether a source is wrong.**

The last intraday print of a session *is* that session's close. There is nothing to validate —
derive it and the failure mode is gone rather than detected. `scripts/fx.py` does this for five
pairs and additionally prints a warning whenever the daily bar disagrees with the derived close by
more than 0.5%, purely so the scale of the problem stays visible.

## Where this bites beyond FX

The same reasoning was already applied once to equity prior-closes in `scripts/intraday.py`. The
general shape — a vendor's aggregated bar disagreeing with the ticks it was aggregated from — has
now appeared in two separate data families from the same vendor. Treat any *derived* series
(daily bars, weekly bars, adjusted closes, returns) as the vendor's opinion, and the underlying
prints as the fact.

Related: [[india-aggregate-earnings-are-three-companies]]
