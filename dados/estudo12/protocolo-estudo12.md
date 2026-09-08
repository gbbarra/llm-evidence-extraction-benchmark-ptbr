# EXTRAI — Pre-registered protocol, Study 12: the three-anchor, six-model campaign, with both sheets registered from the start

**Registered 2026-09-08, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). Frozen against commit `PENDING-SEAL`; the corpora, keys and instruments named here are the versions in that tree, not the working directory.

**Author's directive (2026-09-08, verbatim intent)**: redo the EXTRAI meta-analysis reproductions with all six models running at once, registered from the start rather than as an addendum, so the article reads better; add the methylene-blue meta-analysis as a third anchor, begun from the beginning and with the harness in its current state. Hours are not a problem — run it calmly, but build it so that an interruption can be continued from where it stopped.

---

## 1. Question (frozen)

**Does the architecture that measured five local readers on two anchors hold when it is stretched on three axes at once — a sixth reader registered as a peer rather than an extension, a third anchor in a third estimand (the odds ratio), and both extraction sheets run as a declared arm — and, on an anchor whose published cells are wrong in two of eight trials, does source-faithful extraction land the correction that peer review missed?**

The second half is not rhetorical. The two-layer key exists so that a model which reads the source correctly is not penalized for disagreeing with the humans who read it badly. Until this campaign that was a design principle demonstrated on transcription errors. Anchor 3 makes it decisive: reproducing the published pooled estimate now **requires reproducing an error**, and this protocol registers, before any run, that failure to reproduce the published diamond is the expected and correct outcome for a model that reads the sources.

## 2. Design principles (frozen)

- **Six readers, peers from the start.** No extension arm, no addendum, no phase that runs for a subset. The cast is fixed in §3 and runs every anchor and every sheet.
- **Two sheets as a declared arm.** Study 9 asked whether mandatory verbatim quotation preserves accuracy, answered it on four models and two anchors, and closed by stating that four models on two anchors cannot settle it. This campaign runs six on three. Neither sheet is the default.
- **The engines are the frozen ones, plus a declared new half.** `scripts/estudo2/e2-harness.py` is imported and never edited. The odds-ratio half is `scripts/estudo12/e12-or.py`, built and validated before this protocol was written, reusing the frozen continuity rule verbatim.
- **Grading is against layer 2.** Where the review's published cell and the source-verified cell disagree, the source decides. The published cell stays on record as layer 1, and the disagreement is reported as an erratum, never silently resolved.
- **Warn-only.** Detection nets flag; they never substitute a value. Quotation before verdict; flag before fix.
- **Nothing is discovered mid-analysis.** The anchor's own contradictions are listed in §5 before the runs. The reach of the reading proof on anchor 3 is measured in §6 before the runs, so its limits are declared rather than met.
- **Resumable by construction.** A campaign this long will be interrupted. An interruption must cost at most one model call, must never leave a file that a resume mistakes for finished, and must be reconcilable by an inventory that counts what exists against what this protocol predicts.

## 3. The cast (frozen)

Six local models, one resident at a time, `ollama stop` between them, vendor sampling, `think:false`. The cast order is the run order:

| # | Key | Ollama tag | Quantization |
|---|---|---|---|
| 1 | `gemma12` | `gemma4:12b` | Q4_K_M |
| 2 | `qwen14` | `qwen3:14b` | Q4_K_M |
| 3 | `llama8` | `llama3.1:8b` | Q4_K_M |
| 4 | `qwen35` | `qwen3.5:9b` | Q4_K_M |
| 5 | `deepseek14` | `deepseek-r1:14b` | Q4_K_M |
| 6 | `qwen27q2` | `smtek/Qwen3.8-27B:Q2_K_XL` | mixed, 3.13 bits/weight measured |

**Frozen decision: the sixth model is a peer of the other five in this campaign.** Study 8 registered it by dated amendment and ran it on phases the five had already finished; here it is registered before the first token. Study 8's §7 excluded "new models beyond the cast"; that clause is superseded for this study and no other. Its second published tag (`…:Q2_K_XL-16gb`) shares the weight blob and template and differs only in declared `num_ctx` and speculative decoding, both overridden or irrelevant under this protocol; it is a deployment question, answered by the footprint note in §9 rather than by a seventh arm.

