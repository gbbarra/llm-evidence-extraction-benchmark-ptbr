# Study 8 — the English-instrument replication campaign: consolidated verdict

**Registered 2026-09-01, all phases run and measured the same day** ([protocol](protocolo-estudo8.md)). Per-phase records: [P1 READ](avaliacao-p1.md) · [P2 CALCULATE](avaliacao-p2.md) · [P3 CREATE](avaliacao-p3.md) · [P4 ORCHESTRATE](avaliacao-p4.md) · P5 DEPLOY = [Study 7's record](../estudo7/avaliacao-estudo7.md), already English. Compute: 277 model calls (P1 140 · P2 60 corridas · P3-b 70 · P4 7+pool), ≈ 10.8 h total, zero queue failures, everything resume-safe and committed before each run.

## The pre-registered question

**How well do local iGPU models CORRECT and CREATE meta-analyses against published ones under English instruments — and does the instruction-language change move any result of the Portuguese record?**

## The answer

**The chain reproduces end to end, and the language moved nothing that matters.** The flagship number is the cleanest statement of it: gemma12's unperturbed MA-2 diamond is **−0.27 under Portuguese instruments and −0.27 under English instruments** — identical to the hundredth across the language change, beside the published −0.24.

## Hypothesis verdicts

| hypothesis | claim | measured | verdict |
|---|---|---|---|
| H8.1 | gemma12 in its band; PT ranking preserved | gemma12 103/124 (83.1%) / stability 96.0% (PT: 80.6% / 96.0%); zero attributable recitations in 140 sheets (5 candidates all adjudicated to incomplete-perturbation artifacts, with quotes); deepseek14's parse-fragility class recurs (1 replicate) | **passes** |
| H8.2 | unaided arithmetic fails; calculator repairs | arm A: **1 exact CI in 57**; arm B: **41/50 (82%)** exact CIs among tool-operating models; pools stay beyond the iGPU class in both arms (PT-consistent) | **passes** |
| H8.3 | gemma12 reproduces both anchors; only it reaches the MA-2 diamond | MA-1 pools reproduce (0.779/1.023 vs 0.778/1.021); MA-2 lens **−0.27 ≡ PT −0.27**; others land −0.47…−0.80 | **passes** |
| H8.4 | harness behaviors reproduce under the EN build | 7/7 closed; warnings confirm-or-correct (Goday derivation net ×2, the PT class); pooling digit-consistent; weather Δ0.02; zero orphans; flags never substitute | **passes** |
| H8.5 | per-phase EN−PT deltas within replicate-level variance | reading +3 cells (format-noise band), stability identical; arithmetic signature identical; creation flagship identical to the hundredth; orchestration Δ within the weather band | **passes — "Portuguese did not drive the results" is the measured conclusion** |

## Two findings beyond the replication itself

1. **The dichotomous chain is robust across the entire cast** (new vs the PT record, which had measured it only for gemma12): all five models' MA-1 morbidity and mortality pools reproduce the published values. Counting events and denominators is within reach of every model in this class; **the discriminating task is the continuous chain** — means, dispersions, declared types — exactly where the five MA-2 diamonds separate (−0.27 vs −0.47…−0.80).
2. **The perturbation instrument's known gaps got cross-model evidence**: three models independently *reconstructed* a displaced count from a surviving percentage (57.7% × n printed beside it), and two read a surviving prose copy verbatim — the already-registered gaps #2/#4, now demonstrably exploited by multiple architectures, and zero true recitations.

## The article (the campaign's purpose)

The single article's spine, in the phases' order: **READ** (five models, perturbation proof, the human key on trial, the rite) → **CALCULATE** (unaided fails, the tool repairs) → **CREATE** (the engines build both meta-analyses; the erratum-aware comparison corrects the published one — 17 errata; the five diamonds crown one reader) → **ORCHESTRATE** (the best reader runs its own calculations under warn-only nets) → **DEPLOY** (clean texts, no key: Study 7's three-configuration detection comparison). Every claim draws from this study's record plus Study 7's; the PT-vs-EN ablation is the methods-level result that removes instruction language as a confounder.
