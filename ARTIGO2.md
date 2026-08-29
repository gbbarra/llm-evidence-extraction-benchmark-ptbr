# EXTRAI, parte 2: nenhum modelo acertou um intervalo de confiança de cabeça — aí eu dei a calculadora, e um deles fechou a metanálise perfeita

*A parte 1 terminou com um paradoxo: os quatro modelos locais extraem evidência quase sem erro, mas concluem "no olho" — contam estudos favoráveis onde a metanálise agregada diz "sem diferença significativa". Faltava saber: eles fazem as contas? O Estudo 2 respondeu com dois braços, numa ideia do próprio dono do benchmark: primeiro os modelos calculam risk ratios, intervalos de confiança e agrupamentos **de cabeça**; depois ganham uma **calculadora** que chamam por texto. De cabeça: zero intervalos de confiança corretos em trinta tentativas, nos quatro. Com a calculadora: um deles fechou 8 de 8 pontos e 8 de 8 intervalos. E o braço bônus, com thinking, produziu a cena mais estranha da série: dezessete minutos de raciocínio terminando em desfechos que não existem.*

> 📄 Série EXTRAI: [parte 1](ARTIGO1.md) · parte 2 (esta) · Dados, protocolos e correção mecânica: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Benchmark irmão: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## O contexto, para quem chega agora

