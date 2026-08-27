---
title: "Home"
type: moc
tags: [moc, home]
---

# market-intel

Daily multi-market research loop. **India · United States · Crypto.**
Live market sessions run **09:00-14:00 IST** while the Indian market is open.

## Start here

- [[SESSION-STATE]] — where things stand right now. **Read this first after any context reset.**
- [[open-theses]] — the live book, invalidation conditions, running scorecard
- [[CLAUDE]] — how this workspace works

## The hubs

| Hub | What's in it |
|---|---|
| [[MOC-Corrections]] | **Every claim this workspace got wrong.** Start here — it's the most useful note in the vault |
| [[MOC-India]] | India — valuation, flows, policy, sectors |
| [[MOC-United-States]] | US — earnings, positioning, fiscal, the AI capex cycle |
| [[MOC-Crypto]] | Crypto — flows, on-chain, regulation, the DAT overhang |
| [[MOC-Cross-Market]] | Where one market previews another. **The reason we run three.** |
| [[MOC-Method]] | The rules that stop us fooling ourselves |
| [[MOC-Portfolio]] | Sizing, correlation, risk contribution |

## Playbooks

- [[daily-research-loop]] — the cycle, in order: flows → political economy → macro → breadth → rotation → extremes
- [[market-hours]] — the 09:00-14:00 IST live session
- [[political-economy-layer]] — who is positioned, who holds the levers, who benefits, what's on the calendar
- [[data-quality-rules]] — every rule here exists because the data lied once and got caught
- [[research-budget-constraints]] — the 200-call search cap and what it does to confidence
- [[roadmap]] — the end goal and the phase gates

## Graph legend

Colours are driven by frontmatter, stamped by `tools/kb.py`:

- **red** — corrections · **amber** — India · **blue** — US · **purple** — crypto
- **orange** — cross-market · **grey** — method · **bright orange** — `degraded` confidence

⚠ **Degraded** means the note was gathered after the session search cap, via news
aggregators rather than primary sources. Re-verify before acting on it.

## Maintenance

```bash
uv run tools/kb.py all             # frontmatter, hubs, link check
uv run tools/session_state.py      # regenerate SESSION-STATE
```

## The one thing to remember

**This workspace has no evidence of skill yet.** Not one thesis has been scored forward to its
horizon. Any backward-looking number that flatters the book is measuring hindsight —
see [[backtests-of-chosen-names-measure-hindsight]].
