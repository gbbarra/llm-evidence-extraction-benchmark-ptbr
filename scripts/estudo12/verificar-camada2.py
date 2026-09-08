# -*- coding: utf-8 -*-
"""Confere a camada 1 da âncora 3, célula a célula, contra os oito artigos primários.

A camada 1 é o que a revisão publicou, recuperada da Figura 3 e verificada por aritmética
(`verificar-figura3.py`). A camada 2 é o que a fonte diz, com a frase transcrita. Este script não
recalcula nada: ele põe as duas lado a lado e diz onde discordam.

Cada linha carrega a citação verbatim que a sustenta, porque no gabarito deste projeto veredito sem
citação não vale. As citações foram lidas dos primários em 2026-09-08 e estão em
`dados/estudo11/primarios/`. Onde a fonte publica percentual e não contagem, o percentual é
reconvertido e a reconversão é conferida aqui, não aceita de palavra.

Resultado em 2026-09-08: seis dos oito conferem; dois não. E os dois erros são de naturezas
diferentes, o que importa para o que a errata diz.
"""
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PRIM = Path(__file__).resolve().parents[2] / "dados" / "estudo11" / "primarios"

# ------------------------------------------------------------------ camada 1, da Figura 3
CAMADA1 = {
    "Luis-Silva, 2024":      (9, 19, 14, 23),
    "Shaker, 2025":         (15, 30, 14, 30),
    "Ibarra-Estrada, 2023": (15, 45, 21, 46),
    "Aguilar, 2016":        (24, 30, 19, 30),
    "Kirov, 2001":           (5, 10,  7, 10),
    "Levin, 2004":           (0, 28,  6, 28),
    "Dong, 2025":            (9, 36, 15, 36),
    "Memis, 2002":           (4, 15,  4, 15),
}

# ------------------------------------------------------------------ camada 2, dos primários
# (celulas na fonte, arquivo, trecho que tem de existir literalmente no arquivo, como se leu)
CAMADA2 = {
    "Luis-Silva, 2024": (
        (9, 19, 14, 23), "PMC11514138.xml",
        "mortality rate in 30 days of 47% versus 61% in the Control group",
        "a fonte publica percentual: 9/19 = 47,4% e 14/23 = 60,9%, com os N do proprio artigo",
    ),
    "Shaker, 2025": (
        None, "PMC11707904.xml",
        "Mortality rate",
        "tres bracos: A placebo 14/30, B azul 1 mg/kg 9/30, C azul 4 mg/kg 6/30. Nao existe braco 15/30.",
    ),
    "Ibarra-Estrada, 2023": (
        (15, 45, 21, 46), "PMC10010212.xml",
        "15/45",
        "a tabela publica as contagens diretamente",
    ),
    "Aguilar, 2016": (
        (6, 30, 11, 30), "aguilar-2016-medcrit.txt",
        "la mortalidad al egreso fue de 20.0%",
        "a fonte publica percentual na alta e aos 21 dias: 20,0% de 30 = 6 e 36,6% de 30 = 11",
    ),
    "Kirov, 2001": (
        (5, 10, 7, 10), "kirov2001.txt",
        "Survivors at day 28",
        "a Tabela 5 publica SOBREVIVENTES em 28 dias, 5 e 3; os mortos sao 10-5 e 10-3",
    ),
    "Levin, 2004": (
        (0, 28, 6, 28), "levin2004.txt",
        "There were no deaths in those treated with MB",
        "a fonte publica as contagens: zero e seis",
    ),
    "Dong, 2025": (
        (9, 36, 15, 36), "PMC12751372.xml",
        "Mortality at 28 days",
        "a tabela publica contagem e percentual",
    ),
    "Memis, 2002": (
        (4, 15, 4, 15), "memis2002.txt",
        "The overall hospital mortality rate was similar in both groups",
        "a Tabela 1 lista o desfecho paciente a paciente; os mortos sao contados aqui",
    ),
}

ok = True


def existe(arquivo, trecho):
    """A citacao tem de estar literalmente no arquivo. Sem isso a linha nao vale."""
    p = PRIM / arquivo
    if not p.exists():
        return None
    t = re.sub(r"\s+", " ", io.open(p, encoding="utf-8", errors="replace").read())
    return re.sub(r"\s+", " ", trecho) in t


# ------------------------------------------------------------------ conferências derivadas
print("1. reconversões e contagens, refeitas aqui e não aceitas de palavra\n")

