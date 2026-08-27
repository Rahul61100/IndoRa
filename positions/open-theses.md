# Open theses and running scorecard

One row per live thesis. **A thesis with no invalidation condition is an opinion and does not
belong here.** Prices are the close from the snapshot named in the row; refresh before acting.

Horizons are fixed and do not blur:
- **SHORT** — months. Needs a dated catalyst *and* a trend *and* a stop — **and, from 2026-08-27,
  an expected gross edge of at least 10-12% over the best long-horizon alternative.** Indian STCG
  at 20% against LTCG at 12.5%, plus a ₹1.25L annual LTCG exemption that STCG does not get, means
  a sub-12-month trade must out-earn a >12-month hold by ~9.85% gross (≈11.8% at high income) just
  to break even after tax. **A modest edge held briefly is worse than the same idea held long.**
  [[short-horizon-needs-a-10-12-percent-tax-edge]]
- **MEDIUM** — 2-3 years. Staggered entry, no stop, reviewed on earnings.
- **LONG** — decades. Entry price matters, trend does not.

---

## Revision log

### 2026-08-27 (second pass) — the frame itself was wrong

The morning's governance pass changed three positions. This pass changed the **question**.

**The premise failed its own base rate.** For a rupee-spender, the S&P-in-INR beat the Nifty in
**97% of 108 rolling ten-year windows**, 92% of five-year and 72% of three-year, mean gap ~4.5pp/yr,
in every calendar sub-period since 2008. Equal-weight S&P beats cap-weight, so it is not a
Magnificent-7 artefact. India **beat** EM and roughly tied developed-ex-US — it lost only to the US.

Consequence for this file: **beating the Nifty is not the job.** Every thesis here now carries a
hurdle of roughly 4.5pp/yr against a passive foreign alternative, and `tools/score.py` prints
each position against both the Nifty and the S&P-in-INR from today. With **4 theses scored against
30 needed**, there is no evidence yet that this book clears it.

| Pick | Was | Now | Why |
|---|---|---|---|
| **Dixon** | MEDIUM, capped ×3 | **CLOSED** | Q1 FY27 revenue +21.1%, **operating income −8.6%**, net income +194.8% at **1.86× operating income** — the profit is below the line. Operating margin **2.29%**, down five straight quarters, and the thesis's own written invalidation was "margin below ~3%", which had already triggered **two quarters** before anything looked. Forward P/E 52.2 above trailing 43.2 means consensus expects EPS −17%. *A thesis that needs three caps has already been falsified and is being kept alive with qualifiers.* |
| **NTPC** | LONG, open | LONG, **flagged** | Only book position carrying an earnings-quality flag: forward P/E 11.7 above trailing 10.1, implying EPS −13%. Does not invalidate a 2032 capacity thesis, but the entry is not as cheap as the trailing multiple suggests. |
| **Infosys** | bench | bench, **risk re-framed** | Pharma-style trade risk was mis-specified. IT's US exposure is H-1B and the HIRE Act, not the Section 301 tariff — and the 301 action is a **60-country forced-labour programme**, not a bilateral India dispute, so it will not be resolved by a deal. |

**Three corrections to things stated earlier in this workspace, all in the same direction —
I had the mechanism wrong, not just the number:**

1. **The tariff.** In force is **Section 301(b)/304(a)**, 91 FR 47318, effective ~2026-07-24, at
   **10%** — but **~45% of India's US-bound exports (~$87bn) are exempt** under Annex I/II, so the
   effective rate across the basket is far below 10%. And India sits in a tier with Bangladesh,
   Cambodia, Indonesia, Malaysia and Pakistan: it was never targeted.
   [[india-us-tariff-the-actual-legal-instruments]]
2. **Generic pharma is 0% until August 2028**, then 100%, then 200% — Section 232, which the IEEPA
   ruling does not touch. Near-term risk zero, structural risk worse.
3. **Oil.** Indian equities *rise* with oil unconditionally, because oil proxies global demand.
   Only **supply** shocks hurt: in the four large ones in ten years the Nifty fell **every time**
   (mean −3.91%, worst −12.0%). **ONGC does not hedge them** — 50% hit rate, median +0.55%, because
   the windfall levy takes the gain exactly when it would matter. The ONGC close was right, but for
   a reason I had not identified.

**And the currency risk is larger than assumed.** Reserves near their high at $716.9bn conceal
record net dollar sales of **$53.1bn** in FY26 and a net forward book **short $103.1bn** at 31 March,
short in every maturity, widened $25.4bn in one month. The rupee is **10th of 12** EM currencies
since 1 July, weakening while the dollar fell 2.1%. The ~3.5%/yr depreciation in the base-rate work
is what was realised *during a record defence*, not a conservative assumption.
[[the-rupee-is-held-up-not-holding-up]]

