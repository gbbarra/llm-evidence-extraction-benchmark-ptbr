# Campanha de três âncoras e seis modelos — decisões da Fase 0

**Nada foi registrado e nada rodou.** Este arquivo reúne o que precisa ser decidido, por escrito, antes
de o protocolo ser congelado. Cada decisão traz as opções, o que cada uma custa, e a recomendação com o
motivo. A decisão é do pesquisador.

O que a campanha muda em relação à atual: **seis modelos desde o início**, sem elenco de duas classes e
sem braço de extensão, e **três âncoras**, o que responde à limitação que o próprio manuscrito declara
hoje ("two anchors from a single journal family and 21 primaries are the whole evidence base").

---

## Decisão 1 — razão de risco ou razão de chances na âncora 3

**O problema.** O motor congelado (`scripts/estudo2/e2-harness.py`) agrupa razão de risco e diferença de
médias, e só isso. A âncora 3, azul de metileno no choque do adulto (PMC13302755), publica o desfecho
primário como **razão de chances**: OR 0,73 (IC 95% 0,40 a 1,36) para mortalidade em 28 a 30 dias, 8
estudos. Reproduzir esse estimando exige agrupar no log da razão de chances.

| Opção | O que ganha | O que perde |
|---|---|---|
| 1. Comparar em razão de risco | o motor fica intocado, que é a lógica do portão de generalização | não há número publicado ao lado do qual pousar |
| 2. Acrescentar o agrupador de razão de chances | comparação dígito a dígito com o diamante publicado | o motor sob teste deixa de ser o que os estudos anteriores congelaram |

**Recomendação: opção 2, com a razão de risco reportada junto, e o instrumento construído ANTES de
congelar o protocolo, não como emenda no meio da campanha.** A pergunta do portão de generalização é se
a arquitetura transfere para outro domínio e outro estimando, não se uma função ficou sem tocar.
Reportar os dois estimandos mantém o resultado do motor intocado no registro.

**Estado: o instrumento está pronto e validado**, em `scripts/estudo12/e12-or.py`. Ele importa o motor
congelado e não o edita; reusa a regra de continuidade verbatim; acrescenta `odds_ratio`, `ci95_or`,
`pool_or_mh` (Mantel-Haenszel com variância de Robins-Breslow-Greenland) e `pool_or_dl`
(DerSimonian-Laird no log da razão de chances). As oito verificações passam:

| # | Verificação | Como é conferida |
|---|---|---|
| 1 | identidade OR = RR × (1−pc)/(1−pe) | contra a função `rr` congelada |
| 2 | intervalo de Woolf | pelo caminho explícito 1/a + 1/b + 1/c + 1/d |
| 3 | Mantel-Haenszel | pelo somatório de produtos, calculado no próprio teste |
| 4 | variância de Robins-Breslow-Greenland | pelos três termos explícitos |
| 5 | convergência em evento raro | o agrupamento em OR se aproxima do `pool_dl` congelado |
| 6 | simetria dos braços | trocar os braços inverte a razão |
| 7 | correção de continuidade | célula zero tratada pela regra congelada, com o caso real 0/28 contra 6/28 |
| 8 | heterogeneidade nula | DL colapsa no efeito fixo de variância inversa |

Nenhuma verificação usa o 0,73 publicado como valor esperado. Ele vira o caso de teste publicado desta
metade do motor quando a chave estiver completa, e reproduzi-lo será **resultado da campanha**, não
pré-condição do instrumento.

---

## Decisão 2 — ficha v1 ou ficha com citação obrigatória (v2)

**O problema.** "Harness no estado atual" é ambíguo. O Estudo 9 mediu a ficha v2, em que toda célula
carrega a frase literal da fonte, num A/B contra a v1 congelada. O veredito é dividido.

| Modelo | v1 | v2 | delta |
|---|---|---|---|
| gemma4:12b | 103/124 | 104/124 | +1 |
| qwen3:14b | 104/124 | 85/124 | −19 |
| llama3.1:8b | 88/124 | 79/124 | −9 |

A hipótese de acurácia preservada vale só para o gemma4:12b. A perda tem mecanismo nomeado: o qwen3:14b
escreve "não relatado" em vez de produzir uma citação que não consegue sustentar, e 18 das suas 28
omissões são do mesmo campo. A hipótese de falso alarme abaixo de 5% **falha nos quatro modelos**, por
um ponto cego em célula de tabela. O candidato v3, que deixaria a célula citar a linha da tabela, está
no backlog e não foi construído nem medido.

**Recomendação revista, depois de ler o registro inteiro do Estudo 9.** A primeira recomendação foi
"v1 apenas", e estava mal fundamentada: olhava a metade do resultado. O que o Estudo 9 diz por inteiro é
que a citação **custa transcrição descritiva e compra leitura meta-analítica**, e as duas coisas vivem em
camadas diferentes da mesma ficha. Nos diamantes da âncora 2:

| Modelo | v1 | v2 |
|---|---|---|
| gemma4:12b | −0,27 [−0,38; −0,17], I² 28,6% | **−0,24 [−0,32; −0,16], I² 7,6%** |
| llama3.1:8b | −0,60, 5 de 7 ensaios | −0,50, 7 de 7 |
| qwen3:14b | −0,63 | −0,53 |
| publicado | | −0,24 [−0,32; −0,16], I² 6% |

