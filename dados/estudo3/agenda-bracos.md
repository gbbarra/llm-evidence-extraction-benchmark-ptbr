# Study 3 — question ledger

## Paper 1 (CLOSED — preprint ready)

The baseline arc: read → compute → chain → **reproduce the low-carb meta-analysis** (unperturbed diamond −0.28 [−0.39, −0.17] vs published −0.24 [−0.32, −0.16]). Ends at the first diamond by the author's editorial decision (commit 70c4249).

## Paper 2 (REORGANIZED 2026-08-30 — one question, one answer)

**Question: can local models that fit on the integrated GPU (≤14B) reach the expected meta-analytic value, if the harness is fixed?**

Design principles set by the author:
- **Focus**: iGPU models only — gemma4:12b + qwen3:14b — and harness engineering; bigger/CPU models (gemma26, qwen38) return later only as reference points; previously discarded small models (e.g., llama3.1:8b, qwen3.5:9b, deepseek-r1:14b) may enter after the harness works.
- **Starting point**: the extraction sheets already exist (gemma12, 98%, replicate-identical) — the study starts from the audited-clean sheets, not from the PDFs.
- **Outcome**: the diamond. Primary metric = |pooled MD − mechanical truth over the same sheets| (target: digit-exact, as the 27B achieved on committee-OR sheets); anchor comparison via the unperturbation lens (published −0.24).
- **Seeded errors: DROPPED from the main line** (decision record below). **Corpus perturbation: KEPT** (contamination defense; costs nothing — the sheets already live in the perturbed world; the double target sheet-truth/unperturbed-vs-anchor is already built).

The harness ladder (independent variable; each rung pre-registered before running):

| Rung | Harness | Status |
|---|---|---|
| H0 | v2, spontaneous discipline | **measured**: both small models fail (mixed-round; by-head; wrong-side diamonds) |
| H1 | v3 nets (flow policing) | **partially measured** (gemma12 L+S ran before the pause): flow fixed — tool used, pool reconciled, closed — diamond still wrong (+0.37/+0.36) because argument assembly drops signs; content failure, nets can't reach it |
| H2 | **harness-driven ("esteira dirigida")**: harness owns everything deterministic; model consulted only at judgment triggers | **MEASURED (Amendment 8)**: zero triggers fired on these sheets (the extractor had already resolved the signs via its route choices) → all three arms = mechanical truth **digit for digit** (−0.52 [−0.82, −0.22]). The answer to Paper 2's question is YES — and stronger than predicted: on this corpus, model necessity concentrates 100% at extraction; everything after is code |
| H3 | H2 + targeted field re-verification (one field, one question) where sheets are uncertain | optional rung |

**Answer: YES.** With the harness owning the flow, the expected value comes out exact using only the 12B extractor — the judge models were not even needed on this corpus (zero triggers). Caveats for the paper: zero triggers is corpus-specific (the extractor picked negative-sign routes); the judge-model comparison needs corpora whose triggers fire — which is the generalization study's opening question.

### Seeds decision record (author asked for rigor here)
The 8 seeded errors existed to answer ONE question — "is the audit gate real?" — and that question is **answered** (sensitivity matrix: 27B 90%, 14B 70%, 12B 60%; complementary blind spots; committee rules quantified end to end). For Paper 2's question the outcome is the diamond, and a seeded lane would conflate harness effects with corruption-propagation effects. Seeds therefore leave the main line; if H2/H3 includes an audit step, its value is measured by **diamond delta with vs without the step**, not by seed sensitivity. The seed matrix becomes Paper-2 motivation/appendix material. (Distinct from seeds, the corpus perturbation stays: without it, "reached the expected value" cannot be told apart from "remembered the published value".)

### Inventory of already-run arms (Paper-2 motivation material; no re-runs)
- all-gemma (Amendment 3): spontaneous small-cast pipeline inverts the answer (+0.85).
- igpu (Amendment 4): audit half works (70%, corrections 7/7), calc dies at the mixed-round joint.
- committee (Amendment 5): OR repairs 10/10 and the 27B calcs sheet-truth digit-for-digit — proof the SHEETS support an exact diamond; MAJ preserves truth but the champion went by-head.
- championship under v3 (Amendment 6, **interrupted by design**): gemma12 L+S only — flow nets work, content assembly fails. gemma26/qwen38 runs and the aud26 arm (Amendment 7) are **paused**, returning only as reference points after H2.