**Open action for tomorrow:** the RBI Weekly Statistical Supplement was due **28 Aug 2026**. The
forward book is the number to read, not the reserve headline.

### 2026-08-26 — first technical pass, three theses changed

The 2026-08-25 note was built on valuation and macro only. Pulling actual price data the next
day contradicted three of the nine picks. Recorded in full because this is the pattern the
scorecard exists to catch.

| Pick | Was | Now | Why |
|---|---|---|---|
| ONGC | SHORT buy | **CLOSED before entry** | Oil and gas is the only sector with **0% of members above their 200 DMA**. ONGC in downtrend, RSI 32, 0.2% above its 52-week low. Brent is 26.9% *below* its high and the EIA forward view is $69 for 2027. The "oil hedge" was built on a spike that is already deflating. Thesis was wrong on the direction of its own driver. |
| HDFC Bank | SHORT trade | **MOVED to MEDIUM** | -26% over a year, 14.3% below its 200 DMA, RSI 38, 1.0% above its 52-week low, relative strength -24.7%. There is no technical base to place a stop against, and the NIM recovery is explicitly a multi-quarter mechanic. Correct thesis, wrong horizon. |
| Infosys | MEDIUM core | **MEDIUM, demoted to bench** | Guidance was *trimmed* to 1.5-3.0% at Q1 FY27. Negative revisions are still in progress. Keep the thesis, do not size it yet. |

Added in their place: ICICI Bank and HAL for SHORT, Dixon promoted to MEDIUM core.

**Lesson promoted to knowledge:** [[value-and-momentum-are-split]] — screening on valuation alone
in this tape produces a book of confirmed downtrends.

### 2026-08-26 (second pass) — a US supply-chain fact lands on an Indian thesis

No positions changed, but one **material risk was added to Dixon that was not in the thesis when
it was opened**, and it came from the US universe rather than the Indian one.

Gartner: DRAM and SSD prices up **130% by end-2026**, pushing smartphone prices +13% and PCs +17%,
driving **smartphone shipments -8.4% and PC shipments -10.4%** — the steepest device contraction
in over a decade. The pain is concentrated in **entry and mid-tier Android**, where memory is the
largest BOM swing and demand is most price-elastic. That is precisely Dixon's segment.

A ~3%-margin contract assembler paid per unit has neither the margin to absorb a BOM shock nor the
pricing power to pass one on, and a shipment contraction hits volume and margin together. The
policy tailwind (₹1.9 lakh crore across Semicon 2.0 and Mobile PLI 2.0) is unchanged and still
real; it now has to be weighed against a component-cost headwind.

**Action:** Dixon stays core at half position but is **capped — no adds** until BOM pass-through
terms are checked and monthly smartphone shipment data is being tracked as a thesis input.
Full note: [[memory-shortage-is-a-tax-on-device-makers]].

**Also sharpened, no action:** the standing L&T bench note. The India capex divergence resolved —
it is **execution quality, not demand**. Aggregate capital-goods order inflow excluding L&T was
₹32,400 crore in Q3 FY26, *down* year on year; the strength is concentrated in electrification and
automation (Siemens +32.6%, ABB +25%), while infrastructure EPC inflow barely moved (₹565bn in
Q4 FY26 against ₹548bn in Q3) with huge dispersion between contractors. Buy the capex theme through
equipment, not tonnage. [[india-capex-divergence-is-execution-not-demand]]

**Lesson promoted:** when a shortage makes an upstream supplier a star, ask who pays for it
downstream and whether we own them. The multi-market universe is what surfaced this — an
India-only view would not have seen it.

### 2026-08-26 (third pass) — the core India valuation claim does not survive

Deep research overturned the premise the whole India book was built on. Recording it in full
because this is the largest single error the workspace has produced.

**1. The equity risk premium is NEGATIVE.** India's 10-year G-sec yields **6.85%**; the Nifty's
earnings yield is **4.89%**. ERP is **−1.93% to −2.09%**, robust to every forward-P/E proxy. I
called Indian large caps cheap on the basis of a P/E 12.6% below its own 10-year average. That is
a comparison to India's past, not to the risk-free alternative available today, and on the
rate-adjusted test India is expensive. [[CORRECTION-india-erp-is-negative]]

**2. "Earnings +18%" was a quarter, not a year, and it was five stocks.** FY26 full-year growth
was **4.5%**, against 12-15% expected. FY25 was **3.4%** against ~15%. Two consecutive years of
delivering about a third of what was promised, and nine straight years of missing start-of-year
consensus. Of Q1 FY27's incremental profit, **60% came from ONGC, Hindalco, Reliance, JSW Steel
and Bharti Airtel** — a commodity base effect plus telecom tariffs. Meanwhile FY27 consensus EPS
was **cut ~9% over twelve months**. [[CORRECTION-india-earnings-growth-was-4-5-percent]]

