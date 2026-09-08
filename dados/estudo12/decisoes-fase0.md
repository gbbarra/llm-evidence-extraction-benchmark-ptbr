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

**DECIDIDO em 2026-09-08 pelo pesquisador: opção 2 — entra o agrupador de razão de chances, e ganha-se a
comparação dígito a dígito com o diamante publicado.** A razão de risco vai reportada ao lado, pelo motor
congelado, em toda tabela de resultado da âncora 3.

**Descoberta que muda o alcance desta decisão, medida em 2026-09-08.** Recuperada a Figura 3 (ver Decisão
4), foi possível testar o agrupador contra o diamante publicado antes de rodar qualquer modelo. O
resultado: **o `pool_or_dl` não reproduz o 0,73.** Devolve 0,737 [0,449; 1,208] com tau² 0,1065. O que
reproduz, dígito a dígito, é o estimador de **Paule-Mandel** com o ajuste de **Hartung-Knapp**: tau²
0,1334, os oito pesos idênticos aos impressos, intervalo [0,40; 1,36]. Isso não é defeito do instrumento
nem da leitura; é a revisão ter usado outro estimador — que é o padrão do pacote `meta` do R nas versões
recentes, e que ela não declara nos métodos.

Consequência prática, e ela é boa: a comparação dígito a dígito continua possível, mas passa a ter **dois
alvos declarados em vez de um**, e o protocolo tem de dizer qual é qual antes de rodar.

| Caminho | Quem o roda | Contra o quê é comparado |
|---|---|---|
| DerSimonian-Laird sobre log OR | o motor do banco, `e12-or.py` | o mesmo caminho aplicado às células do gabarito — mede o modelo, não a revisão |
| Paule-Mandel com Hartung-Knapp | só o conferidor, `verificar-figura3.py` | o diamante publicado — mede a revisão, não o modelo |

Sem essa separação, um modelo que extraísse as dezesseis células **corretamente** seria reprovado por não
chegar a 0,73, quando a distância inteira vem do estimador. O erro teria sido atribuído ao modelo. Este é
exatamente o tipo de contaminação que o portão de generalização existe para não deixar passar, e ele foi
apanhado antes do primeiro token, porque a chave foi construída antes do protocolo ser congelado.

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

**DECIDIDO em 2026-09-08 pelo pesquisador: opção (a) — vai tentar obter os quatro faltantes.**

**A lista dos quatro mudou, e ficou mais fácil.** A recuperação da Figura 3 (Decisão 4) mostrou quais são
de fato os oito ensaios da análise primária, e não são os que a Tabela 1 sugeria:

| Ensaio | No gráfico de floresta | Primário | Situação |
|---|---|---|---|
| Luis-Silva, 2024 | sim | PMC11514138 | aberto, baixado, **camada 2 confere** |
| Shaker, 2025 | sim | PMC11707904 | aberto, baixado, **camada 2 diverge** (ver A3-D1) |
| Ibarra-Estrada, 2023 | sim | PMC10010212 | aberto, baixado, **camada 2 confere** |
| Dong, 2025 | sim | PMC12751372 | aberto, baixado, **camada 2 confere** |
| Aguilar, 2016 | sim | — | **falta** |
| Kirov, 2001 | sim | — | **falta** |
| Levin, 2004 | sim | — | **falta** |
| Memis, 2002 | sim | — | **falta** |
| Kuri, 2025 | **não** | PMC11915450 | aberto, baixado, **fora da análise de mortalidade** |

Três correções ao que este arquivo dizia antes:

1. O Kuri 2025 está baixado mas **não entra na análise primária**. Não é um dos nove: a Tabela 1 lista
   nove ensaios, o agrupamento usa oito, e o que sai é o Kuri, não o Levin.
2. O Levin 2004 **entra**, ao contrário do que a seção 3.5 da revisão afirma em texto. E o par que este
   arquivo dizia ser recuperável da Tabela 1 — 0/28 contra 6/28 — está confirmado pela figura.
