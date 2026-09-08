# Errata and internal inconsistencies of the anchor-3 meta-analysis (PMC13302755)

Record under §5 of the [protocol](protocolo-estudo12.md). Every item decided against a primary source carries the literal quotation that decides it. The review's published cells remain untouched as layer 1 in [`ancora3-camada1.json`](ancora3-camada1.json); the grading ruler is layer 2 of the same file, and the arithmetic is reproducible by [`cenarios-ancora3.py`](../../scripts/estudo12/cenarios-ancora3.py).

**Who did what.** Unlike anchor 1, where the first discrepancy was *raised by the local models* and only then confirmed, **every item here was raised by the adjudicator (Claude) during the construction of the key, before any model had been called**, under the benchmark author's supervision. No local model has yet read this anchor. That ordering matters for how the campaign may later be described: whatever the six models do on anchor 3, they will not have discovered these errata — they will have been measured against them.

**How the published cells were recovered at all.** The review prints no per-trial cells in text. Its eight cells exist only inside Figure 3, a raster forest plot. They were read by vision and then verified by reconstruction: the sixteen read cells predict 48 other printed values on the same figure — eight odds ratios, sixteen confidence limits, eight weights, τ², χ², I², and the diamond with its interval — all of which reproduce ([`verificar-figura3.py`](../../scripts/estudo12/verificar-figura3.py), 48 of 48). The reading is therefore verified by arithmetic rather than trusted.

**A note of fairness.** Six of the eight trials check out cell for cell against their sources ([`verificar-camada2.py`](../../scripts/estudo12/verificar-camada2.py)), including two where the source makes the extraction genuinely awkward — Kirov, which publishes survivors rather than deaths, and Memis, which publishes no per-arm count at all and had to be tallied patient by patient from a table. Transcription errors happen in any hand-made review; this benchmark's own adjudicator logged three of them on anchor 1 and had to withdraw two published entries. The point is the process, not the authors.

---

## A. Confirmed against the primary source

### 1. Shaker 2025 — events of two arms, denominator of one

The review's forest plot records **15/30** in the methylene-blue arm. The trial has three arms:

> Group A (n = 30) was given a placebo in the form of 100 ml of 0.9% NaCl … Group B (n = 30) received a bolus of MB 1 mg/kg; and Group C (n = 30) received a bolus of MB 4 mg/kg in the same manner.

> Mortality rate | 14 (46.7%) | 9 (30.0%) | 6 (20.0%) | 0.083

The two active arms carry 9 and 6 deaths. **9 + 6 = 15**, which is the published numerator; the denominator stayed at one arm's 30 instead of the pooled 60. Correct pooling of both active arms against the shared control gives **15/60 against 14/30**.

Effect on the trial's own estimate: **OR 1.14 [0.41; 3.15] → 0.38 [0.15; 0.96]** — from slightly against methylene blue to significantly in its favour. The trial carries 16.9% of the pooled weight.

### 2. Aguilar 2016 — survivors placed in the events column

The review's forest plot records **24/30** and **19/30**. The source:

> se pudo observar que en el grupo A la mortalidad al egreso fue de 20.0% y no varió a los 21 días, a diferencia del grupo C, donde al egreso la mortalidad fue de 36.6% y a los 21 días, de igual forma, no varió.

with the arms defined as *"grupo A (azul de metileno), grupo C (grupo control)"* and thirty patients per arm. 20.0% of 30 is **6**; 36.6% of 30 is **11**. And 30 − 6 = 24, 30 − 11 = 19: **the published cells are the survivors, not the deaths.**

Effect on the trial's own estimate: **OR 2.32 [0.72; 7.41] → 0.43 [0.14; 1.38]** — a reversal of direction. The trial carries 14.0% of the pooled weight.

This also resolves an internal contradiction the review carries in plain sight: its own Table 1 records *"↓ Mortality"* for Aguilar, which agrees with the source and disagrees with its own forest plot.

**Why this is an inversion and not a reporting convention.** Kirov 2001 publishes the same kind of datum — survivors rather than deaths:

> Survivors at day 28 | 5 | 3

with ten patients per arm. There the review converted correctly, recording 5/10 and 7/10. The same team, the same structure of source datum, opposite outcomes. A convention would have applied to both.

---

## B. Confirmed inside the review itself, without recourse to any source

### 3. The primary analysis is described three incompatible ways