O gemma sob v2 reproduz o diamante publicado dígito a dígito, e a ressalva honesta que o manuscrito
atual carrega — a de que o melhor diamante não reproduz a homogeneidade da âncora — é fechada pelo
instrumento, não por aritmética melhor: o motor é idêntico. O custo, além disso, cai nos campos
descritivos que o próprio artigo diz que os motores nunca consomem, e o ganho cai na estimativa
agrupada. No único modelo com controle interno, a citação custou 32% mais tokens e 27% mais tempo, e
**reduziu à metade** a taxa de falha de leitura do JSON.

**DECIDIDO em 2026-09-08 pelo pesquisador: rodar as duas fichas, v1 e v2, como braço declarado da
campanha.** Seis modelos e três âncoras é exatamente a escala que o Estudo 9 disse não ter para decidir
("Four models on two anchors cannot settle this; it is stated so a later study can test it"). O que hoje
é hipótese registrada vira resultado. As redes de proveniência entram como braço exploratório, não como
critério, porque a hipótese de falso alarme abaixo de 5% falhou nos quatro modelos por ponto cego em
célula de tabela — defeito da rede, não da ficha.

**Custo:** dobra a extração. O orçamento revisado está no fim deste arquivo.

---

## Decisão 3 — os quatro primários fechados da âncora 3

**O problema.** Dos 9 ensaios, 5 estão abertos e já baixados (`dados/estudo11/primarios/`). Quatro são
fechados. E três deles têm janela de seguimento de 48 horas, 72 horas e 24 horas, o que significa que
**pode não existir neles um número de mortalidade em 28 a 30 dias** — que é justamente o desfecho que a
revisão agrupou.

| Opção | Consequência |
|---|---|
| a. Obter os quatro legalmente e ler | a chave fecha; dá para saber se o 0,73 se reproduz dos próprios insumos |
| b. Rodar com os cinco abertos, mais o Levin recuperável da Tabela 1 da revisão (0/28 contra 6/28) | 6 de 9 ensaios; a restrição vai declarada e o diamante não é comparável de frente |
| c. Trocar a âncora 3 | perde o portão de generalização já reconhecido |

**Recomendação: (a), e é trabalho do pesquisador** — obter artigo fechado não é coisa que eu faça. Se
não for possível, (b) com a restrição declarada no protocolo antes de rodar, nunca depois.

**Este é o item que governa o cronograma.** Sem ele resolvido, a Fase 1 não fecha.

---

## Decisão 4 — a chave da âncora 3 tem uma camada, não duas

**O problema.** As âncoras 1 e 2 têm chave de duas camadas: o que a revisão publicou e o que a fonte diz.
A âncora 3 **publica uma única estimativa em texto**: o OR 0,73 (IC 95% 0,40 a 1,36), que aparece na
seção 3.5 e na tabela GRADE. As estimativas por estudo, os pesos e o I² existem apenas na Figura 3, que
é uma imagem rasterizada. Conferido no XML em 2026-09-08.

**Recomendação: declarar que a chave da âncora 3 tem camada da fonte completa e camada da revisão com um
único valor, e tratar isso como resultado, não como limitação.** É a primeira âncora em que o registro
humano não é conferível célula a célula, e isso diz algo sobre prática editorial que o artigo deve dizer
com todas as letras.

**Correção ao reconhecimento de 2026-09-02.** Aquele arquivo afirma que a revisão "prints no numbers in
its Results prose". Isso vale para as estimativas por estudo, não para o diamante: a frase "The pooled
OR for 28–30-day mortality was 0.73 (95% CI 0.40–1.36)" está no corpo do texto. A afirmação original era
forte demais.

---

## Decisão 5 — a segunda tag do 27B não é um sétimo modelo

**Levantada pelo pesquisador em 2026-09-08.** Existe `smtek/Qwen3.8-27B:Q2_K_XL-16gb`, anunciada para
GPU de até 16 GB. Medido com `ollama show --modelfile`:

- **mesmo blob de pesos** que a tag simples (`sha256-dd04d13a…`), portanto os mesmos 27,32 bilhões de
  parâmetros a 3,13 bits por peso;
- **mesmo template**, `TEMPLATE {{ .Prompt }}`;
- diferenças: `num_ctx` 262144 contra 131072, e `draft_num_predict` 4 contra 0.

O harness fixa o contexto em 16.384 por chamada, o que sobrescreve as duas. Sobra a decodificação
especulativa, que muda velocidade e não leitura.

**Recomendação: não entra como sétimo braço.** Rodá-la custaria cerca de cinco horas para medir
configuração de execução, não leitura, e devolveria um quase duplicado do sexto modelo. O que ela
responde é uma pergunta de implantação, e essa merece **uma medição de pegada de memória no contexto de
16.384**, de meia hora, entrando no artigo como nota de hardware.