**Execution parameters (frozen, including the absences)**: `POST /api/generate` at `localhost:11434`; `num_ctx = 24576` for all six models and all three anchors; `think:false`; `stream:false`; output allowance 4,000 tokens for v1 and 8,000 for v2, as in Study 9. All six models carry `cpu=False` and none receives `num_gpu = 0`; the 27B was measured loading and answering wholly on the integrated GPU at 24,576, and the other five are smaller, but **the footprint of the other five at this context has not been measured** and is a declared exploratory item in §9. **No `seed`, no `temperature`, no `top_p`/`top_k`, no `stop`, no `keep_alive`** — sampling is the vendor default embedded in the model, as in every prior study. The consequence is declared rather than discovered: **runs are not bit-reproducible, and a resumed run does not reproduce the run it resumes.** Replicate stability is the instrument for that, and H12.5 gives it a threshold.

**The context change is a variable, and it is controlled.** The record ran at 16,384. This campaign runs at 24,576, because anchor 3's largest primary needs 14,741 prompt tokens: 19,641 with the sheet and the v1 allowance, leaving 4,935 of headroom, and **23,641 under the v2 allowance of 8,000, leaving 935**. It fits, and the thin margin is stated rather than hidden: measured v2 sheets ran 1,216–1,691 tokens, an order below the allowance, so the ceiling is never approached in practice. Anchors 1 and 2 are re-run in full at the new context, and H12.5 exists to separate this change from everything else.

## 4. The anchors (frozen)

| | Anchor 1 | Anchor 2 | Anchor 3 |
|---|---|---|---|
| Topic | goal-directed fluid therapy | low-carbohydrate diet in T2DM | methylene blue in adult shock |
| Review | PMC13235771 | PMC13242649 | PMC13302755 |
| Trials in the target analysis | 14 | 7 | **8** |
| Estimand | RR, MD | MD | **odds ratio** |
| Published diamond | RR 0.778 [0.567–1.068], I² 76.3%; RR 1.021 [0.446–2.337], I² 0.0% | MD −0.24 [−0.32; −0.16], I² 6% | OR 0.73 [0.40; 1.36], I² 21.3% |
| Graded cells | 124 eligible of 392 | 49 | **32**: the (events, denominator) pair of each of 16 arms |
| Reading proof | sealed perturbation, 32 pairs | sealed perturbation, 17 pairs | **partial, 4.5 of 8 trials — §6** |

**Frozen decision: anchor 3's target is the eight trials of the mortality forest plot** — Luis-Silva 2024, Shaker 2025, Ibarra-Estrada 2023, Aguilar 2016, Kirov 2001, Levin 2004, Dong 2025, Memis 2002. The review gives three incompatible descriptions of its own primary analysis (§5); this one is chosen because it is the only one with cells attached. **Kuri 2025 is in the review's Table 1 and outside this analysis**, is not extracted, and enters no denominator.

**Frozen decision: anchor 3's accuracy denominator is 32 cells** — the event count and the arm denominator for each of the 16 arms. The sheet also collects the reported percentage and the outcome timepoint per arm; those are recorded, carry the reading proof and settle A3-D5, but stay out of the accuracy denominator, because the meta-analysis consumes only the pair.

**Frozen decision: anchor 3's layer 1 carries provenance but no quotation, and it is the first key in the series of which that is true.** The published cells exist only inside a raster forest plot; they were read by vision and then verified by reconstruction — 48 printed values predicted from the 16 read cells (`verificar-figura3.py`). Their provenance is the figure coordinate plus that reconstruction, not a transcribable sentence. Layer 2 carries quotation as always (`verificar-camada2.py`: 8 of 8 trials sourced, 6 agreeing, 2 diverging). Since grading is against layer 2, no verdict in this campaign rests on an unquoted cell.

