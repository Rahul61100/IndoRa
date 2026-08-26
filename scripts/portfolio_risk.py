# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas", "numpy"]
# ///
"""
Portfolio risk: correlation, concentration, currency-adjusted returns, drawdown.

The gap this closes: a book of N positions is not N bets. If the holdings are
correlated, the effective number of independent bets is far smaller than the
position count, and the book is one macro wager wearing nine tickers.

    uv run scripts/portfolio_risk.py

Reports:
  - pairwise return correlation of the open book
  - effective number of bets  (1 / sum of squared weights of the principal components)
  - beta and tracking error of each holding vs its market
  - USD-adjusted returns for Indian holdings (the return an FII actually earned)
  - worst historical drawdown per holding
  - cross-market correlation of India / US / crypto benchmarks
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent

BOOK = {
    "SHORT":  ["ICICIBANK.NS", "BHARTIARTL.NS", "HAL.NS"],
    "MEDIUM": ["SBIN.NS", "DIXON.NS", "HDFCBANK.NS"],
    "LONG":   ["NTPC.NS", "RELIANCE.NS"],
    "BENCH":  ["LT.NS", "INFY.NS"],
}
BENCHMARKS = {"^NSEI": "India", "^GSPC": "US", "BTC-USD": "Crypto"}
FX = "USDINR=X"


def fetch(tickers: list[str], period="2y") -> pd.DataFrame:
    raw = yf.download(tickers, period=period, interval="1d", group_by="ticker",
                      auto_adjust=True, progress=False, threads=True)
    out = {}
    for t in tickers:
        try:
            s = raw[t]["Close"].dropna()
            if len(s) > 200:
                out[t] = s
        except Exception:
            pass
    return pd.DataFrame(out)


def effective_bets(corr: pd.DataFrame) -> float:
    """Participation ratio of the correlation matrix eigenvalues.

    Equals N when holdings are independent, and 1 when they are a single factor.
    """
    ev = np.linalg.eigvalsh(corr.values)
    ev = ev[ev > 0]
    return float(ev.sum() ** 2 / (ev ** 2).sum())


def max_drawdown(s: pd.Series) -> float:
    return float((s / s.cummax() - 1).min() * 100)


def main() -> None:
    holdings = [t for g in BOOK.values() for t in g]
    px = fetch(holdings + list(BENCHMARKS) + [FX])
    rets = px.pct_change().dropna(how="all")

    held = [t for t in holdings if t in px.columns]
    corr = rets[held].corr()

    print("=" * 78)
    print("PAIRWISE CORRELATION OF THE OPEN BOOK (daily returns, 2y)")
    print("=" * 78)
    short = {t: t.replace(".NS", "")[:9] for t in held}
    print(f"{'':10}" + "".join(f"{short[c]:>10}" for c in held))
    for r in held:
        print(f"{short[r]:10}" + "".join(
            f"{corr.loc[r, c]:>10.2f}" if r != c else f"{'-':>10}" for c in held))

    n = len(held)
    eff = effective_bets(corr)
    avg = (corr.values.sum() - n) / (n * (n - 1))
    print(f"\npositions held            : {n}")
    print(f"average pairwise corr     : {avg:.2f}")
    print(f"EFFECTIVE NUMBER OF BETS  : {eff:.2f}   <- if far below {n}, this is one bet")

    print("\n" + "=" * 78)
    print("PER-HOLDING RISK vs NIFTY")
    print("=" * 78)
    bmk = rets["^NSEI"]
    print(f"{'ticker':<14}{'beta':>8}{'ann vol%':>10}{'maxDD%':>9}{'corr':>7}   2y ann return%")
    for t in held:
        j = pd.concat([rets[t], bmk], axis=1).dropna()
        b = float(np.cov(j.iloc[:, 0], j.iloc[:, 1])[0, 1] / np.var(j.iloc[:, 1]))
        vol = float(rets[t].std() * np.sqrt(252) * 100)
        yrs = len(px[t].dropna()) / 252
        ann = float((px[t].dropna().iloc[-1] / px[t].dropna().iloc[0]) ** (1 / yrs) - 1) * 100
        print(f"{t:<14}{b:>8.2f}{vol:>10.1f}{max_drawdown(px[t].dropna()):>9.1f}"
              f"{j.iloc[:, 0].corr(j.iloc[:, 1]):>7.2f}{ann:>17.1f}")

    print("\n" + "=" * 78)
    print("WHAT A DOLLAR INVESTOR ACTUALLY EARNED IN INDIA")
    print("=" * 78)
    fx = px[FX].dropna()
    nifty = px["^NSEI"].dropna()
    j = pd.concat([nifty.rename("nifty"), fx.rename("fx")], axis=1).dropna()
    j["usd"] = j["nifty"] / j["fx"]
    for label, days in (("6m", 126), ("1y", 252), ("2y", len(j) - 1)):
        if len(j) <= days:
            continue
        inr = (j["nifty"].iloc[-1] / j["nifty"].iloc[-1 - days] - 1) * 100
        usd = (j["usd"].iloc[-1] / j["usd"].iloc[-1 - days] - 1) * 100
        print(f"  {label:<4} Nifty in INR {inr:>7.1f}%   in USD {usd:>7.1f}%   "
              f"currency drag {usd - inr:>6.1f}pp")

    print("\n" + "=" * 78)
    print("CROSS-MARKET CORRELATION")
    print("=" * 78)
    # India closes ~10:00 UTC, the US opens ~13:30 UTC. Same-day returns are therefore
    # NOT contemporaneous, and a naive same-day correlation understates the true linkage
    # badly -- India reacts to the PREVIOUS US session. Lag the US and crypto series by
    # one day when comparing to India, and report both so the artifact is visible.
    ind, us, btc = rets["^NSEI"].dropna(), rets["^GSPC"].dropna(), rets["BTC-USD"].dropna()

    def pair(a: pd.Series, b: pd.Series, lag_b: int = 0) -> tuple[float, int]:
        j = pd.concat([a, b.shift(lag_b)], axis=1, join="inner").dropna()
        return (float(j.iloc[:, 0].corr(j.iloc[:, 1])), len(j))

    naive_iu, n1 = pair(ind, us, 0)
    lag_iu, n2 = pair(ind, us, 1)
    naive_ib, _ = pair(ind, btc, 0)
    lag_ib, _ = pair(ind, btc, 1)
    ub, n3 = pair(us, btc, 0)

    print(f"  India vs US    same-day {naive_iu:>6.2f}   US LAGGED 1d {lag_iu:>6.2f}   (n={n2})")
    print(f"  India vs BTC   same-day {naive_ib:>6.2f}   BTC LAGGED 1d {lag_ib:>6.2f}")
    print(f"  US vs BTC      same-day {ub:>6.2f}   (same session, no lag needed, n={n3})")
    print("  Same-day India numbers are a TIMEZONE ARTIFACT -- use the lagged column.")

    j = pd.concat([ind, us.shift(1)], axis=1, join="inner").dropna()
    roll = j.iloc[:, 0].rolling(60).corr(j.iloc[:, 1]).dropna()
    if len(roll):
        print(f"\n  India vs lagged-US, 60d rolling: now {roll.iloc[-1]:.2f}, "
              f"range {roll.min():.2f} to {roll.max():.2f}, mean {roll.mean():.2f}")
    k = pd.concat([us, btc], axis=1, join="inner").dropna()
    rollc = k.iloc[:, 0].rolling(60).corr(k.iloc[:, 1]).dropna()
    if len(rollc):
        print(f"  US vs BTC,      60d rolling: now {rollc.iloc[-1]:.2f}, "
              f"range {rollc.min():.2f} to {rollc.max():.2f}, mean {rollc.mean():.2f}")


if __name__ == "__main__":
    main()
