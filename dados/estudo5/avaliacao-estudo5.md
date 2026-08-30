# EXTRAI — Study 5 evaluation (grading record): "GEMMA-SÓ, the minimal-harness frontier"

Closed 2026-08-30, same day as the runs. Protocol with three dated amendments ([`protocolo-estudo5.md`](protocolo-estudo5.md)); frozen prompts in [`prompts/`](prompts/); every rung's full turn-by-turn transcripts — including the two invalidated runs — under [`saidas/`](saidas/) and rendered readably in `transcricoes-*.md`; the end-to-end pipeline record in [`pipeline/`](pipeline/).

**Who did what**: gemma4:12b (the pinned build, `think=false`) emitted every calculator call, every re-emission after a warning, the pooling call, and the final narrative; the harness executed functions on command, detected and warned (never substituting a value), pre-computed participant totals, and drew the forest; the adjudicator (Claude, under the author's supervision) graded against the graders' mechanical truths — and logs **four harness errata of his own** (§6), each proven by transcript.

## 1. The question (frozen before any run)

**Between H1 (the model assembles its own calls — measured failure: signs dropped, wrong-side diamond) and H2 (code assembles everything — exact by construction), what is the MINIMAL harness under which gemma4:12b orchestrates the meta-analytic arithmetic of its own sheets correctly — if one exists?**

## 2. How it was measured

A ladder of rungs over the model's own round-2 extraction sheets (frozen at `194241e`; orchestration isolated from extraction), under one inviolable rule: **nets may detect and warn, never substitute** — a harness that fixes an argument collapses into H2 and kills the claim. Ceiling: the graders' mechanical truth over the same sheets ($-0.52$ $[-0.82, -0.22]$), never shown to the model. Each rung ran only after the previous was graded; every warning, re-emission and perseveration is archived verbatim.

## 3. The answer

**A minimal harness exists, and it is small.** Schema-constrained emission (Ollama `format`, per-rung grammar), one call per turn, and four detection-only nets — sign-echo, declared-source check, arity with the Portuguese signature, and menu guidance — are enough for gemma4:12b to: assemble per-study calls at 5/7 exactness with zero format failures; **execute the DerSimonian–Laird pooling over its own seven sextets, faithfully and digit-consistently, twice in a row** — the call no model of any size had ever executed in this benchmark; and close the pipeline with a narrative synthesis containing **zero invented numbers**. What the minimal harness does *not* fix has a name (§7).

## 4. The rungs

| Rung | Harness | Result |
|---|---|---|
| G0 (prior) | v3 flow nets, free text | flow OK, signs dropped, wrong-side diamond (+0.37) — the baseline failure |
| **G1** | + sign-echo net (detection-only) | **5/7 exact**, 5.2 min; the Dorans transcript shows the full anatomy: bounds swapped → negative SD → warning → one stubborn repeat → corrected → exact |
| G2 (run 1) | + schema + declared sources | **invalidated as a model measurement** — the harness's arm-blind source net fired on correct control-arm values and steered the model to corrupt them (E5-1); no arity net (E5-2). Archived as evidence of harness-induced damage |
| **G2b** | Amendment-1 fixes | **5/7 exact**, 6.7 min, zero format failures, zero spurious warnings; the two misses are the same two, same classes, as G1 |
| G3 (run 1) | pooling | **invalidated** — the schema helper bound the G2 grammar (off-menu calls representable, E5-3) and an empty pool executed as a misleading `division by zero` (E5-4). Archived |
| **G3b** | Amendment-2 fixes | **PASSED, one turn**: `pool_dl_md` over all seven own sextets, first emission faithful, aggregate closed consistent exact ($-0.50$ $[-0.74, -0.26]$) |
| **Pipeline** (Amendment 3) | all stages, 100% gemma12 | 7/7 studies closed with **zero warnings needed**; pooling consistent again ($-0.46$ $[-0.67, -0.26]$, digit-exact vs its own sextets); 493 participants pre-computed by code; synthesis with **zero orphan numbers**, correctly singling out Wang 2018 as the only CI crossing zero; forest drawn by code |

## 5. Pre-registered hypotheses — verdicts

| Hypothesis | Verdict |
|---|---|
| **H5.1** — schema eliminates format failures | **CONFIRMED**: zero format failures in G2b, G3b and the pipeline (G1's free text had needed format warnings) |
| **H5.2** — sign errors persist at first emission but ≥80% correct after one targeted warning | **MECHANISM CONFIRMED, QUANTIFIER UNDERPOWERED**: the one genuine sign/assembly episode (Dorans G1) was corrected after warnings and ended exact (1/1); the pipeline run needed zero warnings, leaving no sample to quantify the ≥80% |
| **H5.3** — the pooling executes consistently or fails by input, not format | **CONFIRMED, AFFIRMATIVE — the study's headline**: executed consistently twice (G3b and pipeline), faithful sextets, exact closure both times |
| **H5.4** — by-head CIs fail even with confere/não-confere | **NOT RUN**: the author's directive to assemble the full pipeline superseded the G4 probe; it remains available |

## 6. Harness errata (the rite applied to ourselves; all transcript-proven)

**E5-1** arm-blind source resolution — fired on correct control-arm values and actively steered the model to corrupt them: the instrument-A/B lesson of Study 4 reproduced on our own harness. **E5-2** missing arity net — a five-argument call perseverated against a truncated English Python error. **E5-3** wrong grammar bound in G3 — constrained decoding admitted functions the rung does not offer. **E5-4** meaningless execution instead of guidance — an empty pool returned `division by zero` to a model that had not called the pool. Three amendments in one study, each registered before its re-run, each defective run preserved. The meta-result is the thesis of the papers, measured live: **the harness is part of the system under test, and a benchmark that does not audit its own instruments will bill the model for the harness's sins.**

## 7. The 12B's remaining frontiers (named, with evidence)

- **Derived values**: when the sheet forces derivation (Goday: only levels printed), the model derives the *dispersions* correctly (both change-SDs via r=0.5 in the pipeline run) but persists in passing the final **levels** as means ($5.3, 7.1$ → $-1.8$, vs the change-difference $-1.9$) — a route error the detection nets cannot see, because there is no sheet field to echo.
- **Run-to-run habit variability**: the over-conversion habit (feeding its own correct r=0.5 result into `dp_de_se`) appeared in G2b's Goday and vanished in the pipeline's — same model, same sheet, same instruments. Orchestration reliability at 12B is stochastic at the margins; replicates remain mandatory.
- **A consistent private route**: Saslow 2023 came out $-0.18$ $[-0.22, -0.14]$ in every rung — reproducibly different from the graders' route, never unstable. Consistency is not correctness (the Study-4 lesson, again).

## 8. Standing

The author's directive — *turn the best reader into an orchestrator, correcting stage by stage, toward a 100%-gemma12 meta-analysis pipeline* — is fulfilled and archived: reader (round-2 sheets, 92.2% cells), orchestrator (this study), synthesist (zero inventions), with code doing only what code should (execute on command, count, draw, verify). Editorial decision pending: this record becomes Paper 3, or the second half of Paper 2.
