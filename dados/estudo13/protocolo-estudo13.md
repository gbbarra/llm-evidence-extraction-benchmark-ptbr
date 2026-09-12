# EXTRAI — Protocol draft, Study 13: the v3 sheet ("cite what is printed; the program derives")

**Status: DRAFT, NOT REGISTERED, NO RUN.** Written 2026-09-12 from the Study 12 findings, at the author's request, so that the design is on record before it is executed. Registration is the author's act: it fixes a freeze commit and a date at the top of this file, and only then may Phase 1 start. Amendments after registration only as dated sections. General method: [`METHOD.md`](../../METHOD.md).

**Origin (Study 12, `dados/estudo12/`) — corrected 2026-09-12.** The v2 sheet, which makes a verbatim quotation mandatory for every cell, lowered cell agreement on anchor 1 (mean −6.8 of 124 cells, descriptive fields). Its apparent "starvation" of the anchor-2 pools was a grader artifact, not a sheet effect: the models transcribed the confidence interval and its type with a quotation, and the Phase-2 converter stringified the type object before the route read it, so CI-type dispersions were graded as omissions and SE-type ones as wrong-type slips (`dados/estudo12/p2/artefato-v2-tipo.md`: 42 cells, 15 of them correct against the key; the corrected v2 pools regain 5–7 trials). A second defect of the same route — the interval parser dropped Unicode minus signs and could take a repeated value as a bound — was found during the regrade and fixed too. Both are fixed in the grader with regression tests, and the Study 12 record was re-graded on 2026-09-12 (a2 v2 cells 34 · 22 · 16/42 · 30 · 24 · 36; v2 pools with 5–7 trials; H12.3's estimate criterion met on anchor 2 only). What remains true of v2: the anchor-1 cost; three anchor-3 sheets refused by the strict JSON reader because the quotation carried control characters inherited from PDF-derived text; and the models' own wrong-type dispersions, to be recounted after the re-grade. The v3 design below therefore aims at verifiability of the printed inputs (table-row quotations, a type label checked by a net, text hygiene), with the corrector deriving by the key's rules — not at recovering completeness, which the corrected v2 already has.

**What to do before any Study 13 run (in order).** (1) Re-grade Study 12 anchor 2 with the fixed grader (`e12-p2.py`, then `e12-p4.py`; no model call) and replace the affected numbers in the record and the article, stating the correction — **done 2026-09-12**. (2) Re-read the reader's verdicts on the affected cells — **done 2026-09-12** (5 re-issued, 4 new; 89 verdicts, residue 0). (3) Re-derive the v2 baseline used by H13.1–H13.5 from the corrected record — **done 2026-09-12** (the comparator numbers in §6 are now the regraded ones; H13.1's v1 pool sizes did not change); the thresholds themselves are confirmed by the author at registration. (4) Build the instruments — **done 2026-09-12** (§4), to be committed. (5) Register this protocol (freeze commit and date; the harness refuses a real call until then). (6) Run P1-A.

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

## 4. The v3 sheets and their instruments (built 2026-09-12, sealed, NOT run, not yet registered)

Three sheets in `dados/estudo13/prompts/`, sealed by SHA-256 in `dados/estudo13/fichas.sha256` (`scripts/estudo13/e13-sela-fichas.py`); the harness refuses to start if any seal differs.

**Anchor 2 (`a2-extraction-v3.txt`, written by hand).** Same two-arm layout and same `{"value", "where", "quote"}` objects as v2, so the harness's integrity gate, the nets and the Phase-2 unwrapper read it unchanged and the same seven grader cells are compared with v1 and v2. What changes is what is asked: per arm, only **printed** quantities — `n_randomized`, `n_analyzed`, and for HbA1c the baseline, the final (with its `timepoint`) and the change (with its `timepoint`), each as a mean, a dispersion and a `dispersion_type` field whose value is the word the article uses (`SD`, `SE`, `CI95: lower to upper`, `IQR`, `range`, or `NR` when the article does not say). Rules printed on the sheet: (i) copy numbers exactly as printed, sign included; (ii) reading only — never compute, derive or convert (no change from baseline and final, no SD from an interval or a standard error); what is not printed is `NR`; (iii) never guess the type; (iv) a table row counts as a quotation, copied as printed and prefixed with the table's title; (v) multi-arm trials use the groupings the text itself compares, as in v1 and v2 (the anchor-3 sheet keeps its `arms`/`mortality` lists and the corrector reduces, as in Study 12).

