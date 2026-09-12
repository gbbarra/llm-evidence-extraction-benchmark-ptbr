# EXTRAI — Protocol draft, Study 13: the v3 sheet ("cite what is printed; the program derives")

**Status: DRAFT, NOT REGISTERED, NO RUN.** Written 2026-09-12 from the Study 12 findings, at the author's request, so that the design is on record before it is executed. Registration is the author's act: it fixes a freeze commit and a date at the top of this file, and only then may Phase 1 start. Amendments after registration only as dated sections. General method: [`METHOD.md`](../../METHOD.md).

**Origin (Study 12, `dados/estudo12/`).** The v2 sheet, which makes a verbatim quotation mandatory for every cell, lowered cell agreement on anchor 1 (mean −6.8 of 124 cells) and starved the anchor-2 pools: the two best readers went from 7 of 7 trials pooled under v1 to 4 of 7 under v2, because they left blank exactly the change SDs that Saslow 2017, Dorans 2022 and Chen 2020 do not print (the trials print a confidence interval or a standard error, from which the key derives the SD). A trial missing any of its six cells drops out of the pool. The largest class of genuine reading slips in Study 12 was the wrong-type dispersion (28 cells: a standard error or an interval half-width written as an SD). On anchor 3, three v2 sheets were refused by the strict JSON reader because the quotation carried control characters inherited from PDF-derived text.

---

## 1. Question (to be frozen at registration)

**Does a sheet that asks the model only for printed quantities — each with its quotation and its type label — and moves every derivation into frozen code recover the completeness of v1 while keeping the verifiability of v2, and does it remove the wrong-type-dispersion slip?**

## 2. Design principles

- **Cite the printed, derive by code.** The model never computes a meta-analytic quantity. It transcribes what the trial prints (means, dispersions, intervals, counts), labels each value's type and timepoint, and quotes the text or the table row it came from. The frozen corrector derives the sextet (change mean, change SD, n per arm) by the key's own rules, and records the route per cell.
- **A table row is a quotation.** The quotation may be the row of a table, prefixed by the table's title, because that is where these values live; the provenance nets accept that form.
- **"Not printed" means NR.** If a quantity is not printed in any form, the model writes NR and nothing else. Inventing or deriving is a protocol violation of the sheet, graded as such.
- **Nothing from Study 12 is recomputed.** Its v1 and v2 records, keys, seals and lens are the comparators, untouched. The same six models, the same context (24,576 tokens), the same corpora and seals.
- **Warn-only; quotation before verdict**, as in every prior study.

## 3. The cast, the anchors, the seals (unchanged from Study 12)

Six models, one resident at a time, cast order: `gemma4:12b`, `qwen3:14b`, `llama3.1:8b`, `qwen3.5:9b`, `deepseek-r1:14b`, `smtek/Qwen3.8-27B:Q2_K_XL` (`qwen27q2`). Execution parameters as in Study 12 §3 (`num_ctx = 24576`, `think:false`, vendor sampling, no seed; output allowance 8,000 tokens for v3, as for v2). Anchors 1–3 as in Study 12 §4; perturbed corpora, seals and lenses as sealed there; grading against layer 2.

## 4. The v3 sheet (instrument to be built and frozen before registration)

Per trial, per arm, the sheet asks for **printed** quantities only, each as `{"value", "type", "timepoint", "where", "quote"}`:

| field | what the model reports | allowed `type` labels |
|---|---|---|
| `n_randomized`, `n_analysed` | both counts, if printed | count |
| `outcome_baseline` | the outcome at baseline: central value and dispersion | mean/SD, mean/SE, median/IQR, mean/CI |
| `outcome_final` | the outcome at the visit the review pooled | same |
| `outcome_change` | the change from baseline, only if printed as such | mean/SD, mean/SE, mean/CI |
| `events` | for dichotomous outcomes: events and denominator per arm (anchors 1 and 3, as in Study 12) | count |

Rules printed on the sheet: (i) copy numbers exactly as printed, sign included; (ii) label the dispersion with the word the trial uses (SD, SE, 95% CI, IQR) — never guess the type; (iii) if a quantity is not printed, write NR — do not compute it; (iv) the `quote` is the sentence or the table row (with the table title) containing the value; (v) every arm the trial has is reported, no reduction of multi-arm trials (the corrector reduces, as in Study 12).

