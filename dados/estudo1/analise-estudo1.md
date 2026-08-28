# EXTRAI — Análise do Estudo 1 (vereditos e achados)

Encerrado em 2026-08-28. Números completos na [avaliação](avaliacao-estudo1.md); erros
da âncora e do adjudicador em [erratas-da-ancora.md](erratas-da-ancora.md).

## Vereditos das hipóteses pré-registradas

| Hipótese | Predição | Veredito |
|---|---|---|
| **H1.1** — inversão de ordem (27B ≥ 26b > 12b ≥ 14b na extração) | os grandes fiéis vencem | **REFUTADA.** Ordem real: 12b = 26b (100%) > 27B (98%) > 14b (90%). A disciplina gemma venceu a extração também. Nuance real a favor dos grandes: o 27B tem o recorde de células exatas (79) — ele perde por *recusar*, não por errar. |
| **H1.2** — zero recitações | leitura, não memória | **CONFIRMADA.** 0 recitações atribuíveis em 132 corridas (124 células perturbadas devolvidas como lidas; 2 células neutralizadas por vazamento do harness, Emenda 3). |
| **H1.3** — invenção < 5%; omissão > invenção | inventar é raro | **CONFIRMADA COM FOLGA.** Invenção = 0% nos quatro. Omissões: 0–10 por modelo. |
| **H1.4** — concordância RoB entre 60% e 90% | faixa inter-revisor humana | **PARCIAL.** gemmas dentro (78%/77%); qwens abaixo (57%/57%). O desvio concentra-se num único domínio doutrinário (cegamento de participantes: MA "Unclear" × modelos "High"). |
| **H1.5** — síntese preserva direção onde as extrações estão certas | erro só a jusante | **CONFIRMADA.** Quatro sínteses na faixa de palavras, direções compatíveis, zero números órfãos (checagem mecânica). |
| **H1.6** — ≥1 discordância adjudicada a favor do modelo | o benchmark acha erro humano | **CONFIRMADA (3×).** Yoon: braços trocados na tabela de características (3 modelos flagraram; fonte confirma). Weinberg: ASA "Not stated" que a tabela do artigo reporta. Sun: conversão do tempo até dieta oral contradiz o texto-fonte ("by 2 days"; 4 modelos unânimes). |

## Os seis achados do Estudo 1

1. **Modelos locais extraem evidência no nível de revisor — e acima dele em fidelidade.**
   396 células decididas, zero valores errados, inventados ou recitados. As 12 perdas
   totais dos quatro modelos são todas omissões ("NR" onde a fonte reporta). No mesmo
   corpus, os revisores humanos da metanálise publicada cometeram os erros do arquivo de
   erratas: braços trocados, dado declarado inexistente que existe, conversão que
   contradiz a própria fonte, célula corrompida por Excel.

2. **A previsão "os grandes são os extratores" caiu.** A tarefa de extração não inverteu
   o ranking do FIEL: os gemma disciplinados empataram no topo (100%), o 27B fiel ficou a
   2 pontos (98%) e o 14b pagou sua conservadorismo (90%). A diferença entre famílias não
   é acerto — é **disposição a responder**: qwen diz "NR" onde gemma responde e acerta.

3. **Os modelos auditaram a metanálise — e o adjudicador.** Três erratas confirmadas da
   âncora (duas levantadas pelos próprios modelos), duas divergências definicionais
   documentadas (analisados vs randomizados), e **duas erratas do adjudicador na mesma
   noite** (Redondo: abstract contradiz o corpo do próprio primário; Wu: janela de busca
   rígida escondeu dados que os modelos extraíram literalmente). A régua não se dobrou
   para ninguém — nem para quem a segura.

4. **No risco de viés, os modelos são mais duros que os revisores.** A concordância cai
   quase inteira num domínio: cegamento de participantes/equipe (21%), onde a MA julgou
   "Unclear" e os modelos "High" — a leitura literal da regra Cochrane para intervenção
   impossível de cegar. Doutrina, não desatenção.

5. **A síntese sem calculadora é honesta mas míope.** Nenhum modelo fabricou RR ou IC;
   todos descreveram estudo a estudo com hedges. Mas sem agregação, a morbidade "parece
   favorável" (contagem de estudos) onde a MA agregada diz "sem diferença significativa"
   (RR 0,78, IC cruzando 1). A lacuna é exatamente a pergunta do Estudo 2 ("as contas").

6. **A economia é da iGPU.** O 12b fez o bloco inteiro em 84 minutos e empatou no topo.
   O 27B custou 4,5× o tempo para −2 pontos. Para extração estruturada, o modelo pequeno
   disciplinado em GPU integrada é o ótimo custo-benefício desta tabela.

## Limitações

Uma única metanálise-âncora, de uma revista (Cureus) — os erros dela não generalizam
para toda a literatura. 8 dos 14 primários (estrato aberto); o estrato fechado já está
garantido e entra por emenda. O adjudicador é o mesmo assistente que construiu o
harness — mitigado por citação literal obrigatória em cada decisão e pelos próprios
erros registrados em público. Corpus só-texto (figuras e suplementos fora de alcance:
6 células pendentes não pontuaram). Duas perturbações vazaram (Emenda 3). As sínteses
foram julgadas pelo adjudicador, não por revisor humano independente.

## Próximos passos registrados

Emenda 2: estrato fechado (6 primários, ~96 corridas, fronteira de perturbação
corrigida). Estudo 2 "as contas": braço A de cabeça vs braço B com calculadora
([roadmap](../../roadmap.md)). Parte 1 do EXTRAI para publicação.