Na parte 1, os quatro modelos refizeram a extração de dados dos 14 ensaios de uma metanálise publicada ([Ashraf et al., Cureus, 2026](https://doi.org/10.7759/cureus.110243) — a âncora de todo o benchmark) com uma célula errada em 624 — mas as sínteses deles, sem ferramenta de agregação, descreviam "tendência favorável" onde a estatística agregada diz "não significativo". O Estudo 2 isola a habilidade que faltou: **a aritmética meta-analítica**. Cada modelo recebe *as próprias extrações* da parte 1 (fidelidade ao que ele mesmo leu) e calcula, por ensaio e agregado: risk ratios (RR — a razão entre o risco do desfecho no braço guiado e no controle), diferenças de médias (MD), intervalos de confiança de 95% (IC95) e os agregados de efeitos fixos (Mantel-Haenszel, "MH") e aleatórios (DerSimonian-Laird, "DL"). A correção é 100% mecânica — a verdade de cada quantidade é a recomputação, por funções validadas contra os valores publicados da âncora (o caso-teste as reproduz exatamente: RR 0,573; IC 0,372–0,884), sobre o insumo que o modelo recebeu. Nenhum juiz de linguagem opina.

## O que exatamente foi feito

Dois braços por modelo, duas réplicas, três famílias de tarefa (RRs por estudo; diferenças de médias; agrupamentos) — 51 corridas em 71 minutos. No braço A, de cabeça, com a instrução de que "NAO-CALCULAVEL" é resposta digna, nunca chute. No braço B, o protocolo de ferramenta é uma linha de texto — o modelo escreve a chamada, o harness executa em Python e devolve o resultado no contexto, até vinte chamadas:

```
CALC: rr(28, 39, 30, 36)
RESULTADO: 0.862
CALC: ic95_rr(28, 39, 30, 36)
RESULTADO: [0.674, 1.101]
```

Braço exploratório: o thinking do qwen3:14b, a "vocação matemática" que o FIEL nunca testou.

## O que encontramos

### 1. De cabeça: a direção sim, o número não — e o intervalo de confiança nunca

| Modelo (braço A) | Pontos | Exatos | Direção certa | Errados | IC95 exatos |
|---|---|---|---|---|---|
| qwen3.8:27b | 7 | 3 | 2 | 2 | **0/7** |
| qwen3:14b | 8 | 2 | 4 | 2 | **0/8** |
| gemma4:12b | 7 | 1 | 5 | 1 | **0/7** |
| gemma4:26b | 8 | 1 | 5 | 2 | **0/8** |

O que "direção certa, valor errado" significa em números reais — gemma4:12b, morbidade, de cabeça:

| Estudo | Modelo respondeu | A verdade (dos números dele mesmo) |
|---|---|---|
| Yoon | RR 0,931 [0,549–1,611] | RR 0,862 [0,674–1,101] |
| Wu | RR 0,473 [0,252–0,893] | RR 0,594 [0,381–0,925] |

Lado certo do 1, vizinhança certa — e nenhum dígito confiável. **IC95 de cabeça: 0 exato em 30 tentativas, nos quatro modelos.** É a fronteira mais nítida que esta linha de benchmarks já mediu: logaritmo, raiz e exponencial mentais não existem aqui. Qualquer IC "de cabeça" em texto de modelo local é decoração com formato de estatística.

### 2. Com a calculadora, um modelo virou metanalista completo

| Modelo (braço B) | Pontos exatos | IC95 exatos | Chamadas CALC |
|---|---|---|---|
| qwen3.8:27b | **8/8** | **8/8** | 32 |
| qwen3:14b | 7/8 | 7/8 | 36 |
| gemma4:12b | 6/8 | 6/8 | 36 |
| gemma4:26b | não fechou (ver achado 3) | — | 40 |

A primeira rodada do qwen3.8:27b, literal — planejamento limpo, um par de chamadas por estudo:

```
CALC: rr(18, 224, 35, 226)
CALC: ic95_rr(18, 224, 35, 226)
CALC: rr(28, 39, 30, 36)
CALC: ic95_rr(28, 39, 30, 36)
```

A hipótese pré-registrada pedia que a ferramenta ao menos dobrasse as exatas; ela as triplicou a sextuplicou. Com a conta terceirizada, sobra o que os modelos realmente têm: saber **o que** calcular com **quais** números.

### 3. O fracasso que sobrou é de fluxo, não de matemática — três falhas, cada uma com prova

**O que não fecha**: o gemma4:26b disparou as 20 chamadas permitidas e nunca emitiu a resposta final — a última rodada dele ainda era isto:

```
CALC: rr(19, 61, 32, 61)
CALC: ic95_rr(19, 61, 32, 61)
```

**O que ignora a ferramenta**: no agrupamento, qwen14 e qwen38 responderam de cabeça com a calculadora à disposição (0 chamadas) — e o insumo que o qwen14 declarou ter "agrupado" mostra o erro na veia: `"estudos_usados": [[8.6, 224, 16.6, 226], …]` — **percentuais no lugar de contagens de eventos**. **O que confunde chamada com dado**: o 26b escreveu `"call": "CALC: pool_rr_mh([[…]])"` *dentro* do JSON, como texto — entendeu o quê, não o como. Resultado agregado: **nenhum modelo orquestrou uma metanálise completa via ferramenta**. Para o deployment, isso pede um harness que force o fechamento — não um modelo maior.

### 4. O ranking inverteu — cada família tem o seu músculo

| | Extração (parte 1) | Contas de cabeça (parte 2) |
|---|---|---|
| gemma4:12b | **100%** | 1 exata |
| gemma4:26b | **99%** | 1 exata |
| qwen3.8:27b | 97% | **3 exatas** |
| qwen3:14b | 92% | 2 exatas |

O formulário é dos gemma; a aritmética, dos qwens — e nenhum ranking prevê o outro. Quem monta uma esteira real deveria escalar cada etapa como quem contrata gente: o meticuloso para a ficha, o numérico para a conta.

### 5. O thinking é meia-calculadora — com um fantasma dentro

| qwen3:14b, braço A | Sem thinking | Com thinking (12 mil tokens) |
|---|---|---|
| RR/MD exatos | 2/8 | **6/7** |
| IC95 exatos | 0/8 | **0/7** |
| Custo por corrida | ~1 min | 5–17 min (10–17×) |

Com 5.600 tokens de orçamento, colapso mudo — o raciocínio consome tudo e a resposta sai vazia (o eco exato do que a Série 1 do FIEL viu na escrita). Com 12.000, converge e quase alcança a ferramenta na aritmética simples. Mas no agrupamento, após 17 minutos pensando, veio a cena — o JSON final, literal:

```json
{"morbidity":  {"fixed_effect": {"rr": 0.768}, "random_effects": {"rr": 0.741}},
 "mortality":  {"fixed_effect": {"rr": 0.768}, "random_effects": {"rr": 0.741}},
 "recurrence": {"fixed_effect": {"rr": 0.768}, "random_effects": {"rr": 0.741}},
 "symptoms":   {"fixed_effect": {"rr": 0.768}, "random_effects": {"rr": 0.741}}}
```

O mesmo par de números clonado em quatro desfechos — dois dos quais ("recurrence", "symptoms") **não existem no insumo**. A única fabricação de todo o Estudo 2 veio do braço que mais pensou. A calculadora vence o thinking em precisão, custo e sanidade.

### 6. E as contas da própria metanálise? Quase perfeitas — com um rótulo trocado

O mesmo corretor auditou a âncora:

| Quantidade | Publicado | Recomputado | Veredito |
|---|---|---|---|
| RRs por estudo (11 células, tabelas 5/6/11) | — | — | **11/11 corretos** (±0,015) |
| Morbidade agregada | 0,778 [0,57–1,07] | DL: **0,774** [0,566–1,059] | número certo… |
| …calculada como | "Mantel-Haenszel" (legenda) | MH daria **0,863** | **…nome do método errado** |

A aritmética dos revisores humanos está absolvida — os erros da parte 1 eram de *transcrição*. Mas o agregado da morbidade é um DerSimonian-Laird exato rotulado de Mantel-Haenszel: a 15ª entrada do arquivo público de erratas.

## O que isso significa

A esteira de revisão sistemática em hardware de consumidor agora tem receita medida etapa por etapa: **extrair com o gemma4:12b na GPU integrada** (100% na parte 1), **calcular com o protocolo CALC** (o 27B fecha perfeito; o 14b quase, em fração do tempo), e **agregar sempre pela ferramenta — nunca pela cabeça de ninguém, humana ou artificial**. E uma lição de leitura crítica que vale além dos modelos: a honestidade deles é assimétrica — declaram "não calculável" quando faltam *dados*, nunca quando falta *capacidade*. Diante do IC, todos tentaram e erraram com confiança. Desconfie de qualquer estatística inferencial entregue sem a conta à mostra.

## Limitações

Uma réplica pontuada por braço (a segunda mede estabilidade); o protocolo CALC é uma implementação particular de ferramenta — tool calling nativo pode se comportar diferente; os insumos herdam as extrações (e perturbações) da parte 1 por desenho; o braço thinking é exploratório, de uma réplica, num único modelo. A auditoria da âncora cobre a aritmética das tabelas — não os dados que entraram nelas (esses foram o assunto da parte 1).

*Na parte 3: a pergunta que os dois estudos deixam armada — a esteira inteira, do PDF ao forest plot, num mini-PC sem nuvem, com um modelo auditando o outro. A fila decide.*
