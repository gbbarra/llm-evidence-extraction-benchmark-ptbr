# EXTRAI — Pre-registered protocol, Study 12: the three-anchor, six-model campaign, with both sheets registered from the start

**Registered 2026-09-08, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). Frozen against commit `32a7894`; the corpora, keys and instruments this protocol names are the versions in that tree, not the working directory.

**Author's directive (2026-09-08, verbatim intent)**: redo the EXTRAI meta-analysis reproductions with all six models running at once, registered from the start and not as an addendum, so the article reads better; add the methylene-blue meta-analysis as a third anchor, begun from the beginning and with the harness in its current state. Hours are not a problem — run it calmly, but build it so that if it is interrupted we can continue from where it stopped.

---

## 1. Question (frozen)

**Does the architecture that measured five local readers on two anchors hold when it is stretched on three axes at once — a sixth reader registered as a peer rather than an extension, a third anchor in a third estimand (the odds ratio), and both extraction sheets run as a declared arm — and, on an anchor whose published cells are wrong in two of eight trials, does source-faithful extraction land the correction that peer review missed?**

The second half is not rhetorical. The two-layer key exists so that a model which reads the source correctly is not penalised for disagreeing with the humans who read it badly. Until this campaign that was a design principle demonstrated on an errata of transcription. Anchor 3 makes it decisive: reproducing the published pooled estimate now **requires reproducing an error**, and this protocol registers, before any run, that failure to reproduce the published diamond is the expected and correct outcome for a model that reads the sources.

## 2. Design principles (frozen)

- **Six readers, peers from the start.** No extension arm, no addendum, no phase that runs for a subset. The cast is fixed in §3 and the same cast runs every anchor and every sheet.
- **Two sheets as a declared arm.** Study 9 asked whether mandatory verbatim quotation preserves accuracy and answered it on four models and two anchors, closing with the statement that four models on two anchors cannot settle it. This campaign runs six on three. Both sheets are registered here; neither is the default.
- **The engines are the frozen ones, plus a declared new half.** `scripts/estudo2/e2-harness.py` is imported and never edited. The odds-ratio half lives in `scripts/estudo12/e12-or.py`, was built and validated **before** this protocol was written, and reuses the frozen continuity rule verbatim.
- **Grading is against layer 2.** Where the review's published cell and the source-verified cell disagree, the source decides. The published cell stays on record as layer 1 and the disagreement is reported as an erratum, never silently resolved.
- **Warn-only.** Detection nets flag; they never substitute a value. Quotation before verdict; flag before fix.
- **Nothing is discovered mid-analysis.** The anchors' own internal inconsistencies are listed in §9 before the runs, so grading has no interpretive freedom. The perturbation reach of anchor 3 is measured in §5 before the runs, so its limits are declared rather than met.
- **Resumable by construction.** A campaign of this length will be interrupted. Interruption must cost at most one model call, must never leave a file that a resume mistakes for finished, and must be reconcilable by an inventory that counts what exists against what this protocol predicts.

## 3. The cast (frozen)

Six local models, one resident at a time, `ollama stop` between them, vendor sampling, `think:false`. Order of the cast is the order of the runs:

| # | Key | Ollama tag | Quantization | Notes |
|---|---|---|---|---|
| 1 | `gemma12` | `gemma4:12b` | Q4_K_M | the campaign's reference reader |
| 2 | `qwen14` | `qwen3:14b` | Q4_K_M | |
| 3 | `llama8` | `llama3.1:8b` | Q4_K_M | |
| 4 | `qwen35` | `qwen3.5:9b` | Q4_K_M | |
| 5 | `deepseek14` | `deepseek-r1:14b` | Q4_K_M | |
| 6 | `qwen27q2` | `smtek/Qwen3.8-27B:Q2_K_XL` | mixed, 3.13 bits/weight measured | "Argos"; enters as a peer, not an extension |

**Frozen decision: the sixth model is a peer of the other five in this campaign.** Study 8 registered it by dated amendment and ran it on phases the five had already finished; here it is registered before the first token and runs every phase the others run. Study 8's §7 excluded "new models beyond the cast"; that clause is superseded for this study and no other.

