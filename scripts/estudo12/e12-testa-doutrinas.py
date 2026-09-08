# -*- coding: utf-8 -*-
"""As doutrinas do projeto, testadas contra o código da Fase 0. Nenhum modelo é chamado.

O EXTRAI não é um script: é um conjunto de compromissos sobre como se mede. Eles estão escritos em
`METHOD.md` e nos protocolos, e até aqui viviam só como prosa — o que significa que um refactor podia
quebrá-los em silêncio. Este arquivo os transforma em teste.

Cada bloco abaixo é uma doutrina do projeto, com o teste que a exerce e o cenário concreto em que ela
seria violada. Quando um teste falha, o defeito não é de estilo: é uma promessa do método que o código
deixou de cumprir.

Rodar antes da P1, e depois de qualquer mexida em instrumento.
"""
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent
D12 = RAIZ / "dados" / "estudo12"


def _carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = _carrega("h12", AQUI / "e12-harness.py")
A = _carrega("av12", AQUI / "e12-avalia-a3.py")
L = _carrega("lente", AQUI / "e12-lente.py")
GAB = json.loads(io.open(D12 / "gabarito-a3.json", encoding="utf-8").read())
SELO = json.loads(io.open(D12 / "perturbacoes-a3.json", encoding="utf-8").read())

ok = True
falhas = []


def diz(rot, passou, det=""):
    global ok
    ok = ok and passou
    if not passou:
        falhas.append(rot)
    print(f"  {'ok  ' if passou else 'FALHA'} {rot:56s} {det}")


def secao(n, titulo, doutrina):
    print(f"\n{n}. {titulo}")
    print(f"   \"{doutrina}\"")


# ══════════════════════════════════════════════════════════════════════════
secao(1, "MOTORES CONGELADOS", "frozen models, engines and configs; the engine under test is the one the earlier studies froze")
FROZEN = ["scripts/estudo2/e2-harness.py", "scripts/estudo3/e3-harness.py",
          "scripts/estudo1/perturbar.py", "scripts/estudo6/e6-avalia.py",
          "scripts/estudo1/e1-harness.py", "scripts/estudo6/e6-downstream.py"]
# o Estudo 12 começou no commit em que decisoes-fase0.md nasceu
base = subprocess.run(["git", "log", "--format=%H", "--diff-filter=A", "--",
                       "dados/estudo12/decisoes-fase0.md"],
                      capture_output=True, text=True, cwd=str(RAIZ)).stdout.strip().splitlines()
base = base[-1] if base else "HEAD~30"
for f in FROZEN:
    d = subprocess.run(["git", "diff", "--stat", base, "HEAD", "--", f],
                       capture_output=True, text=True, cwd=str(RAIZ)).stdout.strip()
    diz(f"{f.split('/')[-1]} intocado desde o início do Estudo 12", not d, d[:50])
diz("h3.CTX segue 16.384 em memória", H.h3.CTX == 16384, f"CTX={H.h3.CTX}")

# ══════════════════════════════════════════════════════════════════════════
secao(2, "CHAVE DE DUAS CAMADAS", "the published cell and the source-verified cell are both kept; the source decides")
sem_ma = [(t, c) for t, cs in GAB["celulas"].items() for c, v in cs.items() if not str(v.get("ma", "")).strip()]
sem_fonte = [(t, c) for t, cs in GAB["celulas"].items() for c, v in cs.items() if not str(v.get("valor_fonte", "")).strip()]
diz("toda célula tem camada 1 (o que a revisão publicou)", not sem_ma, str(sem_ma[:3]))
diz("toda célula tem camada 2 (o que a fonte diz)", not sem_fonte, str(sem_fonte[:3]))
n_err = sum(1 for cs in GAB["celulas"].values() for v in cs.values() if v["veredito"] == "errata-ma")
diz("as camadas divergem onde a errata diz que divergem", n_err == 3, f"{n_err} células errata-ma")

