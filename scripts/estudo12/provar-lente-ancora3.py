# -*- coding: utf-8 -*-
"""A lente de desperturbação sobrevive ao selo da âncora 3? Medido nos dois desenhos.

O defeito, achado pela revisão adversarial do protocolo em 2026-09-08. A lente congelada é

    txt = json.dumps(ficha)
    for reg in SELO[tid]:
        txt = txt.replace(perturbado, original)          # e6-downstream.py:75-81

— substring cru, sequencial, sobre a ficha inteira, **inclusive o campo de citação da ficha v2**, que
carrega até 240 caracteres de texto do artigo. Minha prova de viabilidade (`provar-perturbacao-
coerente.py`) testou ausência **com fronteira** (`perturbar.py:92`), que é outro critério. Os dois não
testam a mesma coisa, e o Estudo 9 já pagou por isso: o par 31→28 aplicado dentro de "1283.2" reprovou
quatro transcrições corretas.

A âncora 3 agrava o problema porque seus valores são inteiros de dois dígitos, que ocorrem como
substring de quase todo número longo de um artigo clínico, enquanto as âncoras 1 e 2 deslocavam
decimais de quatro ou cinco dígitos.

Este script mede o estrago sobre o pior caso real — o texto inteiro do artigo, que é o que uma citação
da ficha v2 pode conter — e testa se a correção proposta o elimina:

  LENTE A (congelada)  replaces sequenciais, substring, na ordem do selo
  LENTE B (proposta)   passe único simultâneo, com fronteira numérica, sem reescrever a própria saída

Não altera a lente de ninguém: as âncoras 1 e 2 continuam com a A. A pergunta é se a âncora 3 precisa
da B, e a resposta tem de estar no protocolo antes de qualquer chamada.
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
PRIM = RAIZ / "dados" / "estudo11" / "primarios"
SELOS = json.loads(io.open(RAIZ / "dados" / "estudo12" / "perturbacao-coerente-ancora3.json",
                           encoding="utf-8").read())

ARQ = {"Luis-Silva, 2024": "PMC11514138.xml", "Shaker, 2025": "PMC11707904.xml",
       "Ibarra-Estrada, 2023": "PMC10010212.xml", "Aguilar, 2016": "aguilar-2016-medcrit.txt",
       "Kirov, 2001": "kirov2001.txt", "Levin, 2004": "levin2004.txt",
       "Dong, 2025": "PMC12751372.xml", "Memis, 2002": "memis2002.txt"}


def texto_de(arq):
    t = io.open(PRIM / arq, encoding="utf-8", errors="replace").read()
    if arq.endswith(".xml"):
        t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def selo_de(ensaio):
    """Pares perturbado->original do ensaio, como o selo os guardaria."""
    pares = []
    for b in SELOS["bracos"]:
        if b["ensaio"] != ensaio or not b["viavel"]:
            continue
        par_n = (str(b["novo_n"]), str(b["n"]))
        if par_n not in pares:
            pares.append(par_n)
        if b["novo_pct"] and b["pct_fonte"]:
            pares.append((str(b["novo_pct"]), str(b["pct_fonte"])))
    return pares


def lente_A(txt, selo):
    """A congelada: replaces sequenciais de substring, na ordem do selo."""
    for p, o in selo:
        txt = txt.replace(p, o)
    return txt


def lente_B(txt, selo):
    """A proposta: passe único simultâneo, com fronteira numérica. A saída nunca é reescrita."""
    if not selo:
        return txt
    # o mais longo primeiro dentro da alternância, para o casamento preferir 36.6 a 36
    alt = "|".join(re.escape(p) for p, _ in sorted(selo, key=lambda x: -len(x[0])))
    mapa = dict(selo)
    pad = re.compile(r"(?<![\w.,\-–])(" + alt + r")(?![\w.])")
    return pad.sub(lambda m: mapa[m.group(1)], txt)


print(f"{'ensaio':22s} {'pares':>6s} {'A: trocas':>10s} {'A: indevidas':>13s} {'B: trocas':>10s} {'B: indevidas':>13s}")
print("-" * 88)
tot_a = tot_b = 0
detalhe = []
for ensaio, arq in ARQ.items():
    selo = selo_de(ensaio)
    if not selo:
        print(f"{ensaio:22s} {'—':>6s}   (sem prova de leitura; nada a selar)")
        continue
    txt = texto_de(arq)
    # o alvo legítimo: quantas ocorrências COM FRONTEIRA de cada valor perturbado existiriam
    legitimas = sum(len(re.findall(r"(?<![\w.,\-–])" + re.escape(p) + r"(?![\w.])", txt)) for p, _ in selo)
    # aplicamos as lentes ao texto ORIGINAL: toda troca aqui é indevida por definição, porque o texto
    # original não contém valores perturbados -- exceto onde o perturbado calha de ser substring
    a = sum(txt.count(p) for p, _ in selo)
    b = len(re.findall(r"(?<![\w.,\-–])(" + "|".join(re.escape(p) for p, _ in selo) + r")(?![\w.])", txt))
    tot_a += a; tot_b += b
    vitimas = []
    for p, o in selo:
        for m in re.finditer(re.escape(p), txt):
            ctx = txt[max(0, m.start() - 8):m.end() + 8]
            n = re.search(r"[\d.,]*" + re.escape(p) + r"[\d.,]*", ctx)
            if n and n.group(0) != p:
                vitimas.append(n.group(0))
    detalhe.append((ensaio, sorted(set(vitimas))[:7]))
    print(f"{ensaio:22s} {len(selo):6d} {a:10d} {a:13d} {b:10d} {b:13d}")

print("-" * 88)
print(f"{'TOTAL':22s} {'':6s} {tot_a:10d} {tot_a:13d} {tot_b:10d} {tot_b:13d}")
print("""
Leitura da tabela. O texto testado é o ORIGINAL do artigo, que não contém valor perturbado nenhum.
Logo TODA troca aqui é indevida: é a lente reescrevendo um número que não é dela. É o pior caso real,
porque a citação da ficha v2 pode conter qualquer trecho do artigo.
""")
print("as vítimas, por ensaio — números do próprio artigo que contêm o valor perturbado:")
for ensaio, v in detalhe:
    if v:
        print(f"  {ensaio:22s} {', '.join(v)}")

print(f"""
VEREDITO. A lente A comete {tot_a} substituições indevidas; a lente B comete {tot_b}.
{'A correção proposta elimina o defeito.' if tot_b == 0 else 'A correção proposta NÃO basta: rever.'}

Consequência para o protocolo: a âncora 3 não pode ser corrigida pela lente congelada. Precisa da
lente de passe único com fronteira, encomendada como instrumento e declarada como diferença nomeada
entre a âncora 3 e as âncoras 1 e 2 -- que continuam com a lente A, intocada, para não quebrar a
comparabilidade com o registro publicado.""")
