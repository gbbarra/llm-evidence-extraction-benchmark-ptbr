# -*- coding: utf-8 -*-
"""As sete cópias das células da âncora 3 concordam entre si? Nenhum modelo é chamado.

As dezesseis células desta âncora foram escritas sete vezes, em momentos diferentes e por caminhos
diferentes: lidas da Figura 3, conferidas contra os primários, digitadas nos cenários de correção,
listadas para medir a perturbação, listadas de novo para provar o deslocamento coerente, gravadas no
registro de investigação e gravadas na régua.

A revisão adversarial chamou isso de duplicação, e a leitura mais natural seria deduplicar. Este
arquivo faz o contrário, de propósito: **a duplicação é o ativo, e o que faltava era compará-la.**
Cada cópia foi derivada por um caminho independente — uma leitura de imagem verificada por
reconstrução aritmética, uma conferência linha a linha contra oito primários, uma redução multi-braço
aplicada a mão. Que sete caminhos independentes cheguem ao mesmo lugar é evidência; colapsá-los numa
fonte única trocaria essa evidência por conveniência, e um erro na fonte única não teria mais quem o
contradissesse.

O que este teste proíbe é a divergência silenciosa. A régua (`gabarito-a3.json`) é a autoridade; toda
outra cópia é conferida contra ela, e uma discordância reprova.
"""
import importlib.util
import io
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent
D12 = RAIZ / "dados" / "estudo12"


def _carrega(nome, caminho):
    """Carrega o módulo pelas suas TABELAS, engolindo o relatório que ele imprime.

    Cada um destes scripts é executável e conta a própria história ao rodar. Aqui só interessam as
    listas que eles carregam, então a saída deles vai para o vazio -- e o SystemExit com que alguns
    terminam é tratado como fim normal.
    """
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    class _Mudo(io.StringIO):
        # os scripts chamam sys.stdout.reconfigure() no topo; um StringIO cru não o tem
        def reconfigure(self, **kw):
            return None

    old_out, old_argv = sys.stdout, sys.argv
    sys.stdout = _Mudo()
    sys.argv = [str(caminho)]
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    finally:
        sys.stdout, sys.argv = old_out, old_argv
    return m


ok, falhas = True, []


def diz(rot, passou, det=""):
    global ok
    ok = ok and passou
    if not passou:
        falhas.append(rot)
    print(f"  {'ok  ' if passou else 'FALHA'} {rot:56s} {det}")


# ══════════════════════════════════════════════ a autoridade
GAB = json.loads(io.open(D12 / "gabarito-a3.json", encoding="utf-8").read())
NOME = {t: f["ensaio"] for t, f in GAB["bracos_da_fonte"].items()}
POR_NOME = {f["ensaio"]: t for t, f in GAB["bracos_da_fonte"].items()}

camada2 = {t: tuple(int(float(GAB["celulas"][t][c]["valor_fonte"]))
                    for c in ("eventos_mb", "n_mb", "eventos_ct", "n_ct")) for t in GAB["celulas"]}
camada1 = {t: tuple(int(float(GAB["celulas"][t][c]["ma"]))
                    for c in ("eventos_mb", "n_mb", "eventos_ct", "n_ct")) for t in GAB["celulas"]}
bracos = {t: {(b["braco"], b["eventos"], b["n"], b["pct"]) for b in f["bracos"]}
          for t, f in GAB["bracos_da_fonte"].items()}

print(f"autoridade: gabarito-a3.json — {len(camada2)} ensaios, 32 células\n")

# ══════════════════════════════════════════════ 1. o registro de investigação
print("1. ancora3-camada1.json — o registro de como a camada 1 foi recuperada")
reg = json.loads(io.open(D12 / "ancora3-camada1.json", encoding="utf-8").read())
c1_reg = {POR_NOME[e["estudo"]]: (e["eventos_mb"], e["n_mb"], e["eventos_st"], e["n_st"])
          for e in reg["estudos"]}
diz("camada 1 idêntica à da régua", c1_reg == camada1,
    str({t: (c1_reg[t], camada1[t]) for t in camada1 if c1_reg.get(t) != camada1[t]}))

# ══════════════════════════════════════════════ 2. a leitura da Figura 3
print("\n2. verificar-figura3.py — a leitura da imagem, verificada por reconstrução")
F3 = _carrega("f3", AQUI / "verificar-figura3.py")
c1_fig = {POR_NOME[x[0]]: (x[1], x[2], x[3], x[4]) for x in F3.FIG3}
diz("camada 1 idêntica à da régua", c1_fig == camada1,
    str({t: (c1_fig.get(t), camada1[t]) for t in camada1 if c1_fig.get(t) != camada1[t]}))
diz("o diamante publicado é o mesmo", (F3.DIAMANTE, tuple(F3.IC_DIAM)) == (0.73, (0.40, 1.36)))

# ══════════════════════════════════════════════ 3. a conferência contra as fontes
print("\n3. verificar-camada2.py — a conferência linha a linha contra os oito primários")
C2 = _carrega("c2", AQUI / "verificar-camada2.py")
c1_v = {POR_NOME[k]: v for k, v in C2.CAMADA1.items()}
diz("camada 1 idêntica à da régua", c1_v == camada1,
    str({t: (c1_v.get(t), camada1[t]) for t in camada1 if c1_v.get(t) != camada1[t]}))