**Not in the cast**: `smtek/Qwen3.8-27B:Q2_K_XL-16gb`, which shares the weight blob and template of model 6 and differs only in declared `num_ctx` and speculative decoding — both overridden or irrelevant under this protocol's fixed context. It is a deployment question, and it is answered by the memory-footprint note in §8, not by a seventh arm.

**Execution parameters (frozen, and declared including the absences)**: `POST http://localhost:11434/api/generate`; `num_ctx = 24576` for all six models and all three anchors; `think:false`; `stream:false`; output allowance 4,000 tokens for v1 and 8,000 for v2, matching Study 9; `num_gpu = 0` for no model, because all six run on the integrated GPU at this context. **No `seed`, no `temperature`, no `top_p`/`top_k`, no `stop`, no `keep_alive`** — sampling is the vendor default embedded in the model, as in every prior study. The consequence is declared here rather than discovered: **runs are not bit-reproducible, and a resumed run does not reproduce the run it resumes.** Replicate stability is measured, not assumed, and the two replicates per trial are the instrument for it.

**The context change is a variable, and it is controlled.** The published record ran at 16,384; this campaign runs at 24,576, because measurement showed anchor 3's largest primary needs 19,641 tokens with the sheet and the output allowance. Anchors 1 and 2 are therefore re-run in full at the new context, and H12.5 exists to separate the context change from everything else.

## 4. The anchors (frozen)

| | Anchor 1 | Anchor 2 | Anchor 3 |
|---|---|---|---|
| Topic | goal-directed fluid therapy | low-carbohydrate diet in T2DM | methylene blue in adult shock |
| Review | PMC13235771 | PMC13242649 | PMC13302755 |
| Trials in the target analysis | 14 | 7 | **8** |
| Estimand | RR (dichotomous), MD (continuous) | MD | **odds ratio** |
| Published diamond | RR 0.778 [0.567–1.068], I² 76.3% (morbidity); RR 1.021 [0.446–2.337], I² 0.0% (mortality) | MD −0.24 [−0.32; −0.16], I² 6% | OR 0.73 [0.40; 1.36], I² 21.3% |
| Key | two layers, 392 cells / 124 eligible | two layers, 49 cells | two layers, 16 cells, both closed |
| Reading proof | sealed perturbation, 32 pairs | sealed perturbation, 17 pairs | **partial, 4.5 of 8 trials — see §5** |

**Frozen decision: anchor 3's target is the eight trials of the mortality forest plot** — Luis-Silva 2024, Shaker 2025, Ibarra-Estrada 2023, Aguilar 2016, Kirov 2001, Levin 2004, Dong 2025, Memis 2002. The review contains three incompatible descriptions of its own primary analysis (§9, A3-D3 and A3-D4); this one is chosen because it is the only one with cells attached. **Kuri 2025 is in the review's Table 1 and outside this analysis**, is not extracted, and is not part of any denominator.

**Frozen decision: anchor 3's corpus is heterogeneous in format and in language, and that is declared, not hidden.** Five primaries are Europe PMC XML; three are publisher PDFs converted to plain text (Kirov, Memis, Levin); one is a PDF in **Spanish** (Aguilar 2016, open access at Medigraphic and SciELO México, CC BY-NC per the SciELO landing page). No prior anchor had either property. Neither is corrected for, because correcting would mean rewriting sources; both are named as threats in §10 and reported per-trial so that a reader can see whether accuracy tracks format or language.

## 5. The reading proof on anchor 3, and its measured limit

The perturbation doctrine is constitutive of the method, not an accessory: it is what turns "the model did not recite" from a premise into a measurement. Before writing this protocol the frozen operator (`scripts/estudo1/perturbar.py`) was run against the real text of all eight primaries with the real key cells, 200 seeds per value (`scripts/estudo12/medir-perturbabilidade.py`, output committed as `perturbabilidade-ancora3.json`):

| Value type | Perturbable |
|---|---|
| percentages with a decimal place | **9 of 9** |
| integer event counts | **3 of 15** |
| per-arm denominators | 7 of 10 |

