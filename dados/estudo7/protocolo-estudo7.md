# EXTRAI — Pre-registered protocol, Study 7: "the side-by-side, in the open" (clean texts, both anchors)

**Registered 2026-08-31, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). Author's directive (ledger, 2026-08-31): the natural-conditions head-to-head — the anchor authors' extraction, the local model's extraction, and the deterministic recomputation — side by side on **clean, unperturbed texts**, for both anchor meta-analyses, as Paper 5's record.

## 1. Question (frozen)

**In natural conditions — original texts, no perturbation — how do the three extraction chains compare, cell by cell and effect by effect: the human sheet the anchor authors published, the local reader's fresh sheet (two replicates), and the deterministic recomputation of every effect and pool? And does the erratum-aware comparison make the anchors' documented errata directly visible in the three-way table — the human column disagreeing with the source exactly where the errata live, the model column siding with the source?**

## 2. Scoping declaration (the design's honesty clause)

**This study makes no reading-proof claim.** On clean texts, agreement with the published values cannot distinguish reading from training-data recall — the anchors and most primaries are plausibly in the model's training data. The reading proof is the perturbed record of Studies 1–6 (zero attributable recitations; four sealed lenses on the published values), which this study cites as established. Study 7's claims are confined to: replicate reliability in natural conditions, the *structure* of agreement and disagreement across the three columns, and the recomputation of the published pools by validated code. This scoping is stated in the article's design section, verbatim in spirit.

## 3. Materials (all existing, frozen at registration)

- **Anchor 1 (GDFT, MA-1)**: the goal-directed fluid therapy meta-analysis (PMC13235771) and its 14 primary RCTs — original texts: 8 open (`corpus/primarios-texto/`) + 6 closed (`corpus/fechados-texto/`, local-only, never redistributed; scripts rebuild from legally obtained copies). Human column: the anchor's published tables, structured in `dados/estudo1/gabarito-ma.json`. Grading ruler: the two-layer source-verified key `dados/estudo1/gabarito-oficial.json` **as corrected 2026-08-31** (errata #10 and #17 applied to its `valor_fonte` layer — this study grades under the corrected key). Public errata file: 17 confirmed/withdrawn entries plus pending items.
- **Anchor 2 (low-carbohydrate, MA-2)**: the HbA1c meta-analysis and its 7 primary RCTs — original texts: `corpus/estudo3/primarios-texto/` (REF9 and REF12 local-only, same closed-stratum rule). Human column: the anchor's published forest cells, structured in `corpus/estudo3/ma/ma-lowcarb-meta.json`. Grading ruler: the two-layer key `dados/estudo3/gabarito-fonte.json`.
- **Instruments — the first study frozen from the English library** (`dados/instruments-en/`, working-language directive of 2026-08-31): the MA-1 sheet `t1-extraction.txt` and the MA-2 sheet `e3-extraction.txt`, copied verbatim into `dados/estudo7/prompts/` at registration. **Declared design change**: Studies 1–6 ran Portuguese instruments; no cross-study comparability is claimed across the language change (the instruction-language ablation named in Paper 1 remains future work).
- **Reader**: `gemma4:12b`, pinned build (digest 4eb23ef187e2, `MODELS.md`), reasoning off, context 16,384, two replicates per trial.
- **Engine**: the validated function set only — dichotomous `rr`/`ic95_rr`/`pool_rr_mh`/`pool_dl` (Study 2) and continuous `md`/`ic95_md`/conversions/`pool_dl_md` (Studies 3–4). **No model touches a number downstream of its sheet.**

## 4. Design

