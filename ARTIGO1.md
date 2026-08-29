# EXTRAI, parte 1: pus quatro modelos locais para refazer a extração de uma metanálise — eles acharam mais erros nela do que ela neles

*Depois de catorze partes do benchmark FIEL medindo se modelos locais escrevem resumos fiéis, resolvi duvidar do meu próprio veredito. As partes 13 e 14 diziam que os modelos grandes seriam "extratores e auditores, não escritores" — uma frase que nunca tinha sido testada na tarefa real. Então nasceu o EXTRAI: os mesmos quatro modelos, num mini-PC, refazendo célula a célula a extração de uma metanálise publicada e revisada por pares — os 14 ensaios clínicos dela, inteiros. O placar: em 624 células corrigidas, os modelos erraram exatamente uma. A auditoria da metanálise publicada somou nove erratas confirmadas na fonte (num arquivo público de 15 entradas). E o juiz — eu — foi corrigido três vezes pelos próprios modelos.*

> 📄 Série EXTRAI: parte 1 (esta) · [parte 2](ARTIGO2.md) · Dados, protocolos pré-registrados e erratas: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Benchmark irmão: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## O contexto, para quem chega agora

O EXTRAI é o segundo benchmark de uma linha que roda inteira em hardware de consumidor (Ryzen 7, GPU integrada, 32 GB de RAM). O primeiro, FIEL, media escrita fiel; este mede **leitura de revisor**: dado o texto integral de um ensaio clínico, o modelo preenche a mesma ficha de extração que os revisores humanos de uma metanálise publicada preencheram — números certos, das seções certas, admitindo o que o artigo não reporta. Três escolhas de método atacam as fraquezas conhecidas do FIEL: (1) a correção principal é **mecânica** — um script compara célula a célula, e o juiz de linguagem só arbitra empates, com citação obrigatória da fonte; (2) o gabarito humano **também está em julgamento** — cada célula da metanálise foi verificada contra o artigo original, e quando modelo e revisores discordam, a fonte decide; (3) os artigos que os modelos leem são **perturbados** — números discretamente alterados, de modo que devolver o valor publicado denuncia recitação, não leitura.

## O que exatamente foi feito

