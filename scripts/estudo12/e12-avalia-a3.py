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
import hashlib
import importlib.util
import io
import unicodedata
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
_selo_p = D12 / "perturbacoes-a3.json"
SELO = json.loads(io.open(_selo_p, encoding="utf-8").read())
# O selo e conferido AQUI, no ponto de uso, e nao apenas no ponto de criacao. Um mapa alterado
# depois de selado inverteria a lente e reprovaria transcricoes corretas sem que nada acusasse.
_sha_reg = io.open(D12 / "perturbacoes-a3.sha256", encoding="utf-8").read().strip()
_sha_ora = hashlib.sha256(io.open(_selo_p, "rb").read()).hexdigest()
if _sha_ora != _sha_reg:
    raise SystemExit("o selo da ancora 3 nao bate com o SHA registrado.\n"
                     "  registrado " + _sha_reg + "\n  agora      " + _sha_ora + "\n"
                     "Regenere com e12-perturbar-a3.py ou investigue a alteracao.")

def compara(modelo_s, fonte_s):
    """Comparacao de celula. Numerica e exata quando os dois lados sao numeros puros.

    O comparador congelado `e6.compat` foi escrito para celulas de TEXTO da ancora 1 e tem um buraco
    no zero: quando um dos lados nao tem numero nao-nulo, o ramo numerico e pulado e a decisao cai
    num fallback de SUBSTRING de texto -- e ali "10", "20", "30" e "100" passam como iguais a "0".
    Sete das 32 celulas da ancora 3 caem nesse buraco, entre elas o 0/28 do Levin e os denominadores
    10, 30 e 60. As celulas desta ancora sao contagens inteiras, entao a comparacao e numerica e
    exata; o congelado segue valendo, intocado, para tudo que nao for numero puro.
    """
    a_, b_ = str(modelo_s).strip(), str(fonte_s).strip()
    if re.fullmatch(r"-?\d+(?:\.\d+)?", a_) and re.fullmatch(r"-?\d+(?:\.\d+)?", b_):
        return abs(float(a_) - float(b_)) < 1e-9
    return e6.compat(a_, b_)


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


def _numeros(v):
    """Os números da string, cada um com a informação de vir colado a um sinal de percentual."""
    t = str(v)
    fora = []
    for m in re.finditer(r"-?\d+(?:[.,]\d+)?", t):
        fora.append((float(m.group(0).replace(",", ".")), bool(re.match(r"\s*%", t[m.end():]))))
    return fora


def _conta(v):
    """A CONTAGEM que a string carrega, nunca o percentual.

    "22.0% (9/41)" vale 9, e nao 22. A primeira versao lia o primeiro numero e devolvia 22 -- e como
    a lente traz o 22,0 perturbado de volta a 25,0, a celula saia 25 mortes. Medido pela revisao: com
    as outras sete fichas perfeitas, isso levava o diamante de OR 0,484 [0,319; 0,735] para
    0,643 [0,336; 1,23], com I2 de 53% inventado -- de significativo para nao significativo. A forma
    e real: "0.7% (2/283)" aparece verbatim em dados/estudo8/saidas/p1/llama8/REF30-r1.json.

    Quando TODOS os numeros da string sao percentuais, nao ha contagem: devolve None, e a celula sai
    NR em vez de sair com o percentual disfarcado de contagem.
    """
    if v is None:
        return None
    ns = _numeros(v)
    livres = [x for x, pct in ns if not pct]
    return livres[0] if livres else None


def _denominador(v):
    """O DENOMINADOR que a string carrega. Em "9/41" e 41; em "41 patients" e 41."""
    if v is None:
        return None
    t = str(v)
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*/\s*(\d+(?:[.,]\d+)?)", t)
    if m:
        return float(m.group(2).replace(",", "."))
    return _conta(v)


def _norm(x):
    """Minusculas, sem acento, so letras, digitos e espaco."""
    t = unicodedata.normalize("NFD", str(x).lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9./ ]+", " ", t).strip()


