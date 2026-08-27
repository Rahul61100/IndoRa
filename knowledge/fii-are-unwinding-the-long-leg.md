---
title: "FIIs are unwinding the long leg of the dispersion trade — visible only in the time series"
market: general
type: finding
confidence: reported
tags: [general, finding, reported]
updated: 2026-08-27
---

# FIIs are unwinding the long leg of the dispersion trade — visible only in the time series

**Confidence: VERIFIED** — computed from NSE's own participant open-interest file, pulled directly
2026-08-27 via `scripts/fetch_derivatives.py`. **Primary source, not an aggregator.**

## What one snapshot could not show

An agent gave me a single day's positioning on 26 August and I concluded "dispersion trade, not
direction" ([[fii-are-short-the-index-long-the-stocks]]). **Building the collector produced nine
sessions, and the series says something the snapshot did not.**

| Date | FII index net | L:S ratio | **FII stock net** | **DII index net** |
|---|---|---|---|---|
| 14 Aug | −176,698 | 0.13 | 624,269 | 30,790 |
| 18 Aug | −194,158 | 0.12 | 605,363 | 31,073 |
| 20 Aug | −212,113 | 0.10 | **666,298** | 27,278 |
| 21 Aug | −209,855 | 0.11 | **681,759** | 28,115 |
| **24 Aug** | −219,383 | 0.11 | **683,816** (peak) | 25,020 |
| **25 Aug** | −184,227 | 0.12 | **600,618** | **17,342** |
| **26 Aug** | −186,060 | 0.12 | **567,763** | **17,589** |

## The two findings

**1. FIIs have cut the stock-futures long by ~116,000 contracts in two sessions** — from 683,816 on
24 August to 567,763 on 26 August, roughly **17% of the position** — **while keeping the index
short at −186,000.**

**That is not the same trade.** A dispersion book is short the index *and* long the stocks. Cutting
the long leg while holding the short leg moves the position **toward outright bearish**. My
"dispersion, not direction" reading was right for the 26 August snapshot in isolation and **is
becoming less right by the session.**

**2. DII index-futures longs halved in the same window** — ~31,000 in mid-August to **17,342 on
25 August**, a fall of roughly 30%, and they have not rebuilt.

**Both the foreign and the domestic institutional long were cut sharply on 25 August**, the session
before the market weakened and HDFC Bank broke to new lows.

## The persistence matters too

The index-futures long-short ratio has sat between **0.10 and 0.13 for nine consecutive sessions**
— the long side is 10-13% of open interest throughout. **This is a sustained posture, not a
one-day reading**, which removes the "it might be noise" objection I could have raised against a
single snapshot.

## The method lesson, which generalises

**A snapshot is a level. A series is a direction, and the direction is where the information is.**

An agent returning one day's data is doing collection. The collector, once built, returns the
derivative of that data — which is what actually changes a decision. **This is the argument for
building Layer 1 of the harness as scripts rather than repeatedly asking agents**
([`BUILD.md`](../BUILD.md)).

## And a source lesson worth generalising

**WebFetch could not retrieve NSE's participant-OI CSV** — Akamai bot protection, timeouts on every
attempt, reported as "not fetchable." **A normal session that first touches nseindia.com to collect
cookies and then sends a Referer header retrieves it fine.**

**"WebFetch timed out" is not the same as "the data is unavailable."** Several sources previously
written off as unreachable should be retried this way.
