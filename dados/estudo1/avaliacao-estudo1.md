# EXTRAI — Study 1 evaluation (grading record)

Grading closed 2026-08-28, **across both strata** (open: 8 primaries; closed, Amendment 2: 6 primaries — the entire meta-analysis). Ruler: `gabarito-oficial.json` (layer 2, verified against the primary sources — Amendment 4), with the perturbations on top and the public adjudications in `adjudicacoes-t1.json` + `adjudicacoes-t1-fechados.json`. Instruments: `corrigir.py` (T1), `corrigir-rob.py` (T2), and the syntheses' anti-invention check.

**Who did what**: the local models produced the 232 graded runs (queues of 2026-08-27/28); the mechanical grader decided the cells under pre-declared equivalences; the adjudicator (Claude, under the author's supervision) decided the textual cells, each with a source quote; the adjudicator's own errors along the way are in `erratas-da-ancora.md`.

## T1 — Structured extraction (primary metric: accuracy against the source)

156 gradable cells per model (99 open stratum + 57 closed; the rest of the form — no MA value with no source verification, pending, or datum absent from the input — counts against no one). Zero cells left undecided.

| Model | Open | Closed | **TOTAL** | Omissions | Wrong | Invented/Recited |
|---|---|---|---|---|---|---|
| gemma4:12b | 100% | 100% | **100%** (156/156) | 0 | 0 | 0 |
| gemma4:26b | 100% | 98% | **99%** (155/156) | 1 | 0 | 0 |
| qwen3.8:27b | 98% | 96% | **97%** (152/156) | 3 | 1 | 0 |
| qwen3:14b | 90% | 95% | **92%** (143/156) | 13 | 0 | 0 |

- **Across 624 decided cells in the four models: ONE wrong, zero invented, zero attributable recitations.** The study's single wrong cell belongs to qwen3.8:27b on de Waal: it placed the PGDT arm's perturbed value in the control field while reading a flowchart the PDF extraction had linearized into genuine ambiguity ("…274 Assigned to PGDT group 259 Received…"). Everything else lost is omission: "NR" where the source reports.
- qwen3.8:27b holds the **highest count of exact cells** — when it answers, it is the most literal; it loses by refusing. qwen3:14b is the most conservative (13 omissions).
- Format failure: 1 invalid JSON in 64 open-stratum extractions — gemma4:26b, Sujatha r1, a key fused with a value ("ao_control: statistically…"), the MoE token-corruption signature seen in FIEL E14; the valid replicate 2 scored (first-parseable-replicate rule).
- Between-replicate stability (identical field r1=r2): qwen14 84% · gemma26 82% · qwen38 76% · gemma12 75%. Differences are mostly formatting (punctuation/order), not content.

## Reading proof (perturbation)

| Model | Read (perturbed value returned) | Recited | Absent |
|---|---|---|---|
| gemma4:12b | 54 | 0* | 8 |
| gemma4:26b | 53 | 0* | 7 |
| qwen3.8:27b | 50 | 0* | 13 |
| qwen3:14b | 47 | 0* | 14 |

\* Amendment 3: in the cells with harness leaks ("4088mL"; "800-2750"; Diaper's PDF-split "1 13"), returning the original is reading of inconsistent input, not recitation. **No attributable recitation across 228 runs** — the models read what they were given; no sign of training contamination (post-cutoff anchor) or primary memorization.

## T2 — Risk of bias (agreement with the MA's reviewers)

7 Cochrane domains × 13 trials (Weinberg excluded: the MA has no RoB row for it — pre-registered inconsistency #1). Overall judgment reported separately (the MA uses a scale with "Moderate").

| Model | Agreement (7 domains, 13 trials) | Overall equal | Stability r1=r2 |
|---|---|---|---|
| gemma4:12b | **80%** (73/91) | 5/13 | 97% |
| gemma4:26b | **79%** (69/87) | 6/13 | 95% |
| qwen3.8:27b | 62% (56/91) | 0/13 | 80% |
| qwen3:14b | 59% (54/91) | 4/13 | 97% |

By domain (4 models pooled, 14 trials): selective reporting 92% · sequence generation 90% · allocation concealment 77% · incomplete outcome data 76% · outcome-assessor blinding 65% · other bias 63% · **participant/personnel blinding 27%**. In that last domain the pattern is one-sided: the MA judged "Unclear" and the models "High" — in a fluid-therapy trial the anesthesiologist executing the algorithm cannot be blinded, and the models apply the Cochrane rule literally where the reviewers were lenient. A divergence of doctrine, not of reading.

## T3 — Narrative synthesis

Reference (the anchor's abstract, 14 trials): morbidity **no** significant reduction (RR 0.78; CI 0.57–1.07); mortality no difference; **shorter** hospital stay with GDFT; **better** gut function (flatus, oral diet, ileus RR 0.48).

| Model | Words (250–400) | Orphan numbers | Direction verdict |
|---|---|---|---|
| gemma4:12b | 364 ✓ | 0 | compatible, heavy hedging (undersells the gut benefit its own data shows) |
| qwen3:14b | 355 ✓ | 0 | compatible; morbidity more optimistic than the pooled MA, but faithful to its own extractions ("five of eight trials") |
| gemma4:26b | 361 ✓ | 0 | compatible; faithfully cites the perturbed values of its own input |
| qwen3.8:27b | 328 ✓ | 0 | compatible and the most structured; original correct observation ("GDFT reduced fluid volume in every trial that reported it") |

**Mechanical anti-invention check: zero orphan numbers in all four syntheses** — every cited number exists in the model's own T1 extractions. No model invented a meta-analytic aggregate (no fabricated RR/CI); the divergences from the MA (morbidity described as favorable) reflect study-counting without a pooling tool — exactly the gap Study 2 measures.

### T3b — synthesis over the 14 trials (Amendment 2)

Execution record: the prompt with 14 extractions (~16.3k tokens) exceeds the frozen 16,384 context — the first round truncated gemma12 and qwen38 and was discarded; the valid round used `num_ctx=24576` for all four (section-8 clause applied by analogy, recorded in `rodar-t3b.py`).

| Model | Words | Orphan numbers | Morbidity described as |
|---|---|---|---|
| gemma4:12b | 345 ✓ | 0 | "results are inconsistent" |
| qwen3:14b | 316 ✓ | 0 | "beneficial effect… though with inconsistencies" |
| gemma4:26b | 330 ✓ | 0 | "the evidence is inconsistent" |
| qwen3.8:27b | 338 ✓ | 0 | "inconsistent and contradictory" |

**T3b finding**: with 14 trials instead of 8, three of the four models moved morbidity from "favorable to GDFT" to "inconsistent" — **approaching the MA's pooled verdict (not significant)** with no statistical tool, just from seeing more contradictory evidence. More context calibrated the conclusion; formal pooling remains the gap (Study 2).

## Machine time

| Block | Duration (open + closed) | Median/run |
|---|---|---|
| gemma4:12b (integrated GPU) | ~2.2 h | 143–154 s |
| qwen3:14b (integrated GPU) | ~1.7 h | 88 s |
| gemma4:26b (CPU, MoE) | ~2.0 h | 116–123 s |
| qwen3.8:27b (CPU, dense) | ~7.1 h | 417–476 s |

Full queues: 8.3 h (open) + 5.9 h (closed). KV prefix caching (article before instructions) cut replicate cost by ~50–70% relative to each article's first run.