**Erro corrigido no caminho.** Ao medir isso descobri que o artigo e o registro afirmavam que o braço de
extensão rodou com "template de chat padrão". Está errado: o build carrega o template de prompt cru, o
mesmo do 27B da fase de desenvolvimento de instrumentos. Só a quantização é confundidor contra aquele
registro. Corrigido em `paper/extrai-unified.tex`, `MODELS.md` e `avaliacao-amend1.md`; o protocolo
pré-registrado recebeu nota datada e não foi reescrito.

---

## Decisão 6 — o contexto sobe de 16.384 para 24.576

**Levantada pelo pesquisador em 2026-09-08: "16.384 é suficiente?" A medição diz que não.**

Em 823 chamadas gravadas nenhuma foi truncada, mas a margem era fina e ninguém tinha olhado:

| Fase | Chamadas | Prompt mediano | Prompt máximo | Máximo mais 4.000 de saída |
|---|---|---|---|---|
| Âncora 1 (P1) | 168 | 9.805 | 11.558 | 15.558, cabe |
| Âncora 2 (P3-b) | 84 | 10.572 | 12.770 | 16.770, **não cabe** |

No pior caso real sobraram 613 tokens. A folga **nominal**, porém, chegou a 41 numa chamada e a −351 em
outra: se o modelo tivesse usado o orçamento de 4.000 que o harness oferece, teria batido no teto. Nada
quebrou porque as fichas da âncora 2 saíram curtas.

**A âncora 3 não cabe em 16.384.** Estimado pelos cinco primários abertos já baixados, com a razão de
3,21 caracteres por token medida no próprio corpus:

| Primário | Tokens do artigo | Prompt mais 4.000 de saída |
|---|---|---|
| PMC12751372 | 14.749 | 19.649 |
| PMC11514138 | 13.795 | 18.695 |
| PMC10010212 | 13.232 | 18.132 |
| PMC11707904 | 11.636 | 16.536 |
| PMC11915450 | 7.606 | 12.506, cabe |

Quatro dos cinco estouram, o pior por 3.265 tokens, e os quatro fechados ainda não foram medidos.

**Testado na máquina em 2026-09-08, com o maior modelo (o 27B, 11 GB):** carrega e responde em 24.576,
em 32.768 e em 40.960 de contexto, sempre **100% na GPU integrada**, sem cair para a CPU. O custo é
tempo de processamento do prompt, proporcional ao tamanho do prompt e não ao teto declarado.

**DECIDIDO em 2026-09-08 pelo pesquisador: 24.576, uniforme para os seis modelos e as três âncoras.**
Cobre o pior primário aberto da âncora 3 com quase 5.000 de folga e dá margem para os quatro fechados
ainda desconhecidos. A uniformidade evita que o contexto vire variável confundida entre âncoras. A
mudança quebra a comparabilidade direta com o registro atual, que rodou em 16.384, e o protocolo deve
declarar que a motivação foi esta medição.

---

## O que acontece depois que as decisões forem tomadas

**Fase 1** — corpus e chave da âncora 3, com as duas discrepâncias já achadas registradas: o n de 479
não bate com nenhum agrupamento que os primários permitem, e o Kuri declara não ter avaliado mortalidade.
**Fase 2** — protocolo único, registrado e congelado: seis modelos, três âncoras, cinco fases, hipóteses
numeradas, sem adendo.
**Fase 3** — a campanha, fila sequencial, um modelo residente por vez, retomável.
**Fase 4** — correção e adjudicação, com citação antes do veredito.
**Fase 5** — o artigo reescrito com seis modelos e três âncoras desde a primeira linha.

**Orçamento revisto depois das decisões 2 e 6**, pelas taxas medidas (2,8 minutos por chamada na âncora
1 e 2,2 na âncora 2, ambas medidas; mais 27% para a ficha v2, medido no único modelo com controle
interno; mais 35% na âncora 3, cujos artigos são maiores na mesma proporção dos tokens estimados):

| Âncora | Chamadas por ficha | v1 | v2 | Soma |
|---|---|---|---|---|
| 1 — fluidoterapia, 14 ensaios | 168 | 470 min | 598 min | 1.068 min |
| 2 — dieta, 7 ensaios | 84 | 185 min | 235 min | 420 min |
| 3 — azul de metileno, 9 ensaios | 108 | 410 min | 518 min | 928 min |
| **extração** | **720 chamadas** | | | **2.416 min** |

Somando a aritmética (72 corridas, cerca de 108 minutos) e a orquestração, dá **cerca de 43 horas de
máquina sequencial**, contra as 10,8 da campanha atual e as 18 a 20 que uma ficha só custaria. São dois
dias de máquina contínua, retomável, um modelo residente por vez. Correção, adjudicação e reescrita à
parte.

**Se esse custo for proibitivo**, a contenção com menor perda científica é rodar as duas fichas nas
âncoras 2 e 3, onde está a leitura meta-analítica que a v2 compra, e só a v1 na âncora 1, cujos campos
descritivos são justamente onde a v2 cobra e que os motores não consomem. Isso corta para cerca de 33
horas e mantém a pergunta do Estudo 9 respondida nas duas âncoras que importam para ela.

O artigo atual continua válido e é o registro até que haja o que o substitua.