**Anchors 1 and 3 (`a1-extraction-v3.txt`, `a3-extraction-v3.txt`).** Derived deterministically from the frozen v2 sheets by `scripts/estudo13/e13-fichas.py`: the v2 text plus two rules — the table-row quotation (rule 8) and never-compute (rule 9: no percentage turned into a count, no sum across arms, no difference between visits; on anchor 3 a printed mortality percentage goes to `deaths_percent` and `deaths` stays `NR`). Fields unchanged, so the v1/v2 denominators (124 and 32 cells) are kept.

**The v3 corrector** (`scripts/estudo13/e13-corrector.py`, built). Unwraps every `{value, where, quote}` object before any rule reads it (the Study 12 defect); applies the key's own functions (`e3-harness`: `dp_de_ic`, `dp_de_se`, `dp_mudanca_r05`) to the printed inputs in the key's priority order — the declared change first, its dispersion converted by the declared type (SD as printed; SE × √n; CI half-width × √n / 1.96, the bounds parsed after normalizing Unicode minus signs and stripping the "CI95" token and taken in ascending order); when no change dispersion is printed, the r = 0.5 imputation from the baseline and final SDs (each converted first if printed as SE); `change = final − baseline` when no change is printed; an IQR, a range or a dispersion without a type label is never used. For each derived cell it records the rule, the inputs and their quotations (the route). Derivations happen after the seal reversal, so the lens sees only printed values (this also removes the "derived through the seal" grader artifact of Study 12). **Build gate** (`--gate`): every derived cell of the anchor-2 key — 12 cells: 6 `dp_de_ic`, 2 `dp_de_se`, 2 `media_de_basal_final`, 2 `dp_imputada_r05` — must be reproduced by the corrector from the inputs the key cites in its `conta` strings; 12 of 12 on 2026-09-12. Anchor 3: `deaths = round(percent × n / 100)` when only the percentage is printed.

**Provenance nets** (`scripts/estudo13/e13-redes.py`, built; warn-only as in every prior study). N9-1 (quotation found in the source) accepts a table row prefixed with its title (the title is stripped before the search); N9-2 (value found in its quotation) normalizes both sides first, so a printed en dash or Unicode minus counts as the sign it is, and is not applied to `dispersion_type` cells, whose word is a label the model assigns; the new net **N13-1** flags a `dispersion_type` label that contradicts the printed form of its dispersion's quotation (`SD`/`SE` declared while the quotation prints an interval; `CI` declared while it prints a lone ± spread), reusing Study 9's recognizers. Self-test: the four expected flags and no other.

**Text hygiene** (`scripts/estudo13/e13-higiene.py`, built). Control characters (U+0001–U+0008, U+000B, U+000C, U+000E–U+001F, U+007F) are replaced by a space **at read time, inside the harness**, so the sealed corpora on disk stay the bytes Study 12 read (the comparators of H13.1–H13.5 need the same texts) and the count removed is written into every output record (`higiene_removidos`). On the current corpora only two anchor-3 primaries carry them (`kirov2001.txt` 127, `levin2004.txt` 18); the script proves that no number changes in any file. The Phase-2 reader for v3 is the tolerant one (`acha_json`), declared primary; the strict reader runs as a sensitivity.

