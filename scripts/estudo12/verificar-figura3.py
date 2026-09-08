# -*- coding: utf-8 -*-
"""Verifica, por aritmética, a leitura da Figura 3 da âncora 3 (azul de metileno em choque).

O problema. A camada 1 do gabarito é "o que a revisão publicou". Nas âncoras 1 e 2 isso estava em
tabelas de texto. Nesta, o único lugar onde os dados por ensaio aparecem é a Figura 3, que é um
raster. Ler um raster é ler por visão, e uma leitura por visão não carrega citação: não há frase
para transcrever. Pela regra do projeto, veredito sem citação não entra em gabarito.

A saída. Uma leitura de imagem não pode ser aceita por confiança, mas pode ser aceita por
reconstrução. Se as células lidas forem as verdadeiras, então elas têm de prever, por um caminho
que não é o da leitura, tudo o mais que está impresso na mesma figura e fora dela:

  1. os denominadores por braço, que estão na Tabela 1 -- texto XML de verdade, não imagem;
  2. as oito razões de chances por ensaio e seus dezesseis limites de intervalo;
  3. a heterogeneidade: qui quadrado, graus de liberdade, I quadrado;
  4. os oito pesos do modelo aleatório;
  5. o diamante agrupado e seu intervalo.

São 51 valores impressos previstos a partir de 16 células lidas. Uma leitura errada em qualquer
célula quebra a previsão da linha correspondente e, pelos pesos, também a do diamante. É este
script, e não a minha vista, que autoriza o uso dos números.

Nota de método. O diamante NÃO fecha pelo DerSimonian-Laird do motor congelado (0,737 [0,45; 1,21],
tau quadrado 0,1065). Fecha pelo estimador de Paule-Mandel com o ajuste de Hartung-Knapp: tau
quadrado 0,1334, pesos idênticos aos impressos nas oito linhas, intervalo [0,40; 1,36]. Isso não é
defeito da leitura nem do motor: é a revisão tendo usado outro estimador, o que é a configuração
padrão do pacote `meta` do R nas versões recentes. Fica registrado porque muda o que se cobra dos
modelos: a camada 1 desta âncora tem de ser agrupada por Paule-Mandel e Hartung-Knapp para ser
comparada com o publicado, enquanto o motor do banco continua a rodar DerSimonian-Laird.

Leitura feita em 2026-09-08 sobre jcm-15-04481-g003.jpg, extraído do pacote suplementar do
Europe PMC (PMC13302755).
"""
import importlib.util
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("e12or", AQUI / "e12-or.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# ------------------------------------------------------------------ lido da Figura 3
# (estudo, eventos MB, total MB, eventos ST, total ST, OR impresso, IC impresso, peso impresso)
FIG3 = [
    ("Luis-Silva, 2024",       9, 19, 14, 23, 0.58, (0.17, 1.98), 12.9),
    ("Shaker, 2025",          15, 30, 14, 30, 1.14, (0.41, 3.15), 16.9),
    ("Ibarra-Estrada, 2023",  15, 45, 21, 46, 0.60, (0.25, 1.39), 21.1),
    ("Aguilar, 2016",         24, 30, 19, 30, 2.32, (0.72, 7.41), 14.0),
    ("Kirov, 2001",            5, 10,  7, 10, 0.43, (0.07, 2.68),  6.7),
    ("Levin, 2004",            0, 28,  6, 28, 0.06, (0.00, 1.14),  2.9),
    ("Dong, 2025",             9, 36, 15, 36, 0.47, (0.17, 1.27), 17.1),
    ("Memis, 2002",            4, 15,  4, 15, 1.00, (0.20, 5.04),  8.3),
]
DIAMANTE, IC_DIAM = 0.73, (0.40, 1.36)
TAU2, CHI2, GL, I2 = 0.1334, 8.89, 7, 21.3
TOT_MB, TOT_ST = 213, 218
T_STUDENT_7 = 2.364624   # t bicaudal 95%, 7 graus de liberdade

# denominadores por braço, da Tabela 1 (texto XML, não imagem)
TAB1 = {"Kirov, 2001": (10, 10), "Memis, 2002": (15, 15), "Aguilar, 2016": (30, 30),
        "Ibarra-Estrada, 2023": (45, 46), "Luis-Silva, 2024": (19, 23), "Dong, 2025": (36, 36),
        "Levin, 2004": (28, 28)}
# Shaker tem três braços na Tabela 1 (30 baixa / 30 alta / 30 controle); a figura usa 30 e 30

ok = True
conferidos = 0


def linha(rotulo, obtido, esperado, tol):
    global ok, conferidos
    bate = abs(obtido - esperado) <= tol
    ok = ok and bate
    conferidos += 1
    print(f"  {'ok  ' if bate else 'ERRO'} {rotulo:36s} calculado {obtido:>9.4f}   impresso {esperado:>9.4f}")


def igual(rotulo, obtido, esperado):
    global ok, conferidos
    bate = obtido == esperado
    ok = ok and bate
    conferidos += 1
    print(f"  {'ok  ' if bate else 'ERRO'} {rotulo:36s} calculado {str(obtido):>9s}   impresso {str(esperado):>9s}")


# ------------------------------------------------------------------ 1. denominadores
print("1. denominadores lidos da figura contra a Tabela 1 (texto XML, caminho independente)")
for nome, ev1, n1, ev2, n2, *_ in FIG3:
    if nome in TAB1:
        igual(nome, (n1, n2), TAB1[nome])
    else:
        print(f"       {nome:36s} três braços na Tabela 1; a figura usa {n1} e {n2}")
    if ev1 > n1 or ev2 > n2:
        print(f"  ERRO {nome}: eventos maiores que o total"); ok = False
igual("soma dos totais MB", sum(x[2] for x in FIG3), TOT_MB)
igual("soma dos totais ST", sum(x[4] for x in FIG3), TOT_ST)

# ------------------------------------------------------------------ 2. cada ensaio
print("\n2. razão de chances por ensaio, recalculada pelo motor do banco")
for nome, ev1, n1, ev2, n2, orp, (li, ls), _ in FIG3:
    a, b = m.ci95_or(ev1, n1, ev2, n2)
    linha(f"{nome} OR", m.odds_ratio(ev1, n1, ev2, n2), orp, 0.005 + 0.005 * orp)
    linha(f"{nome} IC inferior", a, li, 0.005 + 0.01 * max(li, 0.01))
    linha(f"{nome} IC superior", b, ls, 0.005 + 0.01 * ls)

# ------------------------------------------------------------------ 3. heterogeneidade
estudos = [(x[1], x[2], x[3], x[4]) for x in FIG3]
ys, vs = [], []
for ev1, n1, ev2, n2 in estudos:
    a, b, c, d, _ = m._cells(float(ev1), float(n1), float(ev2), float(n2))
    ys.append(math.log((a * d) / (b * c)))
    vs.append(1 / a + 1 / b + 1 / c + 1 / d)
gl = len(ys) - 1


def media(t2):
    w = [1 / (v + t2) for v in vs]
    return sum(x * y for x, y in zip(w, ys)) / sum(w), w


def Q(t2):
    yb, w = media(t2)
    return sum(x * (y - yb) ** 2 for x, y in zip(w, ys))


print("\n3. heterogeneidade")
linha("qui quadrado", Q(0.0), CHI2, 0.06)
igual("graus de liberdade", gl, GL)
linha("I quadrado (%)", 100 * (Q(0.0) - gl) / Q(0.0), I2, 0.15)

# Paule-Mandel: o tau quadrado que faz Q(tau2) valer os graus de liberdade
lo, hi = 0.0, 5.0
for _ in range(200):
    meio = (lo + hi) / 2
    lo, hi = (meio, hi) if Q(meio) > gl else (lo, meio)
pm = (lo + hi) / 2
linha("tau quadrado (Paule-Mandel)", pm, TAU2, 0.0005)

# ------------------------------------------------------------------ 4. pesos
print("\n4. pesos do modelo aleatório (%)")
yb, w = media(pm)
sw = sum(w)
for (nome, *_, peso), wi in zip(FIG3, w):
    linha(f"{nome} peso", 100 * wi / sw, peso, 0.05)

# ------------------------------------------------------------------ 5. diamante
print("\n5. diamante agrupado (Paule-Mandel com Hartung-Knapp)")
se_hk = math.sqrt(Q(pm) / (gl * sw))
linha("OR agrupado", math.exp(yb), DIAMANTE, 0.006)
linha("IC inferior", math.exp(yb - T_STUDENT_7 * se_hk), IC_DIAM[0], 0.005)
linha("IC superior", math.exp(yb + T_STUDENT_7 * se_hk), IC_DIAM[1], 0.005)

dl = m.pool_or_dl(estudos)
print(f"\n   para contraste, o motor do banco (DerSimonian-Laird, normal): "
      f"OR {dl['or']} [{dl['ic95'][0]}; {dl['ic95'][1]}], tau quadrado {dl['tau2']}, I quadrado {dl['i2']}%")

print("\n" + "=" * 78)
print(f"{'VERIFICADA' if ok else 'REPROVADA'}: {conferidos} valores impressos previstos a partir de 16 células lidas."
      if ok else f"REPROVADA: a leitura não fecha em {conferidos} conferências. Não usar.")
print("=" * 78)
sys.exit(0 if ok else 1)
