# Harness roadmap — every improvement tied to a measured failure

The prioritized instrument backlog distilled from Studies 1–5. Rule of admission: an improvement enters this list only if it targets a **named, measured failure** with public evidence; anything else is decoration. Standing design law, inherited from Study 5's protocol: **nets detect and warn, never substitute a value** — whatever must be fixed automatically belongs explicitly to the deterministic code side, not to a net. Items are executed forward only (dated amendments before the runs they govern), never retroactively.

## Priority 1 — the three that pay most

| # | Improvement | Measured failure it targets | Evidence |
|---|---|---|---|
| 1 | **Runtime anti-invention net at extraction**: Stage E has the source text in hand; after the sheet is filled, the harness scans every written number and asks one question per value that appears nowhere in the text ("o valor X não aparece no artigo; confirme ou corrija"). Detection-only; the model corrects or confirms. | The benchmark's most dangerous class: outright inventions (llama3.1:8b's finals/changes printed nowhere) and computed-instead-of-read values (qwen3:14b's CI half-widths; Goday's self-derived changes) | [Round-2 adjudications](dados/estudo4/rodada2/correcao/adjudicacoes.json) |
| 2 | **Schema-constrained extraction** (Ollama `format` also at Stage E): numeric fields typed as numbers, text fields bounded. | Kills by construction: chain-of-thought written into a form field (qwen3.5:9b), `±`-prefixed values that break parsers, malformed dispersion cells — and with well-formed sheets, the engine/grader parser divergence (E4-4) loses its object | [Round-2 record](dados/estudo4/rodada2/avaliacao-rodada2.md) · [Study-5 G2b](dados/estudo5/avaliacao-estudo5.md) |
| 3 | **Declarable-derivation net**: when an argument's declared source is "derivado", the model declares the operation and operands (`final − basal` of which fields); the harness checks the arithmetic of the declaration itself and warns on mismatch. **Measured outcome (pipeline v2): never engaged — the model declared the TRUE source fields of values placed in the WRONG role.** Successor net registered: a **role check** — an m-slot fed from a `*_final_media`/`*_basal_media` field draws a warning (provenance nets verify origin, not role). | The last measured per-study frontier: levels-passed-as-changes on Goday ($-1.8$ vs $-1.9$), invisible to provenance checks because the provenance is honest | [Study-5 evaluation §8](dados/estudo5/avaliacao-estudo5.md) |

**Successors from pipeline v2's measured outcomes (author-caught erratum E5-5)**: a **coherence net** — an interval that does not contain its own MD is mechanically impossible and draws a warning at the call and at the closing answer; and the **product rule** — the assembly layer (forest, synthesis data) flags incoherent reported values, never endorses them (implemented in pipeline v2's corrected product).

## Priority 2 — structural guards

4. **Unit field + mixed-unit refusal**: a mandatory `unidade` per numeric block on the sheet; the engine warns and counts (never silently converts) when a pool would mix units. — Targets the mmol/mol chimera that wrecked Thomsen's row for two models ([adjudications](dados/estudo4/rodada2/correcao/adjudicacoes.json)).
5. **Double-replicate orchestration with agreement check** (as extraction already does): divergence between replicate diamonds becomes a flag. — Targets the stochastic habits: over-conversion present in G2b's Goday, absent in the pipeline's, same model, same sheet ([Study-5 §7](dados/estudo5/avaliacao-estudo5.md)).
6. **Grader-side debts**: one shared bounds/route parser for engine and graders (E4-4); the Wang printed-positive-is-drop convention scoped to drop-labeled fields (E4-3). — Both quantified in the [round-2 record](dados/estudo4/rodada2/avaliacao-rodada2.md).

## Priority 3 — product quality

7. **Structured claims block in the synthesis**: alongside the prose, a typed JSON of every number cited — the orphan scan becomes an exact reconciliation, and prose artifacts (a stray `$I^2$`) disappear via typing.
8. **Per-study weights and a prediction interval in the forest**: the DL pool already computes the weights; at $I^2$ 91\% a prediction interval is standard meta-analytic practice — one new function, validated at the startup gate like all others.
9. **Corpus-instrument backlog** (registered since Study 3; execute before any new corpus): title/byline kept (two models confabulated authorship); perturbation operator covering number words, visible-addend totals, twin tables, rounded prose restatements; the `estudo` field graded.

## The gate that ranks above everything

**Generalization is not a property until measured**: before trusting any of this outside the current domain, run the pre-registered frozen-engine test on a new anchor in a different area (the methylene-blue meta-analysis is staged: dichotomous outcomes, which also exercises the built-but-untested RR/Mantel–Haenszel half of the engine). Seal, extract, gate, compare — the harness makes that cheap.

---

*Provenance: distilled 2026-08-30 from the measured records. Companion documents: [RECOMMENDATIONS.md](RECOMMENDATIONS.md) (what to trust today) · the question ledger ([agenda-bracos.md](dados/estudo3/agenda-bracos.md)) · the five study protocols with their dated amendments.*
