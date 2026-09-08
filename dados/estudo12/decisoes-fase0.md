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

**Recomendação: v1 como instrumento único da campanha, com o motivo escrito no protocolo e citando os
números acima.** Adotar um instrumento que o próprio A/B pré-registrado reprovou em três de quatro
modelos seria adotar por esperança. O ganho da v2 é real na leitura meta-analítica e está registrado;
ele volta quando a v3 existir e for medida.

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

## O que acontece depois que as cinco forem decididas

**Fase 1** — corpus e chave da âncora 3, com as duas discrepâncias já achadas registradas: o n de 479
não bate com nenhum agrupamento que os primários permitem, e o Kuri declara não ter avaliado mortalidade.
**Fase 2** — protocolo único, registrado e congelado: seis modelos, três âncoras, cinco fases, hipóteses
numeradas, sem adendo.
**Fase 3** — a campanha, fila sequencial, um modelo residente por vez, retomável.
**Fase 4** — correção e adjudicação, com citação antes do veredito.
**Fase 5** — o artigo reescrito com seis modelos e três âncoras desde a primeira linha.

**Custo estimado pelas taxas medidas** (2,8 minutos por chamada de extração na âncora 1; 2,2 na âncora
2): 168 chamadas na primeira, 84 na segunda, cerca de 108 na terceira, mais aritmética e orquestração —
**18 a 20 horas de máquina sequencial**, contra as 10,8 da campanha atual. Correção, adjudicação e
reescrita à parte.

O artigo atual continua válido e é o registro até que haja o que o substitua.
