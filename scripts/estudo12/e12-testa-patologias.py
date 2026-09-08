# -*- coding: utf-8 -*-
"""As patologias reais de saída de modelo, contra o corretor da âncora 3. Nenhum modelo é chamado.

Por que este arquivo existe. O autoteste do corretor montava fichas a partir do próprio gabarito:
rótulo do gabarito, uma janela por ensaio, todo campo preenchido, todo número em string limpa. Passava
sempre — e passou enquanto o corretor tinha cinco defeitos que a revisão adversarial reproduziu, cada
um capaz de mudar o diamante sem levantar exceção nenhuma.

Modelos de verdade não devolvem fichas limpas. Cada caso abaixo tem procedência: ou é uma forma
colhida das saídas gravadas dos Estudos 8 e 9, ou é o comportamento que a própria ficha instrui. O
teste não pergunta se o corretor sobrevive: pergunta se ele acerta, e onde não puder acertar, se ele
diz que não sabe em vez de inventar um número.

A regra que organiza tudo: **errar é aceitável, inventar não é.** Uma célula que sai NR com o motivo
escrito vai para adjudicação. Uma célula que sai com número plausível e errado entra no artigo.
"""
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent


def _carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


A = _carrega("av", AQUI / "e12-avalia-a3.py")
GAB, SELO = A.GAB, A.SELO
ok, falhas = True, []


def diz(rot, passou, det=""):
    global ok
    ok = ok and passou
    if not passou:
        falhas.append(rot)
    print(f"  {'ok  ' if passou else 'FALHA'} {rot:58s} {det}")


def sel(tid):
    return {r["original"]: r["perturbado"] for r in (SELO.get(tid) or [])}


def ficha(tid, como_rotula=None, como_mortos=None, como_n=None, janela=None):
    """A ficha de um leitor PERFEITO do corpus perturbado, com a escrita variando."""
    f, s = GAB["bracos_da_fonte"][tid], sel(tid)
    fora = []
    for b in f["bracos"]:
        n = s.get(str(b["n"]), str(b["n"]))
        fora.append({"arm_label": {"value": (como_rotula or (lambda x: x["rotulo_fonte"]))(b)},
                     "timepoint": {"value": janela or f["janela"]},
                     "deaths": {"value": (como_mortos or (lambda b_, n_: str(b_["eventos"])))(b, n)},
                     "n": {"value": (como_n or (lambda b_, n_: n_))(b, n)},
                     "deaths_percent": {"value": "NR"}})
    return {"mortality": fora}


def celulas(r):
    return {k: r["celulas"][k]["modelo"] for k in A.CAMPOS}


def acertos(r):
    return sum(1 for c in r["celulas"].values() if c["acerta"])


# ══════════════════════════════════════════════════════════════════════════
print("1. RÓTULO DO BRAÇO — o modelo não copia o rótulo do gabarito; ele escreve o que entendeu")
print("   procedência: a própria ficha dá 'methylene blue 1 mg/kg' como exemplo de label\n")
CASOS_ROTULO = [
    ("shaker2025", "pela dose, como a ficha exemplifica",
     lambda b: {"ct": "placebo", "mb_baixa": "methylene blue 1 mg/kg",
                "mb_alta": "methylene blue 4 mg/kg"}[b["braco"]], {"eventos_mb": "15", "n_mb": "60"}),
    ("shaker2025", "pela letra do grupo", lambda b: b["rotulo_fonte"], {"eventos_mb": "15", "n_mb": "60"}),
    ("shaker2025", "letra minúscula e sem espaço", lambda b: b["rotulo_fonte"].replace("Group ", "group").lower(),
     {"eventos_mb": "15", "n_mb": "60"}),
    ("aguilar2016", "traduzido para o inglês (o artigo é em espanhol)",
     lambda b: b["rotulo_fonte"].replace("grupo", "Group"), {"eventos_mb": "6", "n_mb": "30"}),
    ("aguilar2016", "pelo papel, sem a letra",
     lambda b: "methylene blue" if b["papel_norm"] == "azul" else "control", {"eventos_mb": "6", "n_mb": "30"}),
    ("dong2025", "com o nome por extenso", lambda b: "methylene blue group" if b["papel_norm"] == "azul"
     else "control group", {"eventos_mb": "9", "n_mb": "36"}),
    ("levin2004", "abreviado", lambda b: "MB" if b["papel_norm"] == "azul" else "placebo",
     {"eventos_mb": "0", "n_mb": "28"}),
]
for tid, rot, f_rot, esperado in CASOS_ROTULO:
    r = A.corrige(ficha(tid, como_rotula=f_rot), tid)
    c = celulas(r)
    bate = all(c[k] == v for k, v in esperado.items())
    diz(f"{GAB['bracos_da_fonte'][tid]['ensaio'][:18]:20s} {rot}", bate,
        f"{c['eventos_mb']}/{c['n_mb']}" + (f"  órfãos={r['bracos_nao_atribuidos']}" if r["bracos_nao_atribuidos"] else ""))