**Frozen decision: anchor 3's corpus is heterogeneous in format and in language, and that is declared, not hidden.** Of the eight, four are Europe PMC XML, three are publisher PDFs converted to plain text (Kirov, Memis, Levin), and one is a PDF **in Spanish** (Aguilar 2016, open access at Medigraphic and SciELO México, CC BY-NC per the SciELO landing page). Format heterogeneity is not new — anchor 1 already carries six closed primaries as extracted text — but **a non-English primary is new to the series**, and the instruments are in English. Neither is corrected for, since correcting would mean rewriting sources; both are reported per trial and carried as declared exploratory items in §9.

## 5. Anchor 3's own inconsistencies, registered before the runs

Per the freezing contract of `METHOD.md`, the anchor's internal contradictions are listed before any run so that grading has no interpretive freedom. Record and citations: `ancora3-camada1.json`.

| Id | What | Status | Frozen handling |
|---|---|---|---|
| **A3-D1** | Shaker 2025: the review records 15/30 in the methylene-blue arm. The trial has three arms — placebo 14/30, MB 1 mg/kg 9/30, MB 4 mg/kg 6/30. The review summed the events of both active arms and kept one arm's denominator. | confirmed against source | Layer 2 is **15/60 against 14/30**: both active arms pooled against the shared control. This is the multi-arm reduction rule for this anchor. |
| **A3-D2** | Aguilar 2016: the review records 24/30 and 19/30. The source reports mortality of 20.0% and 36.6% in arms of 30 — 6 and 11 deaths. 30−6 = 24 and 30−11 = 19: the review placed **survivors** in the events column. | confirmed against source | Layer 2 is **6/30 against 11/30**. Layer 1 stays on record; this is the campaign's principal erratum. |
| **A3-D3** | The review's §3.5 states the analysis was restricted to the eight septic-shock trials, excluding Levin 2004. The forest plot's eight *include* Levin and *exclude* Kuri 2025. | confirmed within the review | The forest plot governs (§4). The text is reported, not reconciled. |
| **A3-D4** | The GRADE table reports 8 studies, n = 479. The forest plot totals 213 + 218 = 431. 479 is the sum of Table 1's eight septic trials — a third composition. | confirmed within the review | Neither denominator is used for grading. Reported. |
| **A3-D5** | The analysis is labelled 28–30-day mortality, but Aguilar publishes mortality at ICU discharge and at 21 days, stating in text that at 28 days there was no difference and giving no numbers. | partially confirmed | **Frozen decision: Aguilar's 21-day figure is used, and its exclusion runs as a pre-registered sensitivity analysis.** Both are computed by `cenarios-ancora3.py`: with it, PM+HK 0.484 [0.342; 0.685]; without it, seven trials and six degrees of freedom, 0.493 [0.326; 0.744]. The conclusion does not depend on the choice, and that is registered before the run rather than discovered after. |

**Two pooling targets, declared, because they answer different questions.** The published diamond does not reproduce under DerSimonian-Laird (0.737 [0.449; 1.208]); it reproduces digit-for-digit under Paule-Mandel with the Hartung-Knapp adjustment and Student's *t* at *k*−1 degrees of freedom, which the review does not declare in its methods. The campaign's engine runs DL over each model's cells — that measures the model. PM+HK is computed only by the comparator, against the published diamond — that measures the review. **No model is ever graded against 0.73.** Without this separation a model that extracted all sixteen arms correctly would be failed for an estimator it never chose.

**Tolerances (frozen)**: ±0.01 on a pooled odds ratio and on each confidence limit, matching the risk-ratio family; ±0.1 on a mean difference; cell comparison by the frozen magnitude comparator at 0.01, with every unmatched cell going to adjudication rather than to an automatic verdict.

## 6. The reading proof on anchor 3, and its measured limit

The perturbation doctrine is constitutive of the method: it is what turns "the model did not recite" from a premise into a measurement. Before this protocol was written, the frozen operator was run against the real text of all eight primaries with the real key cells, 200 seeds per value (`medir-perturbabilidade.py`):

| Value as the source prints it | Perturbable |
|---|---|
| percentages carrying a decimal place | **9 of 9** |
| numbers printed without a decimal — 12 integer event counts and 3 whole-number percentages | **3 of 15** |
| per-arm denominators | 7 of 10 |

