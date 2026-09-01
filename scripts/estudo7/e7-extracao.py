# -*- coding: utf-8 -*-
"""EXTRAI Study 7 — fresh extraction, clean texts, both anchors (protocol §4.3).

gemma4:12b reads every ORIGINAL, unperturbed primary — MA-1's 14 GDFT trials
and MA-2's 7 low-carb trials — two replicates each, under the frozen ENGLISH
instruments copied into dados/estudo7/prompts/ at registration. No seal, no
reversal: natural conditions (protocol §2 scoping applies). Resume-safe.

Run: python scripts/estudo7/e7-extracao.py
Outputs: dados/estudo7/saidas/gemma12/{ma1,ma2}/<id>-r{1,2}.json
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E7 = ROOT / "dados" / "estudo7"
MODELO = "gemma12"

_sp = importlib.util.spec_from_file_location("e1", ROOT / "scripts" / "estudo1" / "e1-harness.py")
e1 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(e1)

MA1_DIRS = [ROOT / "corpus" / "primarios-texto", ROOT / "corpus" / "fechados-texto"]
MA2_DIRS = [ROOT / "corpus" / "estudo3" / "primarios-texto"]


def trials(dirs):
    ts = []
    for d in dirs:
        ts += [(p.stem, p) for p in sorted(d.glob("*.txt"))]
    return ts


def roda_anchor(rotulo, dirs, tpl_nome, monta_prompt):
    tpl = (E7 / "prompts" / tpl_nome).read_text(encoding="utf-8")
    out_dir = E7 / "saidas" / "gemma12" / rotulo
    out_dir.mkdir(parents=True, exist_ok=True)
    lista = trials(dirs)
    print(f"===== Study 7 · {rotulo} · {MODELO} · {len(lista)} primaries x 2 (clean texts)", flush=True)
    for tid, caminho in lista:
        prompt = monta_prompt(tpl, caminho.read_text(encoding="utf-8"))
        for rep in (1, 2):
            out = out_dir / f"{tid}-r{rep}.json"
            if out.exists():
                print(f"  skip {tid}-r{rep}", flush=True)
                continue
            r = e1.run_ollama(MODELO, prompt, e1.MAX_TOKENS["t1"])
            out.write_text(json.dumps(dict(modelo=MODELO, trial=tid, replica=rep,
                                           anchor=rotulo, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  {rotulo} {tid}-r{rep}: {r['dt']:.0f}s, {r['tokens']} tok, fim={r['finish']}",
                  flush=True)


def main():
    t0 = time.time()
    # MA-1 sheet: {ARTICLE} placeholder replaced with the full text
    roda_anchor("ma1", MA1_DIRS, "t1-extraction.txt",
                lambda tpl, txt: tpl.replace("{ARTICLE}", txt))
    # MA-2 sheet: the instrument ends with "ARTICLE:", the text is appended
    roda_anchor("ma2", MA2_DIRS, "e3-extraction.txt",
                lambda tpl, txt: tpl + "\n" + txt)
    print(f"\n== STUDY 7 EXTRACTION COMPLETE in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
