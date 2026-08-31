# EXTRAI — Pre-registered protocol, Study 5: "GEMMA-SÓ — the minimal-harness frontier"

**Registered 2026-08-30, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). Author's directive: turn the benchmark's best reader into its own orchestrator, correcting stage by stage, toward a 100%-gemma4:12b meta-analysis pipeline.

## 1. Question (frozen)

**Between H1 (the model assembles its own calculator calls — measured failure: signs dropped in arguments, wrong-side diamond $+0.37$) and H2 (code assembles everything — exact by construction), what is the MINIMAL harness under which gemma4:12b orchestrates the meta-analytic arithmetic of its own sheets correctly — if one exists?**

The design constraint that keeps the question meaningful: **harness nets may DETECT and WARN, never substitute a value.** A net that fixes an argument collapses the rung into H2 and kills the claim "the model orchestrated". Every warning and every re-emission is logged verbatim; a call that stands wrong after its warning budget enters the result wrong — measured, not repaired.

## 2. Materials

- **Input sheets**: gemma4:12b's own round-2 extraction sheets (first-parseable), frozen and published at commit `194241e` — orchestration isolated from extraction.
- **Reference ceiling**: the graders' mechanical truth over the same sheets, $-0.52$ $[-0.82, -0.22]$ (the H2 result). Never shown to the model.
- **Functions offered** (the Study-3 calculator, unchanged): `md`, `ic95_md`, `dp_de_ic`, `dp_de_se`, `dp_mudanca_r05`; `pool_dl_md` only in rung G3.
- **Model**: the pinned gemma4:12b build (`4eb23ef187e2`), `think=false`, one call per turn (the mixed-round fix). Native tool-calling APIs are out of scope: the pinned build does not expose the tools template, and swapping builds would change the instrument (possible later arm, by amendment).

## 3. The rungs (each run only after the previous is graded)

