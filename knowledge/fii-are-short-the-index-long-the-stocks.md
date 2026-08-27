---
title: "FIIs are short the index and long single stocks — the cash flow number was misleading me"
market: general
type: finding
confidence: verified
tags: [general, finding, verified]
updated: 2026-08-27
---

# FIIs are short the index and long single stocks — the cash flow number was misleading me

Verified 2026-08-27, data as at 26 August close. **Confidence: REPORTED** — NSE's own participant-OI
CSV timed out on every attempt (bot protection), so this is niftytrader.in republishing NSE data.
Re-verify from the primary CSV when a session-capable fetch is available.

## The positioning

| Segment | Long | Short | Net |
|---|---|---|---|
| **Index futures** | 25,651 | **2,11,711** | **−1,86,060 (net short)** |
| **Stock futures** | 34,25,528 | 28,57,765 | **+5,67,763 (net long)** |

**The index-futures long-short ratio is roughly 1:8.25** — the long side is only ~10.8% of open
interest. For scale, a 10:1 reading in August 2025 was reported as "notably extreme bearish." This
sits in the same zone.

**And over the last five sessions they added index-futures longs (+26,053) while trimming
stock-futures longs (−98,535).**

## Why this matters more than anything else in the F&O data

**I have been reading FII cash flows as a sentiment gauge.** On 26 August FIIs were **net buyers of
₹503 crore in cash** — which I reported as mild bullishness alongside DII buying of ₹6,425 crore.

**The derivatives book says that reading is wrong.** Short the index, long single stocks, is a
**dispersion or hedged-rotation trade — not a directional view.** They are expressing "these
specific stocks beat the index", not "India goes up."

**Any conclusion drawn from FII cash flow alone, without the derivatives position beside it, is
incomplete.** That applies retroactively to every flow reference in this workspace
([[who-is-actually-buying-india]], [[india-supply-versus-the-sip-bid]]).

## Volatility is priced for silence

**India VIX 10.94**, against a 52-week range of **8.72 to 28.90** — roughly the **bottom 11%** of
its own year.

That is into a three-week window containing **Q1 FY27 GDP on 31 August**
([[india-q1-fy27-gdp-preview]]), a **live Fed decision on 15-16 September** where three members
already voted to hike ([[the-fed-is-actively-weighing-a-hike]]), and **India's largest-ever IPO**
in the same month ([[nse-ipo-is-the-supply-event-that-matters]]).

**The options market is pricing all three as non-events.** Cash prices cannot show this — they
carry no expectations component. Term structure was not obtainable, so whether the complacency
extends to later expiries is unknown.

## The expiry calendar changed and I did not know

- **Nifty weekly expiry moved from Thursday to TUESDAY**, effective 1 September 2025
- **Bank Nifty lost weekly expiry entirely** on 20 November 2024 — **monthly only**, last Tuesday
- **August monthly expiry was Tuesday 25 August 2026**
- **Next Nifty weekly: Tuesday 1 September. Next monthly, both indices: Tuesday 29 September.**

**Max pain** — Nifty **24,200** for the 1 September weekly against spot ~24,150; Bank Nifty
**57,800** for the 29 September monthly against spot ~57,615. Both already gravitating to the next
expiry's centre of gravity two sessions after the last one settled.

**PCR diverges:** Nifty roughly neutral at 0.6-0.8 (the source's own pages disagree — unresolved),
but **Bank Nifty at 1.10, clearly put-heavy.** Banks carry more defensive positioning than the
broad index.

## Single-stock positioning confirms the rotation I saw in cash

On 27 August: **short build-up in HDFC Bank (−1%), NTPC (−1.6%), SBI (−0.53%), Reliance**;
**long build-up in ICICI Bank (+0.83%), Kotak (+1.8%), Axis (+0.4%), Tech Mahindra, Sun Pharma.**
Bharti Airtel showed short build-up on 26 August (−1.5%).

**That is a pairs rotation *within* financials**, and it independently confirms the HDFC-Bank-down
/ ICICI-up divergence seen in cash ([[session-2026-08-27-india]]). A sector-level read — "banks
being sold" — would have flattened it into noise.

**Three names I hold are on the short-build-up side: HDFC Bank, SBI and NTPC.** SBI is new
information; it flipped from long build-up on 26 August, so treat it as tentative.

## Two footnotes worth keeping

**A suspected "fat-finger" trade in Bharti Airtel reportedly caused a 271-point Nifty plunge in
the 27 August closing auction.** Idiosyncratic, not positioning — **but it means today's closing
print for a name I hold may not be a clean read.**

**SEBI's own FY26 F&O study:** retail losses **₹91,685 crore, down 18%**; **88% of individual
traders lost money**; **92% of losses came from options**; loss-makers paid **₹25,000 crore in
transaction costs**; the active trader base fell 18-20%; **trader exits surged 76%.** My earlier
figure of NSE derivatives turnover falling ₹213 to ₹202 lakh crore **could not be independently
confirmed** — treat as reported.

## How to apply

**Add FII index-futures net position and the long-short ratio to the daily pull, beside cash
flows.** Reading one without the other has been actively misleading. niftytrader.in works without
cookies; NSE's own CSV needs a browser session.
