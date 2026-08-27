# Playbook — data quality rules

Every rule here exists because the data lied once and was caught. Add to it whenever that
happens again.

## Rules

**1. Yahoo's NSE sector indices carry multi-week history gaps.**
On 2026-08-26 every `^CNX*` sector index showed a 40-day hole. The first print after the hole
was rendered as a single-day move: Nifty Auto appeared to jump 7.0%, Metal 8.9%, Media 5.9%.
Independent reporting put Nifty Auto's actual session at +0.4%. **Never quote a sector index
one-day move from this source.** Sector rotation is computed from constituent baskets in
`universe/sectors.json`.

**2. Any index one-day move beyond 4%, or stock move beyond 15%, is suspect until confirmed.**
The fetcher flags these automatically. Confirm against a news source before it enters a note.

**3. A demerger or split makes long-window returns meaningless.**
`TMPV.NS` shows roughly -54% over a year. That is the Tata Motors demerger, not a drawdown.
Before treating any large negative long-window return as a signal, check for a corporate action.
Yahoo's adjustment for Indian demergers is unreliable in a way its split adjustment is not.

**4. Grouped downloads drop symbols that fetch fine alone.**
The fetcher already retries individually. If a symbol is still missing after the retry it is
genuinely unavailable — check whether it was renamed (LTIM), demerged (TATAMOTORS) or delisted.

**5. The last bar may be an incomplete session.**
An intraday bar shows volume 0 or an unusually low volume ratio. Treat the newest close as
provisional until the next day's fetch confirms it.

**6. Fundamentals decay faster than the file suggests.**
Anything in `data/fundamentals/` older than a week gets refreshed before it is quoted. Prices
move daily; the multiples derived from them go stale silently.

**7. Index P/E from aggregator sites is trailing and definition-dependent.**
Different sources publish materially different Nifty P/E numbers for the same day depending on
standalone vs consolidated and free-float treatment. Always name the source and the date.

## The general rule

The fetcher is the only thing that produces prices. If a number appears in a note without a
matching row in that day's snapshot, it should not be there.

**8. Derive the prior close from the intraday series, never from Yahoo's daily bar.**
On 2026-08-27 the intraday monitor reported USDINR up **2.13% overnight** — a move that would
have been genuine news. It was fabricated. Yahoo's 26 August daily bar for USDINR carried
`Close 93.546` against a `High` of 95.412, with the true rate near 95.5. The bad close became
the reference point and manufactured a 2% gap.

A first fix — reject a prior close deviating more than 8% from the trailing median — **failed**,
because the corruption was only 2.25% off. Small enough to pass a tolerance check, large enough
to look like a story. That is the dangerous size.

The working fix: the 5-minute series spans two sessions, so **the last bar of the prior session
is the real prior close** and needs no sanity check at all. The daily bar is now only a fallback
for tickers whose intraday history does not reach back a session.

**The general lesson: prefer a source that cannot be wrong over a check that decides whether a
source is wrong.** Validation thresholds always have a gap, and the errors that fit through it
are exactly the plausible-looking ones.