**The failure is structural, not a seed accident.** The operator requires the displaced value to be *absent from the text*; a one-digit integer displaced by 5–15% lands on another one-digit integer, which occurs dozens of times in any clinical article. Levin's `0` is impossible by construction, since the rule requires the new value to exceed zero. Anchors 1 and 2 were built on means and standard deviations with decimal places; anchor 3 is built on event counts.

**Frozen decision: anchor 3 is perturbed on the per-arm denominator, with the dependent percentage recomputed for coherence, and the integer event count is left untouched.** Displacing Dong's `n` from 36 to 41 and rewriting the reported percentages from 25.0% and 41.7% to 22.0% and 36.6% keeps the article internally consistent — 9/41 *is* 22.0% — while a recited denominator (36) becomes detectable. The alternative of displacing the percentage alone was rejected because it makes count, denominator and percentage mutually contradictory inside the source, which is a defect a reader could notice and repair, contaminating the measurement it was meant to protect.

**The design was proved feasible before being frozen, not assumed** (`scripts/estudo12/provar-perturbacao-coerente.py`, output committed as `perturbacao-coerente-ancora3.json`). Feasibility is not the denominator's perturbability alone: the displaced denominator **and** every percentage recomputed from it must be absent from the original text, because the unperturbation lens substitutes pairs inside the model's sheet and a colliding value would convert a correct transcription into a wrong one — the defect that failed four correct cells in Study 9. And arms that share a denominator must receive **the same** displacement, since the operator replaces every occurrence of the number rather than a chosen one. Under both constraints the design admits a displacement for **10 of 16 arms**:

| Trial | n | n′ | Arms covered |
|---|---|---|---|
| Shaker 2025 | 30 | 33 | all three: 14/33, 9/33, 6/33 |
| Aguilar 2016 | 30 | 32 | both: 6/32, 11/32 |
| Levin 2004 | 28 | 31 | both: 0/31, 6/31 |
| Dong 2025 | 36 | 41 | both: 9/41, 15/41 |
| Luis-Silva 2024 | 23 | 26 | control only; the MB arm's 19 admits no displacement absent from the text |
| Ibarra-Estrada 2023 | 45, 46 | — | none: n′ is free, but every recomputed percentage collides with the text |
| Kirov 2001 | 10 | — | none |
| Memis 2002 | 15 | — | none |

**Declared consequences, so nothing is found mid-analysis:**

1. The recomputation of a dependent value is **a new capability of the perturbation instrument**, not present in anchors 1 and 2. It is commissioned in §7 and committed with its seal before any run. The operator's displacement rule itself is untouched.
2. **The event counts carry no reading proof in anchor 3.** A model that recites a remembered death count cannot be caught by this instrument. This is stated as a limit of the anchor, and it is the sharpest limit in the campaign, because anchor 3's primaries are from 2001, 2002, 2004 and 2016 — comfortably inside every cast model's training window, unlike the two post-cutoff reviews.
3. **Three trials carry no reading proof at all** — Kirov 2001 and Memis 2002, whose denominators of 10 and 15 are unperturbable for the same structural reason, and Ibarra-Estrada 2023, where the denominator is free but every recomputable percentage collides with the text. Luis-Silva 2024 is covered on the control arm only. The proof therefore covers **four and a half of eight trials**, and every table reporting anchor-3 accuracy carries that denominator alongside the accuracy figure.
4. There is one recitation trap that costs nothing and is registered here: **Aguilar 2016's published cell is wrong in the review** (§9, A3-D2). A model that emits 24/30 has not read the primary, whatever else it has done.

## 6. Phases (run strictly in sequence; each is resumable, and resumption never crosses a phase)

- **P0 — instruments.** Everything in §7 is built, self-checked and committed. No model is called in this phase.
- **P1 — extraction.** Six models × three anchors × two sheets × two replicates over the perturbed corpora. 696 model calls. One resident model at a time; the run order is the cast order of §3, and within a model the anchor order 1 → 2 → 3.
- **P2 — grading.** The sealed unperturbation lens is applied by the grader; cells are compared to layer 2 by the frozen magnitude comparator; unmatched cells go to adjudication, never to an automatic verdict.
- **P3 — arithmetic.** The frozen engine over each model's own cells: RR and MD for anchors 1 and 2, and for anchor 3 **both** the odds ratio (`e12-or.py`) and the risk ratio (frozen `rr`/`pool_dl`), reported side by side.
- **P4 — adjudication and errata.** Divergences between layers, between replicates and between models are adjudicated with the quotation shown before the verdict; every rejected output is recorded with its reason and nothing is deleted.
- **P5 — writing.** One article. No phase is added after results are seen except by dated amendment.