# Aguilar: percentual -> contagem
for rot, pct, n, esp in (("Aguilar azul", 20.0, 30, 6), ("Aguilar controle", 36.6, 30, 11)):
    obt = pct / 100 * n
    bate = abs(obt - esp) < 0.2
    ok = ok and bate
    print(f"  {'ok  ' if bate else 'ERRO'} {rot:20s} {pct}% de {n} = {obt:.1f}  ->  {esp}")

# Luis-Silva: contagem -> percentual
for rot, ev, n, pct in (("Luis-Silva azul", 9, 19, 47), ("Luis-Silva controle", 14, 23, 61)):
    obt = 100 * ev / n
    bate = abs(obt - pct) < 1.0
    ok = ok and bate
    print(f"  {'ok  ' if bate else 'ERRO'} {rot:20s} {ev}/{n} = {obt:.1f}%  ->  publicado {pct}%")

# Kirov: sobreviventes -> mortos
for rot, sobrev, n, esp in (("Kirov azul", 5, 10, 5), ("Kirov controle", 3, 10, 7)):
    obt = n - sobrev
    bate = obt == esp
    ok = ok and bate
    print(f"  {'ok  ' if bate else 'ERRO'} {rot:20s} {n} - {sobrev} sobreviventes = {obt} mortos")

# Memis: contagem dos "Died" na tabela de pacientes
p = PRIM / "memis2002.txt"
if p.exists():
    t = re.sub(r"\s+", " ", io.open(p, encoding="utf-8", errors="replace").read())
    i, j = t.find("MB group 1 56 M"), t.find("Control group 1 58 M")
    k = t.find("MB=Methylene blue", j)
    mb, ct = t[i:j].count("Died"), t[j:k].count("Died")
    bate = (mb, ct) == (4, 4)
    ok = ok and bate
    print(f"  {'ok  ' if bate else 'ERRO'} {'Memis, contados':20s} azul {mb} mortos, controle {ct} mortos, na Tabela 1")
    print(f"       {100*mb/15:.1f}% e {100*ct/15:.1f}%, contra os 26,6% que o texto publica para ambos")

# ------------------------------------------------------------------ as duas camadas lado a lado
print("\n2. camada 1 (o que a revisão publicou) contra camada 2 (o que a fonte diz)\n")
print(f"  {'ensaio':22s} {'camada 1':>16s} {'camada 2':>16s}   citação confere?")
print("  " + "-" * 76)
divergem = []
for nome, c1 in CAMADA1.items():
    c2, arq, cit, _ = CAMADA2[nome]
    achou = existe(arq, cit)
    s1 = f"{c1[0]}/{c1[1]} · {c1[2]}/{c1[3]}"
    s2 = f"{c2[0]}/{c2[1]} · {c2[2]}/{c2[3]}" if c2 else "não existe tal braço"
    bate = c2 is not None and c1 == c2
    if not bate:
        divergem.append(nome)
    marca = "ok " if bate else "DIVERGE"
    cm = "sim" if achou else ("ARQUIVO AUSENTE" if achou is None else "NÃO ACHOU A FRASE")
    if achou is not True:
        ok = False
    print(f"  {marca:8s} {nome:22s} {s1:>16s} {s2:>16s}   {cm}")

# ------------------------------------------------------------------ leitura
print("\n3. as duas divergências, e elas não são do mesmo tipo\n")
print("  Shaker 2025  — DENOMINADOR. A revisão somou os eventos dos dois braços de azul (9 + 6 = 15)")
print("                 e manteve o denominador de um braço só. Deveria ser 15/60.")
print("  Aguilar 2016 — INVERSÃO. A revisão pôs os SOBREVIVENTES na coluna de eventos:")
print("                 30 − 6 = 24 e 30 − 11 = 19. Não é arredondamento nem escolha de braço.")
print("\n  O contraste que fecha o argumento: no Kirov a fonte também publica sobreviventes,")
print("  e ali a revisão converteu certo (5 e 3 sobreviventes viraram 5 e 7 mortos). O mesmo")
print("  time fez a conversão certa num ensaio e a errada no outro.")

print("\n" + "=" * 80)
print(f"{'CAMADA 2 FECHADA' if ok else 'INCOMPLETA'}: 8 de 8 ensaios com fonte e citação; "
      f"{8 - len(divergem)} conferem, {len(divergem)} divergem ({', '.join(divergem)}).")
print("=" * 80)
sys.exit(0 if ok else 1)
