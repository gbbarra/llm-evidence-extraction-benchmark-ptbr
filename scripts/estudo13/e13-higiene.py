# -*- coding: utf-8 -*-
"""EXTRAI Study 13 — text hygiene: strip the control characters that PDF-to-text conversion leaves in a primary
(U+0001–U+0008, U+000B, U+000C, U+000E–U+001F, U+007F) before the model reads it. Applied at read time by the
Study 13 harness, so the sealed corpora on disk are untouched; the count removed is recorded per call. Numbers
are never touched — `main` proves it on every corpus file.

Run: python scripts/estudo13/e13-higiene.py    (report per corpus file; fails if a number would change)
"""
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
CONTROLE = re.compile("[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]")
NUMEROS = re.compile(r"\d+(?:[.,]\d+)?")
CORPORA = [RAIZ / "corpus" / "perturbados", RAIZ / "corpus" / "perturbados-fechados",
           RAIZ / "corpus" / "estudo3" / "perturbados", RAIZ / "corpus" / "estudo12" / "perturbados"]


def limpa(texto):
    """(clean text, characters removed). A control character is replaced by a space so that two tokens it
    separated do not fuse into one."""
    novo, n = CONTROLE.subn(" ", texto)
    return novo, n


def main():
    total, ruins = 0, []
    for d in CORPORA:
        if not d.exists():
            continue
        for p in sorted(d.glob("*.txt")):
            s = io.open(p, encoding="utf-8").read()
            novo, n = limpa(s)
            if NUMEROS.findall(s) != NUMEROS.findall(novo):
                ruins.append(str(p))
            if n:
                print(f"  {d.name}/{p.name}: {n} control characters removed")
            total += n
    print(f"total removed: {total}; numbers unchanged in every file: {'yes' if not ruins else 'NO — ' + ', '.join(ruins)}")
    if ruins:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
