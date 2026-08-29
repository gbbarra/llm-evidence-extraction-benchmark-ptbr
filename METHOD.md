# EXTRAI — the benchmark that asks whether a model reads like a reviewer

**EXTRAI** is a scientific evidence-extraction benchmark for local language models, sibling of [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr) (the faithful-summarization benchmark). The name is the Portuguese verb "extract!": the central question is whether a model, facing a full clinical trial, **extracts** what a human meta-analysis reviewer would extract — the right numbers, from the right sections, admitting what the paper does not report.

> FIEL asks whether the model *writes* faithfully. EXTRAI asks whether it *reads* like a reviewer.

## Why it exists

EXTRAI was born from deliberate doubt about FIEL's own results. Fourteen parts of a summarization benchmark produced a recurring verdict: the big models (qwen3.8:27b, gemma4:26b) have near-perfect fidelity but undisciplined writing — they would be "extractors and auditors, not writers". That phrase became a hypothesis that had never been tested **on the actual extraction task**. EXTRAI is that test, with three method changes designed to attack FIEL's known weaknesses:

1. **The answer key is human and external.** In FIEL, the judge (a larger LLM) decides what counts as an error. In EXTRAI, the gold standard is the extraction tables of a published, peer-reviewed meta-analysis — what two real human reviewers extracted from the same papers the model reads.
2. **Primary grading is mechanical.** A script compares the model's extraction with the answer key cell by cell, under pre-registered tolerances. The LLM judge only enters for adjudicating disagreements and for the synthesis phase — drastically reducing the surface of subjectivity FIEL admitted.
3. **The answer key is itself on trial.** When the model disagrees with the key, the primary source decides — by the rite inherited from FIEL: *verify against the source before deducting*. If the human reviewers got a cell wrong, the disagreement is adjudicated in the model's favor and becomes a **documented erratum of the meta-analysis**. The benchmark measures the model and audits the review at the same time.

## The design, in one sentence

An anchor meta-analysis published **after the models' training cutoffs**, with primaries in open access, supplies the task (extract evidence from the primaries), the answer key (its own extraction tables) and the human reference judgment (risk of bias and synthesis) — and the primaries are **numerically perturbed** before reading, so that reciting memorized values (from the original article or from the meta-analysis itself) becomes detectable.

## The three tasks

| Task | What the model receives | What it returns | How it is graded |
|---|---|---|---|
| **T1 — Structured extraction** | Full text of a primary RCT (perturbed) + an extraction form | JSON with the cells (value + location in the article) | Script compares with the meta-analysis's key, cell by cell; disagreements go to adjudication |
| **T2 — Risk of bias** | The same primary + the 7 Cochrane domains | Low/High/Unclear judgment per domain + justification | Agreement with the reviewers' RoB table, domain by domain |
| **T3 — Synthesis** | The model's **own T1 extractions** (all primaries) | Narrative synthesis of the evidence body | LLM judge under the rite, against the meta-analysis's conclusions: direction of effect per outcome, uncertainty, no invention |

## Cell scoring (T1)

Each form cell receives exactly one label:

| Label | Definition | Value |
|---|---|---|
| **exact** | Equal to the key under the pre-registered tolerances (rounding, unit) | 1.0 |
| **derivable** | Not literal in the key, but correct arithmetic over source values (e.g., a percentage computed from events/total) | 1.0 |
| **disagreement-adjudicated-to-model** | Differs from the key, but the primary source confirms the model → meta-analysis erratum | 1.0 |
| **correct-NR** | Model declares "not reported" and the datum is in fact absent from the primary | 1.0 |
| **omission** | Model leaves empty or "NR" when the datum is in the primary | 0.0 |
| **wrong** | Differs from the key and the source confirms the key | 0.0 |
| **invented** | A value that exists nowhere in the source | 0.0 and counted separately (invention rate) |

The primary metric is **cell accuracy** (share of cells worth 1.0). The **invention rate** is reported separately, because inventing is worse than omitting — FIEL's signature carries over.

Cells that are the reviewers' meta-analytic computations (risk ratio, mean difference, 95% CI, weights, GRADE) stay **out** of the form: the model extracts primary facts, it does not redo the meta-analysis — except in T3, where the qualitative direction of effect is what gets judged (and in Study 2, where the arithmetic itself becomes the object).

## The dual reading proof

Inherited from FIEL and adapted: in each primary, K numbers that appear in the answer key are quietly altered before the model reads (the original↔perturbed table stays sealed until grading). At grading time, a perturbed cell has three fates:

- **perturbed value** → the model *read* the article it received (the cell is graded normally, against the perturbed value);
- **original published value** → the model *recited* — either the primary memorized from training, or the meta-analysis itself. Recitation zeroes the cell and is counted as evidence of contamination;
- **absent/other** → normal rules apply.

