# EXTRAI — o benchmark que pergunta se o modelo lê como um revisor

**EXTRAI** é um benchmark de extração de evidência científica para modelos de linguagem locais, irmão do [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr) (benchmark de sumarização fiel). O nome é o verbo: a pergunta central é se o modelo, diante de um ensaio clínico completo, **extrai** o que um revisor humano de metanálise extrairia — os números certos, das seções certas, admitindo o que o artigo não reporta.

> O FIEL pergunta se o modelo *escreve* com fidelidade. O EXTRAI pergunta se ele *lê* como um revisor.

## Por que existe

O EXTRAI nasceu de uma dúvida deliberada sobre os resultados do próprio FIEL. Quatorze partes de benchmark de sumarização produziram um veredito recorrente: os modelos grandes (qwen3.8:27b, gemma4:26b) têm fidelidade quase perfeita mas escrita indisciplinada — seriam "extratores e auditores, não escritores". Essa frase virou hipótese e nunca foi testada **na tarefa de extração de verdade**. O EXTRAI é esse teste, com três mudanças metodológicas desenhadas para atacar as fraquezas conhecidas do FIEL:

1. **O gabarito é humano e externo.** No FIEL, o juiz (um LLM maior) decide o que é erro. No EXTRAI, o padrão-ouro são as tabelas de extração de uma metanálise publicada e revisada por pares — o que dois revisores humanos de verdade extraíram dos mesmos artigos que o modelo vai ler.
2. **A correção principal é mecânica.** Um script compara célula a célula a extração do modelo com o gabarito, sob tolerâncias pré-registradas. O juiz LLM só entra na adjudicação de discordâncias e na fase de síntese — o que reduz drasticamente a superfície de subjetividade que o FIEL admitia.
3. **O gabarito também está em julgamento.** Quando o modelo discorda do gabarito, a fonte primária decide — pelo rito herdado do FIEL: *verificar na fonte antes de deduzir*. Se os revisores humanos erraram uma célula, a discordância é adjudicada a favor do modelo e vira **errata documentada da metanálise**. O benchmark mede o modelo e audita a revisão ao mesmo tempo.

## O desenho, em uma frase

Uma metanálise-âncora publicada **depois do corte de treino dos modelos**, com primários em acesso aberto, fornece a tarefa (extrair evidência dos primários), o gabarito (suas próprias tabelas de extração) e o juízo humano de referência (risco de viés e síntese) — e os primários são **perturbados numericamente** antes da leitura, de modo que recitar valores decorados (do artigo original ou da própria metanálise) fica detectável.

## As três tarefas

| Tarefa | O que o modelo recebe | O que devolve | Como é corrigido |
|---|---|---|---|
| **T1 — Extração estruturada** | Texto integral de um RCT primário (perturbado) + formulário de extração | JSON com as células (valor + localização no artigo) | Script compara com o gabarito da metanálise, célula a célula; discordâncias vão a adjudicação |
| **T2 — Risco de viés** | O mesmo primário + os 7 domínios Cochrane | Julgamento Low/High/Unclear por domínio + justificativa | Concordância com a tabela de RoB dos revisores, domínio a domínio |
| **T3 — Síntese** | As **próprias extrações** do modelo (todos os primários) | Síntese narrativa do corpo de evidência | Juiz LLM sob rito, contra as conclusões da metanálise: direção do efeito por desfecho, incerteza, sem invenção |

## Pontuação de célula (T1)

Cada célula do formulário recebe exatamente um rótulo:

