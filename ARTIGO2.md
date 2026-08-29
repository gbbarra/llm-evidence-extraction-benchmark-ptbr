# EXTRAI, parte 2: nenhum modelo acertou um intervalo de confiança de cabeça — aí eu dei a calculadora, e um deles fechou a metanálise perfeita

*A parte 1 terminou com um paradoxo: os quatro modelos locais extraem evidência quase sem erro, mas concluem "no olho" — contam estudos favoráveis onde a metanálise agregada diz "sem diferença significativa". Faltava saber: eles fazem as contas? O Estudo 2 respondeu com dois braços, numa ideia do próprio dono do benchmark: primeiro os modelos calculam risk ratios, intervalos de confiança e agrupamentos **de cabeça**; depois ganham uma **calculadora** que chamam por texto. De cabeça: zero intervalos de confiança corretos em trinta tentativas, nos quatro. Com a calculadora: um deles fechou 8 de 8 pontos e 8 de 8 intervalos. E o braço bônus, com thinking, produziu a cena mais estranha da série: dezessete minutos de raciocínio terminando em desfechos que não existem.*

> 📄 Série EXTRAI: [parte 1](ARTIGO1.md) · parte 2 (esta) · [parte 3](ARTIGO3.md) · Dados, protocolos e correção mecânica: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Benchmark irmão: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## O contexto, para quem chega agora