# ══════════════════════════════════════════════════════════════════════════
secao(3, "CITAÇÃO ANTES DO VEREDITO", "quote before verdict: no verdict without the literal sentence that decides it")
sem_cit = [(t, c) for t, cs in GAB["celulas"].items() for c, v in cs.items() if not str(v.get("cit", "")).strip()]
diz("toda célula graduável carrega citação", not sem_cit, str(sem_cit[:3]))
faltando = []
for tid, f in GAB["bracos_da_fonte"].items():
    t = io.open(RAIZ / "dados" / "estudo11" / "primarios" / f["primario"], encoding="utf-8",
                errors="replace").read()
    if f["primario"].endswith(".xml"):
        t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t)
    for c, v in GAB["celulas"][tid].items():
        if re.sub(r"\s+", " ", v["cit"]) not in t:
            faltando.append(f"{tid}.{c}")
diz("cada citação existe literalmente no primário", not faltando, str(sorted(set(faltando))[:3]))

# ══════════════════════════════════════════════════════════════════════════
secao(4, "CORREÇÃO CONTRA A CAMADA 2", "grading is against the source, never against the review")
tid = "aguilar2016"
mort = [{"arm_label": {"value": "grupo A"}, "timepoint": {"value": "21 days"},
         "deaths": {"value": "24"}, "n": {"value": "30"}, "deaths_percent": {"value": "NR"}},
        {"arm_label": {"value": "grupo C"}, "timepoint": {"value": "21 days"},
         "deaths": {"value": "19"}, "n": {"value": "30"}, "deaths_percent": {"value": "NR"}}]
r = A.corrige({"mortality": mort}, tid)
diz("reproduzir a revisão REPROVA contra a fonte", not r["celulas"]["eventos_mb"]["acerta"],
    f"modelo 24, fonte {r['celulas']['eventos_mb']['fonte']}")
diz("e o acerto contra a revisão fica registrado à parte", r["celulas"]["eventos_mb"]["acerta_a_revisao"])

# ══════════════════════════════════════════════════════════════════════════
secao(5, "SÓ AVISAR, NUNCA SUBSTITUIR", "nets detect and warn, never substitute a value")
f = GAB["bracos_da_fonte"]["dong2025"]
mort = [{"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": "28 days"},
         "deaths": {"value": str(b["eventos"])}, "n": {"value": str(b["n"])},   # 36: o original
         "deaths_percent": {"value": "NR"}} for b in f["bracos"]]
r = A.corrige({"mortality": mort}, "dong2025")
diz("a rede de recitação acusa", len(r["recitacao"]) >= 2, f"{len(r['recitacao'])} candidatos")
diz("e NÃO trocou o valor que o modelo escreveu", r["celulas"]["n_mb"]["modelo"] == "36",
    f"a célula continua {r['celulas']['n_mb']['modelo']}")

# ══════════════════════════════════════════════════════════════════════════
secao(6, "REPROVADO É REGISTRADO, NÃO APAGADO", "record the rejected; never delete")
fonte = io.open(AQUI / "e12-harness.py", encoding="utf-8").read()
diz("o harness não apaga saída em lugar nenhum",
    "unlink" not in fonte.replace("os.unlink(tmp)", ""), "só o temporário de escrita é apagado")
with tempfile.TemporaryDirectory() as td:
    d = Path(td)
    p = d / "a" / "b" / "c" / "x-r1.json"
    p.parent.mkdir(parents=True)
    io.open(p, "w", encoding="utf-8").write('{"finish": "length"}')
    antes, H.RECUSADOS = H.RECUSADOS, d / "rec"
    H.afasta(p, "truncada")
    achados = sorted(x.name for x in (d / "rec").iterdir())
    H.RECUSADOS = antes
    diz("o afastado é preservado com o motivo ao lado", len(achados) == 2, str(achados))