1. **The authors' trail (article section, no instrument)**: each anchor's published search and selection path, summarized with quotes from its methods — descriptive material only.
2. **The human column**: the anchors' published tables as published (already structured; untouched).
3. **The model column**: gemma12 extracts every primary from the ORIGINAL text, 2 replicates; the first-parseable replicate is the primary sheet; replicate 2 serves the reliability metric. Both columns — human and model — are graded against the same two-layer keys by the same rite (quote before verdict; the mechanical comparator is Study 6's magnitude comparator, declared an approximation; residue goes to adjudication).
4. **Deterministic recomputation**: per-study effects and pools from the model's sheets — MA-1's five frozen outcome families (morbidity, mortality, ileus RRs; flatus, oral-diet MDs), pools under MH and DL with the comparison under DL (anchor erratum #15); MA-2's per-study HbA1c MDs and the DL pool. The MA-1 **ileus pooled comparison is non-comparable by construction** (erratum #16: one published row is a different outcome) — reported as such, counted, never silent.
5. **The three-way exhibit**: per trial, one table — source quote × human cell × model cell — with every disagreement classified into Study 6's frozen categories (reproduz / difere-por-errata-da-âncora-#N / rota-do-modelo / erro-do-modelo / fonte-indisponível). The reader sees the errata rather than trusting our word.
6. **No perturbation, no seal, no reversal** — declared: graders compare directly.

## 5. Pre-registered hypotheses

- **H7.1 (reliability in natural conditions)**: replicate 1 vs replicate 2 agree on ≥95% of graded cells, per anchor.
- **H7.2 (the errata are visible in the model column)** — over the MA-1 errata-cell panel, frozen here: Yoon n (#1: source 39/36), Weinberg ASA (#3: source reports what the anchor calls "Not stated"), Sun oral-diet time (#9: source medians 4.0/6.0 days), de Waal ASA (#10: source GDFT 17:132:95:4), Diaper ASA (#11: source reports), Castro ileus (#16: source has no ileus → NR is the correct cell), Coeckelenbergh blood loss (#17: source GDFT 450 [300–600]). Claim: the model's cells side with the **source** on ≥90% of the panel (format variance allowed, e.g. percentages for counts), and on **100% of the direction-critical swaps** (#1, #10, #17). MA-2 has no confirmed anchor-errata panel; its three-way table is exhibited without this hypothesis, and any new discovery is logged as a pending item, never invented.
- **H7.3 (the recomputation lands)**: from the model's clean-text sheets, the engine reproduces — MA-1 pooled morbidity and mortality under DL within ±0.01 on RR and each CI bound; MA-2 pooled MD within ±0.02 of −0.24 and CI bounds within ±0.02 of [−0.32, −0.16] (fresh-extraction variance measured at one hundredth in Study 6).
- **H7.4 (the measured band holds)**: all sheets parseable; ≥90% of key-graded cells filled; **zero inventions**.
- *Declared exploratory (not a hypothesis)*: a descriptive cell-level comparison of Study 7's clean-text MA-1 sheets against Study 6's perturbed-text sheets — **confounded by the instrument-language change** (PT→EN) and reported descriptively only.

## 6. Outputs

`dados/estudo7/saidas/gemma12/{ma1,ma2}/` (raw runs) · `prompts/` (frozen instrument copies) · per-trial three-way tables (`tabela-tripla-*.md`) · per-outcome comparison + pools · paired forest plots · `avaliacao-estudo7.md` · run log.

## 7. Out of scope

Reading-proof claims (see §2); other models; orchestration (all arithmetic is code); audit stages; committees; any change to keys, instruments or errata beyond what is frozen here.

---

## Amendment 1 (2026-09-01) — detection nets over the deterministic downstream (registered before the run)

**Author's directive**: as an advance within Study 7's deterministic sequence, arm detection-only nets over the **same frozen sheets** and re-emit the downstream. Study 5's doctrine unchanged: nets **detect and warn, never substitute a value**. The primary H7.3 record stands exactly as measured (MA-2 pool −0.34); this amendment adds a measured question, not a correction.

**Provenance (the "which harness" question, answered for the record)**: the benchmark has exactly one detection-net harness — Study 5's frozen ten-net, warn-only conversational harness — and its product-level CI-coherence check is what flagged Chen in Study 6's formal MA-2 run. That harness operates on *model-emitted calls and reports*; Study 7's downstream has no model in the loop (§7), so the same code cannot literally run here. This amendment **ports the same doctrine to the sheet layer** as two deterministic nets, declared here before any execution:

- **N7-1 — dispersion-type vs printed source form (per arm, MA-2 sheets)**: locate the arm's declared change mean in the ORIGINAL text (tolerance ±0.05 for the model's rounding); mechanically classify the dispersion form printed around it — single-spread ("± x", "(x)") vs interval ("(a ~ b)", "(a to b)", "(a, b)"); **FLAG** when the sheet declares a single-spread type (SD/SE) but only interval forms are printed at that mean, with the detail strengthened when the declared dispersion equals the printed interval's half-width. A mean not locatable in the text is reported as *not-located*, never flagged.
- **N7-2 — weight dominance (product layer; Paper 3's recommended flag)**: each study's DerSimonian–Laird weight share in the pool; **FLAG** any share > 40%. Applied to the MA-2 pool and, for symmetry, the MA-1 dichotomous pools — with the declared caveat that pools of ≤2 studies exceed 40% structurally (reported, not counted as dominance findings).

**Inputs**: the existing replicate-1 sheets and the original texts — no re-extraction, **no model call anywhere**. **Outputs**: `redes-deteccao.md` + JSON, and an amendment section in the evaluation record.

**Pre-registered hypotheses**:
- **A7-H1**: N7-1 flags exactly Chen's two arms and **no other MA-2 arm** (zero false positives).
- **A7-H2**: among pools with ≥3 studies (MA-2; MA-1 morbidity), N7-2 flags the MA-2 pool — with Chen the dominant study — and does not flag morbidity.

## Amendment 2 (2026-09-01) — N7-1b, the both-forms consistency rule (registered before its run; after Amendment 1's run)

**Amendment 1's measured outcome, recorded before this extension**: **A7-H1 failed** — N7-1 as registered flagged nothing, and the reason is itself a finding: Chen's primary prints the change in **two layers** — the table as mean (95% CI), *"−1.63(−1.96 ~ −1.30)"*, and the results prose as *"the HbA1c (−1.6±0.3 vs. −1.0±0.3%)"* — so a spread-form **is** printed at that mean and N7-1's declared rule correctly stays silent. The model's cell is a verbatim transcription of the prose layer, not a computed value; the failure of the sheet is the **type judgment** on an ambiguous "±" (0.3 equals the table CI's half-width 0.33 — the paper's ± denotes the CI, not an SD). **A7-H2 also failed**: Chen's DL weight share is 19.3% (τ² absorbs the outlier and re-equalizes weights); the distortion's product signature is **heterogeneity inflation** (published I² 6% → ours 79%), not weight share — the >40% flag is blind to this mode.

**N7-1b (declared here, detection-only, before its run)**: when BOTH forms are printed at the same mean — an interval and a "± x" spread — and the sheet declares a single-spread type, compare the spread value against the interval's half-width: **FLAG** if they coincide (±0.06), because a ± that equals the CI half-width is the CI in disguise, and an SD declaration over it is mechanically suspect. A spread that differs from the half-width (a genuine SD/SE printed alongside a CI) is coherent — no flag.

**Hypothesis A7-H3**: N7-1b flags exactly Chen's two arms and no other MA-2 arm.

## Amendment 3 (2026-09-01) — the deployment cell: model under the frozen ten-net harness, clean texts (registered before the run)

**Author's directive**: release the Study-5 configuration — the model orchestrating its own calculations under the frozen warn-only harness — into Study 7's clean-text scenario, to identify the configuration closest to the truth in **real-world conditions: no answer key anywhere in the loop**. This fills the last cell of the series' 2×2 (perturbed/clean × deterministic/harness-orchestrated) and turns Study 7 into a three-configuration comparison on the same corpus: (a) deterministic, no nets — the silent distortion; (b) deterministic + sheet-layer nets (Amendments 1–2) — one mechanical flag; (c) model + conversational ten-net harness — this run.

**Procedure (frozen, reused, declared)**:
- The **frozen Study-5 pipeline-v3 procedure** (`pipeline3-gemma.py`), run under Study-7 labels: rung **CALC3E7** (the `CALC3*` prefix arms the complete frozen net set — schema-constrained typed calls with per-argument declared sources, source/derivation/type/interval-order/interval-coherence nets, negative-SD check, closing-vs-executed check, warning budgets), pooling **POOL3E7** (G3b instruments), then code totals, the E5-5 product-layer CI-coherence check (flag, never endorse), synthesis with the orphan check, and the forest by code. Harness artifacts land under the harness's own tree (`dados/estudo5/saidas/CALC3E7`, `resultados-POOL3E7.json`), as in Study 6's formal run — precedent §3.5 there.
- **No new extraction**: the input sheets are Study 7's frozen clean-text MA-2 sheets (first-parseable replicate, the same ones the deterministic analysis used), converted EN→PT by the frozen correspondence tables (`dados/instruments-en/README.md`) and seeded into the pipeline's sheet folder — values untouched, presentation-layer conversion only.
- The **harness dialogue runs as frozen — in Portuguese**: it is the archived Study-5 instrument, and running it unmodified is the point (the English harness build remains future work, as declared in the instrument library).
- **No answer key, no published value, and no seal is visible to any model stage**; grader-side comparison happens only afterward, for the record.

**Pre-registered hypotheses**:
- **AE3-H1 (the deployment claim)**: the product-layer coherence check flags Chen — as it did in Study 6 — with **no key in the loop and no value substituted**.
- **AE3-H2 (warn-only doctrine visible)**: the pipeline's pool is internally consistent with its own executed sextets and stays in the distorted band (more negative than −0.30) — the harness makes the problem visible, it does not make the number right.
- **AE3-H3**: zero orphan numbers in the synthesis; zero substitutions anywhere.
