# Playbook — live market hours (09:00-14:00 IST)

From 2026-08-27 the working session runs **09:00 to 14:00 IST, while the Indian market is
open.** That is a different job from the end-of-day loop and it needs a different rhythm.

**Indian market clock:** pre-open auction 09:00-09:15 · continuous trading 09:15-15:30 ·
so a 09:00-14:00 session covers the open and roughly **75% of the session**, ending before
the close. Plan around not seeing the close live.

## Why intraday is worth watching at all

The daily bar destroys the two things that matter most for reading flow:

1. **Volume pace.** A stock down 1% on double its normal pace and one down 1% on half of it
   are different events. The close reports them identically.
2. **Where the day opened relative to the prior close.** A gap down that fills by 11am and a
   gap down that extends all day produce a similar close and mean opposite things.

`scripts/intraday.py` reports both. It also flags a 50 DMA cross the moment it happens rather
than the evening after.

## The rhythm

### 08:45 — before the open
```bash
cd ~/market-intel
uv run tools/session_state.py     # re-read where things stand
uv run scripts/fetch_flows.py     # yesterday's FII/DII lands overnight
```
Read, in order: overnight US close and Asia · **crude curve and crack spreads, not the flat
price** · USDJPY and any BOJ headline · the open book's overnight ADRs where they exist.
Write down **what would change your mind today**, before the market can influence it.

### 09:00-09:15 — pre-open
The auction sets the opening print. Watch for gaps above ~1% on any held name and know the
reason **before** the continuous session starts.

### 09:15-14:00 — the session
```bash
uv run scripts/intraday.py --log        # every 45-60 min is plenty
```
Log each snapshot. What you are looking for, in priority order:

- **A held position running heavy volume** — pace above ~1.6x. That is someone with size, and
  it usually precedes news or is the news.
- **A level breaking** — 50 DMA crosses, 52-week highs and lows, the prior day's range.
- **Divergence between the index and the book.** If the Nifty is flat and the book is down
  five of eight, the book has an idiosyncratic problem.
- **Sector leadership rotating intraday** — what leads the first hour often does not lead
  the last.

**Do not trade the noise.** Every open thesis in `positions/open-theses.md` has a written
invalidation condition. An intraday move that does not touch one of them is information, not
a signal.

### 14:00 — hand off
```bash
uv run tools/session_state.py
```
Write the day's narrative note. **Say what changed, not what the table already shows.**
Flag anything you will miss between 14:00 and the 15:30 close so tomorrow's pre-open picks it up.

## What to add to the watch as the loop matures

- Advance/decline for the full universe, computed live rather than at the close
- Intraday FII/DII provisional numbers (published after the close, so they land next morning)
- Options open-interest shifts at key strikes — the derivative market often moves first
- Bulk and block deals: `archives.nseindia.com/content/equities/bulk.csv` and `block.csv`,
  both confirmed free and machine-readable, refreshed through the day

## The trap of watching live

**Screen time creates the illusion of information.** Most intraday movement is noise, and
watching it for five hours makes it feel like signal. Two defences:

1. **Write down what would change your mind before the open**, and check the day against
   that list rather than against your mood.
2. **Log the snapshots.** A written record makes it obvious afterwards how much of the day
   actually mattered — the answer is usually one or two moments, and everything else was
   texture.