**3. The flow evidence is worse than the currency data alone showed.** MSCI India is **−5.34%** in
USD over one year against MSCI EM **+37.06%** — a 42-point gap. India's MSCI EM weight has roughly
**halved from ~19-21% to ~12%**, dropping from second to fourth behind China, Taiwan and Korea.
And India remains the most expensive major EM at 20-22x forward against Taiwan 14-16x, China
10-13x, Korea 10-12x. [[india-lost-half-its-em-weight]]

**4. Two names in the book are among the biggest FY27 downgrades: HDFC Bank and Infosys.**

**Actions taken:**
- **HDFC Bank — MEDIUM position reduced from core to half, and no adds.** The NIM mechanics still
  hold, but I was buying a name whose forward estimates are being cut while calling it cheap on a
  book multiple. Both cannot be true without an explicit view on which wins, and I did not have
  one. The LONG tranche stands — a decades thesis on the deposit franchise survives an estimate
  cut; a two-year thesis does not.
- **Infosys — stays benched, now with confirmation.** It is on the downgrade list. The entry
  signal remains a guidance raise.
- **Whole-book framing changed.** The India case is no longer "cheap large caps re-rate". It is
  "a negative-ERP market held up by a domestic bid, where the return has to come from stock
  selection, not from the index". That is what the regime label already said
  ([[regime-labels-aug-2026]]) — the valuation work now agrees with the breadth work.
- **Open question that must be answered before adding any India equity risk:** at 6.85% risk-free
  and a negative ERP, *why own Indian equities at all rather than G-secs?*
  **ANSWERED 2026-08-27 by four adversarial archetypes — and the question was malformed.** The ERP
  metric has an R² of 0.5%, was quoted pre-tax and duration-mismatched, and a negative naive reading
  is *expected* in an economy compounding nominal GDP at 10%. **Freeze lifted for the MEDIUM and
  LONG horizons on stock-specific evidence only.** The SHORT bucket stays frozen — it needs a
  10-12% after-tax edge it has never been held to. Full verdict: [[india-the-adversarial-verdict]].

**Method lessons, both promoted to knowledge:**
- Trailing beats and forward cuts routinely coexist. **Check revision direction before calling
  anything a de-rating.**
- A multiple is only meaningful against the risk-free rate, never against its own history alone.

### 2026-08-26 (fourth pass) — the political-economy layer hits three positions at once

Added the political economy layer after correctly being told the analysis was running a Western
textbook on a market where proximity to power is a pricing factor. **It immediately found
problems in three open positions that no price series or financial statement contained.**

*Confidence: DEGRADED — this research ran after the session search cap, via news aggregation
rather than primary sources. Directionally strong; each item below needs primary re-verification
before it drives a trade.*

**1. HAL — the flagship programme is late and penalties are reportedly being considered.**
**Tejas Mk1A delivery is running 2+ years behind schedule** on GE F404-IN20 engine acceptance
failures, and the **MoD is reportedly planning financial penalties on HAL.** I bought HAL on trend
plus a rising defence budget, and explicitly logged the 7% revenue CAGR as the known weakness —
but I did not know the delay had reached the penalty stage. That is the *mechanism* by which a
7% CAGR persists despite a ₹94,000 crore order book.
**Action: HAL cut to half position and the stop tightened to its 50 DMA.** The trend thesis is
intact; the fundamental floor under it is weaker than I thought.

**2. L&T — its headline wins are European, not Indian.** The ~₹30,000 crore and ~₹15,000 crore
(TenneT offshore-wind transmission) awards in this window are **European export contracts, not
Indian NIP capex.** I have been holding L&T as *the* India-capex proxy. Partly wrong — a
meaningful slice of the order momentum is European offshore wind.
Compounding it: **NHAI awards are at a seven-year low** with debt down 43% from the FY22 peak and
no rebound expected in FY27, and **no NIP or Gati-Shakti-labelled awards were found at all.**
**Action: the L&T thesis is restated, not closed.** It stays on the bench. If the thesis is
"India capex", the vehicle should be electrification and equipment
([[india-capex-divergence-is-execution-not-demand]]); if the thesis is L&T, it must be underwritten
as a global E&C business with European exposure — a different analysis I have not done.

