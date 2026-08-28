# -*- coding: utf-8 -*-
"""EXTRAI E1 — Emenda 2: extrai texto dos 6 primários fechados (staging → fechados-texto).

PDFs: pypdf + normalização (ligaduras ﬁ/ﬂ/ﬀ/ﬃ, des-hifenização de quebra, espaços).
XML (manuscrito de autor via eutils): mesmo fluxo dos abertos (abstract + body,
ref-list removida). Saída com pseudo-IDs REF<n> em corpus/fechados-texto/ (fora do repo).
Também reporta o F0 do estrato (palavras/tokens estimados).
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from pypdf import PdfReader

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
STAG = RAIZ / "corpus" / "fechados-staging"
OUT = RAIZ / "corpus" / "fechados-texto"

FONTES = {
    "REF26": ("pdf", "ref26-diaper-2021.pdf"),
    "REF29": ("pdf", "ref29-dewaal-2021.pdf"),
    "REF30": ("xml", "PMC8320377.xml"),
    "REF33": ("pdf", "ref33-calvovecino-2018.pdf"),
    "REF41": ("pdf", "PMC12713225.pdf"),
    "REF47": ("pdf", "ref47-hokenek-2022.pdf"),
}
LIGADURAS = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "­": ""}


def normaliza(t):
    for a, b in LIGADURAS.items():
        t = t.replace(a, b)
    # des-hifenização de quebra de linha/coluna: "man- agement" -> "management"
    t = re.sub(r"(?<=[a-z])-\s+(?=[a-z])", "", t)
    t = t.replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", re.sub(r"\s*\n\s*", " ", t)).strip()


def corta_referencias(t):
    """Remove a seção de referências (última ocorrência do título no terço final)."""
    for pad in (r"\bR\s?e\s?f\s?e\s?r\s?e\s?n\s?c\s?e\s?s\b", r"\bREFERENCES\b", r"\bBibliography\b"):
        ms = list(re.finditer(pad, t))
        if ms and ms[-1].start() > 0.6 * len(t):
            return t[:ms[-1].start()]
    return t


def do_pdf(caminho):
    r = PdfReader(caminho)
    return normaliza(corta_referencias(" ".join((p.extract_text() or "") for p in r.pages)))


def do_xml(caminho):
    raw = caminho.read_text(encoding="utf-8")
    xml = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", raw, count=1)
    root = ET.fromstring(xml)
    for pai in root.iter():
        for rl in list(pai):
            if rl.tag == "ref-list":
                pai.remove(rl)
    partes = []
    ab = root.find(".//abstract")
    if ab is not None:
        partes.append(" ".join(ab.itertext()))
    body = root.find(".//body")
    if body is not None:
        partes.append(" ".join(body.itertext()))
    return normaliza(" ".join(partes))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"{'ID':<7} {'palavras':>9} {'~tokens':>9}  fonte")
    for rid, (tipo, nome) in FONTES.items():
        caminho = STAG / nome
        t = do_pdf(caminho) if tipo == "pdf" else do_xml(caminho)
        (OUT / f"{rid}.txt").write_text(t, encoding="utf-8")
        pal = len(t.split())
        aviso = "  <-- excede contexto!" if pal * 1.45 > 13500 else ""
        print(f"{rid:<7} {pal:>9,} {int(pal*1.45):>9,}  {nome}{aviso}")


if __name__ == "__main__":
    main()