**No integer event count is perturbable, and the failure is structural rather than a seed accident.** The operator requires the displaced value to be absent from the text, and a one- or two-digit integer displaced by 5–15% lands on another small integer that occurs dozens of times in any clinical article. Levin's `0` is impossible by construction, the rule requiring the new value to exceed zero. Anchors 1 and 2 were built on means and standard deviations with decimal places; anchor 3 is built on counts.

**Frozen decision: anchor 3 is perturbed on the per-arm denominator, with the dependent percentage recomputed for coherence, and the integer event count left untouched.** Displacing Dong's `n` from 36 to 41 and rewriting its percentages from 25.0% and 41.7% to 22.0% and 36.6% keeps the article internally consistent — 9/41 *is* 22.0% — while a recited denominator (36) becomes detectable. Displacing the percentage alone was rejected: it makes count, denominator and percentage mutually contradictory inside the source, a defect a reader could notice and repair, contaminating the measurement it was meant to protect.

**The design was proved before being frozen, and the proof rejected two earlier versions of it** (`provar-perturbacao-coerente.py`, `provar-lente-ancora3.py`; outputs committed). Feasibility requires more than a perturbable denominator. Arms sharing a denominator must receive the same displacement, since the operator replaces every occurrence rather than a chosen one. And every recomputed percentage must also be absent from the source, because the unperturbation lens substitutes pairs inside the model's sheet. Under both constraints the design admits a displacement for **10 of the 17 arms**:

| Trial | n | n′ | Arms covered |
|---|---|---|---|
| Shaker 2025 | 30 | 33 | all three: 14/33, 9/33, 6/33 |
| Aguilar 2016 | 30 | 32 | both: 6/32, 11/32 |
| Levin 2004 | 28 | 31 | both: 0/31, 6/31 |
| Dong 2025 | 36 | 41 | both: 9/41, 15/41 |
| Luis-Silva 2024 | 23 | 26 | control only; the active arm's 19 admits no displacement absent from the text |
| Ibarra-Estrada 2023 | 45, 46 | — | none: n′ is free, but every recomputable percentage collides |
| Kirov 2001 | 10 | — | none |
| Memis 2002 | 15 | — | none |

**Frozen decision: anchor 3 is graded through a boundary-aware single-pass lens, and anchors 1 and 2 keep the frozen one untouched.** The frozen lens is a sequence of ordered substring replacements over the serialized sheet (`e6-downstream.py`), which is what failed four correct cells in Study 9 when the pair 31→28 was applied inside `1283.2`. Anchor 3 makes that failure certain rather than possible, because its seal values are two-digit integers: measured over the eight source texts, **the frozen lens commits 42 undue substitutions and a single simultaneous pass with numeric boundaries commits none** (`provar-lente-ancora3.py`). Among the frozen lens's victims is Dong's `41.7`, which is itself a layer-2 value. The new lens is commissioned in §8 and applies to anchor 3 alone, so the comparability of anchors 1 and 2 with the published record is untouched; §12 is narrowed accordingly.

**Declared consequences, so nothing is found mid-analysis:**

1. Coherent recomputation of a dependent value, and the boundary-aware lens, are **new capabilities of the perturbation instrument**, absent from anchors 1 and 2. The operator's displacement rule is untouched, but its *selection* rule is not: anchor 3 selects the values to displace by their role in the key rather than by the operator's own candidate search. Both are commissioned in §8 and sealed before any run.
2. **The event counts carry no reading proof.** A model that recites a remembered death count cannot be caught by this instrument. This is the campaign's sharpest limit, because anchor 3's primaries run from 2001 to 2025 — mostly inside every cast model's training window, unlike the two post-cutoff reviews.
3. **Three trials carry no reading proof at all** — Kirov and Memis, whose denominators of 10 and 15 are unperturbable for the same structural reason, and Ibarra-Estrada, where the denominator is free but every recomputable percentage collides. Luis-Silva is covered on the control arm only. The proof covers **four and a half of eight trials**, and every table reporting anchor-3 accuracy carries that denominator beside the accuracy figure.
4. One recitation trap costs nothing and is registered here: **Aguilar 2016's published cell is wrong in the review** (§5, A3-D2). A model that emits 24/30 has not read the primary, whatever else it has done.