**The v3 corrector** (`scripts/estudo13/e13-corrector.py`, to be built): applies the key's rules to the printed inputs — `sd_from_ci`, `sd_from_se`, `change = final − baseline`, `sd_change_r05(sd_baseline, sd_final)` — in the key's priority order (declared change first; then CI/SE conversion; then the r = 0.5 imputation), produces the sextet per trial, and records for each derived cell the rule, the inputs and their quotations. Derivations happen after the seal reversal, so the lens sees only printed values (this also removes the "derived through the seal" grader artifact of Study 12).

**Provenance nets**: N9-1 (quotation found in the source) and N9-2 (value found in its quotation) extended to accept a table row with its title as a quotation; a new net **N13-1** flags a `type` label inconsistent with the quotation (for example, `SD` when the quotation says "SE" or prints an interval).

**Text hygiene**: the corpus builder strips control characters (U+0001–U+0008, U+000B–U+000C, U+000E–U+001F) from PDF-derived texts before sealing, with the count per file recorded; the JSON reader used for v3 is the tolerant one, declared as primary for this study (the strict reader runs as a sensitivity).

## 5. Phases

- **P0 — instruments.** The v3 sheet for the three anchors, the v3 corrector with self-checks against the key's own `conta` strings (every derived key cell must be reproduced from its cited inputs by the corrector — a build gate), the extended nets, the text hygiene, the inventory. Committed before registration.
- **P1-A — anchor 2 first.** Six models × 7 trials × 2 replicates under v3: 84 calls (≈ 3–4 h at Study 12's anchor-2 rate). Staged because anchor 2 is where the defect lives; P1-B runs only if H13.1 holds on P1-A.
- **P1-B — anchors 1 and 3.** Six models × 22 trials × 2 replicates: 264 calls (≈ 13 h).
- **P2 — grading**, P3 — pooling, P4 — adjudication under the rite, exactly as in Study 12 (`e12-p2.py`, `e12-p4.py` extended for the v3 fields).
- **P5 — writing.** A dated section in the article's Study-12 results (the v3 arm) or a short follow-up, decided by the author after the record exists.

## 6. Pre-registered hypotheses (thresholds to be frozen at registration)

Comparators are the Study 12 v1 and v2 records of the same models at the same context.

- **H13.1 (completeness recovered).** On anchor 2, for each model, the number of trials pooled under v3 is ≥ the number pooled under v1 in Study 12 (7/7 for `gemma12`, `qwen14`, `qwen27q2`; 5/7 for `llama8`, `qwen35`, `deepseek14`). Failure in any model fails the hypothesis.
- **H13.2 (verifiability kept).** ≥ 95% of the non-NR v3 cells carry a quotation that N9-1 finds in the source text (table rows included), in every model.
- **H13.3 (accuracy preserved).** Anchor-2 cell agreement under v3, on the 49-cell denominator after the corrector's derivation, is no worse than v1 − 2 cells per model; on anchor 1 (P1-B), the mean v3 − v1 delta is no worse than −4 cells of 124 (Study 12's replicate band).
- **H13.4 (the dispersion slip removed).** Wrong-type dispersion cells under v3 total ≤ 5 across the six models on anchor 2 (Study 12: 28 across v1 and v2), and N13-1 flags every remaining one.
- **H13.5 (estimates).** The v3 anchor-2 pool lands within ±0.1 of the layer-2 −0.24 in ≥ 4 of 6 models (Study 12 primary: v1 2 of 6, v2 3 of 6).
- **H13.6 (the honest null).** It is a legitimate outcome that v3 recovers completeness (H13.1) but not accuracy or estimates (H13.3, H13.5 fail): the derivation by code then removes omissions without removing reading errors, and the sheet is reported as such, not adopted.
- *Declared exploratory*: the rate of NR under v3 where the trial does print the quantity (omission by over-caution); the residency and per-call time under the longer v3 sheet.

## 7. Compute budget (declared)

P1-A 84 calls ≈ 3–4 h; P1-B 264 calls ≈ 13 h; grading and adjudication ≈ 2 h of machine time. Total ≈ 17–19 h. P1-B is conditional on H13.1.

## 8. Outputs

This protocol (registered, with freeze commit and date) · the three v3 sheets, sealed · the v3 corrector and its build gate · the extended nets · per-call outputs under `dados/estudo13/saidas/<anchor>/v3/<model>/` · P2–P4 records in the Study 12 shape · a dated ledger entry per phase · the article section.

## 9. Out of scope

Any change to Study 12's records, keys, seals, lenses, v1 or v2 sheets; any seventh model; any cloud model in an evaluated pipeline; adopting v3 as the library default before the record exists (the author's decision, after).

---

*Registration: (pending — the author fixes the freeze commit and the date here before any run).*
