# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance","pandas","numpy"]
# ///
import yfinance as yf, pandas as pd, numpy as np
# RSP = equal-weight S&P 500. ACWI = global. EFA = developed ex-US. VT = total world.
T={"^NSEI":"Nifty","^GSPC":"S&P capweight","RSP":"S&P EQUAL weight","ACWI":"MSCI ACWI",
   "EFA":"Developed ex-US","EEM":"EM ex-India-heavy","VT":"Total world"}
px=yf.download([*T,"INR=X"],period="max",interval="1mo",progress=False,auto_adjust=True)["Close"].ffill()
fx=px["INR=X"]
px=px.drop(columns=["INR=X"])
com=px.dropna()
print(f"common window {com.index[0].date()} -> {com.index[-1].date()}  ({len(com)} months)")
f=fx.reindex(com.index).ffill()
inr={}
for c in com.columns:
    inr[c]= com[c] if c=="^NSEI" else com[c]*f
inr=pd.DataFrame(inr)
yrs=len(inr)/12
print(f"\nCAGR IN RUPEES over the common window ({yrs:.1f}y)")
print("="*70)
nif=(float(inr['^NSEI'].iloc[-1])/float(inr['^NSEI'].iloc[0]))**(1/yrs)-1
rows=[]
for c in inr.columns:
    g=(float(inr[c].iloc[-1])/float(inr[c].iloc[0]))**(1/yrs)-1
    rows.append((T[c],g,g-nif))
for n,g,d in sorted(rows,key=lambda r:-r[1]):
    m="  <-- INDIA" if n=="Nifty" else ""
    print(f"  {n:<20}{g*100:>+8.2f}%   vs Nifty {d*100:>+7.2f}pp{m}")
# rolling 5y win rate vs Nifty, in rupees
W=60
print(f"\nROLLING {W//12}-YEAR WIN RATE vs Nifty, in rupees")
print("="*70)
r=(inr/inr.shift(W))**(12/W)-1
r=r.dropna()
for c in inr.columns:
    if c=="^NSEI": continue
    gap=(r[c]-r["^NSEI"])*100
    print(f"  {T[c]:<20}beat Nifty in {(gap>0).mean()*100:>3.0f}% of {len(gap)} windows   "
          f"mean {gap.mean():+6.2f}pp   worst {gap.min():+6.2f}pp")
