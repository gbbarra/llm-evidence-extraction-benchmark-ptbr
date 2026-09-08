# -*- coding: utf-8 -*-
"""O desenho de perturbação da âncora 3 é factível? Prova, não promessa.

Corrigido em 2026-09-08: a primeira versão tratou os braços como independentes e deu 4,5 de 8. Está
errado. Braços que compartilham o denominador (Shaker 30/30/30, Aguilar 30/30, Levin 28/28, Dong
36/36, Kirov 10/10) têm de receber o MESMO deslocamento, porque o operador troca todas as ocorrências
do número no texto e não uma ocorrência escolhida. Um n' por grupo, e todos os percentuais
recomputados daquele grupo têm de passar.

A §5 do protocolo propõe deslocar o DENOMINADOR por braço e recomputar o percentual dependente, para
que o artigo continue internamente coerente (9 de 40 É 22,5%) enquanto um denominador recitado (36)
fica detectável. O desenho só se sustenta se, para cada ensaio, existir um deslocamento em que
**as duas** condições do operador congelado valham para os **dois** valores:

  1. o novo denominador está ausente do texto original;
  2. o percentual recomputado está ausente do texto original.

A segunda condição não é decorativa. A lente de desperturbação desfaz o deslocamento trocando
perturbado por original **na ficha do modelo**, e uma colisão já reprovou quatro transcrições corretas
no Estudo 9 (o par 31->28 aplicado dentro de "1283.2"). Se o percentual recomputado já existir no
artigo, a lente o converte em outra coisa e o erro aparece como se fosse do modelo.

Este script varre os deslocamentos admissíveis pelo operador congelado (5 a 15%, mesmas casas) e diz,
por ensaio, se existe algum par que passa nas duas. Não perturba nada: só prova que daria.
"""
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("pert", RAIZ / "scripts" / "estudo1" / "perturbar.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
PRIM = RAIZ / "dados" / "estudo11" / "primarios"

# (ensaio, arquivo, [(braço, eventos, denominador, percentual como a fonte imprime ou None)])
ALVOS = [
    ("Luis-Silva, 2024", "PMC11514138.xml",
     [("azul", 9, 19, "47"), ("controle", 14, 23, "61")]),
    ("Shaker, 2025", "PMC11707904.xml",
     [("placebo", 14, 30, "46.7"), ("1 mg/kg", 9, 30, "30.0"), ("4 mg/kg", 6, 30, "20.0")]),
    ("Ibarra-Estrada, 2023", "PMC10010212.xml",
     [("azul", 15, 45, "33"), ("controle", 21, 46, "46")]),
    ("Aguilar, 2016", "aguilar-2016-medcrit.txt",
     [("azul", 6, 30, "20.0"), ("controle", 11, 30, "36.6")]),
    ("Kirov, 2001", "kirov2001.txt",
     [("azul", 5, 10, None), ("controle", 7, 10, None)]),
    ("Levin, 2004", "levin2004.txt",
     [("azul", 0, 28, None), ("controle", 6, 28, "21.4")]),
    ("Dong, 2025", "PMC12751372.xml",
     [("azul", 9, 36, "25.0"), ("controle", 15, 36, "41.7")]),
    # dois braços, sem percentual por braço: a fonte publica 26,6% como taxa GLOBAL dos dois grupos
    # ("The overall hospital mortality rate was similar in both groups (26.6%)"), e as contagens por
    # braço só existem na tabela de pacientes. A primeira versão desta lista modelava o ensaio como
    # um braço só com aquele percentual, o que divergia da régua -- apanhado por e12-testa-coerencia.
    ("Memis, 2002", "memis2002.txt",
     [("azul", 4, 15, None), ("controle", 4, 15, None)]),
]


def texto_de(arq):
    t = io.open(PRIM / arq, encoding="utf-8", errors="replace").read()
    if arq.endswith(".xml"):
        t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def ausente(txt, s):
    return not P.ocorrencias(txt, s)[0]


print(f"{'ensaio':22s} {'n original':>11s} {'n deslocado':>12s}  braços cobertos e o % recomputado de cada")
print("-" * 108)
registro = []
for ensaio, arq, bracos in ALVOS:
    txt = texto_de(arq)
    # os braços que COMPARTILHAM um denominador têm de receber o MESMO deslocamento: o operador
    # troca todas as ocorrências do número no texto, não uma ocorrência escolhida.
    grupos = {}
    for braco, a, n, pct in bracos:
        grupos.setdefault(n, []).append((braco, a, pct))
    for n, membros in grupos.items():
        achado, motivo = None, ""
        cands = sorted({int(round(n * (1 + s * f / 100))) for f in range(5, 16) for s in (1, -1)})
        for novo_n in cands:
            if novo_n == n or novo_n <= max(a for _, a, _ in membros) or novo_n <= 0:
                continue
            if not ausente(txt, str(novo_n)):
                motivo = motivo or "todo n' admissível já ocorre no texto"
                continue
            pcts, ok = {}, True
            for braco, a, pct in membros:
                if pct is None:
                    continue
                casas = len(pct.split(".")[1]) if "." in pct else 0
                np_ = f"{100 * a / novo_n:.{casas}f}"
                if np_ == pct or not ausente(txt, np_):
                    ok = False; motivo = "n' livre, mas um %' recomputado colide com o texto"; break
                pcts[braco] = np_
            if ok:
                achado = (novo_n, pcts); break
        if achado:
            nn, pcts = achado
            det = " · ".join(f"{b} {a}/{nn}" + (f" = {pcts[b]}%" if b in pcts else " (sem % na fonte)")
                             for b, a, _ in membros)
            print(f"{ensaio:22s} {n:11d} {nn:12d}  {det}")
        else:
            print(f"{ensaio:22s} {n:11d} {'NENHUM':>12s}  {motivo}")
        for braco, a, pct in membros:
            registro.append(dict(ensaio=ensaio, braco=braco, eventos=a, n=n, pct_fonte=pct,
                                 novo_n=achado[0] if achado else None,
                                 novo_pct=(achado[1].get(braco) if achado else None),
                                 viavel=bool(achado), motivo="" if achado else motivo))

print("-" * 108)
por_ensaio = {}
for r in registro:
    por_ensaio.setdefault(r["ensaio"], []).append(r["viavel"])
inteiros = [e for e, v in por_ensaio.items() if all(v)]
parciais = [e for e, v in por_ensaio.items() if any(v) and not all(v)]
nenhum = [e for e, v in por_ensaio.items() if not any(v)]
print(f"braços cobertos: {sum(r['viavel'] for r in registro)} de {len(registro)}")
print(f"ensaios com prova de leitura completa ({len(inteiros)}): {', '.join(inteiros) or '—'}")
print(f"ensaios com prova parcial ({len(parciais)}): {', '.join(parciais) or '—'}")
print(f"ensaios SEM prova de leitura ({len(nenhum)}): {', '.join(nenhum) or '—'}")
cob = len(inteiros) + 0.5 * len(parciais)
print(f"\ncobertura: {cob} de {len(por_ensaio)} ensaios")

io.open(RAIZ / "dados" / "estudo12" / "perturbacao-coerente-ancora3.json", "w", encoding="utf-8").write(
    json.dumps(dict(criterio="n' e %' recomputado ambos ausentes do texto original; deslocamento 5-15%",
                    cobertura_ensaios=cob, total_ensaios=len(por_ensaio),
                    completos=inteiros, parciais=parciais, sem_prova=nenhum,
                    bracos=registro), ensure_ascii=False, indent=2) + "\n")
print("gravado: dados/estudo12/perturbacao-coerente-ancora3.json")
