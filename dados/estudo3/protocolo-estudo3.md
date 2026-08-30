# EXTRAI — Pre-registered protocol, Study 3: "the pipeline"

**Registered 2026-08-29, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). Design sketched in the [roadmap](../../roadmap.md); the two arm-level decisions below marked *(author's choice)* were made by the author before this registration.

> Language note (repo convention): protocol in English; task prompts in Portuguese (frozen pre-registered instruments — the benchmark scenario is Portuguese instructions over English articles).

## 1. Question

Study 1 measured extraction in isolation (champion: 100% over 156 cells). Study 2 measured arithmetic in isolation (champion: 8/8 + 8/8 CIs under the CALC protocol). Study 3 asks: **does a pipeline of local models — each stage cast by its measured winner — carry a stack of trial reports all the way to a finished forest plot, with no human between stages?** And the new capability under test: **can a second model serve as the quality gate**, verifying another model's extraction sheet against the source and catching errors deliberately planted in it?

## 2. Anchor and corpus

Chosen after a five-round hunt (~320 candidate meta-analyses screened; record in the [roadmap](../../roadmap.md)). A genetics/genomics angle was explored at the author's request and found unviable: pharmacogenomics RCT primaries live behind paywalls (0–33% OA in every candidate probed), gene-therapy meta-analyses pool single-arm trials (no comparator), and diagnostic-yield meta-analyses pool cohorts, not RCTs.

**Anchor**: *Effect of Low-Carbohydrate Diets on Glycemic Control in Type 2 Diabetes Mellitus* (PMC13242649, Cureus, 2026-06, CC BY 4.0; DOI 10.7759/cureus.108479). Seven RCTs, 562 participants, one outcome: HbA1c change (%) vs control diet, mean difference by inverse variance, random effects. Published diamond: **MD −0.24 [−0.32, −0.16], I² = 6%, Tau² = 0.00**.

- The per-study table (mean/SD/n both arms × 7 trials) exists only in the forest-plot figure; it was transcribed by Claude (assistant) into [`ma-lowcarb-meta.json`](../../corpus/estudo3/ma/ma-lowcarb-meta.json) and **mechanically validated before this registration**: all 7 per-study MDs and 95% CIs reproduce exactly (±0.01) under the Study-2 functions; the IV pooled MD reproduces exactly (−0.24) with CI bounds 0.01 inside the published ones — consistent with 2-decimal input rounding (tolerance policy in §8).
- **Corpus**: 5/7 primaries carry CC BY licenses (XMLs versioned in `corpus/estudo3/primarios/`). Two are closed-stratum (local only, never versioned): Saslow 2023 (DOI 10.1370/afm.2968, Annals of Family Medicine; legally obtained by the author) and Thomsen 2022 (DOI 10.1007/s00125-021-05628-8, Diabetologia; full text available via the PMC COVID-19 Open Access Subset, whose re-use grant is tied to the ended WHO pandemic declaration — treated conservatively as non-redistributable). Per-file license record in `primarios.json`.
- **Contamination stance**: the anchor is post-cutoff (2026-06); the primaries (2016–2023) predate the models' cutoffs. Defense is the perturbation operator (§5): every load-bearing number in the texts the models read is displaced, so a model reciting a remembered published value scores as a source mismatch — memory becomes detectable, not helpful. (Author's design note: the models are unlikely to remember trial-level numbers at all; the perturbation makes this an observable rather than an assumption.)

## 3. Design: five stages, two lanes

Stages are cast by the **measured winners** of Studies 1–2 (attribution: who does what is fixed here, before any run):

