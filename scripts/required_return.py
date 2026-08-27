# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
What must be true for Indian equities to beat a G-sec — decomposed, after tax.

    uv run scripts/required_return.py

The equity risk premium I have been quoting (earnings yield 4.89% vs G-sec 6.85%,
so −1.96%) is a PRE-TAX comparison. For a taxable Indian resident those two income
streams are taxed very differently:

    G-sec interest   taxed at SLAB, with the ordinary surcharge ladder (up to 37%)
    Equity LTCG      12.5%, with surcharge statutorily CAPPED at 15%

That is not a detail. It can invert the sign of the premium. This computes the
after-tax hurdle properly at each income band, then decomposes what earnings growth
is required under different multiple paths.
"""
from __future__ import annotations

CESS = 0.04
GSEC = 0.0685
EARNINGS_YIELD = 0.0489
DIV_YIELD = 0.0120          # Nifty ~1.16-1.25%
PE_NOW = 20.46
PE_10Y_AVG = 23.33

# (label, slab rate on interest, surcharge on ORDINARY income, surcharge on LTCG)
# LTCG surcharge is capped at 15% by statute regardless of income; interest is not.
BANDS = [
    ("income < ₹50L",        0.30, 0.00, 0.00),
    ("₹50L-1cr",             0.30, 0.10, 0.10),
    ("₹1-2cr",               0.30, 0.15, 0.15),
    ("₹2-5cr",               0.30, 0.25, 0.15),
    ("> ₹5cr (old regime)",  0.30, 0.37, 0.15),
]


def eff(rate: float, surcharge: float) -> float:
    return rate * (1 + surcharge) * (1 + CESS)


print("=" * 78)
print("THE EQUITY RISK PREMIUM, AFTER TAX")
print("=" * 78)
print(f"  G-sec 10y {GSEC:.2%} (taxed at slab)   vs   Nifty earnings yield "
      f"{EARNINGS_YIELD:.2%} (LTCG 12.5%)")
print(f"  Pre-tax ERP: {EARNINGS_YIELD - GSEC:+.2%}   <- the number I have been quoting\n")
print(f"  {'income band':<24}{'g-sec tax':>10}{'net g-sec':>11}{'LTCG tax':>10}"
      f"{'equity hurdle':>14}{'ERP after tax':>15}")
for label, slab, sur_ord, sur_ltcg in BANDS:
    t_int = eff(slab, sur_ord)
    t_ltcg = eff(0.125, sur_ltcg)
    net_gsec = GSEC * (1 - t_int)
    hurdle = net_gsec / (1 - t_ltcg)      # pre-tax equity return needed to match
    erp_after = EARNINGS_YIELD - hurdle
    flag = "  <-- POSITIVE" if erp_after > 0 else ""
    print(f"  {label:<24}{t_int:>9.1%}{net_gsec:>11.2%}{t_ltcg:>10.1%}"
          f"{hurdle:>14.2%}{erp_after:>+15.2%}{flag}")

print("\n  The pre-tax premium is negative at every band. After tax it turns POSITIVE")
print("  for higher earners, because G-sec interest carries the full surcharge ladder")
print("  while equity LTCG surcharge is capped at 15% by statute.")

print("\n" + "=" * 78)
print("WHAT EARNINGS GROWTH IS REQUIRED — 5-year horizon")
print("=" * 78)
print("  Total return ≈ dividend yield + earnings growth + annualised multiple change\n")
scenarios = [
    ("multiple unchanged at 20.46x", PE_NOW),
    ("re-rates to the 10y avg 23.33x", PE_10Y_AVG),
    ("de-rates to 18x", 18.0),
    ("de-rates to 16x", 16.0),
]
_, slab, sur_ord, sur_ltcg = BANDS[3]           # ₹2-5cr band as the working case
hurdle = GSEC * (1 - eff(slab, sur_ord)) / (1 - eff(0.125, sur_ltcg))
print(f"  Using the ₹2-5cr band: after-tax-equivalent equity hurdle = {hurdle:.2%}\n")
print(f"  {'multiple path':<34}{'Δmult p.a.':>12}{'required EPS growth':>22}")
for label, target in scenarios:
    dmult = (target / PE_NOW) ** (1 / 5) - 1
    req_g = hurdle - DIV_YIELD - dmult
    print(f"  {label:<34}{dmult:>+11.2%}{req_g:>21.2%}")

print("\n" + "=" * 78)
print("AGAINST THE DELIVERED RECORD")
print("=" * 78)
for yr, actual, expected in (("FY25", 3.4, 15.0), ("FY26", 4.5, 13.5)):
    print(f"  {yr}: delivered {actual:.1f}% against {expected:.1f}% expected  "
          f"(miss {expected-actual:.1f}pp)")
print("  Nine consecutive years of missing start-of-year consensus.")
print("\n  Two-year mean delivered growth: 3.95%.")
for label, target in scenarios:
    dmult = (target / PE_NOW) ** (1 / 5) - 1
    tot = DIV_YIELD + 0.0395 + dmult
    verdict = "BEATS the hurdle" if tot > hurdle else "MISSES the hurdle"
    print(f"    at 3.95% growth, {label:<34} total {tot:>+7.2%}   {verdict}")
