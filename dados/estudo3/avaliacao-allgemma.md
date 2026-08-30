# EXTRAI — Study 3, Amendment-3 arm evaluation: the all-gemma cast

Exploratory arm registered in [protocol Amendment 3](protocolo-estudo3.md) *before* the run and executed 2026-08-30: stages A/C/S all performed by **gemma4:12b** (integrated GPU); Stage E reused verbatim from the baseline (same extractor, same sheets, same sealed seeds) — the arm isolates the audit/arithmetic/synthesis cast with identical inputs. Queue: 18 runs in **61 minutes** (baseline: 272). Grading mechanical (`corrigir-e3.py`, arm-aware namespace; a verdict-flattener handles the auditor's nested JSON for metrics while `ficha_auditada` keeps the as-run behavior). Provenance note: the audit outputs' `modelo` field initially recorded the baseline literal (a non-parameterized label, fixed in source mid-run); execution was gemma4:12b throughout (cast log + 3–5-minute iGPU timings vs 13–18 CPU minutes for the baseline auditor); the files carry a correction note.

## Verdict in one line

**The all-gemma pipeline runs — 4.5× faster — and produces a confidently inverted meta-analysis**: pooled MD **+0.85 [+0.31, +1.39]** (clean lane) where the truth over its own sheets is −0.52 and the anchor published −0.24, with the synthesis narrating the wrong sign as a "statistically significant reduction". The measured-winners casting is vindicated by ablation; the collapse concentrates in the arithmetic stage.

## Stage A — the gemma auditor: a per-sheet anomaly gate, not a per-field verifier

| Metric | baseline (qwen3.8:27b) | all-gemma (gemma4:12b) |
|---|---|---|
| Seeded cells caught | 9/10 (90%) | **6/10 (60%)** |
| Exact corrections | 8/9 | 4/6 |
| False alarms, clean lane | 6/93 (6.5%) | **0/95 (0%)** |
| Genuine Chen errors (its own) | half-caught | **confirmed (0/2)** |
| Verdict format | flat keys, as instructed | **nested JSON** (instruction-format slip; corrections were consequently not applied to the sheets the arithmetic stage received — measured, not repaired) |

The catch pattern is qualitatively different and internally consistent: **sheets containing an arm swap received full scrutiny** (13–14 corrections each on Chen and Thomsen, including both swaps fixed with literal quotes and Thomsen's transposed n); **sheets with only an isolated seed received blanket confirms** (both lone sign flips, both Dorans character seeds — 0 corrections). A real-time prediction from this gating hypothesis (the lone Wang sign would pass) was registered mid-run and confirmed. Two cross-family constants: the Chen table's ambiguous column map produced the *identical* baseline confusion (the seeded digit "corrected" to the other arm's value; baselines swapped between arms — the arm's only 3 false alarms), and the imputation habit (computing finals as baseline+change) appeared in both casts. The purest correlated-blindness result: auditing **its own** extraction, gemma12 confirmed its own two genuine dispersion errors, 26/26.

Bonus finding for the instrument file: the gemma auditor surfaced a **literal route everyone had missed** — Chen's prose restates the change as "*HbA1c (-1.6±0.3 vs. -1.0±0.3%)*" (the ± being the rounded CI half-width, a third dispersion representation of the same fact). This exposed perturbation gap #4: **rounded prose restatements survive digit replacement** (the table's −1.63 was perturbed to −1.44; the prose "−1.6" stayed), leaving the text internally contradictory; affected cells grade symmetrically.

## Stage C — the collapse: by-head arithmetic wearing a pipeline

Both lanes "closed" with **zero executed CALC calls**. In lane L the model wrote six `md(...)` calls *and* the final JSON in the same output — the harness's round order accepts a complete-looking JSON before executing that round's calls, so the calls were discarded (an instrument gap co-producing this result, noted for v3: execute pending calls before accepting a final JSON; the baseline never mixed rounds, so its record is untouched). What the by-head JSONs contain:

- Lane L: **2 of 7 studies** (task truncated), both **signs inverted** (+0.8 and +0.18 for reductions), pooled **+0.85 [+0.31, +1.39]** with an invented I² — the wrong side of zero end to end.
- Lane S: seven entries whose *study names are fabricated or mangled* ("Tidgren et al.", "Taves", "S.I. et al. (2021)", "Brackgold et al." — with hedging meta-commentary crammed into the name fields), pooled **+0.61 [+0.13, +1.09]**. These are the **first fabrications of the entire Study-3 cycle**, and they appear exactly where Study 2 located them: where computation goes mental.

The closure nets (non-closure; call-as-data) never fired: the by-head mode satisfies *form* perfectly. A net against tool-avoidance ("no calls executed → reprompt to use CALC") is possible but starts to shade from scaffolding into hand-holding — a design question deferred to the hardened-pipeline study.

## Stage S — fluent propagation

Both syntheses (239/242 words, again under the 250 floor) narrate the inverted pool as "*efeito agregado favorável … estatisticamente significativo*" with textbook heterogeneity prose. Nothing in a synthesis stage defends against a wrong number delivered in the right shape.

## Comparative table (the arm's contribution to the series)

| | baseline (measured winners) | all-gemma12 |
|---|---|---|
| Wall clock | 272 min | **61 min** |
| Audit sensitivity / FA (clean) | 90% / 6.5% | 60% / **0%** |
| Auditor mechanism | per-field verification | per-sheet anomaly gate |
| CALC executed calls | 23 + 22, closed clean | **0 + 0**, by-head |
| Per-study MDs (lane L) | 6/7 exact | 0/7 (2 attempted, both wrong sign) |
| Pooled vs truth | −0.39 vs −0.52 (Δ0.13) | **+0.85 vs −0.52 (wrong side of zero)** |
| Fabrications | none | invented study names (lane S) |

**Answer to the arm's question** (*can the whole pipeline run on the extraction champion alone?*): it runs, it is fast, its audit is a usable coarse gate with zero false alarms — and its output is an inverted meta-analysis delivered with full confidence. Extraction excellence does not transfer to tool discipline; casting stages by measured winners is not an optimization, it is a correctness requirement.
