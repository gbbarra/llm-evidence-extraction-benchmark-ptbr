# EXTRAI, parte 1: pus quatro modelos locais para refazer a extração de uma metanálise — eles acharam mais erros nela do que ela neles

*Depois de catorze partes do benchmark FIEL medindo se modelos locais escrevem resumos fiéis, resolvi duvidar do meu próprio veredito. As partes 13 e 14 diziam que os modelos grandes seriam "extratores e auditores, não escritores" — uma frase que nunca tinha sido testada na tarefa real. Então nasceu o EXTRAI: os mesmos quatro modelos, num mini-PC, refazendo célula a célula a extração de uma metanálise publicada e revisada por pares — os 14 ensaios clínicos dela, inteiros. O placar: em 624 células corrigidas, os modelos erraram exatamente uma. A metanálise publicada acumulou 15 itens de errata. E o juiz — eu — foi corrigido três vezes pelos próprios modelos.*

> 📄 Série EXTRAI: parte 1 (esta) · [parte 2](ARTIGO2.md) · Dados, protocolos pré-registrados e erratas: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Benchmark irmão: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## O contexto, para quem chega agora

O EXTRAI é o segundo benchmark de uma linha que roda inteira em hardware de consumidor (Ryzen 7, GPU integrada, 32 GB de RAM). O primeiro, FIEL, media escrita fiel; este mede **leitura de revisor**: dado o texto integral de um ensaio clínico, o modelo preenche a mesma ficha de extração que os revisores humanos de uma metanálise publicada preencheram — números certos, das seções certas, admitindo o que o artigo não reporta. Três escolhas de método atacam as fraquezas conhecidas do FIEL: (1) a correção principal é **mecânica** — um script compara célula a célula, e o juiz de linguagem só arbitra empates, com citação obrigatória da fonte; (2) o gabarito humano **também está em julgamento** — cada célula da metanálise foi verificada contra o artigo original, e quando modelo e revisores discordam, a fonte decide; (3) os artigos que os modelos leem são **perturbados** — números discretamente alterados, de modo que devolver o valor publicado denuncia recitação, não leitura.

## O que exatamente foi feito

A âncora: uma metanálise de fluidoterapia guiada por metas (Cureus, junho/2026 — publicada *depois* do corte de treino dos modelos), com 14 ensaios randomizados. Os 8 de acesso aberto vieram do Europe PMC; os 6 fechados, do meu acesso institucional e de manuscritos de autor legais — **a metanálise inteira**. Cada modelo leu cada ensaio e cumpriu três tarefas: a ficha de 30 campos (T1), o risco de viés nos 7 domínios Cochrane (T2) e uma síntese usando só as próprias extrações (T3). Duas réplicas por tarefa, 232 corridas corrigidas:

| Bloco | Execução | Corridas | Tempo |
|---|---|---|---|
| gemma4:12b | iGPU (Vulkan) | 57 | ~2,2 h |
| qwen3:14b | iGPU (Vulkan) | 57 | ~1,7 h |
| gemma4:26b (MoE) | CPU | 57 | ~2,0 h |
| qwen3.8:27b | CPU | 57 | ~7,1 h |

## O que encontramos

### 1. O placar: extração de evidência está praticamente resolvida neste hardware

156 células pontuáveis por modelo (as demais: sem valor verificável, pendentes ou dado ausente do insumo — não contam contra ninguém):

| Modelo | Estrato aberto | Estrato fechado | **Total** | Omissas | Erradas | Inventadas | Recitadas |
|---|---|---|---|---|---|---|---|
| gemma4:12b | 100% | 100% | **100%** (156/156) | 0 | 0 | 0 | 0 |
| gemma4:26b | 100% | 98% | **99%** (155/156) | 1 | 0 | 0 | 0 |
| qwen3.8:27b | 98% | 96% | **97%** (152/156) | 3 | 1 | 0 | 0 |
| qwen3:14b | 90% | 95% | **92%** (143/156) | 13 | 0 | 0 | 0 |

