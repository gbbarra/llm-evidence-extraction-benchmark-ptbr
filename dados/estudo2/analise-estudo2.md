# EXTRAI — Análise do Estudo 2 "as contas" (vereditos e achados)

Encerrado em 2026-08-29. Números completos na [avaliação](avaliacao-estudo2.md);
protocolo pré-registrado [aqui](protocolo-estudo2.md).

## Vereditos das hipóteses pré-registradas

| Hipótese | Veredito |
|---|---|
| **H2.1** — braço B ≥ 2× o braço A em exatas | **CONFIRMADA COM FOLGA** nos três modelos que fecharam o B (12b: 1→6; 14b: 2→7; 27B: 3→8 = perfeito). O quarto (26b) virou o caso de estudo da exceção: usa a ferramenta e não fecha a resposta. |
| **H2.2** — anatomia do braço A (direção sim, RR ~metade, IC ~zero) | **CONFIRMADA em cheio.** Direção certa em ~75–85% dos pontos; RRs exatos 1–3 por modelo; **IC95: 0 exato em 30 tentativas nos quatro modelos** — o intervalo de confiança de cabeça é impossível para todos. |
| **H2.3** — agrupamento é outro músculo, mesmo com ferramenta | **CONFIRMADA da forma mais reveladora**: os modelos nem tentaram — qwen14 e qwen38 responderam o pool de cabeça ignorando a calculadora disponível; gemma26 escreveu as chamadas dentro do JSON como texto. Zero agrupamentos orquestrados corretamente via ferramenta. |
| **H2.4** — honestidade (NC nos ICs; fabricação <5%) | **PARCIAL.** NAO-CALCULAVEL apareceu (2 recusas legítimas no A), mas os modelos preferiram *tentar* o IC e errar a declarar NC — o IC de cabeça saiu com cara de estatística e valor errado em 30/30. Fabricação no sentido estrito (número sem insumo) ≈ 0; "aritmética confiante e errada" é o modo dominante. |
| **H2.5** — ranking das contas ≠ ranking da extração | **CONFIRMADA.** No braço A: 27B (3 exatas) > 14b (2) > 12b = 26b (1) — os qwens sobem, invertendo a tabela da extração (12b=26b no topo). No braço B o 27B fecha perfeito (8/8 + IC 8/8). A vocação aritmética é da família qwen; a disciplina de formulário, da gemma. |
| **H2.6** — auditoria da âncora | **CONFIRMADA (com nuance elegante).** Os 11 RRs por estudo publicados estão todos certos. O agregado da morbidade reproduz exatamente sob DerSimonian-Laird (0,774 vs 0,778 publicado) — mas a legenda o chama de Mantel-Haenszel (que daria 0,863). **Errata de rótulo de método** na âncora: número certo, nome errado. |

## Os quatro achados

1. **A calculadora transforma o problema.** De cabeça: 7 RRs exatos em 30 pontos e
   nenhum IC certo, nos quatro modelos somados. Com o protocolo CALC: o qwen3.8:27b
   fecha 8/8 pontos e 8/8 intervalos — nível de metanalista — e 12b/14b chegam a 6–7/8.
   O gargalo não é conceitual: com a conta terceirizada, os modelos sabem exatamente o
   que calcular com quais números.

2. **O fracasso residual é de fluxo, não de matemática.** As três falhas do braço B são
   de *workflow*: não fechar a resposta depois de chamar (gemma26 no rr), ignorar a
   ferramenta na tarefa mais difícil (qwen14/qwen38 no pool) e confundir chamada com
   dado (gemma26 no pool). Para deployment, isso pede um harness que force o fechamento
   — não um modelo maior.

3. **O intervalo de confiança é a fronteira nítida da aritmética mental.** 0/30. Nem o
   melhor modelo chega perto de um IC de cabeça (log, raiz, exponencial). Direção e
   ordem de grandeza, sim; inferência, nunca. Qualquer IC "de cabeça" num texto de LLM
   local deve ser tratado como decoração.

4. **A honestidade tem assimetria.** Os modelos declaram NC quando *faltam dados*, mas
   não quando *falta capacidade*: diante do IC, todos tentaram e erraram com confiança.
   O "sabe que não sabe" funciona para o insumo, não para o próprio limite aritmético.

5. **O thinking é meia-calculadora com um preço e um fantasma** (braço exploratório,
   qwen3:14b). Na aritmética simples, pensar ~10 mil tokens triplica as exatas (6/7 vs
   2/8) — quase nível ferramenta. Mas o IC continua 0/7, o custo é 10–17× e, no
   agrupamento, 17 minutos de raciocínio terminaram em perseveração: os mesmos números
   clonados em quatro desfechos, dois deles inexistentes no insumo — a única fabricação
   de todo o estudo. A calculadora vence o thinking em precisão, custo e sanidade.

## Limitações

Uma réplica pontuada por braço (a segunda existe e mede estabilidade); insumos herdados
do E1 com células perturbadas (coerente por desenho — a verdade é recomputada sobre o
mesmo insumo); o protocolo CALC é uma implementação particular de ferramenta (tool
calling nativo pode diferir); pools comparados contra o conjunto parseável (subconjuntos
declarados pelos modelos foram raros). O braço thinking é exploratório (1 réplica).

## Próximo

Os resultados A×B alimentam a Parte 2 do EXTRAI. Deployment sugerido pelo conjunto
E1+E2: extração pelo gemma4:12b (100% na iGPU), contas pelo protocolo CALC com qualquer
modelo que feche (27B se houver tempo, 14b se não), agregação SEMPRE pela ferramenta —
nunca pela cabeça de ninguém, humana ou artificial.
