---
title: "Same-day correlation across timezones is a measurement artifact"
market: cross
type: method
confidence: verified
tags: [cross, method, verified]
updated: 2026-08-27
---

# Same-day correlation across timezones is a measurement artifact

Method rule, established 2026-08-26 after I computed a nonsense number and caught it.

India closes around 10:00 UTC; the US opens around 13:30 UTC. **A same-day daily return in India
and the US is not contemporaneous** — India reacts to the *previous* US session. Correlating them
same-day measures nothing and reports it as a low number.

Measured both ways, two years of daily returns:

| Pair | Same-day | US/BTC lagged 1 day |
|---|---|---|
| India vs US | 0.08 | **0.07** |
| India vs BTC | 0.02 | **0.16** |
| US vs BTC | **0.43** | (same session, no lag needed) |

In this case the lag barely moved the India-US number — so **the low correlation is real, not an
artifact.** But the India-BTC figure went from 0.02 to 0.16, which is an eightfold change, and
that one *was* the artifact. The rule holds even where this instance was benign.

**The substantive finding underneath:** Indian equities are close to uncorrelated with the US on
a daily basis — 60-day rolling India-vs-lagged-US correlation is **0.03 now, mean 0.09, two-year
range -0.28 to +0.40.** India is genuinely domestically driven. US-BTC is **0.30 now against a
0.49 mean, range 0.23 to 0.68** — crypto is a US risk-asset proxy, and materially so.

**How to apply:** always lag the later-opening market by one session when correlating across
timezones, and report both figures so the artifact stays visible. Note the consequence for
[[cross-market-lead-lag-is-the-edge]] — running three markets *does* deliver real diversification
in India's case, on top of the lead-lag value. But crypto adds far less than it appears to,
because it is 0.3-0.5 correlated with US equities and therefore mostly the same bet.
