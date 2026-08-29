---
title: "I capped ICICI on a governance fight that had already been resolved in its favour"
market: general
type: finding
confidence: high
tags: [general, finding, high]
updated: 2026-08-29
---

# I capped ICICI on a governance fight that had already been resolved in its favour

A red-team pass on my own book found a factual error in a live position, and it is the more
embarrassing kind — not a number that moved, but a conclusion that was never true.

## What I wrote, and what actually happened

**What the book said:** ICICI capped, in part because the "CEO reappointment [was] contested to RBI,
escalated 24 Aug."

**What happened:** **RBI approved Sandeep Bakhshi's reappointment through 2028 on 22–23 May 2026** —
reported concordantly by Reuters, Economic Times, Moneycontrol, BusinessLine and Business Today. The
stock **rallied 2%** on the news. Every article framing the reappointment as "contested" is dated
**28 April – 20 May 2026 — all of it before the regulator ruled.** Five separate targeted searches
for an August escalation returned nothing.

**The regulator sided with the bank three months before I capped the position for the fight being
unresolved.**

## The error underneath the error

There *is* a live item: a **24 August letter from Prashant Bhushan** concerning "employee governance
concerns" — but it is **multi-bank, not ICICI-specific**, and its **substance is unknown**. I appear
to have collapsed that into the earlier, separate, already-decided CEO-reappointment matter because
both involved the same complainant writing to the same regulator about the same bank.

And I compounded it by bundling in the GST notices. Those are real — five or six demands totalling
roughly **₹1,320–1,420cr** over six months — but that is about **one quarter's "other expenses"
against ₹45,000cr+ of annual net profit**, and Indian GST demands are routinely reduced by half or
more on appeal. It is margin noise.

**So a single "CAPPED" verdict fused a resolved governance question with an immaterial tax-friction
question.** This workspace already records "governance scandal read as a margin story" as a past
mistake. This is the same conflation running the other way — and I made it while holding a note
warning against it.

## What I am doing about it, and what I am not

**Not upgrading.** The obvious move — and the one the workflow's decide agent recommended — is to
lift the cap and add. I am not doing that, because the 24 August letter's substance is **genuinely
unresolved**, and the red team itself said it "cannot rule out a fresh Aug 24 event my tooling
missed." **An unresolved factual question is a reason to wait, not a reason to add.** Correcting a
wrong reason for caution does not by itself produce a reason for conviction.

**What I am doing:**

1. The cap reason in `positions/theses.json` is rewritten to say what is actually live.
2. The two questions are now **separate invalidation lines** — governance and tax friction — because
   they do not move together and do not resolve on the same trigger.
3. The open action is specific: **establish what the 24 August letter says.** Until then the
   position stays where it is.

## The generalisable lesson

**A cap is a claim, and it needs the same evidentiary standard as a buy.** I applied real rigour to
opening positions today — earnings quality, invalidation conditions, base rates — and applied
none of it to the reason for being cautious. Caution feels free. It is not: this cap sat on a
position that is **+1.3% since entry and ahead of the Nifty by 1.8pp**, on a premise that was
already false when written.

**Every reason to be cautious should carry a date and a source, exactly like every reason to buy.**
The scorecard now surfaces manual conditions daily, which is what put this in front of a red team
at all — but it surfaced the *wrong text* every day until something checked the text itself.

**Source:** red-team agent research against multiple named outlets with dates; the underlying
reappointment approval is **reported** across five outlets concordantly, not confirmed against an
RBI primary release. The 24 August letter is **unresolved** and that is the load-bearing gap.

Related: [[the-equity-proxy-for-a-commodity-keeps-failing]] · [[what-the-spreads-say-about-my-own-emphasis]] · [[dixon-profit-is-not-operating]] · [[the-monsoon-is-the-trade-i-missed]]
