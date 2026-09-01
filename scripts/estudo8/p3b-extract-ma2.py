# -*- coding: utf-8 -*-
"""Study 8 / P3-b CREATE (protocol §3): fresh five-model extraction of the 7
perturbed MA-2 primaries under the ENGLISH sheet (e3-extraction.txt, article
appended). Same corpus and seals as the Portuguese round-2 record; uniform
4000-token allowance; one model resident at a time; resume-safe.

Run: python scripts/estudo8/p3b-extract-ma2.py [model ...]
Outputs: dados/estudo8/saidas/p3b/<model>/<trial>-r{1,2}.json
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E8 = ROOT / "dados" / "estudo8"
PERT = ROOT / "corpus" / "estudo3" / "perturbados"
CAST = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14"]
MAXTOK = 4000

_x = importlib.util.spec_from_file_location("ext", ROOT / "scripts" / "estudo4" / "e4-extensao.py")
ext = importlib.util.module_from_spec(_x)
_x.loader.exec_module(ext)
h3 = ext.h3


def descarrega(tag=None):
    tags = [tag] if tag else sorted({m["ollama"] for m in h3.MODELS.values()})
    for t in tags:
        subprocess.run(["ollama", "stop", t], capture_output=True)


def main():
    alvo = sys.argv[1:] or CAST
    p = ROOT / "dados" / "estudo3" / "perturbacoes-estudo3.json"
    print(f"SHA-256 perturbacoes-estudo3.json: {hashlib.sha256(p.read_bytes()).hexdigest()}",
          flush=True)
    tpl = (E8 / "prompts" / "e3-extraction.txt").read_text(encoding="utf-8")
    print("initial memory sweep:", flush=True)
    descarrega()
    t0 = time.time()
    anterior = None
    for modelo in alvo:
        if anterior:
            descarrega(h3.MODELS[anterior]["ollama"])
        out_dir = E8 / "saidas" / "p3b" / modelo
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n===== Study 8 · P3-b MA-2 · {modelo} [{h3.MODELS[modelo]['ollama']}] · "
              f"7 primaries x 2 (EN sheet)", flush=True)
        for tid in h3.TRIALS:
            texto = (PERT / f"{tid}.txt").read_text(encoding="utf-8")
            for rep in (1, 2):
                out = out_dir / f"{tid}-r{rep}.json"
                if out.exists():
                    print(f"  skip {modelo} {tid}-r{rep}", flush=True)
                    continue
                r = h3.gerar(modelo, tpl + texto, max_tokens=MAXTOK)
                out.write_text(json.dumps(dict(modelo=modelo, trial=tid, replica=rep, **r),
                                          ensure_ascii=False, indent=1), encoding="utf-8")
                print(f"  {modelo} {tid}-r{rep}: {r['dt']:.0f}s, {r['tokens']} tok, "
                      f"fim={r['finish']}", flush=True)
        anterior = modelo
    if anterior:
        descarrega(h3.MODELS[anterior]["ollama"])
    print(f"\n== P3-B MA-2 EXTRACTION COMPLETE in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