## 7. Instrument work commissioned by this protocol (built and committed BEFORE the phases that use them)

None of these exist today; each is a declared prerequisite of P1, and each is a named gap the Phase-0 survey found in the current code.

1. **`e12-harness.py` — the campaign harness.** Sets `num_ctx = 24576` in its own request body. It must **not** edit `scripts/estudo3/e3-harness.py`, whose `CTX = 16384` is a module-global imported by Studies 3, 4, 7, 8 and 9; changing it would silently redefine the configuration of five registered studies. The transport (`post_json`) is reused; the options are the new harness's own.
2. **The resume gate, per call.** Before each call, the output path is checked for existence *and integrity* (parses as JSON and carries the expected keys). A file that fails integrity is moved aside with its reason, never silently skipped. The current orchestrator's gate is `.exists()` at whole-study granularity, up to sixteen model calls per file; that is not sufficient for a 37-hour run.
3. **Atomic write.** Every output is written to a temporary file and renamed into place. No script in the repository does this today, and the combination of direct writes with an `.exists()` gate is precisely the corruption window the author's instruction forbids.
4. **Per-call record.** Each output records the model key and Ollama tag, anchor, sheet, trial, replicate, `prompt_tokens`, `eval_count`, `done_reason`, wall-clock duration, and the SHA-256 of the prompt actually sent. Today none of this is written for the orchestration stage, and `done_reason` is never read, so truncation has never been detectable after the fact.
5. **The inventory.** A script that counts what exists against what this protocol predicts — 696 calls, enumerated — and prints what is missing, what failed integrity, and what remains. It is the answer to "where did it stop", and it must be runnable at any moment without touching a running job.
6. **The anchor-3 extraction sheets, v1 and v2.** Domain adaptations of the frozen library, structurally parallel to the existing pair. Each data cell asks for the **event count**, the **denominator**, the **reported percentage** and the **outcome timepoint**, as separate fields, for **every arm the trial has**. Three notes on what these sheets deliberately do *not* do:
   - They carry **no polarity instruction**. The sheet asks for deaths, as the anchor-1 sheet always has. It does not warn against reporting survivors, even though the review's Aguilar error was exactly that inversion. Warning would convert a measurement into a hint.
   - They do **not** reduce a multi-arm trial. The model reports every arm; the reduction to two cells is performed by the corrector under the rule frozen in §8. This is a mechanical necessity — the existing multi-arm rule returns free text no calculator can parse — and it is deliberately placed outside the model.
   - They ask for the timepoint as a field rather than fixing it by decree, because on this anchor the timepoint is contested (§9, A3-D5).
7. **The odds-ratio grading path.** No grader, comparator or field map in the repository knows the `or` family; `CAMPOS_FAM` has only `rr` and `md`. The path is written and self-checked before P2.
8. **The perturbation extension** described in §5: coherent recomputation of a dependent percentage when its denominator is displaced. Sealed map committed, SHA-256 recorded in every run log that uses it.

## 8. Pre-registered hypotheses

