# -*- coding: utf-8 -*-
"""Escreve as duas fichas de extração da âncora 3. Instrumento 6 da §8.

A v1 é escrita aqui por extenso. A v2 é **derivada** dela por transformação mecânica, e não redigida
em paralelo: no Estudo 9 as duas fichas foram escritas à mão e o par saiu assimétrico entre as âncoras
(a v2 da âncora 1 manda aparar a citação em 240 caracteres e proíbe traduzir; a da âncora 2 não diz
nem uma coisa nem outra). Derivar garante que a única diferença entre os braços do A/B seja a citação,
que é o que o A/B existe para medir.

A transformação é a mesma que o Estudo 9 aplicou: acrescenta uma regra sobre a citação, e troca a
forma dos campos de DADO de {"value","where"} para {"value","where","quote"}. Campos descritivos —
rótulo do braço e descrição da intervenção — ficam como estão, seguindo o precedente da ficha da
âncora 2.

O que esta ficha faz de diferente das duas congeladas, e a §8 do protocolo declara:
  · pede os braços em LISTA, porque um dos ensaios tem três e a regra de braço múltiplo das fichas
    antigas devolve texto livre com " | " que nenhum calculador transforma em pares (a, n);
  · pede o percentual por braço como campo próprio, porque dois dos oito ensaios publicam só o
    percentual e nenhuma contagem;
  · pede o ponto no tempo como campo próprio, porque nesta âncora a janela do desfecho é disputada.
Nenhuma dessas três é neutra em relação aos dois erros humanos da revisão, e o protocolo diz isso com
todas as letras em vez de deixar a leitura bondosa passar.

O que a ficha NÃO faz: não avisa contra transcrever sobreviventes no lugar de mortos, embora tenha
sido esse o erro do Aguilar. Avisar transformaria uma medição em dica.
"""
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DEST = Path(__file__).resolve().parents[2] / "dados" / "estudo12" / "prompts"

V1 = """SCIENTIFIC ARTICLE (sole and exclusive source for this task):

{ARTICLE}

---

TASK — EVIDENCE EXTRACTION FOR META-ANALYSIS

You are a systematic-review reviewer. Extract from the article above the data on ALL-CAUSE MORTALITY, arm by arm.

Mandatory rules:
1. Use ONLY the article above. Do not use any prior knowledge about this trial.
2. Transcribe the values AS REPORTED in the article: keep the original decimal places, and copy a percentage exactly as printed.
3. If the datum is NOT reported in the article, write exactly "NR" in the value field.
4. List EVERY arm the trial has, in the order the article introduces them, including placebo arms and active-comparator arms. Report each arm on its own; combining arms is not part of this task.
5. Report mortality once for EACH moment at which the article measures it. If the article reports mortality at 28 days and again at 90 days, that is two entries per arm.
6. Answer ONLY with a valid JSON object, with no text before or after it, and no code fences.
7. Each field is an object {"value": "...", "where": ""} — "where" states the section or table of the article the datum was taken from (e.g., "Results", "Table 2", "Abstract").

Form (use exactly these keys; repeat the objects inside "arms" and "mortality" as many times as the trial requires):

{
  "study": {"value": "", "where": ""},
  "design": {"value": "", "where": ""},
  "arms": [
    {
      "label": {"value": "", "where": ""},
      "intervention": {"value": "", "where": ""},
      "n_randomized": {"value": "", "where": ""},
      "n_analyzed": {"value": "", "where": ""}
    }
  ],
  "mortality": [
    {
      "arm_label": {"value": "", "where": ""},
      "timepoint": {"value": "", "where": ""},
      "deaths": {"value": "", "where": ""},
      "n": {"value": "", "where": ""},
      "deaths_percent": {"value": "", "where": ""}
    }
  ]
}

Definition notes: "label" = what the article calls that arm (e.g., "Group A", "methylene blue 1 mg/kg", "placebo"); "intervention" = what that arm received, in the article's words; "n_randomized" = patients randomized to that arm; "n_analyzed" = patients of that arm who entered the mortality analysis; "arm_label" = the label of the arm this mortality entry belongs to, exactly as written in "arms"; "timepoint" = the moment the article measures that mortality at, in the article's own words (e.g., "28 days", "at ICU discharge", "in-hospital", "90 days"); "deaths" = the number of patients in that arm who died; "n" = the denominator the article uses for that mortality figure; "deaths_percent" = the percentage the article prints for that arm's mortality, exactly as printed.
"""

# campos de dado: ganham citação na v2. Campos descritivos ficam como estão.
DADOS = ["n_randomized", "n_analyzed", "timepoint", "deaths", "n", "deaths_percent"]
DESCRITIVOS = ["study", "design", "label", "intervention", "arm_label"]