r = A.corrige(ficha("shaker2025", como_rotula=lambda b: "methylene blue"), "shaker2025")
diz("rótulo AMBÍGUO nos dois braços ativos não é adivinhado", celulas(r)["eventos_mb"] == "NR",
    f"órfãos={r['bracos_nao_atribuidos']}")

# ══════════════════════════════════════════════════════════════════════════
print("\n2. FORMA DO NÚMERO — colhidas das saídas gravadas dos Estudos 8 e 9")
print("   ex.: \"mortality_gdft\": {\"value\": \"0.7% (2/283)\"} em p1/llama8/REF30-r1.json\n")
CASOS_NUM = [
    ("contagem simples", lambda b, n: str(b["eventos"]), "9"),
    ("com o percentual entre parênteses", lambda b, n: f"{b['eventos']} ({100*b['eventos']/int(n):.1f}%)", "9"),
    ("percentual ANTES da contagem", lambda b, n: f"{100*b['eventos']/int(n):.1f}% ({b['eventos']}/{n})", "9"),
    ("como fração", lambda b, n: f"{b['eventos']}/{n}", "9"),
    ("com casa decimal, como o Dong imprime", lambda b, n: f"{b['eventos']}.0", "9"),
    ("com palavra junto", lambda b, n: f"{b['eventos']} patients", "9"),
    ("com vírgula decimal", lambda b, n: f"{b['eventos']},0", "9"),
]
for rot, f_m, esp in CASOS_NUM:
    r = A.corrige(ficha("dong2025", como_mortos=f_m), "dong2025")
    c = celulas(r)
    diz(f"mortos escritos {rot}", c["eventos_mb"] == esp, f"eventos_mb={c['eventos_mb']}")

r = A.corrige(ficha("dong2025", como_mortos=lambda b, n: f"{100*b['eventos']/int(n):.1f}%"), "dong2025")
diz("SÓ o percentual, sem contagem: sai NR, não vira contagem", celulas(r)["eventos_mb"] == "NR",
    f"eventos_mb={celulas(r)['eventos_mb']}")

for rot, f_n, esp in (("denominador com casa decimal", lambda b, n: f"{n}.0", "36"),
                      ("denominador como 'n=41'", lambda b, n: f"n={n}", "36"),
                      ("denominador como fração", lambda b, n: f"{b['eventos']}/{n}", "36")):
    r = A.corrige(ficha("dong2025", como_n=f_n), "dong2025")
    diz(rot, celulas(r)["n_mb"] == esp, f"n_mb={celulas(r)['n_mb']}")

# ══════════════════════════════════════════════════════════════════════════
print("\n3. CAMPO FALTANDO — 'NR' é a resposta mais comum dos modelos em campo de mortalidade")
print("   243 ocorrências nas saídas gravadas dos Estudos 8 e 9\n")
f = GAB["bracos_da_fonte"]["shaker2025"]
s = sel("shaker2025")
mort = []
for b in f["bracos"]:
    n = s.get(str(b["n"]), str(b["n"]))
    mort.append({"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": "28 days"},
                 "deaths": {"value": "NR" if b["braco"] == "mb_alta" else str(b["eventos"])},
                 "n": {"value": n}, "deaths_percent": {"value": "NR"}})
