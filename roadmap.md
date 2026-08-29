# EXTRAI — roadmap

Record of future studies discussed with the author. Nothing here is a protocol: each study gets its own pre-registration (hypotheses, rules, corpus) before any run.

## Study 1 — extraction, risk of bias and synthesis (COMPLETE)

Protocol: [`dados/estudo1/protocolo-estudo1.md`](dados/estudo1/protocolo-estudo1.md). Both strata run and graded (2026-08-27/28): all 14 primaries, 232 graded runs, final scoreboard in [`METHOD.md`](METHOD.md).

## Study 2 — "the arithmetic": redoing the meta-analysis's statistics (COMPLETE)

Protocol: [`dados/estudo2/protocolo-estudo2.md`](dados/estudo2/protocolo-estudo2.md). Two arms over the models' own Study-1 extractions — arm A by head (with "NOT-COMPUTABLE" as a dignified answer), arm B through the uniform text-protocol calculator (`CALC: rr(19, 58, 32, 56)` → `RESULTADO: 0.573`), plus an exploratory thinking arm. Graded 2026-08-29; results in the [evaluation](dados/estudo2/avaliacao-estudo2.md) and [analysis](dados/estudo2/analise-estudo2.md). The A→B delta was the gold measure: it separated "doesn't know meta-analysis" from "just lacks a calculator" — the answer is the latter, with workflow (closing the loop, using the tool on pooling) as the residual failure.

## Study 3 — the end-to-end pipeline (COMPLETED 2026-08-29)

Protocol: [`dados/estudo3/protocolo-estudo3.md`](dados/estudo3/protocolo-estudo3.md) (+ Amendments 1–2); results in the [evaluation](dados/estudo3/avaliacao-estudo3.md) and [analysis](dados/estudo3/analise-estudo3.md); article: part 3 ([en](ARTICLE3.md)/[pt](ARTIGO3.md)). Headline: seven trials in, one meta-analysis out — unperturbed diamond −0.28 [−0.39, −0.17] beside the published −0.24 [−0.32, −0.16]; seeds caught 9/10; **the quality gate's own slips cost 6× the planted sabotage** (0.13 vs 0.02 on the pooled MD); the by-head ghost reappeared in three cracks (a flipped implausible sign, unreconciled pool inputs, mental participant sums). The question both studies leave loaded: starting from raw PDFs of a **new** anchor meta-analysis (second clinical domain, post-cutoff, open-access primaries), can the local models produce a complete, auditable **mini meta-analysis** — text to forest plot — in one mini-PC night? And where does error propagate when the stages chain?

**Anchor hunt record (closed 2026-08-29, five rounds, ~320 candidates screened via Europe PMC)**: round 1 (strict: post-cutoff 2026, CC BY, ≥6 OA primaries) → best: methylene blue in shock, 5/9 OA; round 2 batch sweep → best 1/5; round 3 author-year sweep → best 3/11; round 4 (relaxed window + Cureus-targeted) → **low-carbohydrate diets in T2DM, 6/7 OA (86%)**; round 5 (genetics/genomics at the author's request, window widened to 2024–2026) → unviable as a class: pharmacogenomics RCT primaries paywalled (NEJM/JAMA/JACC; 0–33% OA in every probe), gene-therapy MAs pool single-arm trials, diagnostic-yield MAs pool cohorts. Author's final choice among three finalists (low-carb 6/7 single-outcome; pregnancy nutrition 4/6 dual-outcome; methylene blue 5/9): **low-carb T2DM** (PMC13242649) — best corpus feasibility; the single continuous outcome still exercises the full MD chain (per-study MD → CI → DL pool → I² → forest).

The pipeline, each stage cast by its measured winner ("hire like people"):

1. **Extraction** — gemma4:12b on the integrated GPU (100% in Study 1);
2. **Cross-audit** — qwen3.8:27b checks the 12b's cells and flags disagreements (the "model audits model" idea from FIEL E11/E17), with **seeded known errors** to measure the auditor's sensitivity — the reading proof, audit edition;
3. **Arithmetic** — the CALC protocol with the harness **forcing closure** (the workflow fix Study 2 demands: a final mandatory "now only the JSON" round);
4. **Synthesis with numbers** — T3 redone with the pooled results in context: does the morbidity myopia heal when the model sees the pool?
5. **Deliverable** — a script draws the forest plot from the model's numbers; out comes a mini meta-analysis with characteristics table, RoB, forest and conclusion, every cell traceable to its source.

New measurements: cross-stage error propagation (every stage logged), the cross-auditor's catch rate, end-to-end fidelity against a source-verified key, and true total cost (the headline to chase: *"an auditable meta-analysis for zero cloud dollars"*). Author decisions before pre-registration: (a) hunt the second anchor (2–3 candidates from another domain); (b) whether to include a screening stage (PICO → which papers enter); (c) the seeded-errors arm for the auditor (recommended).

## Queued ideas (no design)

- Language study (English vs Portuguese instructions).
- gemma4:31b (dense) as a fifth extractor (probed in FIEL E14: 2.7 tok/s, viable-marginal).
- Cross model-audits-model as a standing verification layer (E11/FIEL heritage).