3. A preocupação com a janela de seguimento era pertinente mas não é fatal: a Tabela 1 registra
   seguimento de 24 a 96 horas, e ainda assim o Luis-Silva publica mortalidade em **30 dias** e o Dong em
   **28 dias**. A coluna de seguimento da Tabela 1 descreve a janela hemodinâmica, não a do desfecho
   agrupado. Fica como discrepância pendente (A3-D5) para os quatro fechados.

**A camada 1 já está completa e verificada para os oito.** O que os quatro fechados fazem é fechar a
**camada 2** — a verificação na fonte, com citação — de quatro ensaios entre oito, e resolver a
discrepância A3-D2 do Aguilar. A Fase 1 já não está bloqueada por eles: está bloqueada apenas a metade
de auditoria da chave, e o que ela custa está escrito em `ancora3-camada1.json`.

---

## Decisão 4 — a chave da âncora 3 tinha uma camada, não duas

### Primeiro, o que é uma chave de duas camadas

Isto foi mal explicado antes e é o que a decisão inteira depende de entender.

Quando um modelo lê os artigos primários e devolve uma tabela de células — mortos e total em cada braço
de cada ensaio —, é preciso ter contra o que conferir. A campanha confere contra **duas coisas
diferentes**, e elas respondem a perguntas diferentes:

| | O que é | De onde vem | Que pergunta responde |
|---|---|---|---|
| **Camada 1** | o que a revisão publicou | a tabela da própria revisão | o modelo chega ao mesmo lugar que os extratores humanos chegaram? |
| **Camada 2** | o que a fonte diz | o artigo primário, com a frase transcrita | o modelo chega ao lugar **certo**? |

Ter as duas é o que separa este banco de um exercício de cópia. Quando as duas concordam, medir contra
qualquer uma dá no mesmo. **Quando discordam, a discordância é o resultado**: significa que os humanos
erraram, e o modelo que acertou a fonte estaria sendo reprovado por acertar. Foi assim que a âncora 1
produziu a errata de dezessete entradas — dezessete células em que a revisão publicada não bate com o que
os ensaios dizem.

**O problema da âncora 3 era este:** a camada 2 estava disponível como sempre, mas a camada 1 quase não
existia. A revisão imprime em texto **um único número agrupado** — o OR 0,73 (IC 95% 0,40 a 1,36), na
seção 3.5 e na tabela GRADE — e nenhuma célula por ensaio. As dezesseis células, os oito intervalos e os
oito pesos existiam só dentro da **Figura 3**, um gráfico de floresta em imagem. Sem eles, a âncora 3
mediria os modelos mas não poderia auditar os humanos, e o portão de generalização perderia metade do que
o torna interessante.

### O que foi feito

**RESOLVIDA em 2026-09-08. A camada 1 existe, está completa e está verificada.** Três passos:

**1. O pacote suplementar foi baixado e não tinha os dados.** `jcm-15-04481-s001.zip`, no Europe PMC,
contém três páginas: estratégias de busca por base e a lista de excluídos com motivo. Nenhuma célula.
Essa porta estava fechada e agora está fechada por medição, não por suposição.

**2. A Figura 3 foi lida.** O gráfico é do tipo produzido pelo pacote `meta` do R, que **imprime as
colunas de eventos e totais como texto dentro da imagem**. Não é um gráfico do qual se estima valor
medindo pixel: os números estão escritos. Foram lidos por visão em 2026-09-08.

**3. A leitura foi verificada por reconstrução, e é isso que a torna utilizável.** Ler imagem por visão
não produz citação — não há frase para transcrever —, e a regra do projeto é que veredito sem citação não
entra em gabarito. A saída não foi flexibilizar a regra; foi submeter a leitura a um teste que uma
leitura errada não passaria. Se as dezesseis células lidas forem as verdadeiras, então elas têm de
prever, por caminhos que não são o da leitura, tudo o mais que está impresso:

| O que foi previsto | Confere com |
|---|---|
| os denominadores por braço dos 7 ensaios de dois braços | a Tabela 1, que é texto XML de verdade, não imagem |
| as somas 213 e 218 | as linhas de total da própria figura |
| 8 razões de chances e 16 limites de intervalo | recalculados pelo motor do banco |
| qui-quadrado 8,89, 7 graus de liberdade, I² 21,3% | a linha de heterogeneidade da figura |
| os 8 pesos do modelo aleatório | a coluna de peso da figura, ao décimo |
| o diamante 0,73 [0,40; 1,36] | a linha de total da figura |

**48 de 48 valores impressos previstos a partir de 16 células lidas.** O script é
`scripts/estudo12/verificar-figura3.py` e roda em segundos. A chave está em
`dados/estudo12/ancora3-camada1.json`, com a procedência declarada: coordenada na figura mais
verificação aritmética, **e não citação**. O protocolo dirá isso com todas as letras.

### O que a verificação encontrou de quebra

Reproduzir a figura exigiu descobrir **como** ela foi calculada, e o caminho óbvio não era o certo. Está
registrado na Decisão 1: a revisão usou Paule-Mandel com Hartung-Knapp, não DerSimonian-Laird, e não
declara isso nos métodos. Sem essa descoberta, um modelo que extraísse as dezesseis células
**corretamente** seria reprovado por não chegar a 0,73.

E a camada 2, conferida nos quatro primários abertos que estão na análise, já devolveu **um erro duro na
revisão publicada**:

> **Shaker 2025.** A revisão registra 15/30 no braço de azul de metileno. O ensaio tem **três** braços:
> placebo 14/30, azul 1 mg/kg 9/30, azul 4 mg/kg 6/30. A revisão **somou os eventos dos dois braços de
> azul (9 + 6 = 15) e manteve o denominador de um braço só** — 30 onde deveriam ser 60.
>
> Sozinho, o Shaker vai de OR 1,14 [0,41; 3,15] para **0,38 [0,15; 0,96]**: de discretamente contra o
> azul para significativamente a favor. No diamante, com peso de 16,9%, o agrupado vai de 0,73 [0,40;
> 1,36] para **0,60 [0,33; 1,12]**.
>
> A conclusão da revisão sobrevive — continua sem significância —, mas o número publicado muda.

Os outros três abertos conferem célula a célula, com citação. Faltam quatro, todos fechados (Decisão 3),
e um deles carrega uma discrepância **interna à própria revisão**, ainda por resolver: a Figura 3 dá o
Aguilar 2016 como 24/30 contra 19/30, OR 2,32, **a favor do controle**, enquanto a Tabela 1 da mesma
revisão registra redução de mortalidade para o mesmo ensaio. As cinco discrepâncias candidatas estão
catalogadas em `ancora3-camada1.json`, duas já confirmadas dentro da própria revisão sem precisar de
fonte nenhuma: a seção 3.5 descreve uma composição de oito ensaios que não é a da figura, e o `n = 479`
da tabela GRADE não é o 431 que a figura soma.

### O que isso muda no desenho

A âncora 3 deixa de ser a âncora fraca. Entra com **camada 1 completa e verificada, camada 2 já em
construção com um erro confirmado, e cinco discrepâncias catalogadas antes do primeiro token**. É a
primeira âncora em que o gabarito foi fechado antes de qualquer modelo rodar, e não depois — o que é
exatamente a ordem que o pré-registro exige e que as âncoras 1 e 2 só conseguiram em parte.

Uma coisa não muda e vale dizer: **nada disso é acessível aos modelos.** Eles leem os primários e
devolvem células. A figura, o suplementar e este arquivo são material de correção, e ficam do lado do
conferidor, como a lente de desperturbação sempre ficou.

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

