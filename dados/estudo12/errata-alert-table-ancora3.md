# Source-confirmed errata of the published methylene-blue meta-analysis — alert table for the journal and authors

**Prepared 2026-09-08** from the benchmark's errata file ([`erratas-ancora-3.md`](erratas-ancora-3.md)), where every entry carries the literal source quotation that decides it. This table contains only items that are **either confirmed against a primary source or verifiable inside the published article itself**; nothing here depends on the benchmark's own judgement of what a trial ought to have reported.

**Reference**: *Methylene blue in adult circulatory shock: a systematic review and meta-analysis of randomized controlled trials.* J Clin Med (PMC13302755).

**Two things the authors should know before reading the table.** First, six of the eight pooled trials reproduce cell for cell against their sources, including the two where the source makes extraction genuinely awkward. Second, the benchmark that found these items is an evaluation harness for language models, and its own adjudicator has published and then withdrawn errors of the same kind on another meta-analysis; the items below are offered as verifiable claims with quotations attached, not as a judgement of the review.

## A. Errors confirmed against the primary sources

| # | Where | Published | The source says (quotation on file) | Impact on conclusions |
|---|---|---|---|---|
| 1 | Figure 3, Shaker 2025 | 15/30 in the methylene-blue arm | Three arms: *"Group A (n = 30) … placebo … Group B (n = 30) … MB 1 mg/kg; and Group C (n = 30) … MB 4 mg/kg"*; *"Mortality rate \| 14 (46.7%) \| 9 (30.0%) \| 6 (20.0%)"*. The published numerator is 9 + 6; the denominator is one arm's 30, not the pooled 60 | **Trial estimate reverses**: OR 1.14 [0.41; 3.15] → 0.38 [0.15; 0.96]. Weight 16.9% |
| 2 | Figure 3, Aguilar 2016 | 24/30 and 19/30 | *"en el grupo A la mortalidad al egreso fue de 20.0% … del grupo C, donde al egreso la mortalidad fue de 36.6%"*, with n = 30 per arm and group A the methylene-blue arm. 20.0% × 30 = 6 and 36.6% × 30 = 11; the published cells are 30 − 6 and 30 − 11, i.e. **the survivors** | **Trial estimate reverses**: OR 2.32 [0.72; 7.41] → 0.43 [0.14; 1.38]. Weight 14.0%. The review's own Table 1 records "↓ Mortality" for this trial, agreeing with the source and disagreeing with Figure 3 |

**Combined effect on the primary outcome.** By the review's own estimator (Paule–Mandel with Hartung–Knapp, which is what reproduces the published diamond digit-for-digit):

| | Pooled OR, 28–30-day mortality |
|---|---|
| as published | 0.73 [0.40; 1.36] — not significant |
| item 1 corrected | 0.60 [0.33; 1.12] — not significant |
| item 2 corrected | 0.59 [0.39; 0.91] — **significant** |
| **both corrected** | **0.48 [0.34; 0.69] — significant** |
| both corrected, Aguilar removed altogether | 0.49 [0.33; 0.74] — **significant** |

**The published conclusion does not survive either correction, by any route, including simply removing the disputed trial.** The trial sequential analysis and the required information size are computed from the uncorrected data and would need recomputation.

## B. Internal inconsistencies, verifiable inside the published article

| # | Where | The inconsistency |
|---|---|---|
| 3 | §3.5 against Figure 3 | The text states the analysis was *"restricted to the eight septic shock trials, excluding Levin et al. (2004)"*. Figure 3's eight rows **include** Levin 2004 and **exclude** Kuri 2025 |
| 4 | Table 2 (GRADE) against Figure 3 | GRADE reports *"8 studies; n = 479"*. Figure 3's arm totals are 213 + 218 = **431**. 479 is the sum of Table 1's eight septic-shock trials — a third composition again |
| 5 | Methods against the printed diamond | The published diamond (OR 0.73 [0.40; 1.36], τ² 0.1334, I² 21.3%) does not reproduce under DerSimonian–Laird (0.737 [0.449; 1.208], τ² 0.1065). It reproduces exactly under **Paule–Mandel with the Hartung–Knapp adjustment** — the default of recent `meta` versions, but not named in the methods. Numbers correct; method undeclared |
| 6 | Outcome label against Aguilar 2016 | The analysis is labelled 28–30-day mortality. Aguilar reports mortality at ICU discharge and at 21 days and states *"a los 28 días no se obtuvieron diferencias en la mortalidad"*, giving no 28-day numbers |

## How the published cells were obtained for checking

The review prints no per-trial cells in its text; they exist only inside Figure 3. They were read from the figure and then verified by reconstruction: the sixteen read cells predict 48 further printed values on the same figure — the eight odds ratios, sixteen confidence limits, eight weights, τ², χ², I², and the diamond with its interval — and all 48 reproduce. Scripts and the full record, including the quotation supporting every layer-2 cell, are available on request.

---

*Draft. Not sent. Held for the benchmark author's decision on whether, and in what form, to contact the journal or the authors.*
