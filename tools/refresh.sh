#!/usr/bin/env bash
# Refresh everything: data, flows, derived views, vault, session state.
# Safe to run repeatedly. Run at the start and end of every session.
set -uo pipefail
cd "$(dirname "$0")/.."

echo "=== FX (intraday-derived; Yahoo daily FX bars are known-bad) ==="
uv run --quiet scripts/fx.py

echo "=== flows: cash (MUST run daily -- NSE serves only the latest session) ==="
uv run --quiet scripts/fetch_flows.py

echo "=== flows: derivatives (never read cash flow without this) ==="
uv run --quiet scripts/fetch_derivatives.py --days 7 | tail -14

for m in india us crypto; do
  echo "=== $m ==="
  uv run --quiet scripts/fetch_daily.py --universe "$m" --period 3y
  uv run --quiet scripts/report_daily.py --market "$m" --write
done

echo "=== estimate revisions (Yahoo serves only a snapshot -- history exists only if this runs) ==="
uv run --quiet scripts/fetch_revisions.py --universe india --top 10 | tail -30

echo "=== cross-sectional spreads (group vs group -- invisible to a name-level screen) ==="
uv run --quiet scripts/spreads.py

echo "=== regime ==="
uv run --quiet scripts/regime.py | sed -n '/REGIME/,/BOOK STRESS/p'

echo "=== prediction-market ingest (the odds log cannot be re-fetched later) ==="
uv run --quiet scripts/predict_ingest.py

echo "=== odds moves (a sharp move on a topic we hold a view on is a RESEARCH GAP) ==="
uv run --quiet scripts/odds_moves.py

echo "=== catalyst calendar (a past date here is a bug, not an entry) ==="
uv run --quiet tools/catalysts.py --horizon 120

echo "=== BOOK SCORECARD -- every written invalidation, checked, every day ==="
uv run --quiet tools/score.py

echo "=== vault (frontmatter, hubs, link check) ==="
uv run --quiet tools/kb.py all

echo "=== session state ==="
uv run --quiet tools/session_state.py

echo
echo "Done. Obsidian picks up changes automatically -- no reload needed."
