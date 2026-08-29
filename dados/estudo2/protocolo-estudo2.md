# EXTRAI — Pre-registered protocol, Study 2: "the arithmetic"

**Registered 2026-08-28, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). Design sketched in the [roadmap](../../roadmap.md) and proposed by the author ("what if we hand the models the formulas as a plugin, or code they can call?").

> *English translation of the pre-registered protocol (originally written in Brazilian Portuguese; original wording preserved in git history).*

## 1. Question

Study 1 showed the four models extract evidence almost without error (624 cells, 1 wrong) but synthesize "by eye" — describing morbidity as favorable where the pooled meta-analysis says not significant. Study 2 asks: **can they turn their own extractions into an actual meta-analysis — risk ratio, confidence interval, pooling?** And: how much of the failure is conceptual (not knowing what to compute) versus arithmetic (not having a calculator)?

## 2. Design: two arms per model

- **Arm A — by head.** The model receives the per-study 2×2 tables/statistics (extracted by ITSELF in Study 1, replicate 1) and computes unaided. Explicit instruction: *"if you cannot compute with confidence, write NAO-CALCULAVEL"* ("NOT-COMPUTABLE") — measuring arithmetic honesty is a primary objective, not an accessory.
- **Arm B — with a calculator (uniform text protocol).** Same input, but the model may write lines `CALC: <function>(<args>)`; the harness intercepts, computes in Python and returns `RESULTADO: <value>` into the context, up to 20 calls per run. Exposed functions (signatures in the prompt): `rr(ev_gdft, n_gdft, ev_ctrl, n_ctrl)`, `ic95_rr(...)`, `md(m1, sd1, n1, m2, sd2, n2)`, `ic95_md(...)`, `pool_rr_mh(list of [ev1,n1,ev2,n2])`, `pool_md_iv(list)`, `pool_dl(list)` (DerSimonian-Laird random effects).
- The text protocol (rather than native tool calling) is the main arm because it is the same mechanism for all four families; Ollama's native tool calling remains an optional exploratory arm, reported separately if run.

## 3. Materials and outcomes

Input per model: ITS OWN Study-1 T1-r1 extractions (14 studies), reduced by the harness to the relevant cells per outcome (no article texts). Outcomes computed:

| Outcome | Type | Studies with data in the anchor |
|---|---|---|
| Overall morbidity | per-study RR + pooled | 5 (MA table 5) |
| Mortality | per-study RR + pooled | 3 (table 6) |
| Postoperative ileus | per-study RR + pooled | 3 (table 11) |
| Time to flatus / oral diet | per-study MD | tables 8–9 |

**Triple answer key**, fully mechanical: (a) the arithmetic truth (recomputed in Python from the official answer key's cells); (b) the anchor's published values (RR/CI/weights of tables 5–11) — which also audits the meta-analysis's own statistics, again; (c) for arm B, the literal log of CALC calls and their returns (did the model use the right tool with the right numbers?).

## 4. Models, replicates and queue

The 4 veterans under Study 1's frozen configurations. Per model: arm A ×2 replicates + arm B ×2 replicates, one run per task family (per-study RRs; MDs; pooling) — an estimated ~64 short runs (small input, no article). Exploratory arm: qwen3:14b with thinking enabled in arm A (the "mathematical vocation" FIEL's Series 1 never tested), 1 replicate, reported separately.

## 5. Scoring (mechanical, no language judge)

Per computed quantity: **exact** (|Δ| ≤ 0.01 for RR/CI at 2 decimals; ≤ 0.1 for MD) · **right-direction** (RR on the correct side of 1 / MD on the correct side of 0) · **wrong** · **NOT-COMPUTABLE declared** (does not count against in arm A; counts as refusal in B) · **fabricated** (a statistic-shaped number matching no valid computation over the inputs — the worst category, counted separately). In arm B, additionally: correct calls / wrong-argument calls / ignored results.

## 6. Pre-registered hypotheses

- **H2.1 (the calculator pays):** exact accuracy in arm B ≥ 2× arm A, in all 4 models.
- **H2.2 (arm-A anatomy):** direction ≥ 80%; simple RR ≈ half; 95% CI ≈ zero.
- **H2.3 (pooling is a different muscle):** even in arm B, pooling lands below per-study RR — orchestrating several calls and combining is planning, not arithmetic.
- **H2.4 (honesty):** in arm A, NOT-COMPUTABLE concentrates on CIs and pooling; fabrication < 5% of quantities in all 4 models.
- **H2.5 (its own ranking):** the arithmetic ranking does NOT repeat the extraction ranking (12b=26b>27B>14b); directional prediction: the qwens rise in arm A (the family with the math reputation).
- **H2.6 (auditing the anchor, again):** ≥ 1 divergence between the arithmetic truth and the MA's published value (tables 5–11 inherit the documented extraction errors — e.g., Yoon's morbidity RR with swapped arms).

## 7. Out of scope

Meta-regression, heterogeneity beyond pool_dl's τ²/I², GRADE, and continuity corrections for zero cells (recorded as a limitation if they arise). No perturbation in this study: the inputs are the model's own extractions, already audited in Study 1.

---

*Amendments: (none)*
