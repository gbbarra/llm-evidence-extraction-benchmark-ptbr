# -*- coding: utf-8 -*-
"""Study 5 — render the turn-by-turn transcripts as a readable screenplay.

Run: python scripts/estudo5/transcricao-md.py [G1|G2|G3...]
Output: dados/estudo5/transcricoes-<rung>.md
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D5 = ROOT / "dados" / "estudo5"

for rung in (sys.argv[1:] or ["G1", "G2"]):
    pasta = D5 / "saidas" / rung.upper()
    if not pasta.exists():
        continue
    L = [f"# Estudo 5 · {rung.upper()} — transcrição turno a turno",
         "",
         "O que o modelo emitiu (MODELO), o que o harness devolveu (HARNESS: resultado "
         "ou aviso). Não há canal de pensamento: `think=false` — isto é tudo que o "
         "modelo produz. Fichas de entrada: as extrações da rodada 2 do próprio gemma12.",
         ""]
    for f in sorted(pasta.glob("*.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        L.append(f"## {j.get('estudo', f.stem)}")
        L.append("")
        L.append("```")
        for t in j.get("turnos", []):
            L.append(f"MODELO : {t.get('emitiu', '')}")
            if t.get("aviso") and t["aviso"] != "formato":
                L.append(f"HARNESS: {t['aviso']}")
            elif t.get("aviso") == "formato":
                L.append("HARNESS: AVISO: formato inválido — emita exatamente uma chamada.")
            elif t.get("resultado"):
                L.append(f"HARNESS: {t['resultado']}")
        L.append(f"FINAL  : {json.dumps(j.get('final'), ensure_ascii=False)}")
        L.append("```")
        L.append("")
    out = D5 / f"transcricoes-{rung.upper()}.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"gravado {out}")
