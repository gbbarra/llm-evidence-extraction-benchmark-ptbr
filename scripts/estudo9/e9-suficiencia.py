# -*- coding: utf-8 -*-
"""Auto-suficiencia das citacoes v2: um revisor decidiria olhando so a ficha?

Para cada celula elegivel da chave, junta o que o gemma escreveu (valor + citacao),
o valor verificado na fonte e o veredito do comparador. Marca mecanicamente o que
da para checar sem ler o artigo; o julgamento de suficiencia e editorial, feito na leitura.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"C:\Users\gbbarra\Documents\localtts\extrai")


def carrega(n, rel):
    sp = importlib.util.spec_from_file_location(n, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


e6a = carrega("e6a", "scripts/estudo6/e6-avalia.py")
e7d = carrega("e7d", "scripts/estudo7/e7-downstream.py")
red = carrega("red", "scripts/estudo9/e9-redes.py")
d6, compat = e6a.d6, e6a.compat
PT2EN = {v: k for k, v in e7d.MA1_EN2PT.items()}


def eleg():
    out = {}
    for tid, campos in d6.GAB.items():
        for campo, cel in campos.items():
            vf, ver = cel.get("valor_fonte"), str(cel.get("veredito"))
            if vf in (None, "") or ver in ("sem-valor-na-ma", "pendente-adjudicacao",
                                           "nao-sustentada", "dado-fora-do-insumo"):
                continue
            if re.search(r"\d", str(vf)):
                out.setdefault(tid, []).append(campo)
    return out


def celula(js, campo_pt):
    v = (js or {}).get(PT2EN[campo_pt])
    return v if isinstance(v, dict) else {"value": v, "where": "", "quote": ""}


linhas = []
for tid, campos in eleg().items():
    js = None
    for rep in (1, 2):
        f = ROOT / "dados/estudo9/saidas/v2/gemma12/ma1" / f"{tid}-r{rep}.json"
        if f.exists():
            j = d6.h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            if isinstance(j, dict):
                js = j
                break
    if js is None:
        continue
    cel_pt = {p: {"valor": str(celula(js, p).get("value", "") or "")} for p in PT2EN}
    rev = d6.desperturba(tid, cel_pt)
    for campo in campos:
        c = celula(js, campo)
        val = str(c.get("value", "") or "")
        quote = str(c.get("quote", "") or "")
        fonte = str(d6.GAB[tid][campo].get("valor_fonte"))
        ok = compat((rev.get(campo) or {}).get("valor"), fonte)
        # checavel sem abrir o artigo: todo numero do valor aparece na propria citacao
        # o hifen ENTRE digitos e separador de intervalo, nao sinal negativo:
        # "1474-2600" nao deve virar 1474 e -2600, senao a checagem falha sozinha
        nums = re.findall(r"(?<![\d.])-?\d+(?:[.,]\d+)?", val.replace(",", "."))
        na_citacao = bool(nums) and all(red.num_no_texto(n, quote) for n in nums)
        linhas.append(dict(trial=tid, campo=campo, valor=val, quote=quote,
                           where=str(c.get("where", "") or ""), fonte=fonte,
                           correto=bool(ok), autocheca=na_citacao, tem_quote=bool(quote.strip())))

ROOT.joinpath("dados", "estudo9", "suficiencia-gemma12.json").write_text(
    json.dumps(linhas, ensure_ascii=False, indent=1), encoding="utf-8")

n = len(linhas)
print(f"celulas elegiveis avaliadas: {n}")
print(f"  corretas vs chave           : {sum(l['correto'] for l in linhas)}")
print(f"  com citacao preenchida      : {sum(l['tem_quote'] for l in linhas)}")
print(f"  valor conferivel na citacao : {sum(l['autocheca'] for l in linhas)}")
print()
print("=== cruzamento: acerto x auto-checavel ===")
for corr in (True, False):
    for auto in (True, False):
        k = [l for l in linhas if l["correto"] == corr and l["autocheca"] == auto]
        print(f"  {'correto' if corr else 'divergente':<11} {'auto-checavel' if auto else 'NAO auto-checavel':<18} {len(k):>4}")