# ══════════════════════════════════════════════════════════════════════════
secao(7, "SELOS COM SHA-256", "sealed maps, their hash recorded, and checked when used")
corpo = json.dumps(SELO, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
sha_agora = hashlib.sha256(corpo.encode("utf-8")).hexdigest()
sha_gravado = io.open(D12 / "perturbacoes-a3.sha256", encoding="utf-8").read().strip()
diz("o SHA gravado do selo bate com o selo em disco", sha_agora == sha_gravado,
    f"{sha_agora[:16]}… contra {sha_gravado[:16]}…")

# ══════════════════════════════════════════════════════════════════════════
secao(8, "CORPUS CONGELADO", "the perturbed corpus is exactly the original plus the sealed map")
divergem = []
for tid in GAB["bracos_da_fonte"]:
    orig = io.open(RAIZ / "corpus" / "estudo12" / "original" / f"{tid}.txt", encoding="utf-8").read()
    pert = io.open(RAIZ / "corpus" / "estudo12" / "perturbados" / f"{tid}.txt", encoding="utf-8").read()
    volta, _ = L.aplica(pert, [(r["perturbado"], r["original"]) for r in (SELO.get(tid) or [])])
    if volta != orig:
        divergem.append(tid)
diz("a lente devolve o perturbado ao original, byte a byte", not divergem, str(divergem))
# o corpus perturbado não pode devolver o denominador original por aritmética de uma linha. Deixar o
# TOTAL intacto fazia o Aguilar dizer "Quedaron N: 60 pacientes" com braços de 32 e 32 — e a rede de
# recitação acusaria justamente quem reconciliasse os dois números.
delatores = []
for tid in GAB["bracos_da_fonte"]:
    desloc = {int(r["original"]): int(r["perturbado"])
              for r in (SELO.get(tid) or []) if r["papel"] == "denominador"}
    if not desloc:
        continue
    txt = io.open(RAIZ / "corpus" / "estudo12" / "perturbados" / f"{tid}.txt", encoding="utf-8").read()
    txt = re.sub(r"\s+", " ", txt)
    k = len(GAB["bracos_da_fonte"][tid]["bracos"])
    for n_o, n_p in desloc.items():
        for mult in range(1, k + 1):
            alvo = n_o * mult
            if alvo == n_p * mult:
                continue
            for m in re.finditer(r"(?<![\w.,\-–])" + str(alvo) + r"(?![\w.])[^.]{0,60}", txt):
                if re.search(r"patient|pacient|randomi|enroll|includ|incluid|divided|allocat",
                             m.group(0), re.I):
                    delatores.append(f"{tid}: {alvo} = {n_o}×{mult}")
diz("nenhum total do corpus devolve o denominador original", not delatores, str(delatores[:2]))

sem_selo = [t for t in GAB["bracos_da_fonte"] if not SELO.get(t)]
identicos = [t for t in sem_selo
             if io.open(RAIZ / "corpus" / "estudo12" / "original" / f"{t}.txt", encoding="utf-8").read()
             == io.open(RAIZ / "corpus" / "estudo12" / "perturbados" / f"{t}.txt", encoding="utf-8").read()]
diz("os ensaios sem selo têm corpus idêntico ao original",
    sorted(identicos) == sorted(sem_selo), f"sem prova de leitura: {sorted(sem_selo)}")

# ══════════════════════════════════════════════════════════════════════════
secao(9, "NADA DE CAP SILENCIOSO", "no silent caps: what is dropped is logged")
mort = [{"arm_label": {"value": "grupo inexistente"}, "timepoint": {"value": "28 days"},
         "deaths": {"value": "3"}, "n": {"value": "33"}, "deaths_percent": {"value": "NR"}}]
r = A.corrige({"mortality": mort}, "shaker2025")
diz("braço não atribuível é reportado, não descartado em silêncio",
    bool(r.get("bracos_nao_atribuidos")), str(r.get("bracos_nao_atribuidos")))
p = A.agrupa({"dong2025": r})
diz("agrupar com um ensaio só não produz diamante", p["dl"] is None, p.get("motivo", ""))
diz("e diz QUAIS ensaios ficaram de fora, um a um", len(p["descartados"]) == 8,
    f"{len(p['descartados'])} descartados, ex.: {p['descartados'][0][:52]}")
# eventos maiores que o denominador é o caso natural de quem transcreve percentual como contagem
mau = {t: dict(celulas={c: dict(modelo="99" if c.startswith("eventos") else "30", fonte="",
                                ma="", acerta=False, acerta_a_revisao=False,
                                veredito_gabarito="", cit="") for c in A.CAMPOS})
       for t in list(GAB["celulas"])[:3]}
p = A.agrupa(mau)
diz("eventos acima do denominador não estouram, são descartados com o motivo",
    p["dl"] is None and any("passam do denominador" in x for x in p["descartados"]),
    p["descartados"][0][:60] if p["descartados"] else "")

# ══════════════════════════════════════════════════════════════════════════
secao(10, "NUNCA SOMAR ATRAVÉS DE JANELAS", "arms are summed by the frozen rule; timepoints never are")
f = GAB["bracos_da_fonte"]["dong2025"]
selo_d = {x["original"]: x["perturbado"] for x in SELO["dong2025"]}
for grafia in ("28 days", "28 d", "day 28", "28-day mortality"):
    mort = []
    for b in f["bracos"]:
        n = selo_d.get(str(b["n"]), str(b["n"]))
        mort.append({"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": grafia},
                     "deaths": {"value": str(b["eventos"])}, "n": {"value": n}, "deaths_percent": {"value": "NR"}})
        mort.append({"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": "90 days"},
                     "deaths": {"value": "12" if b["braco"] == "mb" else "17"}, "n": {"value": n},
                     "deaths_percent": {"value": "NR"}})
    r = A.corrige({"mortality": mort}, "dong2025")
    c = r["celulas"]
    diz(f"Dong com a janela escrita {grafia!r}",
        (c["eventos_mb"]["modelo"], c["n_mb"]["modelo"]) == ("9", "36"),
        f"{c['eventos_mb']['modelo']}/{c['n_mb']['modelo']}")
