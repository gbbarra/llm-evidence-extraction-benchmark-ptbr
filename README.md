# EXTRAI — an evidence-extraction benchmark for local LLMs

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22159050.svg)](https://doi.org/10.5281/zenodo.22159050)

[FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr) asks whether a local model *writes* faithfully. **EXTRAI** (Portuguese for "extract!") asks whether it *reads* like a systematic reviewer: given a clinical trial's full text, does the model extract what the human reviewers of a published meta-analysis extracted — the right numbers, from the right sections, admitting what the paper does not report?

- **[METHOD.md](METHOD.md)** — the full method: the three tasks (structured extraction, risk of bias, synthesis), cell-level scoring with a mechanical grader, the dual reading-proof by number perturbation, and the adjudication rite in which the human answer key is itself on trial.
- **[Study 1 protocol](dados/estudo1/protocolo-estudo1.md)** — pre-registered 2026-08-27: a goal-directed fluid therapy meta-analysis as anchor (Cureus, June 2026, CC BY), all 14 primary RCTs (8 open access + 6 legally obtained), 4 FIEL-veteran models, 6 hypotheses, 4 dated amendments.
- **[Study 2 protocol](dados/estudo2/protocolo-estudo2.md)** — pre-registered 2026-08-28: the meta-analytic arithmetic, by head (arm A) vs through a text-protocol calculator (arm B), plus an exploratory thinking arm.
- **Results**: Study 1 [evaluation](dados/estudo1/avaliacao-estudo1.md) · [analysis](dados/estudo1/analise-estudo1.md) · [anchor errata](dados/estudo1/erratas-da-ancora.md) — Study 2 [evaluation](dados/estudo2/avaliacao-estudo2.md) · [analysis](dados/estudo2/analise-estudo2.md).
- **Articles**: part 1 [en](ARTICLE1.md)/[pt](ARTIGO1.md) ([published](https://www.linkedin.com/pulse/extrai-part-1-i-made-four-local-models-redo-data-extraction-barra-dvfsf/)) · part 2 [en](ARTICLE2.md)/[pt](ARTIGO2.md) ([published](https://www.linkedin.com/pulse/extrai-part-2-model-got-single-confidence-interval-right-barra-oqixf/)) · part 3 [en](ARTICLE3.md)/[pt](ARTIGO3.md) ([published](https://www.linkedin.com/pulse/extrai-part-3-i-built-meta-analysis-pipeline-out-local-gustavo-barra-jpxzf/)).

## Headline results

Study 1 (extraction, all 14 RCTs, 156 gradable cells per model): **gemma4:12b 100% · gemma4:26b 99% · qwen3.8:27b 97% · qwen3:14b 92%** — across 624 decided cells, one wrong cell, zero inventions, zero recitations, while the published meta-analysis accumulated 15 errata/divergence entries and the adjudicator logged 3 of his own. Study 2 (arithmetic): by head, **0/30 exact confidence intervals across all four models**; with the CALC tool, qwen3.8:27b closes **8/8 point estimates and 8/8 intervals**.

## Repository layout

```
METHOD.md                     the benchmark's constitution
corpus/ma/                    anchor meta-analysis (full XML + metadata)
corpus/primarios/             open-access primary RCTs (full XML)
dados/estudo1/                Study 1: protocol, answer keys, adjudications, gradings, model outputs
dados/estudo2/                Study 2: protocol, prompts, gradings, model outputs
scripts/estudo1/              corpus building, perturbation, harness, graders, audit panel
scripts/estudo2/              arithmetic harness (CALC protocol) and mechanical grader
```

## Language conventions

Documentation is in English. The **task prompts are in Brazilian Portuguese by design** — the benchmark's pre-registered scenario is a Brazilian researcher instructing local models in Portuguese over English-language papers; the prompts are frozen experimental instruments and are not translated. Data files (answer keys, adjudication records, model outputs) keep Portuguese field names because the public grading scripts depend on them. File names keep their original Portuguese stems (`protocolo-`, `avaliacao-`, `erratas-`) to preserve published links; the pre-registered protocols were originally written in Portuguese and the original wording is preserved in the git history.

Perturbed copies of the primaries are not versioned: they are regenerated locally by deterministic script, and the original↔perturbed seal stays closed until each grading is published (see protocol §6). Closed-stratum article files are never redistributed (copyright); scripts rebuild the corpus from legally obtained copies.

## Corpus licenses

The anchor meta-analysis (PMC13235771) is CC BY 4.0. The open-stratum primaries are CC BY, except Castro et al. (PMC11061212), CC BY-NC-ND 4.0 — redistributed verbatim, without derivatives, in a non-commercial context. Full attributions in the study protocol. Closed-stratum primaries are not redistributed.

## Author

Gustavo Barra — benchmark conducted with the assistance of Claude (Anthropic). Models evaluated: gemma4:12b, qwen3:14b, qwen3.8:27b, gemma4:26b via Ollama, on consumer hardware (Ryzen 7 + 780M integrated GPU, no discrete GPU).
