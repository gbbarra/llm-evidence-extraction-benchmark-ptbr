# -*- coding: utf-8 -*-
"""O harness da campanha do Estudo 12. Instrumentos 1 a 4 da §8.

Por que existe um harness novo, em vez de um argumento a mais no antigo. O contexto desta campanha é
24.576, e o único lugar onde o contexto vive hoje é `CTX = 16384`, uma constante de módulo em
`scripts/estudo3/e3-harness.py` que sete estudos registrados importam, direta ou indiretamente. Mudar
lá redefiniria em silêncio a configuração declarada de todos eles. Então o transporte é reusado — a
mesma função HTTP, o mesmo tempo limite — e as opções da chamada são deste módulo.

Os quatro instrumentos:

  1. contexto próprio      num_ctx 24.576 no corpo do pedido, sem tocar em e3-harness.py
  2. portão de retomada    por CHAMADA, e por integridade, não por existência. Um arquivo que não
                           abre, que não tem os campos previstos, ou que foi truncado pelo teto de
                           saída (done_reason == "length") não conta como feito: sai do caminho com o
                           motivo anotado e a chamada é refeita.
  3. escrita atômica       arquivo temporário e rename. Nenhum script do repositório fazia isso, e
                           escrita direta atrás de um portão de existência é uma janela em que uma
                           interrupção deixa meio arquivo que a retomada aceita como pronto.
  4. registro por chamada  modelo, tag, âncora, ficha, ensaio, réplica, tokens de entrada e de saída,
                           done_reason, duração e o SHA-256 do prompt efetivamente enviado. O caminho
                           de orquestração descartava tudo isso, e por isso truncamento nunca foi
                           detectável depois do fato.

A regra de operação do pesquisador — "faça de forma que se for interrompido possamos continuar de onde
parou" — é o que os instrumentos 2, 3 e 4 servem. Interromper com Ctrl-C custa, no máximo, a chamada
em curso.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent

CTX = 24576                     # §3 do protocolo, congelado
SAIDA = {"v1": 4000, "v2": 8000}
REPLICAS = 2
CAMPOS_OBRIGATORIOS = ("modelo", "tag", "ancora", "ficha", "ensaio", "replica",
                       "conteudo", "prompt_tokens", "tokens", "finish", "dt", "sha_prompt")


def _carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# O registro de modelos é montado em três camadas, e a ordem importa. `e4-extensao.py` injeta os três
# modelos do Estudo 4 no h3 QUE ELE MESMO CARREGOU -- um objeto de módulo próprio, porque cada
# importlib cria um novo. Carregar o e3-harness por conta e esperar que a injeção apareça nele é o
# defeito que fazia quatro dos seis modelos do elenco sumirem: a campanha rodaria gemma12 e qwen14 e
# depois gravaria 464 arquivos de erro em segundos, terminando com código zero. O e9-extract, que de
# fato rodou, faz a coisa certa: pega `ext.h3`. E o sexto modelo não se injeta sozinho -- o
# e8-amend1-cast só define `registrar(h3)`, que precisa ser chamado.
_ext = _carrega("ext", RAIZ / "scripts" / "estudo4" / "e4-extensao.py")
h3 = _ext.h3                                                             # o h3 que a extensão mutou
_am1 = _carrega("am1", RAIZ / "scripts" / "estudo8" / "e8-amend1-cast.py")
_am1.registrar(h3)                                                       # e o sexto leitor

# §3 do protocolo: o elenco, e a ordem do elenco é a ordem das corridas
ELENCO = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14", "qwen27q2"]

_faltam = [m for m in ELENCO if m not in h3.MODELS]
if _faltam:
    raise SystemExit(f"elenco incompleto no registro do harness: {_faltam}. "
                     f"Registrados: {sorted(h3.MODELS)}. A campanha não pode começar.")

ANCORAS = {
    "a1": dict(corpus=[RAIZ / "corpus" / "perturbados", RAIZ / "corpus" / "perturbados-fechados"],
               fichas={"v1": RAIZ / "dados" / "instruments-en" / "estudo1" / "t1-extraction.txt",
                       "v2": RAIZ / "dados" / "estudo9" / "prompts" / "t1-extraction-v2.txt"}),
    "a2": dict(corpus=[RAIZ / "corpus" / "estudo3" / "perturbados"],
               fichas={"v1": RAIZ / "dados" / "instruments-en" / "estudo3" / "e3-extraction.txt",
                       "v2": RAIZ / "dados" / "estudo9" / "prompts" / "e3-extraction-v2.txt"}),
    "a3": dict(corpus=[RAIZ / "corpus" / "estudo12" / "perturbados"],
               fichas={"v1": RAIZ / "dados" / "estudo12" / "prompts" / "a3-extraction.txt",
                       "v2": RAIZ / "dados" / "estudo12" / "prompts" / "a3-extraction-v2.txt"}),
}
SAIDAS = RAIZ / "dados" / "estudo12" / "saidas"
RECUSADOS = RAIZ / "dados" / "estudo12" / "recusados"


# ------------------------------------------------------------------ o plano, enumerado
def ensaios(ancora):
    fora = []
    for d in ANCORAS[ancora]["corpus"]:
        fora += [(p.stem, p) for p in sorted(d.glob("*.txt"))]
    return fora


def plano():
    """As chamadas da campanha, na ordem em que rodam. Um modelo residente por vez."""
    for modelo in ELENCO:
        for ancora in ("a1", "a2", "a3"):
            for ficha in ("v1", "v2"):
                for tid, caminho in ensaios(ancora):
                    for rep in range(1, REPLICAS + 1):
                        yield dict(modelo=modelo, ancora=ancora, ficha=ficha,
                                   ensaio=tid, replica=rep, caminho=caminho)


def destino(c):
    return SAIDAS / c["ancora"] / c["ficha"] / c["modelo"] / f"{c['ensaio']}-r{c['replica']}.json"


# ------------------------------------------------------------------ instrumento 2: portão por integridade
def integro(p):
    """(ok, motivo). Existir não basta: tem de abrir, ter os campos e não ter sido truncado."""
    try:
        j = json.loads(io.open(p, encoding="utf-8").read())
    except Exception as e:
        return False, f"não abre como JSON: {type(e).__name__}"
    faltam = [c for c in CAMPOS_OBRIGATORIOS if c not in j]
    if faltam:
        return False, "faltam campos: " + ", ".join(faltam)
    if j.get("finish") == "length":
        return False, "saída truncada pelo teto (done_reason=length)"
    if not str(j.get("conteudo", "")).strip():
        return False, "conteúdo vazio"
    return True, ""


def afasta(p, motivo):
    """Recusado é registrado, não apagado."""
    RECUSADOS.mkdir(parents=True, exist_ok=True)
    alvo = RECUSADOS / f"{p.parent.parent.parent.name}-{p.parent.parent.name}-{p.parent.name}-{p.name}"
    i = 0
    while alvo.exists():
        i += 1
        alvo = alvo.with_suffix(f".{i}.json")
    os.replace(p, alvo)
    io.open(alvo.with_suffix(alvo.suffix + ".motivo"), "w", encoding="utf-8").write(motivo + "\n")


# ------------------------------------------------------------------ instrumento 3: escrita atômica
def grava(p, obj):
    """Temporário no mesmo diretório e rename. Rename é atômico; escrita não é."""
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), suffix=".parcial")
    try:
        with io.open(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ------------------------------------------------------------------ instrumentos 1 e 4: a chamada
def descarrega(tag=None):
    for t in ([tag] if tag else sorted({m["ollama"] for m in h3.MODELS.values()})):
        subprocess.run(["ollama", "stop", t], capture_output=True)


def monta(tpl, texto):
    return tpl.replace("{ARTICLE}", texto) if "{ARTICLE}" in tpl else tpl + texto


def chama(c, prompt):
    m = h3.MODELS[c["modelo"]]
    opts = dict(num_predict=SAIDA[c["ficha"]], num_ctx=CTX)
    if m["cpu"]:
        opts["num_gpu"] = 0
    body = dict(model=m["ollama"], prompt=prompt, stream=False, think=False, options=opts)
    r, dt = h3.post_json(h3.OLLAMA + "/api/generate", body)
    if r.get("error"):
        raise RuntimeError(r["error"])
    return dict(modelo=c["modelo"], tag=m["ollama"], ancora=c["ancora"], ficha=c["ficha"],
                ensaio=c["ensaio"], replica=c["replica"],
                conteudo=r.get("response", "") or "",
                prompt_tokens=r.get("prompt_eval_count", 0), tokens=r.get("eval_count", 0),
                finish=r.get("done_reason"), dt=round(r.get("total_duration", 0) / 1e9 or dt, 2),
                num_ctx=CTX, num_predict=SAIDA[c["ficha"]],
                sha_prompt=hashlib.sha256(prompt.encode("utf-8")).hexdigest())


# ------------------------------------------------------------------ a corrida
def roda(so_modelo=None, so_ancora=None, so_ficha=None, seco=False):
    todas = [c for c in plano()
             if (not so_modelo or c["modelo"] == so_modelo)
             and (not so_ancora or c["ancora"] == so_ancora)
             and (not so_ficha or c["ficha"] == so_ficha)]
    print(f"plano: {len(todas)} chamadas · contexto {CTX} · saída {SAIDA}")
    residente, feitas, puladas, refeitas, erros = None, 0, 0, 0, 0
    t0 = time.time()
    for i, c in enumerate(todas, 1):
        p = destino(c)
        if p.exists():
            ok, motivo = integro(p)
            if ok:
                puladas += 1
                continue
            print(f"  [{i}/{len(todas)}] {p.name}: RECUSADO — {motivo}", flush=True)
            afasta(p, motivo)
            refeitas += 1
        if seco:
            feitas += 1
            continue
        if residente != c["modelo"]:
            if residente:
                descarrega(h3.MODELS[residente]["ollama"])
            residente = c["modelo"]
            print(f"\n=== modelo residente: {residente} ({h3.MODELS[residente]['ollama']})", flush=True)
        tpl = io.open(ANCORAS[c["ancora"]]["fichas"][c["ficha"]], encoding="utf-8").read()
        prompt = monta(tpl, io.open(c["caminho"], encoding="utf-8").read())
        try:
            r = chama(c, prompt)
        except KeyboardInterrupt:
            print("\ninterrompido. Nada a meio: a chamada em curso não foi gravada.", flush=True)
            raise
        except Exception as e:
            erros += 1
            print(f"  [{i}/{len(todas)}] {c['modelo']} {c['ancora']}/{c['ficha']}/{c['ensaio']}-r"
                  f"{c['replica']}: ERRO {type(e).__name__}: {str(e)[:120]}", flush=True)
            grava(RECUSADOS / f"erro-{c['modelo']}-{c['ancora']}-{c['ficha']}-{c['ensaio']}-r{c['replica']}.json",
                  dict(**{k: c[k] for k in ("modelo", "ancora", "ficha", "ensaio", "replica")},
                       erro=f"{type(e).__name__}: {e}"))
            continue
        grava(p, r)
        feitas += 1
        print(f"  [{i}/{len(todas)}] {c['modelo']:11s} {c['ancora']}/{c['ficha']} {c['ensaio']}-r{c['replica']}"
              f"  {r['prompt_tokens']:6d}+{r['tokens']:5d} tok  {r['dt']:6.1f}s  fim={r['finish']}", flush=True)
    if residente and not seco:
        descarrega(h3.MODELS[residente]["ollama"])
    dt = time.time() - t0
    print(f"\nfeitas {feitas} · já prontas {puladas} · refeitas por integridade {refeitas} · erros {erros}")
    print(f"tempo {dt/60:.1f} min")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="harness da campanha do Estudo 12")
    ap.add_argument("--modelo", choices=ELENCO)
    ap.add_argument("--ancora", choices=("a1", "a2", "a3"))
    ap.add_argument("--ficha", choices=("v1", "v2"))
    ap.add_argument("--seco", action="store_true", help="não chama modelo nenhum; só mostra o plano")
    a = ap.parse_args()
    roda(a.modelo, a.ancora, a.ficha, a.seco)
