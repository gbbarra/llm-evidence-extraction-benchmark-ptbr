# -*- coding: utf-8 -*-
"""EXTRAI — Estudo 1: extrai as tabelas da metanálise-âncora para JSON estruturado.

O gabarito bruto preserva TODAS as células como publicadas (fidelidade ao humano,
mesmo onde o humano possa ter errado — discordâncias são adjudicadas na correção,
nunca editadas aqui). Cada linha ganha o número da referência citada e a marcação
de acesso aberto vinda de corpus/primarios/primarios.json.

Saída: dados/estudo1/gabarito-ma.json
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]


def celulas(tr):
    return [" ".join(td.itertext()).strip().replace("\xa0", " ") for td in list(tr)]


def main():
    raw = (RAIZ / "corpus" / "ma" / "ma-gdft.xml").read_text(encoding="utf-8")
    xml = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", raw, count=1)
    root = ET.fromstring(xml)

    prim = json.loads((RAIZ / "corpus" / "primarios" / "primarios.json").read_text(encoding="utf-8"))
    oa = {p["ref"]: p.get("xml_baixado", False) for p in prim}
    pmcid = {p["ref"]: p.get("pmcid") for p in prim}

    tabelas = []
    for i, t in enumerate(root.findall(".//table-wrap"), 1):
        capel = t.find(".//caption")
        cap = " ".join(capel.itertext()).strip() if capel is not None else ""
        trs = t.findall(".//tr")
        if not trs:
            continue
        cab = celulas(trs[0])
        linhas = []
        for tr in trs[1:]:
            cel = celulas(tr)
            if not cel or not any(cel):
                continue
            rotulo = cel[0]
            # colchete de abertura pode se perder no XML ("Hokenek et al. 47]")
            m = re.search(r"\[?\s*(\d{1,3})\s*\]", rotulo)
            ref = m.group(1) if m else None
            aberto = bool(ref and oa.get(ref))
            # Emenda 2: primários fechados ganham pseudo-ID REF<n> (estrato fechado)
            FECHADOS = {"26", "29", "30", "33", "41", "47"}
            pid = pmcid.get(ref) if aberto else (f"REF{ref}" if ref in FECHADOS else None)
            linhas.append(dict(
                rotulo=re.sub(r"\[?\s*\d{1,3}\s*\]\s*", "", rotulo).strip(),
                ref=ref,
                acesso_aberto=aberto,
                pmcid=pid,
                celulas=dict(zip(cab[1:], cel[1:len(cab)])),
            ))
        tabelas.append(dict(numero=i, legenda=cap, colunas=cab, linhas=linhas))
        n_oa = sum(1 for l in linhas if l["acesso_aberto"])
        print(f"{i:>2}. {cap[:70]}")
        print(f"      {len(linhas)} linhas | {n_oa} de estudos abertos")

    out = RAIZ / "dados" / "estudo1" / "gabarito-ma.json"
    out.write_text(json.dumps(dict(
        fonte="PMC13235771 — tabelas transcritas como publicadas (sem correção)",
        tabelas=tabelas), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nsalvo: {out.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
