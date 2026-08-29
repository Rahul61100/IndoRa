---
name: prediction-market-risk-review
description: Review a prediction-market or trading-adjacent workflow for advice boundary, venue/regulatory exposure, data quality, secrets, and privacy before it touches auth, portfolio data, API keys, or anything execution-capable. Use before wiring a new venue or shipping a workflow that reads the book.
---

# Prediction market risk review

Adapted from ECC's `prediction-market-risk-review` skill (MIT).

Run this **before** a workflow touches venue authentication, portfolio data, an API key, or any
tool that could place an order.

## Gates

### Advice boundary

- Output must be informational. Strip buy/sell/hold and any position size.
- Every decision point stays with the human, explicitly.
- This workspace holds real theses and real positions — the line between "the model says the market
  disagrees with your thesis" and "the model told me to trade" is the whole gate. Keep it visible.

### Venue and regulatory boundary

- Record the venue's terms, geography restrictions, account limits and API rules.
- **Never bypass a venue restriction or a rate limit.** `fetch_open()` stops on the venue's HTTP 422
  paging signal — that stop condition is a contract with the venue, not an inconvenience to route
  around.
- Flag betting / derivatives / securities ambiguity for a human when the classification is unclear,
  especially for an Indian resident on an offshore venue. Do not resolve it yourself.

### Data quality

- Liquidity, spread, resolution rules, stale prints, source timestamps — all checked before the
  number is used anywhere downstream.
- **Label public venue data separately from anything private or gated.** Never merge them into one
  unlabelled table.
- A flagged row does not silently become an input.

### Security

- Never request or store private keys, seed phrases, or passwords. There is no reason a research
  workspace needs any of them.
- Venue API keys stay out of logs, docs, notes, and commits. This repo is an Obsidian vault — a key
  pasted into a note is a key in git.
- **Read-only scopes by default.** A trading scope requires a separate, explicit decision.
- Anything execution-capable needs, before it exists: a written plan, a dry run, spend limits, a
  circuit breaker, and human approval per action. Absent any one of those, the answer is no.

### Privacy

- Minimize what portfolio and position data enters a prompt at all.
- Redact private sources in anything shared or published.
- Keep only the fields the review actually needs.

## Output

1. scope reviewed · 2. pass / warn / fail per gate · 3. blocked actions · 4. required mitigations ·
5. the safe next step

If any execution-capable step was requested, return a plan and stop. Do not build it in the same
pass that reviewed it.