E a prova de leitura (as células com números perturbados):

| Modelo | Leu (devolveu o perturbado) | Recitou | Ausente |
|---|---|---|---|
| gemma4:12b | 54 | 0 | 8 |
| gemma4:26b | 53 | 0 | 7 |
| qwen3.8:27b | 50 | 0 | 13 |
| qwen3:14b | 47 | 0 | 14 |

**Zero recitações atribuíveis em 228 corridas.** Exemplo do que isso significa na prática: o texto perturbado do Castro dizia ASA II = 28 (o real, publicado, é 31); os três modelos que responderam escreveram "II: 28 (72%)" — o valor que só existe no texto que leram. A única célula errada de todo o estudo foi do 27B: pôs o valor de um braço no campo do outro ao ler um fluxograma que a extração do PDF havia embaralhado ("…274 Assigned to PGDT group 259 Received…").

### 2. A hipótese central caiu — e o modo de falha é a recusa

O pré-registro (H1.1) apostava nos grandes fiéis: 27B ≥ 26b > 12b ≥ 14b. A ordem real ficou **12b > 26b > 27B > 14b** — a disciplina gemma venceu a extração também. E a anatomia das perdas prova o resto: das 17 células perdidas pelos quatro modelos somados, **16 são omissões** — "NR" escrito onde a fonte reporta. Exemplo: a perda sanguínea do Castro está literal na fonte ("1100.1 ± 851.1"); o qwen3:14b respondeu "NR". Nenhum modelo mentiu; alguns se calaram.

### 3. Os modelos auditaram a metanálise publicada — 15 itens de errata, todos com citação

O [arquivo de erratas](dados/estudo1/erratas-da-ancora.md) registra cada item com o trecho da fonte que o decide. Os principais:

| # | Estudo | O que a MA publicou | O que a fonte diz |
|---|---|---|---|
| 1 | Yoon | braços GDFT 36 / controle 39 | *"The GDHT group (n = 39)… the control group (n = 36)"* — *trocados* |
| 2 | de Waal | ASA(GDFT) 24:123:86:1 | a aritmética prova a inversão: 123 = 52,6% × 234 (o braço *controle*) |
| 3 | Weinberg | ASA "Not stated" | *"ASA Class I-II 7 (27%)… ≥ III 19 (73%)"* — está na tabela do artigo |
| 4 | Diaper | ASA "Not stated" | *"ASA-PS classes III & IV 98 (50.0) 85 (42.9)"* — idem |
| 5 | Diaper e Coeckelenbergh | tempos de flatus (55±14 h etc.) | a palavra "flatus" **não existe** nos dois textos |
| 6 | Sun | dieta oral 72±24 vs 96±30 h (diferença de 1 dia) | o próprio texto: *"shorten… by 2 days"* — 4 modelos extraíram 4,0/6,0 dias, unânimes |
| 7 | Sujatha | ASA "95:105" e célula *"2 days, 11:42:00"* | corrompida por formatação de hora do Excel |
| 8 | 6 estudos | coluna "n" | usa *analisados* como se fossem *randomizados*, sem nota (Wu 61→58/56; Hokenek 40→39…) |

O item 1 foi levantado **pelos modelos**: três deles extraíram 39/36 independentemente, contra a tabela publicada — e a fonte confirmou.

### 4. Os modelos corrigiram o juiz — três vezes

O rito do benchmark ("verificar na fonte antes de deduzir") vale para o adjudicador também. Três vezes declarei erro de modelo, três vezes a fonte me desmentiu: no **Redondo**, adjudiquei pelo abstract ("GDHT (n = 16)") sem ver que fluxograma e três tabelas dizem o oposto — o primário se contradiz, e a MA estava certa; no **Wu**, minhas janelas de busca rígidas esconderam a linha *"Number of patients using norepinephrine 15 (25.9) 24 (42.9)"* que os modelos haviam extraído literalmente — cheguei a acusá-los de fabricação; no **Hokenek**, o "40/40" que eu ia deduzir está letra por letra na fonte: *"randomised into two groups (control group: 40, PVI group: 40)"*. As três erratas do adjudicador estão públicas, ao lado das da metanálise.

