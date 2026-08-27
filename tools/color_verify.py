# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
import re, sys, pathlib
sys.path.insert(0,'/private/tmp/claude-501/-Users-rahul-gamerun-repo/aca7c6f3-3a8f-4e85-8919-af711e973fbf/scratchpad')
from color import hex2oklch, contrast
css = pathlib.Path('/Users/rahul/market-intel/predict/templates/base.html').read_text()
blocks = re.findall(r'(?::root\{|:root\[data-theme="dark"\]\{)(.*?)\n\}', css, re.S)
for name, blk in zip(("LIGHT","DARK"), blocks):
    t = dict(re.findall(r'--([\w-]+):(#[0-9A-Fa-f]{6})', blk))
    if not t: continue
    bg = t['bg']; print(f"\n{name}  (as shipped)")
    for k in ('ink','ink-2','ink-3','cold','warm','hot'):
        cr = contrast(t[k], bg); L,C,H = hex2oklch(t[k])
        ok = "AA body" if cr>=4.5 else ("AA large/UI" if cr>=3.0 else "*** FAIL ***")
        print(f"  {k:<7}{t[k]}  L{L:.3f} C{C:.3f} H{H:6.1f}  {cr:5.2f}:1  {ok}")
    cl,cc,ch = hex2oklch(t['cold']); wl,wc,wh = hex2oklch(t['warm'])
    d=abs(ch-wh); d=min(d,360-d)
    print(f"  accents  hue sep {d:.1f}°  ΔL {abs(cl-wl):.4f}  ΔC {abs(cc-wc):.4f}")
