# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Audit the knowledge base for unsourced claims — the anti-hallucination check.

    uv run tools/audit.py            # summary
    uv run tools/audit.py --detail   # per-note breakdown

Every note in this workspace is one of four things, and the difference matters:

  verified   pulled from a primary source or computed from our own data this session
  reported   secondary source, dated and attributed
  degraded   gathered after the session search cap, via aggregators; re-verify
  unsourced  A CLAIM WITH NO SOURCE AND NO DATE. This is where hallucination hides.

The last category is the point. A note asserting numbers with no URL, no date and no
"computed from" line cannot be checked by anyone later, including me. This flags them.
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KD = ROOT / "knowledge"

URL = re.compile(r"https?://")
DATE = re.compile(r"\b(20\d\d-\d\d-\d\d|\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)|"
                  r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+20\d\d)", re.I)
OWN_DATA = re.compile(r"computed from|from our own|our own (series|data|pull|snapshot)|"
                      r"derived from our own|scripts?/[a-z_]+\.py|data/(daily|flows|revisions)", re.I)
NUMBER = re.compile(r"[₹$]\s?[\d,]+(?:\.\d+)?|\b\d+(?:\.\d+)?%|\b\d{1,3}(?:,\d{2,3})+\b")


def classify(text: str) -> tuple[str, dict]:
    conf = re.search(r"^confidence:\s*(\S+)", text, re.M)
    tag = conf.group(1) if conf else "unknown"
    body = re.sub(r"^---.*?^---", "", text, flags=re.S | re.M)
    m = {
        "urls": len(URL.findall(body)),
        "dates": len(DATE.findall(body)),
        "numbers": len(NUMBER.findall(body)),
        "own_data": bool(OWN_DATA.search(body)),
    }
    # A note making numeric claims with no URL, no date and no reference to our own
    # computation is unverifiable by anyone later. That is the category that matters.
    if m["numbers"] >= 3 and m["urls"] == 0 and m["dates"] == 0 and not m["own_data"]:
        return "UNSOURCED", m
    return tag, m


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--detail", action="store_true")
    args = ap.parse_args()

    rows = []
    for p in sorted(KD.glob("*.md")):
        if p.stem.startswith("MOC-") or p.stem == "INDEX":
            continue
        verdict, m = classify(p.read_text())
        rows.append((p.stem, verdict, m))

    counts = Counter(v for _, v, _ in rows)
    total = len(rows)
    print("=" * 74)
    print(f"KNOWLEDGE BASE AUDIT — {total} notes")
    print("=" * 74)
    for k in ("verified", "reported", "degraded", "unknown", "UNSOURCED"):
        if counts.get(k):
            bar = "█" * round(counts[k] / total * 40)
            print(f"  {k:<11}{counts[k]:>4}  {counts[k]/total*100:>5.1f}%  {bar}")

    unsourced = [r for r in rows if r[1] == "UNSOURCED"]
    print(f"\n  numeric claims with no URL, no date, no own-data reference: {len(unsourced)}")
    for stem, _, m in unsourced:
        print(f"    ! {stem}  ({m['numbers']} numeric claims)")

    thin = [(s, m) for s, v, m in rows if v != "UNSOURCED" and m["numbers"] >= 8 and m["urls"] == 0]
    if thin:
        print(f"\n  heavy on numbers, no URL (dated or own-data, so traceable but not linkable): {len(thin)}")
        for s, m in sorted(thin, key=lambda x: -x[1]["numbers"])[:12]:
            print(f"    - {s}  ({m['numbers']} numbers, {m['dates']} dates)")

    print(f"\n  totals: {sum(m['urls'] for _, _, m in rows)} source URLs, "
          f"{sum(m['dates'] for _, _, m in rows)} dates, "
          f"{sum(m['numbers'] for _, _, m in rows)} numeric claims across the base")
    own = sum(1 for _, _, m in rows if m["own_data"])
    print(f"  {own} notes ({own/total*100:.0f}%) cite our own collected data rather than reporting")

    if args.detail:
        print("\n" + "=" * 74)
        print(f"{'note':<52}{'conf':<11}{'url':>4}{'date':>5}{'num':>5}")
        for stem, v, m in sorted(rows, key=lambda r: (r[1], -r[2]["numbers"])):
            print(f"{stem[:50]:<52}{v:<11}{m['urls']:>4}{m['dates']:>5}{m['numbers']:>5}")


if __name__ == "__main__":
    main()
