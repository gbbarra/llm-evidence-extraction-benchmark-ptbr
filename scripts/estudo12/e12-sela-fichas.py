# -*- coding: utf-8 -*-
"""Sela as seis fichas da campanha. Rodar de novo só quando uma ficha mudar POR DECISÃO.

As fichas das âncoras 1 e 2 são as congeladas, que produziram o registro publicado. Elas são o
controle da H12.5: se mudarem, o efeito da subida de contexto fica confundido com o de instrumento, e
a hipótese perde o sentido. Este selo existe para que uma edição acidental pare a campanha em vez de
passar despercebida.
"""
import hashlib
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
FICHAS = [
    ("a1/v1", "dados/instruments-en/estudo1/t1-extraction.txt"),
    ("a1/v2", "dados/estudo9/prompts/t1-extraction-v2.txt"),
    ("a2/v1", "dados/instruments-en/estudo3/e3-extraction.txt"),
    ("a2/v2", "dados/estudo9/prompts/e3-extraction-v2.txt"),
    ("a3/v1", "dados/estudo12/prompts/a3-extraction.txt"),
    ("a3/v2", "dados/estudo12/prompts/a3-extraction-v2.txt"),
]
linhas = ["# Selos das seis fichas da campanha do Estudo 12 (§3 e §8.6 do protocolo).",
          "# As das âncoras 1 e 2 são as CONGELADAS, que produziram o registro publicado: elas são o",
          "# controle da H12.5, e uma edição nelas confundiria o efeito do contexto com o do instrumento.",
          "# O harness confere estes selos antes da primeira chamada e se recusa a começar se algum",
          "# divergir. Gerado por scripts/estudo12/e12-sela-fichas.py.", ""]
for rot, rel in FICHAS:
    b = io.open(RAIZ / rel, "rb").read()
    sha = hashlib.sha256(b).hexdigest()
    linhas.append(f"{sha}  {rot}  {rel}")
    print(f"  {rot:6s} {sha[:16]}...  {rel}")
io.open(RAIZ / "dados" / "estudo12" / "fichas.sha256", "w", encoding="utf-8",
        newline=chr(10)).write(chr(10).join(linhas) + chr(10))
print("\ngravado dados/estudo12/fichas.sha256")
