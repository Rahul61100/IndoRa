# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance","pandas","numpy"]
# ///
"""
What an INDIAN RESIDENT actually earns — the hurdle that applies to this book.

    uv run scripts/real_return.py

Written as a correction. Having found that India returned −10.9% in USD against Korea's
+109.3%, the tempting conclusion is "India must clear a currency hurdle." For a dollar-based
allocator that is right. **For an Indian resident it is wrong**, and importing it would be a
category error: someone who earns, spends and retires in rupees is not harmed by the rupee
falling against the dollar. They are harmed by rupee *purchasing power* falling, which is
domestic inflation — and the currency only reaches them through the imported component of it.

So the honest hurdle for this book has three layers, and only the first two are usually stated:

  1. nominal Nifty return
  2. minus CPI                     -> real return
  3. minus tax                     -> real after-tax return, the only number that spends

Plus the part the USD table genuinely does carry over: **the opportunity cost of not being
allowed to compound abroad cheaply.** An Indian resident CAN buy foreign equity under LRS, but
pays 20% TCS on remittance above the threshold and gets no ₹1.25L LTCG exemption on it. That
friction is real and it is what makes the Korea comparison relevant to an Indian resident at all.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import yfinance as yf

# India CPI is not on yfinance. These are the stated assumptions and they are NOT sourced here.
CPI_ASSUMED = 0.05      # ~5% headline, the RBI's target midpoint plus a margin
CPI_RANGE = (0.04, 0.07)


def main() -> None:
    px = yf.download(["^NSEI", "^GSPC", "INR=X"], period="10y", interval="1d",
                     progress=False, auto_adjust=True)["Close"].ffill()
    n = px["^NSEI"].dropna()
    yrs = len(n) / 252
    cagr = (float(n.iloc[-1]) / float(n.iloc[0])) ** (1 / yrs) - 1

    print("WHAT AN INDIAN RESIDENT ACTUALLY EARNS")
    print("=" * 84)
    print(f"  Nifty nominal CAGR, last {yrs:.1f} years        {cagr*100:>7.2f}%")
    for lbl, cpi in [("at 4% CPI", 0.04), ("at 5% CPI", 0.05), ("at 7% CPI", 0.07)]:
        real = (1 + cagr) / (1 + cpi) - 1
        print(f"    real, {lbl:<12}                  {real*100:>7.2f}%")
    print(f"\n  (CPI is an ASSUMPTION, not sourced here. The spread between 4% and 7% is"
          f"\n   {((1+cagr)/1.04 - (1+cagr)/1.07)*100:.2f}pp of real return -- larger than most of the"
          f"\n   stock-picking edge this workspace is trying to establish.)")

    real5 = (1 + cagr) / (1 + CPI_ASSUMED) - 1
    print("\n" + "=" * 84)
    print("  THEN TAX, on the real return, at 5% CPI:")
    for lbl, rate, exempt in [("LTCG 12.5% (held >12m)", 0.125, True),
                              ("STCG 20%  (held <12m)", 0.20, False)]:
        after = cagr * (1 - rate)
        realafter = (1 + after) / (1 + CPI_ASSUMED) - 1
        print(f"    {lbl:<26} nominal {after*100:>6.2f}%   real {realafter*100:>6.2f}%"
              f"{'   (before the Rs1.25L exemption)' if exempt else ''}")

    print("\n" + "=" * 84)
    print("  THE PART THE USD TABLE DOES CARRY OVER — cost of compounding abroad instead")
    print("  LRS route: 20% TCS on remittance above the threshold (recoverable against tax,")
    print("  but a cash-flow cost for the year), and NO Rs1.25L LTCG exemption on foreign equity.")
    fx = px["INR=X"].dropna()
    fx_cagr = (float(fx.iloc[-1]) / float(fx.iloc[0])) ** (1 / (len(fx) / 252)) - 1
    sp = px["^GSPC"].dropna()
    sp_cagr = (float(sp.iloc[-1]) / float(sp.iloc[0])) ** (1 / (len(sp) / 252)) - 1
    print(f"\n    USDINR CAGR over the window        {fx_cagr*100:>6.2f}%  (rupee depreciation)")
    print(f"    S&P 500 CAGR in USD                {sp_cagr*100:>6.2f}%")
    print(f"    S&P 500 CAGR translated to INR     {((1+sp_cagr)*(1+fx_cagr)-1)*100:>6.2f}%")
    print(f"    Nifty CAGR in INR                  {cagr*100:>6.2f}%")
    gap = ((1 + sp_cagr) * (1 + fx_cagr) - 1) - cagr
    print(f"\n    Gap, in the currency the investor spends: {gap*100:+.2f}pp per year to the S&P.")
    print(f"    That is the number an Indian resident should weigh against LRS friction --")
    print(f"    NOT the headline USD table, which overstates the case by counting the rupee")
    print(f"    depreciation as a loss when for a rupee-spender it is the thing that made the")
    print(f"    foreign asset worth more.")


if __name__ == "__main__":
    main()