- **H12.1 (the generalization gate).** The architecture transfers to a third anchor and a third estimand: all six models produce parseable sheets on anchor 3, and each model's pooled odds ratio is digit-consistent with its own extracted cells under the frozen engine — meaning arithmetic never invents, whatever reading did. Failure is any model whose pool disagrees with its own cells.
- **H12.2 (the one that decides — reproducing the published diamond is the wrong answer).** On anchor 3, a model that reads the sources faithfully produces cells that pool to approximately OR 0.48 [0.34; 0.69] under the review's own estimator, **not** to the published 0.73 [0.40; 1.36]. It is registered here, before any run, that landing on the published value would indicate the two erratum cells were reproduced rather than read. The measured quantity is the number of models, of six, whose Aguilar cell is 6/30 (not 24/30) and whose Shaker denominator is 60 (not 30); the honest null is that none manage it and the errata remain a human-only finding.
- **H12.3 (the sheet A/B at the scale Study 9 said it needed).** Study 9 closed by stating that four models on two anchors could not settle whether mandatory quotation preserves accuracy. On six models and three anchors, the per-model v1→v2 cell-accuracy delta is reported with its replicate band; the pre-registered reading is that v2 costs descriptive transcription and buys meta-analytic estimate quality, as the gemma diamond suggested, **or** that the effect does not survive the larger cast, which is a named finding and closes the question in the other direction.
- **H12.4 (the table-cell blind spot, tested where it hurts).** Study 9 measured that the provenance nets are blind to values living in table rows, and anchor 3's mortality cells live almost entirely in table rows. The nets are run as a declared exploratory arm with the false-alarm denominator stated in advance; the pre-registered expectation is that they underperform their anchor-1 and anchor-2 rates, and the finding is the size of that gap.
- **H12.5 (the context control).** Raising `num_ctx` from 16,384 to 24,576 does not move anchors 1 and 2 beyond replicate-level variance — for `gemma12` on anchor 1, within the observed four-cell replicate band of its 103/124 record. If it does move them, the context change is a confounder for every cross-study comparison in this campaign and is reported as such before any anchor-3 result is interpreted.
- **H12.6 (the honest null, stated so it cannot be reframed later).** It is a legitimate and pre-registered outcome that no model reaches usable accuracy on anchor 3, that both sheets perform alike, and that the campaign's contribution is the errata and the instrument rather than a model result.
- *Declared exploratory*: whether accuracy tracks input format (XML against PDF-derived text) or language (the Spanish primary against the seven English ones); the residency footprint of all six models at 24,576, measured once and reported as a hardware note; the number of interruptions the campaign actually takes and what each cost.

## 9. Pre-existing inconsistencies of anchor 3, registered before the runs

Per the freezing contract of `METHOD.md`, the anchor's own contradictions are listed here so grading has no interpretive freedom. Full record and citations: `ancora3-camada1.json`; verification: `verificar-figura3.py` (48 of 48 printed values predicted from 16 read cells) and `verificar-camada2.py` (8 of 8 trials sourced, 6 agree, 2 diverge).

| Id | What | Status | Frozen handling |
|---|---|---|---|
| **A3-D1** | Shaker 2025: the review records 15/30 in the methylene-blue arm. The trial has three arms — placebo 14/30, MB 1 mg/kg 9/30, MB 4 mg/kg 6/30. The review summed the events of both MB arms and kept one arm's denominator. | confirmed against source | Layer 2 is **15/60 against 14/30**: both active arms pooled against the shared control. Registered as the multi-arm reduction rule for this anchor. |
| **A3-D2** | Aguilar 2016: the review records 24/30 and 19/30. The source reports mortality of 20.0% and 36.6% in arms of 30 — 6 and 11 deaths. 30−6 = 24 and 30−11 = 19: the review placed **survivors** in the events column. | confirmed against source | Layer 2 is **6/30 against 11/30**. Layer 1 is retained on record and reported as the campaign's principal erratum. |
| **A3-D3** | The review's §3.5 states the analysis was restricted to the eight septic-shock trials, excluding Levin 2004. The forest plot's eight *include* Levin and *exclude* Kuri 2025. | confirmed within the review | The forest plot governs (§4). The text is reported as an inconsistency, not reconciled. |
| **A3-D4** | The GRADE table reports 8 studies, n = 479. The forest plot totals 213 + 218 = 431. 479 is the sum of Table 1's eight septic trials — a third composition. | confirmed within the review | Neither denominator is used for grading. Reported. |
| **A3-D5** | The analysis is labelled 28–30-day mortality, but Aguilar publishes mortality at ICU discharge and at 21 days and states in text that at 28 days there was no difference, giving no numbers; Table 1 records follow-up windows of 24 to 96 hours across the set. | partially confirmed | **Frozen decision: Aguilar's 21-day figure is used, and its exclusion is run as a pre-registered sensitivity analysis.** Both are already computed: 0.48 [0.34; 0.69] with it, 0.49 [0.33; 0.73] without. The conclusion does not depend on the choice, and that is registered before the run rather than discovered after. |