### 5. No risco de viés, os modelos são mais duros que os revisores

Concordância com os julgamentos Cochrane publicados (7 domínios × 13 estudos — o Weinberg não tem linha de RoB na MA, outra inconsistência):

| Modelo | Concordância | Julgamento global igual | Estabilidade r1=r2 |
|---|---|---|---|
| gemma4:12b | **80%** (73/91) | 5/13 | 97% |
| gemma4:26b | **79%** (69/87) | 6/13 | 95% |
| qwen3.8:27b | 62% (56/91) | 0/13 | 80% |
| qwen3:14b | 59% (54/91) | 4/13 | 97% |

Por domínio, a discordância mora quase toda num lugar: **cegamento de participantes/equipe, 27%** (contra 92% em relato seletivo e 90% em geração de sequência). O padrão é unilateral — a MA julgou "Unclear" e os modelos, "High" — porque o anestesista que executa o algoritmo de fluidos não pode ser cegado. Regra Cochrane ao pé da letra contra a leniência dos revisores: divergência de doutrina, não de leitura.

### 6. A síntese é honesta, mas míope — e mais evidência a calibra

As sínteses passaram na checagem mecânica anti-invenção: **zero números órfãos** (todo número citado existe nas extrações do próprio modelo). Mas sem ferramenta de agregação, a conclusão vem da contagem de estudos — e muda quando o corpo de evidência cresce:

| Modelo | Morbidade na síntese de 8 estudos | Na síntese de 14 estudos |
|---|---|---|
| gemma4:12b | "resultados inconsistentes" | "resultados são inconsistentes" |
| qwen3:14b | "efeito benéfico… cinco dos oito ensaios" | "efeito benéfico… embora com inconsistências" |
| gemma4:26b | "tendência de benefício" | "evidência é inconsistente" |
| qwen3.8:27b | "seis dos oito com redução" | "inconsistente e contraditória" |

Com 14 estudos, três dos quatro migraram para "inconsistente" — **aproximando-se do veredito agregado da própria metanálise (RR 0,78, IC cruzando 1: não significativo) sem nenhuma estatística**, só por verem mais contradição. O que falta — a conta formal — é o assunto da parte 2.

## O que isso significa

Para quem faz revisão sistemática: a extração estruturada, a etapa mais tediosa e propensa a erro do processo, roda num mini-PC sem GPU dedicada com fidelidade que neste corpus **superou a dos revisores publicados** — e com uma vantagem estrutural: o modelo cita *onde* achou cada dado, e a máquina confere. Para a linha FIEL: "grandes = extratores" morreu; o que sobrevive é "disciplinados = tudo, por enquanto". E para quem lê metanálises: os erros que este benchmark achou numa revisão revisada por pares — braços trocados, colunas invertidas, n's mal rotulados — são exatamente os que ninguém confere depois de publicados.

## Limitações

Uma única metanálise, de uma única revista; os erros dela não generalizam para a literatura. O adjudicador é o mesmo assistente que construiu o harness — mitigado por citação literal obrigatória em cada decisão e pelas três erratas próprias em registro público. O corpus é só texto: valores que morem exclusivamente em figuras ou suplementos ficaram fora de pontuação (é possível que os "flatus fantasma" vivam lá). Réplicas de duas corridas medem estabilidade, não significância.

*Na parte 2: dou aos modelos as fórmulas da metanálise — risk ratio, intervalo de confiança, agrupamento — primeiro de cabeça, depois como ferramenta que eles chamam. Spoiler: de cabeça, nenhum dos quatro acertou um único intervalo de confiança.*