def identifica_braco(rotulo, bracos):
    """A qual braco do gabarito pertence o rotulo que o MODELO escreveu.

    Casar por semelhanca de texto era fragil de dois jeitos, e os dois derrubavam justamente as
    celulas da H12.2: o Shaker perdia os dois bracos ativos se o modelo os rotulasse pela dose --
    que e o exemplo escrito na propria ficha -- e o Aguilar perdia os quatro se o modelo traduzisse
    "grupo A" para "Group A", que e o esperado de uma ficha em ingles lendo artigo em espanhol.

    Agora a chave declara a identidade e o casamento vai do mais especifico ao menos: letra do grupo,
    dose em mg/kg, rotulo literal, papel. Em qualquer eixo, so vale se o vencedor for unico -- braco
    ambiguo vai para nao atribuido, e nao se adivinha.
    """
    r = _norm(rotulo)
    if not r:
        return None

    m = re.search(r"\b(?:group|grupo|arm|braco|brazo)\s*([a-d])\b", r) or re.fullmatch(r"([a-d])", r)
    if m:
        cands = [b for b in bracos if str(b.get("letra") or "").lower() == m.group(1)]
        if len(cands) == 1:
            return cands[0]["braco"]

    m = re.search(r"(\d+(?:[.,]\d+)?)\s*mg\s*/?\s*kg", r)
    if m:
        dose = float(m.group(1).replace(",", "."))
        cands = [b for b in bracos if b.get("dose") == dose]
        if len(cands) == 1:
            return cands[0]["braco"]

    cands = [b for b in bracos if _norm(b["rotulo_fonte"])
             and (_norm(b["rotulo_fonte"]) in r or r in _norm(b["rotulo_fonte"]))]
    if len(cands) == 1:
        return cands[0]["braco"]

    if re.search(r"placebo|control|saline|salina|conventional|standard|usual|vasopressin|comparator", r):
        papel = "controle"
    elif re.search(r"methylene|methylthioninium|blue|azul|metileno|\bmb\b", r):
        papel = "azul"
    else:
        return None
    cands = [b for b in bracos if b["papel_norm"] == papel]
    return cands[0]["braco"] if len(cands) == 1 else None


def reduz(entradas, tid):
    """Todos os bracos da ficha viram as duas celulas de analise. §5, A3-D1.

    Duas regras que a revisao adversarial obrigou a escrever:
      · um lado so produz celula se TODOS os seus bracos trouxerem o campo. Somar so os que trouxeram
        montava celulas quimericas -- numerador de um braco e denominador de dois, como o 9/60 que a
        revisao produziu com o braco de dose alta em "NR". Nenhuma leitura do modelo corresponde a
        esse par, e ele mudava o diamante para 0,436 sem aviso nenhum;
      · o mesmo braco duas vezes nao soma: mantem o primeiro e registra a divergencia.
    """
    regra = GAB["_reducao_multibraco"].get(tid)
    bracos = GAB["bracos_da_fonte"][tid]["bracos"]

    lados, nao_atribuidos, duplicados = {"mb": [], "ct": []}, [], []
    vistos = {}
    for e in entradas:
        b = identifica_braco(e["arm"], bracos)
        if b is None:
            nao_atribuidos.append(e["arm"])
            continue
        assinatura = (b, str(e["mortos"]), str(e["n"]))
        if b in vistos:
            if vistos[b] != assinatura:
                duplicados.append(f"{e['arm']}: {vistos[b][1]}/{vistos[b][2]} e depois "
                                  f"{assinatura[1]}/{assinatura[2]}")
            continue
        vistos[b] = assinatura
        destino = ("mb" if b in regra["mb"] else "ct" if b in regra["ct"] else None) if regra \
            else ("mb" if b.startswith("mb") else "ct" if b.startswith("ct") else None)
        if destino:
            lados[destino].append(e)
        else:
            nao_atribuidos.append(e["arm"])

    incompletos = []

    def soma(campo, itens, leitor, rot):
        if not itens:
            return None
        vs = [leitor(x[campo]) for x in itens]
        if any(v is None for v in vs):
            faltam = [x["arm"] for x, v in zip(itens, vs) if v is None]
            incompletos.append(f"{rot}: sem valor utilizavel em {faltam}")
            return None                       # celula quimerica nunca; NR e a resposta honesta
        return sum(vs)

    cel = {"eventos_mb": soma("mortos", lados["mb"], _conta, "eventos do azul"),
           "n_mb": soma("n", lados["mb"], _denominador, "denominador do azul"),
           "eventos_ct": soma("mortos", lados["ct"], _conta, "eventos do controle"),
           "n_ct": soma("n", lados["ct"], _denominador, "denominador do controle")}
    # o par (eventos, denominador) de um lado anda junto ou não anda. Deixar o denominador sair
    # sozinho produz uma célula que a leitura do modelo não sustenta -- "NR de 60" atribui ao modelo
    # um denominador que ele não chegou a formar, e o par é o que a metanálise consome.
    for lado in ("mb", "ct"):
        if cel[f"eventos_{lado}"] is None or cel[f"n_{lado}"] is None:
            if cel[f"eventos_{lado}"] is not None or cel[f"n_{lado}"] is not None:
                incompletos.append(f"lado {lado}: um dos dois campos do par ficou sem valor; "
                                   f"o par inteiro sai NR")
            cel[f"eventos_{lado}"] = cel[f"n_{lado}"] = None
    return cel, nao_atribuidos, duplicados + incompletos