## 7. Phases (run strictly in sequence; each is resumable, and resumption never crosses a phase)

- **P0 — instruments.** Everything in §8 is built, self-checked, sealed and committed. No model is called.
- **P1 — extraction.** Six models × three anchors × two sheets × two replicates over the perturbed corpora: 696 calls, one resident model at a time, cast order, anchors 1 → 2 → 3 within a model.
- **P2 — grading.** The sealed lens is applied to the model's sheet by the grader; the resulting cells are compared to layer 2 by the frozen magnitude comparator; unmatched cells go to adjudication.
- **P3 — arithmetic.** The frozen engine over each model's graded cells: RR and MD for anchors 1 and 2; for anchor 3 both the odds ratio and the risk ratio, side by side.
- **P4 — adjudication and errata.** Divergences between layers, replicates and models are adjudicated with the quotation shown before the verdict; every rejected output is recorded with its reason and nothing is deleted.
- **P5 — writing.** One article. No phase is added after results are seen except by dated amendment.

## 8. Instrument work commissioned by this protocol (built and committed BEFORE the phases that use them)

None exists today; each is a declared prerequisite of P1 or P2.

1. **`e12-harness.py` — the campaign harness.** Sets `num_ctx = 24576` in its own request body. It must **not** edit `scripts/estudo3/e3-harness.py`, whose `CTX = 16384` is a module global on which seven registered studies depend, directly or through `e4-extensao.py`; changing it would silently redefine their configuration. The transport is reused; the options are the new harness's own.
2. **The resume gate, per call.** Before each call the output path is checked for existence *and* integrity — parses as JSON, carries the expected keys, and its recorded `done_reason` is not `length`. A file failing any check is moved aside with its reason, never silently skipped. The current orchestration gate is `.exists()` at whole-study granularity, up to sixteen model calls per file.
3. **Atomic write.** Every output is written to a temporary file and renamed into place. No script in the repository does this today, and direct writes behind an `.exists()` gate are exactly the corruption window the author's instruction forbids.
4. **Per-call record.** Model key and Ollama tag, anchor, sheet, trial, replicate, `prompt_eval_count`, `eval_count`, `done_reason`, wall-clock duration, and the SHA-256 of the prompt sent. The extraction engines already read `done_reason` and the token counts; **the orchestration path discards them**, so truncation has never been detectable after the fact in that stage. This closes the gap for the whole campaign.
5. **The inventory.** A script counting what exists against what this protocol predicts — the 696 calls, enumerated — printing what is missing, what failed integrity and what remains. It answers "where did it stop" and must run at any moment without touching a running job.
6. **The anchor-3 extraction sheets, v1 and v2.** Domain adaptations of the frozen library. Each data cell asks for the **event count**, the **denominator**, the **reported percentage** and the **outcome timepoint**, as separate fields, **for every arm the trial has**. Two properties are deliberate and one is a declared departure:
   - They carry **no polarity instruction**. The sheet asks for deaths, as the anchor-1 sheet always has, and does not warn against reporting survivors even though the review's Aguilar error was exactly that inversion. Warning would convert a measurement into a hint.
   - They do **not** reduce a multi-arm trial. The model reports every arm; the reduction to two cells is done by the corrector under the rule frozen in §5 (A3-D1). This is mechanical necessity — the existing multi-arm rule returns free text no calculator can parse — and it is deliberately outside the model.
   - **They are not structurally parallel to the existing pair, and the departure is declared.** Anchor 1's sheet asks for a single mortality count per arm; anchor 3's asks for four fields per arm, over all arms. The reason is the domain — Aguilar and Memis publish only percentages, Shaker has three arms — but the two added axes, per-arm percentage and enumerated arms, are the same two on which the review's human extractors failed. **A model that lands the errata is therefore helped by the instrument, and any claim that the models found the erratum must be read against this sentence.**
