# EXTRAI — Avaliação do Estudo 2 "as contas" (registro de correção)

Fila de 51 corridas concluída em 71 min (2026-08-28); correção 100% mecânica
(`corrigir-e2.py`): a verdade de cada quantidade é a recomputação — pelas funções do
harness, validadas contra os valores publicados da âncora (RR 0,573; IC 0,372–0,884 no
caso-teste) — sobre o insumo que o próprio modelo recebeu (as suas extrações do E1,
interpretadas por regras fixas documentadas no corretor).

**Quem fez o quê**: os modelos calcularam (braço A) ou orquestraram chamadas (braço B);
o harness executou as funções e devolveu resultados; o corretor rotulou cada quantidade
sem intervenção de juiz de linguagem.

## Registro de execução

- Bug corrigido antes da análise: o braço exploratório *thinking* saiu vazio na primeira
  rodada (o orçamento de raciocínio consumia todo o `num_predict`); re-rodado com
  `4000 + 1600` tokens.
- gemma26 no braço B (família rr) atingiu o teto de 20 chamadas sem emitir o JSON final
  em 5 rodadas — pontuado como falha de fechamento (json-inválido), não de aritmética.
- No braço B da família *pool*, qwen14 e qwen38 **não chamaram a calculadora** (0 CALC)
  e responderam direto; gemma26 escreveu as chamadas **dentro** do JSON como texto
  (entendeu o quê, não o como). Só o registro de comportamento já é resultado.

## Placar (réplica 1; ponto = RR ou MD por estudo)

| Modelo | Braço | Quantidades | Exatas | Direção certa | Erradas | NC-recusa | IC95 exatos |
|---|---|---|---|---|---|---|---|
| gemma4:12b | A | 7 | 1 | 5 | 1 | 1 | **0/7** |
| gemma4:12b | **B** | 8 | **6** | 2 | 0 | 0 | **6/8** |
| qwen3:14b | A | 8 | 2 | 4 | 2 | 0 | **0/8** |
| qwen3:14b | **B** | 8 | **7** | 1 | 0 | 0 | **7/8** |
| gemma4:26b | A | 8 | 1 | 5 | 2 | 0 | **0/8** |
| gemma4:26b | **B** | — | falha de fechamento (rr); md honesto (NC×5) | | | | |
| qwen3.8:27b | A | 7 | 3 | 2 | 2 | 1 | **0/7** |
| qwen3.8:27b | **B** | 8 | **8** | 0 | 0 | 0 | **8/8** |

Agrupamentos (MH/DL/IV): braço A — 2 exatos em 24 tentativas (gemma26 acertou 2 pools
de cabeça; o resto errado ou NC); braço B — qwen14/qwen38 ignoraram a ferramenta no
pool (valores de cabeça, errados), gemma26 não fechou; **nenhum modelo orquestrou o
agrupamento com a calculadora**.

## Braço exploratório (qwen3:14b + thinking, braço A, 1 réplica)

*(preenchido na re-rodada corrigida — ver seção de emendas do protocolo/registro acima)*

## Auditoria aritmética da âncora (H2.6)

Recomputação mecânica das tabelas 5/6/11 da MA a partir das células publicadas:

- **RRs por estudo: todos corretos** (11/11 dentro de ±0,015).
- **Agregado da morbidade: o número publicado (0,778; IC 0,57–1,07) reproduz exatamente
  sob DerSimonian-Laird (recomputado: 0,774; 0,566–1,059) — mas a legenda da tabela 5
  o descreve como Mantel-Haenszel** (o MH recomputado dá 0,863). Errata de rótulo de
  método: número certo, nome errado. Agregado da mortalidade: divergência de 0,027
  (nível de arredondamento/definição de n; não adjudicável como erro).