- **G0 (baseline, already measured — no re-run)**: free-text CALC with the v3 flow nets. Flow succeeded; content failed (sign loss in argument assembly; $+0.37$).
- **G1 — sign-echo net, detection only.** Free-text CALC as in G0, plus one net: after parsing a call, each numeric argument is compared against every number readable in the study's sheet (fields and numbers inside strings, signs included). If some sheet number matches the argument's magnitude with the OPPOSITE sign, and no sheet number equals the argument as emitted, the harness returns a warning naming the sheet field and asks the model to re-emit (or confirm). Budget: 2 warnings per call, then the call executes as emitted. Measures: **can gemma12 correct its own signs when told where to look?**
- **G2 — structured calls under constrained decoding.** Each call is emitted as a JSON object under an Ollama `format` JSON-Schema (function name from an enum; numeric `argumentos`; a declared `fonte` — the sheet field each argument came from, or `"derivado"`). The same detection-only net now checks each argument against its declared source field (value and sign). Measures: **does schema-constrained emission eliminate format and transcription failures, and does the declared source make sign errors self-correctable?**
- **G3 — the pooling.** After the per-study calls, the model must emit and execute `pool_dl_md` over its own per-study sextets, with the v3 reconciliation net (pool arguments vs the model's own prior results; detection only). This is the measured zero of Study 2 (no model, any size, ever executed the pooling call). The genuine unknown; no directional prediction.
- **G4 (cheap probe, one replicate) — "the mathematician".** By-head computation with the harness answering only "confere/não confere" (max 2 rounds), never showing the correct value. Registered expectation: per-study MDs may pass; CIs fail (measured prior: 0/8 unaided, 0/7 with reasoning mode).

## 4. Scoring (mechanical)

Per rung: call-level accounting (arguments correct/wrong at FIRST emission; corrected/kept after warnings; warnings fired; format failures); per-study MD and CI vs the truth sextets (exact = ±0.01). G3 adds the primary metric of the program: **|pooled diamond − own-sheet mechanical truth|, target exact** — the H2 ceiling reached with the model, not code, doing the assembly. Every transcript archived.

## 5. Pre-registered hypotheses

- **H5.1**: G2's constrained decoding eliminates format failures entirely (every call parses; every argument is a number).
- **H5.2**: sign errors still occur at first emission (the assembly habit), but **≥80% are corrected after one targeted warning** — the Goday A/B precedent: this model judges correctly when asked neutrally and specifically.
- **H5.3**: G3 either executes consistently under schema+net or fails by input inconsistency, not by format. No directional prediction; this rung decides the study.
- **H5.4**: G4's by-head CIs fail even with confere/não-confere feedback.

## 6. Out of scope

Other models; changes to extraction or to the frozen extraction instrument; native tool-calling (build swap); the synthesis stage (returns only if G3 passes, to complete the 100%-gemma12 pipeline with precomputed totals per the Study-3 lesson).

---

## Amendment 1 (2026-08-30, after G1 and the first G2 run; before G2b)

G1 measured 5/7 exact (transcript-verified self-correction under warnings). The first G2 run (4/7, two starved studies, one degraded) is **invalidated as a model measurement and preserved as evidence**: its transcripts show two harness defects doing the damage. **E5-1 — arm-blind source resolution**: the fonte net resolved declared field names against the experimental arm regardless of which arm the argument came from, firing spurious warnings on correct control-arm values and steering the model to corrupt them (harness-induced damage, the instrument-A/B lesson repeated on ourselves). **E5-2 — no arity net**: a five-argument `ic95_md` call received a truncated English Python error and the model perseverated to the turn cap. Fixes, both detection-only: the fonte net goes arm-agnostic (silent if the argument matches the declared field in ANY arm; fires only when it matches none, listing both arms' values); an arity pre-check returns the full Portuguese signature. Observability addition, zero behavioral effect: every turn now streams to the run log as it happens. The re-run under this amendment is **G2b**; the defective G2 record stays archived.

## Amendment 2 (2026-08-30, after the first G3 run; before G3b)

The first G3 run is invalidated as a model measurement and preserved as evidence — both defects are the harness's. **E5-3 — wrong grammar bound**: the schema helper hard-coded the G2 grammar, so G3's constrained decoding still admitted the per-study functions the rung does not offer; the model emitted `dp_de_se` (visibly attempting to recompute study 1 instead of pooling) and the correct G3 grammar (enum `pool_dl_md`/`fim` only) would have made that emission unrepresentable. **E5-4 — meaningless execution instead of guidance**: an off-menu or empty-`sextetos` call was executed as an empty pool, returning a misleading `division by zero`; the model reasonably perseverated against an incoherent harness. Fixes, detection/guidance only: the schema is now bound per rung, and a pooling call without at least two sextets draws a Portuguese warning naming the missing field instead of executing. The re-run is **G3b**; run 1 stays archived.

## Amendment 3 (2026-08-30, after G3b passed): the complete 100%-gemma12 pipeline

G3b answered H5.3 affirmatively (pooling executed in one turn, all seven own sextets faithful, consistent exact), so §6's conditional stage returns: the full pipeline is assembled and run end to end — **every model role is gemma4:12b; the harness only detects, warns, computes on command, and draws**. Stages: (1) per-study orchestration, G2b instruments unchanged (rung label `G2PIPE`, fresh run); (2) pooling, G3b instruments unchanged, over the sextets of stage 1; (3) **synthesis** — a new frozen instrument (`prompts/e5-sintese.txt`): 150–300 words in Portuguese using ONLY the numbers provided, with participant totals PRE-COMPUTED by code (the Study-3 lesson: no mental sums), checked by the mechanical orphan-number scan (report-only); (4) forest plot drawn by deterministic script from stage-1/2 results. Wiring-only harness edits (source dirs and labels become parameters); nets unchanged. Outputs under `dados/estudo5/pipeline/`.

## Amendment 4 (2026-08-30, registered before the run): pipeline v2 — Priority-1 improvements, extraction to result

Author's directive: apply the roadmap's Priority-1 items and repeat the COMPLETE pipeline from fresh extraction to final product, 100\% gemma4:12b, as Study 5's complement. Registered changes, all detection-only (the model corrects itself; the harness never substitutes):

1. **Schema-constrained extraction** (roadmap #2): Stage E re-runs from zero (7×2, the frozen `e3-extracao.txt` prompt VERBATIM) with the sheet's exact field set enforced by constrained decoding — every field present, string-typed and length-bounded, nothing extra representable. The prompt is unchanged; only the decoding grammar is added.
2. **Runtime anti-invention net** (roadmap #1): after each sheet parses, the harness scans every numeric token of the countable fields against the perturbed source text; each value printed nowhere draws ONE question (frozen instrument `prompts/e5-verifica.txt`, article in context): answer the value as printed, or NR. The model's answer is applied as its own correction and fully logged; at most 6 questions per sheet (excess flagged, uncapped list recorded).
3. **Declarable-derivation net** (roadmap #3): the calc stage (rung `CALC2`, prompt `e5-calc2.txt` = the G2b instrument plus one rule) adds an optional `derivacao` field to the call schema; when any argument declares fonte "derivado", the model must state the operation (e.g. "7.1 - 6.8"), and the harness checks — detection-only — that the operands are sheet values and that the declared arithmetic matches the argument sent.
4. Downstream unchanged: pooling (G3b instruments, over CALC2's sextets), totals pre-computed by code, synthesis (`e5-sintese.txt` frozen), forest by code.
5. **Scoring, extraction to result**: cells of the fresh sheets vs the Study-3 amended ruler; per-study and pooled vs the graders' mechanical truth over the SAME fresh sheets; and the sealed unperturbation lens vs the published $-0.24$ $[-0.32, -0.16]$ — the headline: does the improved, self-verifying pipeline still reconstruct the literature?

Outputs: `dados/estudo5/saidas/EXTRA2` (extraction + verification log), `saidas/CALC2`, `saidas/POOL2`, `dados/estudo5/pipeline2/`.

## Amendment 5 (2026-08-30, registered before any G2c run): typed calls

Pipeline v2 sharpened the residual failure class to one shape — **role errors with honest provenance** (Goday's levels passed as means; the study's own MD result passed as an arm mean inside `ic95_md`, producing the author-caught invalid interval $[-9.22, -8.58]$; raw SDs used where the model's own derived SDs existed) — and erratum E5-5 exposed a family of mechanically impossible values that no net refused. Rung **G2c** re-runs the per-study stage under the CALC2 instruments plus, all detection-only:

1. **Argument type system**: each function slot declares the class of sheet field that may feed it (mean-slots: `hba1c_mudanca_media` or a declared final−basal derivation; SD-slots: `hba1c_*_dispersao`/`_dp`, a `dp_*` function result, or an r=0.5 derivation; n-slots: `n_*` fields). A declared source of the wrong class draws a warning naming slot, class and field. Same budget and confirm-by-repeat as all nets.
2. **Coherence nets**: an `ic95_md` result that does not contain the same sexteto's `md`; a negative SD anywhere; a non-integer or $\le 1$ n — each mechanically impossible, each a warning.
3. **Closing-restatement check**: a `fim` differing from the study's last executed `md`/`ic95_md` results draws a warning (transcription is the measured failure surface).
4. **Escalation flag**: any call standing wrong after its budget enters the study's record with `requer_revisao_humana: true`, propagated to the product layer (flag, never endorse — E5-5's rule).
5. **Reported harness complexity**: the record states the active-net count per rung (G0: 1; G1: 2; G2b: 4; G2c: 8) beside accuracy — how much harness the model needs is itself the result.

**Registered prediction**: the type net converts the Goday levels-as-means route into a warned self-correction, making 7/7 per-study exactness reachable for the first time; if the model insists through the budget, the study arrives flagged, not silent. Inputs: the EXTRA2 sheets (unchanged). Outputs: `saidas/CALC2C`, `resultados-CALC2C`.

## Amendment 6 (2026-08-30, registered before the run): two micro-nets, then the FROZEN harness runs v3 from extraction

G2c measured 6/7 + one flagged; its two self-corrected incidents share one root the nets only catch downstream: **CI bounds emitted in swapped order** at the conversion call (Dorans G1; Chen G2c), surfacing later as a negative SD. Two coherence micro-nets close it at the source, both detection-only: (1) `dp_de_ic` with inferior $>$ superior draws an order warning at the call; (2) a negative result from any `dp_*` conversion returns with an attached warning (an SD cannot be negative — check bound order and signs), instead of silently entering the context. **After these two, the harness is declared FROZEN at 10 nets**: further nets require a new, named, measured failure (the roadmap's admission rule; complexity is a reported cost).

**Pipeline v3** then re-runs EVERYTHING (see below); Amendment 7 follows it.

## Amendment 7 (2026-08-30, registered before the run): the code-specialist orchestrator

Author's directive: test whether a code-tuned model of the same family orchestrates better. **Division of labor: extraction stays gemma4:12b's** (the frozen EXTRA3 sheets, unchanged) **and the orchestrator under test becomes `codegemma:latest`** (build pinned at run time), on the SAME frozen 10-net harness, same instruments, same one-call-per-turn protocol — rung `CALC3G`, directly comparable to v3's CALC3 (gemma12: 5 exact, 1 route-divergent, 1 starved). If the per-study stage closes, the pooling runs as `POOLG` under the G3b instruments. Open questions registered rather than predicted: code-tuned models are format-strong by training, but this build is an earlier generation, and the frozen instruments are Portuguese by design — format discipline, instruction language and role semantics are all under test at once; whatever separates its transcript from gemma12's under identical nets is the measurement.

**Addendum (same date, before the CALC3F run) — the same-family coder.** A second orchestrator joins the arm: `xentriom/gemma-4-12B-coder-fable5-composer2.5-v1` (an Ollama mirror of a community GGUF fine-tune of gemma-4-12B specialized for Python/algorithmic coding; unofficial, hobbyist provenance — mirror namespace differs from the Hugging Face author, both recorded with the pinned digest in MODELS.md). This is the scientifically cleaner comparison: the SAME base family and size as the reader, isolating the code-tuning delta. Rung `CALC3F`, identical frozen harness and inputs; `POOLF` if it closes. The three-orchestrator table under one harness — gemma12 base × codegemma (older generation) × gemma4-12B-coder (same base, code-tuned) — is the arm's product.

## Amendment 8 (2026-08-30, registered before the runs): the four cheap arms

All over the frozen 10-net harness and the EXTRA3 sheets, comparable to CALC3/CALC3F. Rules and predictions frozen here.

- **Arm A — replicate orchestration with an agreement rule** (rung `CALC3R2`: a second, identically configured gemma12 run). Rule, truth-free: per study, if both replicates' finals agree (MD and both bounds within $\pm 0.01$) → accepted-concordant; one null → the other stands, flagged \emph{single-source}; both present but different → flagged \emph{discordant} (human). **Registered prediction**: the Goday starvation is stochastic (v2 ran it clean, v3 starved), so at least one of the two replicates closes it — agreement restores completeness at zero doctrinal cost.
- **Arm B — temperature zero** (rungs `CALC3T1`, `CALC3T2`: two greedy-decoding replicates; a run-time sampling option, the instruments untouched). The sharp question: are greedy twins \emph{identical}? If yes, the measured run-to-run weather is sampling noise; if habits persist and twins diverge, the variance is prompt-state-driven. No directional prediction.
- **Arm C — the orchestrator committee** (no new runs: mechanical composition of the archived CALC3 and CALC3F finals). Rule, truth-free: both agree → auto-accept; one null or incoherent → the valid one, flagged single-source; both valid but different → flagged discordant. **Registered prediction** (from the union data): every auto-accepted study is exact — 100\% precision on auto-accepts, zero wrong values passing without a flag.
- **Arm D — the two product flags** (mechanical checker, applied retroactively to the three pipeline pools as demonstration): \emph{missing-study} (a trial with parseable sheets but no pooled row) and \emph{weight-dominance} (any single study above 40\% of the DerSimonian--Laird weight). **Registered expectation**: v3 raises both (Goday absent; Saslow 2023 dominant); the flags would have converted its silent composition distortion into two named warnings.

Outputs: `saidas/CALC3R2·CALC3T1·CALC3T2`, `resultados-bracos-baratos.json`, analysis script `scripts/estudo5/bracos-baratos.py`. from fresh extraction under the frozen instruments: Stage E from zero (schema-constrained, prompt verbatim, runtime anti-invention net) → typed per-study orchestration (rung `CALC3` = the full G2c net set + the two micro-nets, `e5-calc2.txt` unchanged) → pooling (G3b instruments) → totals by code → synthesis → product with the flag-never-endorse rules. Scoring as in Amendment 4 (cells · own-sheet truth · sealed lens vs $-0.24$). A third fresh extraction also yields the first three-round extraction-stability datum. Outputs: `saidas/EXTRA3`, `saidas/CALC3`, `saidas/POOL3`, `dados/estudo5/pipeline3/`. Genuine model behavior already visible through the noise, logged for the record: **over-conversion** — the model derived the Goday change-SD correctly via r=0.5 and then fed its own result into a further conversion (`dp_de_se(0.96, 45)`), a conceptual chaining habit, not transcription.
