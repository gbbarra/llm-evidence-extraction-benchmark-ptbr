# EXTRAI — Pre-registered protocol, Study 6: "the replication, in detail" (Paper 4's record)

**Registered 2026-08-31, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). Author's directive: reproduce in detail the replication of BOTH anchor meta-analyses under the frozen architecture, as Paper 4.

## 1. Question (frozen)

**Does the frozen architecture — the measured local reader (gemma4:12b) plus deterministic code — replicate both anchor meta-analyses in detail: every per-study effect, every pooled estimate, every outcome family, with ALL residue decomposed into named categories — including the category no replication framework offers, "the published value is the one that is wrong"?**

## 2. Materials (all existing, all validated, nothing new invented for this study)

- **Anchor 1 (GDFT)**: the goal-directed fluid therapy meta-analysis and its 14 primary RCTs; sealed perturbations (`dados/estudo1/perturbacoes-*.json`); the two-layer source-verified key (`gabarito-oficial.json`); the public 15-entry anchor errata file. Outcomes and field maps frozen from Study 2's harness: overall morbidity RR (table 5), mortality RR (table 6), postoperative ileus RR (table 11), time-to-flatus MD (table 8), time-to-oral-diet MD (table 9).
- **Anchor 2 (low-carbohydrate)**: the HbA1c meta-analysis, its 7 RCTs and Study 3/4/5 instruments, unchanged.
- **Engine**: the validated functions only — `rr`, `ic95_rr`, `pool_rr_mh`, `pool_dl`, `pool_md_iv` (Study 2; test case reproduces the anchor's RR 0.573 [0.372–0.884]; its pooled morbidity reproduces digit-for-digit under DL) and the Study-3/4 continuous set. **No model touches a number downstream of its sheet.**
- **Reader**: gemma4:12b, pinned build, frozen Study-1 extraction instrument verbatim (context 16,384; reasoning off).

## 3. Design

1. **MA-1, fresh from zero**: gemma12 re-extracts all 14 perturbed primaries (2 replicates, first-parseable) under the frozen E1 instrument. The archived Study-1 sheets (100\% graded cells) become the **stability arm** — the benchmark's fourth extraction-stability datum, this time on the first corpus.
2. **Deterministic downstream, no triggers**: the dichotomous route selector maps the sheet's event/n fields per outcome (Study-2's frozen field map); a study missing a required cell leaves that outcome's pool, **counted, never silent** (no judgment-trigger classes exist for 2×2 counts; this is declared, not discovered). Per-study RR + 95\% CI per dichotomous outcome; MD for the two continuous outcomes; pools under **both** Mantel–Haenszel and DerSimonian–Laird.
3. **The sealed lens**: perturbations reversed by the graders (the models never see the seal), then the comparison with the published tables 5–11 — with the pooled comparison made under DL, the method the published numbers actually instantiate (anchor erratum \#15: right numbers, wrong caption).
4. **Erratum-aware comparison, the study's signature**: every cell of the side-by-side tables is classified into frozen categories:
   - **reproduz** (per-study RR/CI within $\pm 0.01$; MD within $\pm 0.1$ — Study 2's pre-registered tolerances);
   - **difere-por-errata-da-âncora-\#N** — the difference is explained by a documented, source-confirmed error of the published meta-analysis (eligible entries fixed here: \#1 Yoon arms swapped; \#9 Sun's oral-diet conversion contradicting its source; \#13 the systematic analyzed-as-randomized ns; \#12's unsupported flatus/fluid cells, which are excluded as in Study 1);
   - **rota-do-modelo** (a documented alternative literal reading);
   - **erro-do-modelo**;
   - **fonte-indisponível** (figure/supplement-only cells, excluded as in Study 1).
5. **MA-2, one formal run for symmetry**: the Study-5 pipeline-v2 procedure re-executed once under this protocol's label, consolidating the three measured lenses into Paper 4's table.

## 4. Pre-registered hypotheses

- **H6.1**: gemma12's fresh MA-1 extraction stays in its measured band — $\ge 90\%$ graded cells, zero inventions, zero attributable recitations.
- **H6.2 (the replication claim)**: after the sealed reversal, every per-study and pooled difference from the published tables decomposes into the frozen categories with **zero unexplained residue** — and at least the Yoon rows and the analyzed-vs-randomized ns land in *difere-por-errata-da-âncora*, making this a replication that grades the original.
- **H6.3 (stability)**: fresh vs archived gemma12 sheets agree on $\ge 95\%$ of graded cells.
- **H6.4**: MA-2's lens lands beside $-0.24$ $[-0.32, -0.16]$ a fourth time.

## 5. Outputs

`dados/estudo6/saidas/gemma12/extracao/` (fresh runs) · `resultados-por-desfecho.json` · `comparacao-detalhada.md` (the full side-by-side tables, every cell categorized) · paired forest plots per outcome (ours vs published, drawn by code) · `avaliacao-estudo6.md` · run log with the seals' SHA-256.

## 6. Out of scope

Other models (the measured reader only); audit stages; orchestration (Paper 3 closed it; all arithmetic here is code); committees; any change to instruments, seals or keys.

---

*Amendments: (none)*
