# -*- coding: utf-8 -*-
"""O caminho de correção da razão de chances, da âncora 3. Instrumento 8 da §8.

Nenhum corretor, comparador ou mapa de campos do repositório conhece a família `or`: `CAMPOS_FAM` tem
`rr` e `md`, e só. Este módulo fecha essa lacuna sem tocar em nada do que existe. Ele importa e reusa,
verbatim:

  · `compat` de `e6-avalia.py`     — o comparador de magnitude congelado, com sua tolerância de 0,01
  · `acha_json` de `e3-harness.py` — a leitura tolerante do JSON que o modelo devolve
  · `e12-or.py`                    — o agrupamento em razão de chances, já validado
  · `e12-lente.py`                 — a lente de passe único com fronteira, da §6

O que ele acrescenta é a tradução entre a ficha da âncora 3 e as duas células de análise por ensaio,
que é onde moram as três regras congeladas da §5 e da §8:

  janela      a ficha traz uma entrada de mortalidade por MOMENTO. A regra escolhe a entrada de 28 a
              30 dias; onde o ensaio não publica essa janela, cai para a que o gabarito registra como
              a janela daquele ensaio, e a escolha vai anotada em cada célula.
  braço       a ficha traz TODOS os braços. A redução a duas células é feita aqui, não pelo modelo:
              os braços ativos somados contra o controle compartilhado (§5, A3-D1).
  polaridade  não existe regra de polaridade, nem aqui nem na ficha. Se o modelo transcrever
              sobreviventes, ele erra a célula, e é isso que a campanha quer medir.

Ordem, que a §7 do protocolo congela: a lente PRIMEIRO, sobre a ficha crua; a comparação depois.
Nunca o contrário.
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


e6 = _carrega("e6", RAIZ / "scripts" / "estudo6" / "e6-avalia.py")   # compat, congelado
h3 = _carrega("h3", RAIZ / "scripts" / "estudo3" / "e3-harness.py")  # acha_json, congelado
OR = _carrega("e12or", AQUI / "e12-or.py")
L = _carrega("lente", AQUI / "e12-lente.py")

D12 = RAIZ / "dados" / "estudo12"
GAB = json.loads(io.open(D12 / "gabarito-a3.json", encoding="utf-8").read())
SELO = json.loads(io.open(D12 / "perturbacoes-a3.json", encoding="utf-8").read())

JANELA_ALVO = re.compile(r"\b(28|29|30)\b\s*[-‑–]?\s*(?:day|d[ií]a)", re.I)
CAMPOS = ("eventos_mb", "n_mb", "eventos_ct", "n_ct")


def valor(x):
    """A ficha v1 traz {value, where}; a v2 traz {value, where, quote}. As duas leem igual."""
    if isinstance(x, dict):
        return x.get("value")
    return x


def desperturba(ficha, tid):
    """A lente, antes de qualquer comparação. Ensaio sem selo passa intacto."""
    regs = SELO.get(tid) or []
    return L.desperturba(ficha, regs) if regs else ficha


def entradas_de(ficha):
    """As linhas de mortalidade da ficha, normalizadas."""
    fora = []
    for e in (ficha.get("mortality") or []):
        if not isinstance(e, dict):
            continue
        fora.append(dict(arm=str(valor(e.get("arm_label")) or "").strip(),
                         janela=str(valor(e.get("timepoint")) or "").strip(),
                         mortos=valor(e.get("deaths")), n=valor(e.get("n")),
                         pct=valor(e.get("deaths_percent"))))
    return fora


def escolhe_janela(entradas, tid):
    """A regra congelada da janela. Nunca devolve entradas de janelas diferentes.

    Ordem: descarta a janela recusada; prefere a aceita; se ainda sobrar mais de uma janela distinta,
    devolve o conflito em vez de somar. A primeira versao devolvia TODAS as entradas quando nenhuma
    casava a alvo, e reduz() as somava: o Aguilar saia 12/60 em vez de 6/30. Somar atraves de bracos e
    a regra da §5; somar atraves de janelas nunca foi regra nenhuma.
    """
    j = GAB["bracos_da_fonte"][tid]
    aceita, recusada = j.get("janela_aceita"), j.get("janela_recusada")

    vivas = [e for e in entradas
             if not (recusada and re.search(recusada, e["janela"], re.I))]
    descartadas = len(entradas) - len(vivas)

    boas = [e for e in vivas if aceita and re.search(aceita, e["janela"], re.I)]
    if boas:
        janelas = {re.sub(r"[^a-z0-9]+", " ", e["janela"].lower()).strip() for e in boas}
        motivo = f"janela aceita do ensaio ({j['janela']})"
        if descartadas:
            motivo += f"; {descartadas} entrada(s) de janela recusada descartada(s)"
        if len(janelas) > 1:
            motivo += f"; {len(janelas)} redacoes da mesma janela: {sorted(janelas)}"
        return boas, motivo, None

    # nenhuma casa a aceita. So da para seguir se TODAS as vivas estiverem na MESMA janela.
    janelas = {re.sub(r"[^a-z0-9]+", " ", e["janela"].lower()).strip() for e in vivas}
    if len(janelas) == 1 and vivas:
        return vivas, (f"nenhuma entrada casa a janela aceita ({aceita}); todas estao em "
                       f"{sorted(janelas)[0]!r} e foram usadas"), None
    return [], "", (f"a ficha traz {len(janelas)} janelas distintas e nenhuma casa a aceita do "
                    f"ensaio: {sorted(janelas)}. Nao se soma atraves de janelas; celula a adjudicar.")


def reduz(entradas, tid):
    """Todos os bracos da ficha viram as duas celulas de analise. §5, A3-D1.

    A atribuicao usa o rotulo que o ARTIGO da ao braco (`rotulo_fonte` no gabarito), porque e esse
    que o modelo transcreve. A primeira versao casava contra a descricao em portugues do gabarito, e
    palavras comuns a todos os bracos -- "grupo" -- faziam tudo cair no mesmo lado: os tres bracos do
    Shaker viravam 29/90.
    """
    regra = GAB["_reducao_multibraco"].get(tid)
    bracos = GAB["bracos_da_fonte"][tid]["bracos"]

    def norm(x):
        return re.sub(r"[^a-z0-9]+", " ", str(x).lower()).strip()

    def lado_de(e):
        r = norm(e["arm"])
        if not r:
            return None
        casos = [b["braco"] for b in bracos
                 if norm(b["rotulo_fonte"]) and (norm(b["rotulo_fonte"]) in r or r in norm(b["rotulo_fonte"]))]
        if len(casos) == 1:
            return casos[0]
        if len(casos) > 1:
            return None                       # ambiguo: nao se adivinha
        if re.search(r"placebo|control|saline|conventional|standard|vasopressin", r):
            return next((b["braco"] for b in bracos if b["braco"].startswith("ct")), None)
        if re.search(r"methylene|blue|azul|\bmb\b", r):
            cands = [b["braco"] for b in bracos if b["braco"].startswith("mb")]
            return cands[0] if len(cands) == 1 else None
        return None

    lados, nao_atribuidos, duplicados = {"mb": [], "ct": []}, [], []
    vistos = {}
    for e in entradas:
        b = lado_de(e)
        if b is None:
            nao_atribuidos.append(e["arm"])
            continue
        # o mesmo braco duas vezes na mesma janela: mantem o primeiro e registra, nunca soma
        assinatura = (b, str(e["mortos"]), str(e["n"]))
        if b in vistos:
            if vistos[b] != assinatura:
                duplicados.append(f"{e['arm']}: {vistos[b][1]}/{vistos[b][2]} e depois "
                                  f"{assinatura[1]}/{assinatura[2]}")
            continue
        vistos[b] = assinatura
        destino = ("mb" if b in regra["mb"] else "ct" if b in regra["ct"] else None) if regra             else ("mb" if b.startswith("mb") else "ct" if b.startswith("ct") else None)
        if destino:
            lados[destino].append(e)
        else:
            nao_atribuidos.append(e["arm"])

    def soma(campo, itens):
        vs = [v for v in (_num(x[campo]) for x in itens) if v is not None]
        return None if not vs else sum(vs)

    return ({"eventos_mb": soma("mortos", lados["mb"]), "n_mb": soma("n", lados["mb"]),
             "eventos_ct": soma("mortos", lados["ct"]), "n_ct": soma("n", lados["ct"])},
            nao_atribuidos, duplicados)


def tela_recitacao(ficha_crua, tid):
    """Rede de recitacao, sobre a ficha CRUA -- antes da lente, que e o unico momento em que da.

    Depois da lente a recitacao fica invisivel: o modelo que le devolve 41 e a lente o traz a 36; o
    que recita ja devolve 36, e a lente nao mexe. As duas celulas chegam identicas ao comparador. A
    unica assinatura esta no que o modelo ESCREVEU: um valor igual ao original de um par selado, num
    corpus onde aquele valor nao existe mais.

    Doutrina de so avisar: a rede acusa, nunca substitui. Cada candidato vai a adjudicacao.
    """
    regs = SELO.get(tid) or []
    originais = {str(r["original"]): r for r in regs if r["papel"] == "denominador"}
    if not originais:
        return []
    achados = []
    for e in entradas_de(ficha_crua):
        for campo in ("n", "mortos", "pct"):
            v = e.get(campo)
            if v is None:
                continue
            m = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)\s*%?\s*", str(v))
            if not m:
                continue
            chave = m.group(1)
            if chave.endswith(".0"):
                chave = chave[:-2]
            if chave in originais:
                achados.append(dict(braco=e["arm"], campo=campo, valor=str(v),
                                    perturbado=originais[chave]["perturbado"],
                                    aviso="valor igual ao original selado; nao existe no corpus lido"))
    return achados


def _num(v):
    if v is None:
        return None
    m = re.search(r"-?\d+(?:\.\d+)?", str(v))
    return float(m.group(0)) if m else None


def corrige(bruto, tid):
    """Uma ficha crua -> as quatro células corrigidas contra a camada 2, com a citação do gabarito."""
    ficha = h3.acha_json(bruto) if isinstance(bruto, str) else bruto
    if not ficha:
        return dict(tid=tid, lido=False, motivo="a ficha não devolveu JSON legível", celulas={})
    recitacao = tela_recitacao(ficha, tid)                # a rede ANTES da lente
    ficha = desperturba(ficha, tid)                       # a lente antes de comparar
    ents = entradas_de(ficha)
    if not ents:
        return dict(tid=tid, lido=False, motivo="a ficha não traz entradas de mortalidade", celulas={})
    ents, motivo_janela, conflito = escolhe_janela(ents, tid)
    if conflito:
        return dict(tid=tid, lido=True, motivo=conflito, janela="conflito", recitacao=recitacao,
                    bracos_nao_atribuidos=[], duplicados=[],
                    celulas={c: dict(modelo="NR", fonte=GAB["celulas"][tid][c]["valor_fonte"],
                                     ma=GAB["celulas"][tid][c]["ma"], acerta=False,
                                     acerta_a_revisao=False,
                                     veredito_gabarito=GAB["celulas"][tid][c]["veredito"],
                                     cit=GAB["celulas"][tid][c]["cit"]) for c in CAMPOS})
    cel, orfaos, duplicados = reduz(ents, tid)
    gab = GAB["celulas"][tid]
    saida = {}
    for campo in CAMPOS:
        m = cel.get(campo)
        m_s = "NR" if m is None else (str(int(m)) if float(m).is_integer() else str(m))
        f_s = gab[campo]["valor_fonte"]
        saida[campo] = dict(modelo=m_s, fonte=f_s, ma=gab[campo]["ma"],
                            acerta=e6.compat(m_s, f_s),
                            acerta_a_revisao=e6.compat(m_s, gab[campo]["ma"]),
                            veredito_gabarito=gab[campo]["veredito"], cit=gab[campo]["cit"])
    return dict(tid=tid, lido=True, motivo="", janela=motivo_janela,
                bracos_nao_atribuidos=orfaos, duplicados=duplicados,
                recitacao=recitacao, celulas=saida)


def agrupa(fichas):
    """As oito duplas corrigidas -> o diamante, pelas duas rotas que a §5 declara."""
    est = []
    for tid in GAB["celulas"]:
        c = (fichas.get(tid) or {}).get("celulas") or {}
        v = [_num(c.get(k, {}).get("modelo")) for k in CAMPOS]
        if any(x is None for x in v) or v[1] <= 0 or v[3] <= 0:
            continue
        est.append((v[0], v[1], v[2], v[3]))
    if len(est) < 2:
        return None
    return dict(k=len(est), dl=OR.pool_or_dl(est), mh=OR.pool_or_mh(est))


# ------------------------------------------------------------------ autoteste
if __name__ == "__main__":
    ok = True

    def diz(rot, passou, det=""):
        global ok
        ok = ok and passou
        print(f"  {'ok  ' if passou else 'ERRO'} {rot:52s} {det}")

    print("1. um leitor perfeito, sobre o corpus PERTURBADO, tem de tirar nota cheia")
    fichas = {}
    for tid, f in GAB["bracos_da_fonte"].items():
        regs = {r["original"]: r["perturbado"] for r in (SELO.get(tid) or [])}
        mort = []
        for b in f["bracos"]:
            n = regs.get(str(b["n"]), str(b["n"]))          # o que o modelo LÊ é o perturbado
            mort.append({"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": f["janela"]},
                         "deaths": {"value": str(b["eventos"])}, "n": {"value": n},
                         "deaths_percent": {"value": regs.get(b["pct"], b["pct"]) if b["pct"] else "NR"}})
        r = corrige({"mortality": mort}, tid)
        fichas[tid] = r
        acertos = sum(1 for c in r["celulas"].values() if c["acerta"])
        diz(f"{f['ensaio']}", r["lido"] and acertos == 4 and not r["bracos_nao_atribuidos"],
            f"{acertos}/4" + (f" · órfãos {r['bracos_nao_atribuidos']}" if r["bracos_nao_atribuidos"] else ""))

    print("\n2. o diamante desse leitor perfeito tem de ser o da camada 2")
    p = agrupa(fichas)
    diz("oito ensaios agrupados", p and p["k"] == 8, f"k={p['k'] if p else 0}")
    diz("DL devolve 0,484 [0,319; 0,735]", p and p["dl"]["or"] == 0.484
        and p["dl"]["ic95"] == [0.319, 0.735], str(p["dl"]) if p else "")

    print("\n3. quem RECITA o denominador original é apanhado pela REDE, não pela célula")
    tid = "dong2025"
    f = GAB["bracos_da_fonte"][tid]
    mort = [{"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": f["janela"]},
             "deaths": {"value": str(b["eventos"])}, "n": {"value": str(b["n"])},   # 36, o original
             "deaths_percent": {"value": b["pct"]}} for b in f["bracos"]]
    r = corrige({"mortality": mort}, tid)
    diz("a rede de recitação acusa", len(r["recitacao"]) >= 2,
        f"{len(r['recitacao'])} candidatos: " + ", ".join(sorted({x['valor'] for x in r['recitacao']})))
    diz("e a célula, sozinha, NÃO acusaria", r["celulas"]["n_mb"]["acerta"],
        "é por isso que a rede tem de rodar antes da lente")

    print("\n4. quem transcreve SOBREVIVENTES no Aguilar erra, e a ficha não avisou")
    tid = "aguilar2016"
    f = GAB["bracos_da_fonte"][tid]
    regs = {x["original"]: x["perturbado"] for x in SELO[tid]}
    mort = [{"arm_label": {"value": b["rotulo_fonte"]}, "timepoint": {"value": f["janela"]},
             "deaths": {"value": str(int(regs.get(str(b["n"]), b["n"])) - b["eventos"])},
             "n": {"value": regs.get(str(b["n"]), str(b["n"]))},
             "deaths_percent": {"value": "NR"}} for b in f["bracos"]]
    r = corrige({"mortality": mort}, tid)
    diz("a inversão é reprovada contra a fonte", not r["celulas"]["eventos_mb"]["acerta"],
        f"modelo diz {r['celulas']['eventos_mb']['modelo']}, fonte {r['celulas']['eventos_mb']['fonte']}")
    diz("e também não bate com a revisão", not r["celulas"]["eventos_mb"]["acerta_a_revisao"],
        f"a revisão publicou {r['celulas']['eventos_mb']['ma']}")

    print("\n5. quem devolve a célula PUBLICADA do Aguilar acerta a revisão e erra a fonte")
    mort = [{"arm_label": {"value": "grupo A"}, "timepoint": {"value": f["janela"]},
             "deaths": {"value": "24"}, "n": {"value": "30"}, "deaths_percent": {"value": "NR"}},
            {"arm_label": {"value": "grupo C"}, "timepoint": {"value": f["janela"]},
             "deaths": {"value": "19"}, "n": {"value": "30"}, "deaths_percent": {"value": "NR"}}]
    r = corrige({"mortality": mort}, tid)
    diz("acerta a revisão", r["celulas"]["eventos_mb"]["acerta_a_revisao"],
        f"a revisão publicou {r['celulas']['eventos_mb']['ma']}")
    diz("erra a fonte", not r["celulas"]["eventos_mb"]["acerta"],
        f"a fonte diz {r['celulas']['eventos_mb']['fonte']}")
    diz("e a rede acusa o denominador recitado", any(x["valor"] == "30" for x in r["recitacao"]),
        f"{len(r['recitacao'])} candidatos")

    print("\n6. o Shaker de três braços é reduzido pelo corretor, não pelo modelo")
    tid = "shaker2025"
    diz("os três braços viram 15/60 contra 14/30",
        fichas[tid]["celulas"]["eventos_mb"]["modelo"] == "15"
        and fichas[tid]["celulas"]["n_mb"]["modelo"] == "60"
        and fichas[tid]["celulas"]["n_ct"]["modelo"] == "30",
        f"{fichas[tid]['celulas']['eventos_mb']['modelo']}/{fichas[tid]['celulas']['n_mb']['modelo']}"
        f" contra {fichas[tid]['celulas']['eventos_ct']['modelo']}/{fichas[tid]['celulas']['n_ct']['modelo']}")

    print("\n" + "=" * 78)
    print("CAMINHO DA RAZÃO DE CHANCES VERIFICADO" if ok else "FALHOU")
    print("=" * 78)
    sys.exit(0 if ok else 1)
