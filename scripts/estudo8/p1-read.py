# -*- coding: utf-8 -*-
"""EXTRAI Study 8 — Phase P1 READ (protocol §3): the five-model extraction
replication under ENGLISH instruments.

All five iGPU cast models extract the 14 perturbed MA-1 primaries from zero,
two replicates, under the frozen English T1 sheet (dados/estudo8/prompts/
t1-extraction.txt, {ARTICLE} replaced verbatim). Same corpora, same seals,
same keys as the Portuguese record — only the instruction language changes.
Uniform token allowance (4000) per the round-2 precedent. One model resident
at a time (unload discipline). Resume-safe.

Run: python scripts/estudo8/p1-read.py [model ...]
Outputs: dados/estudo8/saidas/p1/<model>/<trial>-r{1,2}.json
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
ABERTOS = ROOT / "corpus" / "perturbados"
FECHADOS = ROOT / "corpus" / "perturbados-fechados"
CAST = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14"]
MAXTOK = 4000  # uniform allowance for all five (Study-4 round-2 precedent)

_x = importlib.util.spec_from_file_location("ext", ROOT / "scripts" / "estudo4" / "e4-extensao.py")
ext = importlib.util.module_from_spec(_x)
_x.loader.exec_module(ext)
h3 = ext.h3  # five-model registry injected by the extension


def descarrega(tag=None):
    tags = [tag] if tag else sorted({m["ollama"] for m in h3.MODELS.values()})
    for t in tags:
        subprocess.run(["ollama", "stop", t], capture_output=True)


def trials():
    ts = [(p.stem, p) for p in sorted(ABERTOS.glob("*.txt"))]
    ts += [(p.stem, p) for p in sorted(FECHADOS.glob("*.txt"))]
    return ts


def roda_modelo(modelo, tpl, lista):
    out_dir = E8 / "saidas" / "p1" / modelo
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n===== Study 8 · P1 READ · {modelo} [{h3.MODELS[modelo]['ollama']}] · "
          f"{len(lista)} primaries x 2 (EN instrument)", flush=True)
    for tid, caminho in lista:
        prompt = tpl.replace("{ARTICLE}", caminho.read_text(encoding="utf-8"))
        for rep in (1, 2):
            out = out_dir / f"{tid}-r{rep}.json"
            if out.exists():
                print(f"  skip {modelo} {tid}-r{rep}", flush=True)
                continue
            r = h3.gerar(modelo, prompt, max_tokens=MAXTOK)
            out.write_text(json.dumps(dict(modelo=modelo, trial=tid, replica=rep, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  {modelo} {tid}-r{rep}: {r['dt']:.0f}s, {r['tokens']} tok, "
                  f"fim={r['finish']}", flush=True)


def main():
    alvo = sys.argv[1:] or CAST
    for selo in ("perturbacoes-estudo1.json", "perturbacoes-fechados.json",
                 "perturbacoes-manuais.json", "perturbacoes-fechados-manuais.json"):
        p = ROOT / "dados" / "estudo1" / selo
        if p.exists():
            print(f"SHA-256 {selo}: {hashlib.sha256(p.read_bytes()).hexdigest()}", flush=True)
    tpl = (E8 / "prompts" / "t1-extraction.txt").read_text(encoding="utf-8")
    lista = trials()
    print("initial memory sweep:", flush=True)
    descarrega()
    t0 = time.time()
    anterior = None
    for modelo in alvo:
        if anterior:
            descarrega(h3.MODELS[anterior]["ollama"])
        roda_modelo(modelo, tpl, lista)
        anterior = modelo
    if anterior:
        descarrega(h3.MODELS[anterior]["ollama"])
    print(f"\n== P1 READ COMPLETE in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
