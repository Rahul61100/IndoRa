---
title: "The governance agent never launched, and that is exactly where the loss was"
market: general
type: finding
confidence: verified
tags: [general, finding, verified]
updated: 2026-08-27
---

# The governance agent never launched, and that is exactly where the loss was

Process failure, recorded 2026-08-27.

On 2026-08-26 I commissioned a fleet of research agents, one of which was a **forensic accounting
and governance check on every name in the open book** — promoter activity, auditor changes,
related-party transactions, **regulatory and legal actions**, accounting-quality flags, board and
management churn.

**It never ran.** It was one of five agents rejected with "Concurrent subagent limit reached."
I noted the cap, launched what fitted, and **never came back for the ones that failed.**

**The very next day, the largest single-day move in the book turned out to be a governance event**
— HDFC Bank's MSRDC differential-interest controversy, an RBI query into the adequacy of the
board's own penalty, and a US securities class action
([[hdfc-bank-msrdc-governance-overhang]]). Developing since May. Entirely public.

Meanwhile I had produced, on that same position, a detailed NIM analysis, a flow analysis, a
correlation matrix and a risk-contribution table. **All of it accurate. None of it the driver.**

## Why it happened

1. **A failed tool call was treated as noise rather than as a queued task.** Nothing tracked the
   five rejected agents. There was no list to come back to.
2. **The dropped work was the least quantitative.** When capacity is short, the instinct is to keep
   what produces numbers. Governance produces prose, so it was implicitly lowest priority — which
   is exactly backwards in India, where a court ruling or a regulatory action reprices a stock
   faster than any earnings cycle ([[india-policy-calendar-and-two-corrections]]).

## The rules

- **A failed or rejected agent launch is an open task. Write it down, and re-launch it before
  starting anything new.**
- **Run the governance and regulatory check on every held name BEFORE the quantitative work, not
  after.** It is a gate, not a supplement. A name with an active regulator query does not need a
  correlation matrix; it needs a decision.
- **In India specifically, legal and regulatory risk is not tail risk — it is regular risk.** Four
  instances inside eighteen months: a Supreme Court gaming ban with retrospective GST, an STT hike,
  a reintroduced windfall levy, and F&O curbs. All publicly trackable, none visible in any price
  series or financial statement.
- **When capacity is short, cut the work that produces numbers before the work that produces
  judgement.** The numbers were never the binding constraint.
