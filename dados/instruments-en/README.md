# English instrument library

**Created 2026-08-31 by the author's directive: the benchmark's working language switches to English for everything from this date forward — instruments passed to models, reports, and records.**

## Policy (read before using anything here)

- The Portuguese instruments under `dados/estudo{1,2,3,5}/prompts/` are the **frozen instruments of Studies 1–6** and remain untouched: they are the record of what actually ran. Nothing here is retroactive.
- This directory is the **forward library**: any protocol pre-registered after 2026-08-31 freezes its instruments from these files (copying them into its own record at freeze time, as always).
- Each file is a **precise translation** of its Portuguese original — same rules, same ordering, same constraints, same markers — with all model-facing tokens (JSON keys, calculator function names, verdict vocabulary, placeholders) translated per the tables below. The one deliberate semantic change: synthesis tasks now ask for English text instead of Portuguese (a declared design change, not a translation artifact).
- Papers 1–3 describe the Portuguese-instrument design ("Instructions are Portuguese-only by design; instruction-language effects are future work"). The language switch is the future work beginning; results measured under the two instrument languages are **not directly comparable** unless a study runs both arms on the same corpus and seals.
- The archived harness code (Studies 2, 3, 5, 6) keeps its Portuguese model-facing strings — it is the record. An English harness build is cut together with the next protocol that needs one, mapping the function names and tokens per the tables below.

## Files

| English file | Portuguese original |
|---|---|
| `estudo1/t1-extraction.txt` | `dados/estudo1/prompts/t1-extracao.txt` |
| `estudo1/t2-rob.txt` | `dados/estudo1/prompts/t2-rob.txt` |
| `estudo1/t3-synthesis.txt` | `dados/estudo1/prompts/t3-sintese.txt` |
| `estudo2/{md,rr,pool}-{A,B}.txt` | `dados/estudo2/prompts/` (same names) |
| `estudo3/e3-extraction.txt` | `dados/estudo3/prompts/e3-extracao.txt` |
| `estudo3/e3-audit.txt` | `dados/estudo3/prompts/e3-auditoria.txt` |
| `estudo3/e3-calc.txt` | `dados/estudo3/prompts/e3-calc.txt` |
| `estudo3/e3-synthesis.txt` | `dados/estudo3/prompts/e3-sintese.txt` |
| `estudo5/e5-g1.txt`, `e5-g2.txt`, `e5-g3.txt`, `e5-calc2.txt` | `dados/estudo5/prompts/` (same names) |
| `estudo5/e5-verify.txt` | `dados/estudo5/prompts/e5-verifica.txt` |
| `estudo5/e5-synthesis.txt` | `dados/estudo5/prompts/e5-sintese.txt` |

## Placeholder renames (future harness code fills these)

`{ARTIGO}` → `{ARTICLE}` · `{EXTRACOES}` → `{EXTRACTIONS}` · `{FICHA}` → `{SHEET}` · `{RESUMO}` → `{SUMMARY}` · `{DADOS}` → `{DATA}` · `{CAMPO}` → `{FIELD}` · `{VALOR}` → `{VALUE}`

## Marker and vocabulary correspondence

| Portuguese (Studies 1–6) | English (this library) |
|---|---|
| `NR` | `NR` (unchanged) |
| `NAO-CALCULAVEL` | `NOT-COMPUTABLE` |
| `FIM` / `"funcao": "fim"` | `END` / `"function": "end"` |
| `AVISO` / `RESULTADO` (harness dialogue) | `WARNING` / `RESULT` |
| `confirma` / `corrige` / `nao-encontrado` (audit verdicts) | `confirms` / `corrects` / `not-found` |
| `derivado` / `resultado-anterior` / `derivacao` (source tags) | `derived` / `previous-result` / `derivation` |
| dispersion types `DP` / `EP` / `IC95: <inf> a <sup>` | `SD` / `SE` / `CI95: <lower> to <upper>` |
| `valor` / `onde` (cell object) | `value` / `where` |
| `julgamento` / `justificativa` (RoB) | `judgment` / `justification` |
| `veredito` / `valor_corrigido` (audit) | `verdict` / `corrected_value` |
| `funcao` / `argumentos` / `fonte` / `sextetos` (typed calls) | `function` / `arguments` / `source` / `sextets` |
| `por_estudo` / `agregado` / `metodo` / `estudos_usados` / `nota` | `per_study` / `pooled` / `method` / `studies_used` / `note` |

