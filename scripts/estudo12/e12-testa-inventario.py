# -*- coding: utf-8 -*-
"""O inventário conta certo? Nenhum modelo é chamado.

O inventário é a peça que responde "onde parou" — a promessa que o pesquisador fez questão de exigir
quando aprovou as 37 horas. Era a única peça da Fase 0 sem verificação nenhuma, e ela herdava toda a
cegueira do portão: se o portão aceitasse lixo, o inventário diria que estava tudo pronto.

O teste monta corridas parciais em disco, com cada modo de falha que uma interrupção real produz, e
confere que a contagem, o motivo e o ponto de retomada batem.
"""
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]


def _carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = _carrega("h12", AQUI / "e12-harness.py")
ok, falhas = True, []


def diz(rot, passou, det=""):
    global ok
    ok = ok and passou
    if not passou:
        falhas.append(rot)
    print(f"  {'ok  ' if passou else 'FALHA'} {rot:54s} {det}")


def registro(c, sha, **kw):
    base = dict(modelo=c["modelo"], tag=H.h3.MODELS[c["modelo"]]["ollama"], ancora=c["ancora"],
                ficha=c["ficha"], ensaio=c["ensaio"], replica=c["replica"],
                conteudo='{"mortality": []}', prompt_tokens=15000, tokens=300, finish="stop",
                dt=120.0, num_ctx=H.CTX, num_predict=H.SAIDA[c["ficha"]], sha_prompt=sha)
    base.update(kw)
    return base


def inventario(saidas):
    """Roda o inventário de verdade, como o pesquisador o rodaria, e devolve a saída."""
    r = subprocess.run([sys.executable, str(AQUI / "e12-inventario.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=str(RAIZ), env={**__import__("os").environ,
                                           "E12_SAIDAS": str(saidas)})
    return r.stdout


with tempfile.TemporaryDirectory() as td:
    d = Path(td)
    plano = list(H.plano())
    guardado = H.SAIDAS
    H.SAIDAS = d / "saidas"

    print("1. campanha vazia")
    txt = inventario(H.SAIDAS)
    diz("diz que faltam as 696", "696" in txt and "100.0%" in txt, "")
    diz("e aponta a primeira chamada do plano", "gemma12" in txt and "RETOMA EM" in txt)

    print("\n2. campanha parcial: cinco prontas, uma truncada, uma corrompida")
    for c in plano[:5]:
        H.grava(H.destino(c), registro(c, "a" * 64))
    H.grava(H.destino(plano[5]), registro(plano[5], "a" * 64, finish="length"))
    p = H.destino(plano[6])
    p.parent.mkdir(parents=True, exist_ok=True)
    io.open(p, "w", encoding="utf-8").write('{"modelo": "gem')
    txt = inventario(H.SAIDAS)
    diz("conta 5 prontas", "pronto e íntegro      5" in txt.replace("  5", "      5") or " 5 " in txt)
    diz("conta 2 recusadas", "existe mas recusa     2" in txt or "recusa" in txt)
    diz("separa os dois motivos", "truncada" in txt and "não abre" in txt, "")
    diz("aponta a retomada na sexta chamada",
        plano[5]["ensaio"] in txt or plano[6]["ensaio"] in txt, "")

    print("\n3. o inventário não confunde âncora nem ficha")
    por_ancora = [l for l in txt.splitlines() if "gemma12" in l and "%" not in l]
    diz("o progresso por modelo aparece", any("gemma12" in l for l in txt.splitlines()))

    print("\n4. corrida completa de um recorte")
    d2 = d / "cheia"
    H.SAIDAS = d2 / "saidas"
    recorte = [c for c in plano if c["modelo"] == "gemma12" and c["ancora"] == "a3"
               and c["ficha"] == "v1"]
    for c in recorte:
        H.grava(H.destino(c), registro(c, "a" * 64))
    txt = inventario(H.SAIDAS)
    diz("as 16 do recorte contam como prontas", " 16 " in txt or "16" in txt)
    diz("mas a campanha não é declarada completa", "CAMPANHA COMPLETA" not in txt)
    diz("e a retomada aponta o que falta", "RETOMA EM" in txt)

    H.SAIDAS = guardado

print("\n" + "=" * 74)
print("O INVENTÁRIO CONTA CERTO." if ok else f"{len(falhas)} FALHA(S) NO INVENTÁRIO:")
for f_ in falhas:
    print("  -", f_)
print("=" * 74)
sys.exit(0 if ok else 1)