| Stage | Task | Model (why) |
|---|---|---|
| **E — extract** | Per-trial extraction sheet (~14 fields: identity, design, country, duration, arm definitions, n randomized/analyzed per arm, HbA1c change mean/SD/n per arm, unit) from the **perturbed** full text | gemma4:12b (Study 1: 100% on 156 cells, fastest) |
| **A — audit** | Receives the perturbed text + an extraction sheet; must verify **every field** against the text and emit per-field verdicts: `confirma` / `corrige: <value>` / `nao-encontrado` | qwen3.8:27b (Study 2 champion; different family from Stage E = independent eyes) |
| **C — arithmetic** | Per-study MD + 95% CI + pooled DL + I², via the CALC text protocol with **forced closure** | qwen3.8:27b (Study 2: 8/8 + 8/8) |
| **S — synthesis** | 250–400-word evidence summary **with the pooled numbers in its context** (Study-1 T3b lesson) | gemma4:26b (Study 1's strongest long-form profile) |
| **F — forest plot** | Deterministic matplotlib render of Stage C's numbers. **No model.** Fidelity is judged on the numbers, not the pixels | script |

**Two lanes end-to-end** (the seeded-errors arm is the author's choice, locked before registration):

- **Lane L (clean)**: E → A (E's real sheets) → C → S → F.
- **Lane S (seeded)**: E → A (same sheets with k planted errors, §4) → C → S → F.

Stage A's output sheet (auditor-corrected) is what flows downstream in both lanes, so an uncaught seed **propagates** — the pipeline measures not just each stage but the cost of a missed catch on the final diamond.

Replicates: Stage E ×2 (second measures stability; first parseable proceeds), Stages A/C/S ×1 per lane. Estimated ~30 runs total.

## 4. Seeded errors (Lane S)

**k = 8 seeds** over the 7 sheets: at most 2 per sheet, and **at least 2 sheets left untouched** (specificity controls — the auditor is never told whether or how many errors exist). Four classes, 2 each, chosen to span semantic distance:

| Class | Example | Tests |
|---|---|---|
| `troca-de-braco` | experimental and control means swapped for one quantity | semantic reading (direction) |
| `digito` | one digit altered (0.44 → 0.64) | character-level verification |
| `n-trocado` | digit transposition in a sample size (75 → 57) | numeric attention |
| `sinal` | sign flipped (−0.35 → 0.35) | direction sense |

The seed list is generated and **sealed before any run** (`dados/estudo3/sementes-auditoria.json`, gitignored like the perturbation files; its SHA-256 is printed into the run log at execution time and the file is published with the grading).

**Measures**: sensitivity (seeds caught), false-alarm rate (clean fields wrongly "corrected"), correction accuracy (does `corrige` land on the text's true value?), and **propagation** (Δ on the pooled MD per uncaught seed).

## 5. Perturbation (proof of reading)

The Study-1 operator (semantic anchors ±120 chars, distinctiveness tiers, manual curation, leak verification) applied to the 7 primary texts; seals gitignored until grading is published. Extraction is scored against the **perturbed** values: matching the perturbed text proves reading; matching the published value instead is scored as recitation (`recitou`).

## 6. Frozen configurations

Ollama `/api/generate`; ctx 16384 (Stage S: 24576 if the prompt exceeds ~15k tokens — Study-1 T3b lesson); `think: false` everywhere (Stage C outsources arithmetic to CALC, not to reasoning); temperature at model default; `num_gpu: 0` for the CPU-assigned models; queue order fastest-first; resume-safe queues; first-parseable-replicate rule.

**CALC harness extension (declared before runs)**: Study 2's `pool_dl` covers dichotomous quadruples only; Study 3 adds `pool_dl_md` (DerSimonian-Laird over continuous sextuples) to the function table. It is validated against the anchor's published diamond before the queue starts, exactly as Study 2's functions were validated against its anchor (validation output kept in the run log).

**Forced closure (Stage C)**: if a run makes CALC calls but emits no final JSON, the harness appends the calls-and-results transcript and reprompts — *"emita agora o JSON final"* — up to 3 times before scoring a closure failure. This is the harness fix motivated by Study 2's finding 2 (all arm-B failures were workflow, not arithmetic).

## 7. Prompts

Portuguese, frozen before the queue starts, in `dados/estudo3/prompts/` (e3-extracao.txt, e3-auditoria.txt, e3-calc.txt, e3-sintese.txt). The audit prompt instructs field-by-field verification against the text and forbids assuming the sheet is right or wrong a priori.

## 8. Scoring (mechanical core + adjudication rite)

- **Numeric fields**: exact vs the perturbed source (tolerance ±0.01 for MD/CI at 2 decimals; ±0.5 pp for I²). Text fields: Study-1 cell labels with the adjudication rite (verify against source before deducting; public rule-and-verdict record).
- **Anchor comparison** (Stage C vs the published diamond): tolerance ±0.01 per bound **plus** a documented rounding allowance — the anchor's own inputs are 2-decimal rounded, so divergences ≤0.02 per CI bound are recorded as rounding-consistent; only >0.02 is flagged as a divergence for adjudication.
- **End-to-end fidelity**: |pipeline pooled MD − mechanical truth recomputed over the pipeline's own audited inputs| (lane L and lane S separately), and the same against the anchor's published diamond.
- **Attribution**: every report states what the local models did, what the harness did, and what Claude (assistant) did — standing rule.

## 9. Pre-registered hypotheses

- **H3.1 (extraction holds at pipeline scale)**: Stage E ≥95% cell accuracy (Study 1 measured 100%).
- **H3.2 (the audit is real)**: sensitivity ≥75% on seeds AND false-alarm rate ≤10% on clean fields; directional: `troca-de-braco`/`sinal` (semantic) caught more often than `digito`/`n-trocado` (character-level).
- **H3.3 (closure is a harness property)**: with forced closure, 100% of Stage-C runs emit a final JSON (Study 2 without it: 2 of 4 families failed closure).
- **H3.4 (end-to-end fidelity)**: lane L's pooled MD within ±0.02 of the mechanical truth over its own inputs; the full pipeline reproduces the anchor's diamond within the rounding allowance.
- **H3.5 (propagation is weight-proportional)**: an uncaught seed's Δ on the pooled MD scales with the study's IV weight (a seed in Dorans, 53.6% weight, moves the diamond an order of magnitude more than one in Chen, 2.4%).
- **H3.6 (anchor audit, formalized)**: the pre-registration validation stands as the anchor's arithmetic audit — 7/7 per-study values exact; pooled bounds within rounding; any divergence beyond §8's allowance found during the study becomes an erratum candidate.
- **H3.7 (synthesis with numbers in hand)**: Stage S contains zero orphan numbers and states the direction, magnitude and significance of the pooled effect correctly in both lanes — including any distortion inherited from lane S's uncaught seeds (the interesting failure mode).

## 10. Out of scope

Screening/PRISMA reproduction (author's choice: not in this study); risk-of-bias stage (measured in Study 1); subgroup analysis and meta-regression (the anchor has none); native tool calling; proportion pooling; GRADE.

---

## Amendment 1 (2026-08-29, after source reconnaissance, before any prompt was frozen or any run made)

The cell-by-cell verification of the anchor's forest inputs against the 7 primary texts (`scripts/estudo3/verify-source.py` + manual digs; two-layer key in [`gabarito-fonte.json`](gabarito-fonte.json), **42/42 cells mechanically validated** against the published forest) changed four pre-run decisions:

1. **Corpus builder fix**: some journals (Nature family — Goday) ship tables in `<floats-group>` outside `<body>`; the extractor now appends those table-wraps (Study-1 echo: this is where Sujatha's "table 4 out of input" lived). Without the fix, Goday's primary-endpoint table was absent from the model input.
2. **The MA's SD column is mostly derived, not extracted**: of 14 per-arm dispersions, only Thomsen's 2 (and Wang's 2) are literal change-SDs; 6 come from 95% CIs (SD = half-width/1.96×√n: Saslow 2017, Dorans, Chen), 2 from SEs (×√n: Saslow 2023), and 2 from Cochrane's r=0.5 imputation over baseline/final SDs (Goday — whose change means are themselves baseline→final differences). Saslow 2023 is a 2×2 factorial whose "arms" are diet margins (n=45/49 nowhere literal). **Stage E's sheet therefore extracts what the text states** — per arm: label, n randomized (total and per arm if stated), n analyzed, HbA1c change mean *as reported* (sign as printed), dispersion value + **dispersion type** (SD | SE | CI bounds), and baseline/final mean (SD) when the change is not reported — and **Stage C owns the derivations**, with three new CALC functions: `dp_de_ic(lo, hi, n)`, `dp_de_se(se, n)`, `dp_mudanca_r05(dp1, dp2)`, alongside `pool_dl_md`. All four are validated against the anchor's forest before the queue (the 42/42 validation above stands as the record).
3. **Perturbation targets are the source-side numbers** (table/prose values the sheet extracts), never the forest-side derived values; multi-occurrence facts are perturbed at every occurrence within their semantic anchors (E1 operator), and known numeric collisions found in the reconnaissance are excluded (e.g., Dorans's 0.31 doubles as a baseline SD; Thomsen's 0.83 doubles as a p-value; Saslow 2023's 0.07 SE repeats across rows).
4. **Wang reports the drop as a positive "MD"** (0.54/0.28) that the MA sign-flips; the sheet instructs "sign as printed in the source" and the key records the convention, so neither reading is penalized mechanically.

## Amendment 2 (2026-08-29, after Stage E completed and was graded; before any audit-lane grading)

Grading the 14 extraction sheets against the source under the rite ("verify before deducting") exposed **three instrument gaps and four missed literal routes** — all fixes are to the *ruler* (grading key), never to the frozen corpus or prompts, and are recorded before Stage A's lanes are graded:

1. **Number words survive the perturbation operator.** The perturbation replaces digit strings; three trials also state the same facts in words: Thomsen's total ("*Seventy-two adults (CD 36, CRHP 36…)*" — digits 72→63 were replaced, the word form survived), Wang's total ("*Fifty-six T2DM participants*", digits 56→49), Chen's total ("*Ninety-two patients*", never perturbed). The affected cells (2) are graded **symmetrically** (both the perturbed and the surviving-word value accepted; no recitation attributable) — the E1 Amendment-3 treatment. Instrument note for future studies: extend the operator to number words.
2. **Totals with visible addends cannot prove recitation.** Wang's 28+28 and Thomsen's 36+36 remain in the text, so a model can *derive* the original total; those cells are excluded from the reading-proof count.
3. **Twin analysis tables.** Wang reports the HbA1c change **twice**: the row the MA used (0.54±1.12, n=28/28 population) and a per-protocol twin (0.63±1.18 / 0.31±0.70, n=24/25) that also appears in the abstract. The extractor took the twin — literal, defensible; the key now accepts both routes (the divergence's arithmetic cost, if any, is measured downstream).
4. **Missed literal routes added to the key**: Saslow 2017's control completers-with-data ("*0% (0/8) in the control group*" → 8), Dorans's 6-month analyzed columns ("*(n = 73) … (n = 69)*"), Thomsen's randomized arms ("*CD 36, CRHP 36*").

**Stage-E result under the amended key** (public adjudications in [`adjudicacoes-e3.json`](adjudicacoes-e3.json)): replicate 1 = **99/101 cells (98%)**, 2 wrong (one root cause: Chen's final-timepoint SDs paired to the change mean), 0 omissions, 0 attributable recitations; replicate 2 **identical cell-for-cell** (stability 100%). H3.1 (≥95%) is met; formal verdicts wait for the full pipeline.

## Amendment 3 (2026-08-30, registered before any run of the arm; the baseline pipeline was complete and graded)

**Exploratory arm: the all-gemma cast** (author's question: can the whole pipeline run on the extraction champion alone?). Cast: stages A, C and S all performed by **gemma4:12b** (integrated GPU); Stage E is **reused verbatim** from the baseline (the extractor is gemma4:12b in both casts), so the arm isolates the audit/arithmetic/synthesis cast with **identical inputs and identical sealed seeds**. Frozen and unchanged: prompts, context 16384, the 24-call CALC cap (exhausting it is a measured outcome, not a reason to widen), corpus, perturbation and seed seals, auto-application of audit corrections (the flags-not-fixes redesign belongs to a future hardened-pipeline study, not to this arm).

**Harness v2** (three changes, committed before the run):
1. **Cast/namespace parameterization** (`E3_ELENCO` env var; outputs to `saidas-allgemma/`) so alternative arms can never overwrite the baseline record.
2. **Closure net extended to the call-as-data mode**: a final JSON containing `CALC:` strings counts as not-closed and triggers a fixed reprompt ("write the CALC calls OUTSIDE the JSON…", up to the same 3 tries, calls executed if emitted). Mechanical trigger, zero content hints; **provably inert on the baseline cast** (the qwen closed clean and would never meet the trigger).
3. **Pool-input echo, log-only**: the raw per-study `md()` call arguments and the `pool_dl_md` rows are recorded in the run output for mechanical comparison at grading (measures the Study-3 finding-5 discrepancy; no intervention).

**Directional expectations (exploratory, not formal hypotheses)**: audit sensitivity below the baseline's 90% with the correlated-blindness question open (same-family auditor may confirm same-family misreadings); CALC exactness near Study 2's 6/8 with more input-assembly slips; wall-clock several-fold faster (every stage on the integrated GPU).

## Amendment 4 (2026-08-30, registered before the run; the all-gemma arm was complete and graded)

**Exploratory arm: the mixed integrated-GPU cast** (author's question: does gemma+qwen on the iGPU yield the deployment sweet spot?). Cast: Stage E reused verbatim (gemma4:12b, as in every arm); **A and C = qwen3:14b** (cross-family audit independence — the structural ingredient whose absence sank the all-gemma arm — plus the family's measured arithmetic vocation: 7/8 points + 7/8 CIs in Study 2's arm B, second only to the 27B); **S = gemma4:12b**. Everything else frozen exactly as in Amendment 3, **including harness v2's known mixed-round gap** (a final JSON emitted alongside calls is accepted before the calls execute): the gap stays measured-not-fixed so the three casts are comparable under identical rules; the fix belongs to the hardened-pipeline study.

**Directional expectations (exploratory)**: extraction identical (reused); CALC near 7/8 with the Study-2 pool risk (qwen3:14b answered pooling by head there — whether the pipeline's prompt structure tames it, as it tamed the 27B, is the measurement); audit sensitivity unknown (the experiment; the model's Study-1 profile was omission-prone, so a rubber-stamp tendency is plausible), false alarms low; wall-clock near the all-gemma arm's ~1 hour.

## Amendment 5 (2026-08-30, registered before the run; prompted by the author's challenge "the committee has not been tested — what would a committee even be?")

**The committee as a mechanism, not a retrospective union.** The three casts' lane-S audits are independent by construction (identical input sheets, identical sealed seeds, no communication), so their verdicts can legitimately be **combined mechanically after the fact** — but a committee is a combination *rule*, and the retrospective table shows the trade-off space (seeds/false alarms over the same runs): 27B alone 9/10 / 5.9%; 14B alone 7/10 / 9.4%; **27B∪14B union 10/10 / 15.3%** (a detection ceiling above the 10% FA bound); majority-of-3 7/10 / 3.5%; AND-intersection 6/10 / 0%.

This arm tests two pre-registered combination rules end to end, with **no new audit runs** (the members' verdicts are the already-graded ones):

- **Rule OR-27B**: a field flagged by the 27B or the 14B is corrected; on value conflict, the 27B's correction applies (measured-champion prior).
- **Rule MAJ-3**: a field flagged by ≥2 of the 3 auditors is corrected; the value is the one two members agree on, else the 27B's.

The committee-audited sheets are built mechanically from the shared lane-S inputs, then the **baseline calculator (qwen3.8:27b) and synthesist (gemma4:26b) run once per rule** under the frozen v2 harness rules — 4 model runs total. Metrics: committee-sheet cell accuracy vs the ruler; seeds corrected/surviving; pooled MD vs mechanical truth over the same sheets; comparison against the single-gate lane-S results. Declared limitation: corrections still **auto-apply** in this arm (like-for-like with the single gates); the union+re-verification composition that the false-alarm arithmetic demands remains the hardened-pipeline study's subject.

## Amendment 6 (2026-08-30, registered before any run; question ledger in [`agenda-bracos.md`](agenda-bracos.md))

**Harness v3 and the calculator championship.** The author's question — *who is the best tool calculator, fairly compared?* — cannot be answered under the v2 loop, whose round order discards calls written alongside a final JSON (the joint where both small casts died). **Harness v3** ([`calc-v3.py`](../../scripts/estudo3/calc-v3.py), a separate module; the frozen v1/v2 harness is untouched) adds four mechanical nets: (1) *mixed-round fix* — pending calls execute before any final JSON is accepted (an answer only wins in a round that wrote no new calls); (2) *tool-avoidance net* — a zero-calls final answer gets one fixed reprompt to use the calculator; (3) *pool reconciliation* — pool rows not matching the model's own `md()` calls get one fixed reprompt to reconcile (finding 5 as a net); (4) the v2 nets (forced closure; call-as-data) are kept. Philosophy shift, declared: v1/v2 measured *spontaneous* tool discipline (answer: only the 27B has it); v3 measures *scaffolded* discipline — the minimum harness under which small local models close the loop.

**Championship design**: the four veterans × the two baseline lanes (L and S audited sheets — identical inputs for every model), calculator stage only, under v3; 8 runs. Metrics: executed calls, nets triggered, per-study MD/CI exactness vs the mechanical truth over the same sheets, pooled MD, and closure. Directional expectations: the 27B stays first and needs no nets; the 14B approaches it once the mixed-round joint is fixed; the gemma family closes under the nets but with more input-assembly slips; the tool-avoidance net converts by-head modes into tool modes at unknown quality — which is precisely the measurement.

## Amendment 7 (2026-08-30, registered before the run)

**gemma4:26b as auditor** — the last empty cell of the 4-veteran audit matrix (author's request). Cast `aud26` runs the audit stage only, over the same shared sheets and sealed seeds (outputs to `saidas-aud26/`); everything frozen as in the other audit arms. Expectations (exploratory): the MoE's audit personality is unmeasured — its Study-1 profile (99% extraction, disciplined) suggests a verifier; its Study-2 tool record is irrelevant here (the audit is single-shot JSON, no tool loop, and its baseline Study-3 synthesis showed clean long-form emission). After grading, the committee-rule table is recomputed with four members. *(Status note, 2026-08-30: paused before running, together with the CPU half of the Amendment-6 championship, by the author's reorganization of the follow-up work around a single question — see the [question ledger](agenda-bracos.md). Both return later only as reference points.)*

## Amendment 8 (2026-08-30, registered before the run; validated by the author)

**H2 — the harness-driven pipeline ("esteira dirigida").** Paper 2's single question: *can local models that fit on the integrated GPU (≤14B) reach the expected meta-analytic value, if the harness is fixed?* H0 (spontaneous, v2) and H1 (flow nets, v3) are measured: the nets repair every workflow mode, and the small models still fail on **content** — argument assembly drops signs and maps fields to the wrong slots. H2 inverts the division of labor:

- **The harness owns everything deterministic**: it reads the extraction-sheet fields directly, selects the dispersion conversion from the sheet's declared type (SD as-is; SE→SD; CI-bounds→SD by the last-two-numbers rule; baseline/final→Cochrane r=0.5 change-SD), computes every per-study MD and 95% CI, assembles and executes the pool — with the same validated functions the graders use. The model writes no calls and orchestrates nothing.
- **The model is consulted only at judgment points** — mechanically detected ambiguities, one narrow question each, answered from the sheet excerpt shown: on these sheets the sole trigger is the **as-reported positive change** (Wang prints the HbA1c *drop* as a positive "MD"), yielding two sign questions (one per arm). NR-fields and factorial-margin questions are defined as triggers but do not fire on these sheets (the factorial's margin normalization was an audit-layer behavior; the sheet-scoped pipeline uses the sheet's own cells, matching the mechanical-truth reference).
- **Inputs**: the raw Stage-E sheets (gemma4:12b, replicate 1, first-parseable) — a pure iGPU provenance chain; no audit stage and **no seeded errors** (the seeds' question is answered; see the ledger's decision record). Corpus perturbation stands (contamination defense).
- **Arms**: three diamonds — (i) *default rules, no model* (signs taken as printed: quantifies what the judgments are worth); (ii) *gemma4:12b as judge*; (iii) *qwen3:14b as judge*. Reference = the mechanical truth over the same sheets under the graders' documented resolutions.
- **Pre-registered prediction**: both models answer the sign judgments correctly and their diamonds match the mechanical truth **digit for digit**; the default-rules diamond is visibly distorted — locating the small models' entire remaining contribution (and sufficiency) at reading and judgment, with arithmetic and flow in code.
