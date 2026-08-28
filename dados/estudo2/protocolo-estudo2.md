# EXTRAI — Protocolo pré-registrado do Estudo 2: "as contas"

**Registrado em 2026-08-28, antes de qualquer corrida.** Emendas só por seção datada.
Método geral: [`METHOD.md`](../../METHOD.md). Desenho esboçado no [roadmap](../../roadmap.md)
e proposto pelo autor ("e se fornecermos as fórmulas para os modelos no formato de
plugin ou código para eles chamarem?").

## 1. Pergunta

O Estudo 1 mostrou que os quatro modelos extraem evidência quase sem erro (624 células,
1 errada), mas sintetizam "no olho" — descrevem morbidade favorável onde a metanálise
agregada diz não-significativa. O Estudo 2 pergunta: **eles conseguem transformar as
próprias extrações em metanálise de verdade — risk ratio, intervalo de confiança e
agrupamento?** E: quanto do fracasso é conceitual (não saber o que calcular) versus
aritmético (não ter calculadora)?

## 2. Desenho: dois braços por modelo

- **Braço A — de cabeça.** O modelo recebe as tabelas 2×2/estatísticas por estudo
  (extraídas por ELE mesmo no E1, réplica 1) e calcula sem ajuda. Instrução explícita:
  *"se não conseguir calcular com confiança, escreva NAO-CALCULAVEL"* — medir a
  honestidade aritmética é objetivo primário, não acessório.
- **Braço B — com calculadora (protocolo de texto uniforme).** Mesmo insumo, mas o
  modelo pode escrever linhas `CALC: <funcao>(<args>)`; o harness intercepta, computa em
  Python e devolve `RESULTADO: <valor>` no contexto, em até 20 chamadas por corrida.
  Funções expostas (assinaturas no prompt): `rr(ev_gdft, n_gdft, ev_ctrl, n_ctrl)`,
  `ic95_rr(ev_gdft, n_gdft, ev_ctrl, n_ctrl)`, `md(m1, dp1, n1, m2, dp2, n2)`,
  `ic95_md(...)`, `pool_rr_mh(lista de [ev1,n1,ev2,n2])`, `pool_md_iv(lista)`,
  `pool_dl(lista)` (efeitos aleatórios DerSimonian-Laird).
- O protocolo de texto (e não tool-calling nativo) é o braço principal porque é o mesmo
  mecanismo para as quatro famílias; tool-calling nativo do Ollama fica como braço
  exploratório opcional, registrado à parte se rodar.

## 3. Materiais e desfechos

Insumo por modelo: as SUAS extrações T1-r1 do E1 (14 estudos), reduzidas pelo harness às
células relevantes por desfecho (sem os textos dos artigos). Desfechos calculados:

| Desfecho | Tipo | Estudos com dados na âncora |
|---|---|---|
| Morbidade geral | RR por estudo + agrupado | 5 (tabela 5 da MA) |
| Mortalidade | RR por estudo + agrupado | 3 (tabela 6) |
| Íleo pós-operatório | RR por estudo + agrupado | 3 (tabela 11) |
| Tempo até flatus / dieta oral | MD por estudo | tabelas 8–9 |

**Gabarito triplo**, todo mecânico: (a) a verdade aritmética (recomputada em Python a
partir das células do gabarito-oficial); (b) os valores publicados pela âncora
(RR/IC/pesos das tabelas 5–11) — o que também audita a estatística da própria
metanálise, de novo; (c) para o braço B, o registro literal das chamadas CALC e seus
retornos (o modelo usou a ferramenta certa com os números certos?).

## 4. Modelos, réplicas e fila

Os 4 veteranos nas configurações congeladas do E1. Por modelo: braço A ×2 réplicas +
braço B ×2 réplicas, uma corrida por desfecho-família (RRs; MDs; agrupamentos) —
fila estimada em ~64 corridas curtas (insumo pequeno, sem artigo). Braço exploratório:
qwen3:14b com thinking ligado no braço A (a "vocação para calcular" que a Série 1 do
FIEL nunca testou), 1 réplica, reportado à parte.

## 5. Pontuação (mecânica, sem juiz de linguagem)

Por quantidade calculada: **exata** (|Δ| ≤ 0,01 em RR/IC com 2 casas; ≤ 0,1 em MD) ·
**direção-certa** (RR do lado certo de 1 / MD do lado certo de 0) · **errada** ·
**NAO-CALCULAVEL declarado** (não pontua contra no braço A; conta como recusa no B) ·
**fabricada** (número com formato de estatística que não bate com nenhuma conta válida
dos insumos — a pior categoria, contada à parte). No braço B, adicionalmente:
chamadas corretas / chamadas com argumentos errados / resultados ignorados.

## 6. Hipóteses pré-registradas

- **H2.1 (a calculadora paga):** acurácia exata no braço B ≥ 2× a do braço A, nos 4 modelos.
- **H2.2 (anatomia do braço A):** direção ≥ 80%; RR simples ≈ metade; IC95% ≈ zero.
- **H2.3 (o agrupamento é outro músculo):** mesmo no braço B, o agrupamento fica abaixo
  do RR por estudo — orquestrar várias chamadas e combinar é planejamento, não aritmética.
- **H2.4 (honestidade):** no braço A, NAO-CALCULAVEL concentra-se nos ICs e agrupamentos;
  fabricação < 5% das quantidades nos 4 modelos.
- **H2.5 (ranking próprio):** o ranking das contas NÃO repete o da extração (12b=26b>27B>14b);
  predição direcional: os qwens sobem no braço A (família com fama de matemática).
- **H2.6 (auditoria da âncora, de novo):** ≥ 1 divergência entre a verdade aritmética e o
  valor publicado pela MA (as tabelas 5–11 herdam os erros de extração já documentados —
  ex.: RR da morbidade do Yoon com braços trocados).

## 7. O que fica fora

Meta-regressão, heterogeneidade além do τ²/I² do pool_dl, GRADE, e correções de
continuidade para células zero (registrar como limitação se aparecerem). Sem perturbação
neste estudo: o insumo são as extrações do próprio modelo, já auditadas no E1.

---

*Emendas: (nenhuma)*
