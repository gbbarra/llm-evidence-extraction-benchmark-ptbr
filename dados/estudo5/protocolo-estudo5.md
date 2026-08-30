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

*Amendments: (none)*
