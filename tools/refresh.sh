#!/usr/bin/env bash
# Refresh everything: data, flows, derived views, vault, session state.
# Safe to run repeatedly. Run at the start and end of every session.
set -uo pipefail
cd "$(dirname "$0")/.."

echo "=== flows (MUST run daily -- NSE serves only the latest session) ==="
uv run --quiet scripts/fetch_flows.py

for m in india us crypto; do
  echo "=== $m ==="
  uv run --quiet scripts/fetch_daily.py --universe "$m" --period 3y
  uv run --quiet scripts/report_daily.py --market "$m" --write
done

echo "=== estimate revisions (Yahoo serves only a snapshot -- history exists only if this runs) ==="
uv run --quiet scripts/fetch_revisions.py --universe india --top 10 | tail -30

echo "=== regime ==="
uv run --quiet scripts/regime.py | sed -n '/REGIME/,/BOOK STRESS/p'

echo "=== vault (frontmatter, hubs, link check) ==="
uv run --quiet tools/kb.py all

echo "=== session state ==="
uv run --quiet tools/session_state.py

echo
echo "Done. Obsidian picks up changes automatically -- no reload needed."
