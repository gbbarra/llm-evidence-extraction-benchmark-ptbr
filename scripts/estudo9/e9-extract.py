# -*- coding: utf-8 -*-
"""EXTRAI Study 9 — the quote-bearing sheet (schema v2), A/B against frozen v1.

Protocol: dados/estudo9/protocolo-estudo9.md (amendments A9-1..A9-3).

Runs one model over both anchors under a chosen schema:
  v2 = {"value","where","quote"}  (arm A, the new instruments)
  v1 = {"value","where"}          (arm B; only granite4.2:8b needs new v1 runs,
                                   the other three have archived campaign records)

Per A9-3 the cast is gemma12, qwen14, llama8, granite8; granite runs BOTH arms.
Token allowance: 8000 for v2 (declared raise, v2 sheets are larger by design),
4000 for v1 (the campaign's frozen allowance, so arm B stays comparable).

Run:  python scripts/estudo9/e9-extract.py <model> <v1|v2> [ma1|ma2]
Out:  dados/estudo9/saidas/<schema>/<model>/{ma1,ma2}/<trial>-r{1,2}.json
Resume-safe: existing files are skipped.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E8, E9 = ROOT / "dados" / "estudo8", ROOT / "dados" / "estudo9"
MA1_ABERTOS = ROOT / "corpus" / "perturbados"
MA1_FECHADOS = ROOT / "corpus" / "perturbados-fechados"
MA2_PERT = ROOT / "corpus" / "estudo3" / "perturbados"

_x = importlib.util.spec_from_file_location("ext", ROOT / "scripts" / "estudo4" / "e4-extensao.py")
ext = importlib.util.module_from_spec(_x)
_x.loader.exec_module(ext)
h3 = ext.h3

# A9-3: granite4.2:8b joins the registry (never in the campaign; both arms here)
h3.MODELS.setdefault("granite8", dict(ollama="granite4.2:8b", cpu=False))

MAXTOK = {"v1": 4000, "v2": 8000}
PROMPTS = {
    ("v1", "ma1"): E8 / "prompts" / "t1-extraction.txt",
    ("v1", "ma2"): E8 / "prompts" / "e3-extraction.txt",
    ("v2", "ma1"): E9 / "prompts" / "t1-extraction-v2.txt",
    ("v2", "ma2"): E9 / "prompts" / "e3-extraction-v2.txt",
}


def descarrega(tag=None):
    tags = [tag] if tag else sorted({m["ollama"] for m in h3.MODELS.values()})
    for t in tags:
        subprocess.run(["ollama", "stop", t], capture_output=True)


def primarios(ancora):
    if ancora == "ma1":
        return ([(p.stem, p) for p in sorted(MA1_ABERTOS.glob("*.txt"))]
                + [(p.stem, p) for p in sorted(MA1_FECHADOS.glob("*.txt"))])
    return [(p.stem, p) for p in sorted(MA2_PERT.glob("*.txt"))]


def monta(tpl, texto):
    """MA-1 sheets carry a {ARTICLE} placeholder; MA-2 sheets append the text."""
    return tpl.replace("{ARTICLE}", texto) if "{ARTICLE}" in tpl else tpl + texto


def previa(bruto, esquema):
    """A short, honest window on what the model actually wrote, for the terminal.

    Never parses for grading here — grading is a separate, later, frozen step.
    """
    js = h3.acha_json(bruto) if hasattr(h3, "acha_json") else None
    if js is None:
        m = re.search(r"\{.*\}", bruto, re.S)
        try:
            js = json.loads(m.group(0)) if m else None
        except Exception:
            js = None
    if not isinstance(js, dict):
        return "      [unparseable at preview time -- kept raw for the grader]"

    def celulas(obj, prefixo=""):
        """MA-2 sheets nest cells inside arm objects; MA-1 sheets are flat."""
        for campo, v in obj.items():
            if not isinstance(v, dict):
                continue
            if "value" in v:
                yield prefixo + campo, v
            else:
                yield from celulas(v, campo.replace("_arm", "") + ".")

    todas = list(celulas(js))
    if not todas:
        return "      [no {value,...} cells found at preview time]"
    linhas = []
    preenchidas = [(c, v) for c, v in todas
                   if str(v.get("value", "")).strip() not in ("", "NR")]
    for campo, v in preenchidas[:3]:
        val = str(v.get("value", ""))[:44]
        onde = str(v.get("where", ""))[:26]
        linhas.append(f"      {campo[:30]:<30} = {val}")
        if esquema == "v2":
            q = str(v.get("quote", "")).strip()
            linhas.append(f"         where: {onde} | quote: "
                          + (f"“{q[:58]}…”" if q else "(EMPTY)"))
        else:
            linhas.append(f"         where: {onde}")
    n_q = sum(1 for _, v in preenchidas if str(v.get("quote", "")).strip())
    linhas.append(f"      ({len(todas)} cells, {len(preenchidas)} filled"
                  + (f", {n_q} of those quoted)" if esquema == "v2" else ")"))
    return "\n".join(linhas)


def roda(modelo, esquema, ancora):
    tpl = PROMPTS[(esquema, ancora)].read_text(encoding="utf-8")
    out_dir = E9 / "saidas" / esquema / modelo / ancora
    out_dir.mkdir(parents=True, exist_ok=True)
    lista = primarios(ancora)
    tag = h3.MODELS[modelo]["ollama"]
    print(f"\n===== Study 9 · {esquema.upper()} · {ancora.upper()} · {modelo} [{tag}] · "
          f"{len(lista)} primaries x 2 · allowance {MAXTOK[esquema]} tok", flush=True)
    feitos = 0
    for tid, caminho in lista:
        prompt = monta(tpl, caminho.read_text(encoding="utf-8"))
        for rep in (1, 2):
            out = out_dir / f"{tid}-r{rep}.json"
            if out.exists():
                print(f"  skip {tid}-r{rep} (already done)", flush=True)
                continue
            r = h3.gerar(modelo, prompt, max_tokens=MAXTOK[esquema])
            out.write_text(json.dumps(dict(modelo=modelo, esquema=esquema, ancora=ancora,
                                           trial=tid, replica=rep, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            feitos += 1
            print(f"  {tid}-r{rep}: {r['dt']:.0f}s · {r['tokens']} tok · finish={r['finish']}",
                  flush=True)
            print(previa(r.get("content", ""), esquema), flush=True)
    return feitos


def main():
    if len(sys.argv) < 3:
        sys.exit("uso: e9-extract.py <model> <v1|v2> [ma1|ma2]")
    modelo, esquema = sys.argv[1], sys.argv[2]
    ancoras = [sys.argv[3]] if len(sys.argv) > 3 else ["ma1", "ma2"]
    if modelo not in h3.MODELS:
        sys.exit(f"modelo desconhecido: {modelo} (conhecidos: {sorted(h3.MODELS)})")
    if esquema not in ("v1", "v2"):
        sys.exit("esquema deve ser v1 ou v2")

    for selo in ("estudo1/perturbacoes-estudo1.json", "estudo1/perturbacoes-fechados.json",
                 "estudo1/perturbacoes-manuais.json", "estudo1/perturbacoes-fechados-manuais.json",
                 "estudo3/perturbacoes-estudo3.json"):
        p = ROOT / "dados" / selo
        if p.exists():
            print(f"SHA-256 {Path(selo).name}: {hashlib.sha256(p.read_bytes()).hexdigest()}",
                  flush=True)
    for k, v in PROMPTS.items():
        if k[0] == esquema:
            print(f"SHA-256 {v.name}: {hashlib.sha256(v.read_bytes()).hexdigest()}", flush=True)

    descarrega()
    t0 = time.time()
    total = sum(roda(modelo, esquema, a) for a in ancoras)
    descarrega(h3.MODELS[modelo]["ollama"])
    print(f"\n== {modelo} {esquema} COMPLETE: {total} new calls in "
          f"{(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