A âncora: Ashraf N, Zargar OUU e Albina A, **"Comparison of Goal-Directed Fluid Therapy and Conventional Fluid Therapy in Elective Major Abdominal Surgery: A Meta-Analysis of Randomized Controlled Trials"** ([Cureus, junho de 2026, acesso aberto CC BY](https://doi.org/10.7759/cureus.110243)) — uma metanálise de fluidoterapia guiada por metas (GDFT, na sigla em inglês: a estratégia de dar fluidos na cirurgia guiando-se por metas hemodinâmicas medidas, em vez de volumes fixos), publicada *depois* do corte de treino dos modelos, com 14 ensaios randomizados. Os 8 de acesso aberto vieram do Europe PMC; os 6 fechados, do meu acesso institucional e de manuscritos de autor legais — **a metanálise inteira**. Cada modelo leu cada ensaio e cumpriu três tarefas: a ficha de 30 campos (T1), o risco de viés nos 7 domínios Cochrane (T2) e uma síntese usando só as próprias extrações (T3). Duas réplicas por tarefa, 232 corridas corrigidas.

*Como ler: cada linha é um modelo; a coluna "execução" diz onde ele rodou no mini-PC.*

```
modelo        execução                 corridas   tempo
gemma4:12b    GPU integrada (Vulkan)      57      ~2,2 h
qwen3:14b     GPU integrada (Vulkan)      57      ~1,7 h
gemma4:26b*   CPU                         57      ~2,0 h
qwen3.8:27b   CPU                         57      ~7,1 h
```

\* MoE = mixture-of-experts: dos 26 bilhões de parâmetros, só ~4 bilhões ficam ativos por token — por isso o 26b é rápido até em CPU.

## O que encontramos

### 1. O placar: extração de evidência está praticamente resolvida neste hardware

156 células pontuáveis por modelo (as demais: sem valor verificável, pendentes ou dado ausente do insumo — não contam contra ninguém). Os dois estratos do corpus: **aberto** = os 8 ensaios de acesso aberto (Europe PMC); **fechado** = os 6 atrás de paywall, obtidos legalmente — cada estrato rodou como uma fila própria, com as mesmas regras.

*Como ler: acertos/células pontuadas de cada modelo em cada um dos 14 ensaios (nome do primeiro autor; 🔒 = estrato fechado). A última linha soma tudo.*

```
estudo             gemma12  gemma26  qwen38   qwen14
Yoon                11/11    11/11    11/11     9/11
Sun                 22/22    22/22    22/22    21/22
Wu                  10/10    10/10    10/10     9/10
Castro              15/15    15/15    15/15    13/15
Redondo Calvo       10/10    10/10    10/10     8/10
Schmid               7/7      7/7      7/7      7/7
Weinberg            10/10    10/10     9/10     9/10
Sujatha             14/14    14/14    13/14    13/14
Diaper 🔒           11/11    11/11    11/11     9/11
de Waal 🔒           9/9      9/9      8/9      9/9
Arslan-Carlon 🔒    10/10    10/10     9/10     9/10
Calvo-Vecino 🔒      9/9      8/9      9/9      9/9
Coeckelenbergh 🔒   11/11    11/11    11/11    11/11
Hokenek 🔒           7/7      7/7      7/7      7/7
TOTAL              156/156  155/156  152/156  143/156
                    100%     99%      97%      92%
```

Nenhuma célula errada nos gemma; a única errada dos quatro modelos é do qwen38 (a linha de Waal 8/9 — o caso literal aparece no achado 2). Todo o resto que se perdeu foi omissão. E a prova de leitura — as células cujos números foram perturbados no texto que o modelo leu:

*Como ler: "leu" = devolveu o valor perturbado (só existe no texto lido); "recitou" = devolveu o valor original publicado (indicaria memória, não leitura).*

```
modelo        leu   recitou   ausente da resposta
gemma4:12b     54      0            8
gemma4:26b     53      0            7
qwen3.8:27b    50      0           13
qwen3:14b      47      0           14
```

**Zero recitações atribuíveis em 228 corridas.** Exemplo concreto: o texto perturbado do Castro dizia que os pacientes ASA II eram 28 (o real, publicado, é 31 — ASA é a escala da Sociedade Americana de Anestesiologistas que gradua o estado físico do paciente antes da cirurgia, de I, saudável, a IV, gravíssimo); os três modelos que responderam escreveram "II: 28 (72%)" — o valor que só existe no texto que leram.

### 2. A hipótese central caiu — e o modo de falha é a recusa

O pré-registro (H1.1) apostava nos grandes fiéis: 27B ≥ 26b > 12b ≥ 14b. A ordem real ficou **12b > 26b > 27B > 14b** — a disciplina gemma venceu a extração também. E aqui está **cada célula perdida do estudo inteiro**, as 18, uma a uma (a primeira versão deste artigo somava "17, sendo 16 omissões"; a tabela completa corrige: 18, sendo 17 omissões e 1 errada):

*Como ler: o que o modelo respondeu vs o que a fonte reporta (camada fonte do gabarito oficial; em célula perturbada, o valor esperado é o do texto perturbado que o modelo leu).*

```
modelo   estudo      campo               modelo   a fonte reporta
gemma26  Calvo-Vec.  laparoscopia ctl    (omitiu) 109 (50,2%)
qwen38   Weinberg    uso inotrópico      NR       "used more
                                                  frequently" (GDT)
qwen38   Sujatha     fluido total GDFT   NR       cristaloides
                                                  1842|1715 ml
qwen38   de Waal ★   n randomiz. ctl     305      259 — o 305 é o
         (a única                                 valor perturbado
          ERRADA)                                 do braço GDFT
qwen38   Arslan-C.   uso inotrópico      NR       vasopressores
                                                  comparáveis
qwen14   Yoon        ASA braço GDFT      NR       4:29:6:0
qwen14   Yoon        ASA braço ctl       NR       2:27:7:0
qwen14   Sun         uso inotrópico      NR       18 (36%) vs
                                                  27 (54%)
qwen14   Wu          uso inotrópico      NR       norepi 15 vs 24;
                                                  fenil. 12 vs 24
qwen14   Castro      perda sang. GDFT    NR       1100.1 ± 851.1
qwen14   Castro      perda sang. ctl     NR       1283.2 ± 959.7
qwen14   Redondo     ASA braço GDFT      NR       0:13:6:0
qwen14   Redondo     ASA braço ctl       NR       0:10:6:0
qwen14   Weinberg    uso inotrópico      NR       "used more
                                                  frequently" (GDT)
qwen14   Sujatha     cristaloide GDFT    NR       FloTrac 1842 |
                                                  PVI 1715 ml
qwen14   Diaper      ASA braço GDFT      NR       III-IV: 98 (50,0%)
qwen14   Diaper      ASA braço ctl       NR       III-IV: 85 (42,9%)
qwen14   Arslan-C.   uso inotrópico      NR       vasopressores
                                                  comparáveis
```

Dezessete das dezoito são "NR" escrito onde a fonte reporta — nenhum modelo mentiu; alguns se calaram. A única **errada** é instrutiva: no fluxograma do de Waal, mutilado pela extração do PDF ("…274 Assigned to PGDT group 259 Received…"), o 27B pôs o valor do braço GDFT (perturbado para 305) no campo do braço controle. Uma troca de braço num texto embaralhado — em 624 células.

### 3. Os modelos auditaram a metanálise publicada — um arquivo de erratas com 15 entradas

Antes da lista, uma nota de justiça: erros de transcrição acontecem em qualquer revisão feita à mão — o próprio juiz deste benchmark registrou as próprias erratas na mesma rodada (elas estão NA lista, retiradas e riscadas, não escondidas), e o ponto aqui é o processo, não os autores. O [arquivo de erratas](dados/estudo1/erratas-da-ancora.md) registra cada entrada com o trecho da fonte que a decide; a tabela abaixo espelha o arquivo, número por número. "MA" é a metanálise-âncora — a revisão publicada cujas tabelas servem de gabarito; cada ensaio nomeia seu braço guiado à própria maneira (GDHT, PGDT, GDT — é sempre o braço GDFT).

*Como ler: as 15 entradas do arquivo, na numeração oficial. Categorias: ERRATA = erro confirmado na fonte; RETIRADA = acusação minha que a fonte desmentiu (errata do juiz, não da MA); DIVERGÊNCIA = escolha não declarada, não erro; PRIMÁRIOS = problema dos ensaios, não da MA.*

```
#   estudo(s)      categoria     o que a fonte decide
1   Yoon           ERRATA        MA: GDFT 36/ctl 39. Fonte:
                                 "GDHT group (n=39)… control
                                 (n=36)" — braços TROCADOS
2   Redondo Calvo  RETIRADA      acusei braços trocados lendo
                                 só o abstract; fluxograma e 3
                                 tabelas dizem o oposto — a MA
                                 estava CERTA (erro do juiz)
3   Weinberg       ERRATA        MA: ASA "Not stated". Fonte:
                                 "ASA I-II 7 (27%)… ≥III 19
                                 (73%)" — está na tabela
4   Wu             RETIRADA      acusei "Inotrope use" sem
                                 apoio; a fonte TEM: "norepi…
                                 15 (25.9) 24 (42.9)" — os
                                 modelos estavam certos
5   Sujatha        ERRATA        ASA "95:105" sem apoio; célula
                                 corrompida por hora do Excel
                                 ("2 days, 11:42:00")
6   Sujatha        DIVERGÊNCIA   n=200/101 são ANALISADOS; a
                                 fonte randomizou 102 por braço
                                 (escolha não declarada)
7   Castro         DIVERGÊNCIA   rótulo "bowel surgeries"
                                 estreito; fonte inclui hepato,
                                 gastro e pâncreas
8   Wu             DIVERGÊNCIA   n 58/56 = analisados; fonte:
                                 "61 patients… another 61"
9   Sun            ERRATA        dieta oral 72±24 vs 96±30 h
                                 (Δ 1 dia) contradiz o próprio
                                 texto: "by 2 days"; medianas
                                 4,0/6,0 d — 4 modelos unânimes
10  de Waal        ERRATA        colunas ASA trocadas entre
                                 braços; aritmética prova:
                                 123 = 52,6% × 234 (o CONTROLE)
11  Diaper         ERRATA        ASA "Not stated" que a fonte
                                 reporta: "III & IV 98 (50.0)
                                 85 (42.9)"
12  Diaper &       ERRATA        tempos de flatus publicados;
    Coeckelenbergh               a palavra "flatus" NÃO EXISTE
                                 nos dois textos integrais
13  6 estudos      ERRATA        coluna "n" mistura analisados
                                 com randomizados sem nota (Wu
                                 61→58/56; de Waal 274/259→
                                 248/234; Hokenek 40→39…)
14  Diaper, FEDORA PRIMÁRIOS     ensaios internamente contra-
                                 ditórios (prosa vs tabela;
                                 abstract vs métodos)
15  (agregado)     ERRATA        aritmética — chega na parte 2:
                                 número certo, método com nome
                                 errado
```

Saldo: **9 erratas confirmadas da MA, 3 divergências definicionais, 2 erratas do próprio juiz e 1 problema dos primários.** A entrada 1 foi levantada **pelos modelos**: três deles extraíram 39/36 independentemente, contra a tabela publicada — e a fonte confirmou.

### 4. Os modelos corrigiram o juiz — três vezes

O rito do benchmark ("verificar na fonte antes de deduzir") vale para o adjudicador também. Três vezes declarei erro de modelo, três vezes a fonte me desmentiu: no **Redondo**, adjudiquei pelo abstract ("GDHT (n = 16)") sem ver que fluxograma e três tabelas dizem o oposto — o primário se contradiz, e a MA estava certa; no **Wu**, minhas janelas de busca rígidas esconderam a linha *"Number of patients using norepinephrine 15 (25.9) 24 (42.9)"* que os modelos haviam extraído literalmente — cheguei a acusá-los de fabricação; no **Hokenek**, o "40/40" que eu ia deduzir está letra por letra na fonte: *"randomised into two groups (control group: 40, PVI group: 40)"*. As três erratas do adjudicador estão públicas, ao lado das da metanálise.

### 5. No risco de viés, os modelos são mais duros que os revisores

Concordância com os julgamentos Cochrane publicados (7 domínios × 13 estudos — o Weinberg não tem linha de risco de viés na MA, outra inconsistência):

*Como ler: concordância célula a célula com a tabela da MA; "global igual" = mesmo veredito de risco geral do estudo; estabilidade = réplica 1 vs réplica 2 do próprio modelo.*

```
modelo        concordância    global igual   estabilidade
gemma4:12b    80% (73/91)        5/13            97%
gemma4:26b    79% (69/87)        6/13            95%
qwen3.8:27b   62% (56/91)        0/13            80%
qwen3:14b     59% (54/91)        4/13            97%
```

E o mapa por domínio — os quatro modelos somados — mostra onde mora a divergência:

*Como ler: concordância dos 4 modelos com a MA em cada domínio Cochrane (52 julgamentos = 13 estudos × 4 modelos; dois domínios têm menos por células ausentes).*

```
domínio Cochrane                    concordância
relato seletivo                      92% (48/52)
geração da sequência aleatória       90% (47/52)
ocultação da alocação                77% (40/52)
dados de desfecho incompletos        76% (37/49)
cegamento de avaliadores             65% (33/51)
outros vieses                        63% (33/52)
cegamento participantes/equipe       27% (14/52)  ←
```

A discordância mora quase toda num lugar: **cegamento de participantes e equipe, 27%**. O padrão é unilateral — a MA julgou "Unclear" e os modelos, "High" — porque o anestesista que executa o algoritmo de fluidos não pode ser cegado. Regra Cochrane ao pé da letra contra a leniência dos revisores: divergência de doutrina, não de leitura.

### 6. A síntese é honesta, mas míope — e mais evidência a calibra

As sínteses passaram na checagem mecânica anti-invenção: **zero números órfãos** (todo número citado existe nas extrações do próprio modelo). Mas sem ferramenta de agregação, a conclusão vem da contagem de estudos — e muda quando o corpo de evidência cresce:

*Como ler: como cada modelo descreveu a morbidade (complicações pós-operatórias) sintetizando 8 estudos vs 14 estudos — frases literais das sínteses.*

```
modelo        com 8 estudos            com 14 estudos
gemma4:12b    "resultados              "resultados são
              inconsistentes"          inconsistentes"
qwen3:14b     "efeito benéfico…        "efeito benéfico…
              cinco dos oito"          embora com
                                       inconsistências"
gemma4:26b    "tendência de            "evidência é
              benefício"               inconsistente"
qwen3.8:27b   "seis dos oito           "inconsistente e
              com redução"             contraditória"
```

Com 14 estudos, três dos quatro migraram para "inconsistente" — **aproximando-se do veredito agregado da própria metanálise (RR 0,78, IC cruzando 1: não significativo) sem nenhuma estatística**, só por verem mais contradição. O que falta — a conta formal — é o assunto da parte 2.

## O que isso significa

Para quem faz revisão sistemática: a extração estruturada, a etapa mais tediosa e propensa a erro do processo, roda num mini-PC sem GPU dedicada com fidelidade que neste corpus **superou a dos revisores publicados** — e com uma vantagem estrutural: o modelo cita *onde* achou cada dado, e a máquina confere. Para a linha FIEL: "grandes = extratores" morreu; o que sobrevive é "disciplinados = tudo, por enquanto". E para quem lê metanálises: os erros que este benchmark achou numa revisão revisada por pares — braços trocados, colunas invertidas, n's mal rotulados — são exatamente os que ninguém confere depois de publicados.

## Quem fez o quê

**Os modelos locais** (gemma4:12b, qwen3:14b, gemma4:26b, qwen3.8:27b, via Ollama no mini-PC) leram os 14 textos perturbados e preencheram fichas, julgamentos de viés e sínteses — 232 corridas. **O harness e os scripts** (públicos no repositório) montaram os prompts, rodaram as filas, compararam célula a célula com o gabarito e contaram os placares — toda a correção primária é mecânica. **O Claude (assistente, Anthropic)** desenhou o benchmark com o autor, construiu o gabarito oficial verificado na fonte (com citação literal por decisão), adjudicou os empates sob o rito público — e registrou as próprias três erratas. **O autor** decidiu o desenho, caçou os 6 PDFs fechados legalmente e revisou tudo.

## Limitações

Uma única metanálise, de uma única revista; os erros dela não generalizam para a literatura. O adjudicador é o mesmo assistente que construiu o harness — mitigado por citação literal obrigatória em cada decisão e pelas três erratas próprias em registro público. O corpus é só texto: valores que morem exclusivamente em figuras ou suplementos ficaram fora de pontuação (é possível que os "flatus fantasma" vivam lá). Réplicas de duas corridas medem estabilidade, não significância.

*Na parte 2: dou aos modelos as fórmulas da metanálise — risk ratio, intervalo de confiança, agrupamento — primeiro de cabeça, depois como ferramenta que eles chamam. Spoiler: de cabeça, nenhum dos quatro acertou um único intervalo de confiança.*