f = GAB["bracos_da_fonte"]["aguilar2016"]
selo_a = {x["original"]: x["perturbado"] for x in SELO["aguilar2016"]}
mort = []
for b in f["bracos"]:
    n = selo_a.get(str(b["n"]), str(b["n"]))
    for j in ("at ICU discharge", "21 days"):
        mort.append({"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": j},
                     "deaths": {"value": str(b["eventos"])}, "n": {"value": n}, "deaths_percent": {"value": "NR"}})
r = A.corrige({"mortality": mort}, "aguilar2016")
diz("Aguilar com duas janelas não duplica",
    (r["celulas"]["eventos_mb"]["modelo"], r["celulas"]["n_mb"]["modelo"]) == ("6", "30"),
    f"{r['celulas']['eventos_mb']['modelo']}/{r['celulas']['n_mb']['modelo']}")

# ══════════════════════════════════════════════════════════════════════════
secao(11, "CONTEXTO DECLARADO É O CONTEXTO ENVIADO", "num_ctx 24576 in the request body, not only in the protocol")
capturado = {}


def espia(url, body, timeout=7200):
    capturado.update(url=url, body=body)
    raise RuntimeError("interceptado pelo teste: nenhuma chamada sai daqui")


guardado = H.h3.post_json
H.h3.post_json = espia
try:
    H.chama(dict(modelo="gemma12", ancora="a3", ficha="v2", ensaio="dong2025", replica=1), "prompt")
except RuntimeError:
    pass
finally:
    H.h3.post_json = guardado
b = capturado.get("body", {})
diz("num_ctx enviado é 24.576", b.get("options", {}).get("num_ctx") == 24576, str(b.get("options")))
diz("num_predict da v2 é 8.000", b.get("options", {}).get("num_predict") == 8000)
diz("think vem desligado", b.get("think") is False)
diz("stream vem desligado", b.get("stream") is False)
diz("nenhuma semente nem temperatura é enviada",
    not ({"seed", "temperature", "top_p", "top_k"} & set(b.get("options", {}))), str(b.get("options")))
diz("o endpoint é o local", "localhost:11434/api/generate" in capturado.get("url", ""))

# ══════════════════════════════════════════════════════════════════════════
secao(12, "O PLANO É O DO PROTOCOLO", "696 calls, enumerated, covering exactly the three anchors")
todas = list(H.plano())
por = {}
for c in todas:
    por[(c["ancora"], c["ficha"])] = por.get((c["ancora"], c["ficha"]), 0) + 1
