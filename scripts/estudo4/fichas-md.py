# -*- coding: utf-8 -*-
"""EXTRAI Study 4 round 2 — side-by-side reading sheets, human-readable.

Builds a Markdown document showing, for every trial and every graded field,
what each of the five models wrote (first-parseable replicate), what the
answer key accepts, and the mechanical grader's verdict for that cell.

Run: python scripts/estudo4/fichas-md.py
Output: dados/estudo4/rodada2/fichas-comparadas.md
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
R2 = ROOT / "dados" / "estudo4" / "rodada2"
MODELOS = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14"]
GLIFO = {"exata": "✓", "derivavel": "≈", "nr-correta": "✓NR", "omissa": "—",
         "errada": "✗", "recitou": "‼", "recitacao-inatribuivel": "~", "adjudicar": "?"}


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


h3 = carrega("h3", "scripts/estudo3/e3-harness.py")
c3 = carrega("c3", "scripts/estudo3/corrigir-e3.py")

corr = json.loads((R2 / "correcao" / "extracao-gemma12-qwen14-llama8-qwen35-deepseek14.json")
                  .read_text(encoding="utf-8"))
rotulo = {(d["modelo"], d["trial"], d["rep"], d["campo"]): d["rotulo"] for d in corr["detalhes"]}


def ficha_rep(modelo, tid):
    for rep in (1, 2):
        f = R2 / "saidas" / modelo / "extracao" / f"{tid}-r{rep}.json"
        if f.exists():
            js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            if js:
                return js, rep
    return None, None


def curto(v, n=16):
    s = "·" if v is None else str(v).strip()
    return s if len(s) <= n else s[:n - 1] + "…"


L = ["# Estudo 4 · rodada 2 — fichas de leitura lado a lado",
     "",
     "O que cada modelo escreveu em cada campo com gabarito (réplica que alimenta o pool), "
     "o que o gabarito aceita (valores do MUNDO PERTURBADO — os textos lidos têm números "
     "deliberadamente trocados), e o veredito mecânico da célula.",
     "",
     "Vereditos: ✓ exata · ≈ derivável · ✓NR não-relatado correto · — omitiu · "
     "✗ errada · ? aguardando adjudicação na fonte (rito) · ‼ recitou o valor original · "
     "· = campo vazio. Fichas brutas (JSON) em `saidas/<modelo>/extracao/`.",
     ""]

for tid in h3.TRIALS:
    rot = h3.ROT[tid]
    L.append(f"## {rot} ({tid})")
    L.append("")
    fichas = {}
    reps = {}
    for m in MODELOS:
        fichas[m], reps[m] = ficha_rep(m, tid)
    L.append("| campo | gabarito aceita | " + " | ".join(
        f"{m} (r{reps[m]})" if reps[m] else f"{m} (falhou)" for m in MODELOS) + " |")
    L.append("|" + "---|" * (len(MODELOS) + 2))
    for campo, esp in c3.EXPECTED[tid].items():
        aceitos = curto(" ou ".join(str(a) for a in esp["aceitos"]), 22)
        cells = []
        for m in MODELOS:
            if not fichas[m]:
                cells.append("(sem ficha)")
                continue
            v = c3.pega(fichas[m], campo)
            g = GLIFO.get(rotulo.get((m, tid, reps[m], campo), ""), "")
            cells.append(f"{g} {curto(v)}".strip())
        L.append(f"| {campo.replace('braco_', '').replace('hba1c_', '')} | {aceitos} | "
                 + " | ".join(cells) + " |")
    L.append("")

out = R2 / "fichas-comparadas.md"
out.write_text("\n".join(L), encoding="utf-8")
print(f"gravado {out} ({len(L)} linhas)")