r = A.corrige({"mortality": mort}, "shaker2025")
c = celulas(r)
diz("um braço ativo sem contagem NÃO produz célula quimérica",
    c["eventos_mb"] == "NR" and c["n_mb"] == "NR", f"{c['eventos_mb']}/{c['n_mb']}")
diz("e o motivo fica registrado", bool(r.get("duplicados")), str(r.get("duplicados"))[:70])

# ══════════════════════════════════════════════════════════════════════════
print("\n4. O BURACO DO ZERO — o comparador congelado aceitava qualquer número com um '0'")
print("   sete das 32 células caíam nele, entre elas o 0/28 do Levin\n")
for falso in ("10", "20", "30", "100", "0.0"):
    esperado_ok = falso == "0.0"
    passa = A.compara(falso, "0")
    diz(f"modelo diz {falso!r} onde a fonte diz '0'", passa == esperado_ok,
        "aceito" if passa else "reprovado")
for falso in ("0", "1", "60"):
    diz(f"modelo diz {falso!r} onde a fonte diz '10'", A.compara(falso, "10") == (falso == "10"),
        "aceito" if A.compara(falso, "10") else "reprovado")

# ══════════════════════════════════════════════════════════════════════════
print("\n5. FICHA MALFORMADA — o corretor não pode travar a campanha nem inventar")
MALFORMADAS = [
    ("prosa antes do JSON", 'Here is the extracted data:\n{"mortality": []}'),
    ("cerca de código", '```json\n{"mortality": []}\n```'),
    ("mortality como objeto e não lista", '{"mortality": {"arm_label": "MB"}}'),
    ("ficha embrulhada", '{"result": {"mortality": []}}'),
    ("JSON inválido", '{"mortality": [,]}'),
    ("vazio", ""),
    ("só prosa", "The article does not report mortality."),
]
for rot, bruto in MALFORMADAS:
    try:
        r = A.corrige(bruto, "dong2025")
        travou = False
        inventou = r.get("lido") and any(v["modelo"] not in ("NR",) for v in r["celulas"].values())
    except Exception as e:
        travou, inventou, r = True, False, {"motivo": f"{type(e).__name__}: {e}"}
    diz(f"{rot}: não trava e não inventa", not travou and not inventou,
        (r.get("motivo") or "lida")[:52])

# ══════════════════════════════════════════════════════════════════════════
print("\n6. O DIAMANTE NÃO SE MEXE POR PATOLOGIA DE ESCRITA")
print("   a mesma leitura correta, escrita de sete jeitos, tem de dar o mesmo diamante\n")
for rot, kw in (("rótulo pela dose", dict(como_rotula=lambda b: {"ct": "placebo", "mb": "methylene blue",
                                                                 "mb_baixa": "methylene blue 1 mg/kg",
                                                                 "mb_alta": "methylene blue 4 mg/kg"}.get(b["braco"], b["rotulo_fonte"]))),
                ("número com percentual junto", dict(como_mortos=lambda b, n: f"{b['eventos']} ({100*b['eventos']/int(n):.1f}%)")),
                ("denominador com casa decimal", dict(como_n=lambda b, n: f"{n}.0")),
                ("tudo como fração", dict(como_mortos=lambda b, n: f"{b['eventos']}/{n}",
                                          como_n=lambda b, n: f"{b['eventos']}/{n}"))):
    fichas = {t: A.corrige(ficha(t, **kw), t) for t in GAB["celulas"]}
    p = A.agrupa(fichas)
    n_ac = sum(acertos(r) for r in fichas.values())
    diz(f"{rot}: 32/32 e o diamante da camada 2",
        n_ac == 32 and p["dl"] and p["dl"]["or"] == 0.484 and p["dl"]["ic95"] == [0.319, 0.735],
        f"{n_ac}/32 · {p['dl'] if p['dl'] else p.get('motivo')}"
        + (f" · descartados {p['descartados']}" if p.get("descartados") else ""))

print("\n" + "=" * 80)
if ok:
    print("O CORRETOR SOBREVIVE ÀS PATOLOGIAS REAIS.")
else:
    print(f"{len(falhas)} PATOLOGIA(S) DERRUBAM O CORRETOR — não rodar a campanha:")
    for f_ in falhas:
        print("  -", f_)
print("=" * 80)
sys.exit(0 if ok else 1)