diz("696 chamadas", len(todas) == 696, str(len(todas)))
diz("cada âncora × ficha aparece 6 modelos × 2 réplicas × ensaios",
    por == {("a1", "v1"): 168, ("a1", "v2"): 168, ("a2", "v1"): 84,
            ("a2", "v2"): 84, ("a3", "v1"): 96, ("a3", "v2"): 96}, str(por))
diz("nenhum destino colide", len({str(H.destino(c)) for c in todas}) == len(todas))
faltam_ficheiros = [str(c["caminho"]) for c in todas if not Path(c["caminho"]).exists()]
diz("todo ensaio do plano tem arquivo em disco", not faltam_ficheiros, str(faltam_ficheiros[:2]))
diz("as três âncoras montam prompt sem deixar marcador",
    all("{ARTICLE}" not in H.monta(io.open(H.ANCORAS[a]["fichas"][v], encoding="utf-8").read(),
                                   io.open(H.ensaios(a)[0][1], encoding="utf-8").read())
        for a in ("a1", "a2", "a3") for v in ("v1", "v2")))

# ══════════════════════════════════════════════════════════════════════════
secao(13, "ARTEFATOS REPRODUTÍVEIS", "a pre-registered artifact must rebuild byte-identical")
for script, alvo in (("e12-gabarito-a3.py", "gabarito-a3.json"),
                     ("e12-perturbar-a3.py", "perturbacoes-a3.json"),
                     ("e12-fichas-a3.py", "prompts/a3-extraction.txt")):
    antes = hashlib.sha256(io.open(D12 / alvo, "rb").read()).hexdigest()
    subprocess.run([sys.executable, str(AQUI / script)], capture_output=True, cwd=str(RAIZ))
    depois = hashlib.sha256(io.open(D12 / alvo, "rb").read()).hexdigest()
    diz(f"{alvo} reconstrói idêntico", antes == depois, f"{antes[:12]} contra {depois[:12]}")

# ══════════════════════════════════════════════════════════════════════════
secao(14, "INCONSISTÊNCIAS REGISTRADAS ANTES", "the anchor's own contradictions are listed before the runs")
prot = io.open(D12 / "protocolo-estudo12.md", encoding="utf-8").read()
for d in ("A3-D1", "A3-D2", "A3-D3", "A3-D4", "A3-D5"):
    diz(f"{d} está no protocolo", d in prot)
diz("e o registro de erratas existe, com as duas peças",
    (D12 / "erratas-ancora-3.md").exists() and (D12 / "errata-alert-table-ancora3.md").exists())

# ══════════════════════════════════════════════════════════════════════════
secao(15, "O LEITOR PERFEITO FECHA COM A CAMADA 2", "the whole chain agrees with itself")
fichas = {}
for tid, f in GAB["bracos_da_fonte"].items():
    regs = {x["original"]: x["perturbado"] for x in (SELO.get(tid) or [])}
    mort = [{"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": f["janela"]},
             "deaths": {"value": str(b["eventos"])},
             "n": {"value": regs.get(str(b["n"]), str(b["n"]))},
             "deaths_percent": {"value": regs.get(b["pct"], b["pct"]) if b["pct"] else "NR"}}
            for b in f["bracos"]]
    fichas[tid] = A.corrige({"mortality": mort}, tid)
acertos = sum(1 for r in fichas.values() for c in r["celulas"].values() if c["acerta"])
diz("32 de 32 células", acertos == 32, f"{acertos}/32")
p = A.agrupa(fichas)
diz("e o diamante é 0,484 [0,319; 0,735]",
    p and p["dl"]["or"] == 0.484 and p["dl"]["ic95"] == [0.319, 0.735], str(p["dl"]) if p else "")
diz("nenhuma recitação falsa acusada num leitor honesto",
    not any(r.get("recitacao") for r in fichas.values()),
    str([t for t, r in fichas.items() if r.get("recitacao")]))

# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
if ok:
    print("TODAS AS DOUTRINAS PASSAM.")
else:
    print(f"{len(falhas)} DOUTRINA(S) VIOLADA(S) — não rodar a campanha:")
    for f in falhas:
        print("  -", f)
print("=" * 78)
sys.exit(0 if ok else 1)
