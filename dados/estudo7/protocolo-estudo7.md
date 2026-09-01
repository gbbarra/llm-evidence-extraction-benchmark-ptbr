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

*Amendments: (none)*