**3. Dixon — Mobile PLI 2.0 has not disbursed a rupee.** The ₹62,500 crore scheme was **cleared on
15 July 2026**; disbursement has not begun. Dixon and peers rallied on the *clearance*. And auto
PLI has disbursed **under 10%** of outlay while pharma API has disbursed **1.3%** — the base rate
for Indian scheme disbursement is poor. Dixon is already capped for the memory-BOM reason
([[memory-shortage-is-a-tax-on-device-makers]]); this is a second, independent reason.
**Action: no change to sizing — already capped — but the thesis note now records that the policy
leg is an approval, not a cash flow.**

**Method lesson, promoted:** **always ask whether something is approved, awarded, or paid.** Three
different things, routinely reported as one. [[announced-is-not-disbursed]]

### 2026-08-26 (fifth pass) — positioning data partly reverses this morning's HDFC Bank cut

*Confidence: DEGRADED — post-cap research. Acting on sizing, not on conviction.*

**HDFC Bank: FIIs cut their stake 360bps in the March quarter — roughly ₹35,000 crore sold**, the
largest single-stock FII sale found anywhere in the sweep. That is a **mechanical explanation for
the −26%**, and it changes the character of the thesis: I had been treating the fall as the market
disagreeing about NIM. A forced seller of that size **finishes**; a structural problem does not.

And **as of 22 August, financials are staging an FII comeback** — banks had been sold at ~₹1,100
crore a day through H1 and that has partially turned.

**Action: HDFC Bank stays at half in MEDIUM — no re-add yet — but the reason for the cut is now
narrower than when I made it.** The FY27 downgrade is real and still stands
([[CORRECTION-india-earnings-growth-was-4-5-percent]]). But "cheap on book while estimates fall"
and "sold ₹35,000 crore in one quarter by a foreign seller who has now started coming back" are
different situations, and the second is more favourable. **Re-add trigger: two consecutive months
of positive FII financials flow AND a Q2 NIM that does not make a new low.**

**Reliance — the decades thesis is corroborated by the insider.** The **promoter group bought
~₹8,500-9,000 crore in July 2026, lifting its stake to 50.48%** — the largest insider purchase
found in the sweep, into their own weakness, with the stock near a 52-week low. That is the
sum-of-parts argument being made with the promoter's own money. **No sizing change; conviction
raised.**

**Infosys — positioning is now emptied out.** ₹17,000 crore of FII selling in Indian IT in
February alone, **holdings at a four-year low**, a $9bn three-year exodus. That is the contrarian
half of the setup. **The other half — revisions turning — has still not happened, so it stays
benched.** But the entry condition is now two-sided: guidance raise *plus* a flow turn.

**SBI and ICICI Bank — corroborated.** Mutual funds are at a **three-year-high overweight in PSU
banks**, and overweight capital goods (17-month high) and healthcare, underweight IT.

**A new risk I had not counted.** Supply is materially larger than the IPO pipeline alone: block
deals are approaching **₹4 lakh crore in 2026**, **~$32bn of listed PE holdings still await
monetisation**, and government OFS is running hard (LIC alone 6.5% for ₹31,552 crore). Domestic
funds are absorbing it — but that is the *same* pool the SIP bid fills.

**And the sharpest warning in the data:** **large-cap fund inflows turned negative in July 2026 for
the first time since December 2023**, while small-cap inflows rose 39% and SIP totals hit a
five-month high. **Domestic retail is rotating down the cap curve into the two-sigma-expensive
segment.** That is where the next drawdown concentrates, and it is the 2017-18 analog setting up
exactly as described ([[regime-analog-is-a-splice-not-one-year]]).

### 2026-08-27 — first live market session; two theses degrade

**HDFC Bank — CLOSED in MEDIUM. The driver was never NIM.**

*(Revised later the same day, once the cause was identified.)* The fall is a **governance
overhang**: an alleged ~₹45 crore above-market "differential interest" payment to MSRDC to win
state deposits, the bank's own board calling it "business overreach" and fining the MD/CEO, CFO and
a Group Head **₹1 lakh each** on 27 July, the **RBI seeking a formal explanation on 31 July as to
why**, and a **US securities class action escalating 25-27 August**. Three consecutive 52-week
lows. [[hdfc-bank-msrdc-governance-overhang]]

**I cannot hold a position on NIM mechanics while the regulator is questioning whether the board's
own sanction on its CEO was adequate.** That is a different category of risk from a margin cycle,
and it was developing publicly since May while I built a NIM thesis, a flow thesis, a correlation
matrix and a risk table on top of it.

**Action: MEDIUM tranche closed entirely.** The LONG (decades) tranche is **suspended — no adds**
— pending the outcome of the RBI query and the US suit. A multi-decade thesis on a deposit
franchise can survive a margin cycle; it cannot be added to while management conduct is the open
question.

