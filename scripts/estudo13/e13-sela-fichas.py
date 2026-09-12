# -*- coding: utf-8 -*-
"""Seals the three v3 sheets of Study 13. Rerun only when a sheet changes BY DECISION, before registration."""
import hashlib
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
FICHAS = [("a1/v3", "dados/estudo13/prompts/a1-extraction-v3.txt"),
          ("a2/v3", "dados/estudo13/prompts/a2-extraction-v3.txt"),
          ("a3/v3", "dados/estudo13/prompts/a3-extraction-v3.txt")]
linhas = ["# Selos das três fichas v3 do Estudo 13 (protocolo §4). O harness confere estes selos antes da",
          "# primeira chamada e se recusa a começar se algum divergir. Gerado por scripts/estudo13/e13-sela-fichas.py.", ""]
for rot, rel in FICHAS:
    sha = hashlib.sha256(io.open(RAIZ / rel, "rb").read()).hexdigest()
    linhas.append(f"{sha}  {rot}  {rel}")
    print(f"  {rot:6s} {sha[:16]}...  {rel}")
io.open(RAIZ / "dados" / "estudo13" / "fichas.sha256", "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(linhas) + chr(10))
print("gravado dados/estudo13/fichas.sha256")