Since the anchor meta-analysis postdates the training cutoffs, reciting the review is unlikely — but the perturbation turns that assumption into something **measured**.

## The adjudication rite

Every disagreement between model and key passes through the rite before becoming a deduction: **verify against the primary source before deducting**. The adjudicator (LLM judge + human author) locates the source passage that decides the cell and records the literal quote in the grading file. The human key has no immunity: anchor errata found along the way are documented in their own file, never silently edited — the ruler bends for no one, not even published reviewers.

## Transparency of authorship

Every EXTRAI report, grading and article separates three voices, always named:

1. **The local model** — the object under measurement. Its outputs are quoted verbatim and marked as such ("gemma4:12b returned…"), together with the mechanism: which prompt it received, what it returned, in how long.
2. **The mechanical grader** — a deterministic script (public in the repository) that compares cell by cell. Every numeric metric comes from it.
3. **The adjudicator** (LLM judge + human author) — enters only on disagreements and on the synthesis, always with the deciding source quote.

No harness or judge analysis is presented as model output, and vice versa.

## Freezing contracts

1. **Frozen corpus**: the anchor meta-analysis, the primaries and the perturbations are fixed before any measurement and do not change within a series.
2. **Pre-registered protocol**: hypotheses, form, tolerances and scoring rules are written before the first run; later changes only by dated amendment.
3. **Frozen models and configs**: models enter with the same configurations as the standing FIEL table (vendor sampling, recorded context, CPU/GPU recorded per model).
4. **Pre-existing inconsistencies registered**: internal contradictions of the meta-analysis itself, detected while building the corpus, are listed in the protocol *before* the runs, so grading has no interpretive freedom.

## Reproduction

```
scripts/estudo1/baixar-corpus.py      # downloads MA + open-access primaries (Europe PMC)
scripts/estudo1/extrair-gabarito.py   # MA tables -> structured answer-key JSON
# (remaining scripts listed in each study's protocol)
```

Requirements: Python 3.12 (stdlib only for the corpus; pypdf for the closed stratum), Ollama for the local models. Each study has its own protocol in `dados/estudoN/` with the exact execution queue. Task prompts are in Brazilian Portuguese by design (see README, "Language conventions").

## Studies

| Study | Question | Status |
|---|---|---|
| [Study 1](dados/estudo1/protocolo-estudo1.md) | Do the four FIEL veterans extract evidence like the anchor meta-analysis's reviewers? | **complete** ([evaluation](dados/estudo1/avaliacao-estudo1.md) · [analysis](dados/estudo1/analise-estudo1.md) · [anchor errata](dados/estudo1/erratas-da-ancora.md)) |
| [Study 2](dados/estudo2/protocolo-estudo2.md) | Can they redo the meta-analysis's statistics — by head and with a calculator? | **complete** ([evaluation](dados/estudo2/avaliacao-estudo2.md) · [analysis](dados/estudo2/analise-estudo2.md)) |

## Standing table

Study 1 complete (all 14 primaries — open + closed strata; 156 gradable cells/model; graded 2026-08-28):

| Metric | gemma4:12b | gemma4:26b | qwen3.8:27b | qwen3:14b |
|---|---|---|---|---|
| Extraction (accuracy vs source) | **100%** | **99%** | 97% | 92% |
| — wrong / invented / recited cells | 0 / 0 / 0 | 0 / 0 / 0 | 1 / 0 / 0 | 0 / 0 / 0 |
| RoB (agreement, 7 domains × 13 trials) | **80%** | 79% | 62% | 59% |
| Synthesis (compatible direction + zero orphan numbers) | ✓ | ✓ | ✓ | ✓ |
| Total time (57 runs) | ~2.2 h | ~2.0 h | ~7.1 h | ~1.7 h |

Verdicts: H1.1 refuted (gemma discipline won extraction too) · H1.2, H1.3, H1.5, H1.6 confirmed · H1.4 partial. **Across 624 decided cells: 1 wrong, 0 invented, 0 attributable recitations** — while the published meta-analysis accumulated 15 source-confirmed errata/divergence entries, and the adjudicator logged 3 errata of his own, on public record. The ruler bends for no one.

Study 2 (the arithmetic; graded 2026-08-29): by head, exact 95% CI = **0/30 across the four models** and 1–3 exact RRs per model; with the calculator (CALC protocol), qwen3.8:27b closes **8/8 point estimates and 8/8 intervals**, qwen14 7/8, gemma12 6/8 — and gemma26 fires 20 calls without ever emitting the answer. No model orchestrated the pooling through the tool. Thinking (exploratory): triples simple arithmetic, costs 10–17×, and collapses into perseveration on pooling. Bonus: the anchor's 11 per-study RRs are all correct, but its pooled morbidity is an exact DerSimonian-Laird labeled Mantel-Haenszel in the caption — erratum 15.