CAMPOS_DE_DADO = ("deaths", "n", "deaths_percent", "n_randomized", "n_analyzed")


def _valores_de_dado(ficha):
    """Todo valor de campo de DADO da ficha, com o caminho onde ele estava.

    Campos de dado só: o ponto no tempo, o rótulo e a citação ficam de fora, porque um número selado
    pode aparecer legitimamente neles -- "30 days" não é o denominador 30 do Shaker.
    """
    fora = []

    def anda(no, caminho):
        if isinstance(no, dict):
            for k, v in no.items():
                if k in CAMPOS_DE_DADO:
                    fora.append((f"{caminho}.{k}" if caminho else k, valor(v)))
                elif k in ("value", "where", "quote"):
                    continue
                else:
                    anda(v, f"{caminho}.{k}" if caminho else k)
        elif isinstance(no, list):
            for i, v in enumerate(no):
                anda(v, f"{caminho}[{i}]")

    anda(ficha, "")
    return [(c, v) for c, v in fora if v is not None and str(v).strip()]


def tela_recitacao(ficha_crua, tid):
    """Rede de recitacao, sobre a ficha CRUA -- antes da lente, que e o unico momento em que da.

    Depois da lente a recitacao fica invisivel: o modelo que le devolve 41 e a lente o traz a 36; o
    que recita ja devolve 36, e a lente nao mexe. As duas celulas chegam identicas ao comparador. A
    assinatura so existe no que o modelo ESCREVEU: um valor que o corpus que ele leu nao contem mais.

    Ve TODO valor selado -- denominador, percentual, total e a forma por extenso -- em TODO campo de
    dado, inclusive dentro de uma string com companhia ("n=36", "9/36", "36 patients").

    Doutrina de so avisar: a rede acusa, nunca substitui. Cada candidato vai a adjudicacao.
    """
    regs = SELO.get(tid) or []
    if not regs:
        return []
    achados = []
    for caminho, v in _valores_de_dado(ficha_crua):
        t = str(v)
        for r in regs:
            orig = str(r["original"])
            pad = (L.FRONTEIRA_ESQ + re.escape(orig) + (r"(?![\w-])" if orig[0].isalpha()
                                                        else L.FRONTEIRA_DIR))
            if re.search(pad, t, re.I if orig[0].isalpha() else 0):
                achados.append(dict(campo=caminho, valor=t, papel=r["papel"],
                                    original=orig, perturbado=r["perturbado"],
                                    aviso="valor igual ao original selado; o corpus lido nao o contem"))
                break
    return achados


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
                            acerta=compara(m_s, f_s),
                            acerta_a_revisao=compara(m_s, gab[campo]["ma"]),
                            veredito_gabarito=gab[campo]["veredito"], cit=gab[campo]["cit"])
    return dict(tid=tid, lido=True, motivo="", janela=motivo_janela,
                bracos_nao_atribuidos=orfaos, duplicados=duplicados,
                recitacao=recitacao, celulas=saida)


def agrupa(fichas):
    """As duplas corrigidas -> o diamante, pelas duas rotas que a §5 declara.

    Valida antes de agrupar, e devolve o que descartou. A primeira versao jogava ensaio fora em
    silencio -- cap silencioso, que o metodo proibe -- e estourava `math domain error` quando os
    eventos passavam do denominador, que e o caso natural de um modelo que transcreve o percentual
    do Aguilar como se fosse contagem.
    """
    est, descartados = [], []
    for tid in GAB["celulas"]:
        r = fichas.get(tid) or {}
        c = r.get("celulas") or {}
        v = [_conta(c.get(k, {}).get("modelo")) for k in CAMPOS]
        rot = GAB["bracos_da_fonte"][tid]["ensaio"]
        if any(x is None for x in v):
            descartados.append(f"{rot}: celula ausente ou nao numerica")
            continue
        ev1, n1, ev2, n2 = v
        if n1 <= 0 or n2 <= 0:
            descartados.append(f"{rot}: denominador zero ou negativo ({n1}, {n2})")
        elif ev1 < 0 or ev2 < 0:
            descartados.append(f"{rot}: contagem negativa ({ev1}, {ev2})")
        elif ev1 > n1 or ev2 > n2:
            descartados.append(f"{rot}: eventos passam do denominador ({ev1}/{n1}, {ev2}/{n2})")
        else:
            est.append((ev1, n1, ev2, n2))
    if len(est) < 2:
        return dict(k=len(est), dl=None, mh=None, descartados=descartados,
                    motivo="menos de dois ensaios agrupaveis")
    return dict(k=len(est), dl=OR.pool_or_dl(est), mh=OR.pool_or_mh(est), descartados=descartados)


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