c2_v = {POR_NOME[k]: v[0] for k, v in C2.CAMADA2.items() if v[0]}
divs = {t: (c2_v[t], camada2[t]) for t in c2_v if c2_v[t] != camada2[t]}
diz("camada 2 idêntica à da régua onde ela a declara", not divs, str(divs))
diz("e o Shaker é o único sem par direto (é o que a redução resolve)",
    [k for k, v in C2.CAMADA2.items() if v[0] is None] == ["Shaker, 2025"])

# ══════════════════════════════════════════════ 4. os cenários de correção
print("\n4. cenarios-ancora3.py — os cinco cenários publicados na errata")
CE = _carrega("ce", AQUI / "cenarios-ancora3.py")
pub = {POR_NOME[n]: t for n, t in zip(
    ["Luis-Silva, 2024", "Shaker, 2025", "Ibarra-Estrada, 2023", "Aguilar, 2016",
     "Kirov, 2001", "Levin, 2004", "Dong, 2025", "Memis, 2002"],
    [CE.LS, CE.SH, CE.IB, CE.AG, CE.KI, CE.LE, CE.DO, CE.ME])}
diz("as células publicadas são a camada 1 da régua", pub == camada1,
    str({t: (pub[t], camada1[t]) for t in camada1 if pub[t] != camada1[t]}))
diz("a correção do Shaker é a da régua", CE.SHc == camada2["shaker2025"][:2] + camada1["shaker2025"][2:],
    f"{CE.SHc} contra {camada2['shaker2025']}")
diz("a correção do Aguilar é a da régua", CE.AGc == camada2["aguilar2016"], str(CE.AGc))

# ══════════════════════════════════════════════ 5 e 6. as duas listas de braços
print("\n5. medir-perturbabilidade.py e provar-perturbacao-coerente.py — os braços da fonte")
MP = _carrega("mp", AQUI / "medir-perturbabilidade.py")
den_mp = {POR_NOME[e]: {(v, ) for r, v, papel in linhas if papel == "denominador"}
          for e, linhas in MP.COMO_A_FONTE_IMPRIME.items()}
den_gab = {t: {(str(b["n"]), ) for b in f["bracos"]} for t, f in GAB["bracos_da_fonte"].items()}
diz("os denominadores medidos são os da régua", den_mp == den_gab,
    str({t: (den_mp.get(t), den_gab[t]) for t in den_gab if den_mp.get(t) != den_gab[t]}))

PC = _carrega("pc", AQUI / "provar-perturbacao-coerente.py")
br_pc = {POR_NOME[e]: {(b, ev, n, pct) for b, ev, n, pct in bracos_}
         for e, arq, bracos_ in PC.ALVOS}
br_gab = {t: {(b["papel"] if t != "shaker2025" else b["braco"], b["eventos"], b["n"], b["pct"])
              for b in f["bracos"]} for t, f in GAB["bracos_da_fonte"].items()}
# compara só os números, porque os rótulos dessas listas são descritivos e não normativos
num_pc = {t: sorted((ev, n, pct) for _, ev, n, pct in v) for t, v in br_pc.items()}
num_gab = {t: sorted((b["eventos"], b["n"], b["pct"]) for b in GAB["bracos_da_fonte"][t]["bracos"])
           for t in GAB["bracos_da_fonte"]}
diz("os braços da prova de viabilidade são os da régua", num_pc == num_gab,
    str({t: (num_pc.get(t), num_gab[t]) for t in num_gab if num_pc.get(t) != num_gab[t]}))

# ══════════════════════════════════════════════ 7. o selo, contra os braços
print("\n6. o selo — todo denominador selado é um denominador de braço da régua")
SELO = json.loads(io.open(D12 / "perturbacoes-a3.json", encoding="utf-8").read())
soltos = []
for t, regs in SELO.items():
    ns = {b["n"] for b in GAB["bracos_da_fonte"][t]["bracos"]}
    tot = sum(b["n"] for b in GAB["bracos_da_fonte"][t]["bracos"])
    for r in regs:
        if r["papel"] == "denominador" and int(r["original"]) not in ns:
            soltos.append(f"{t}: {r['original']}")
        if r["papel"] == "total" and int(r["original"]) != tot:
            soltos.append(f"{t}: total {r['original']} != {tot}")
diz("nenhum valor selado é estranho à régua", not soltos, str(soltos[:3]))

# ══════════════════════════════════════════════ a aritmética, dos dois lados
print("\n7. e a aritmética fecha nas duas camadas")
tot_ma = (sum(camada1[t][0] + camada1[t][2] for t in camada1),
          sum(camada1[t][1] for t in camada1), sum(camada1[t][3] for t in camada1))
diz("os totais por braço da camada 1 são os 213 e 218 da Figura 3",
    (tot_ma[1], tot_ma[2]) == (213, 218), f"{tot_ma[1]} e {tot_ma[2]}")
diz("na camada 2 o Shaker leva o denominador a 60", camada2["shaker2025"][1] == 60,
    str(camada2["shaker2025"]))
diz("e o Aguilar leva os eventos a 6 e 11",
    (camada2["aguilar2016"][0], camada2["aguilar2016"][2]) == (6, 11), str(camada2["aguilar2016"]))

print("\n" + "=" * 80)
if ok:
    print("AS SETE CÓPIAS CONCORDAM. A duplicação é evidência, e agora é evidência conferida.")
else:
    print(f"{len(falhas)} DIVERGÊNCIA(S) ENTRE AS CÓPIAS:")
    for f_ in falhas:
        print("  -", f_)
print("=" * 80)
sys.exit(0 if ok else 1)
