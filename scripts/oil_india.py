# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas", "numpy"]
# ///
"""
India's oil exposure: the empirical linkage, then the arithmetic.

    uv run scripts/oil_india.py

Written after noticing that Brent peaked at $118.3 on 2026-03-31 and is +21.9% off its
July trough — an oil shock this workspace had been treating as a benign backdrop while
separately recording a trade-deficit blowout and a current-account reversal as if they
were unrelated facts. They are the same event.

Two parts, deliberately kept apart. The regressions are what the data says. The current-account
arithmetic is a stated-assumption calculation and is only as good as the import-volume
assumption, which is NOT sourced here and is flagged as such.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import yfinance as yf

SERIES = {"^NSEI": "Nifty 50", "INR=X": "USDINR", "ONGC.NS": "ONGC", "IOC.NS": "IOC",
          "BPCL.NS": "BPCL", "RELIANCE.NS": "Reliance", "ASIANPAINT.NS": "Asian Paints", "INDIGO.NS": "IndiGo"}


def main() -> None:
    tick = ["BZ=F", *SERIES]
    px = yf.download(tick, period="2y", interval="1d", progress=False, auto_adjust=True)["Close"]
    px = px.dropna(how="all").ffill()
    # Drop series with no data at all -- a single all-NaN column (Yahoo's NSE sector
    # indices are routinely empty) turns a how="any" dropna into an empty frame, which
    # silently produces a blank table rather than an error.
    empty = [c for c in px.columns if px[c].notna().sum() < 100]
    if empty:
        print(f"  (no usable series, excluded: {', '.join(empty)})\n")
        px = px.drop(columns=empty)
    ret = np.log(px / px.shift(1))   # pairwise dropna happens per regression below
    if "BZ=F" not in ret:
        print("no Brent series"); return
    b = ret["BZ=F"]

    print("BETA TO BRENT — 2 years of daily log returns")
    print("=" * 84)
    print(f"  {'series':<16}{'beta':>8}{'corr':>8}{'r2':>7}{'ann vol':>9}   reading")
    rows = []
    for s, name in SERIES.items():
        if s not in ret:
            continue
        j = pd.concat([b, ret[s]], axis=1).dropna()
        if len(j) < 100:
            continue
        x, y = j.iloc[:, 0], j.iloc[:, 1]
        beta = float(np.cov(x, y)[0, 1] / np.var(x))
        corr = float(np.corrcoef(x, y)[0, 1])
        vol = float(y.std() * np.sqrt(252) * 100)
        rows.append((name, beta, corr, vol))
    for name, beta, corr, vol in sorted(rows, key=lambda r: -r[1]):
        read = ("rises with oil" if beta > 0.05 else
                "falls with oil" if beta < -0.05 else "no meaningful link")
        print(f"  {name:<16}{beta:>8.3f}{corr:>8.3f}{corr**2:>7.3f}{vol:>8.1f}%   {read}")

    print("\n" + "=" * 84)
    print("WHAT BRENT HAS ACTUALLY DONE")
    bp = px["BZ=F"].dropna()
    pk, tr = bp.idxmax(), bp[bp.index >= bp.idxmax()].idxmin()
    print(f"  peak      ${float(bp.max()):6.1f}  {pk.date()}")
    print(f"  trough    ${float(bp[tr]):6.1f}  {tr.date()}   ({(float(bp[tr])/float(bp.max())-1)*100:+.1f}% from peak)")
    print(f"  now       ${float(bp.iloc[-1]):6.1f}  {bp.index[-1].date()}   "
          f"({(float(bp.iloc[-1])/float(bp[tr])-1)*100:+.1f}% off trough, "
          f"{(float(bp.iloc[-1])/float(bp.max())-1)*100:+.1f}% from peak)")

    print("\n" + "=" * 84)
    print("CURRENT-ACCOUNT ARITHMETIC — stated assumptions, NOT sourced data")
    print("  assumed net crude imports 4.5-5.5 mb/d; assumed GDP $4.2tn.")
    print("  These are from memory, not from a primary source. Treat the SHAPE as the finding,")
    print("  not the decimals. A 20% error in the volume assumption moves every row 20%.")
    print()
    spot, trough = float(bp.iloc[-1]), float(bp[tr])
    print(f"  {'scenario':<34}{'$/bbl':>8}{'Δ vs now':>10}{'$bn/yr':>18}{'% of GDP':>11}")
    for label, level in [("July trough", trough), ("today", spot), ("back to $100", 100.0),
                         ("back to the Q1 peak", float(bp.max()))]:
        d = level - spot
        lo, hi = d * 4.5e6 * 365 / 1e9, d * 5.5e6 * 365 / 1e9
        print(f"  {label:<34}{level:>8.1f}{d:>+10.1f}{f'{lo:+,.1f} to {hi:+,.1f}':>18}"
              f"{f'{lo/4200*100:+.2f} to {hi/4200*100:+.2f}':>11}")
    print("\n  Rule of thumb that falls out: every $10 on Brent costs India roughly")
    print("  $16-20bn a year on the import bill, or about 0.4-0.5% of GDP on the current account.")


if __name__ == "__main__":
    main()
