# -*- coding: utf-8 -*-
"""A costura P1 → P2 → P3, ponta a ponta. Nenhum modelo é chamado.

Este era o maior buraco da Fase 0 depois da revisão adversarial: o harness gravava num formato, o
corretor esperava outro, e **nada no repositório ligava os dois**. Cada um passava no seu autoteste
com fichas que ele mesmo fabricava. A primeira vez que os dois formatos se encontrariam de verdade
seria depois de 37 horas de campanha — e um desencontro ali não custa uma correção, custa a campanha.

O teste faz o caminho inteiro sem chamar modelo nenhum:

  P1  intercepta o transporte do harness e devolve, no lugar da resposta do Ollama, a ficha de um
      leitor definido pelo teste. Tudo o mais é o harness de verdade: o mesmo plano, o mesmo portão,
      a mesma escrita atômica, o mesmo registro por chamada.
  P2  lê os arquivos que o harness gravou — não fichas fabricadas — e os corrige.
  P3  agrupa as células corrigidas e compara com o diamante da camada 2.

Três leitores, escolhidos para separar o que a campanha precisa distinguir: o que lê certo, o que
recita, e o que devolve lixo.
"""
import importlib.util
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent


def _carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = _carrega("h12", AQUI / "e12-harness.py")
A = _carrega("av12", AQUI / "e12-avalia-a3.py")
GAB, SELO = A.GAB, A.SELO

ok, falhas = True, []


def diz(rot, passou, det=""):
    global ok
    ok = ok and passou
    if not passou:
        falhas.append(rot)
    print(f"  {'ok  ' if passou else 'FALHA'} {rot:54s} {det}")


def ficha_de(tid, modo):
    """A ficha que o leitor devolveria, em JSON, como um modelo devolveria."""
    f = GAB["bracos_da_fonte"][tid]
    s = {r["original"]: r["perturbado"] for r in (SELO.get(tid) or [])}
    linhas = []
    for b in f["bracos"]:
        n_lido = s.get(str(b["n"]), str(b["n"]))          # o que está no corpus perturbado
        n = str(b["n"]) if modo == "recita" else n_lido   # o recitador devolve o original
        linhas.append({"arm_label": {"value": b["rotulo_fonte"], "where": "Table 1"},
                       "timepoint": {"value": f["janela"], "where": "Results"},
                       "deaths": {"value": str(b["eventos"]), "where": "Table 2"},
                       "n": {"value": n, "where": "Table 2"},
                       "deaths_percent": {"value": "NR", "where": ""}})
    return json.dumps({"study": {"value": f["ensaio"]}, "arms": [], "mortality": linhas},
                      ensure_ascii=False)


def roda_p1(destino, modo):
    """A P1 de verdade, com o transporte interceptado. O harness não sabe que não há Ollama."""
    chamadas = {"n": 0}

    # o ensaio é identificado pelo CORPUS que está dentro do prompt, e não pelo nome do autor: a
    # primeira versão procurava "Dong" no prompt e casava com a lista de referências de outros
    # artigos, devolvendo a ficha do ensaio errado. Foi o teste que errou, não o código — mas o
    # sintoma (21/32 e três ensaios sem célula) era indistinguível de um defeito de verdade.
    corpora = {t: io.open(H.ANCORAS["a3"]["corpus"][0] / f"{t}.txt", encoding="utf-8").read()
               for t in GAB["celulas"]}

    def falso_post(url, body, timeout=7200):
        chamadas["n"] += 1
        prompt = body["prompt"]
        candidatos = [t for t, txt in corpora.items() if txt[:2000] in prompt]
        if len(candidatos) != 1:
            raise AssertionError(f"o prompt casou {len(candidatos)} corpora: {candidatos}")
        tid = candidatos[0]
        resposta = "isto não é JSON nenhum" if modo == "lixo" else ficha_de(tid, modo)
        return {"response": resposta, "done_reason": "stop", "prompt_eval_count": 15000,
                "eval_count": 300, "total_duration": 120 * 10 ** 9}, 120.0

    guardado_post, guardado_stop = H.h3.post_json, H.subprocess.run
    guardado_saidas, guardado_rec = H.SAIDAS, H.RECUSADOS
    H.h3.post_json = falso_post
    H.subprocess.run = lambda *a, **k: None
    H.SAIDAS, H.RECUSADOS = destino / "saidas", destino / "recusados"
    H.TRAVA = destino / "harness.trava"      # roda() toma a trava; a do teste e a sua
    try:
        H.roda(so_modelo="gemma12", so_ancora="a3", so_ficha="v1")
    finally:
        H.h3.post_json, H.subprocess.run = guardado_post, guardado_stop
        H.SAIDAS, H.RECUSADOS = guardado_saidas, guardado_rec
    return chamadas["n"]


