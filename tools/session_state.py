# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Generate SESSION-STATE.md — the file a fresh session reads first.

    uv run tools/session_state.py

The problem this solves: a context window ends and everything not written down is gone.
This assembles the resume brief mechanically from what is on disk -- open theses, the
scorecard, recent commits, data freshness, and the carried-forward questions -- so no
part of it depends on the previous session remembering to summarise itself.

Run it at the end of every session, and after any material change to the book.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sh(*args: str) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                              timeout=30).stdout.strip()
    except Exception:
        return ""


def data_freshness() -> list[str]:
    out = []
    for market in ("india", "us", "crypto"):
        p = ROOT / "data" / "daily" / market / "latest.json"
        if not p.exists():
            out.append(f"| {market} | **MISSING** | — | — |")
            continue
        d = json.loads(p.read_text())
        n = sum(len(g) for g in d["groups"].values())
        flags = len(d.get("quality_flags", []))
        out.append(f"| {market} | {d['generated_at'][:10]} | {n} tickers | "
                   f"{flags} quality flag{'s' if flags != 1 else ''} |")
    for name, label in (("india_fii_dii.json", "India FII/DII"),
                        ("stablecoin_supply.json", "Stablecoin supply"),
                        ("defi_tvl.json", "DeFi TVL")):
        p = ROOT / "data" / "flows" / name
        if p.exists():
            rows = json.loads(p.read_text())
            out.append(f"| {label} | {rows[-1]['date']} | {len(rows)} rows | flows ledger |")
        else:
            out.append(f"| {label} | **MISSING** | — | — |")
    return out


def scorecard_tail(n: int = 12) -> list[str]:
    p = ROOT / "positions" / "open-theses.md"
    if not p.exists():
        return []
    rows = [l for l in p.read_text().splitlines()
            if l.startswith("| 20") and l.count("|") >= 4]
    return rows[-n:]


def open_questions() -> list[str]:
    js = sorted((ROOT / "journal").glob("2*.md"))
    js = [j for j in js if "-data" not in j.name]
    if not js:
        return []
    text = js[-1].read_text()
    m = re.search(r"## Open questions.*?\n(.*?)(?=\n## |\Z)", text, re.S)
    if not m:
        return []
    return [l for l in m.group(1).splitlines() if l.strip()]


def main() -> None:
    now = datetime.now(timezone.utc)
    kn = len(list((ROOT / "knowledge").glob("*.md")))
    commits = sh("git", "log", "--oneline", "-12")
    dirty = sh("git", "status", "--porcelain")

    L = [
        "# SESSION STATE — read this first",
        "",
        f"_Generated {now:%Y-%m-%d %H:%M} UTC by `tools/session_state.py`. "
        "Regenerate at the end of every session._",
        "",
        "## Start here, in this order",
        "",
        "1. `CLAUDE.md` — how this workspace works",
        "2. **This file** — where things stand right now",
        "3. `positions/open-theses.md` — the live book, invalidation conditions, and the",
        "   running scorecard. **Score the open book before forming any new view.**",
        "4. `playbooks/daily-research-loop.md` — the cycle to run",
        "5. `playbooks/political-economy-layer.md` — who is positioned, who holds the levers,",
        "   who benefits, what is on the calendar. Runs daily, second, right after flows.",
        "6. `knowledge/INDEX.md` or the `MOC-*` hub notes — the durable facts",
        "",
        "## Refresh the data before reasoning about any price",
        "",
        "```bash",
        "cd ~/market-intel",
        "for m in india us crypto; do",
        "  uv run scripts/fetch_daily.py --universe $m --period 3y",
        "  uv run scripts/report_daily.py --market $m --write",
        "done",
        "uv run scripts/fetch_flows.py      # MUST run daily -- NSE serves only the latest session",
        "uv run scripts/regime.py           # regime label per market",
        "uv run scripts/portfolio_risk.py   # correlation, effective bets, USD-adjusted returns",
        "uv run tools/kb.py all             # frontmatter, MOCs, link check",
        "```",
        "",
        "## Data freshness",
        "",
        "| Series | Last updated | Size | Notes |",
        "|---|---|---|---|",
        *data_freshness(),
        "",
        f"## Knowledge base: {kn} notes",
        "",
        "Load-bearing corrections — **these overturn things earlier sessions asserted**:",
        "",
        "- `CORRECTION-india-erp-is-negative` — the 6.85% G-sec beats the 4.89% earnings yield.",
        "  \"Cheap versus its own history\" is not cheap.",
        "- `CORRECTION-india-earnings-growth-was-4-5-percent` — the \"+18%\" was one quarter and",
        "  60% of it was five stocks. FY26 grew 4.5% against 12-15% expected.",
        "- `CORRECTION-india-did-not-halt-russian-crude` — India was outbid by China, not acting",
        "  on policy. Not reversible by diplomacy.",
        "- `CORRECTION-ieepa-tariffs-were-struck-down` — the Supreme Court voided the authority",
        "  6-3 in February 2026.",
        "- `announced-is-not-disbursed` — approved, awarded and paid are three different things.",
        "",
        "## Standing rules that are easy to forget",
        "",
        "- **Never state a price, multiple or return without pulling it that session.**",
        "- **Quote Indian returns in BOTH currencies.** INR-only overstates the case badly.",
        "- **Check revision direction before calling anything a de-rating.** Trailing beats and",
        "  forward cuts routinely coexist.",
        "- **Decompose every headline growth number** before using it.",
        "- **Ask: approved, awarded, or paid?**",
        "- **Read the oil curve and crack spreads, not the flat price.**",
        "- Confidence tags: `verified` / `reported` / `degraded` / `not found`. **\"Not found\"**",
        "  **never means \"does not exist.\"**",
        "- WebSearch is capped at **200 calls per session, shared with all subagents**. Budget it;",
        "  roughly 5-8 deep agents, not 14. Put premises in the *question*, not the framing —",
        "  an agent that inherits a wrong assumption researches around it.",
        "- **Do not publish artifacts without asking** — pass this down to subagents too.",
        "",
        "## Scorecard — most recent entries",
        "",
        "| Date | Thesis | Status | Note |",
        "|---|---|---|---|",
        *scorecard_tail(),
        "",
        "## Questions carried forward",
        "",
        *(open_questions() or ["- (none recorded in the latest journal)"]),
        "",
        "## Repo",
        "",
        f"Remote: `{sh('git', 'remote', 'get-url', 'origin')}`",
        "",
        "```",
        commits,
        "```",
        "",
        f"Working tree: {'**UNCOMMITTED CHANGES PRESENT**' if dirty else 'clean'}",
        "",
        "## The one thing to hold on to",
        "",
        "This workspace has **no evidence of skill yet.** Not a single thesis has been scored",
        "forward to its horizon. Phase 3 of `playbooks/roadmap.md` is the gate, and it needs",
        "~30 scored theses. Any backward-looking number that flatters the book is measuring",
        "hindsight — see `backtests-of-chosen-names-measure-hindsight`.",
    ]
    (ROOT / "SESSION-STATE.md").write_text("\n".join(L) + "\n")
    print(f"wrote {ROOT / 'SESSION-STATE.md'}  ({kn} knowledge notes)")


if __name__ == "__main__":
    main()
