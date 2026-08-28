# -*- coding: utf-8 -*-
"""EXTRAI — Estudo 1: harness das três tarefas (T1 extração, T2 RoB, T3 síntese).

Motor idêntico ao do FIEL (Séries 2–3): Ollama /api/generate, contexto 16.384,
thinking desligado, amostragem do fabricante embutida no modelo, num_gpu=0 nos
modelos grandes (teto de memória compartilhada da 780M, decisão do E12/FIEL).

Fila por modelo (ordem: mais rápidos primeiro, decisão do autor) e, por primário,
T1r1 → T1r2 → T2r1 → T2r2 — o artigo vem antes das instruções, então as quatro
corridas reaproveitam o prefixo KV. T3 roda ao fim do bloco do modelo, sobre as
extrações T1-r1 dele mesmo.

Uso:
  python e1-harness.py run [--models gemma12,qwen14,gemma26,qwen38]
                           [--tasks t1,t2,t3] [--reps 2]
  python e1-harness.py smoke          # 1 corrida T1 (gemma12, menor primário)

Saídas: dados/estudo1/saidas/<modelo>/<pmcid>-<tarefa>-r<n>.json
(fora do repositório até a correção — contêm os valores perturbados)
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
OLLAMA = "http://localhost:11434"
CTX = 16384

# ordem da fila = ordem de inserção (mais rápidos primeiro, pedido do autor)
MODELS = {
    "gemma12": dict(ollama="gemma4:12b", cpu=False),
    "qwen14":  dict(ollama="qwen3:14b", cpu=False),
    "gemma26": dict(ollama="gemma4:26b", cpu=True),
    "qwen38":  dict(ollama="qwen3.8:27b-texto", cpu=True),
}
MAX_TOKENS = {"t1": 2200, "t2": 1400, "t3": 900}
DIR_PERT = RAIZ / "corpus" / "perturbados"      # Emenda 2: sobrescrito por --pert-dir
DIR_PROMPTS = RAIZ / "dados" / "estudo1" / "prompts"
DIR_OUT = RAIZ / "dados" / "estudo1" / "saidas"


def rotulos():
    prim = json.loads((RAIZ / "corpus" / "primarios" / "primarios.json").read_text(encoding="utf-8"))
    r = {}
    for p in prim:
        if p.get("xml_baixado"):
            sobrenome = (p.get("autores") or "?").split()[0].rstrip(",")
            r[p["pmcid"]] = f"{sobrenome} et al., {p.get('ano', '?')}"
    return r


def primarios():
    return sorted(DIR_PERT.glob("*.txt"))


def prompt_artigo(tarefa, pmcid):
    tpl = (DIR_PROMPTS / ("t1-extracao.txt" if tarefa == "t1" else "t2-rob.txt")).read_text(encoding="utf-8")
    artigo = (DIR_PERT / f"{pmcid}.txt").read_text(encoding="utf-8")
    return tpl.replace("{ARTIGO}", artigo)


def prompt_t3(model):
    rots = rotulos()
    blocos = []
    for p in primarios():
        pmcid = p.stem
        f = DIR_OUT / model / f"{pmcid}-t1-r1.json"
        if not f.exists():
            raise RuntimeError(f"T3 requer T1-r1 de {pmcid} (não encontrado)")
        content = json.loads(f.read_text(encoding="utf-8"))["content"]
        blocos.append(f"=== ENSAIO {pmcid} ({rots.get(pmcid, '?')}) ===\n{content.strip()}")
    tpl = (DIR_PROMPTS / "t3-sintese.txt").read_text(encoding="utf-8")
    return tpl.replace("{EXTRACOES}", "\n\n".join(blocos))


def post_json(url, body, timeout=3600):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=timeout))
    return r, time.time() - t0


def run_ollama(model, prompt, max_tokens):
    m = MODELS[model]
    opts = dict(num_predict=max_tokens, num_ctx=CTX)
    if m["cpu"]:
        opts["num_gpu"] = 0
    body = dict(model=m["ollama"], prompt=prompt, stream=False, think=False, options=opts)
    r, dt = post_json(OLLAMA + "/api/generate", body)
    if r.get("error"):
        raise RuntimeError(r["error"])
    return dict(content=r.get("response", "") or "", reasoning=r.get("thinking", "") or "",
                finish=r.get("done_reason"), tokens=r.get("eval_count", 0),
                dt=r.get("total_duration", 0) / 1e9 or dt,
                prompt_tokens=r.get("prompt_eval_count", 0))


def medir(model, tarefa, replica, pmcid, prompt, outdir):
    nome = f"{pmcid}-{tarefa}-r{replica}.json" if pmcid else f"{tarefa}-r{replica}.json"
    out = outdir / nome
    if out.exists():
        print(f"  pulando (já feito): {model} {nome}", flush=True)
        return
    t0 = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        r = run_ollama(model, prompt, MAX_TOKENS[tarefa])
        registro = dict(modelo=model, ollama=MODELS[model]["ollama"], pmcid=pmcid,
                        tarefa=tarefa, replica=replica, inicio=t0, **r)
        out.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {model} {nome}: {r['dt']:.0f}s, {r['prompt_tokens']}+{r['tokens']} tok, fim={r['finish']}", flush=True)
    except Exception as e:
        (outdir / (nome + ".erro")).write_text(f"{t0}\n{e}", encoding="utf-8")
        print(f"  ERRO {model} {nome}: {str(e)[:200]}", flush=True)


def fila(models, tasks, reps):
    t_ini = time.time()
    for model in models:
        outdir = DIR_OUT / model
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"\n=== {model} ({MODELS[model]['ollama']}) — {time.strftime('%H:%M')} ===", flush=True)
        for p in primarios():
            pmcid = p.stem
            for tarefa in [t for t in ("t1", "t2") if t in tasks]:
                for rep in range(1, reps + 1):
                    medir(model, tarefa, rep, pmcid, prompt_artigo(tarefa, pmcid), outdir)
        if "t3" in tasks:
            try:
                medir(model, "t3", 1, None, prompt_t3(model), outdir)
            except RuntimeError as e:
                print(f"  T3 pulada: {e}", flush=True)
    print(f"\nFILA CONCLUÍDA em {(time.time()-t_ini)/3600:.1f} h.", flush=True)


def main():
    global DIR_PERT
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "smoke"])
    ap.add_argument("--models", default="gemma12,qwen14,gemma26,qwen38")
    ap.add_argument("--tasks", default="t1,t2,t3")
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--pert-dir", default=None,
                    help="diretório dos perturbados (Emenda 2: corpus/perturbados-fechados)")
    a = ap.parse_args()
    if a.pert_dir:
        DIR_PERT = RAIZ / a.pert_dir

    if a.cmd == "smoke":
        outdir = DIR_OUT / "smoke-gemma12"
        outdir.mkdir(parents=True, exist_ok=True)
        menor = min(primarios(), key=lambda p: p.stat().st_size).stem
        print(f"smoke: gemma12 T1 em {menor}", flush=True)
        medir("gemma12", "t1", 1, menor, prompt_artigo("t1", menor), outdir)
        return
    fila([m.strip() for m in a.models.split(",")], a.tasks.split(","), a.reps)


if __name__ == "__main__":
    main()
