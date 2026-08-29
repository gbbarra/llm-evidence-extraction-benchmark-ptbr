# EXTRAI, parte 3: montei uma esteira de metanálise com IAs locais se auditando — e o portão de qualidade fez mais estrago que a sabotagem que ele existia para pegar

*Nas partes 1 e 2, quatro modelos locais provaram que extraem evidência quase sem erro e que calculam perfeitamente — desde que alguém aperte as etapas uma a uma. Faltava a pergunta de produção: e se ninguém apertar? O Estudo 3 ligou as etapas em série: um modelo extrai, outro audita campo a campo, o auditado vira insumo da calculadora, a calculadora alimenta a síntese, e um script desenha o forest plot — sete ensaios clínicos entrando, uma metanálise saindo, num mini-PC, sem nuvem. Para medir se a auditoria é real, semeei oito erros deliberados nas fichas. O placar: 9 de 10 células sabotadas foram pegas, com a citação literal da prova. Mas a contabilidade da propagação guardava a ironia do estudo: a sabotagem não detectada moveu o resultado final em 0,02; as correções falsas do próprio auditor — junto com um sinal que o calculista trocou por achar implausível — moveram 0,13. E no fim, desfeitas as perturbações, o diamante da esteira pousou ao lado do publicado: −0,28 contra −0,24.*

> 📄 Série EXTRAI: [parte 1](ARTIGO1.md) · [parte 2](ARTIGO2.md) · parte 3 (esta) · Dados, protocolos pré-registrados e correção mecânica: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Benchmark irmão: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## O contexto, para quem chega agora

Uma metanálise — o estudo que junta os resultados de vários ensaios clínicos numa única estimativa — é feita de três ofícios: extrair os números de cada artigo, conferi-los, e agregá-los com estatística. A parte 1 mediu o primeiro ofício isolado (624 células, 1 erro); a parte 2 mediu o terceiro (de cabeça: nenhum intervalo de confiança certo em 30 tentativas; com calculadora: um modelo fechou perfeito). O Estudo 3 pergunta o que acontece quando os ofícios se encadeiam **sem humano no meio** — cada etapa entregue ao modelo que venceu a medição anterior, como quem escala um time pelos números do campeonato. E acrescenta o ofício do meio, nunca testado: **um modelo auditando o trabalho do outro**, campo a campo, contra o artigo original.

Duas defesas de desenho, herdadas da série: os textos que os modelos leem são **perturbados** (números discretamente alterados — devolver o valor publicado denunciaria memória de treino, não leitura; os sete ensaios aqui são de 2016–2023, anteriores ao corte dos modelos, e a perturbação converte qualquer lembrança em sinal detectável); e a correção é **mecânica** — scripts comparam célula a célula, e o juiz humano-assistente só arbitra empates, obrigado a citar a fonte. O juiz, aliás, foi corrigido três vezes neste estudo. De novo.

## O que exatamente foi feito

