---
title: "Dixon's profit growth is not coming from operations"
market: general
type: finding
confidence: verified
tags: [general, finding, verified]
updated: 2026-08-27
---

# Dixon's profit growth is not coming from operations

The data conflict logged as `dixon-pat` — a screen showing PAT −36% YoY against our own TTM pull
showing +119% — is settled, and **neither number describes what is happening.** Both compare the
wrong things. The honest decomposition, Q1 FY27 against Q1 FY26 like for like:

| | Q1 FY26 | Q1 FY27 | change |
|---|---|---|---|
| Revenue | ₹12,835.7cr | ₹15,547.7cr | **+21.1%** |
| Operating income | ₹389.7cr | ₹356.2cr | **−8.6%** |
| Net income | ₹225.0cr | ₹663.4cr | **+194.8%** |
| Operating margin | 3.04% | **2.29%** | −75 bps |

Revenue grew a fifth. Operating profit *fell*. Net profit nearly tripled. Net income came in at
**1.86× operating income** — the profit is below the line, not from the business.

## The margin has been falling for five straight quarters

3.47% → 3.04% → 2.96% → 2.89% → **2.29%**

Monotonic, and not noise: the largest single-quarter drop is the most recent one, on the largest
revenue quarter in the company's history. Volume up, money made per unit of it down — the
characteristic signature of contract-manufacturing scale that is being bought rather than earned.

## This triggered a written invalidation I had already published

The Dixon thesis in `positions/theses.json` lists, verbatim, **"margin below ~3%"** as an
invalidation condition. The operating margin has been below 3% for **three consecutive quarters**
and is now 71 bps under the line. It did not trigger this quarter — it triggered two quarters ago
and nothing in the process looked.

Why nothing looked is a process defect, not a research one. `tools/score.py` mechanically checks
price and revision diffusion. The margin condition was typed `manual`, so it printed as a daily
REVIEW line rather than being evaluated. That review line is what prompted this pull — so the
scorecard did its job — but a condition a script *could* check should never be left to a human eye
that has to be in a good mood. **Fixed the same day: `margin_below` is now a mechanical check type.**

## The forward multiple already said it

Trailing P/E 43.2, forward P/E **52.2**. A forward multiple *above* the trailing one means consensus
expects earnings to fall — roughly −17% from trailing EPS of ₹340. The market had already worked out
that the trailing number is inflated by something non-recurring. The thesis was paying 43× for
growth consensus does not think is there.

## Decision

**CLOSED.** Not capped again — closed. The EMS thesis rested on operating leverage arriving with
scale; the reported data shows operating *deleverage* arriving with scale. The three caps already
placed on this position (memory BOM shock, Mobile PLI 2.0 disbursing nothing, and the moat *being*
the China dependency) were all about future risks. This is not a future risk. It is in the numbers now.

The position was capped three separate times before being closed. **A thesis that needs three caps
has already been falsified and is being kept alive by adding qualifiers.** Cap, cap, cap, close is
the pattern to watch for in the rest of the book.

## Caveat on the source

From `yfinance` quarterly financials; the Sep 2025 quarter is missing from the series, which does
not affect any comparison above (Jun 2026 and Jun 2025 are both present). The operating-income line
is EBIT. This has **not** been checked against a company filing and should be before the number is
repeated externally.

**Source:** own pull of quarterly financials, decomposed in this repo. **Not** checked against a company filing — see the caveat above before repeating any figure externally.

Related: [[india-diversification-concentrated-on-washington]] · [[india-vs-north-asia-the-trade-already-happened]]
