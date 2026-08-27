# EXTRAI — roadmap

Registro de estudos futuros discutidos com o autor. Nada aqui é protocolo: cada estudo
ganha pré-registro próprio (hipóteses, regras, corpus) antes de qualquer corrida.

## Estudo 1 — extração, risco de viés e síntese (EM ANDAMENTO)

Protocolo: [`dados/estudo1/protocolo-estudo1.md`](dados/estudo1/protocolo-estudo1.md).
Fila oficial dos 8 primários abertos rodando desde 2026-08-27.

**Extensão já garantida (Emenda 2, a registrar ao fim da fila):** o autor obteve
legalmente os 6 primários fechados (acesso institucional + manuscritos de autor
gratuitos localizados via Europe PMC/NCBI) — o corpus salta para **14/14, a
metanálise inteira**. Estrato fechado roda simetricamente para os 4 modelos após a
fila principal; os PDFs/XMLs fechados nunca entram no repositório (direitos
autorais; ficam em `corpus/fechados-staging/`, fora do versionamento). Pipeline
extra: extração de texto de PDF (pypdf) com normalização de ligaduras (ﬂ→fl) e
hifenização.

## Estudo 2 — "as contas": refazer a estatística da metanálise (DESENHADO, não registrado)

Pergunta: os modelos conseguem transformar as extrações em metanálise de verdade —
RR/MD por estudo, IC95%, agrupamento (Mantel-Haenszel / variância inversa /
DerSimonian-Laird)?

Desenho em dois braços, mesmo corpus e mesmas extrações T1 do Estudo 1:

- **Braço A — de cabeça**: o modelo calcula sem ajuda. Mede aritmética bruta e,
  mais importante, se o modelo *admite* não conseguir calcular ou confabula um
  IC95% com cara de estatística (a invenção mais perigosa numa revisão).
- **Braço B — com calculadora (a proposta do autor)**: o harness oferece funções
  (`rr`, `ic95_rr`, `md`, `pool_mh`, `pool_dl`); o modelo chama, o Python computa,
  o resultado volta ao contexto. Protocolo de TEXTO uniforme como braço principal
  (`CALC: rr(19, 58, 32, 56)` → `RESULTADO: 0.573`) — mesmo mecanismo para as 4
  famílias, sem depender de template de tool-calling. Tool calling nativo do
  Ollama (`/api/chat` + `tools`) como braço exploratório.
- **Delta A→B é a medida de ouro**: separa "não sabe metanálise" de "só não tem
  calculadora". Se B ≈ teto, a conclusão é deployável: modelo local + biblioteca
  de funções = assistente de revisão sistemática em hardware de consumidor.

Gabarito duplo: os valores publicados na âncora (tabelas 5–11) + os valores
verdadeiros recomputados em Python (o que também audita a estatística da própria
metanálise). Candidato natural para reativar o braço *thinking* do qwen3 (inútil
para escrever nas Séries 1–2 do FIEL; nunca testado para calcular).

Predições a formalizar no pré-registro: direção quase sempre certa; RR por estudo
~metade no braço A e perto do teto no B; IC95% e agrupamento ≈ zero no A;
agrupamento ainda difícil no B (orquestrar várias chamadas é planejamento
multi-etapa); ranking real = quem sabe que não sabe.

## Ideias em fila (sem desenho)

- Estudo de línguas (instruções em inglês vs português).
- gemma4:31b denso como quinto extrator (sondado no FIEL E14: 2,7 tok/s, viável-marginal).
- Juiz-extrator cruzado: um modelo local audita as extrações de outro (herança do E11/FIEL).
