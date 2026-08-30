# What to trust when building a meta-analysis pipeline with local LLMs

Practical recommendations distilled from the EXTRAI benchmark's measured record (Studies 1–4, both papers). Every claim below links to the public evidence that grounds it; nothing here is opinion without a measurement behind it. **Scope**: measured on one clinical domain (type-2 diabetes / diet), one continuous outcome (HbA1c), seven primary RCTs, one quantization per model, consumer hardware (AMD iGPU, Ollama, no cloud APIs). Re-verify before transferring to other domains — see *The generalization caveat* below.

## Trustworthy today (use, with the stated conditions)

| Tool | Measured evidence | Condition of use |
|---|---|---|
| **gemma4:12b as the reader/extractor** | 100% cells in Study 1 ([624 cells](dados/estudo1/avaliacao-estudo1.md)); 92–94% in fresh from-zero rounds ([round 2](dados/estudo4/rodada2/avaliacao-rodada2.md)); 96% replicate agreement; reconstructed the published meta-analysis twice (−0.24 and −0.27 vs published −0.24) | Always two reads per document with an agreement check; factorial groupings routed to a human |
| **The deterministic engine (all arithmetic in code)** | Digit-for-digit reproduction in every verification ([the accounts](dados/estudo4/rodada2/contas-comparadas.md)); validated against published values before any run | The statistical core (DerSimonian–Laird, MD/CI, SD conversions) is textbook and general; **always** run the startup gate (reproduce a known published MA first) and use one shared parser for engine and graders |
| **Sealed perturbation as a reading proof** | Zero attributable recitations across the benchmark; caught every plausibility flip, genuine or instrument-made | Essential when *evaluating* models; optional when *using* an already-validated reader |
| **Narrow, logged judgment triggers** | The neutral sign question kept a genuinely worsened arm's +0.3 (the leading version had manufactured a flip — [the A/B](dados/estudo4/rodada2/avaliacao-rodada2.md)); the missing-field trigger recovered 3 legitimate values | Only with **neutral** questions (no embedded premise about what the data means) and verbatim logging of every firing and answer |
| **Double replicates, first-parseable proceeds** | Separated the stable reader (96%) from the unstable one (58%) | Cheap — always |

## Conditional (only with a human in the loop)

- **A model as auditor** (qwen3.8:27b): caught 9/10 seeded errors **and caused six times more pooled-estimate damage than the sabotage it caught** ([Study 3](dados/estudo3/avaliacao-estudo3.md)). Use exclusively as a **flagger for human review**; never let its corrections enter the flow unreviewed. This is the benchmark's most transferable single recommendation.
- **Auditor committees (OR rule)**: repaired 10/10 seeded errors — promising, but measured only on seeded errors, on one corpus. Same rule: flags, human decides.
- **gemma4:26b as extractor**: read well (99% in Study 1) but failed every workflow task and is CPU-slow. Only if the 12B is unavailable.

## Not trustworthy (do not use, with the measured reason)

- **Any model doing arithmetic in its head** — 0/30 correct confidence intervals unaided; reasoning mode did not save it (0/7) and collapsed at pooling ([Study 2](dados/estudo2/avaliacao-estudo2.md)). An inferential statistic delivered without the computation in sight is decoration.
- **Any model orchestrating its own tools** — no model closed the pooling through the calculator; the best calculator model flipped a sign inside its own call arguments. Orchestration is code's job ([the ladder](dados/estudo3/agenda-bracos.md)).
- **The other four extractors tested** ([round-2 record](dados/estudo4/rodada2/avaliacao-rodada2.md), [sheets side by side](dados/estudo4/rodada2/fichas-comparadas.md)): qwen3:14b computes where it should read and mixes units and levels of analysis; **llama3.1:8b invents values printed nowhere** (the benchmark's only outright fabricator); qwen3.5:9b averages group sizes into "n = 41.5" and writes its reasoning into form fields; deepseek-r1:14b extracts the wrong timepoint and agrees with itself only 58% of the time.

## The recipe, in one sentence

A validated reader (gemma4:12b, double replicates) + all arithmetic in frozen, gate-validated code + neutral logged triggers + automated audit demoted to a flagger + a human at every judgment point — all local, on an integrated GPU.

## The generalization caveat (mandatory)

This confidence was measured on one domain, one continuous outcome, seven trials. The dichotomous half of the engine (RR, Mantel–Haenszel) is built and validated against a second published meta-analysis but has never run under pipeline conditions; transfer to a new domain is a designed, pre-registered next step (a frozen-engine test on a new anchor), not a demonstrated property. If your pipeline targets another domain, run the generalization test before trusting — the harness makes that cheap: seal, extract, gate, compare.

---

*Provenance: distilled 2026-08-30 from the pre-registered records in this repository (protocols with dated amendments, sealed perturbations, mechanical grading, source-quoted adjudications). The two papers carry the full argument: the companion preprint (Studies 1–3) and EXTRAI-2 (Study 4), both in [`paper/`](paper/).*
