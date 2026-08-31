# EXTRAI — Study 5 evaluation (grading record): "GEMMA-SÓ, the minimal-harness frontier"

Closed 2026-08-30, same day as the runs. Protocol with three dated amendments ([`protocolo-estudo5.md`](protocolo-estudo5.md)); frozen prompts in [`prompts/`](prompts/); every rung's full turn-by-turn transcripts — including the two invalidated runs — under [`saidas/`](saidas/) and rendered readably in `transcricoes-*.md`; the end-to-end pipeline record in [`pipeline/`](pipeline/).

**Who did what**: gemma4:12b (the pinned build, `think=false`) emitted every calculator call, every re-emission after a warning, the pooling call, and the final narrative; the harness executed functions on command, detected and warned (never substituting a value), pre-computed participant totals, and drew the forest; the adjudicator (Claude, under the author's supervision) graded against the graders' mechanical truths — and logs **four harness errata of his own** (§6), each proven by transcript.

## 1. The question (frozen before any run)

**Between H1 (the model assembles its own calls — measured failure: signs dropped, wrong-side diamond) and H2 (code assembles everything — exact by construction), what is the MINIMAL harness under which gemma4:12b orchestrates the meta-analytic arithmetic of its own sheets correctly — if one exists?**

## 2. How it was measured

A ladder of rungs over the model's own round-2 extraction sheets (frozen at `194241e`; orchestration isolated from extraction), under one inviolable rule: **nets may detect and warn, never substitute** — a harness that fixes an argument collapses into H2 and kills the claim. Ceiling: the graders' mechanical truth over the same sheets ($-0.52$ $[-0.82, -0.22]$), never shown to the model. Each rung ran only after the previous was graded; every warning, re-emission and perseveration is archived verbatim.

## 3. The answer

**A minimal harness exists, and it is small.** Schema-constrained emission (Ollama `format`, per-rung grammar), one call per turn, and four detection-only nets — sign-echo, declared-source check, arity with the Portuguese signature, and menu guidance — are enough for gemma4:12b to: assemble per-study calls at 5/7 exactness with zero format failures; **execute the DerSimonian–Laird pooling over its own seven sextets, faithfully and digit-consistently, twice in a row** — the call no model of any size had ever executed in this benchmark; and close the pipeline with a narrative synthesis containing **zero invented numbers**. What the minimal harness does *not* fix has a name (§7).

## 4. The rungs

| Rung | Harness | Result |
|---|---|---|
| G0 (prior) | v3 flow nets, free text | flow OK, signs dropped, wrong-side diamond (+0.37) — the baseline failure |
| **G1** | + sign-echo net (detection-only) | **5/7 exact**, 5.2 min; the Dorans transcript shows the full anatomy: bounds swapped → negative SD → warning → one stubborn repeat → corrected → exact |
| G2 (run 1) | + schema + declared sources | **invalidated as a model measurement** — the harness's arm-blind source net fired on correct control-arm values and steered the model to corrupt them (E5-1); no arity net (E5-2). Archived as evidence of harness-induced damage |
| **G2b** | Amendment-1 fixes | **5/7 exact**, 6.7 min, zero format failures, zero spurious warnings; the two misses are the same two, same classes, as G1 |
| G3 (run 1) | pooling | **invalidated** — the schema helper bound the G2 grammar (off-menu calls representable, E5-3) and an empty pool executed as a misleading `division by zero` (E5-4). Archived |
| **G3b** | Amendment-2 fixes | **PASSED, one turn**: `pool_dl_md` over all seven own sextets, first emission faithful, aggregate closed consistent exact ($-0.50$ $[-0.74, -0.26]$) |
| **Pipeline** (Amendment 3) | all stages, 100% gemma12 | 7/7 studies closed with **zero warnings needed**; pooling consistent again ($-0.46$ $[-0.67, -0.26]$, digit-exact vs its own sextets); 493 participants pre-computed by code; synthesis with **zero orphan numbers**, correctly singling out Wang 2018 as the only CI crossing zero; forest drawn by code |

## 5. Pre-registered hypotheses — verdicts

| Hypothesis | Verdict |
|---|---|
| **H5.1** — schema eliminates format failures | **CONFIRMED**: zero format failures in G2b, G3b and the pipeline (G1's free text had needed format warnings) |
| **H5.2** — sign errors persist at first emission but ≥80% correct after one targeted warning | **MECHANISM CONFIRMED, QUANTIFIER UNDERPOWERED**: the one genuine sign/assembly episode (Dorans G1) was corrected after warnings and ended exact (1/1); the pipeline run needed zero warnings, leaving no sample to quantify the ≥80% |
| **H5.3** — the pooling executes consistently or fails by input, not format | **CONFIRMED, AFFIRMATIVE — the study's headline**: executed consistently twice (G3b and pipeline), faithful sextets, exact closure both times |
| **H5.4** — by-head CIs fail even with confere/não-confere | **NOT RUN**: the author's directive to assemble the full pipeline superseded the G4 probe; it remains available |

## 6. Harness errata (the rite applied to ourselves; all transcript-proven)

**E5-1** arm-blind source resolution — fired on correct control-arm values and actively steered the model to corrupt them: the instrument-A/B lesson of Study 4 reproduced on our own harness. **E5-2** missing arity net — a five-argument call perseverated against a truncated English Python error. **E5-3** wrong grammar bound in G3 — constrained decoding admitted functions the rung does not offer. **E5-4** meaningless execution instead of guidance — an empty pool returned `division by zero` to a model that had not called the pool. Three amendments in one study, each registered before its re-run, each defective run preserved. The meta-result is the thesis of the papers, measured live: **the harness is part of the system under test, and a benchmark that does not audit its own instruments will bill the model for the harness's sins.**

## 7. The 12B's remaining frontiers (named, with evidence)

- **Derived values**: when the sheet forces derivation (Goday: only levels printed), the model derives the *dispersions* correctly (both change-SDs via r=0.5 in the pipeline run) but persists in passing the final **levels** as means ($5.3, 7.1$ → $-1.8$, vs the change-difference $-1.9$) — a route error the detection nets cannot see, because there is no sheet field to echo.
- **Run-to-run habit variability**: the over-conversion habit (feeding its own correct r=0.5 result into `dp_de_se`) appeared in G2b's Goday and vanished in the pipeline's — same model, same sheet, same instruments. Orchestration reliability at 12B is stochastic at the margins; replicates remain mandatory.
- **A consistent private route**: Saslow 2023 came out $-0.18$ $[-0.22, -0.14]$ in every rung — reproducibly different from the graders' route, never unstable. Consistency is not correctness (the Study-4 lesson, again).

## 8. Pipeline v2 (Amendment 4) — extraction to result, Priority-1 nets, measured

The author ordered the roadmap's Priority-1 items applied and the whole pipeline repeated from FRESH extraction. Results ([`pipeline2/`](pipeline2/), transcripts in `saidas/EXTRA2·CALC2·POOL2`):

- **The headline — the full circle closes**: fresh sheets (schema-constrained, prompt verbatim) → the model's own orchestration → pooling **consistent for the third consecutive time** ($-0.51$ $[-0.75, -0.26]$, digit-exact vs its own sextets) → and the sealed unperturbation lens lands **on the published value to the hundredth: $-0.24$ $[-0.33, -0.16]$ vs $-0.24$ $[-0.32, -0.16]$**, $I^2$ 7.1\% vs 6\%. A 12B model plus warn-only code, end to end, reconstructs the literature.
- **Pipeline vs mechanical truth over the same fresh sheets**: $\Delta$MD 0.01 ($-0.51$ vs $-0.52$) — near-exact with the model, not code, assembling every call.
- **Anti-invention net (roadmap #1): armed, zero triggers** — none of gemma12's fresh numbers is absent from the source text. The net exists for the invention class measured in other models (llama3.1:8b); on this extractor there was nothing to catch, which is itself the measurement.
- **Derivation net (roadmap #3): never engaged — and that is the finding.** The model dodged it honestly: on Goday it declared the TRUE source fields (`hba1c_final_media`) of values placed in the WRONG role (levels passed as means; $-1.8$ persists, plus one garbage closing CI $[-9.22, -8.58]$ that never touched the pool, which uses the executed call's sextet). Provenance-checking nets verify **where a value came from, not what role it may play** — the precise next net is a ROLE check: an m-slot fed from a `*_final_media` field draws a warning. Registered in the roadmap.
- Cells of the fresh sheets: 184/206 (89.3\%) pre-adjudication — run-to-run route variation, zero inventions; extraction remains the quality bound.
- **E5-5 — caught by the AUTHOR reading the figure** (the human-in-the-loop catch the design invites): Goday's closing interval $[-9.22, -8.58]$ does not contain its own MD ($-1.8$) — the model had passed its previous RESULT as one arm's mean inside `ic95_md` (declared provenance honest: "resultado-anterior"; role wrong again) — and the product layer (forest and synthesis DADOS) endorsed the reported final as-is: the forest plotted it and the synthesis cited it, with the orphan scan blind to provided garbage. Three successor nets registered: a **coherence check** (an interval must contain its own MD — mechanically detectable, warning at the call and at the product); the already-registered **role check**; and the rule that the **product layer flags incoherent reported values, never endorses them** (implemented; the corrected forest marks Goday's interval as invalid instead of plotting it). The pool was never touched (it uses executed-call sextets).

## 9. Rung G2c (Amendment 5) — typed calls, measured

Eight detection-only nets (type system by slot class; coherence: interval-contains-MD, positive SD, integer n; closing-restatement check; escalation flag), over the same EXTRA2 sheets. Result: **6/7 exact — the program's best — in 8.0 min**, and the seventh arrived FLAGGED, not silent, on the escalation net's maiden run.

- **The registered prediction paid where it mattered**: the type net fired on Goday's levels-as-means call, the model re-derived, and **Goday closed on the correct route for the first time in the whole program — $-1.9$ $[-2.3, -1.5]$, digit-exact against the graders' truth.**
- **Chen, the flagged seventh, is the flag working as designed**: the model swapped and unsigned the control CI's bounds (producing SD $-1.27$; the negative-SD net caught it at the `md` call and the model corrected to the RIGHT magnitude), then committed a pure copy error in its closing (`ic95 [0.08, 0.08]`), which the restatement net caught and the model fixed. Its final ($[-0.94, 0.08]$) differs from the graders' truth by a **dispersion-route divergence on the fresh sheet** — internally correct arithmetic, defensible route, flagged for exactly the human judgment it deserves.
- One borderline source warning (Chen's experimental CI) was absorbed by confirm-by-repeat with no damage — the false-alarm cost of the eighth net, measured at one extra turn.
- Harness complexity, as now reported by doctrine: G0 1 net · G1 2 · G2b 4 · **G2c 8** — accuracy 5/7 → 5/7 → **6/7 + 1 flagged**.

## 10. Pipeline v3 (Amendment 6, frozen harness) — the honest ceiling, measured

Everything from fresh extraction under the frozen 10-net harness. The registered 7/7 prediction was **REFUTED — in the instructive direction**:

- **The stable, load-bearing result got its third confirmation**: the sealed lens over the fresh sheets landed on the published value AGAIN — $-0.24$ $[-0.33, -0.16]$ — making it **three independent fresh extractions, three lenses on $-0.24$** (round 2, v2, v3). Reading, the one stage the model owns outright, is reproducibly anchor-faithful. Extraction cells 85.4\% pre-adjudication (fresh-round route variation).
- **The over-conversion habit returned and beat the cap**: on Goday the model again derived the change-SD correctly (0.96, r=0.5) and then insisted on re-converting its own result through `dp_de_se`; the type and derivation nets correctly refused every wrong move, seven times — **detection can refuse, it cannot teach** — and the study starved at 16 turns, closing null and leaving the pool. Per-study finals: 5 exact, 1 route-divergent (Chen, as in G2c), 1 null.
- **The pooling was faithful and the aggregate is distorted anyway**: the model pooled its six surviving sextets consistently (TRUE, digit-exact) — and the product is $-0.19$ $[-0.23, -0.16]$, $I^2$ 0\%, because with Goday absent, heterogeneity collapses and Saslow 2023's tiny stored dispersions (its consistent private route) take dominant weight. **Local honesty at every link does not compose into global sanity**: a chain of correct refusals produced a faithful pool of a distorted composition. Two mechanically detectable product-layer flags are the registered successors (roadmap): a **missing-study flag** (a trial with sheets but no pooled row) and a **weight-dominance flag** (any single study above a declared share of the pooled weight).
- The anti-invention net's four firings were all the corpus's **gap \#1 live** (digits absent because the text spells the numbers out — "ninety-two"); the model confirmed each value at the cost of four turns, zero damage.

**What the three pipeline runs together establish**: the per-study orchestration layer oscillates with the model's stochastic habits (5/7 → 6/7+flag → 5+1+null under an identical frozen harness), while the extraction-level lens does not move ($-0.24$, three times). The division of labor's asymmetry is now measured from both sides: reading is reliable and orchestration is weather — which is precisely why the deterministic-downstream architecture of Study 4 remains the production recommendation, and the GEMMA-SÓ line is the measured map of what a 12B can and cannot yet own.

## 11. Standing

The author's directive — *turn the best reader into an orchestrator, correcting stage by stage, toward a 100%-gemma12 meta-analysis pipeline* — is fulfilled and archived: reader (round-2 sheets, 92.2% cells), orchestrator (this study), synthesist (zero inventions), with code doing only what code should (execute on command, count, draw, verify). Editorial decision pending: this record becomes Paper 3, or the second half of Paper 2.
