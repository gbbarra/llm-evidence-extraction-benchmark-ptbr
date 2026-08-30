# -*- coding: utf-8 -*-
"""EXTRAI Study 4 round 2 — the arithmetic, shown: formulas, verbatim code,
one hand-worked example, and per-model accounts (route + sextet + result).

Self-gating: the generator recomputes every per-study MD/CI and every pool
from the recorded sextets with the same functions and refuses to write if
anything differs from the recorded results.

Run: python scripts/estudo4/contas-md.py
Output: dados/estudo4/rodada2/contas-comparadas.md
"""
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
R2 = ROOT / "dados" / "estudo4" / "rodada2"
MODELOS = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14"]


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


h3 = carrega("h3", "scripts/estudo3/e3-harness.py")
dg = carrega("dg", "scripts/estudo3/dirigida.py")


def fonte(arquivo, nomes):
    txt = (ROOT / arquivo).read_text(encoding="utf-8")
    blocos = []
    for n in nomes:
        m = re.search(rf"^def {n}\(.*?(?=^def |\Z)", txt, re.M | re.S)
        if m:
            blocos.append(m.group(0).rstrip())
    return "\n\n\n".join(blocos)


def ficha_rep(modelo, tid):
    for rep in (1, 2):
        f = R2 / "saidas" / modelo / "extracao" / f"{tid}-r{rep}.json"
        if f.exists():
            js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            if js:
                return js
    return None


def rota_braco(b, julg_valor):
    """Mirror of dirigida.braco_deterministico, returning (trio, route text)."""
    n = dg.num(b.get("n_analisado"))
    rota_n = "n_analisado"
    if n is None:
        n = dg.num(b.get("n_randomizado"))
        rota_n = "n_randomizado"
    m = dg.num(b.get("hba1c_mudanca_media"))
    tipo = str(b.get("hba1c_mudanca_tipo_dispersao", "")).upper()
    dp = dg.num(b.get("hba1c_mudanca_dispersao"))
    rota_m, rota_dp = "mudança lida da ficha", "DP direto da ficha"
    if m is None:
        b0, b1 = dg.num(b.get("hba1c_basal_media")), dg.num(b.get("hba1c_final_media"))
        if b0 is not None and b1 is not None:
            m = round(b1 - b0, 2)
            rota_m = f"derivada: final−basal = {b1}−{b0}"
            d0, d1 = dg.num(b.get("hba1c_basal_dp")), dg.num(b.get("hba1c_final_dp"))
            if d0 is not None and d1 is not None:
                dp = h3.dp_mudanca_r05(d0, d1)
                rota_dp = f"r=0,5 sobre DPs {d0}/{d1}"
                tipo = "DP"
    if tipo.startswith("IC"):
        bb = dg.bounds_ic(b)
        if bb and n:
            dp = h3.dp_de_ic(bb[0], bb[1], n)
            rota_dp = f"IC {bb} → DP (n={int(n)})"
    elif tipo in ("EP", "SE") and dp is not None and n:
        dp = h3.dp_de_se(dp, n)
        rota_dp = f"EP {dg.num(b.get('hba1c_mudanca_dispersao'))} → DP (×√{int(n)})"
    if julg_valor is not None:
        m = julg_valor
        rota_m += f" · GATILHO respondeu {julg_valor}"
    return (m, dp, n), f"{rota_m}; {rota_dp}; {rota_n}"


L = ["# Estudo 4 · rodada 2 — as contas e os códigos",
     "",
     "As fichas (documento-irmão `fichas-comparadas.md`) são a parte dos MODELOS. "
     "Tudo daqui para baixo é a parte do CÓDIGO: nenhum modelo — e nenhum humano — "
     "digita um número. Este documento mostra as fórmulas, o código exato que roda, "
     "um exemplo feito à mão, e, para cada modelo, a rota que levou cada ficha ao "
     "resultado. O gerador deste arquivo recomputa tudo e só grava se bater com o "
     "registrado (gate).",
     "",
     "## 1. O seletor de rota (que campos da ficha viram média, desvio e n)",
     "",
     "Para cada braço: usa `n_analisado` (senão `n_randomizado`); usa a mudança "
     "lida (senão deriva final−basal, com desvio combinado pela regra r=0,5 do "
     "Cochrane); converte o desvio conforme o TIPO que a ficha declara — intervalo "
     "de confiança vira DP pela largura, erro-padrão vira DP multiplicando por √n.",
     "",
     "```python", fonte("scripts/estudo3/dirigida.py", ["bounds_ic", "braco_deterministico"]), "```",
     "",
     "## 2. As cinco fórmulas (código verbatim do harness)",
     "",
     "- `md`: diferença de médias entre braços (m1 − m2).",
     "- `ic95_md`: intervalo de 95% = diferença ± 1,96 × erro-padrão combinado.",
     "- `dp_de_ic`: DP a partir de um IC95 = (largura ÷ 2 ÷ 1,96) × √n.",
     "- `dp_de_se`: DP a partir de um erro-padrão = EP × √n.",
     "- `dp_mudanca_r05`: DP da mudança a partir dos DPs basal/final (correlação 0,5).",
     "- `pool_dl_md`: síntese DerSimonian–Laird (pesos 1/variância; heterogeneidade τ²; I²).",
     "",
     "```python", fonte("scripts/estudo3/e3-harness.py",
                        ["md", "ic95_md", "dp_de_ic", "dp_de_se", "dp_mudanca_r05", "pool_dl_md"]), "```",
     "",
     "## 3. Exemplo feito à mão — gemma12 × Saslow 2017",
     "",
     "Ficha: exp mudança −0.8, tipo `IC95: -1.1 a -0.6`, n analisado 11; "
     "ctl mudança −0.3, tipo `IC95: -0.6 a 0.0`, n 8.",
     "",
     "```",
     "DP exp = (−0.6 − (−1.1)) / 2 / 1.96 × √11 = 0.1276 × 3.3166 = 0.42",
     "DP ctl = ( 0.0 − (−0.6)) / 2 / 1.96 × √8  = 0.1531 × 2.8284 = 0.43",
     "MD     = −0.8 − (−0.3) = −0.50",
     "EP     = √(0.42²/11 + 0.43²/8) = √(0.01604 + 0.02311) = 0.1979",
     "IC95   = −0.50 ± 1.96 × 0.1979 = [−0.89, −0.11]",
     "```",
     "",
     "Confere com a linha registrada do gemma12: `-0.5 [-0.89, -0.11]`.",
     ""]

