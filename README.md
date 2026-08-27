# EXTRAI — benchmark de extração de evidência científica para LLMs locais

*Evidence-extraction benchmark for local LLMs, in Brazilian Portuguese. English articles will accompany each study.*

O [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr) pergunta se um modelo local *escreve* com fidelidade. O **EXTRAI** pergunta se ele *lê* como um revisor: diante de um ensaio clínico completo, o modelo extrai o que os revisores humanos de uma metanálise publicada extraíram — números certos, das seções certas, admitindo o que o artigo não reporta?

- **[METHOD.md](METHOD.md)** — o método completo: as três tarefas (extração estruturada, risco de viés, síntese), a pontuação célula a célula com juiz mecânico, a prova de leitura dupla por perturbação e o rito de adjudicação em que o gabarito humano também está em julgamento.
- **[Protocolo do Estudo 1](dados/estudo1/protocolo-estudo1.md)** — pré-registrado em 2026-08-27: metanálise-âncora de fluidoterapia guiada por metas (Cureus, jun/2026, CC BY), 8 RCTs primários em acesso aberto, 4 modelos veteranos do FIEL, 6 hipóteses.

## Estrutura

```
METHOD.md                     o método (a constituição do benchmark)
corpus/ma/                    metanálise-âncora (XML integral + metadados)
corpus/primarios/             RCTs primários em acesso aberto (XML integral)
dados/estudo1/                protocolo, gabarito e (depois) avaliações do Estudo 1
scripts/estudo1/              scripts de corpus e correção
```

As cópias perturbadas dos primários não são versionadas: são geradas localmente por script determinístico e a tabela de perturbação fica selada até a correção (ver protocolo, seção 6).

## Licenças do corpus

A metanálise-âncora (PMC13235771) é CC BY 4.0. Os primários são CC BY, exceto Castro et al. (PMC11061212), CC BY-NC-ND 4.0 — redistribuído aqui verbatim, sem derivadas, em contexto não comercial. Atribuições completas na tabela do protocolo.

## Autor

Gustavo Barra — benchmark conduzido com assistência de Claude (Anthropic). Modelos avaliados: gemma4:12b, qwen3:14b, qwen3.8:27b, gemma4:26b via Ollama, em hardware de consumidor (Ryzen 7 + iGPU 780M).
