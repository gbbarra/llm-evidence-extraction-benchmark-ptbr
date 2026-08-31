# -*- coding: utf-8 -*-
"""EXTRAI Study 6 — MA-1 fresh extraction (protocol §3.1).

gemma4:12b re-extracts all 14 perturbed GDFT primaries from zero, two
replicates, under the FROZEN Study-1 T1 instrument (template verbatim,
ctx 16384, reasoning off). Open stratum from corpus/perturbados, closed
stratum from corpus/perturbados-fechados. Resume-safe.

Run: python scripts/estudo6/e6-extracao.py
Outputs: dados/estudo6/saidas/gemma12/extracao/<id>-r{1,2}.json
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "dados" / "estudo6" / "saidas" / "gemma12" / "extracao"
ABERTOS = ROOT / "corpus" / "perturbados"
FECHADOS = ROOT / "corpus" / "perturbados-fechados"
MODELO = "gemma12"

_sp = importlib.util.spec_from_file_location("e1", ROOT / "scripts" / "estudo1" / "e1-harness.py")
e1 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(e1)


def trials():
    ts = [(p.stem, p) for p in sorted(ABERTOS.glob("*.txt"))]
    ts += [(p.stem, p) for p in sorted(FECHADOS.glob("*.txt"))]
    return ts


def main():
    tpl = (ROOT / "dados" / "estudo1" / "prompts" / "t1-extracao.txt").read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    lista = trials()
    print(f"===== Estudo 6 · extração fresca MA-1 · {MODELO} · {len(lista)} primários × 2", flush=True)
    t0 = time.time()
    for tid, caminho in lista:
        prompt = tpl.replace("{ARTIGO}", caminho.read_text(encoding="utf-8"))
        for rep in (1, 2):
            out = OUT / f"{tid}-r{rep}.json"
            if out.exists():
                print(f"  pulando {tid}-r{rep}", flush=True)
                continue
            r = e1.run_ollama(MODELO, prompt, e1.MAX_TOKENS["t1"])
            out.write_text(json.dumps(dict(modelo=MODELO, trial=tid, replica=rep, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  extracao {tid}-r{rep}: {r['dt']:.0f}s, {r['tokens']} tok, fim={r['finish']}", flush=True)
    print(f"\nExtração MA-1 completa em {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
