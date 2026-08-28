# EXTRAI — Avaliação do Estudo 1 (registro de correção)

Correção encerrada em 2026-08-28. Régua: `gabarito-oficial.json` (camada 2, verificada
na fonte primária — Emenda 4), com as perturbações por cima e as adjudicações públicas
em `adjudicacoes-t1.json`. Instrumentos: `corrigir.py` (T1), `corrigir-rob.py` (T2),
checagem anti-invenção das sínteses (números da T3 ⊆ extrações do próprio modelo).

**Quem fez o quê**: os modelos locais produziram as 132 corridas (fila de 8,3 h,
2026-08-27/28); o corretor mecânico decidiu as células com equivalências pré-declaradas;
o adjudicador (Claude, sob supervisão do autor) decidiu as 37 células textuais, cada uma
com citação da fonte; os erros do adjudicador no caminho estão em `erratas-da-ancora.md`.

## T1 — Extração estruturada (métrica principal: acurácia contra a fonte)

99 células pontuáveis por modelo (das 240 do formulário; o resto: sem valor na MA e sem
verificação de fonte, pendentes, ou dado fora do insumo — nenhuma conta contra nenhum
modelo). Zero células pendentes de decisão.

| Modelo | Acurácia | Exatas | Deriváveis | NR-corretas | Omissas | Erradas/Inventadas/Recitadas |
|---|---|---|---|---|---|---|
| gemma4:12b | **100%** (99/99) | 72 | 14 | 13 | 0 | 0 |
| gemma4:26b | **100%** (99/99) | 76 | 6 | 17 | 0 | 0 |
| qwen3.8:27b | **98%** (97/99) | 79 | 5 | 13 | 2 | 0 |
| qwen3:14b | **90%** (89/99) | 65 | 6 | 18 | 10 | 0 |

- **Zero valores errados, inventados ou recitados nos quatro modelos** (396 células
  decididas). Todo ponto perdido é omissão: "NR" onde a fonte reporta o dado.
- O qwen3.8:27b tem o **maior número de células exatas** (79) — quando responde, é o
  mais literal; perde por recusar. O qwen3:14b é o mais conservador (10 omissões).
- Falha de formato: 1 JSON inválido em 64 extrações — gemma4:26b, Sujatha r1, chave
  fundida com valor ("ao_control: statistically…"), a assinatura de corrupção de token
  do MoE vista no FIEL E14; a réplica 2, válida, pontuou (regra da primeira réplica
  parseável).
- Estabilidade entre réplicas (campo idêntico r1=r2): qwen14 84% · gemma26 82% ·
  qwen38 76% · gemma12 75%. As diferenças são majoritariamente de formatação
  (pontuação/ordem), não de conteúdo.

## Prova de leitura (perturbação)

| Modelo | Leu (valor perturbado) | Recitou | Ausente |
|---|---|---|---|
| gemma4:12b | 34 | 0 | 4 |
| gemma4:26b | 32 | 0* | 4 |
| qwen3.8:27b | 30 | 0* | 7 |
| qwen3:14b | 28 | 0* | 8 |

\* Emenda 3: nas duas células com vazamento do harness ("4088mL"; "800-2750"), devolver
o original é leitura de insumo inconsistente, não recitação. **Nenhuma recitação
atribuível em 132 corridas** — os modelos leram o que receberam; nenhum sinal de
contaminação de treino (âncora pós-corte) nem de memorização dos primários.

## T2 — Risco de viés (concordância com os revisores da MA)

7 domínios Cochrane × 7 estudos (Weinberg fora: a MA não tem linha de RoB para ele —
inconsistência pré-registrada nº 1). Julgamento global à parte (a MA usa escala com
"Moderate").

| Modelo | Concordância (7 domínios) | Global igual | Estabilidade r1=r2 |
|---|---|---|---|
| gemma4:12b | **78%** (38/49) | 3/7 | 98% |
| gemma4:26b | **77%** (36/47) | 2/7 | 91% |
| qwen3:14b | 57% (28/49) | 2/7 | 98% |
| qwen3.8:27b | 57% (28/49) | 0/7 | 81% |

Por domínio (4 modelos juntos): relato seletivo 89% · geração de sequência 86% · dados
incompletos 74% · ocultação 68% · outros vieses 68% · cegamento de avaliadores 63% ·
**cegamento de participantes/equipe 21%**. Neste último, o padrão é unilateral: a MA
julgou "Unclear" e os modelos, "High" (16 dos 28 pares) — em ensaio de fluidoterapia o
anestesista que executa o algoritmo não pode ser cegado, e os modelos aplicam a regra
Cochrane literalmente onde os revisores foram lenientes. Divergência de doutrina, não de
leitura.

## T3 — Síntese narrativa

Referência (abstract da âncora, 14 estudos): morbidade **sem** redução significativa
(RR 0,78; IC 0,57–1,07); mortalidade sem diferença; internação **menor** com GDFT;
função intestinal **melhor** (flatus, dieta oral, íleo RR 0,48).

| Modelo | Palavras (250–400) | Números órfãos | Veredito de direção |
|---|---|---|---|
| gemma4:12b | 364 ✓ | 0 | compatível, hedge alto (subvende o benefício intestinal dos próprios dados) |
| qwen3:14b | 355 ✓ | 0 | compatível; morbidade mais otimista que a MA agregada, mas fiel às próprias extrações ("cinco de oito ensaios") |
| gemma4:26b | 361 ✓ | 0 | compatível; cita fielmente os valores perturbados do próprio insumo |
| qwen3.8:27b | 328 ✓ | 0 | compatível e o mais estruturado; nota original correta ("GDFT reduziu o volume de fluidos em todos os ensaios que reportaram") |

**Checagem anti-invenção mecânica: zero números órfãos nas quatro sínteses** — cada
número citado existe nas extrações T1 do próprio modelo. Nenhum modelo inventou
agregado meta-analítico (nenhum RR/IC fabricado); as divergências com a MA (morbidade
descrita como favorável) refletem contagem de estudos individuais sem ferramenta de
agregação — exatamente a lacuna que o Estudo 2 ("as contas") vai medir.

## Tempos de máquina

| Bloco | Duração | Mediana/corrida |
|---|---|---|
| gemma4:12b (iGPU) | 84 min | 154 s |
| qwen3:14b (iGPU) | 65 min | 88 s |
| gemma4:26b (CPU, MoE) | 76 min | 116 s |
| qwen3.8:27b (CPU, denso) | 267 min | 476 s |

Fila completa: 8,3 h. O cache de prefixo KV (artigo antes das instruções) cortou as
réplicas em ~50–70% do custo da primeira corrida de cada artigo.