**Note the sell side has not moved:** consensus target **₹1,018.76**, 40 Buy / 1 Hold / 0 Sell
across 41 analysts, against ₹714. Only JM Financial (to ₹800, 25 Aug) and Investec (to Hold,
20 Jul) have revised. Treat that as inertia, not support.

**Superseded reasoning, kept for the record —** New 52-week low at ₹710.00 intraday,
−1.78% on **1.68x volume pace**, while **ICICI Bank was +1.38%** and Bank Nifty only −0.26%. My
re-add trigger required positive FII financials flow *and* a Q2 NIM that does not make a new low;
the stock is instead making a new **price** low. And the within-sector divergence argues the
problem is stock-specific, not the sector flow story I leaned on yesterday. **Stays at half.**
No disclosed cause — no block deal, pledge change, insider filing or rating action in seven days,
which points to an undisclosed seller working an order rather than news.

**Bharti Airtel — the catalyst is slipping. Downgrade to watch, exit on the next bounce.**
The entire thesis was the Jio listing inside an August-October window. As of 27 August: DRHP filed
19 June, **SEBI sought clarifications 25 June, and there is still no observation letter, no price
band and no listing date.** The stock closed **below its 50 DMA** on 26 August and is −0.79% today,
3.0% below its 20 DMA. I wrote at entry that if the event passes without a re-rating this gets
closed rather than converted to a hold. **The event has not passed — it has stalled — which is the
same thing for a position bought purely for it.** Action: **no adds, and exit into any strength
rather than waiting for the stop.** [[session-2026-08-27-india]]

**SBI — a supply fact, not a thesis change.** SBI is the **largest selling shareholder in the NSE
IPO** (~₹30,000-31,500 crore, offer-for-sale only, 4-4.5%). That is a cash inflow to SBI rather
than a claim on it, so the credit-cycle thesis is unaffected — but it is worth knowing that a name
I hold is monetising an asset into the heaviest supply window India has faced. SEBI's observation
letter was still pending on 23 August. **No change.**

**A note on what worked.** Steel rallied hard today — INOX India +6%, HCC +7%, NMDC Steel +5%,
Tata Steel a top gainer — on the Commerce Minister backing the safeguard duty on 24 August. Not
earnings. **The political-economy layer paid off within one session of being added to the loop.**

### 2026-08-27 (late) — the governance screen lands; HAL closes

**HAL — CLOSED.** I bought it on trend plus a rising defence budget and logged the 7% revenue CAGR
as the known weakness. The screen shows why that CAGR persists, and it is not execution drift:
**a fatal Tejas crash at the Dubai Airshow in November 2025, a second incident grounding the fleet
in February, zero Mk-1A jets delivered by June, MoD weighing penalties — and 199 forged supplier
test certificates found by HAL's own audit, with an FIR filed.**

**Forged test certificates on a fighter aircraft is a quality-control governance failure, not a
schedule problem.** Three separate reasons now point the same way: the governance chain, the
already-logged 35.2x multiple on a 7% ten-year revenue CAGR, and the **new 10-12% after-tax hurdle
on the SHORT bucket** ([[short-horizon-needs-a-10-12-percent-tax-edge]]) which a name with this
overhang cannot credibly clear. **Closed.** [[governance-screen-aug-2026]]

**ICICI Bank — HELD, but capped and flagged.** The screen calls it the closest structural analog to
the HDFC pattern: **six GST notices in six months totalling over ₹1,350 crore**, a SEBI warning on
FPI repatriation, an RBI penalty, and **a CEO reappointment publicly contested to the RBI, with the
activist escalating again on 24 August — three days ago, still open.**

Against that: revision breadth is the best in the book (28 up / 4 down, target +20%), price action
is the strongest in the sector, and F&O shows long build-up. **The thesis stands. But this is now a
capped position — no adds — and the CEO thread is a tracked item, not background.** Buying the
"clean alternative to HDFC Bank" only works while it stays clean.

**NTPC and Reliance — flagged on the long theses, no action.** NTPC carries a **live CBI FIR at
Ramagundam naming unnamed NTPC personnel** and a **CMD vacancy running 20+ months through two
failed selection rounds.** Reliance had a **Reliance SVP arrested by the CBI** in an April 2026
DGCA bribery probe and a **SEBI administrative warning** on employee insider trading. Neither is
disqualifying for a decades horizon, both are now on the record rather than absent from it.

**Bharti — the exit call is confirmed.** The screen finds **the heaviest promoter selling of the
nine: Mittal and Singtel sold over $4bn across 2025.** Already downgraded to exit-on-strength this
morning on the stalled Jio catalyst; this is a second, independent reason.

