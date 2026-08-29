# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""Nightly ingest.

    uv run scripts/predict_ingest.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from predict import ODDS_DIR
from predict.db import connect, init_schema
from predict.ingest import run
from predict.venues import polymarket


def main() -> None:
    conn = connect()
    init_schema(conn)
    markets = polymarket.fetch_open()
    print(f"polymarket: {len(markets)} parsed")
    print(run(conn, markets, ODDS_DIR))


if __name__ == "__main__":
    main()