with tempfile.TemporaryDirectory() as td:
    d = Path(td)

    print("1. P1 — o harness roda a âncora 3 com um leitor que LÊ o corpus perturbado")
    n = roda_p1(d, "le")
    arquivos = sorted((d / "saidas" / "a3" / "v1" / "gemma12").glob("*.json"))
    diz("16 chamadas (8 ensaios × 2 réplicas)", n == 16, f"{n} chamadas")
    diz("16 arquivos gravados", len(arquivos) == 16, f"{len(arquivos)} arquivos")
    if arquivos:
        j = json.loads(io.open(arquivos[0], encoding="utf-8").read())
        diz("o registro por chamada tem os doze campos",
            all(k in j for k in H.CAMPOS_OBRIGATORIOS), f"{sorted(set(H.CAMPOS_OBRIGATORIOS) - set(j))}")
        diz("e registra o contexto realmente enviado", j.get("num_ctx") == 24576, str(j.get("num_ctx")))

    print("\n2. retomar não refaz nada, e é o teste da promessa ao pesquisador")
    n2 = roda_p1(d, "le")
    diz("a segunda passada não chama o modelo nenhuma vez", n2 == 0, f"{n2} chamadas")

    print("\n3. P2 — o CORRETOR lê os arquivos que o harness gravou, não fichas fabricadas")
    r = A.corrige_corrida(d / "saidas", "gemma12", "v1")
    diz("os oito ensaios foram lidos", not r["faltam"], f"faltam {r['faltam']}")
    diz("nenhum arquivo deu problema de leitura", not r["problemas"], str(r["problemas"][:1]))
    diz("a réplica 2 foi guardada, não descartada", len(r["replicas"]) == 8, f"{len(r['replicas'])}")
    acertos = sum(1 for f_ in r["fichas"].values() for c in f_["celulas"].values() if c["acerta"])
    diz("32 de 32 células", acertos == 32, f"{acertos}/32")
    diz("o registro da chamada acompanha a ficha corrigida",
        all(f_["chamada"]["modelo"] == "gemma12" for f_ in r["fichas"].values()))

    print("\n4. P3 — e o diamante é o da camada 2")
    p = r["pool"]
    diz("OR 0,484 [0,319; 0,735]", p and p["dl"] and p["dl"]["or"] == 0.484
        and p["dl"]["ic95"] == [0.319, 0.735], str(p["dl"]) if p else "")
    diz("nenhum ensaio descartado", p and not p["descartados"], str(p["descartados"]) if p else "")
    diz("nenhuma recitação acusada num leitor honesto",
        not any(f_["recitacao"] for f_ in r["fichas"].values()),
        str([t for t, f_ in r["fichas"].items() if f_["recitacao"]]))

    print("\n5. o mesmo caminho com um leitor que RECITA o denominador original")
    d2 = d / "recitador"
    roda_p1(d2, "recita")
    r2 = A.corrige_corrida(d2 / "saidas", "gemma12", "v1")
    acusados = [t for t, f_ in r2["fichas"].items() if f_["recitacao"]]
    diz("a rede acusa nos cinco ensaios selados", len(acusados) == 5, str(sorted(acusados)))
    ac2 = sum(1 for f_ in r2["fichas"].values() for c in f_["celulas"].values() if c["acerta"])
    diz("e as células ainda passam — a rede avisa, não substitui", ac2 == 32, f"{ac2}/32")

    print("\n6. o mesmo caminho com um leitor que devolve LIXO")
    d3 = d / "lixo"
    roda_p1(d3, "lixo")
    r3 = A.corrige_corrida(d3 / "saidas", "gemma12", "v1")
    ilegiveis = [t for t, f_ in r3["fichas"].items() if not f_["lido"]]
    diz("as oito fichas são marcadas ilegíveis, sem estourar", len(ilegiveis) == 8, str(len(ilegiveis)))
    p3 = r3["pool"]
    diz("e não sai diamante nenhum", p3 and p3["dl"] is None, str(p3.get("motivo") if p3 else ""))
    diz("com os oito ensaios listados como descartados", p3 and len(p3["descartados"]) == 8,
        str(len(p3["descartados"]) if p3 else 0))

print("\n" + "=" * 78)
if ok:
    print("A COSTURA P1 → P2 → P3 FECHA.")
else:
    print(f"{len(falhas)} FALHA(S) NA COSTURA — não rodar a campanha:")
    for f_ in falhas:
        print("  -", f_)
print("=" * 78)
sys.exit(0 if ok else 1)
