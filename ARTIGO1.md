# EXTRAI, parte 1: pus quatro modelos locais para refazer a extração de uma metanálise — eles acharam mais erros nela do que ela neles

*Depois de catorze partes do benchmark FIEL medindo se modelos locais escrevem resumos fiéis, resolvi duvidar do meu próprio veredito. As partes 13 e 14 diziam que os modelos grandes seriam "extratores e auditores, não escritores" — uma frase bonita que nunca tinha sido testada na tarefa real. Então nasceu o EXTRAI, um segundo benchmark: os mesmos quatro modelos, rodando num mini-PC, refazendo célula a célula o trabalho de extração de uma metanálise publicada e revisada por pares — os 14 ensaios clínicos dela, inteiros. O placar final: em 624 células corrigidas, os modelos erraram exatamente uma. No caminho, encontraram braços trocados, colunas invertidas e dados fantasma na metanálise publicada — e me corrigiram três vezes.*

> 📄 O EXTRAI é irmão do [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr) (14 partes sobre sumarização fiel). Método, protocolo pré-registrado, gabarito verificado na fonte, erratas e todos os dados: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr)

## O desenho, em um parágrafo

Uma metanálise-âncora de fluidoterapia guiada por metas (Cureus, junho de 2026 — publicada *depois* do corte de treino dos modelos) fornece a tarefa e o gabarito: as tabelas que dois revisores humanos extraíram de 14 ensaios clínicos randomizados. Cada modelo recebe o texto integral de cada ensaio e um formulário de 30 campos (pacientes por braço, fluidos, complicações, mortalidade, função intestinal…), depois julga o risco de viés nos 7 domínios Cochrane, e por fim escreve uma síntese usando apenas as próprias extrações. Três truques de rigor: os artigos que os modelos leem são **perturbados** (números discretamente alterados — quem devolve o valor publicado está recitando, não lendo); a correção principal é **mecânica** (um script compara célula a célula; o juiz de linguagem só arbitra empates, com citação obrigatória da fonte); e o gabarito humano **também está em julgamento** — quando modelo e revisores discordam, o artigo original decide.

## O que exatamente foi medido

Quatro veteranos do FIEL — gemma4:12b e qwen3:14b na GPU integrada, gemma4:26b (MoE) e qwen3.8:27b na CPU — sobre os 14 ensaios da metanálise: 8 de acesso aberto e, graças ao acesso institucional do autor, os 6 fechados também. 228 corridas, duas réplicas por tarefa, 8,3 horas de fila no estrato aberto e 5,9 no fechado, tudo num Ryzen 7 com 32 GB de RAM. Nenhuma célula ficou sem veredito: 156 células pontuáveis por modelo, cada decisão pública com o trecho da fonte que a sustenta.

## Os seis achados

### 1. Extração de evidência está praticamente resolvida em hardware de consumidor

O placar: **gemma4:12b 100%, gemma4:26b 99%, qwen3.8:27b 97%, qwen3:14b 92%**. Nas 624 células decididas dos quatro modelos somados, houve **uma** célula errada (uma troca de braço ao ler um fluxograma que o PDF havia embaralhado), **zero valores inventados** e **zero recitações**: nas 124 células com números perturbados que os modelos citaram, eles devolveram o valor do texto que leram, nunca o valor publicado que poderiam ter decorado.

### 2. A hipótese central caiu — e o modo de falha é a recusa

O pré-registro apostava que os modelos grandes e fiéis venceriam a extração. Errado: a disciplina da família gemma venceu de novo, e o pequeno 12b — que faz o serviço na GPU integrada em uma fração do tempo — empatou no topo com nota perfeita. O 27B mantém o recorde de células *exatas* e perde por outro motivo: ele **recusa**. Toda a diferença entre 100% e 92% é feita de "não reportado" escrito onde a fonte reporta. Nenhum modelo mente; alguns se calam.

### 3. Os modelos auditaram a metanálise publicada — e acharam 14 problemas

