# Study 8 — Amendment 1: the sixth reader (qwen3.8:27b low-bit, "Argos")

**Registered 2026-09-07 before the run; run and graded the same day** ([protocol, Amendment 1](protocolo-estudo8.md)). Model: `smtek/Qwen3.8-27B:Q2_K_XL`, digest prefix `d67a36b99f60`, architecture qwen35, **27.32 B parameters at 3.13 bits per weight in 10.68 GB** — a mixed-precision quantization (IQ3_XXS on 77.4% of parameters, IQ3_S on 11.7%, Q3_K and Q2_K on 4.7% each, IQ4_XS on 1.5%, IQ1_M on 0.1%, the rest F32), measured by reading the GGUF header of the weight blob (`scripts/estudo8/gguf-inspect.py`; output `gguf-qwen27q2.json`). Neither name describes it: the tag says `Q2_K_XL` and the header's `general.file_type` says `MOSTLY_Q4_K_S`, which is what `ollama show` prints. The cast's five builds are Q4_K_M, ~4.5 bits per weight. Called exactly like them: `/api/generate`, ctx 16 384, `think:false`, 4 000-token allowance. See [MODELS.md](../../MODELS.md).

**Compute**: 54 model calls in 119 min of sequential iGPU time (P1 READ 77.9 min · P3-b 27.6 min · P2 13.6 min), zero queue failures, zero truncations (all 42 extraction outputs ended with `stop`; 672–1 175 tokens per MA-1 sheet, 400–481 per MA-2 sheet; first replicates 161–295 s, second replicates 42–126 s with the article already cached). Log: [log-amend1-qwen27q2.txt](log-amend1-qwen27q2.txt).

**Record integrity**: the graders were re-run over the extended cast. The five cast models' entries in `avaliacao-p1.json`, `factualidade-p1.json`, `avaliacao-p2.json` and `avaliacao-p3.json` are identical, field by field, to the 2026-09-01 record (pre-run copies kept in `pre-amend1/`); the new model's entries were appended under the key `qwen27q2`.

## The author's question

Does the reader he now uses as primary in the Mnemo review harness reproduce the two anchors, and where does it land against the five-model cast of the English campaign?

## P1 READ — 14 perturbed MA-1 primaries × 2 replicates, English T1 sheet

| model | cells vs key (mechanical) | adjudicated (2026-09-01 rule) | stability r1–r2 | recitation cand. | invention cand. | omissions | value/format |
|---|---|---|---|---|---|---|---|
| gemma12 | 103/124 (83.1%) | 103 | 119/124 (96.0%) | 1 → 0 after adjudication | 0 | 0 | 21 |
| qwen14 | 104/124 (83.9%) | 105 | 123/124 (99.2%) | 1 → 0 | 0 | 6 | 14 |
| llama8 | 88/124 (71.0%) | 89 | 96/124 (77.4%) | 2 → 0 | 0 | 0 | 36 |
| qwen35 | 104/124 (83.9%) | 105 | 103/124 (83.1%) | 0 | 0 | 4 | 16 |
| deepseek14 | 97/124 (78.2%) | 98 | 96/118 (81.4%) | 1 → 0 | 0 | 2 | 25 |
| **qwen27q2** | **107/124 (86.3%)** | **108 (87.1%)** | 117/124 (94.4%) | **0** | **0** | 6 | 11 |

