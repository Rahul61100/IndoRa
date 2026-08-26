# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance", "pandas", "numpy"]
# ///
"""
Position sizing on risk contribution, plus a liquidity check.

The problem this solves: sizing in rupees is not sizing in risk. Dixon at 39% annualised
volatility contributes several times the risk of HDFC Bank at 17.5% for the same rupee
amount, so an "equal weight" book is in fact a concentrated bet on the most volatile name.

Outputs:
  - marginal and percentage risk contribution of each holding at equal weight
  - inverse-volatility and equal-risk-contribution weights for comparison
  - liquidity: 20-day average traded value, and how many days it takes to exit a
    given position size at 20% of daily volume

    uv run scripts/sizing.py [--capital 10000000]   # capital in INR, default 1 crore
"""
from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
import yfinance as yf

BOOK = {
    "ICICIBANK.NS": "SHORT", "BHARTIARTL.NS": "SHORT", "HAL.NS": "SHORT",
    "SBIN.NS": "MEDIUM", "DIXON.NS": "MEDIUM", "HDFCBANK.NS": "MEDIUM",
    "NTPC.NS": "LONG", "RELIANCE.NS": "LONG",
}
PARTICIPATION = 0.20  # assume you can be at most 20% of a day's traded value


def erc_weights(cov: np.ndarray, iters: int = 20000, tol: float = 1e-10) -> np.ndarray:
    """Equal risk contribution via cyclical coordinate descent on the standard
    fixed-point iteration. Converges reliably for a positive-definite covariance."""
    n = cov.shape[0]
    w = np.ones(n) / n
    for _ in range(iters):
        rc = w * (cov @ w)
        target = rc.mean()
        grad = cov @ w
        w_new = w * (target / np.maximum(rc, 1e-18)) ** 0.5
        w_new = np.maximum(w_new, 1e-8)
        w_new /= w_new.sum()
        if np.max(np.abs(w_new - w)) < tol:
            w = w_new
            break
        w = w_new
    return w


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--capital", type=float, default=1e7, help="INR capital, default 1 crore")
    args = ap.parse_args()

    tick = list(BOOK)
    raw = yf.download(tick, period="2y", interval="1d", group_by="ticker",
                      auto_adjust=True, progress=False, threads=True)
    close, vol = {}, {}
    for t in tick:
        try:
            c = raw[t]["Close"].dropna()
            v = raw[t]["Volume"].dropna()
            if len(c) > 250:
                close[t], vol[t] = c, v
        except Exception:
            pass
    px = pd.DataFrame(close)
    held = list(px.columns)
    rets = px.pct_change().dropna()
    cov = rets.cov().values * 252
    sd = np.sqrt(np.diag(cov))

    n = len(held)
    w_eq = np.ones(n) / n
    port_vol = float(np.sqrt(w_eq @ cov @ w_eq))
    rc = w_eq * (cov @ w_eq) / port_vol          # marginal risk contribution
    pct_rc = rc / rc.sum() * 100

    w_iv = (1 / sd) / (1 / sd).sum()
    w_erc = erc_weights(cov)

    print("=" * 92)
    print(f"RISK CONTRIBUTION AT EQUAL WEIGHT   (book vol {port_vol*100:.1f}% annualised)")
    print("=" * 92)
    print(f"{'ticker':<15}{'bucket':<8}{'vol%':>8}{'eq wt%':>9}{'risk contrib%':>15}"
          f"{'inv-vol wt%':>13}{'ERC wt%':>10}")
    order = np.argsort(-pct_rc)
    for i in order:
        t = held[i]
        print(f"{t:<15}{BOOK[t]:<8}{sd[i]*100:>8.1f}{w_eq[i]*100:>9.1f}{pct_rc[i]:>15.1f}"
              f"{w_iv[i]*100:>13.1f}{w_erc[i]*100:>10.1f}")

    worst, best = held[order[0]], held[order[-1]]
    print(f"\n  At equal rupee weight, {worst.replace('.NS','')} carries {pct_rc[order[0]]:.1f}% of book risk")
    print(f"  and {best.replace('.NS','')} carries {pct_rc[order[-1]]:.1f}% — a "
          f"{pct_rc[order[0]]/pct_rc[order[-1]]:.1f}x spread for the same money.")
    print(f"  Equal-risk book vol would be {float(np.sqrt(w_erc @ cov @ w_erc))*100:.1f}% "
          f"vs {port_vol*100:.1f}% equal-weight.")

    print("\n" + "=" * 92)
    print(f"LIQUIDITY   (capital ₹{args.capital/1e7:.1f} crore, equal weight, "
          f"exit at {PARTICIPATION:.0%} of daily volume)")
    print("=" * 92)
    print(f"{'ticker':<15}{'price':>10}{'20d avg traded ₹cr':>21}{'position ₹cr':>15}{'days to exit':>15}")
    per = args.capital / n
    for t in held:
        p = float(px[t].iloc[-1])
        adv_val = float((px[t].tail(20) * vol[t].tail(20)).mean())
        days = per / (adv_val * PARTICIPATION) if adv_val > 0 else float("inf")
        flag = "   <-- illiquid for this size" if days > 1 else ""
        print(f"{t:<15}{p:>10,.1f}{adv_val/1e7:>21,.1f}{per/1e7:>15.2f}{days:>15.2f}{flag}")
    print("\n  Days-to-exit above ~1 means the position cannot be closed in a single session")
    print("  without moving the price. That is a real constraint on any thesis with a stop.")


if __name__ == "__main__":
    main()