**Dixon — a data conflict to resolve.** The screen reports a **36% year-on-year net-profit drop**;
our own revision pull shows **TTM profit +119% and FY+1 EPS revised +10.07%**. Both cannot be right.
**Resolve before any sizing decision.** Also: JV partner **Vivo India is under an active ED/SFIO
money-laundering probe.**

**SBI — a false positive avoided.** SBI generates heavy CBI and ED headline volume from the Anil
Ambani / RCom fraud, **but SBI detected and classified that fraud and every ruling has upheld it.**
That is fraud control working. A keyword screen would have flagged it wrongly. **No change.**

**L&T — the only CLEAN name of the nine.**

---

## SHORT horizon (months)

### ICICI Bank — CORE
- **Entry logic:** the private bank that is actually working while the sector's largest name
  falls. Uptrend, above its 200 DMA, RSI 54, 91st percentile of its 52-week range, +13.8% over
  three months with relative strength +11.1% vs Nifty. P/E 18.2, P/B 2.70, ROE 15.9%.
- **Macro support:** system credit +17.7% year on year, ninth consecutive month of acceleration.
- **Catalyst:** Q2 FY27 results, October.
- **Invalidation:** loses its 200 DMA, or Q2 shows NIM compression alongside slowing advances.
- **Price at open:** ₹1,430 (2026-08-26)

### Bharti Airtel — CORE
- **Entry logic:** dated event. Jio Platforms filed its DRHP on 19 June 2026, listing expected in
  the Aug-Oct 2026 window at a $130-180bn valuation — India's largest IPO. Expected to lift
  telecom's index weight from 4-5% to 7-8%, forcing index buying in Bharti, and to clear the way
  for tariff increases. Jefferies models ~25% cumulative tariff hikes over FY27-28 and ~16% ARPU
  CAGR.
- **Catalyst:** Jio listing; tariff announcement.
- **Invalidation:** listing slips past December, or no tariff move by Q3 FY27.
- **Known weakness, logged at entry:** trend is mildly negative (-1.6% 1y, 2.1% below its 200 DMA,
  RSI 44) and the multiple is 38.9x with FY26 PAT having *fallen*. This is bought for the event
  alone. If the event passes without a re-rating, close it — do not convert it to a hold.
- **Price at open:** ₹1,902 (2026-08-26)

### Hindustan Aeronautics — CORE (replaces ONGC)
- **Entry logic:** defence is re-accelerating with breadth — sector +8.0% over a month, +19.7%
  over six, 75% of members above their 200 DMA, median RSI 58.6. HAL specifically is in an
  uptrend at RSI 54, so it is participating without being extended: 11.2% above its 200 DMA,
  92nd percentile, +13.1% over three months, relative strength +9.0%.
- **Fundamental backdrop:** FY27 defence budget ₹6.81 lakh crore, +13%. Order book ~₹94,000 crore
  against FY26 revenue of ₹33,089 crore. ROE 24%, ROCE 32%.
- **Catalyst:** order announcements; budget execution through H2.
- **Invalidation:** loses its 50 DMA, or a quarter that again shows revenue flat.
- **Known weakness, logged at entry:** **35.2x earnings and 7.98x book against a revenue CAGR of
  7% over ten, five *and* three years.** The order book has never converted at the rate the
  multiple implies. This is bought for trend and sector breadth, not for value.
- **Price at open:** ₹4,865 (2026-08-26)

**Bench (watched, not entered):** Eicher Motors — uptrend, RSI 59, insulated from the monsoon
that threatens tractor and rural demand, but already at the 95th percentile of its range.

---

## MEDIUM horizon (2-3 years)

### State Bank of India — CORE
- **Entry logic:** cheapest large exposure to the credit cycle. P/E 11.5, P/B 1.56, ROE 15.4%,
  FY26 PAT ₹86,666 crore. 22% deposit share, 20% advances. PSU banks are outpacing private banks
  in this credit cycle. Subsidiary stack effectively free at this multiple.
- **Confirmed by the tape:** +28.9% over a year, uptrend, above its 200 DMA, relative strength
  +29.8%. This is the pick that is working.
- **Invalidation:** system credit growth decelerating below ~12%, or a slippage cycle in the
  corporate book.
- **Price at open:** ₹1,048 (2026-08-25)

### Dixon Technologies — CORE (promoted from bench)
- **Entry logic:** the policy push is ₹1.9 lakh crore — Semicon 2.0 at ₹1.27 lakh crore plus
  Mobile PLI 2.0 at ₹62,500 crore, with mobile exports targeted to double from ₹7.5 to ₹15 lakh
  crore. Dixon holds an ECMS camera-module approval. TTM profit +119%, three-year sales CAGR 59%,
  ROE 37.4%.