A âncora: **"Effect of Low-Carbohydrate Diets on Glycemic Control in Type 2 Diabetes Mellitus: A Systematic Review and Meta-Analysis of Randomized Controlled Trials"** ([Cureus, junho de 2026, acesso aberto CC BY](https://doi.org/10.7759/cureus.108479)) — uma metanálise de 7 ensaios randomizados (562 participantes) sobre dietas de baixo carboidrato no controle da hemoglobina glicada (HbA1c, o exame que resume a glicemia de ~3 meses) em diabetes tipo 2. Publicada *depois* do corte de treino dos modelos. Nota de justiça, como sempre: os autores não estão em julgamento — a âncora foi escolhida por ser auditável (aberta, recente, com forest plot completo), e a aritmética dela saiu **impecável** da nossa verificação: as 42 células do gabarito reproduzem dígito a dígito sob as regras de derivação que documentamos (intervalos→desvios, erros-padrão→desvios, imputação r=0,5 do manual Cochrane).

A esteira, com cada etapa escalada pelo vencedor medido:

*Como ler: etapa, quem executa, por que ele, e o volume.*

```
etapa            modelo         por quê              corridas
E  extração      gemma4:12b     100% na parte 1        7×2
A  auditoria     qwen3.8:27b    campeão da parte 2;   7×2 lanes
                                família independente
C  aritmética    qwen3.8:27b    8/8+8/8 com CALC       2
S  síntese       gemma4:26b     melhor texto longo     2
F  forest plot   script (sem modelo — determinístico)  2
```

**As duas lanes**: a auditoria rodou duas vezes sobre as mesmas fichas — a lane **L** (limpa, as fichas reais da extração) e a lane **S** (semeada: 8 erros deliberados plantados em 5 fichas — trocas de braço, sinais invertidos, dígitos alterados, números transpostos — com 2 fichas intactas de controle; a lista foi selada ANTES de qualquer corrida e o auditor nunca soube se ou quantos erros existiam). O que o auditor aprova segue para a calculadora — então erro não pego **propaga**, e a esteira mede o custo disso no resultado final.

Fila completa: 32 corridas em 272 minutos no mini-PC (Ryzen 7, GPU integrada para o 12b, CPU para os grandes). Correção 100% mecânica com régua pública; adjudicações com citação literal; selos de perturbação e sementes publicados junto com a correção.

## O que encontramos

### 1. A esteira inteira funciona — e o resíduo dela tem nome e sobrenome

O produto final da lane limpa, estudo a estudo, ao lado do que a metanálise publicou. MD é a diferença de médias na variação de HbA1c (negativo favorece a dieta low-carb); o IC95% é a faixa de incerteza; os valores da esteira vivem no mundo *perturbado* (por desenho, os números de entrada foram alterados — as diferenças por estudo refletem isso e as escolhas de rota, nunca conta errada).

*Como ler: o MD [IC95%] que a esteira computou vs o publicado pela metanálise.*

```
estudo          esteira (lane L)         publicado (âncora)
Saslow 2017     -0.50 [-0.89, -0.11]     -0.50 [-0.89, -0.11]
Saslow 2023     -0.18 [-0.37, +0.01]     -0.21 [-0.40, -0.02]
Dorans 2022     -0.20 [-0.29, -0.11]     -0.22 [-0.31, -0.13]
Chen 2020       -0.43 [-0.78, -0.08]     -0.62 [-1.13, -0.11]
Thomsen 2022    -0.27 [-0.45, -0.09]     -0.17 [-0.35, +0.01]
Wang 2018       -0.32 [-0.87, +0.23]     -0.26 [-0.74, +0.22]
Goday 2016      -1.30 [-1.56, -1.04]     -0.50 [-0.90, -0.10]
```

E os diamantes — o agregado de efeitos aleatórios (DerSimonian-Laird, "DL") que resume tudo, com o I² medindo a heterogeneidade (quanto os estudos discordam entre si):

*Como ler: quatro agregados — o que o modelo emitiu, a verdade mecânica sobre as MESMAS fichas, a esteira com as perturbações desfeitas, e o publicado.*

```
agregado                          MD      IC95%           I²
modelo (lane L)                  -0.39   [-0.60, -0.18]   76%
verdade mecânica (mesmas fichas) -0.52   [-0.81, -0.22]   91%
esteira DESPERTURBADA            -0.28   [-0.39, -0.17]   32%
âncora publicada                 -0.24   [-0.32, -0.16]    6%
```

📊 *[IMAGEM AQUI: o forest plot da esteira — quadrados/diamante = pipeline; pontos cinza = âncora publicada. Arquivo: `forest-pipeline-L.png`; legenda sugerida: "A metanálise que a esteira produziu, sobreposta à publicada — o outlier do Goday é a perturbação em ação."]*

A linha que importa é a terceira: revertendo as perturbações seladas e agregando mecanicamente as fichas auditadas, a esteira chega a **−0,28 [−0,39, −0,17]** onde a metanálise publicou **−0,24 [−0,32, −0,16]** — mesma direção, mesma significância, intervalos sobrepostos. E o resíduo se decompõe inteiro em escolhas nomeadas: o Wang tem *duas* tabelas de análise e a esteira leu a gêmea (populações 24/25 vs 28/28); o Chen carrega dispersões danificadas pela auditoria (achado 4); os n analisados diferem dos randomizados. **Nada no vão é aritmética.**

### 2. A extração segurou a esteira: 98%, com réplicas idênticas

*Como ler: células certas/pontuadas por ensaio (réplica 1; a réplica 2 saiu IDÊNTICA célula a célula — estabilidade 100%). 🔒 = obtido legalmente fora do acesso aberto.*

```
ensaio            células   nota
Saslow 2017        15/15    leu os basais perturbados 5.8/7.6
Saslow 2023 🔒      9/13*   fatorial 2×2 identificado; ns de
                            célula (23/25) vs margens — *4
                            células adjudicadas como literais
Dorans 2022        13/13    leu -0.24 e total 141 perturbados
Chen 2020          13/17*   as 2 ÚNICAS ERRADAS do estudo: DPs
                            do ponto-final colados na mudança
                            (a dispersão certa era o IC)
Thomsen 2022 🔒    15/15    leu -0.56 e 8.09 perturbados
Wang 2018          11/11    leu a tabela gêmea — rota literal
Goday 2016         17/17    deixou a mudança como NR (correto:
                            o texto só dá basal e final)
TOTAL              99/101 = 98% · 0 omissas · 0 recitações
```

Zero recitações atribuíveis: em todos os alvos válidos, os modelos devolveram o valor perturbado — o que só existe no texto que leram. (A perturbação também levou lições para o manual: números **por extenso** sobrevivem ao operador — "Seventy-two" ficou de pé onde o dígito 72 virou 63 — e totais com parcelas à vista não provam recitação. Tudo documentado como emenda antes de corrigir a auditoria.)

### 3. A auditoria é real — pega 9 de 10 — e tem personalidade

As oito sementes, uma a uma, contra o veredito do auditor (que não sabia se havia erros):

*Como ler: o que foi plantado, e o que o auditor fez — "pegou+corrigiu" exige o valor certo COM citação literal do texto.*

```
semente                     ficha         veredito do auditor
troca de braços (mudanças)  Chen          PEGOU+corrigiu (2/2,
                                          citações literais)
troca de braços (mudanças)  Thomsen       PEGOU+corrigiu (2/2)
sinal invertido (+0.32)     Saslow 2023   PEGOU+corrigiu (-0.32)
sinal invertido (+0.31)     Wang          PEGOU+corrigiu (-0.31)
n transposto (73→37)        Dorans        PEGOU (corrigiu p/ 75,
                                          rota aceita)
n transposto (34→43)        Thomsen       PEGOU+corrigiu (34)
dígito no basal (9.99)      Chen          pegou, corrigiu ERRADO
                                          (valor do outro braço)
dígito DENTRO do IC (-0.37) Dorans        NÃO PEGOU (confirmou)
---
células sabotadas pegas: 9/10 (90%) · correção exata: 8/9
falso alarme real: 6,5% (lane L) e 5,9% (lane S)
fichas intactas de controle: atravessaram limpas
```

A previsão direcional do pré-registro cravou: **erros semânticos (braços, sinais) caem todos, com a prova literal; erros de caractere escapam** — o dígito escondido dentro da string de intervalo foi o único a passar batido. E o auditor tem cinco cacoetes, todos com registro literal: soma as células do fatorial para achar as margens que a metanálise usou (genial); **imputa valores que computa em vez de verificar** — chegou a corrigir um n para **"24,5 pacientes" citando no próprio veredito o "(n = 28)"** que o desmente; inverte o mapa de colunas de tabela ambígua (desfez a troca semeada das mudanças do Chen e, no mesmo gesto, trocou os basais dos braços); desempata a contradição dígito-vs-extenso ora para um lado, ora para outro; e muda de veredito entre lanes sobre a mesma célula.

### 4. A ironia central: o portão fez mais estrago que a sabotagem

A contabilidade da propagação, em centésimos de HbA1c no diamante final:

*Como ler: quem moveu o agregado, e quanto.*

```
causa                                        efeito no diamante
semente NÃO detectada (dígito no IC do        0.02
estudo dominante — infla o erro-padrão
e derruba o peso do Dorans)
correções FALSAS do auditor no Chen +         0.13
sinal trocado pelo calculista no Goday
(split 37/38 fabricada; dispersões
trocadas de braço; -0.3 onde era +0.3)
```

A sabotagem plantada custou 0,02 — proporcional ao peso do estudo, como a hipótese previa. As falhas *espontâneas* do próprio portão de qualidade custaram seis vezes mais. Para quem monta esteira de verdade, a receita muda de figura: **as correções do auditor valem como bandeiras para reverificação na fonte — nunca como consertos auto-aplicados.**

### 5. A cabeça volta pelas frestas — três vezes

Mesmo com a calculadora obrigatória, o "de cabeça" da parte 2 reapareceu em três frestas diferentes. **Primeira**: o controle perturbado do Goday *piorou* (+0,3 de HbA1c); o calculista, com todas as chamadas à disposição, escreveu −0,3 — a chamada literal:

```
CALC: md(-1.6, 0.46, 45, -0.3, 0.7, 40)
                         ^^^^
        a verdade da ficha era +0.3 (controle piorou);
        o modelo recusou o sinal implausível
```

**Segunda**: o pool foi orquestrado via ferramenta (avanço sobre a parte 2, onde ninguém conseguiu) — mas alimentado com um *terceiro conjunto* de dispersões, diferente das que o próprio modelo tinha acabado de usar nas chamadas por estudo:

```
Saslow 2017 nas chamadas por estudo:  dp 0.42 / 0.43
Saslow 2017 na chamada do pool:       dp 0.9  / 1.2
```

A falha da parte 2 subiu um nível de abstração: de "não chama a ferramenta" para "chama com insumos não reconciliados". **Terceira**: as sínteses, com todos os agregados em mãos, somaram os participantes *de cabeça* — e erraram as duas somas (479 e 494, contra 542 reais das próprias fichas). Três estudos, uma moral: **número de modelo local sem a conta à mostra é decoração — mesmo dentro de uma esteira construída para impedir exatamente isso.**

### 6. O juiz caiu três vezes — e a régua é parte do experimento

O rito ("verificar na fonte antes de deduzir") voltou a cobrar do adjudicador. Três correções da régua, públicas: a primeira versão do gabarito não tinha rotas literais que os modelos usaram (o "0% (0/8)" do Saslow, os "(n = 73)…(n = 69)" do Dorans, o "CD 36, CRHP 36" do Thomsen, a tabela gêmea inteira do Wang); o casamento de nomes por sobrenome mandou o "Saslow 2023" para a régua do "Saslow 2017"; e — a mais instrutiva — o parser de intervalos leu o **"95" de "IC95:"** como limite inferior, produzindo verdades de ±68 pontos… enquanto **o modelo tinha computado os limites certos**. Terceiro estudo seguido em que um modelo local acerta antes do juiz. A régua corrigida, com cada mudança datada, está no repositório — porque num benchmark honesto, a régua também é resultado.

## O que isso significa

A revisão sistemática em hardware de consumidor saiu do "cada etapa funciona" para o "a esteira funciona": PDF entra, forest plot sai, 4,5 horas, zero dólares de nuvem, e um resíduo final que se explica linha a linha. A receita, medida em três estudos: **extrair com o disciplinado** (gemma4:12b), **auditar com o numérico** (qwen3.8:27b) *tratando correções como bandeiras*, **calcular e agregar sempre pela ferramenta** com o harness ecoando os insumos do pool contra as chamadas por estudo, **entregar totais pré-computados à síntese** — e manter a rede de fechamento forçado armada, mesmo que nesta fila ela nunca tenha disparado. E a lição transversal, para humanos inclusive: o elo mais perigoso de uma esteira de evidência não é o erro que alguém planta — é a correção confiante que ninguém confere.

## Quem fez o quê

**Os modelos locais**: gemma4:12b leu os 7 textos perturbados e preencheu 14 fichas; qwen3.8:27b auditou 14 fichas campo a campo e orquestrou os 2 agregados via CALC; gemma4:26b escreveu as 2 sínteses. **O harness** rodou a fila, executou as chamadas em Python (funções validadas contra a âncora antes da largada: o diamante publicado reproduz dígito a dígito), plantou as sementes seladas e montou as fichas auditadas. **O corretor mecânico** rotulou cada célula contra a régua pública. **O Claude (assistente)** desenhou o estudo com o autor, verificou o gabarito na fonte (42/42), adjudicou com citação obrigatória — e registrou as próprias três erratas. **O autor** caçou os PDFs fechados legalmente, decidiu o desenho e revisou tudo.

## Limitações

Uma configuração de esteira (um extrator, um auditor, um calculista — os vencedores medidos; outros elencos podem se comportar diferente); uma âncora com um único desfecho contínuo; lanes de uma réplica (as duas réplicas da extração mediram estabilidade; auditoria/cálculo/síntese rodaram uma vez por lane). O catch rate do auditor sobre erros *genuínos* repousa em 2 células (a extração errou pouco demais para testá-lo em volume). A comparação ponta-a-ponta com a âncora depende do mapa de desperturbação — selado antes das corridas e publicado com a correção.

*A série EXTRAI fecha seu primeiro arco aqui: extração (parte 1), aritmética (parte 2), esteira (parte 3) — protocolos, dados, erratas e selos no repositório, DOI na capa. O que vem depois — mais elencos, mais âncoras, outros desfechos — o roadmap decide.*
