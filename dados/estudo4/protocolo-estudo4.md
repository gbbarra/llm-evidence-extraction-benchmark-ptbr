# EXTRAI — Pre-registered protocol, Study 4: "extraction plus deterministic harness"

**Registered 2026-08-30, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). This study is the record behind **Paper 2**; per the author's direction, the GitHub record is built first and the article is written at the end.

## 1. Question (frozen)

**Can local models that fit on the integrated GPU (≤14B) reach the expected meta-analytic value, when extraction is theirs and everything downstream is deterministic code?**

Motivation, measured in Study 3's ladder (see the [question ledger](../estudo3/agenda-bracos.md)): under spontaneous discipline (H0) small models fail at workflow; under flow nets (H1) they fail at content assembly; with the harness owning everything deterministic (H2), the diamond came out digit-exact — but no model worked at runtime (the sheets pre-existed and no judgment trigger fired). Study 4 makes the measurement real: **each model runs the one model-necessary stage — reading — from zero**, and the deterministic engine does the rest.

## 2. Design

- **Corpus**: Study 3's perturbed low-carbohydrate corpus, unchanged (same texts, same sealed perturbations — the reading proof stands; the anchor's published diamond −0.24 [−0.32, −0.16] remains the external reference through the unperturbation lens).
- **Stage E, fresh for every model**: each model extracts all 7 texts, 2 replicates, under the **frozen Study-3 instrument** (`dados/estudo3/prompts/e3-extracao.txt`, unchanged — same instrument, comparable results). All extractions run from zero, including gemma4:12b's (author's decision: nothing inherited).
- **Downstream, 100% deterministic** (the Amendment-8 engine): field parsing, dispersion conversion selected by the sheet's declared type (SD as-is; SE→SD; CI-bounds→SD, last-two-numbers rule; baseline/final→r=0.5 change-SD), per-study MD and 95% CI, DerSimonian–Laird pool — the graders' validated functions. No CALC protocol, no model orchestration.
- **Judgment triggers remain defined** (as-printed positive change; required-field NR; factorial-margin flag): if one fires, the **same model that extracted** answers it (self-contained per-model pipeline), one narrow question per trigger, every firing logged. Study 3's H2 fired zero; whether fresh extractions fire any is itself a result.
- **Models**: now — **gemma4:12b** and **qwen3:14b** (the iGPU pair; qwen3:14b has never extracted this corpus). Extension arm (later, same protocol, dated amendment): previously discarded small models (e.g., llama3.1:8b, qwen3.5:9b, deepseek-r1:14b) as extractors under the identical engine.
- **Replicate rule**: first-parseable proceeds; replicate agreement reported (Study 3 measured 100% cell-identity for gemma12 — a bar to compare against).

## 3. Scoring (mechanical; the rite for ties)

- **Cell level**: each sheet graded against the Study-3 amended ruler (the `EXPECTED` key with its documented alternative literal routes; labels exata/derivavel/nr-correta vs omissa/errada/recitou; residual-leak cells symmetric).
- **Diamond level (primary)**: |pooled MD − mechanical truth over the model's own sheets| — target exact (±0.01 per bound). **Per-model truths may legitimately differ** (different route choices produce different sheet-worlds); each model is judged against its own sheets, and the between-model spread of diamonds is reported as the architecture's signature.
- **Anchor level (secondary)**: unperturbation lens vs the published −0.24 [−0.32, −0.16].
- Studies whose sheets lack sufficient fields are recorded as `dados-insuficientes` and excluded from that model's pool (counted, never silent).

## 4. Pre-registered hypotheses

- **H4.1**: gemma4:12b reproduces its Study-3 extraction profile (≥95% cells; replicate-stable) and its diamond matches its own-sheet truth exactly.
- **H4.2**: qwen3:14b extracts near its Study-1 profile (~90%, omission-dominant); omissions cost pool coverage (`dados-insuficientes`) rather than wrong numbers, and the diamond over its surviving studies still matches its own-sheet truth exactly.
- **H4.3 (the architecture's claim)**: every model's diamond matches its own mechanical truth (deterministic downstream = zero arithmetic error by construction); between-model differences, if any, are fully explained by named extraction differences (routes, omissions) — none by computation.

## 5. Outputs and grading artifacts

`dados/estudo4/saidas/<modelo>/extracao/` (raw runs) · `dados/estudo4/resultados/<modelo>.json` (sheets used, triggers fired, per-study MD/CI, diamond, truth) · `dados/estudo4/correcao/` (cell grading) · run log with the seals' SHA-256.

## 6. Out of scope

Audit stages and seeded errors (Study 3 closed those questions); CPU models (return later only as reference); the CALC text protocol (superseded by the deterministic engine for this question); synthesis and forest rendering (Paper-2 presentation, not measurement).

---

## Amendment 1 (2026-08-30, registered before any extension run): the discarded-smalls extension arm

- **Models**: `llama3.1:8b`, `qwen3.5:9b`, `deepseek-r1:14b` — the small models left out of the original four at screening — as extractors under the **identical** engine, corpus, frozen instrument, 7×2 design, first-parseable rule and §3 scoring. Exact builds pinned in [`MODELS.md`](../../MODELS.md). They are injected into the harness's model table at run time by the new module [`e4-extensao.py`](../../scripts/estudo4/e4-extensao.py); the frozen Study-3 instruments (`e3-harness.py`, `dirigida.py`) are imported, never edited.
- **Output allowance**: `num_predict` 4000 for the three extension models (uniform; the reasoning-family distill may be verbose even with the harness-wide `think=false`). The extraction prompt is unchanged.
- **Erratum fixes applied forward, run-time instruments only**: **E4-1** — the sign-trigger question is rewritten neutrally (states only the analysis convention; no premise about what the printed positive means); **E4-2** — all three pre-declared trigger classes are implemented: as-printed positive; required-field-NR (sheet-scoped: the model may only recover a value from its own sheet, else the trial is dados-insuficientes); factorial-margin (fired by the sheet's declared design — a model that misdeclares the design escapes the trigger, and that escape is itself a logged result). Every firing and answer is logged.
- **E4-3/E4-4 remain grading-side**: the referee (graders' `sexteto`) is unchanged for comparability with the iGPU pair; if malformed cells appear, both parses are reported exactly as done for qwen3:14b.
- **Registered expectations**: the two general-purpose smalls extract in a wide 60–90% band with real wrong-value cells and possible format failures (both-replicate parse failure ⇒ dados-insuficientes, counted); the distill's open question is format compliance under `think=false`; and the architecture claim (H4.3) is expected to hold for all three — |pool − own-sheet truth| decomposes into named extraction/judgment/parsing differences, none arithmetic.