- **Confirmed by the tape:** EMS is the sharpest turn in the market — the basket is -12.8% over a
  year but **+27.9% over three months with 100% of members above their 200 DMA.** Dixon in
  uptrend, 20.9% above its 200 DMA, RSI 61.
- **Invalidation:** loss of a major customer programme, or margin compression below ~3%.
- **Known weakness:** 48.9x earnings on a contract manufacturer with thin margins and heavy
  customer concentration. Half position.
- **Price at open:** ₹14,735 (2026-08-26)

### HDFC Bank — CORE (moved down from SHORT)
- **Entry logic:** see [[hdfc-bank-nim-is-structural]]. Record-low 3.26% NIM is the floor; the
  recovery levers are mechanical — ₹40-50k crore of high-cost borrowing maturing, two-thirds of
  deposit repricing already through, retail funding mix going 52% to 60%. Bought at 1.87x book,
  a near-decade-low multiple for the best deposit franchise in India.
- **Entry method:** staggered accumulation over 6+ months. **No stop** — the horizon absorbs the
  drawdown. Do not size it as if it were a trade.
- **Invalidation:** NIM makes a *new* low below 3.20% in Q2 or Q3 FY27, or the borrowing runoff
  schedule slips.
- **Price at open:** ₹727 (2026-08-26)

**Bench — but the reason has narrowed (2026-08-27).** The capex contradiction is resolved
([[india-capex-the-conversion-rate-collapsed]]): a real, executed capex cycle IS running in large,
capital-intensive corporates above the ~75% utilisation threshold — and **L&T-type names are the
correct investable expression of it, while a broad capex basket is not.** My doubt was about
*which contracts* (European offshore wind rather than Indian NIP), which is a separate question
from whether the cycle exists. **The vehicle was right.** Stays benched only on the contract-mix
question and negative revision breadth (5 up / 9 down), not on the thesis. Original note follows —
L&T — right sector, wrong horse. Capital goods is the broadest uptrend in the market
(100% breadth, +30.2% 1y) but L&T at +12.3% is the sector's *laggard*; ABB +50.3% and Siemens
+26.4% are the momentum expressions. Hold the thesis, consider switching the vehicle.

**Bench:** Infosys — 14.9x, 4.2% dividend yield, ROE 31.9%, ROCE 40%, and AI already 8.2% of
revenue. But FY27 guidance was trimmed. **The entry signal is a guidance raise, not a cheap
multiple.** See [[nifty-it-derated-on-ai-disruption]].

---

## LONG horizon (decades)

### HDFC Bank — CORE
Separate tranche from the MEDIUM entry above, separate money, never sold on the medium thesis.
India's credit-to-GDP is roughly 55% against 150%+ in developed economies; that gap closes over
decades and the winner is whoever funds cheapest. Bought at 1.87x book.

### NTPC — CORE
91 GW today going to ~150 GW by FY32, of which 60 GW renewable via NTPC Green, plus 30 GW of new
thermal and a $62bn / 30 GW nuclear plan to 2044. ₹16.68 lakh crore of committed capex through
FY37. Regulated ~15% RoE compounds book value with a 2.65% yield on top. P/E 11.9, P/B 1.62.
Peak national demand hit a record 270 GW; electricity's share of total energy is heading to 23%.
- **Logged weakness:** power and utilities is the second-worst sector on breadth (20% above their
  200 DMA) and NTPC itself is in a downtrend at RSI 38, -13.5% over three months. For a decades
  horizon that is an entry, not a disqualifier — but do not pretend the tape agrees yet.

### Reliance Industries — CORE
A sum-of-parts argument, not a compounding one. Market cap ~₹17.85 lakh crore ≈ $186bn against a
Jio Platforms IPO valuation of $130-180bn on a stake of roughly two-thirds — so Jio alone is
around half to two-thirds of the whole company, leaving retail, O2C, E&P and new energy close to
free. The listing is the event that forces the market to price the parts.
- **Logged weakness:** ROE 8.91%, TTM profit growth 0%, ten-year profit CAGR 10% — *below* nominal
  GDP. This is a discount-to-parts bet with a catalyst, not a quality compounder. And oil and gas
  has 0% sector breadth.

**Want, wrong price:** Divi's Laboratories. Structurally the correct pharma exposure — CDMO and
custom synthesis, which the 2028/2029 US generic tariff schedule does not touch
([[generic-pharma-tariff-bomb]]), riding China+1 and BIOSECURE, Q1 FY27 PAT +65.5%. But RSI 78,
exactly at its 52-week high, 35.1% above its 200 DMA. **Wait for a pullback toward the 50 DMA.**

---

## Scorecard

