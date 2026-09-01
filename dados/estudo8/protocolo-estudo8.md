# EXTRAI — Pre-registered protocol, Study 8: the English-instrument replication campaign (one article)

**Registered 2026-09-01, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md).

**Author's directive (verbatim intent)**: organize the logic of ONE complete article from what is genuinely relevant across Studies 1–7; repeat the whole logical chain with the **English instruments** — no Portuguese anywhere in any analysis — to **exclude instruction language as a driver of any result** in models trained primarily on English; reproduce the perturbation reading proof, the human key on trial, the adjudication rite, and the between-model comparison; reorder the chain into an ascending line of scientific investigation; register everything first; process everything in sequence.

## 1. Question (frozen)

**How well do local, integrated-GPU language models CORRECT and CREATE meta-analyses when benchmarked against published ones — measured end to end (reading → arithmetic → assembly → orchestration → deployment) under English instruments — and does the instruction-language change move any result of the Portuguese-instrument record?**

## 2. Design principles (frozen)

- **Only the instruction language changes.** Corpora (the same English primary texts), the sealed perturbation maps, the two-layer source-verified keys (as corrected 2026-08-31), the deterministic engines, the mechanical graders and the adjudication rite are **reused identical**. This isolates the language variable: each phase's result is compared 1:1 with its Portuguese-instrument counterpart, and the difference is the ablation measurement.
- **Instruments**: the frozen English library (`dados/instruments-en/`), plus the instrument work this protocol itself commissions (§4) — an **English harness build** (the Study-5 ten-net dialogue ported by the library's correspondence tables: RESULT/WARNING/END markers, English warning texts, same net logic verbatim) and **English trigger questions** (the three declared classes, E4-1-neutral wording). Built and committed before the phases that use them; the Portuguese originals remain untouched as the record of Studies 1–6.
- **Cast**: the five-model iGPU comparison cast of Study 4 round 2 — `gemma4:12b`, `qwen3:14b`, `llama3.1:8b`, `qwen3.5:9b`, `deepseek-r1:14b` — pinned builds per `MODELS.md`, reasoning off where the instrument says so; phases P4 runs the measured best reader only. No cloud API anywhere.
- **Doctrine unchanged**: perturbation reading proof (models live in the perturbed world; graders hold the seal); nets detect and warn, never substitute; quote before verdict; adjudicator errata public; nothing retroactive.

## 3. Phases, in the article's ascending order (all pre-registered here; run strictly in sequence)

**P1 — READ (the Study-1 replication, multi-model).** All five models extract the 14 perturbed GDFT primaries (2 replicates, EN T1 sheet). Graded against the corrected two-layer key; the key remains on trial (new discrepancies follow the rite and can extend the anchor's errata file). Deliverables: cell scores, replicate stability, recitation check, the model ranking, adjudication record.
- **H8.1**: gemma12 stays in its measured band (≥95% cells, zero attributable recitations, omission-dominant failures); the PT ranking is preserved (gemma12 top; llama8's invention class and qwen35/deepseek14 behavior classes recur or their absence is a named finding).

**P2 — CALCULATE (the Study-2 replication).** Each model, over its OWN P1 sheets: mean differences, risk ratios and pools, arm A (unaided) vs arm B (text-protocol calculator), EN prompts.
- **H8.2**: unaided arithmetic fails as before (interval error rates at the PT order of magnitude); the calculator arm reproduces every value its own sheets support — language-independent.

**P3 — CREATE (the Study-4/6 replication: the deterministic architecture builds both meta-analyses).** (a) The validated engines run over each model's P1 sheets → MA-1 per-study effects, MH+DL pools, sealed lens, and the **erratum-aware five-category comparison** with the published tables (the CORRECTION exhibit: the replication grades the original, errata #1–#17 aware). (b) All five models freshly extract the 7 perturbed MA-2 primaries (EN sheet, 2 replicates); engine + lens → five diamonds vs the published −0.24 (the CREATION exhibit and the model-comparison headline). Judgment triggers: the three declared classes, EN wording, logged.
- **H8.3**: gemma12's MA-1 pools reproduce under DL (±0.01) and its MA-2 lens lands beside −0.24; among the five, only gemma12 reaches the published diamond; zero unexplained residue in the category system.

**P4 — ORCHESTRATE (the Study-5 distillation, English harness build).** gemma12 only, over its own P3(b) sheets: typed calls under the full frozen net set (EN port), G3b pooling, product checks, synthesis with orphan check — one formal pipeline run, extraction to result.
- **H8.4**: the harness behaviors reproduce in English — warnings resolved by confirm-or-correct, pooling digit-consistent with its own sextets, flags never substitute; the PT record's phenomena (orchestration weather; warn-only ceiling) recur at their measured size or their absence is a named finding.

**P5 — DEPLOY (already measured; incorporated, not rerun).** Study 7 IS the campaign's deployment phase and already ran under English instruments: clean texts, no key, the three-configuration detection comparison (silent / sheet-nets / conversational harness), errata panel 7/7. Its record enters the article as the closing phase, with its own scoping clause.

**The ablation verdict (cross-phase).**
- **H8.5**: per-phase deltas between the English-instrument results and the Portuguese-instrument record stay within replicate-level variance — the conclusion "instruction language did not drive the results" — and any phase exceeding it becomes a named finding, not an embarrassment.

## 4. Instrument work commissioned by this protocol (built and committed BEFORE the phases that use them)

1. **English harness build**: port of the Study-5/2/3 model-facing dialogue (CALC markers, RESULT/WARNING, net warning texts, END) per the library's correspondence tables — new files under `scripts/estudo8/`, net logic verbatim; the PT harness stays archived.
2. **English trigger questions** (three declared classes, neutral wording per erratum E4-1).
3. Phase runners (adaptations of the archived queue runners; resume-safe; sequential background queue with logs and completion notifications).

## 5. Outputs

`dados/estudo8/` — per-phase raw outputs (`saidas/<fase>/<modelo>/`), gradings, adjudication records, per-phase evaluation pages, the PT-vs-EN ablation table, figures (rankings, paired forests, the deployment table), run logs. The single article draws exclusively from this study's record plus Study 7's.

## 6. Compute budget (declared)

≈ 240 model calls across P1–P4 (P1 ≈ 140; P2 ≈ 30 multi-turn; P3b ≈ 70; P4 ≈ 25 turns), estimated 14–18 h of sequential machine time on the pinned iGPU builds; resume-safe throughout; the queue survives interruptions.

## 7. Out of scope

New anchors; new models beyond the cast; any change to seals, keys, corpora or the frozen category system; retroactive edits to the Portuguese record; reading-proof claims outside the perturbed phases.

---

*Amendments: (none)*
