# Erratas e células não sustentadas da metanálise-âncora (PMC13235771)

Registro da Emenda 4 do [protocolo](protocolo-estudo1.md). Cada item foi decidido pela
fonte primária original, com a citação literal que o sustenta. As tabelas da âncora
permanecem intocadas em `gabarito-ma.json`; a régua da correção é `gabarito-oficial.json`.

**Quem fez o quê**: as discrepâncias 1 e 2 foram *levantadas pelos modelos locais* (três
modelos extraíram, independentemente, valores contrários à tabela publicada) e
*confirmadas pelo adjudicador* (Claude) na fonte; as demais emergiram da verificação
célula a célula do adjudicador. A supervisão é do autor humano do benchmark.

## Confirmadas pela fonte

1. **Yoon et al. — braços trocados na tabela de características.** A MA publica GDFT 36 /
   controle 39. A fonte: *"The GDHT group (n = 39) received the stroke volume index- and
   cardiac index-based…"* e *"the control group (n = 36) received the standard care"*.
   Correto: **GDFT 39 / controle 36**. (Resolve também a inconsistência interna
   pré-registrada nº 3: a linha "Yun" da tabela de morbidade, com 39/36, estava certa.)

2. ~~**Redondo Calvo et al. — braços trocados.**~~ **RETIRADA — errata do adjudicador
   (2026-08-28).** A primeira versão desta lista declarou braços trocados com base apenas
   no abstract (*"randomized to the GDHT (n = 16) and control group (n = 19)"*). O corpo
   do artigo diz o oposto em quatro lugares — fluxograma (*"There were 16 patients in the
   control group and 19 patients in the GDHT group"*) e as três tabelas (*"Control N = 16
   GDHT N = 19"*). Pela preponderância, **a MA está certa (GDFT 19 / controle 16)**; o
   achado real é que **o primário Redondo se contradiz internamente** (abstract vs corpo).
   A correção aceita as duas leituras conforme o "onde" citado pelo modelo. Fica o
   registro público: o adjudicador (Claude) errou por verificar contra um único trecho —
   o mesmo pecado que este benchmark existe para caçar.

3. **Weinberg et al. — ASA "Not stated".** A MA declara a distribuição ASA como não
   reportada. A tabela do artigo reporta, para os dois braços: *"ASA Class I-II 7 (27%)
   7 (27%) ASA Class ≥ III 19 (73%) 19 (73%)"*.

## Não sustentadas no texto integral do primário

4. ~~**Wu et al. — "Inotrope use: Lower in GDFT".**~~ **RETIRADA — errata do adjudicador
   nº 2 (2026-08-28).** A busca da primeira versão usava janelas de contexto rígidas que
   esconderam as linhas da Tabela 3 do Wu. Elas existem e sustentam a MA: *"Number of
   patients using norepinephrine 15 (25.9) 24 (42.9) … phenylephrine 12 (20.7) 24 (42.9)
   … ephedrine 12 (24.0) 19 (35.2)"* — menor uso no braço GDFT nas três drogas. Os três
   modelos que extraíram esses valores (acusados por engano de fabricação na primeira
   análise) estavam **literalmente certos**. Segunda vez na mesma noite que os modelos
   vencem o adjudicador; o instrumento de busca foi corrigido (janelas flexíveis).

5. **Sujatha et al. — ASA "95:105".** O texto reporta apenas a elegibilidade ("ASA I and
   II") e diz que a distribuição foi "comparable", sem números. A célula do braço
   controle, na MA, está corrompida por formatação de hora do Excel (*"2 days,
   11:42:00"*) — inconsistência pré-registrada nº 5.

## Confirmadas pela fonte (adição da adjudicação, 2026-08-28)

8. **Sun et al. — conversão do tempo até dieta oral inconsistente.** A MA publica
   72±24 h (GDFT) vs 96±30 h (controle) — diferença de 1 dia. O próprio texto-fonte diz:
   *"GDFT significantly also shorten … time to first tolerate oral diet **by 2 days**
   (P < 0.001)"*, com medianas 4,0 d (2,7–6,0) vs 6,0 d (5,0–9,3). Os quatro modelos
   extraíram 4,0/6,0 dias, unânimes. A conversão da MA contradiz a fonte que ela resume.

## Divergência definicional (não é erro, é escolha não declarada)

6. **Sujatha et al. — n por braço.** A fonte: *"306 patients, with 102 in each group,
   were enrolled"*. A MA registra 200 (GDFT fundido) e 101 (controle) — números de
   pacientes *analisados*, não *randomizados*, sem declarar a escolha. A correção aceita
   ambas as leituras.

7. **Castro et al. — rótulo de cirurgia estreito.** MA: "All major bowel surgeries";
   fonte: *"elective open abdominal surgeries"*, incluindo hepatectomia, gastrectomia e
   duodenopancreatectomia.

8. **Wu et al. — n por braço.** A MA registra 58/56 (analisados). A fonte diz
   literalmente: *"122 subjects were randomly assigned… Specifically, 61 patients were
   allocated to the PPV group and another 61…"*. Como no Sujatha, a MA usou analisados
   sem declarar; a correção aceita as duas leituras.

## Pendentes de adjudicação final (fora de pontuação)

- Yoon — uso de inotrópicos ("No difference"): comparativo não localizado no texto.
- Sun — íleo 2 (4,0%) / 16 (32,0%): possivelmente derivado do escore I-FEED.
- Castro — íleo 6 (14,0%) / 19 (45,2%): termo "ileus" ausente do texto.
- Redondo — perda sanguínea GDFT 292,6 ± 274,1: valor literal não conferido.

*Nota de método: a verificação usa o texto integral (abstract + corpo, incluindo
tabelas); valores presentes apenas em figuras ou suplementos não são alcançados —
células assim marcadas não pontuam contra nenhum modelo.*