**The 17 divergent cells, by mechanism** (same classes as the record's Supplementary Tables; every cell printed by `p1-divergentes-classifica.py`):

- **7 `tipo_cirurgia` summaries** — the qualitative field summarized ("major abdominal oncologic surgery") instead of the key's enumerated case-mix. The same seven cells are divergent for gemma12, qwen14, llama8 and qwen35 (six for deepseek14): a property of the field, not of the reader.
- **2 REF33 `n_randomizados`** — 224 / 226, the literal allocation numbers; the key's source layer holds 209 / 211 (the analyzed counts, quoted from the primary). Study 1's adjudication had already ruled 224 / 226 "exata" (*"224 alocados (literal; MA usou 209 analisados)"*); the same two cells are divergent for gemma12, qwen14, llama8 and qwen35. Layer choice, and a key-on-trial item that predates this amendment.
- **1 lookup-collision** — Castro (PMC11061212) `perda_sanguinea_controle`: raw `1283.2 ± 959.7 mL`, byte-identical to the key's `1283.2 ± 959.7` plus the unit; the seal reversal corrupted it (grader-side artifact). On 2026-09-01 the author adjudicated this cell correct for qwen14, llama8, qwen35 and deepseek14; the same rule gives the sixth reader **108/124 (87.1%)**.
- **1 re-encoding** — Sun (PMC10694978) `mortalidade_controle`: `0 (0)` vs the key's `0 (0%)`.
- **6 omissions** — NR where the source reports a value: Yun total fluids in both arms (median with IQR), Sun and Wu inotrope use, Diaper ASA in both arms. Omission is the failure class the campaign already calls the acceptable one: the model says it did not find, it does not invent.

**Zero recitation candidates and zero invention candidates**: in 28 sheets the model never wrote a number absent from the perturbed text it read, and never reproduced an original value that the perturbation had displaced. Replicate stability 117/124 (seven cells changed wording or value between replicates; second in the cast to qwen14's 123, ahead of gemma12's 119).

## P2 CALCULATE — arms A (unaided) and B (text-protocol calculator), over its own P1 sheets

| model-arm | exact | direction right | wrong | CI exact | CI wrong | pool exact | pool wrong | not computable (correct answer) | invalid JSON |
|---|---|---|---|---|---|---|---|---|---|
| gemma12-B | 12 | 4 | 0 | 11 | 5 | 0 | 0 | 7 | 1 |
| qwen14-B | 14 | 2 | 0 | 14 | 2 | 0 | 6 | 12 | 1 |
| llama8-B | 8 | 1 | 0 | 8 | 1 | 0 | 0 | 5 | 4 |
| qwen35-B | 8 | 0 | 1 | 8 | 1 | 0 | 10 | 7 | 1 |
| deepseek14-B | 2 | 5 | 1 | 0 | 8 | 1 | 5 | 11 | 2 |
| **qwen27q2-B** | **16** | 0 | 0 | **16** | 0 | **12** | 0 | 12 | 0 |
| qwen27q2-A | 6 | 6 | 3 | 0 | 16 | 2 | 10 | 12 | 0 |

Unaided, the sixth reader shows the cast's signature: 0 exact intervals in 16, pools mostly wrong. With the calculator it is the **first model-arm of the campaign to close every value, every interval and every pool** its sheets support (16/16, 16/16, 12/12, no invalid JSON). The record's sentence *"pool assembly remains beyond the iGPU cast in both arms"* no longer holds for this build; it becomes a named finding of this amendment.

## P3 CREATE — the deterministic engines over the sixth reader's sheets

**(a) MA-1, from the P1 sheets** (erratum-aware comparison in [p3-ma1/qwen27q2/comparacao-detalhada.md](p3-ma1/qwen27q2/comparacao-detalhada.md)):

| pool | qwen27q2 (DL) | gemma12 (DL) | published |
|---|---|---|---|
| morbidity | 0.787 [0.580, 1.068] | 0.779 [0.569, 1.065] | 0.778 [0.567, 1.068] |
| mortality | 1.023 [0.446, 2.346] | 1.023 [0.447, 2.344] | 1.021 [0.446, 2.337] |

Both pools within ±0.01 of the published point estimates. The morbidity difference against gemma12 traces to one row: Calvo-Vecino (REF33), where the sixth reader read the literal counts 18/224 and 35/226 and reproduces the published RR 0.519 exactly, while gemma12 read the percentages (8.6% / 16.6%), derived 19/38 and was flagged for verification. The Wu (PMC10912221) morbidity row (RR 0.594 vs 0.573 published) is flagged "verify" for the sixth reader as for the record — a category-system item, not a new one.

**Invention screen over the Anchor-2 sheets** (`p3b-invention-screen.py`, a re-implementation of the P1 factuality rule for the continuous sheet, run over all six models): the sixth reader's 14 sheets hold 224 numeric cells and 196 numbers, 190 printed verbatim in the perturbed text and 6 derivable from printed pairs — **zero invention candidates**; the same screen returns zero for the five cast models (1,100 cells), which is its own check against the record's 1,104-cell result. Output: `invencao-p3b.json`.

**(b) MA-2, from the P3-b sheets** (7 perturbed primaries × 2, English sheet; 7/7 in the pool, no missing sextet):

| model | sealed lens (unperturbed) | τ² | I² | meets the mechanical "beside" test (all three numbers within 0.05 of the published) |
|---|---|---|---|---|
| **qwen27q2** | **−0.25 [−0.33, −0.16]** | 0.001 | 7.1% | **yes** |
| gemma12 | −0.27 [−0.38, −0.17] | 0.0052 | 28.6% | no (lower bound Δ0.06); called "beside" by the author's judgment in the record |
| deepseek14 | −0.47 [−1.22, 0.28] | 0.9968 | 99.1% | no |
| llama8 | −0.60 [−1.02, −0.18] | 0.1986 | 90.5% | no |
| qwen14 | −0.63 [−1.08, −0.17] | 0.2907 | 95.2% | no |
| qwen35 | −0.80 [−1.67, 0.07] | 0.8977 | 95.0% | no |
| published | −0.24 [−0.32, −0.16] | | | |

The sixth reader's diamond is the closest of the six to the published one, and the first to satisfy the grader's own criterion. Its perturbed-world pool (−0.52 [−0.83, −0.21]) matches gemma12's (−0.52 [−0.82, −0.22]) to the hundredth, as the reading proof requires: the models lived in the perturbed world, and only the sealed lens returns them to the published one.

## Hypothesis verdicts

| hypothesis | claim | measured | verdict |
|---|---|---|---|
| H8.6 | MA-1 dichotomous pools within ±0.01 of 0.778 / 1.021 | 0.787 / 1.023 | **passes** — the "dichotomous chain is robust across the class" finding extends to a 27B low-bit build |
| H8.7 | P1 cells within the cast's range, omission-dominant failures, zero recitations | 107/124 mechanical, 108/124 adjudicated; top of the cast (gemma12 103); classes: 7 summaries, 6 omissions, 2 layer, 1 collision, 1 re-encoding; 0 recitations, 0 inventions | **passes and exceeds** — the best reader of the six |
| H8.8 | MA-2 lens lands beside −0.24 or separates | −0.25 [−0.33, −0.16], the only diamond meeting the mechanical criterion | **lands beside** — the second model to reach the published diamond, and the closest |
| H8.9 | arm B reproduces every supported value; arm A at the cast's error order | B: 16/16 values, 16/16 CIs, 12/12 pools; A: 0/16 CIs | **passes and exceeds** — first perfect arm B including pools |

## Reading, for the author

On this benchmark the reader he uses in Mnemo is the best of the six: the most cells right, the cleanest factuality profile (no inventions, no recitations, failures by omission), both anchors reproduced, and the only one that also assembles the pools correctly when given the calculator. The cost is memory, not time: 10.7 GB resident against 7.6 GB for gemma12 and 9.3 GB for qwen14, and a first-replicate extraction took on average 237 s on the integrated GPU — the same as gemma12's 238 s in the campaign's P1 log (qwen14 231 s, deepseek14 360 s; the two smaller models 106–120 s). Second replicates ran in 42–126 s with the article already cached.

**Caveats, stated once.** One run on one machine; a single community build, mixed-quantized at 3.13 bits per weight, whose two printed names both misdescribe it (measured above); the comparison with the Portuguese-record 27B (Q4_K_M) is not made here, and note that the reason is the quantization alone: this build carries `TEMPLATE {{ .Prompt }}`, the same raw-prompt template that record used (measured 2026-09-08); P4 orchestration was not run for this model and would need a further dated amendment; the two key-on-trial items touched here (REF33 layer choice, Wu morbidity) belong to the record and are not new.

## Files

`saidas/p1/qwen27q2/` (28 sheets) · `saidas/p3b/qwen27q2/` (14 sheets) · `saidas/p2/qwen27q2/` (12 runs) · `p3-ma1/qwen27q2/` (comparison and per-outcome results) · `avaliacao-p1.json`, `factualidade-p1.json`, `divergentes-classificados.json`, `avaliacao-p2.json`, `avaliacao-p3.json` (appended) · `pre-amend1/` (pre-run copies of the five-model gradings) · `log-amend1-qwen27q2.txt`, `log-amend1-graders.txt`.
