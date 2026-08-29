# EXTRAI, parte 2: nenhum modelo acertou um intervalo de confiança de cabeça — aí eu dei a calculadora, e um deles fechou a metanálise perfeita

*A parte 1 terminou com um paradoxo: os quatro modelos locais extraem evidência quase sem erro, mas sintetizam "no olho" — contam estudos favoráveis onde a metanálise agregada diz "sem diferença significativa". Faltava saber: eles conseguem fazer as contas? O Estudo 2 respondeu com um desenho de dois braços sugerido pelo próprio dono do benchmark: primeiro os modelos calculam risk ratios, intervalos de confiança e agrupamentos **de cabeça**; depois ganham uma **calculadora** que podem chamar por texto. O resultado de cabeça: zero intervalos de confiança corretos em trinta tentativas, nos quatro modelos. Com a calculadora: um deles fechou 8 de 8 pontos e 8 de 8 intervalos — nível de metanalista. E o braço bônus, com thinking ligado, produziu a cena mais estranha da série: dezessete minutos de raciocínio terminando em desfechos que não existem.*

> 📄 Parte 1: extração célula a célula ([ARTIGO1](ARTIGO1.md)). Método, protocolos pré-registrados, correção mecânica e todos os dados: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · Benchmark irmão: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## O desenho, em um parágrafo

Cada modelo recebe **as próprias extrações** da parte 1 (fidelidade ao que ele mesmo leu, valores perturbados inclusos) e calcula, para cada ensaio: o risk ratio de morbidade, mortalidade e íleo; as diferenças de médias dos tempos intestinais; e os agrupamentos de efeitos fixos (Mantel-Haenszel) e aleatórios (DerSimonian-Laird). No braço A, de cabeça — com a instrução explícita de que "NAO-CALCULAVEL" é resposta digna, nunca chute. No braço B, com um protocolo de ferramenta de uma linha: o modelo escreve `CALC: rr(19, 58, 32, 56)`, o harness executa em Python e devolve `RESULTADO: 0.573` no contexto, até vinte chamadas. A correção é 100% mecânica: a verdade de cada quantidade é a recomputação — por funções validadas contra os valores publicados da metanálise-âncora (que o caso-teste reproduz exatamente: RR 0,573; IC 0,372–0,884) — sobre o insumo que o modelo recebeu. Nenhum juiz de linguagem opina.

## Os seis achados

### 1. De cabeça: a direção sim, o número não — e o intervalo de confiança nunca

No braço A os quatro modelos acertaram a **direção** do efeito em cerca de 80% dos pontos — sabem de que lado do 1 o risk ratio cai. Mas o valor exato saiu de 1 a 3 vezes por modelo, e o intervalo de confiança de 95% — que exige logaritmo, raiz quadrada e exponencial mentais — deu **zero exatos em trinta tentativas, nos quatro modelos**. É a fronteira mais nítida que este benchmark já mediu: qualquer IC "de cabeça" num texto de modelo local é decoração com formato de estatística.

### 2. Com a calculadora, um modelo virou metanalista completo

No braço B o qwen3.8:27b fechou **8 de 8 pontos e 8 de 8 intervalos** — perfeito; o qwen3:14b, 7 de 8; o gemma4:12b, 6 de 8. A hipótese pré-registrada pedia que a ferramenta ao menos dobrasse as exatas; ela as triplicou a sextuplicou. Com a conta terceirizada, sobra o que os modelos realmente têm: saber **o que** calcular, com **quais** números — e isso eles sabem.

### 3. O fracasso que sobrou é de fluxo, não de matemática

As três falhas do braço B são de *workflow*, e cada uma tem nome. O gemma4:26b disparou as vinte chamadas permitidas e **nunca emitiu a resposta final** — usa a ferramenta e não fecha. No agrupamento, qwen14 e qwen38 **ignoraram a calculadora disponível** e responderam de cabeça (errado); e o 26b escreveu as chamadas *dentro* do JSON, como texto — entendeu o quê chamar, não o como. Resultado agregado: **nenhum modelo orquestrou uma metanálise completa via ferramenta**. Para o deployment, isso pede um harness que force o fechamento — não um modelo maior.

### 4. O ranking inverteu — cada família tem o seu músculo

Na extração da parte 1, os gemma disciplinados venceram (100% e 99%). Nas contas de cabeça, os **qwens** sobem: 27B com 3 exatas, 14b com 2, contra 1 de cada gemma. A vocação aritmética é de família — e nenhum ranking de uma tarefa prevê o da outra. Quem monta uma esteira real deveria escalar cada etapa como se contrata gente: o formulário para o meticuloso, as contas para o numérico.

### 5. O thinking é meia-calculadora — com um fantasma dentro

O braço exploratório ligou o thinking do qwen3:14b. Com orçamento de 5.600 tokens, colapso mudo: raciocínio consome tudo, resposta vazia (o eco exato do que a Série 1 do FIEL viu na escrita). Com 12.000, convergiu — e nas contas simples fez **6 exatas de 7**, quase nível ferramenta. Mas o IC seguiu 0 de 7, cada corrida custou 10 a 17 vezes mais… e no agrupamento veio a cena: após 17 minutos pensando, o modelo entregou o mesmo par de números clonado em **quatro desfechos — dois dos quais não existem no insumo** ("recurrence", "symptoms"). A única fabricação de todo o estudo veio do braço que mais pensou. A calculadora vence o thinking em precisão, custo e sanidade.

### 6. E as contas da própria metanálise? Quase perfeitas — com um rótulo trocado

O mesmo corretor auditou a âncora: os **11 risk ratios por estudo publicados estão todos certos** (o que absolve a aritmética dos revisores humanos — os erros da parte 1 eram de *transcrição*). Mas o RR agregado da morbidade (0,778) reproduz exatamente sob **DerSimonian-Laird** (recomputado: 0,774), enquanto a legenda da tabela o descreve como **Mantel-Haenszel** — que daria 0,863. Número certo, nome do método errado: a 15ª entrada do arquivo público de erratas da âncora.

## O que isso significa

A esteira completa de revisão sistemática em hardware de consumidor agora tem receita, medida etapa por etapa: **extrair com o gemma4:12b na GPU integrada** (100% na parte 1, minutos por artigo), **calcular com o protocolo CALC** (o 27B fecha perfeito; o 14b quase, em fração do tempo), e **agregar sempre pela ferramenta — nunca pela cabeça de ninguém, humana ou artificial**. E uma lição de leitura crítica que vale além dos modelos: a honestidade deles é assimétrica — declaram "não calculável" quando faltam *dados*, mas não quando falta *capacidade*. Diante do IC, todos tentaram e erraram com confiança. Desconfie de qualquer estatística inferencial que um modelo (ou um humano apressado) entregue sem mostrar a conta.

## Limitações

Uma réplica pontuada por braço (a segunda mede estabilidade); o protocolo CALC é uma implementação particular de ferramenta — tool calling nativo pode se comportar diferente; os insumos herdam as extrações (e perturbações) da parte 1 por desenho; o braço thinking é exploratório, de uma réplica, num único modelo. E a auditoria da âncora cobre a aritmética das tabelas — não os dados que entraram nelas (esses foram o assunto da parte 1).

*Na parte 3: a pergunta que os dois estudos deixaram armada — dá para rodar a esteira inteira, do PDF ao forest plot, num mini-PC sem nuvem, e entregar uma mini-metanálise auditável de ponta a ponta? A fila decide.*
