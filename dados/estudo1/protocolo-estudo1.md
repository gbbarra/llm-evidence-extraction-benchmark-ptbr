# EXTRAI — Protocolo pré-registrado do Estudo 1

**Registrado em 2026-08-27, antes de qualquer corrida de modelo.** Emendas posteriores só por seção datada ao final. Método geral: [`METHOD.md`](../../METHOD.md).

## 1. Pergunta

Os quatro modelos veteranos da tabela FIEL extraem evidência de ensaios clínicos primários com a fidelidade de revisores humanos de metanálise — e a ordem entre eles inverte em relação ao ranking de escrita? O veredito das partes 13–14 do FIEL ("os grandes são extratores/auditores, não escritores") vira hipótese testável aqui.

## 2. Metanálise-âncora

> Ashraf N, Zargar OUU, Albina A. **Comparison of Goal-Directed Fluid Therapy and Conventional Fluid Therapy in Elective Major Abdominal Surgery: A Meta-Analysis of Randomized Controlled Trials.** Cureus, 2026-06-04. DOI [10.7759/cureus.110243](https://doi.org/10.7759/cureus.110243) · [PMC13235771](https://europepmc.org/article/PMC/PMC13235771) · CC BY 4.0.

Selecionada por: (a) publicação posterior ao corte de treino dos quatro modelos; (b) licença CC BY; (c) 14 RCTs incluídos, dos quais **8 com texto integral em acesso aberto** (barra de viabilidade era ≥6); (d) 11 tabelas publicadas cobrindo as três tarefas — características basais, dados intraoperatórios, desfechos por braço, risco de viés em 7 domínios e GRADE; (e) tema (hemodinâmica perioperatória) adjacente ao corpus FIEL (artigo A2, circulação extracorpórea), preservando continuidade temática entre os benchmarks.

## 3. Corpus congelado

Os primários avaliáveis são os 8 estudos da tabela de características da âncora com XML integral no Europe PMC (baixados por `scripts/estudo1/baixar-corpus.py` em 2026-08-27, congelados em `corpus/primarios/`):

| Ref | PMCID | Estudo | Ano | Licença |
|---|---|---|---|---|
| 24 | PMC11061212 | Castro et al. | 2024 | CC BY-NC-ND |
| 27 | PMC10694978 | Sun et al. | 2023 | CC BY |
| 28 | PMC10561433 | Yoon et al. | 2023 | CC BY |
| 34 | PMC6907038 | Sujatha et al. | 2019 | CC BY |
| 36 | PMC10912221 | Wu et al. | 2024 | CC BY |
| 39 | PMC5589093 | Weinberg et al. | 2017 | CC BY |
| 44 | PMC4782303 | Schmid et al. | 2016 | CC BY |
| 45 | PMC12565272 | Redondo Calvo et al. | 2025 | CC BY |

Os 6 primários fechados (refs 26, 29, 30, 33, 41, 47) ficam fora do Estudo 1; suas linhas permanecem no gabarito apenas como contexto.

**Gabarito**: `dados/estudo1/gabarito-ma.json` — as 11 tabelas da âncora transcritas célula a célula **como publicadas**, sem qualquer correção (gerado por `scripts/estudo1/extrair-gabarito.py`).

**Regra de versionamento dos perturbados**: as cópias perturbadas NÃO são versionadas no repositório. São geradas localmente por script determinístico com seed fixa a partir dos originais congelados. Motivo duplo: (a) a licença ND do Castro et al. proíbe distribuir derivadas; (b) a tabela de perturbação fica **selada** até a correção, como manda o rito.

## 4. Inconsistências pré-existentes da âncora (registradas ANTES das corridas)

Detectadas na montagem do corpus e congeladas aqui para que a correção não tenha liberdade interpretativa. Nenhuma foi "consertada" no gabarito:

1. **RoB (tabela 1)** lista "Ramsingh et al. [21]" — estudo que **não consta** da tabela de características — e **omite** Weinberg et al. [39].
2. **Intraoperatória (tabela 4)** lista "Koo et al. [37]" e "Peltoniemi et al. [38]" (também fora das características; ambos CC BY) e **omite** Schmid et al. [44].
3. **Morbidade (tabela 5)** traz "**Yun** et al." com totais 39 (GDFT) / 36 (controle), enquanto a tabela de características dá **Yoon** et al. como 36 (GDFT) / 39 (controle) — grafia divergente e braços possivelmente trocados.
4. O título do Redondo Calvo et al. aparece no registro da revista com o typo "Person**alizezed**" (preservado nas citações).
5. **A linha do Sujatha et al. na tabela de características está corrompida**: a célula ASA do controle diz "2 days, 11:42:00" — um artefato clássico de formatação de hora do Excel no lugar de uma razão ASA; o n do GDFT (200) corresponde à fusão dos braços FloTrac+PVI (100+100) do ensaio de três braços, e o n do controle (101) não aparece literalmente no texto do primário.

Linhas dos estudos-fantasma (refs 21, 37, 38) não pontuam em nenhuma tarefa. Cada inconsistência será adjudicada contra as fontes primárias durante a correção e, se confirmada, entra no arquivo de erratas da âncora.

## 5. Tarefas e formulário

### T1 — Extração estruturada (por primário)

O modelo recebe: o texto integral do primário **perturbado** (artigo primeiro, instruções depois — aproveita o cache de prefixo KV) + o formulário abaixo. Devolve JSON, um objeto por campo: `{"valor": "<como reportado>", "onde": "<seção/tabela do artigo>"}`. Campo não reportado no artigo: `{"valor": "NR"}`.

Campos (fatos primários; espelham as colunas das tabelas 3–11 da âncora):

```
n_randomizados_gdft, n_randomizados_controle
tipo_cirurgia
laparoscopia_gdft, laparoscopia_controle            (como reportado: contagem ou %)
asa_gdft, asa_controle                              (razão I:II:III:IV, como reportado)
fluido_total_gdft, fluido_total_controle            (mL; média±DP ou mediana(IIQ), como reportado)
cristaloide_gdft, cristaloide_controle
coloide_gdft, coloide_controle
perda_sanguinea_gdft, perda_sanguinea_controle
uso_inotropico                                      (como reportado)
morbidade_eventos_gdft, morbidade_eventos_controle  (n de pacientes com ≥1 complicação)
mortalidade_gdft, mortalidade_controle              (óbitos intra-hospitalares ou 30 dias)
los_hospitalar_gdft, los_hospitalar_controle        (dias, por braço)
tempo_flatus_gdft, tempo_flatus_controle
tempo_ingesta_oral_gdft, tempo_ingesta_oral_controle
tempo_evacuacao_gdft, tempo_evacuacao_controle
ileo_pos_op_gdft, ileo_pos_op_controle              (n de casos)
```

Ficam fora (cálculo meta-analítico dos revisores): RR, MD, IC95%, pesos, GRADE.

### T2 — Risco de viés (por primário)

Mesmo artigo perturbado (mesmo prefixo KV), instruções distintas: julgar os 7 domínios Cochrane da tabela 1 da âncora — geração de sequência, ocultação de alocação, cegamento de participantes/equipe, cegamento de avaliadores de desfecho, dados incompletos, relato seletivo, outros vieses — mais o julgamento global. Saída JSON: `{"dominio": {"julgamento": "Low|High|Unclear", "justificativa": "<1 frase>"}}`.

### T3 — Síntese (por modelo)

O modelo recebe **as próprias extrações T1** (réplica 1 dos 8 primários, sem o texto dos artigos) e escreve, em português, uma síntese narrativa de 250–400 palavras do corpo de evidência: efeito da GDFT sobre morbidade, mortalidade, tempo de internação e função intestinal, com direção, magnitude qualitativa e incerteza. Proibido inventar números ausentes das extrações.

## 6. Perturbação (prova de leitura dupla)

- **K = 3 números por primário**, escolhidos entre valores que aparecem no gabarito da âncora (garantindo que a célula correspondente do formulário é atingida), um por região distinta do artigo quando possível (abstract/métodos/resultados).
- Magnitude: alteração de 5–15% do valor, plausível no contexto, sem colidir com outro valor real do artigo; mesma quantidade de casas decimais.
- Todas as ocorrências do número no texto são alteradas de forma consistente (inclusive tabelas do primário).
- A tabela original↔perturbado (`perturbacoes-estudo1.json`, local, fora do repositório) fica **selada até a correção** e é publicada integralmente junto com a avaliação.
- Na correção, célula perturbada: valor perturbado → pontua normalmente ("leu"); valor original publicado → **recitação** (zera a célula, conta como evidência de contaminação); demais casos → regras normais.

## 7. Pontuação e tolerâncias (T1)

Rótulos e valores conforme o `METHOD.md`. Tolerâncias pré-registradas para "exata":

- Arredondamento na última casa decimal reportada pelo gabarito (ex.: 3810,4 ≈ 3810).
- Conversão de unidade explícita e correta (L↔mL, h↔dias).
- Formato equivalente de razão ASA (ex.: "7:31:5:0" ≡ "I=7, II=31, III=5, IV=0").
- Média±DP vs mediana(IIQ): se o gabarito e o modelo reportarem estatísticas diferentes, a célula vai a adjudicação (a fonte decide qual estatística o artigo de fato reporta).
- "NR" do gabarito + valor do modelo → adjudicação obrigatória (candidata a discordante-adjudicada-modelo: o revisor pode ter perdido o dado).

**Adjudicação**: toda célula não-exata passa pelo rito (verificar na fonte primária antes de deduzir), com citação literal registrada no arquivo de avaliação. Adjudicador: juiz LLM (Sonnet 5, mesmo da linha FIEL) + autor humano em desempate.

## 8. Modelos e configurações (congelados da tabela FIEL)

| Modelo | Execução | Contexto | Amostragem |
|---|---|---|---|
| gemma4:12b | Vulkan (iGPU 780M) | 16.384* | do fabricante |
| qwen3:14b | Vulkan (iGPU 780M) | 16.384* | do fabricante, thinking off |
| qwen3.8:27b | CPU (`num_gpu=0`) | 16.384* | do fabricante, thinking off |
| gemma4:26b | CPU (`num_gpu=0`) | 16.384* | do fabricante |

\* Os primários integrais são maiores que os artigos do FIEL. A fase F0 (sondagem, antes das corridas oficiais) mede o tamanho real de cada primário em tokens; se algum exceder o contexto, o contexto sobe para 32.768 **para todos os modelos naquele primário**, com registro no relatório. Nenhum truncamento silencioso é permitido.

## 9. Réplicas e fila

- T1: 8 primários × 4 modelos × **2 réplicas** = 64 corridas.
- T2: 8 × 4 × **2 réplicas** = 64 corridas.
- T3: 4 modelos × **1 réplica** = 4 corridas.
- Ordem da fila por (modelo, primário): T1r1 → T1r2 → T2r1 → T2r2 — o artigo vem antes das instruções no prompt, então as quatro corridas reaproveitam o prefixo KV.
- A concordância entre réplicas (proporção de células idênticas r1 vs r2) é reportada como métrica de estabilidade.

## 10. Hipóteses pré-registradas

- **H1.1 (inversão de ordem)**: na acurácia de célula da T1, os dois grandes fiéis superam os dois menores — predição direcional: qwen3.8:27b ≥ gemma4:26b > gemma4:12b ≥ qwen3:14b. A ordem de extração NÃO repete a ordem de escrita do FIEL (onde 12b > 26b > 14b > 27B na média).
- **H1.2 (leitura, não recitação)**: zero células de recitação (valor original em célula perturbada) — a âncora é pós-corte e os primários, mesmo os antigos, não foram decorados com precisão numérica.
- **H1.3 (invenção rara)**: taxa de invenção < 5% das células em todos os modelos; omissão será mais comum que invenção.
- **H1.4 (RoB na faixa humana)**: concordância global com os revisores entre 60% e 90% dos domínios (literatura de concordância inter-revisor humana em RoB fica tipicamente em 70–85%).
- **H1.5 (síntese preserva direção)**: todos os modelos preservam a direção do efeito nos desfechos onde suas próprias extrações estão corretas; erros de direção só ocorrem a jusante de células erradas.
- **H1.6 (auditoria reversa)**: ≥1 discordância será adjudicada a favor do modelo — isto é, o Estudo 1 encontrará pelo menos um erro de extração dos revisores humanos da âncora (as inconsistências da seção 4 sugerem que a revisão não é imaculada).

## 11. Métricas reportadas

1. Acurácia de célula por modelo (principal), com decomposição exata/derivável/adjudicada.
2. Taxa de invenção e taxa de omissão, separadas.
3. Prova de leitura: leu / recitou / ausente, por modelo (12 células perturbadas × réplicas).
4. Concordância RoB global e por domínio; estabilidade entre réplicas.
5. Veredito de síntese por desfecho (direção preservada/invertida/inventada).
6. Erratas da âncora encontradas (H1.6), com citação da fonte.
7. Tempo de parede e tokens por corrida (economia de extração vs sumarização).

## 12. O que este estudo NÃO testa

Prompts em inglês (os primários são em inglês; as instruções, em português — o cenário do pesquisador brasileiro), outras quantizações, modelos fora da tabela FIEL, e extração de figuras/forest plots (só texto e tabelas). Cada um é candidato a estudo futuro.

## 13. F0 — sondagem de tamanhos (2026-08-27, antes de qualquer corrida)

Texto útil (abstract + corpo) dos 8 primários, medido do XML congelado:

| PMCID | Palavras | ~Tokens |
|---|---|---|
| PMC10561433 (Yoon) | 6.122 | ~8.9 mil |
| PMC10694978 (Sun) | 5.040 | ~7.3 mil |
| PMC10912221 (Wu) | 6.744 | ~9.8 mil |
| PMC11061212 (Castro) | 5.092 | ~7.4 mil |
| PMC12565272 (Redondo Calvo) | 5.799 | ~8.4 mil |
| PMC4782303 (Schmid) | 6.888 | ~10.0 mil |
| PMC5589093 (Weinberg) | 5.593 | ~8.1 mil |
| PMC6907038 (Sujatha) | 3.873 | ~5.6 mil |

Maior primário ≈ 10 mil tokens; com formulário (~1,2 mil) e saída T1 (~1,5 mil), o pior caso fica em ~12,7 mil — **dentro do contexto congelado de 16.384 para todos os modelos**. A cláusula de subida para 32.768 (seção 8) não será acionada.

---

## Emendas

### Emenda 1 — regras operacionais da perturbação (2026-08-27, antes de qualquer corrida)

Registrada durante a construção das cópias perturbadas, antes de qualquer modelo ler qualquer texto:

1. **Seleção automática com âncoras semânticas.** Um número do gabarito só é elegível se todas (números redondos ou de 2 dígitos) ou ao menos uma (números com ≥3 dígitos significativos) de suas ocorrências no texto estiverem a ≤120 caracteres de uma palavra-âncora do campo (ex.: fluido→"fluid/volume/infused", morbidade→"complications"). Motivo: a primeira rodada automática mostrou que números curtos ("19", "72", "200") colidem com fatos alheios — porcentagens de outras variáveis, horários de medição, bolus de protocolo e até faixas de páginas de referências. Cada célula do gabarito pode ser perturbada no máximo uma vez; listas de referências são removidas do texto antes de tudo.
2. **Curadoria manual documentada.** Onde o automático não alcança K=3, valores adicionais podem ser escolhidos à mão, com TODAS as ocorrências inspecionadas e registradas (arquivo `perturbacoes-manuais.json`, selado junto com a tabela principal). A inspeção manual substitui a âncora automática.
3. **Primários sem valor literal do gabarito.** Quando nenhuma célula do gabarito existe literalmente no texto (caso Sujatha: a MA fundiu braços e derivou/converteu estatísticas), perturbam-se números do texto que **alimentam campos do formulário** (ex.: cristaloides por braço). Nesses valores a checagem de recitação-da-revisão é vazia por construção (o número não está na MA), mas a checagem de leitura e a de memorização-do-primário permanecem ativas.
4. **K é alvo, não garantia.** Estudos podem ficar com menos de 3 perturbações quando não há valores seguros (caso Schmid: os n dos braços aparecem 14+ vezes em contextos mistos e nenhuma outra célula numérica é utilizável). O número final por estudo fica registrado no selo.

### Emenda 3 — dois vazamentos de perturbação; prova neutralizada em duas células (2026-08-27, detectada durante o bloco 2, antes de qualquer correção)

Auditoria disparada por um evento de aparente "recitação" do qwen3:14b revelou que a falha era **do harness, não do modelo**: a fronteira regex da substituição não alcançou duas ocorrências dos valores originais, que permaneceram no texto perturbado que os modelos leram:

1. **Weinberg (PMC5589093)**: "…2050mL (1199:2700) vs. **4088mL** (3400:4525)…" — o número colado à unidade ("4088mL") escapa do lookahead `(?![\w.])`.
2. **Sun (PMC10694978)**: "…[1199 ml (**800-2750** ml)…" — o hífen de faixa aciona a guarda criada contra "COVID-19"/páginas de referência, e a ocorrência não foi substituída.

Regras decorrentes, simétricas para os quatro modelos:
- Nas células `fluido_total_controle` do Weinberg (4088→4620) e do Sun (2750→2906), o veredito **"recitou" é inatribuível** (o original estava no insumo). "Leu" continua atribuível quando o modelo devolve o valor perturbado. Essas duas células saem do denominador de recitação da H1.2.
- O episódio do qwen3:14b (devolveu 4088 nas duas réplicas) fica registrado como **leitura de insumo inconsistente**, não como contaminação.
- O corpus perturbado permanece **congelado** como está para todo o Estudo 1 (consertar no meio quebraria a comparabilidade entre blocos já corridos e por correr). A correção da fronteira (permitir unidade colada; distinguir hífen de faixa numérica de hífen de sigla) aplica-se ao estrato fechado da Emenda 2 [a registrar] e a estudos futuros.

### Emenda 4 — gabarito oficial verificado na fonte; métrica primária redefinida (2026-08-27, antes de qualquer correção; pedido do autor)

Motivo: durante os blocos 1–3, três modelos extraíram independentemente n=39/36 para o Yoon, contra os 36/39 da tabela de características da âncora — e a fonte primária confirma os modelos ("The GDHT group (n = 39)… the control group (n = 36)"). A metanálise publicada contém erros de extração; usá-la como régua final puniria os modelos por estarem certos.

Regras:
1. **Gabarito em duas camadas.** A camada 1 (`gabarito-ma.json`, como publicado) permanece congelada e intocada. A camada 2 (`gabarito-oficial.json`) é construída verificando **cada célula avaliável na fonte primária original**, com: valor como a fonte reporta, **citação literal** do trecho que o sustenta, e a relação com a MA (literal / derivável / **errata-da-MA** / MA-inferiu / NR-real).
2. **Métricas redefinidas.** A métrica primária do Estudo 1 passa a ser a **acurácia contra a fonte** (camada 2). A **concordância com os revisores humanos** (camada 1) vira métrica secundária — e suas divergências explicadas (erratas da MA) são reportadas como resultado próprio (H1.6).
3. **Método de verificação.** Um script (`verificar-gabarito.py`, público) localiza cada valor na fonte com equivalências pré-declaradas (contagem↔percentual via n do braço; horas↔dias; arredondamento na última casa) e registra os trechos candidatos; o autor-adjudicador (Claude, com supervisão do autor humano) confirma célula a célula. Células sem sustentação clara ficam "pendente-adjudicação" e não pontuam contra nenhum modelo.
4. **Disclosure de independência.** A verificação usa apenas os textos originais e a MA — não as saídas dos modelos —, mas foi iniciada depois de o adjudicador ter visto saídas parciais dos blocos 1–3. Mitigação: toda célula do gabarito oficial carrega citação literal da fonte, auditável por qualquer terceiro; nenhuma célula é aceita sem trecho.
5. As perturbações continuam por cima: célula perturbada pontua contra o valor perturbado (a "verdade do insumo" que o modelo leu), com o original registrado na camada 2.
