# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Audit the INDORA palette with real colorimetry: sRGB -> OKLCH, WCAG contrast."""
import math

# ---------- sRGB <-> linear ----------
def s2l(c):
    c /= 255
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def l2s(c):
    v = 12.92*c if c <= 0.0031308 else 1.055*(c**(1/2.4))-0.055
    return max(0, min(255, round(v*255)))
def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def rgb2hex(r, g, b):
    return '#%02X%02X%02X' % (r, g, b)

# ---------- OKLab (Björn Ottosson) ----------
def rgb2oklab(r, g, b):
    lr, lg, lb = s2l(r), s2l(g), s2l(b)
    l = 0.4122214708*lr + 0.5363325363*lg + 0.0514459929*lb
    m = 0.2119034982*lr + 0.6806995451*lg + 0.1073969566*lb
    s = 0.0883024619*lr + 0.2817188376*lg + 0.6299787005*lb
    l_, m_, s_ = l**(1/3), m**(1/3), s**(1/3)
    return (0.2104542553*l_+0.7936177850*m_-0.0040720468*s_,
            1.9779984951*l_-2.4285922050*m_+0.4505937099*s_,
            0.0259040371*l_+0.7827717662*m_-0.8086757660*s_)
def oklab2rgb(L, a, b):
    l_ = L + 0.3963377774*a + 0.2158037573*b
    m_ = L - 0.1055613458*a - 0.0638541728*b
    s_ = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l_**3, m_**3, s_**3
    return (l2s( 4.0767416621*l - 3.3077115913*m + 0.2309699292*s),
            l2s(-1.2684380046*l + 2.6097574011*m - 0.3413193965*s),
            l2s(-0.0041960863*l - 0.7034186147*m + 1.7076147010*s))
def hex2oklch(h):
    L, a, b = rgb2oklab(*hex2rgb(h))
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    return L, C, H
def oklch2hex(L, C, H):
    a = C*math.cos(math.radians(H)); b = C*math.sin(math.radians(H))
    return rgb2hex(*oklab2rgb(L, a, b))

# ---------- WCAG ----------
def lum(h):
    r, g, b = hex2rgb(h)
    return 0.2126*s2l(r) + 0.7152*s2l(g) + 0.0722*s2l(b)
def contrast(f, b):
    a, c = lum(f), lum(b)
    hi, lo = max(a, c), min(a, c)
    return (hi+0.05)/(lo+0.05)

CUR = {
 "LIGHT": {"bg":"#F7F5F1","panel":"#FFFDFA","ink":"#141009","ink-2":"#5B5348",
           "ink-3":"#8E8578","cold":"#00767F","warm":"#A96200","hot":"#AF2318"},
 "DARK":  {"bg":"#08070D","panel":"#131120","ink":"#F4F1FB","ink-2":"#A49DBD",
           "ink-3":"#6C6489","cold":"#33E1EC","warm":"#FFBB57","hot":"#FF7C6C"},
}

for theme, p in CUR.items():
    print(f"\n{'='*78}\n{theme} — current palette measured in OKLCH\n{'='*78}")
    print(f"  {'token':<8}{'hex':<10}{'L':>6}{'C':>7}{'H':>7}   contrast vs bg")
    bg = p["bg"]
    for k, v in p.items():
        L, C, H = hex2oklch(v)
        cr = contrast(v, bg)
        flag = ""
        if k.startswith("ink") or k in ("cold","warm","hot"):
            if cr < 3.0: flag = "  ✗ FAILS 3:1 (UI/large-text floor)"
            elif cr < 4.5: flag = "  ⚠ under 4.5:1 (body-text AA)"
        print(f"  {k:<8}{v:<10}{L:>6.3f}{C:>7.3f}{H:>7.1f}   {cr:>5.2f}:1{flag}")

    cl, cc, ch = hex2oklch(p["cold"]); wl, wc, wh = hex2oklch(p["warm"])
    dh = abs(ch-wh); dh = min(dh, 360-dh)
    print(f"\n  ACCENT RELATIONSHIP")
    print(f"    hue separation      {dh:.1f}°   (180° = true complement)")
    print(f"    lightness gap       {abs(cl-wl):.3f} L  "
          f"{'← UNBALANCED, one accent will dominate' if abs(cl-wl) > 0.05 else 'balanced'}")
    print(f"    chroma gap          {abs(cc-wc):.3f} C  "
          f"{'← one reads far more saturated' if abs(cc-wc) > 0.04 else 'balanced'}")
