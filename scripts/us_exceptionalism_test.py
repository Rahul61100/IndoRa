# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance","pandas","numpy"]
# ///
import yfinance as yf, pandas as pd, numpy as np
# Is US outperformance at an extreme? Test three ways.
px=yf.download(["^GSPC","ACWI","EFA","EEM","^NSEI","INR=X","RSP"],period="max",interval="1mo",
               progress=False,auto_adjust=True)["Close"].ffill()
d=px.dropna()
print(f"common window {d.index[0].date()} -> {d.index[-1].date()} ({len(d)} months)\n")

# 1. US vs rest-of-world ratio, and where it sits in its own history
r=d["^GSPC"]/d["EFA"]
z=(r-r.rolling(60).mean())/r.rolling(60).std()
print("1. S&P / developed-ex-US ratio")
print(f"   now {float(r.iloc[-1]):.3f}   5y-z {float(z.iloc[-1]):+.2f}   "
      f"percentile of full history {float((r<r.iloc[-1]).mean()*100):.0f}%")
rem=d["^GSPC"]/d["EEM"]
print(f"   S&P / EM ratio: percentile {float((rem<rem.iloc[-1]).mean()*100):.0f}%")

# 2. Equal-weight vs cap-weight: is concentration at an extreme?
c=d["^GSPC"]/d["RSP"]
print(f"\n2. cap-weight / equal-weight S&P ratio")
print(f"   now {float(c.iloc[-1]):.3f}   percentile {float((c<c.iloc[-1]).mean()*100):.0f}%   "
      f"({'concentration near a record' if (c<c.iloc[-1]).mean()>0.9 else 'not extreme'})")
print(f"   trailing 1y: cap-weight {(float(d['^GSPC'].iloc[-1])/float(d['^GSPC'].iloc[-13])-1)*100:+.1f}%  "
      f"equal-weight {(float(d['RSP'].iloc[-1])/float(d['RSP'].iloc[-13])-1)*100:+.1f}%")

# 3. Does past US outperformance predict FUTURE US underperformance? The real question.
W=60
fw=60
excess=((d["^GSPC"]/d["^GSPC"].shift(W))**(12/W)-1)-((d["EFA"]/d["EFA"].shift(W))**(12/W)-1)
fwd=((d["^GSPC"].shift(-fw)/d["^GSPC"])**(12/fw)-1)-((d["EFA"].shift(-fw)/d["EFA"])**(12/fw)-1)
j=pd.concat([excess,fwd],axis=1).dropna(); j.columns=["past5y","next5y"]
if len(j)>24:
    corr=float(np.corrcoef(j.past5y,j.next5y)[0,1])
    print(f"\n3. Does 5y US excess return predict the NEXT 5y? (n={len(j)})")
    print(f"   correlation {corr:+.2f}   r2 {corr**2:.3f}")
    hi=j[j.past5y>j.past5y.quantile(0.75)]
    lo=j[j.past5y<j.past5y.quantile(0.25)]
    print(f"   after the TOP quartile of US outperformance, next 5y US excess: {hi.next5y.mean()*100:+.2f}%/yr "
          f"(positive {int((hi.next5y>0).sum())}/{len(hi)})")
    print(f"   after the BOTTOM quartile,                  next 5y US excess: {lo.next5y.mean()*100:+.2f}%/yr "
          f"(positive {int((lo.next5y>0).sum())}/{len(lo)})")
# 4. same test for Nifty specifically, in rupees
sp_inr=d["^GSPC"]*d["INR=X"]
ex2=((sp_inr/sp_inr.shift(W))**(12/W)-1)-((d["^NSEI"]/d["^NSEI"].shift(W))**(12/W)-1)
fw2=((sp_inr.shift(-fw)/sp_inr)**(12/fw)-1)-((d["^NSEI"].shift(-fw)/d["^NSEI"])**(12/fw)-1)
j2=pd.concat([ex2,fw2],axis=1).dropna(); j2.columns=["past5y","next5y"]
if len(j2)>24:
    c2=float(np.corrcoef(j2.past5y,j2.next5y)[0,1])
    print(f"\n4. Same test, S&P-in-INR vs Nifty (n={len(j2)})")
    print(f"   correlation {c2:+.2f}   r2 {c2**2:.3f}")
    hi=j2[j2.past5y>j2.past5y.quantile(0.75)]
    print(f"   after the top quartile of S&P-in-INR outperformance, next 5y: {hi.next5y.mean()*100:+.2f}%/yr "
          f"(S&P still ahead {int((hi.next5y>0).sum())}/{len(hi)})")
    print(f"   CURRENT past-5y reading: {float(j2.past5y.iloc[-1])*100:+.2f}%/yr  "
          f"(percentile {float((j2.past5y<j2.past5y.iloc[-1]).mean()*100):.0f}%)")
