# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance","pandas","numpy"]
# ///
import yfinance as yf, pandas as pd, numpy as np
px=yf.download(["^NSEI","^GSPC","INR=X"],period="max",interval="1mo",progress=False,auto_adjust=True)["Close"].ffill().dropna()
print(f"monthly data {px.index[0].date()} -> {px.index[-1].date()}, {len(px)} months")
nif=px["^NSEI"]; spx=px["^GSPC"]; fx=px["INR=X"]
spx_inr = spx*fx                      # S&P translated into rupees
for W,label in [(36,"3-year"),(60,"5-year"),(120,"10-year")]:
    if len(px)<W+12: continue
    a=(nif/nif.shift(W))**(12/W)-1
    b=(spx_inr/spx_inr.shift(W))**(12/W)-1
    j=pd.concat([a,b],axis=1).dropna(); j.columns=["nifty","spx_inr"]
    j["gap"]=(j.spx_inr-j.nifty)*100
    win=(j.gap>0).mean()*100
    print(f"\n{label} rolling windows (n={len(j)}), CAGR in RUPEES")
    print(f"  S&P-in-INR beat Nifty in {win:.0f}% of windows")
    print(f"  gap: mean {j.gap.mean():+.2f}pp  median {j.gap.median():+.2f}pp  "
          f"min {j.gap.min():+.2f}pp  max {j.gap.max():+.2f}pp")
    print(f"  Nifty CAGR: mean {j.nifty.mean()*100:+.2f}%   S&P-in-INR CAGR: mean {j.spx_inr.mean()*100:+.2f}%")
    worst=j.gap.idxmin(); best=j.gap.idxmax()
    print(f"  worst window for S&P ends {worst.date()} ({j.gap.min():+.1f}pp), "
          f"best ends {best.date()} ({j.gap.max():+.1f}pp)")
print("\n"+"="*78)
print("BY CALENDAR PERIOD (CAGR in rupees)")
for s,e in [("2008-01","2012-12"),("2013-01","2017-12"),("2018-01","2022-12"),("2023-01","2026-08")]:
    w=px[(px.index>=s)&(px.index<=e)]
    if len(w)<24: continue
    yrs=len(w)/12
    n_=( float(w['^NSEI'].iloc[-1])/float(w['^NSEI'].iloc[0]) )**(1/yrs)-1
    si=(w['^GSPC']*w['INR=X'])
    s_=( float(si.iloc[-1])/float(si.iloc[0]) )**(1/yrs)-1
    print(f"  {s} to {e}   Nifty {n_*100:>+6.2f}%   S&P-in-INR {s_*100:>+6.2f}%   gap {(s_-n_)*100:>+6.2f}pp")