| Date | Thesis | Status | Note |
|---|---|---|---|
| 2026-08-25 | Nine picks across three horizons | opened | Built on valuation and macro; no price data pulled |
| 2026-08-26 | ONGC | **closed, wrong** | Driver was already reversing. Cost of not checking the tape. |
| 2026-08-26 | HDFC Bank short | **rehorizoned** | Right thesis, wrong horizon |
| 2026-08-26 | Infosys | **demoted** | Revisions still negative |
| 2026-08-26 | SBI, Dixon | **confirmed** | Trend and breadth agree with the fundamentals |
| 2026-08-26 | ICICI Bank, HAL | opened | Replacements, trend-confirmed |
| 2026-08-26 | Dixon | **risk added, capped** | Memory BOM shock + shipment contraction; found via the US universe |
| 2026-08-26 | L&T | thesis sharpened | Capex divergence is execution, not demand — equipment over EPC |
| 2026-08-26 | **Whole India book** | **premise overturned** | ERP negative ~200bp; FY26 EPS grew 4.5% not 18%; EM weight halved |
| 2026-08-26 | HDFC Bank (MEDIUM) | **cut to half, no adds** | Among the largest FY27 downgrades |
| 2026-08-26 | India equities | **new positions frozen** | Until the "why not G-secs at 6.85%" question is answered |
| 2026-08-26 | **HAL** | **cut to half, stop tightened** | Tejas Mk1A 2+ yrs late; MoD reportedly weighing penalties |
| 2026-08-26 | **L&T** | **thesis restated** | Headline wins are European, not Indian NIP; NHAI awards at 7-year low |
| 2026-08-26 | Dixon | second risk logged | Mobile PLI 2.0 cleared 15 Jul, nothing disbursed |
| 2026-08-26 | HDFC Bank | **cut reason narrowed** | −26% was ₹35,000cr of FII selling in one quarter; FIIs returning to financials since 22 Aug |
| 2026-08-26 | Reliance | **conviction raised** | Promoter bought ~₹9,000cr in July, stake to 50.48% |
| 2026-08-26 | Infosys | half the setup in place | FII IT holdings at a 4-year low; revisions still negative |
| 2026-08-27 | **Bharti Airtel** | **downgraded to watch — exit on strength** | Jio IPO stalled at SEBI; no observation letter, no price band; stock below 50 DMA |
| 2026-08-27 | **HDFC Bank** | **MEDIUM CLOSED; LONG suspended** | Governance: MSRDC ₹45cr payment, RBI query into the board's own penalty, US class action |
| 2026-08-27 | **Process** | **failure recorded** | The governance agent never launched — and that is exactly where the loss was |
| 2026-08-27 | Infosys | bench confirmed with data | 4 up / 30 down, FY+1 EPS −2.51% over 90d |
| 2026-08-27 | HDFC Bank | close confirmed independently | 7 up / 23 down, EPS −4.35%, target 41.9% above price — value-trap signature |
| 2026-08-27 | ICICI Bank | corroborated | 28 up / 4 down, target +20% — estimates and price agree |
| 2026-08-27 | **Reliance** | **tension flagged** | Promoter bought ~₹9,000cr in July; FY+1 EPS cut 5.23% in 30 days |
| 2026-08-27 | **SHORT bucket** | **hurdle raised** | Needs 10-12% gross edge over a long hold, after tax — never applied before |
| 2026-08-27 | Buyback names | stale note corrected | Budget 2026 restored capital-gains treatment for non-promoters |
| 2026-08-27 | **SBI, NTPC** | **short build-up flagged** | Both showing F&O short build-up; SBI flipped from long in a day — tentative |
| 2026-08-27 | Flow reading | **method corrected** | FIIs net cash buyers while ~1:8.25 short index futures — cash alone was misleading |
| 2026-08-27 | **HAL** | **CLOSED** | 199 forged test certificates, fatal crash, fleet grounding, zero Mk-1A delivered |
| 2026-08-27 | **ICICI Bank** | **capped, CEO thread tracked** | 6 GST notices >₹1,350cr; reappointment contested to RBI, escalated 24 Aug |
| 2026-08-27 | Bharti | exit confirmed independently | Mittal + Singtel sold >$4bn across 2025 |
| 2026-08-27 | Dixon | **data conflict — resolve** | Screen says PAT −36% YoY; our pull says TTM +119% |
| 2026-08-27 | SBI | false positive avoided | RCom fraud headlines are SBI *detecting* fraud, not committing it |
| 2026-08-27 | SBI | supply fact logged | Largest selling shareholder in the NSE IPO |
| 2026-08-26 | ONGC (closed) | **invalidation had already fired** | Windfall levy was reintroduced in March 2026 — I wrote the condition against a false premise |