7. **The anchor-3 gradable key.** Layer 1 and layer 2 in the schema the graders consume, with the per-cell verdict, note and citation fields that the anchor-1 and anchor-2 keys carry. `ancora3-camada1.json` is a record, not a gradable key, and the conversion is instrument work.
8. **The odds-ratio grading path.** No grader, comparator or field map in the repository knows the `or` family; `CAMPOS_FAM` has only `rr` and `md`. Written and self-checked before P2.
9. **The perturbation instrument for anchor 3**: role-based selection of the values to displace, coherent recomputation of dependent percentages, and the boundary-aware single-pass lens of §6. Its self-check must fail the build if any sealed value of a trial collides with any other value of that trial's seal, in either direction. Sealed map committed, SHA-256 recorded in every run log that uses it.

## 9. Pre-registered hypotheses

- **H12.1 (the generalization gate).** All six models produce parseable sheets on anchor 3, and each model's pooled odds ratio under the frozen engine is digit-consistent with its own graded cells within ±0.01 on the estimate and on each limit — arithmetic never invents, whatever reading did. Failure is any model whose pool disagrees with its own cells beyond that.
- **H12.2 (the one that decides — reproducing the published diamond is the wrong answer).** Source-faithful cells pool to OR 0.484 under the campaign's engine, and to 0.484 [0.342; 0.685] under the review's own estimator — **not** to the published 0.73 [0.40; 1.36]. **That number is a derived constant of layer 2, committed before this protocol, and not a prediction**; it is stated so that a run landing on the published value is understood as having reproduced the errata rather than read the sources. **The prediction is a count**: of six models, how many produce a graded Aguilar cell of 6/30 rather than 24/30, and how many enumerate Shaker's three arms so that the frozen reduction yields 15/60. Pre-registered readings: **≥1 of 6 on both cells** is the finding that a local reader recovered what peer review missed; **0 of 6** is the honest null, and the errata remain a human-only finding of this campaign.
- **H12.3 (the sheet A/B at the scale Study 9 said it needed).** Two criteria, both fixed here. *Accuracy preserved*: the mean per-model v1→v2 delta on anchor 1's 124-cell denominator is no worse than −4 cells, Study 9's observed replicate band. *Estimate quality bought*: v2's pooled estimate is closer to the layer-2 pool than v1's in at least four of six models on at least two of three anchors. Both met is the Study-9 hypothesis confirmed at scale; neither met is the named finding that the effect does not survive the larger cast, and it closes the question in the other direction.
- **H12.4 (the table-cell blind spot, tested where it hurts).** Anchor 3's mortality cells live almost entirely in table rows, which Study 9 measured as the provenance nets' blind spot. The nets run as a declared exploratory arm with the denominator fixed here: **every graded cell whose layer-2 value is not NR** — 32 for anchor 3, 124 for anchor 1, 42 for anchor 2 — reported per net and per model. The pre-registered expectation is that N9-1 and N9-2 exceed on anchor 3 the false-alarm rates they showed on anchors 1 and 2 (23–44% and 12–39%); the finding is the size of the gap.
- **H12.5 (the context control).** Raising `num_ctx` from 16,384 to 24,576 does not move anchors 1 and 2 beyond replicate-level variance: `gemma12`'s anchor-1 v1 cell agreement stays within 103/124 ± 4 cells, and anchor 2's deterministic route lands within ±0.05 of its −0.27 record. Outside those bands, the context change is a confounder for every cross-study comparison here and is reported as such **before** any anchor-3 result is interpreted.
- **H12.6 (the honest null, bounded so it cannot be reframed).** It is a legitimate and pre-registered outcome that no model reaches usable accuracy on anchor 3 — defined as no model exceeding 50% of the 32 graded cells averaged over its two replicates — that both sheets perform alike by H12.3's two criteria, and that the campaign's contribution is the errata and the instrument rather than a model result.
- *Declared exploratory*: whether accuracy tracks input format (XML against PDF-derived text) or language (the Spanish primary against the seven English ones); the residency footprint of all six models at 24,576, measured once as a hardware note; the number of interruptions the campaign takes and what each costs.