REGRA_CITACAO = (
    '7. Every data field is an object {"value": "...", "where": "...", "quote": "..."} — "where" '
    'states the section or table of the article the datum was taken from (e.g., "Results", "Table 2", '
    '"Abstract"); "quote" is the VERBATIM sentence or fragment of the article that contains the value, '
    'copied exactly as printed, at most 240 characters. Never paraphrase, never translate, never fix '
    'typography; if the sentence is longer than 240 characters, trim it around the value. If the value '
    'is "NR", write "" in where and quote. Descriptive fields — "study", "design", "label", '
    '"intervention" and "arm_label" — stay {"value": "...", "where": ""}.')


def deriva_v2(v1):
    """A transformação, e nada além dela."""
    fora = v1.replace(
        '7. Each field is an object {"value": "...", "where": ""} — "where" states the section or '
        'table of the article the datum was taken from (e.g., "Results", "Table 2", "Abstract").',
        REGRA_CITACAO)
    if fora == v1:
        raise SystemExit("a regra 7 da v1 não casou; a derivação foi abortada")
    for campo in DADOS:
        alvo = f'"{campo}": {{"value": "", "where": ""}}'
        novo = f'"{campo}": {{"value": "", "where": "", "quote": ""}}'
        if alvo not in fora:
            raise SystemExit(f"campo de dado {campo} não encontrado na v1")
        fora = fora.replace(alvo, novo)
    return fora


V2 = deriva_v2(V1)

# ------------------------------------------------------------------ conferências
falhas = []

# 1. os campos descritivos não podem ter ganhado citação
for campo in DESCRITIVOS:
    if f'"{campo}": {{"value": "", "where": "", "quote": ""}}' in V2:
        falhas.append(f"o campo descritivo {campo} ganhou citação e não devia")

# 2. todo campo de dado tem de ter citação na v2 e não ter na v1
for campo in DADOS:
    if f'"{campo}": {{"value": "", "where": "", "quote": ""}}' not in V2:
        falhas.append(f"o campo de dado {campo} não ganhou citação na v2")
    if '"quote"' in V1:
        falhas.append("a v1 não pode mencionar citação")

# 3. o diff tem de ser cirúrgico: só a regra 7 e as formas dos campos de dado
so_regra = [l for l in V2.splitlines() if l not in V1.splitlines() and not l.strip().startswith('"')]
if len(so_regra) != 1 or not so_regra[0].startswith("7. Every data field"):
    falhas.append(f"o diff tem {len(so_regra)} linhas de prosa diferentes, e devia ter 1: {so_regra}")

# 4. as duas têm de trazer o marcador do artigo e a mesma lista de chaves
for nome, t in (("v1", V1), ("v2", V2)):
    if "{ARTICLE}" not in t:
        falhas.append(f"{nome} não traz o marcador {{ARTICLE}}")
ch1 = sorted(re.findall(r'"(\w+)":\s*\{"value"', V1))
ch2 = sorted(re.findall(r'"(\w+)":\s*\{"value"', V2))
if ch1 != ch2:
    falhas.append(f"as chaves diferem: v1 {ch1} · v2 {ch2}")

# 5. nenhuma das duas pode conter instrução de polaridade
for nome, t in (("v1", V1), ("v2", V2)):
    if re.search(r"surviv|not the survivors|rather than survivors", t, re.I):
        falhas.append(f"{nome} contém instrução de polaridade, que o protocolo proíbe")

print(f"campos de dado com citação na v2: {len(DADOS)}")
print(f"campos descritivos sem citação:   {len(DESCRITIVOS)}")
print(f"chaves, iguais nas duas:          {len(ch1)}")
print(f"linhas de prosa diferentes:       {len(so_regra)} (a regra da citação)")
print(f"instrução de polaridade:          nenhuma")

if falhas:
    print("\nNÃO GRAVADO:")
    for f in falhas:
        print("  -", f)
    sys.exit(1)

DEST.mkdir(parents=True, exist_ok=True)
io.open(DEST / "a3-extraction.txt", "w", encoding="utf-8", newline="\n").write(V1)
io.open(DEST / "a3-extraction-v2.txt", "w", encoding="utf-8", newline="\n").write(V2)
import hashlib
for n in ("a3-extraction.txt", "a3-extraction-v2.txt"):
    b = io.open(DEST / n, "rb").read()
    print(f"\n{n}: {len(b)} bytes · SHA-256 {hashlib.sha256(b).hexdigest()}")
print("\nGRAVADO em dados/estudo12/prompts/")