## Calculator function names

| Portuguese | English | Signature (unchanged) |
|---|---|---|
| `md` | `md` | (m1, sd1, n1, m2, sd2, n2) |
| `ic95_md` | `ci95_md` | (m1, sd1, n1, m2, sd2, n2) |
| `dp_de_ic` | `sd_from_ci` | (lower, upper, n) |
| `dp_de_se` | `sd_from_se` | (se, n) |
| `dp_mudanca_r05` | `sd_change_r05` | (sd_baseline, sd_final) |
| `pool_dl_md` | `pool_dl_md` | (list of sextets) |
| `rr` | `rr` | (events_gdft, n_gdft, events_control, n_control) |
| `ic95_rr` | `ci95_rr` | (events_gdft, n_gdft, events_control, n_control) |
| `pool_rr_mh` / `pool_dl` / `pool_md_iv` | unchanged | as in Study 2 |

## Sheet-key correspondence — T1 (GDFT extraction sheet)

| Portuguese key | English key |
|---|---|
| `n_randomizados_gdft` / `_controle` | `n_randomized_gdft` / `_control` |
| `tipo_cirurgia` | `surgery_type` |
| `laparoscopia_*` | `laparoscopy_*` |
| `asa_*` | `asa_*` |
| `fluido_total_*` | `total_fluid_*` |
| `cristaloide_*` | `crystalloid_*` |
| `coloide_*` | `colloid_*` |
| `perda_sanguinea_*` | `blood_loss_*` |
| `uso_inotropico` | `inotrope_use` |
| `morbidade_eventos_*` | `morbidity_events_*` |
| `mortalidade_*` | `mortality_*` |
| `los_hospitalar_*` | `hospital_los_*` |
| `tempo_flatus_*` | `time_to_flatus_*` |
| `tempo_ingesta_oral_*` | `time_to_oral_intake_*` |
| `tempo_evacuacao_*` | `time_to_defecation_*` |
| `ileo_pos_op_*` | `postop_ileus_*` |

Arm suffixes: `_gdft` unchanged; `_controle` → `_control`.

## Sheet-key correspondence — T2 (risk of bias)

`geracao_sequencia_aleatoria` → `random_sequence_generation` · `ocultacao_alocacao` → `allocation_concealment` · `cegamento_participantes_equipe` → `blinding_participants_personnel` · `cegamento_avaliadores_desfecho` → `blinding_outcome_assessment` · `dados_desfecho_incompletos` → `incomplete_outcome_data` · `relato_seletivo` → `selective_reporting` · `outros_vieses` → `other_bias` · `risco_global` → `overall_risk`

## Sheet-key correspondence — E3 (HbA1c extraction sheet)

| Portuguese key | English key |
|---|---|
| `estudo` / `desenho` / `pais` / `duracao` | `study` / `design` / `country` / `duration` |
| `n_randomizado_total` | `n_randomized_total` |
| `braco_experimental` / `braco_controle` | `experimental_arm` / `control_arm` |
| `rotulo` / `descricao_intervencao` | `label` / `intervention_description` |
| `n_randomizado` / `n_analisado` | `n_randomized` / `n_analyzed` |
| `hba1c_mudanca_media` / `_dispersao` / `_tipo_dispersao` | `hba1c_change_mean` / `_dispersion` / `_dispersion_type` |
| `hba1c_basal_media` / `hba1c_basal_dp` | `hba1c_baseline_mean` / `hba1c_baseline_sd` |
| `hba1c_final_media` / `hba1c_final_dp` | `hba1c_final_mean` / `hba1c_final_sd` |

## Outcome keys (Study-2 answer objects)

`morbidade` → `morbidity` · `mortalidade` → `mortality` · `ileo` → `ileus` · `tempo_flatus_h` → `time_to_flatus_h` · `tempo_dieta_oral` → `time_to_oral_diet`