**Two pooling targets, declared, because they are not the same question.** The review's diamond does not reproduce under DerSimonian-Laird (0.737 [0.449; 1.208]); it reproduces digit-for-digit under Paule-Mandel with the Hartung-Knapp adjustment, which the review does not declare in its methods. The campaign's engine runs DL over each model's cells — that measures the model. PM+HK is computed only by the comparator, against the published diamond — that measures the review. **A model is never graded against 0.73.** Without this separation a model that extracted all sixteen cells correctly would be failed for an estimator it never chose.

**Tolerances (frozen)**: ±0.01 on a pooled odds ratio and on each confidence limit, matching the risk-ratio family; ±0.1 on a mean difference; cell-level comparison by the frozen magnitude comparator at 0.01, with every unmatched cell going to adjudication.

## 10. Compute budget (declared)

Extraction, from the measured rates of the published record — 2.79 min per call on anchor 1, 2.17 on anchor 2, and anchor 1's rate applied to anchor 3, whose articles are of comparable size — plus the 27% v2 overhead measured on the one model with an internal control:

| Anchor | Trials | Calls | v1 | v2 | Total |
|---|---|---|---|---|---|
| 1 — GDFT | 14 | 336 | 469 min | 595 min | 1,064 min |
| 2 — low-carbohydrate diet | 7 | 168 | 182 min | 231 min | 414 min |
| 3 — methylene blue | 8 | 192 | 268 min | 340 min | 608 min |
| **Extraction** | | **696** | | | **2,086 min** |
| Arithmetic and orchestration (estimated) | | | | | 110 min |
| **Total** | | **696** | | | **≈ 37 h** |

This revises the Phase-0 figure of 720 calls and ≈43 h downward, because anchor 3's mortality analysis has eight trials and not nine. **Declared containment, if the cost proves prohibitive**: run both sheets on anchors 2 and 3, where the meta-analytic reading that v2 buys lives, and v1 only on anchor 1, whose descriptive fields are where v2 charges — 528 calls, ≈27 h, with H12.3 answered on two anchors instead of three. Adopting containment is an amendment, dated, and taken before the affected calls run, never after seeing them.

## 11. Outputs

`protocolo-estudo12.md` (this file) · the two anchor-3 sheets in `prompts/`, with seals · the sealed anchor-3 perturbation map and its SHA-256 · the perturbed anchor-3 corpus · per-call outputs under `saidas/<anchor>/<sheet>/<model>/` · the inventory script and its report · grading and adjudication records per anchor · `erratas-ancora-3.md` · the campaign report · one article.

## 12. Out of scope

Any seventh model; any change to the frozen engines, to the anchor-1 and anchor-2 keys, seals, corpora or instruments; any edit to `e3-harness.py`; retroactive edits to the published record; a boundary-aware fix to the unperturbation lens (queued as its own future measurement, and adopting it here would change two variables at once); the readback question of Study 10; adoption of v2 as the library default, which is decided after this study's record and by the author.

---

*Amendments: (none)*

---

### Registration note, 2026-09-08 — one decision in this protocol was not the author's

Three clauses were settled by the drafting assistant rather than by the author, because they arose from measurements taken while this protocol was being written and each blocks P0. They are flagged so the author can overrule any of them before a single model call, which is the only moment at which overruling is free:

1. **§5, the anchor-3 perturbation design** — displacing the denominator with coherent recomputation of the percentage, rather than displacing the percentage alone or declaring the anchor unperturbed. The three options and the reason for the choice are in §5; the measurement behind them is committed.
2. **§4, the target set** — the forest plot's eight trials, among the review's three incompatible descriptions of its own analysis.
3. **§9, A3-D5** — Aguilar's 21-day figure with exclusion as a registered sensitivity analysis, rather than excluding it outright.

Nothing else in this document is new: §§1–3, 6, 8 and 10 follow the six Phase-0 decisions recorded in `decisoes-fase0.md`, all dated 2026-09-08 and all taken by the author.