O arquivo de erratas do benchmark lista, com citações: os braços do ensaio de Yoon **trocados** na tabela de características (três modelos flagraram independentemente; a fonte diz "GDHT group (n = 39)"); as colunas de ASA do de Waal **invertidas** (a aritmética prova: 123 = 52,6% × 234 — do controle); dois estudos com ASA declarado "Not stated" cuja tabela **reporta** o ASA; tempos de flatus publicados para dois artigos que **não contêm a palavra flatus**; uma conversão de horas que contradiz o próprio texto-fonte ("by 2 days"); uma célula corrompida por formatação de hora do Excel ("2 days, 11:42:00" no lugar de uma razão ASA); e um padrão sistemático — em **seis** dos 14 estudos, a coluna "n" da metanálise usa pacientes *analisados* como se fossem *randomizados*, sem nota de método.

### 4. Os modelos corrigiram o juiz — três vezes

O rito do benchmark ("verificar na fonte antes de deduzir") vale para todos, inclusive para mim, o adjudicador. Três vezes declarei erro de modelo e três vezes a fonte me desmentiu: no Redondo, adjudiquei pelo abstract sem ver que o corpo do artigo diz o contrário quatro vezes; no Wu, minhas janelas de busca rígidas esconderam uma tabela de vasoativos que os modelos extraíram literalmente; no Hokenek, os "40/40" que eu ia deduzir estavam escritos letra por letra na fonte. As três erratas do adjudicador estão registradas em público, ao lado das da metanálise.

### 5. No risco de viés, os modelos são mais duros que os revisores

Concordância com os julgamentos Cochrane dos revisores: gemma4:12b 80%, gemma4:26b 79%, qwens ~60%. Quase toda a divergência mora num único domínio: cegamento de participantes e equipe, onde a concordância cai a 27% — a metanálise julgou "Unclear", e os modelos, "High", porque o anestesista que executa o algoritmo de fluidos não pode ser cegado. É a regra Cochrane aplicada ao pé da letra contra a leniência dos revisores: divergência de doutrina, não de leitura.

### 6. A síntese sem calculadora é honesta, mas míope

As sínteses finais respeitaram o limite de palavras e — checagem mecânica — **não contêm um único número que não exista nas extrações do próprio modelo**. Nenhum risk ratio fabricado, nenhum intervalo de confiança inventado. Mas sem ferramenta de agregação, todos os modelos descrevem a morbidade como "favorável à GDFT" contando estudos, enquanto a metanálise agregada diz "sem diferença significativa" (RR 0,78, IC cruzando 1). Essa lacuna exata — saber extrair sem saber somar — é a pergunta do Estudo 2.

## O que isso significa

Para o fluxo de trabalho de quem faz revisão sistemática: a extração estruturada, a parte mais tediosa e propensa a erro humano do processo, roda hoje num mini-PC sem GPU dedicada, com fidelidade que neste corpus superou a dos revisores publicados — e com uma vantagem estrutural: o modelo cita *onde* achou cada dado, e a máquina confere. Para a linha FIEL: o veredito "grandes = extratores" morreu; o que sobrevive é "disciplinados = tudo, por enquanto". E para a leitura de metanálises em geral: os erros que este benchmark achou numa revisão revisada por pares — braços trocados, colunas invertidas, n's mal rotulados — são exatamente os que ninguém confere depois de publicados.

## Limitações

Uma única metanálise, de uma única revista; os erros dela não generalizam para a literatura. O adjudicador é o mesmo assistente que construiu o harness — mitigado por citação literal obrigatória em cada decisão e pelas três erratas próprias registradas. O corpus é só texto: valores que morem exclusivamente em figuras ou suplementos ficaram fora de pontuação (é possível que os "flatus fantasma" vivam lá). E réplicas de duas corridas medem estabilidade, não significância.

*Na parte 2: dou aos modelos as fórmulas da metanálise — risk ratio, intervalo de confiança, agrupamento — primeiro de cabeça, depois como ferramentas que eles podem chamar. Se a extração está resolvida, será que as contas também estão?*
