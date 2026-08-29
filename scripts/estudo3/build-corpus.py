# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — corpus text builder.

Extracts plain text for the 7 primaries of the low-carb T2DM anchor
(PMC13242649) into corpus/estudo3/primarios-texto/ (gitignored, like E1):
  - 5 open-access XMLs from corpus/estudo3/primarios/ (id = PMCID)
  - 2 closed-stratum sources from corpus/estudo3/fechados-staging/
    (id = anchor reference number: REF9 Saslow 2023 PDF, REF12 Thomsen XML)

Same normalization as Study 1's closed-stratum pipeline: ligatures,
line-break de-hyphenation, whitespace collapse, references section cut.
Reports word/token counts (context F0 check: budget is ctx 16384).
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from pypdf import PdfReader

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "corpus" / "estudo3"
OUT = BASE / "primarios-texto"

SOURCES = {
    "PMC5329646": ("xml", BASE / "primarios" / "PMC5329646.xml"),   # Saslow 2017
    "REF9":       ("pdf", BASE / "fechados-staging" / "saslow2023-afm.pdf"),
    "PMC9606840": ("xml", BASE / "primarios" / "PMC9606840.xml"),   # Dorans 2022
    "PMC7535044": ("xml", BASE / "primarios" / "PMC7535044.xml"),   # Chen 2020
    "REF12":      ("xml", BASE / "fechados-staging" / "PMC8739348.xml"),  # Thomsen 2022
    "PMC6024764": ("xml", BASE / "primarios" / "PMC6024764.xml"),   # Wang 2018
    "PMC5048014": ("xml", BASE / "primarios" / "PMC5048014.xml"),   # Goday 2016
}
LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "­": ""}


def normalize(t):
    for a, b in LIGATURES.items():
        t = t.replace(a, b)
    t = re.sub(r"(?<=[a-z])-\s+(?=[a-z])", "", t)  # line-break de-hyphenation
    t = t.replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", re.sub(r"\s*\n\s*", " ", t)).strip()


def cut_references(t):
    """Drop the references section (last title occurrence in the final third)."""
    for pat in (r"\bR\s?e\s?f\s?e\s?r\s?e\s?n\s?c\s?e\s?s\b", r"\bREFERENCES\b", r"\bBibliography\b"):
        ms = list(re.finditer(pat, t))
        if ms and ms[-1].start() > 0.6 * len(t):
            return t[: ms[-1].start()]
    return t


def from_pdf(path):
    r = PdfReader(path)
    return normalize(cut_references(" ".join((p.extract_text() or "") for p in r.pages)))


def from_xml(path):
    raw = path.read_text(encoding="utf-8")
    xml = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", raw, count=1)
    root = ET.fromstring(xml)
    for parent in root.iter():
        for child in list(parent):
            if child.tag == "ref-list":
                parent.remove(child)
    parts = []
    ab = root.find(".//abstract")
    if ab is not None:
        parts.append(" ".join(ab.itertext()))
    body = root.find(".//body")
    if body is not None:
        parts.append(" ".join(body.itertext()))
    # Some journals (e.g. Nature family) ship tables in <floats-group> outside
    # <body>; without this, primary-endpoint tables vanish from the input
    # (Study-1 lesson: Sujatha's "table 4 out of input"). Append only the
    # table-wraps that body did not already contain.
    body_tables = set()
    if body is not None:
        for tw in body.iter("table-wrap"):
            body_tables.add(id(tw))
    for fg in root.iter("floats-group"):
        for tw in fg.iter("table-wrap"):
            if id(tw) not in body_tables:
                parts.append(" ".join(tw.itertext()))
    return normalize(" ".join(parts))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"{'ID':<12} {'words':>9} {'~tokens':>9}  source")
    for tid, (kind, path) in SOURCES.items():
        t = from_pdf(path) if kind == "pdf" else from_xml(path)
        (OUT / f"{tid}.txt").write_text(t, encoding="utf-8")
        words = len(t.split())
        warn = "  <-- exceeds context budget!" if words * 1.45 > 13500 else ""
        print(f"{tid:<12} {words:>9,} {int(words*1.45):>9,}  {path.name}{warn}")


if __name__ == "__main__":
    main()