## 10. Compute budget (declared)

Extraction, from the rates measured in the record — 2.79 min per call on anchor 1 and 2.17 on anchor 2 — with the v2 overhead of +27% measured on `granite4.2:8b`, **a model outside this cast and the only one with an internal v1/v2 control**. Anchor 3's rate is bracketed rather than asserted: Phase 0 estimated +35% over anchor 1 from article length, and this table gives both ends.

| Anchor | Trials | Calls | v1 | v2 | Total |
|---|---|---|---|---|---|
| 1 — GDFT | 14 | 336 | 469 min | 595 min | 1,064 min |
| 2 — low-carbohydrate diet | 7 | 168 | 182 min | 231 min | 414 min |
| 3 — methylene blue, at anchor 1's rate | 8 | 192 | 268 min | 340 min | 608 min |
| 3 — methylene blue, at Phase 0's +35% | | | 362 min | 460 min | 822 min |
| **Extraction** | | **696** | | | **2,086–2,300 min** |
| Arithmetic and orchestration (estimated) | | | | | 110 min |
| **Total** | | **696** | | | **≈ 37 to 40 h** |

Phase 0 budgeted 720 calls and ≈43 h. Two things changed: anchor 3's mortality analysis has eight trials rather than nine, which removes 24 calls, and this table brackets anchor 3's rate rather than fixing it at +35%. **Declared containment, if the cost proves prohibitive**: both sheets on anchors 2 and 3, where the meta-analytic reading that v2 buys lives, and v1 only on anchor 1, whose descriptive fields are where v2 charges — 528 calls, ≈27 h, with H12.3 answered on two anchors instead of three. Adopting containment is a dated amendment taken before the affected calls run, never after seeing them.

## 11. Outputs

This protocol · the two anchor-3 sheets in `prompts/`, sealed · the anchor-3 gradable key · the sealed anchor-3 perturbation map and its SHA-256 · the perturbed anchor-3 corpus · per-call outputs under `saidas/<anchor>/<sheet>/<model>/` · the inventory script and its report · grading and adjudication records per anchor · `erratas-ancora-3.md` · the campaign report · one article.

## 12. Out of scope

Any seventh model; any change to the frozen engines, or to anchor 1's and anchor 2's keys, seals, corpora, instruments **and unperturbation lens**, which stays as it is so that their comparability with the published record is preserved — the boundary-aware lens of §6 is built for anchor 3 alone, and no result of anchors 1 or 2 is recomputed with it; any edit to `e3-harness.py`; retroactive edits to the published record; the readback question of Study 10; adoption of v2 as the library default, which is decided after this study's record and by the author.

---

*Amendments: (none)*

---

### Registration note, 2026-09-08 — what in this document is not the author's

The six Phase-0 decisions recorded in `decisoes-fase0.md`, all dated 2026-09-08 and all taken by the author, fix the cast, the two sheets, the odds-ratio engine, the context and the pursuit of the closed primaries. **Everything else here was drafted by the assistant** — §§5 to 9, 11 and 12 in full, including all six hypotheses and their thresholds, and the nine commissioned instruments. Three of those choices arose from measurements taken while this protocol was being written, and are flagged so the author can overrule them before a single model call, the only moment at which overruling is free:

1. **§6, the anchor-3 perturbation design** — displacing the denominator with coherent recomputation, and grading anchor 3 through a boundary-aware lens, rather than displacing the percentage alone or declaring the anchor unperturbed.
2. **§4, the target set** — the forest plot's eight trials, among the review's three incompatible descriptions of its own analysis.
3. **§5, A3-D5** — Aguilar's 21-day figure with exclusion as a registered sensitivity analysis, rather than excluding it outright.

This document was reviewed before registration by five independent lenses, each finding verified by a skeptic instructed to refute it: 77 raised, 34 refuted, 43 confirmed and applied here. The refuted set includes four separate claims that H12.2 registers a target the frozen engine cannot produce; each fell on the ground that the hypothesis names its estimator and §5 defines it.