falhas = 0
for modelo in MODELOS:
    res = json.loads((R2 / "resultados" / f"{modelo}.json").read_text(encoding="utf-8"))
    L.append(f"## 4.{MODELOS.index(modelo)+1} {modelo} — conta por estudo")
    L.append("")
    L.append("| estudo | sexteto (m,dp,n × 2 braços) | rota experimental | rota controle | MD [IC95] |")
    L.append("|---|---|---|---|---|")
    julg = {}
    preench = {}
    for g in res["gatilhos"]:
        if g.get("classe") == "sinal-como-impresso":
            julg[(g["estudo"], g["lado"])] = g["valor_usado"]
        if g.get("classe") == "campo-faltante" and g.get("preenchidos"):
            preench[(g["estudo"], g["lado"])] = g["preenchidos"]
    for e in res["por_estudo"]:
        rot = e["estudo"]
        if e.get("status") == "dados-insuficientes":
            L.append(f"| {rot} | — | FORA DO POOL: faltou {e['exp']}/{e['ctl']} | | |")
            continue
        tid = next(t for t, r in h3.ROT.items() if r == rot)
        fs = ficha_rep(modelo, tid) or {}
        rotas = []
        trio_ok = True
        for i, lado in enumerate(("braco_experimental", "braco_controle")):
            trio, rota = rota_braco(fs.get(lado, {}), julg.get((rot, lado)))
            if (rot, lado) in preench:
                rota += f" · GATILHO NR preencheu {preench[(rot, lado)]}"
                trio = tuple(e["sexteto"][i * 3:i * 3 + 3])
            rotas.append(rota)
            reg = e["sexteto"][i * 3:i * 3 + 3]
            if any(a is None or abs(float(a) - float(b)) > 0.005 for a, b in zip(trio, reg)):
                trio_ok = False
        s = e["sexteto"]
        md_rec = h3.md(*s)
        ic_rec = h3.ic95_md(*s)
        gate = "" if (md_rec == e["md"] and ic_rec == e["ic95"] and trio_ok) else " ⚠GATE"
        L.append(f"| {rot} | {s} | {rotas[0]} | {rotas[1]} | {e['md']} {e['ic95']}{gate} |")
        if gate:
            falhas += 1
    pool_rec = h3.pool_dl_md([e["sexteto"] for e in res["por_estudo"] if "sexteto" in e])
    ok = pool_rec == res["agregado"]
    if not ok:
        falhas += 1
    L.append("")
    L.append(f"**Pool DerSimonian–Laird**: {res['agregado']['md']} {res['agregado']['ic95']} "
             f"(τ²={res['agregado']['tau2']}, I²={res['agregado']['i2_pct']}%) — "
             f"recomputado pelo gerador: {'idêntico ✓' if ok else 'DIVERGIU ⚠'}")
    L.append("")

L.append("---")
L.append("*Todas as linhas acima foram recomputadas por este gerador a partir das fichas e "
         "conferidas contra os resultados registrados antes de gravar. Fontes: "
         "`scripts/estudo3/e3-harness.py` (fórmulas), `scripts/estudo3/dirigida.py` (rotas), "
         "`scripts/estudo4/e4-rodada2.py` (fila), `resultados/<modelo>.json` (registro).*")

assert falhas == 0, f"gate falhou em {falhas} ponto(s) — nada gravado"
(R2 / "contas-comparadas.md").write_text("\n".join(L), encoding="utf-8")
print(f"gate ok (0 divergências) · gravado {R2 / 'contas-comparadas.md'} ({len(L)} linhas)")