Na parte 1, os quatro modelos refizeram a extração de dados dos 14 ensaios de uma metanálise publicada ([Ashraf et al., Cureus, 2026](https://doi.org/10.7759/cureus.110243) — a âncora de todo o benchmark) com uma célula errada em 624 — mas as sínteses deles, sem ferramenta de agregação, descreviam "tendência favorável" onde a estatística agregada diz "não significativo". O Estudo 2 isola a habilidade que faltou: **a aritmética meta-analítica**. Cada modelo recebe *as próprias extrações* da parte 1 — **incluindo os valores perturbados que leu**, por coerência de desenho: a verdade usada na correção é recomputada sobre o mesmo insumo, então o teste de aritmética é justo e nenhum número do Estudo 2 é um resultado clínico (a auditoria da âncora, achado 6, é a exceção: usou os valores reais publicados). Com esse insumo, o modelo calcula, por ensaio e agregado: risk ratios (RR — a razão entre o risco do desfecho no braço guiado e no controle; abaixo de 1 favorece o guiado), diferenças de médias (MD), intervalos de confiança de 95% (IC95 — a faixa onde a estimativa "real" provavelmente mora) e os agregados de efeitos fixos (Mantel-Haenszel, "MH") e aleatórios (DerSimonian-Laird, "DL"). A correção é 100% mecânica — a verdade de cada quantidade é a recomputação, por funções validadas contra os valores publicados da âncora (o caso-teste as reproduz exatamente: RR 0,573; IC 0,372–0,884), sobre o insumo que o modelo recebeu. Nenhum juiz de linguagem opina.

## O que exatamente foi feito

Dois braços por modelo, duas réplicas, três famílias de tarefa (RRs por estudo; diferenças de médias; agrupamentos) — 51 corridas em 71 minutos. No braço A, de cabeça, com a instrução de que "NAO-CALCULAVEL" é resposta digna, nunca chute. No braço B, o protocolo de ferramenta é uma linha de texto — o modelo escreve a chamada, o harness (o programa que orquestra o benchmark) a executa em Python e devolve o resultado no contexto, até vinte chamadas:

```
CALC: rr(28, 39, 30, 36)
RESULTADO: 0.862
CALC: ic95_rr(28, 39, 30, 36)
RESULTADO: [0.674, 1.101]
```

Braço exploratório: o thinking do qwen3:14b, a "vocação matemática" que o FIEL nunca testou.

## O que encontramos

### 1. A prova inteira, modelo a modelo — de cabeça vs com calculadora

Antes dos placares, os dados que os produzem: **as oito quantidades por estudo de cada modelo, com os dois braços lado a lado**. A "verdade" de cada linha é recomputada sobre os números que aquele modelo extraiu na parte 1 — por isso ela varia um pouco de modelo para modelo (extrações e perturbações diferentes), e por isso o teste é justo: cada um é cobrado pelos próprios números.

*Como ler: cada linha é um RR por estudo (desfecho + ensaio). "verdade" = recomputação mecânica sobre as células do próprio modelo; A = resposta de cabeça; B = com calculadora. Rótulos: exata (±0,01), direção (lado certo do 1, valor errado), errada, NC (declarou NÃO-CALCULÁVEL).*

```
gemma4:12b            verdade   de cabeça (A)     CALC (B)
morb. Calvo-Vecino     0.504    0.515 direção     0.515 direção
morb. Yoon             0.862    0.931 direção     0.862 exata
morb. Diaper           0.966    1.085 errada      0.966 exata
morb. Wu               0.594    0.473 direção     0.594 exata
mort. de Waal          0.942    0.926 direção     0.942 exata
mort. Sun              3.000    NC recusa         3.000 exata
íleo  Arslan-Carlon    1.191    1.190 exata       1.026 direção
íleo  Sun              0.125    0.250 direção     0.125 exata
```

```
qwen3:14b             verdade   de cabeça (A)     CALC (B)
morb. Calvo-Vecino     0.504    0.518 direção     0.523 direção
morb. Yoon             0.862    0.923 direção     0.862 exata
morb. Diaper           0.924    1.089 errada      0.924 exata
morb. Wu               0.573    0.591 direção     0.573 exata
mort. de Waal          0.944    0.930 direção     0.944 exata
mort. Sun              3.000    0.063 errada      3.000 exata
íleo  Arslan-Carlon    1.026    1.028 exata       1.026 exata
íleo  Sun              0.125    0.125 exata       0.125 exata
```

```
gemma4:26b            verdade   de cabeça (A)     CALC (B)
morb. Calvo-Vecino     0.504    0.518 direção     não fechou —
morb. Yoon             0.862    0.921 direção     disparou as 20
morb. Diaper           0.956    1.089 errada      chamadas sem
morb. Wu               0.594    0.473 direção     emitir o JSON
mort. de Waal          0.849    0.930 direção     final (achado 3)
mort. Sun              3.000    0.000 errada
íleo  Arslan-Carlon    1.191    1.190 exata
íleo  Sun              0.125    0.250 direção
```

```
qwen3.8:27b           verdade   de cabeça (A)     CALC (B)
morb. Calvo-Vecino     0.519    0.518 exata       0.519 exata
morb. Yoon             0.862    0.923 direção     0.862 exata
morb. Diaper           0.924    1.088 errada      0.924 exata
morb. Wu               0.594    0.474 direção     0.594 exata
mort. de Waal          1.178    0.928 errada      1.178 exata
mort. Sun              3.000    NC recusa         3.000 exata
íleo  Arslan-Carlon    1.026    1.017 exata       1.026 exata
íleo  Sun              0.125    0.124 exata       0.125 exata
```

Três leituras saem direto das tabelas. **De cabeça, a direção quase sempre, o número quase nunca**: 1–3 exatas por modelo, o resto vizinhança. **Com a calculadora, o 27B fecha 8/8** e os demais só perdem onde erram o *insumo da chamada* — as duas perdas do 12b no braço B são células erradas passadas à calculadora (percentuais no lugar de contagens no Calvo-Vecino; 31 eventos no lugar de 36 no Arslan-Carlon): a conta certa sobre o número errado continua errada. E o caso Diaper ensina o que "errada" significa de cabeça: os quatro modelos responderam ~1,09 (desfavorável ao GDFT) onde os próprios números dão 0,92–0,97 — provavelmente invertendo os braços na cabeça, o mesmo deslize que a parte 1 flagrou em fluxograma.

### 2. O intervalo de confiança é a fronteira nítida — 0 de cabeça, quase perfeito com ferramenta

O IC95 exige logaritmo, raiz quadrada e exponencial encadeados — aritmética mental que não existe aqui:

*Como ler: ICs exatos (as duas bordas a ±0,01) por braço; no B, gemma26 não fechou a resposta.*

```
modelo         IC95 de cabeça (A)   IC95 com CALC (B)
gemma4:12b          0/7                  6/8
qwen3:14b           0/8                  7/8
gemma4:26b          0/8                  não fechou
qwen3.8:27b         0/7                  8/8
TOTAL               0/30                21/24
```

O que um IC "de cabeça" parece por dentro — gemma4:12b, morbidade do Yoon: o modelo respondeu **RR 0,931 [0,549–1,611]**; a verdade dos números dele mesmo é **0,862 [0,674–1,101]**. Lado certo, formato certo, estatística de enfeite. **Qualquer IC "de cabeça" em texto de modelo local é decoração com formato de estatística.** A hipótese pré-registrada pedia que a ferramenta ao menos dobrasse as exatas; ela as triplicou a sextuplicou.

### 3. O fracasso que sobrou é de fluxo, não de matemática — três modos, cada um com prova literal

No agrupamento (juntar os estudos num RR único — a etapa que exige orquestrar várias chamadas), **nenhum modelo completou a metanálise via ferramenta**. Os três modos de falha, nos brutos:

**Modo 1 — não fechar.** O gemma4:26b disparou as 20 chamadas permitidas e nunca emitiu a resposta final; a última rodada dele ainda era:

```
CALC: rr(19, 61, 32, 61)
CALC: ic95_rr(19, 61, 32, 61)
```

**Modo 2 — escrever a chamada DENTRO da resposta, como texto.** Três modelos (gemma12, gemma26 e qwen38) entregaram o JSON final com a chamada embutida como dado — entenderam *o quê*, não *o como*. O gemma12, literal (com um segundo erro dentro: **8.6 e 16.6 são percentuais**, não contagens de eventos):

```json
{"morbidade": {"mh": "CALC: pool_rr_mh([[8.6, 224, 16.6, 226],
               [28, 39, 30, 36], [113, 198, 117, 198],
               [19, 61, 32, 61]])", …}}
```

**Modo 3 — ignorar a ferramenta e chutar número.** O qwen3:14b respondeu o agrupamento de cabeça (0 chamadas), com valores errados em 2 dos 3 desfechos — e o próprio JSON dele confessa o insumo trocado: `"estudos_usados": [[8.6, 224, 16.6, 226], …]` — percentuais no lugar de eventos, de novo.

*(Correção de 2026-08-29: a primeira versão descreveu o qwen38 no agrupamento como "respondeu de cabeça"; o bruto mostra o modo 2 — chamadas escritas dentro do JSON, como os gemma. A avaliação no repositório carrega a mesma nota.)*

Para o uso em produção, isso pede um harness que **force o fechamento** — não um modelo maior. É exatamente o que o Estudo 3 fará.

### 4. O ranking inverteu — cada família tem o seu músculo

*Como ler: o campeão de extração não é o campeão de conta; compare as colunas.*

```
modelo         extração (parte 1)   contas de cabeça (A)
gemma4:12b         100%                 1 exata
gemma4:26b          99%                 1 exata
qwen3.8:27b         97%                 3 exatas
qwen3:14b           92%                 2 exatas
```

O formulário é dos gemma; a aritmética, dos qwens — e nenhum ranking prevê o outro. Quem monta uma esteira real deveria escalar cada etapa como quem contrata gente: o meticuloso para a ficha, o numérico para a conta.

### 5. O thinking é meia-calculadora — com um fantasma dentro

*Como ler: o mesmo modelo, mesma tarefa de cabeça, com e sem raciocínio estendido (thinking) de 12 mil tokens (tokens são as unidades de texto que o modelo processa — ~¾ de palavra cada).*

```
qwen3:14b, braço A     sem thinking   com thinking (12k)
RR/MD exatos               2/8             6/7
IC95 exatos                0/8             0/7
custo por corrida         ~1 min         5–17 min (10–17×)
```

Com 5.600 tokens de orçamento, colapso mudo — o raciocínio consome tudo e a resposta sai vazia (o eco exato do que a Série 1 do FIEL viu na escrita). Com 12.000, converge e quase alcança a ferramenta na aritmética simples — mas o IC segue impossível. E no agrupamento, após 17 minutos pensando, veio a cena — o JSON final, literal:

```json
{"morbidity":  {"fixed_effect":   {"rr": 0.768},
                "random_effects": {"rr": 0.741}},
 "mortality":  {"fixed_effect":   {"rr": 0.768},
                "random_effects": {"rr": 0.741}},
 "recurrence": {"fixed_effect":   {"rr": 0.768},
                "random_effects": {"rr": 0.741}},
 "symptoms":   {"fixed_effect":   {"rr": 0.768},
                "random_effects": {"rr": 0.741}}}
```

O mesmo par de números clonado em quatro desfechos — dois dos quais ("recurrence", "symptoms") **não existem no insumo**. A única fabricação de todo o Estudo 2 veio do braço que mais pensou. A calculadora vence o thinking em precisão, custo e sanidade.

### 6. E as contas da própria metanálise? Recomputei todas — auditáveis linha a linha

O mesmo mecanismo auditou a âncora, agora sobre os **valores reais publicados** (única parte do estudo que toca números clínicos de verdade). Cada linha pode ser refeita numa calculadora de mão: RR = (eventos÷total)ᴳᴰᶠᵀ ÷ (eventos÷total)ᶜᵗˡ.

*Como ler: eventos/total de cada braço como a MA publicou (tabelas 5, 6 e 11), o RR recomputado e o publicado.*

```
RRs POR ESTUDO — células da MA vs recomputação
estudo               GDFT     controle RR calc  RR publ
MORBIDADE (tabela 5)
Calvo-Vecino 2018    18/209   35/211    0.519    0.519  =
Yoon 2022            28/39    30/36     0.862    0.862  =
Diaper 2021         113/196  105/198    1.087    1.087  =
Wu 2017              19/58    32/56     0.573    0.573  =
MORTALIDADE (tabela 6)
de Waal 2021         10/248   10/234    0.944    0.944  =
Sun 2017              1/50     0/50     3.000    3.000  =
ÍLEO (tabela 11; totais derivados dos % publicados)
Arslan-Carlon 2020   36/142   30/141    1.192    1.19   =
Sun 2017              2/50    16/50     0.125    0.13   ~
Castro 2016           6/43    19/42     0.308    0.31   =
```

Nove de nove reproduzem (o "~" do Sun é cara-ou-coroa de arredondamento: 0,125 impresso como 0,13; toda diferença restante é ≤0,015, no nível da derivação dos totais). Os IC95 idem — todos reproduzem nas mesmas tolerâncias ([detalhe por estudo no repositório](dados/estudo2/avaliacao-estudo2.md)). **É no agregado que a história vira:**

*Como ler: uma linha por receita de agregação; compare cada uma com a linha publicada.*

```
MORBIDADE AGREGADA — número certo, nome errado
                       RR      IC95%            I²
publicado (tabela 5)  0.778   [0.567, 1.068]     —   "MH"
DL recomputado        0.778   [0.567, 1.068]   76.3%  EXATO
MH recomputado        0.873   [0.758, 1.005]     —    difere

MORTALIDADE AGREGADA (tabela 6)
publicado             1.021   [0.446, 2.337]
DL recomputado        1.021   [0.446, 2.337]    0.0%  EXATO
```

Os agregados publicados são DerSimonian-Laird **dígito a dígito** — mas a legenda da tabela 5 nomeia Mantel-Haenszel, cuja recomputação dá um 0,873 visivelmente diferente. A aritmética dos revisores humanos está absolvida (os erros da parte 1 eram de *transcrição*); o que sobra é uma errata de rótulo — a 15ª entrada do arquivo público.

*(Correção de 2026-08-29: a primeira versão deste achado imprimiu uma recomputação ad hoc irreproduzível — "DL 0,774 [0,566–1,059]" e "MH 0,863". Re-verificado a partir das células publicadas da âncora com as mesmas funções validadas: a reprodução DL é exata, dígito a dígito, e o MH recomputado é 0,873. O achado fica mais forte, não mais fraco; nota completa na avaliação do Estudo 2 do repositório.)*

## O que isso significa

A esteira de revisão sistemática em hardware de consumidor agora tem receita medida etapa por etapa: **extrair com o gemma4:12b na GPU integrada** (100% na parte 1), **calcular com o protocolo CALC** (o 27B fecha perfeito; o 14b quase, em fração do tempo), e **agregar sempre pela ferramenta — nunca pela cabeça de ninguém, humana ou artificial**. E uma lição de leitura crítica que vale além dos modelos: a honestidade deles é assimétrica — declaram "não calculável" quando faltam *dados*, nunca quando falta *capacidade*. Diante do IC, todos tentaram e erraram com confiança. Desconfie de qualquer estatística inferencial entregue sem a conta à mostra.

## Quem fez o quê

**Os modelos locais** calcularam (braço A) ou escreveram chamadas (braço B) — 51 corridas. **O harness** executou as funções em Python (validadas contra a âncora: RR 0,573/IC 0,372–0,884 reproduzidos exatos), devolveu os resultados ao contexto e correu a fila. **O corretor mecânico** rotulou cada quantidade recomputando a verdade sobre o insumo do próprio modelo — nenhum juiz de linguagem. **O Claude (assistente)** desenhou o estudo com o autor, escreveu harness e corretor, e fez a auditoria da âncora do achado 6 (recomputação mecânica; transcrição conferida). **O autor** propôs a ideia da calculadora, decidiu o desenho e revisou tudo.

## Limitações

Uma réplica pontuada por braço (a segunda mede estabilidade); o protocolo CALC é uma implementação particular de ferramenta — tool calling nativo pode se comportar diferente; os insumos herdam as extrações (e perturbações) da parte 1 por desenho; o braço thinking é exploratório, de uma réplica, num único modelo. A auditoria da âncora cobre a aritmética das tabelas — não os dados que entraram nelas (esses foram o assunto da parte 1).

*Na parte 3: a pergunta que os dois estudos deixam armada — a esteira inteira, do PDF ao forest plot, num mini-PC sem nuvem, com um modelo auditando o outro e erros semeados para medir se a auditoria é real. A fila decide.*
