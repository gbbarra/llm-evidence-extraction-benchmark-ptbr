# -*- coding: utf-8 -*-
"""A prova de leitura por perturbação alcança a âncora 3? Medido, não suposto.

O método do projeto funda a prova de não-recitação no deslocamento selado de números: o modelo lê um
corpus em que valores-chave foram movidos 5 a 15%, e recitar o publicado passa a ser detectável. O
operador congelado (`scripts/estudo1/perturbar.py`) exige três coisas de um valor deslocado: mesmas
casas decimais, maior que zero, e **ausente do texto original**. As âncoras 1 e 2 têm médias e desvios
com casa decimal, onde isso é fácil. A âncora 3 tem contagens de eventos de um dígito, onde pode ser
impossível: qualquer inteiro pequeno já ocorre em qualquer artigo clínico.

Este script mede, valor a valor, o que o operador congelado consegue e o que não consegue nos oito
primários, para que o protocolo declare a consequência em vez de descobri-la no meio da campanha.
Nada aqui perturba nada: só pergunta se daria.
"""
import importlib.util
import io
import json
import random
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("pert", RAIZ / "scripts" / "estudo1" / "perturbar.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

PRIM = RAIZ / "dados" / "estudo11" / "primarios"
ARQ = {
    "Luis-Silva, 2024": "PMC11514138.xml", "Shaker, 2025": "PMC11707904.xml",
    "Ibarra-Estrada, 2023": "PMC10010212.xml", "Aguilar, 2016": "aguilar-2016-medcrit.txt",
    "Kirov, 2001": "kirov2001.txt", "Levin, 2004": "levin2004.txt",
    "Dong, 2025": "PMC12751372.xml", "Memis, 2002": "memis2002.txt",
}
# como cada fonte imprime a mortalidade: (rótulo, valor como aparece, papel)
COMO_A_FONTE_IMPRIME = {
    "Luis-Silva, 2024":     [("azul %", "47", "evento"), ("controle %", "61", "evento"),
                             ("n azul", "19", "denominador"), ("n controle", "23", "denominador")],
    "Shaker, 2025":         [("placebo n", "14", "evento"), ("placebo %", "46.7", "evento"),
                             ("1 mg/kg n", "9", "evento"), ("1 mg/kg %", "30.0", "evento"),
                             ("4 mg/kg n", "6", "evento"), ("4 mg/kg %", "20.0", "evento"),
                             ("n por braço", "30", "denominador")],
    "Ibarra-Estrada, 2023": [("azul n", "15", "evento"), ("azul %", "33", "evento"),
                             ("controle n", "21", "evento"), ("controle %", "46", "evento"),
                             ("n azul", "45", "denominador"), ("n controle", "46", "denominador")],
    "Aguilar, 2016":        [("azul %", "20.0", "evento"), ("controle %", "36.6", "evento"),
                             ("n por braço", "30", "denominador")],
    "Kirov, 2001":          [("sobrev. azul", "5", "evento"), ("sobrev. controle", "3", "evento"),
                             ("n por braço", "10", "denominador")],
    "Levin, 2004":          [("azul n", "0", "evento"), ("controle n", "6", "evento"),
                             ("controle %", "21.4", "evento"), ("n por braço", "28", "denominador")],
    "Dong, 2025":           [("azul n", "9", "evento"), ("azul %", "25.0", "evento"),
                             ("controle n", "15", "evento"), ("controle %", "41.7", "evento"),
                             ("n por braço", "36", "denominador")],
    "Memis, 2002":          [("mortalidade %", "26.6", "evento"), ("n por braço", "15", "denominador")],
}


def texto_de(arq):
    t = io.open(PRIM / arq, encoding="utf-8", errors="replace").read()
    if arq.endswith(".xml"):
        t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


print(f"{'ensaio':22s} {'campo':18s} {'valor':>8s} {'papel':12s} {'ocorre':>7s}  resultado")
print("-" * 96)
linhas = []
for ensaio, arq in ARQ.items():
    txt = texto_de(arq)
    for campo, valor, papel in COMO_A_FONTE_IMPRIME[ensaio]:
        rng = random.Random(2026)                      # semente fixa: o veredito é do operador, não do sorteio
        n_oc = len(P.ocorrencias(txt, valor)[0])
        novo = P.perturbar_valor(valor, rng, txt)
        # tentar 200 sementes antes de declarar impossível: separa azar de impossibilidade estrutural
        if novo is None:
            for s in range(200):
                if P.perturbar_valor(valor, random.Random(s), txt) is not None:
                    novo = "(só com outra semente)"
                    break
        ok = novo is not None
        linhas.append((ensaio, campo, valor, papel, n_oc, ok))
        print(f"{ensaio:22s} {campo:18s} {valor:>8s} {papel:12s} {n_oc:7d}  "
              f"{'perturbável -> ' + str(novo) if ok else 'IMPOSSÍVEL'}")

print("-" * 96)
ev = [x for x in linhas if x[3] == "evento"]
de = [x for x in linhas if x[3] == "denominador"]
dec = [x for x in ev if "." in x[2]]
inte = [x for x in ev if "." not in x[2]]
for rot, g in (("eventos, todos", ev), ("  dos quais com casa decimal", dec),
               ("  dos quais inteiros", inte), ("denominadores", de)):
    if not g:
        continue
    n = sum(1 for x in g if x[5])
    print(f"{rot:32s} {n:2d} de {len(g):2d} perturbáveis")

print(f"""
LEITURA. O padrão não é aleatório e não é azar de semente: o que quebra são os inteiros pequenos.
O operador exige que o valor deslocado esteja AUSENTE do texto, e um inteiro de um dígito deslocado
em 5 a 15% cai noutro inteiro de um dígito, que ocorre dezenas de vezes em qualquer artigo clínico.
O 0/28 do Levin é impossível por construção: a linha exige float(s) > 0.

Os percentuais com casa decimal, porém, se comportam como as âncoras 1 e 2 -- e sete dos oito ensaios
publicam a mortalidade também em percentual. Isso é a saída, e o protocolo tem de declará-la antes.""")

io.open(RAIZ / "dados" / "estudo12" / "perturbabilidade-ancora3.json", "w", encoding="utf-8").write(
    json.dumps([dict(ensaio=a, campo=b, valor=c, papel=d, ocorrencias=e, perturbavel=f)
                for a, b, c, d, e, f in linhas], ensure_ascii=False, indent=2) + "\n")
print("\ngravado: dados/estudo12/perturbabilidade-ancora3.json")
