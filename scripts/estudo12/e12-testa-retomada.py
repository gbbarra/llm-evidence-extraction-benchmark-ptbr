# -*- coding: utf-8 -*-
"""Testa o portão de retomada e a escrita atômica do harness. Sem chamar modelo nenhum.

A instrução do pesquisador — "faça de forma que se for interrompido possamos continuar de onde parou"
— vira, no harness, três mecanismos: portão por integridade, escrita atômica e registro por chamada.
Nenhum dos três foi exercitado por uma corrida ainda, e uma campanha de 37 horas não é lugar para
descobrir que um deles não funciona.

Este teste monta arquivos de saída falsos, em diretório temporário, e verifica que o portão aceita o
que deve aceitar e recusa o que deve recusar, e que a escrita atômica nunca deixa arquivo pela metade
no lugar do bom. Os oito casos abaixo são os modos de falha que uma interrupção real produz.
"""
import importlib.util
import io
import json
import os
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("h12", AQUI / "e12-harness.py")
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)

BOM = dict(modelo="gemma12", tag="gemma4:12b", ancora="a3", ficha="v1", ensaio="dong2025",
           replica=1, conteudo='{"study": {"value": "Dong 2025"}}', prompt_tokens=15581,
           tokens=412, finish="stop", dt=167.4, num_ctx=24576, num_predict=4000,
           sha_prompt="a" * 64)

CASOS = [
    ("saída boa", BOM, True, ""),
    ("truncada pelo teto", dict(BOM, finish="length"), False, "truncada"),
    ("conteúdo vazio", dict(BOM, conteudo=""), False, "vazio"),
    ("conteúdo só espaços", dict(BOM, conteudo="   \n "), False, "vazio"),
    ("sem o campo finish", {k: v for k, v in BOM.items() if k != "finish"}, False, "faltam campos"),
    ("sem os tokens de entrada", {k: v for k, v in BOM.items() if k != "prompt_tokens"}, False, "faltam campos"),
    ("sem o selo do prompt", {k: v for k, v in BOM.items() if k != "sha_prompt"}, False, "faltam campos"),
]

ok = True


def diz(rot, passou, detalhe=""):
    global ok
    ok = ok and passou
    print(f"  {'ok  ' if passou else 'ERRO'} {rot:44s} {detalhe}")


with tempfile.TemporaryDirectory() as td:
    d = Path(td)
    print("1. o portão aceita o bom e recusa cada modo de falha")
    for rot, obj, esperado, pedaco in CASOS:
        p = d / "caso.json"
        io.open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False))
        got, motivo = H.integro(p)
        bate = got == esperado and (esperado or pedaco in motivo)
        diz(rot, bate, "aceita" if got else f"recusa: {motivo}")

    print("\n2. o portão recusa arquivo corrompido por interrupção no meio da escrita")
    inteiro = json.dumps(BOM, ensure_ascii=False)
    for frac, rot in ((0.5, "metade do arquivo"), (0.9, "quase inteiro"), (0.02, "só o começo")):
        p = d / "parcial.json"
        io.open(p, "w", encoding="utf-8").write(inteiro[:int(len(inteiro) * frac)])
        got, motivo = H.integro(p)
        diz(rot, not got, f"recusa: {motivo[:44]}")

    print("\n3. a escrita atômica não deixa parcial no lugar do bom")
    p = d / "alvo.json"
    H.grava(p, BOM)
    diz("grava e o arquivo abre", H.integro(p)[0])
    antes = io.open(p, encoding="utf-8").read()

    # uma carga que o json escreve pela metade e depois recusa: 5 KB de texto bom seguidos de um
    # objeto não serializável. A primeira versão deste teste usava um dict com keys() explodindo, e
    # o json ignorava o override -- a escrita nem chegava a falhar, e o teste passava por engano.
    explode = {"a": "x" * 5000, "b": object()}
    houve_erro = False
    try:
        H.grava(p, explode)
    except TypeError:
        houve_erro = True
    diz("a escrita realmente falhou (senão o teste não testa nada)", houve_erro)
    depois = io.open(p, encoding="utf-8").read()
    diz("o arquivo bom sobrevive à escrita que falhou", antes == depois)
    sobras = [x for x in os.listdir(d) if x.endswith(".parcial")]
    diz("nenhum temporário deixado para trás", not sobras, f"sobrou: {sobras}" if sobras else "")

    print("\n4. o afastamento preserva o recusado e anota o motivo")
    origem = d / "a3" / "v1" / "gemma12" / "dong2025-r1.json"
    origem.parent.mkdir(parents=True, exist_ok=True)
    io.open(origem, "w", encoding="utf-8").write(json.dumps(dict(BOM, finish="length")))
    rec_antes = H.RECUSADOS
    H.RECUSADOS = d / "recusados"
    H.afasta(origem, "saída truncada pelo teto (done_reason=length)")
    achados = sorted(x.name for x in (d / "recusados").iterdir())
    H.RECUSADOS = rec_antes
    diz("o arquivo saiu do caminho", not origem.exists())
    diz("foi preservado, não apagado", any(x.endswith(".json") for x in achados), str(achados))
    diz("o motivo foi gravado ao lado", any(x.endswith(".motivo") for x in achados))

print("\n5. o plano bate com o protocolo")
todas = list(H.plano())
por_ancora = {}
for c in todas:
    por_ancora[c["ancora"]] = por_ancora.get(c["ancora"], 0) + 1
diz("696 chamadas ao todo", len(todas) == 696, f"{len(todas)}")
diz("âncora 1: 14 ensaios × 2 réplicas × 2 fichas × 6 modelos", por_ancora.get("a1") == 336, f"{por_ancora.get('a1')}")
diz("âncora 2: 7 × 2 × 2 × 6", por_ancora.get("a2") == 168, f"{por_ancora.get('a2')}")
diz("âncora 3: 8 × 2 × 2 × 6", por_ancora.get("a3") == 192, f"{por_ancora.get('a3')}")
diz("um modelo residente por vez (o elenco não se intercala)",
    [c["modelo"] for c in todas] == sorted([c["modelo"] for c in todas],
                                           key=lambda m: H.ELENCO.index(m)))
diz("contexto 24.576", H.CTX == 24576)
diz("e3-harness continua em 16.384, intocado", H.h3.CTX == 16384, f"h3.CTX={H.h3.CTX}")
diz("nenhum destino se repete", len({str(H.destino(c)) for c in todas}) == len(todas))

print("\n" + "=" * 74)
print("RETOMADA VERIFICADA" if ok else "FALHOU — não rodar a campanha")
print("=" * 74)
sys.exit(0 if ok else 1)
