# EXTRAI — Study 2 evaluation (grading record): "the arithmetic"

Queue of 51 runs completed in 71 min (2026-08-28); grading 100% mechanical (`corrigir-e2.py`): each quantity's truth is the recomputation — by the harness's functions, validated against the anchor's published values (the test case reproduces them exactly: RR 0.573; CI 0.372–0.884) — over the input the model itself received (its Study-1 extractions, parsed under fixed rules documented in the grader).

**Who did what**: the models computed (arm A) or orchestrated calls (arm B); the harness executed the functions and returned results; the grader labeled every quantity with no language-judge involvement.

## Execution record

- Bug fixed before analysis: the exploratory *thinking* arm came out empty in its first round (the reasoning budget consumed all of `num_predict`); re-run with `12000 + 1600` tokens after a 5,600-token attempt also collapsed silently.
- gemma26 in arm B (rr family) hit the 20-call cap without emitting the final JSON within 5 rounds — scored as a closure failure (invalid JSON), not an arithmetic one.
- In arm B's *pool* family, qwen14 and qwen38 **did not call the calculator** (0 CALC) and answered directly; gemma26 wrote the calls **inside** the JSON as text (understood the what, not the how). The behavioral record is itself a result.

## Scoreboard (replicate 1; a point = one per-study RR or MD)

| Model | Arm | Quantities | Exact | Right direction | Wrong | NC-refusal | Exact 95% CIs |
|---|---|---|---|---|---|---|---|
| gemma4:12b | A | 7 | 1 | 5 | 1 | 1 | **0/7** |
| gemma4:12b | **B** | 8 | **6** | 2 | 0 | 0 | **6/8** |
| qwen3:14b | A | 8 | 2 | 4 | 2 | 0 | **0/8** |
| qwen3:14b | **B** | 8 | **7** | 1 | 0 | 0 | **7/8** |
| gemma4:26b | A | 8 | 1 | 5 | 2 | 0 | **0/8** |
| gemma4:26b | **B** | — | closure failure (rr); honest md (NC×5) | | | | |
| qwen3.8:27b | A | 7 | 3 | 2 | 2 | 1 | **0/7** |
| qwen3.8:27b | **B** | 8 | **8** | 0 | 0 | 0 | **8/8** |

Pooling (MH/DL/IV): arm A — 2 exact of 24 attempts (gemma26 landed 2 pools by head; the rest wrong or NC); arm B — qwen14/qwen38 ignored the tool on pooling (by-head values, wrong), gemma26 did not close; **no model orchestrated the pooling through the calculator**.

## Exploratory arm (qwen3:14b + thinking, arm A, 1 replicate)

Execution record: at 5,600 thinking tokens the reasoning consumed everything and no answer was emitted (the echo of FIEL Series 1's metacognitive collapse); it converged at **12,000 tokens** (323–1,019 s per run — 10–17× the non-thinking cost).

| Family | Result with thinking | Without thinking (same model) |
|---|---|---|
| Per-study RR + MD | **6 exact / 7 points** + 1 honest NC | 2 exact / 8 |
| 95% CI | **0/7** — the boundary holds | 0/8 |
| Pooling | **perseveration collapse**: the same two numbers (0.768/0.741) cloned across four outcomes, two of them ("recurrence", "symptoms") nonexistent in the input — the only *fabrication* in all of Study 2 | wrong/NC |

Reading: thinking is the only "by-head" route that approaches the calculator on simple arithmetic — and its morbidity "random effects 0.741" landed 0.03 from the true DL before being cloned into phantom outcomes. But the CI stays impossible, pooling melts into perseveration, and the cost is an order of magnitude. The calculator beats thinking on precision, cost and sanity.

## Arithmetic audit of the anchor (H2.6)

Mechanical recomputation of the MA's tables 5/6/11 from the published cells:

- **Per-study RRs: all correct** (11/11 within ±0.015).
- **Pooled morbidity: the published number reproduces digit-for-digit under DerSimonian-Laird (recomputed from the as-published cells of table 5: 0.778 [0.567–1.068]; τ² 0.074, I² 76.3%) — but table 5's caption describes it as Mantel-Haenszel** (the recomputed MH gives 0.873 [0.758–1.005]). A method-label erratum: right number, wrong name (anchor erratum 15). Pooled mortality also reproduces digit-for-digit under DL (1.021 [0.446–2.337]).
- *Correction (2026-08-29, verified re-run):* the first ad-hoc recomputation reported here as "0.774 [0.566–1.059]" (MH "0.863"; mortality "0.027 divergence") could not be reproduced from the anchor's cells under any input variant tested (as-published; Yoon arms swapped; Wu 61/61; with deWaal; inverse-variance over the published RRs — all yield 0.778 for morbidity). The verified figures above come from the anchor's as-published cells with the same validated Study-2 functions; the finding is unchanged and stronger (the DL reproduction is exact, not approximate).