**Publication split**: Preprint 1 = the baseline arc (done). Preprint 2 = this page's question; the removed ablation material (`paper/material-preprint2-ablation.tex`) seeds its motivation section.

**Paper-2 writing note (author's directive, 2026-08-30)**: make the perturbation/unperturbation logic explicit in the article. Models live exclusively in the perturbed world — their diamond (e.g. gemma12's fresh −0.52 [−0.83, −0.21], I² 91%) is the **reading proof**, not an error. Unperturbation is a **grader-side deterministic lens**: the sealed reversal map applied over the same sheets, same pool function (fresh-sheet lens −0.24 [−0.33, −0.16], I² 7% vs published −0.24 [−0.32, −0.16], I² 6%). Models never touch the seal: a model that "recomputed" the original world could not be told apart from one remembering the published value (training-data contamination), and the reversal itself is pure table lookup — deterministic work belongs to code.

**Study 4 measured (2026-08-30)** — the record is [`dados/estudo4/`](../estudo4/avaliacao-estudo4.md): gemma12's fresh extraction + deterministic engine = own-truth **digit-exact** (−0.52) and unperturbation lens **on the anchor to the hundredth** (−0.24 [−0.33, −0.16] vs −0.24 [−0.32, −0.16]) — the paper's question answered YES end-to-end from zero. qwen14 maps the boundary: 74.8% cells (error-dominant with full coverage, not omission-dominant), zero arithmetic error, and still no unique diamond — malformed cells make even deterministic parsing a route choice (errata E4-1..E4-4: leading trigger question; 1-of-3 trigger classes implemented; sign-doctrine overreach in `sexteto`; engine/grader parser divergence). First trigger firing ever recorded (Goday +0.3→−0.3, induced by E4-1, not chargeable).

**Round 2 measured and adjudicated (2026-08-30, [record](../estudo4/rodada2/avaliacao-rodada2.md))** — five extractors, continuous flow, uniform fixed instruments. THE ANSWER, cleanly: only gemma4:12b reaches the published value (lens −0.27 vs −0.24; the other four land −0.44..−0.54 for named reading failures). Architecture holds for all five (zero arithmetic; gemma12 and deepseek14 pipeline≡truth digit-exact). The E4-1 A/B landed: qwen14 kept Goday's +0.3 under the neutral question — round 1's flip was instrument-induced. New behavior classes: llama8 invents (first invented values in the benchmark), qwen35 averages ns (41.5) and writes reasoning into fields, deepseek14 extracts the wrong timepoint and leaks `<think>`. Round 2 is Paper 2's primary record.

## Recommended next steps (registered 2026-08-30, after Study 5 closed; order is the recommendation)

1. **Fold Amendment 7 into Paper 3** — the three-orchestrator table, "form is not semantics", and the union-6/7 observation strengthen the manuscript now, while fresh; then Paper 3 is final for the author's read.
2. **Zenodo release v1.2.0** — the repository has grown by five studies' worth of record since v1.1.0; tag and archive before any new submission so Papers 2–3 cite a DOI that contains their own evidence.
3. **Author reads Papers 2 and 3 → medRxiv** (same recipe as Paper 1); when Paper 1's DOI arrives from screening, update the companion citations in both.
4. **The generalization gate** — top of everything experimental: the frozen engine against the methylene-blue anchor (new domain, dichotomous outcomes, exercising the built-but-untested RR/Mantel–Haenszel half). This decides whether anything above transfers.
5. **Cheap pre-registered arms, in value order** (Paper-3 revision or Paper-4 material): replicate orchestration with an agreement rule (tames the measured weather); a temperature-zero arm (is the weather sampling noise?); an **orchestrator committee** (base ∪ coder covered 6/7 with complementary blind spots — the union begs the committee test, echoing Study 3's auditor committees); the two product-layer flags (missing study; weight dominance).
6. **Series part 4 on LinkedIn** — Studies 4–5 and the trilogy deserve the communication piece, after the preprints are public.

Instrument-fix backlog (future corpora/rulers, never retroactive): title/byline kept in corpus text (gap #5 — recurred in Study 4: qwen14 confabulated "Zhou et al. 2019"); `estudo` field graded; perturbation operator covers number words (#1), totals with visible addends (#2), twin tables (#3), rounded prose restatements (#4); neutral trigger question with no embedded premise (E4-1); all three declared trigger classes implemented (E4-2); Wang sign convention scoped to printed-drop fields in `sexteto` (E4-3); one shared bounds/route parser for engine and graders (E4-4).