| Where | What it says | Composition |
|---|---|---|
| §3.5, text | *"when the analysis was restricted to the eight septic shock trials, excluding Levin et al. (2004)"* | eight, **without** Levin, **with** Kuri |
| Figure 3 | the eight rows printed | eight, **with** Levin, **without** Kuri |
| Table 2, GRADE | *"28–30-day all-cause mortality (8 studies; n = 479)"* | a third set: Table 1's eight septic trials |

The totals settle that these are genuinely different analyses and not three descriptions of one: Figure 3 sums 213 + 218 = **431** patients, while the GRADE table reports **479**. The benchmark grades against the forest plot, because it is the only one of the three with cells attached; the discrepancy is reported, not reconciled.

### 4. The GRADE denominator matches neither the figure nor the trials it names

479 is the sum of Table 1's N for the eight septic-shock trials — which includes Kuri 2025 and the whole of Shaker's 90 patients, and excludes Levin. It is not the 431 of the analysis actually run.

---

## C. Undeclared methodological choice (not an error)

### 5. The pooling method is not the one the methods section implies

The review's methods declare random-effects pooling without naming the between-study variance estimator. The published diamond — **OR 0.73 [0.40; 1.36], τ² 0.1334, I² 21.3%** — does **not** reproduce under DerSimonian–Laird, which gives 0.737 [0.449; 1.208] with τ² 0.1065. It reproduces digit-for-digit under **Paule–Mandel with the Hartung–Knapp adjustment** and Student's *t* at *k*−1 degrees of freedom: τ² 0.1334, all eight weights identical to the printed ones, interval [0.40; 1.36].

The numbers are right for the method actually used, and this is the default of recent versions of the R `meta` package. The item is recorded because an analyst reproducing the review from its methods section alone will not land on the published interval, and because the benchmark had to discover it before it could grade a model fairly.

---

## D. Outcome-window divergence, partially confirmed

### 6. Aguilar contributes a 21-day figure to an analysis labelled 28–30 days

The source states that its mortality was measured at ICU discharge and at 21 days, and, explicitly, that at 28 days there was nothing to report:

> aunque se debe notar que esta mortalidad fue al alta de la UCI y que a los 28 días no se obtuvieron diferencias en la mortalidad.

No 28-day per-arm numbers exist in the trial. Whatever cell Aguilar contributes to a 28–30-day analysis is a 21-day cell. Table 1 of the review records follow-up windows of 24 to 96 hours across the whole set, which is a separate labelling problem; but Luis-Silva does publish at 30 days and Dong at 28, so the Table 1 column describes the haemodynamic window rather than the outcome window, and the divergence is confirmed only for Aguilar.

The benchmark's frozen handling is to use the 21-day figure and to run the exclusion as a pre-registered sensitivity analysis (§5, A3-D5). Both are reported below.

---

## E. What the corrections do to the published result

All by the review's own estimator (Paule–Mandel with Hartung–Knapp); the campaign engine's DerSimonian–Laird route agrees in sign and in significance for every scenario.

| Scenario | Pooled OR | Conclusion |
|---|---|---|
| as published | 0.735 [0.397; 1.361] | no significant effect |
| item 1 corrected (Shaker 15/60) | 0.604 [0.325; 1.122] | no significant effect |
| item 2 corrected (Aguilar 6/30 vs 11/30) | 0.592 [0.385; 0.912] | **significant** |
| **both corrected** | **0.484 [0.342; 0.685]** | **significant** |
| both corrected, Aguilar excluded (7 trials) | 0.493 [0.326; 0.744] | **significant** |

**The published conclusion — that current randomised evidence does not demonstrate a mortality benefit — does not survive either correction, and does not survive by any route, including simply removing the disputed trial.** The trial sequential analysis reported alongside the diamond is computed from the uncorrected data and would have to be recomputed; the benchmark does not attempt that here.

---

## F. Verified and correct

Recorded so that the list above is read against its denominator. Six of eight trials agree cell for cell with their sources, each with the quotation on file in `ancora3-camada1.json`: Luis-Silva 2024 (9/19 vs 14/23), Ibarra-Estrada 2023 (15/45 vs 21/46), Kirov 2001 (5/10 vs 7/10, converted correctly from published survivors), Levin 2004 (0/28 vs 6/28), Dong 2025 (9/36 vs 15/36), Memis 2002 (4/15 vs 4/15, tallied from the patient-level table because no per-arm count is printed).

---

*Nothing in this file has been sent to the journal or to the authors. The alert table prepared from it — [`errata-alert-table-ancora3.md`](errata-alert-table-ancora3.md) — is a draft held for the benchmark author's decision.*