| Rótulo | Definição | Valor |
|---|---|---|
| **exata** | Igual ao gabarito sob as tolerâncias pré-registradas (arredondamento, unidade) | 1,0 |
| **derivável** | Não literal no gabarito, mas aritmética correta de valores da fonte (ex.: percentual calculado de eventos/total) | 1,0 |
| **discordante-adjudicada-modelo** | Difere do gabarito, mas a fonte primária confirma o modelo → errata da metanálise | 1,0 |
| **NR-correta** | Modelo declara "não reportado" e o dado de fato não está no primário | 1,0 |
| **omissa** | Modelo deixa vazio ou "NR" quando o dado está no primário | 0,0 |
| **errada** | Difere do gabarito e a fonte confirma o gabarito | 0,0 |
| **inventada** | Valor que não existe em lugar nenhum da fonte | 0,0 e contada à parte (taxa de invenção) |

A métrica principal é a **acurácia de célula** (proporção de células com valor 1,0). A **taxa de invenção** é reportada separadamente, porque inventar é pior que omitir — a assinatura do FIEL continua valendo aqui.

Ficam **fora** do formulário as células que são cálculo meta-analítico dos revisores (risk ratio, mean difference, IC95%, pesos, GRADE): o modelo extrai fatos do primário, não refaz a metanálise — exceto na T3, onde a direção qualitativa do efeito é o que se julga.

## A prova de leitura dupla

Herdada do FIEL e adaptada: em cada primário, K números que aparecem no gabarito são discretamente alterados antes de o modelo ler (a tabela original↔perturbado fica selada até a correção). Na correção, a célula correspondente tem três destinos:

- **valor perturbado** → o modelo *leu* o artigo que recebeu (célula pontua normalmente, contra o valor perturbado);
- **valor original publicado** → o modelo *recitou* — ou o primário decorado do treino, ou a própria metanálise. Recitação zera a célula e é contada como evidência de contaminação;
- **ausente/outro** → segue as regras normais.

Como a metanálise-âncora é posterior ao corte de treino, recitação da revisão é improvável — mas a perturbação transforma essa suposição em coisa **medida**.

## Rito de adjudicação

Toda discordância entre modelo e gabarito passa pelo rito antes de virar dedução: **verificar na fonte primária antes de deduzir**. O adjudicador (LLM juiz + autor humano) localiza o trecho da fonte que decide a célula e registra a citação literal no arquivo de avaliação. O gabarito humano não tem imunidade: as erratas da metanálise-âncora encontradas no caminho são documentadas em arquivo próprio, nunca editadas em silêncio — a régua não se dobra para ninguém, nem para os revisores publicados.

## Contratos de congelamento

1. **Corpus congelado**: a metanálise-âncora, os primários e as perturbações são fixados antes de qualquer medida e não mudam dentro de uma série.
2. **Protocolo pré-registrado**: hipóteses, formulário, tolerâncias e regras de pontuação são escritos antes da primeira corrida; mudanças posteriores só por emenda datada.
3. **Modelos e configs congelados**: os modelos entram com as mesmas configurações da tabela FIEL vigente (amostragem do fabricante, contexto registrado, CPU/GPU registrado por modelo).
4. **Inconsistências pré-existentes registradas**: contradições internas da própria metanálise detectadas na montagem do corpus são listadas no protocolo *antes* das corridas, para que não haja liberdade interpretativa na hora da correção.

## Reprodução

```
scripts/estudo1/baixar-corpus.py      # baixa MA + primários abertos (Europe PMC)
scripts/estudo1/extrair-gabarito.py   # tabelas da MA -> gabarito JSON estruturado
# (demais scripts listados no protocolo de cada estudo)
```

Requisitos: Python 3.12 (stdlib apenas para o corpus), Ollama para os modelos locais. Cada estudo tem protocolo próprio em `dados/estudoN/protocolo-estudoN.md` com a fila de execução exata.

## Estudos

| Estudo | Pergunta | Status |
|---|---|---|
| [Estudo 1](dados/estudo1/protocolo-estudo1.md) | Os quatro veteranos do FIEL extraem evidência como os revisores da metanálise-âncora (GDFT)? | protocolo pré-registrado |

## Tabela vigente

*(vazia — nenhuma medida corrigida ainda)*
