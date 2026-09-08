# -*- coding: utf-8 -*-
"""Os cinco cenários de correção da âncora 3, calculados por script e não à mão.

A revisão adversarial do protocolo apontou duas coisas, ambas certas:

1. Os pools de `ancora3-camada1.json` foram digitados a partir de uma sessão interativa; nenhum script
   commitado os produzia. Um número que entra num registro pré-registrado tem de ter artefato.
2. O cenário "Shaker corrigido, Aguilar excluído" trazia 0,49 [0,33; **0,73**]. Está errado: excluir o
   Aguilar deixa **sete** estudos, logo seis graus de liberdade, logo t de Student 2,4469 e não os
   2,3646 de sete graus. O limite superior correto é **0,74**. Os outros quatro cenários têm oito
   estudos e estavam certos.

Duas rotas, porque a §9 do protocolo declara duas e elas medem coisas diferentes:

  DL          DerSimonian-Laird com quantil normal -- o motor do banco, aplicado às células de um
              modelo. Mede o modelo.
  PM+HK       Paule-Mandel com o ajuste de Hartung-Knapp e t de Student com k-1 graus -- o caminho da
              própria revisão, verificado em `verificar-figura3.py`. Só o conferidor usa. Mede a
              revisão.
"""
import importlib.util
import io
import json
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("e12or", RAIZ / "scripts" / "estudo12" / "e12-or.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# t de Student, bicaudal 95%, por graus de liberdade
T95 = {5: 2.570582, 6: 2.446912, 7: 2.364624, 8: 2.306004}

LS, SH, IB, AG, KI, LE, DO, ME = ((9, 19, 14, 23), (15, 30, 14, 30), (15, 45, 21, 46),
                                  (24, 30, 19, 30), (5, 10, 7, 10), (0, 28, 6, 28),
                                  (9, 36, 15, 36), (4, 15, 4, 15))
SHc, AGc = (15, 60, 14, 30), (6, 30, 11, 30)

CENARIOS = [
    ("como a revisao publicou", [LS, SH, IB, AG, KI, LE, DO, ME]),
    ("so o Shaker corrigido (15/60)", [LS, SHc, IB, AG, KI, LE, DO, ME]),
    ("so o Aguilar corrigido (6/30 contra 11/30)", [LS, SH, IB, AGc, KI, LE, DO, ME]),
    ("os dois corrigidos", [LS, SHc, IB, AGc, KI, LE, DO, ME]),
    ("Shaker corrigido, Aguilar excluido", [LS, SHc, IB, KI, LE, DO, ME]),
]


def pools(est):
    ys, vs = [], []
    for e in est:
        a, b, c, d, _ = m._cells(*map(float, e))
        ys.append(math.log((a * d) / (b * c)))
        vs.append(1 / a + 1 / b + 1 / c + 1 / d)
    gl = len(ys) - 1

    def med(t2):
        w = [1 / (v + t2) for v in vs]
        return sum(x * y for x, y in zip(w, ys)) / sum(w), w

    def Q(t2):
        yb, w = med(t2)
        return sum(x * (y - yb) ** 2 for x, y in zip(w, ys))

    lo, hi = 0.0, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if Q(mid) > gl else (lo, mid)
    pm = (lo + hi) / 2
    yb, w = med(pm)
    sw = sum(w)
    se_hk = math.sqrt(Q(pm) / (gl * sw))
    t = T95[gl]
    i2 = max(0.0, (Q(0.0) - gl) / Q(0.0)) * 100 if Q(0.0) > 0 else 0.0
    return dict(
        k=len(est), gl=gl, t_student=t,
        pm_hk=dict(**{"or": round(math.exp(yb), 3)},
                   ic95=[round(math.exp(yb - t * se_hk), 3), round(math.exp(yb + t * se_hk), 3)],
                   tau2=round(pm, 4), i2=round(i2, 1)),
        dl=m.pool_or_dl(est))


print(f"{'cenário':44s} {'k':>2s} {'gl':>3s} {'t':>7s}   {'PM+HK':>22s}   {'DL':>22s}")
print("-" * 118)
saida = []
for rot, est in CENARIOS:
    r = pools(est)
    p, d = r["pm_hk"], r["dl"]
    sig = "  significativo" if p["ic95"][1] < 1 else ""
    print(f"{rot:44s} {r['k']:2d} {r['gl']:3d} {r['t_student']:7.4f}   "
          f"{p['or']:.3f} [{p['ic95'][0]:.3f}; {p['ic95'][1]:.3f}]   "
          f"{d['or']:.3f} [{d['ic95'][0]:.3f}; {d['ic95'][1]:.3f}]{sig}")
    saida.append(dict(rotulo=rot, **r))

print("""
A conclusão publicada -- de que não há benefício de mortalidade -- não sobrevive à correção por
nenhuma das duas rotas nem por nenhum dos caminhos de tratamento do Aguilar.""")

# grava dentro do gabarito, substituindo os valores digitados à mão
P = RAIZ / "dados" / "estudo12" / "ancora3-camada1.json"
j = json.loads(io.open(P, encoding="utf-8").read())
j["cenarios_de_correcao"] = {
    "produzido_por": "scripts/estudo12/cenarios-ancora3.py",
    "nota": ("PM+HK e a rota da propria revisao (Paule-Mandel, Hartung-Knapp, t de Student com k-1 "
             "graus) e so o conferidor a usa; DL e o motor do banco, aplicado a celula de modelo. "
             "Corrigido em 2026-09-08: o cenario sem o Aguilar tem 7 estudos e 6 graus de liberdade, "
             "e estava usando t de 7 graus -- o limite superior era 0,73 e o correto e 0,74."),
    "cenarios": saida,
    "leitura": ("a conclusao publicada nao sobrevive a correcao por nenhuma rota nem por nenhum "
                "tratamento do Aguilar. Isto e resultado da campanha e vai declarado como tal."),
}
io.open(P, "w", encoding="utf-8").write(json.dumps(j, ensure_ascii=False, indent=2) + "\n")
print("gravado em dados/estudo12/ancora3-camada1.json")
