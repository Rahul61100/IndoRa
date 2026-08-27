# /// script
# requires-python = ">=3.11"
# dependencies = ["yfinance","pandas","numpy"]
# ///
import yfinance as yf, pandas as pd, numpy as np
NAMES={"MUTHOOTFIN.NS":"Muthoot Finance","MANAPPURAM.NS":"Manappuram","IIFL.NS":"IIFL Finance",
       "TITAN.NS":"Titan (jewellery)","^NSEI":"Nifty"}
px=yf.download(["GC=F",*NAMES],period="5y",interval="1d",progress=False,auto_adjust=True)["Close"].ffill()
bad=[c for c in px.columns if px[c].notna().sum()<200]
if bad: print(f"(excluded, no data: {bad})"); px=px.drop(columns=bad)
r=np.log(px/px.shift(1))
g=r["GC=F"]
print("BETA TO GOLD — 5 years of daily log returns")
print("="*82)
print(f"  {'name':<20}{'beta':>8}{'r2':>7}{'1y ret':>9}{'3y ret':>10}{'ann vol':>9}")
for s,n in NAMES.items():
    if s not in r: continue
    j=pd.concat([g,r[s]],axis=1).dropna()
    if len(j)<200: continue
    x,y=j.iloc[:,0],j.iloc[:,1]
    b=float(np.cov(x,y)[0,1]/np.var(x)); c=float(np.corrcoef(x,y)[0,1])
    cl=px[s].dropna()
    r1=(float(cl.iloc[-1])/float(cl.iloc[-252])-1)*100 if len(cl)>252 else float('nan')
    r3=(float(cl.iloc[-1])/float(cl.iloc[-756])-1)*100 if len(cl)>756 else float('nan')
    v=float(y.std()*np.sqrt(252)*100)
    print(f"  {n:<20}{b:>8.3f}{c**2:>7.3f}{r1:>+8.1f}%{r3:>+9.1f}%{v:>8.1f}%")
gc=px["GC=F"].dropna()
print(f"\n  Gold itself: 1y {(float(gc.iloc[-1])/float(gc.iloc[-252])-1)*100:+.1f}%  "
      f"3y {(float(gc.iloc[-1])/float(gc.iloc[-756])-1)*100:+.1f}%  "
      f"spot ${float(gc.iloc[-1]):,.0f}  52w hi ${float(gc[-252:].max()):,.0f}")
# The real question: is the gold beta actually there, or is it a lending book that ignores gold?
print("\n" + "="*82)
print("STRESS CHECK — how did they do in gold's worst and best 20 days?")
gs=g.dropna().sort_values()
worst,best=gs.index[:20],gs.index[-20:]
for s,n in NAMES.items():
    if s not in r: continue
    y=r[s]
    w=float(y.reindex(worst).dropna().mean()*100); bb=float(y.reindex(best).dropna().mean()*100)
    print(f"  {n:<20}gold's worst 20d: {w:+.2f}%/day   gold's best 20d: {bb:+.2f}%/day   spread {bb-w:+.2f}pp")
print(f"  {'gold itself':<20}gold's worst 20d: {float(g.reindex(worst).mean()*100):+.2f}%/day   "
      f"gold's best 20d: {float(g.reindex(best).mean()*100):+.2f}%/day")