**The harness** (`scripts/estudo13/e13-harness.py`, built). The Study 12 harness — transport, atomic writes, integrity gate, resume, single-instance lock, per-call record with the prompt's SHA — re-pointed to the v3 sheets, an output allowance of 8,000 tokens (as v2), the tree `dados/estudo13/saidas/` and the hygiene above; `--etapa P1-A` plans anchor 2 only, `--etapa P1-B` anchors 1 and 3. It refuses any real call until this file carries a `**Registered YYYY-MM-DD` line; `--seco` prints the plan without calling a model. Dry runs of 2026-09-12: 84 and 264 calls, seals 3 of 3, nothing written. **Tests** (`scripts/estudo13/e13-testa-instrumentos.py`, no model): the gate, the routes on synthetic sheets (CI with en dash, SE, SD, baseline/final, SE converted before r = 0.5, IQR and unlabelled dispersions refused, reversed bounds, change without its SD), the percentage rule, the nets' self-test, the hygiene invariant, the sheets' keys and rules, the seals, the plan sizes and the registration refusal — all pass on 2026-09-12.

## 5. Phases

- **P0 — instruments.** The v3 sheet for the three anchors, the v3 corrector with self-checks against the key's own `conta` strings (every derived key cell must be reproduced from its cited inputs by the corrector — a build gate), the extended nets, the text hygiene, the harness. Built and tested 2026-09-12 (§4); to be committed before registration.
- **P1-A — anchor 2 first.** Six models × 7 trials × 2 replicates under v3: 84 calls (≈ 3–4 h at Study 12's anchor-2 rate). Staged because anchor 2 is where the defect lives; P1-B runs only if H13.1 holds on P1-A.
- **P1-B — anchors 1 and 3.** Six models × 22 trials × 2 replicates: 264 calls (≈ 13 h).
- **P2 — grading**, P3 — pooling, P4 — adjudication under the rite, exactly as in Study 12 (`e12-p2.py`, `e12-p4.py` extended for the v3 fields).
- **P5 — writing.** A dated section in the article's Study-12 results (the v3 arm) or a short follow-up, decided by the author after the record exists.

## 6. Pre-registered hypotheses (thresholds to be frozen at registration)

Comparators are the Study 12 v1 and v2 records of the same models at the same context.

- **H13.1 (completeness recovered).** On anchor 2, for each model, the number of trials pooled under v3 is ≥ the number pooled under v1 in Study 12 (7/7 for `gemma12`, `qwen14`, `qwen27q2`; 5/7 for `llama8`, `qwen35`, `deepseek14`). Failure in any model fails the hypothesis.
- **H13.2 (verifiability kept).** ≥ 95% of the non-NR v3 cells carry a quotation that N9-1 finds in the source text (table rows included), in every model.
- **H13.3 (accuracy preserved).** Anchor-2 cell agreement under v3, on the 49-cell denominator after the corrector's derivation, is no worse than v1 − 2 cells per model; on anchor 1 (P1-B), the mean v3 − v1 delta is no worse than −4 cells of 124 (Study 12's replicate band).
- **H13.4 (the dispersion slip removed).** Wrong-type dispersion cells under v3 total ≤ 5 across the six models on anchor 2 (Study 12 after the 2026-09-12 regrade: 20 adjudicated on anchor 2 — 12 under v1, 8 under v2; the 28 quoted before the regrade included the grader's own artifacts), and N13-1 flags every remaining one.
- **H13.5 (estimates).** The v3 anchor-2 pool, on the Phase-3 lens (mechanical, before adjudication), lands within ±0.1 of the layer-2 −0.24 in ≥ 4 of 6 models. Comparators after the 2026-09-12 regrade: v1 2 of 6, v2 4 of 6 on the Phase-3 lens (adjudicated: 4 and 6 of 6). The threshold ≥ 4 of 6 was set when v2 stood at 3 of 6; at registration the author decides whether to raise it to ≥ 5 of 6, so that v3 is not accepted below the corrected v2.
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