**DECIDIDO em 2026-09-08 pelo pesquisador: fica o elenco de seis, com o Argos, que é o que já estamos
usando. A segunda tag não entra.** A nota de hardware muda de contexto: a medição de pegada de memória
passa a ser feita em **24.576**, não em 16.384, para acompanhar a Decisão 6.

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

**Medidos em 2026-09-08, depois que o corpus fechou.** Os oito primários da análise de mortalidade
estão no repositório, e a decisão sobrevive à medição completa:

| Primário | Formato | Tokens estimados | Mais ficha e saída | Folga em 24.576 |
|---|---|---|---|---|
| Dong 2025 | XML | 14.741 | 19.641 | 4.935 |
| Kirov 2001 | PDF em texto | 14.260 | 19.160 | 5.416 |
| Luis-Silva 2024 | XML | 13.787 | 18.687 | 5.889 |
| Ibarra-Estrada 2023 | XML | 13.225 | 18.125 | 6.451 |
| Aguilar 2016 | PDF em texto | 13.083 | 17.983 | 6.593 |
| Shaker 2025 | XML | 11.630 | 16.530 | 8.046 |
| Memis 2002 | PDF em texto | 10.349 | 15.249 | 9.327 |
| Levin 2004 | PDF em texto | 5.566 | 10.466 | 14.110 |

Nenhum estoura. O pior caso continua sendo o Dong, que já estava medido; nenhum dos quatro recém-obtidos
o supera. **24.576 fica, e agora por medição do corpus inteiro e não por extrapolação de cinco nonos.**

**Testado na máquina em 2026-09-08, com o maior modelo (o 27B, 11 GB):** carrega e responde em 24.576,
em 32.768 e em 40.960 de contexto, sempre **100% na GPU integrada**, sem cair para a CPU. O custo é
tempo de processamento do prompt, proporcional ao tamanho do prompt e não ao teto declarado.

**DECIDIDO em 2026-09-08 pelo pesquisador: 24.576, uniforme para os seis modelos e as três âncoras.**
Cobre o pior primário aberto da âncora 3 com quase 5.000 de folga e dá margem para os quatro fechados
ainda desconhecidos. A uniformidade evita que o contexto vire variável confundida entre âncoras. A
mudança quebra a comparabilidade direta com o registro atual, que rodou em 16.384, e o protocolo deve
declarar que a motivação foi esta medição.

---

## Instrução de operação — retomada obrigatória

**Dada pelo pesquisador em 2026-09-08:** *"Não temos problemas de horas, pode rodar tranquilo, faça de
forma que se for interrompido possamos continuar de onde parou."*

Isso é uma restrição de projeto, não uma preferência, e vale para as Fases 3 a 5 inteiras. Traduzida em
requisito verificável, e o orçamento de 43 horas de máquina a torna inegociável:

| Requisito | Como se cumpre |
|---|---|
| Toda chamada gravada assim que volta | uma saída por arquivo, nomeada por âncora, ficha, modelo e ensaio; nada acumulado em memória até o fim |
| Retomar é pular o que existe | antes de chamar, verificar se o arquivo de saída já existe e está íntegro; se estiver, seguir |
| Interrupção não corrompe | escrever em arquivo temporário e renomear ao fim; renomeação é atômica, escrita não é |
| Trocar de modelo é ponto de parada seguro | um modelo residente por vez, `ollama stop` entre eles, e a fronteira entre modelos é onde a retomada custa menos |
| Saber onde parou sem adivinhar | um inventário que conta o que existe contra o que o protocolo prevê, rodável a qualquer momento |
| Reprovado é registrado, não apagado | vale a regra de sempre: saída ruim fica gravada com o motivo |

O harness já grava por chamada. O que falta é o **portão de retomada** e o **inventário**, e os dois
entram na Fase 2, junto com o congelamento do protocolo — não como conserto depois da primeira queda.

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
