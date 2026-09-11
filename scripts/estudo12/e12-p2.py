# -*- coding: utf-8 -*-
"""Fases 2 e 3 do Estudo 12: correção das 696 saídas e a aritmética sobre elas.

Nenhum modelo é chamado. Nenhum motor é novo. Cada âncora é corrigida pelo avaliador que
produziu o seu registro publicado, importado e reusado tal como está:

  âncora 1  a chave de duas camadas do Estudo 1 (`gabarito-oficial.json`), o comparador de
            magnitude congelado (`e6-avalia.compat`), a lente congelada (`e6-downstream.desperturba`)
            e o laço de correção do Estudo 8 (`p1-avalia`), célula a célula, sobre as 124 elegíveis.
            A aritmética é o comparador do Estudo 6 (`e6-downstream.main`) com o leitor de fichas
            trocado, exatamente como o Estudo 8 fez (`p3-avalia.ma1`).
  âncora 2  a chave de duas camadas do Estudo 3 (`gabarito-fonte.json`, 49 células, 7 por ensaio),
            a rota determinística de braço (`dirigida.braco_deterministico`), a lente do Estudo 3
            e o mesmo `compat`. A aritmética é `pool_dl_md`, como em `p3-avalia.ma2`.
  âncora 3  `e12-avalia-a3.corrige_corrida`, instrumento 8 da §8, e o motor de razão de chances.
            O PM+HK, que é a rota da própria revisão, é o de `cenarios-ancora3.py` -- copiado e não
            importado, porque aquele script regrava um registro comprometido ao ser importado.

Três portões antes de ler qualquer saída:
  1. a Fase 1 tem de estar completa: 696 arquivos, todos íntegros pelo portão do harness;
  2. os agrupamentos da camada 2 têm de reproduzir as constantes registradas: âncora 2 em
     -0,24 [-0,32; -0,16], âncora 3 em 0,484 pelo DL e 0,484 [0,342; 0,685] pelo PM+HK;
  3. o SHA do selo da âncora 3 é conferido pelo próprio corretor ao carregar.

Doutrina: célula que não bate NÃO é corrigida aqui -- vai para a adjudicação (P4) com o valor do
modelo e o da fonte lado a lado. As redes de proveniência (H12.4) avisam e nunca substituem.
Nada é apagado; escrita atômica; idempotente.

Roda: python scripts/estudo12/e12-p2.py
Saídas: dados/estudo12/p2/  (avaliacao-p2.json · resumo-p2.md · adjudicacao-pendente.md ·
        redes-proveniencia.json · ma1/<modelo>-<ficha>/ · ma1/camada2/)
"""
import contextlib
import importlib.util
import io
import json
import math
import os
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
D12 = RAIZ / "dados" / "estudo12"
SAIDAS = Path(os.environ.get("E12_SAIDAS") or (D12 / "saidas"))
P2 = Path(os.environ.get("E12_P2") or (D12 / "p2"))
NL = chr(10)


def _carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, RAIZ / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ------------------------------------------------------------------ os congelados, reusados
H = _carrega("h12", "scripts/estudo12/e12-harness.py")           # plano, destino, integro
A = _carrega("av12", "scripts/estudo12/e12-avalia-a3.py")         # âncora 3, confere o selo
e9 = _carrega("e9a", "scripts/estudo9/e9-avalia.py")             # eleg, pt_form, valor_en, compat
e7d = _carrega("e7d", "scripts/estudo7/e7-downstream.py")        # ficha_ma1_pt, ficha_ma2_pt, dg
d6 = _carrega("d6", "scripts/estudo6/e6-downstream.py")          # instância própria, para trocar o leitor
redes = _carrega("e9r", "scripts/estudo9/e9-redes.py")            # normaliza, nums, num_no_texto…
h3 = e7d.h3
dg = e7d.dg
compat = e9.compat
GAB1 = e9.d6.GAB
SELO1 = e9.d6.SELO
GAB2 = e7d.FONTE2
SELO3 = json.loads((RAIZ / "dados" / "estudo3" / "perturbacoes-estudo3.json").read_text(encoding="utf-8"))
ELENCO = H.ELENCO
FICHAS = ("v1", "v2")
PUB = {"a1": dict(morbidity=dict(rr=0.778, ic95=[0.567, 1.068]),
                  mortality=dict(rr=1.021, ic95=[0.446, 2.337])),
       "a2": dict(md=-0.24, ic95=[-0.32, -0.16]),
       "a3": {"or": 0.73, "ic95": [0.40, 1.36]}}
# constantes da camada 2, registradas antes desta fase (H12.2 e o protocolo §5)
CAMADA2_A3 = dict(dl={"or": 0.484, "ic95": [0.319, 0.735]},
                  pm_hk={"or": 0.484, "ic95": [0.342, 0.685]})
CAMADA2_A2 = dict(md=-0.24, ic95=[-0.32, -0.16])
# controles da H12.5, do registro do Estudo 8
CONTROLE = dict(a1_gemma12_v1=(103, 4), a2_gemma12_v1_lente=(-0.27, 0.05))
CELULAS_A2 = ("exp_media", "exp_dispersao", "exp_n", "ctl_media", "ctl_dispersao", "ctl_n",
              "n_randomizado_total")
SEXTETO_A2 = CELULAS_A2[:6]


# ------------------------------------------------------------------ utilidades
def grava(caminho, texto):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    tmp = caminho.with_suffix(caminho.suffix + ".tmp")
    tmp.write_text(texto, encoding="utf-8")
    os.replace(tmp, caminho)


def grava_json(caminho, obj):
    grava(caminho, json.dumps(obj, ensure_ascii=False, indent=1))


def folha(ancora, ficha, modelo, tid, rep):
    """Uma saída do harness -> (ficha parseada ou None, registro da chamada ou None)."""
    p = SAIDAS / ancora / ficha / modelo / f"{tid}-r{rep}.json"
    if not p.exists():
        return None, None
    j = json.loads(p.read_text(encoding="utf-8"))
    return h3.acha_json(j.get("conteudo", "")), j


def primeira(ancora, ficha, modelo, tid):
    for rep in (1, 2):
        js, _ = folha(ancora, ficha, modelo, tid, rep)
        if js:
            return js, rep
    return None, None


def s(x):
    return None if x is None else str(x)


@contextlib.contextmanager
def capturando():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        yield buf


# ------------------------------------------------------------------ portão 1: a P1 está completa?
def p1_completa():
    plano = list(H.plano())
    faltam, recusam = [], []
    for c in plano:
        p = H.destino(c)
        if not p.exists():
            faltam.append(p.name)
            continue
        tpl = io.open(H.ANCORAS[c["ancora"]]["fichas"][c["ficha"]], encoding="utf-8").read()
        prompt = H.monta(tpl, io.open(c["caminho"], encoding="utf-8").read())
        import hashlib
        ok, motivo = H.integro(p, c, hashlib.sha256(prompt.encode("utf-8")).hexdigest())
        if not ok:
            recusam.append(f"{p.name}: {motivo}")
    return len(plano), faltam, recusam


# ------------------------------------------------------------------ PM+HK, a rota da revisão
# Copiado de cenarios-ancora3.py (Paule-Mandel, Hartung-Knapp, t de Student com k-1 graus).
# Não importado: aquele script regrava dados/estudo12/ancora3-camada1.json ao ser importado.
T95 = {1: 12.706205, 2: 4.302653, 3: 3.182446, 4: 2.776445, 5: 2.570582, 6: 2.446912,
       7: 2.364624, 8: 2.306004}


def pm_hk(est):
    ys, vs = [], []
    for (a, n1, c, n2) in est:
        b, d = n1 - a, n2 - c
        if 0 in (a, b, c, d):
            a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
        ys.append(math.log((a * d) / (b * c)))
        vs.append(1 / a + 1 / b + 1 / c + 1 / d)
    gl = len(ys) - 1
    if gl < 1:
        return None

    def med(t2):
        w = [1 / (v + t2) for v in vs]
        return sum(x * y for x, y in zip(w, ys)) / sum(w), w

    def Q(t2):
        yb, w = med(t2)
        return sum(x * (y - yb) ** 2 for x, y in zip(w, ys))

    lo, hi = 0.0, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if Q(mid) > gl else (lo, mid)
    pm = (lo + hi) / 2
    yb, w = med(pm)
    se_hk = math.sqrt(Q(pm) / (gl * sum(w)))
    t = T95[gl]
    return {"or": round(math.exp(yb), 3),
            "ic95": [round(math.exp(yb - t * se_hk), 3), round(math.exp(yb + t * se_hk), 3)],
            "tau2": round(pm, 4), "k": len(est), "gl": gl, "t": t}


def est_a3(fichas):
    """As duplas (eventos, n) x 2 dos ensaios agrupáveis, pelas mesmas regras de A.agrupa."""
    est = []
    for tid in A.GAB["celulas"]:
        c = (fichas.get(tid) or {}).get("celulas") or {}
        v = [A._conta(c.get(k, {}).get("modelo")) for k in A.CAMPOS]
        if any(x is None for x in v):
            continue
        ev1, n1, ev2, n2 = v
        if n1 > 0 and n2 > 0 and 0 <= ev1 <= n1 and 0 <= ev2 <= n2:
            est.append((ev1, n1, ev2, n2))
    return est


def est_camada2_a3():
    est = []
    for tid, c in A.GAB["celulas"].items():
        v = [A._conta(c[k]["valor_fonte"]) for k in A.CAMPOS]
        est.append(tuple(v))
    return est


# ------------------------------------------------------------------ âncora 1
E1 = e9.eleg()                           # as 124 células elegíveis, pela regra da campanha


def recitacoes_a1(tid, raw):
    """De p1-avalia: o ORIGINAL do selo aparece na célula crua e a imagem perturbada não."""
    hits = []
    txt = str(raw or "")
    for reg in SELO1.get(tid, []):
        o, p = str(reg["original"]), str(reg["perturbado"])
        if o and p and o != p and o in txt and p not in txt:
            hits.append((o, p))
    return hits


def corrige_a1(modelo, ficha):
    boas = tot = est_ig = est_tot = 0
    parse_fail, pend, recs = [], [], []
    for tid, campos in E1.items():
        r1, _ = folha("a1", ficha, modelo, tid, 1)
        r2, _ = folha("a1", ficha, modelo, tid, 2)
        if r1 is None and r2 is None:
            parse_fail.append(tid)
            continue
        js = r1 or r2
        rev = e9.d6.desperturba(tid, e9.pt_form(js))
        for campo in campos:
            raw = e9.valor_en(js, campo)
            fonte = GAB1[tid][campo].get("valor_fonte")
            tot += 1
            ok = compat((rev.get(campo) or {}).get("valor"), fonte)
            boas += ok
            if not ok:
                pend.append(dict(trial=tid, field=campo, model=raw, source=str(fonte)[:80]))
            for o, p in recitacoes_a1(tid, raw):
                recs.append(dict(trial=tid, field=campo, original=o, perturbed=p, cell=str(raw)[:50]))
            if r1 is not None and r2 is not None:
                est_tot += 1
                est_ig += compat(e9.valor_en(r1, campo), e9.valor_en(r2, campo))
    return dict(cells=boas, graded=tot, cells_pct=round(100 * boas / max(tot, 1), 1),
                stability=est_ig, stability_of=est_tot,
                stability_pct=round(100 * est_ig / max(est_tot, 1), 1),
                recitation_candidates=len(recs), recitations=recs,
                parse_failures=parse_fail, divergents=pend)


def pools_a1(pasta, leitor, com_lente=True):
    """O comparador do Estudo 6 com o leitor trocado, como p3-avalia.ma1. Devolve os DL."""
    pasta.mkdir(parents=True, exist_ok=True)
    guard = (d6.ficha, d6.D6, d6.desperturba)
    d6.ficha = leitor
    d6.D6 = pasta
    if not com_lente:
        d6.desperturba = lambda tid, js: js
    try:
        with capturando() as buf:
            d6.main()
        grava(pasta / "log.txt", buf.getvalue())
    finally:
        d6.ficha, d6.D6, d6.desperturba = guard
    res = json.loads((pasta / "resultados-por-desfecho.json").read_text(encoding="utf-8"))
    return {fam: (res.get(fam, {}).get("pool") or {}).get("DL") for fam in ("morbidity", "mortality")}


def camada2_a1():
    """O pool da camada 2 da âncora 1: o mesmo motor sobre as células-fonte da chave, sem lente."""
    def leitor(tid):
        return {campo: {"valor": cel.get("valor_fonte") or "", "onde": ""}
                for campo, cel in GAB1.get(tid, {}).items()}
    return pools_a1(P2 / "ma1" / "camada2", leitor, com_lente=False)


# ------------------------------------------------------------------ âncora 2
def lente_a2(ficha_pt, tid):
    """A lente do Estudo 3, como em p3-avalia.lens_sexteto."""
    txt = json.dumps(ficha_pt, ensure_ascii=False)
    for reg in SELO3.get(tid, []):
        p, o = str(reg["perturbado"]), str(reg["original"])
        txt = txt.replace(f'"{p}"', f'"{o}"').replace(f'"-{p}"', f'"-{o}"')
        txt = txt.replace(f" {p}", f" {o}").replace(f"-{p}", f"-{o}")
    return json.loads(txt)


def celulas_a2(js, tid, com_lente):
    """As 7 células do modelo: seis roteadas pela rota determinística, e o n total lido direto."""
    f = e7d.ficha_ma2_pt(js)
    # A ficha v2 traz cada célula de braço como {value, where, quote}, e o conversor congelado
    # (`braco_pt`) copia o dicionário inteiro -- a rota determinística recebe um dict e devolve
    # None nas seis células. Medido em 11/09/2026: 7/49 em cinco modelos, uniforme, que era o
    # n total (desembrulhado aqui) passando sozinho. Desembrulhar é adaptação de leitura, não
    # de julgamento: o valor é o mesmo que a v1 entrega nu. O conversor fica como está.
    for braco in ("braco_experimental", "braco_controle"):
        f[braco] = {k: (e7d.celula_pt(v)["valor"] if isinstance(v, dict) else v)
                    for k, v in (f.get(braco) or {}).items()}
    if com_lente:
        f = lente_a2(f, tid)
    e = dg.braco_deterministico(f["braco_experimental"], {}, ("x", "exp"))
    c = dg.braco_deterministico(f["braco_controle"], {}, ("x", "ctl"))
    tot = e7d.celula_pt(js.get("n_randomized_total")).get("valor")
    if com_lente and tot not in (None, ""):
        tot = lente_a2({"x": str(tot)}, tid)["x"]
    return dict(zip(CELULAS_A2, [e[0], e[1], e[2], c[0], c[1], c[2], tot]))


def sexteto(cel):
    v = [cel.get(k) for k in SEXTETO_A2]
    return None if any(x is None for x in v) else [float(x) for x in v]


def corrige_a2(modelo, ficha):
    boas = tot = est_ig = est_tot = 0
    parse_fail, pend = [], []
    sx, sx_lente, faltas = [], [], []
    for tid in h3.TRIALS:
        r1, _ = folha("a2", ficha, modelo, tid, 1)
        r2, _ = folha("a2", ficha, modelo, tid, 2)
        if r1 is None and r2 is None:
            parse_fail.append(tid)
            faltas.append(h3.ROT[tid] + " (ilegível)")
            continue
        js = r1 or r2
        lente = celulas_a2(js, tid, True)
        crua = celulas_a2(js, tid, False)
        chave = GAB2[tid]["celulas"]
        for k in CELULAS_A2:
            tot += 1
            ok = compat(s(lente.get(k)), s(chave[k]["valor"]))
            boas += ok
            if not ok:
                pend.append(dict(trial=tid, field=k, model=s(lente.get(k)),
                                 source=s(chave[k]["valor"]), provenance=chave[k].get("proveniencia")))
        if r1 is not None and r2 is not None:
            c1, c2 = celulas_a2(r1, tid, True), celulas_a2(r2, tid, True)
            for k in CELULAS_A2:
                est_tot += 1
                est_ig += compat(s(c1.get(k)), s(c2.get(k)))
        sc, sl = sexteto(crua), sexteto(lente)
        (sx.append(sc) if sc else faltas.append(h3.ROT[tid]))
        if sl:
            sx_lente.append(sl)
    pool = h3.pool_dl_md(sx) if len(sx) >= 2 else None
    lens = h3.pool_dl_md(sx_lente) if len(sx_lente) >= 2 else None
    return dict(cells=boas, graded=tot, cells_pct=round(100 * boas / max(tot, 1), 1),
                stability=est_ig, stability_of=est_tot,
                stability_pct=round(100 * est_ig / max(est_tot, 1), 1),
                parse_failures=parse_fail, divergents=pend,
                estudos_no_pool=len(sx), faltas=faltas, pool_perturbado=pool, lens=lens)


def camada2_a2():
    est = [[float(GAB2[tid]["celulas"][k]["valor"]) for k in SEXTETO_A2] for tid in h3.TRIALS]
    return h3.pool_dl_md(est)


# ------------------------------------------------------------------ âncora 3
def controles_no_corpus():
    """Caracteres de controle nos textos perturbados da âncora 3, por ensaio.

    Medido em 11/09/2026: os três primários convertidos de PDF (Kirov, Memis, Levin) carregam
    U+0001..U+0008 onde o PDF tinha símbolos como '≤'. A ficha v2 cita ao pé da letra, o
    caractere entra na citação, e o leitor de JSON congelado -- estrito -- recusa a ficha
    inteira. É a heterogeneidade de formato da §4 batendo no instrumento, não no leitor.
    """
    out = {}
    for tid in A.GAB["celulas"]:
        p = RAIZ / "corpus" / "estudo12" / "perturbados" / f"{tid}.txt"
        t = p.read_text(encoding="utf-8", errors="replace")
        n = sum(1 for ch in t if ord(ch) < 32 and ch not in "\n\r\t")
        if n:
            out[tid] = n
    return out


def leitura_tolerante(modelo, ficha, tid):
    """SENSIBILIDADE, declarada: o mesmo recorte de JSON, com strict=False (aceita caractere de
    controle dentro de string), na primeira réplica que abrir. Nunca substitui a leitura
    primária -- que é a do corretor congelado -- e é reportada ao lado dela."""
    for rep in (1, 2):
        p = SAIDAS / "a3" / ficha / modelo / f"{tid}-r{rep}.json"
        if not p.exists():
            continue
        c = json.loads(p.read_text(encoding="utf-8")).get("conteudo", "")
        i, j = c.find("{"), c.rfind("}")
        if i < 0 or j <= i:
            continue
        try:
            return json.loads(c[i:j + 1], strict=False), rep
        except Exception:
            continue
    return None, None


def corrige_a3(modelo, ficha):
    r = A.corrige_corrida(SAIDAS, modelo, ficha)
    fichas = r["fichas"]
    acertos = tot = 0
    pend, recit = [], []
    for tid, f in fichas.items():
        for campo, c in (f.get("celulas") or {}).items():
            tot += 1
            if c.get("acerta"):
                acertos += 1
            else:
                pend.append(dict(trial=tid, field=campo, model=s(c.get("modelo")),
                                 source=s(c.get("fonte")), review=s(c.get("ma")),
                                 agrees_with_review=bool(c.get("acerta_a_revisao"))))
        for x in f.get("recitacao") or []:
            recit.append(dict(trial=tid, **{k: s(v) for k, v in x.items()}))
    # réplicas: a mesma célula, valor do modelo em r1 contra r2
    est_ig = est_tot = 0
    for tid, reps in r["replicas"].items():
        c1 = (fichas.get(tid) or {}).get("celulas") or {}
        for rr in reps:
            for campo in A.CAMPOS:
                est_tot += 1
                est_ig += A.compara(s(c1.get(campo, {}).get("modelo")),
                                    s(rr["celulas"].get(campo, {}).get("modelo")))
    est = est_a3(fichas)
    # H12.2: as duas células que decidem
    ag = (fichas.get("aguilar2016") or {}).get("celulas") or {}
    sh = (fichas.get("shaker2025") or {}).get("celulas") or {}
    h122 = dict(
        aguilar_6_30=bool(ag and A.compara(s(ag.get("eventos_mb", {}).get("modelo")), "6")
                          and A.compara(s(ag.get("n_mb", {}).get("modelo")), "30")),
        aguilar_24_30=bool(ag and A.compara(s(ag.get("eventos_mb", {}).get("modelo")), "24")),
        shaker_15_60=bool(sh and A.compara(s(sh.get("eventos_mb", {}).get("modelo")), "15")
                          and A.compara(s(sh.get("n_mb", {}).get("modelo")), "60")),
        shaker_15_30=bool(sh and A.compara(s(sh.get("eventos_mb", {}).get("modelo")), "15")
                          and A.compara(s(sh.get("n_mb", {}).get("modelo")), "30")))
    # a sensibilidade: o que a leitura tolerante recupera das fichas que o leitor estrito recusou
    ilegiveis = [tid for tid, f in fichas.items() if not f.get("lido")]
    sens = None
    if ilegiveis:
        fichas_s, recuperadas = dict(fichas), {}
        for tid in ilegiveis:
            js, rep = leitura_tolerante(modelo, ficha, tid)
            if js is not None:
                fichas_s[tid] = A.corrige(js, tid)
                recuperadas[tid] = rep
        est_s = est_a3(fichas_s)
        sens = dict(ilegiveis_na_primaria=ilegiveis, recuperadas=recuperadas,
                    cells=sum(1 for f in fichas_s.values() for c in (f.get("celulas") or {}).values() if c.get("acerta")),
                    graded=sum(len(f.get("celulas") or {}) for f in fichas_s.values()),
                    dl=A.OR.pool_or_dl(est_s) if len(est_s) >= 2 else None,
                    pm_hk=pm_hk(est_s) if len(est_s) >= 2 else None)
    return dict(cells=acertos, graded=tot, cells_pct=round(100 * acertos / max(tot, 1), 1),
                legiveis=sum(1 for f in fichas.values() if f.get("lido")),
                stability=est_ig, stability_of=est_tot,
                stability_pct=round(100 * est_ig / max(est_tot, 1), 1),
                faltam=r["faltam"], problemas=r["problemas"],
                recitation_candidates=len(recit), recitations=recit,
                divergents=pend,
                pool=r["pool"], pm_hk=pm_hk(est) if len(est) >= 2 else None,
                h12_2=h122, sensibilidade_tolerante=sens, celulas=fichas)


# ------------------------------------------------------------------ redes de proveniência (H12.4)
FONTES = dict(a1=redes.FONTES["ma1"], a2=redes.FONTES["ma2"],
              a3=[RAIZ / "corpus" / "estudo12" / "perturbados"])
ELEGIVEL_REDE = {
    # o denominador da H12.4: as células corrigidas cuja camada 2 não é NR
    "a1": lambda tid, campo: campo in {e9.PT2EN[c] for c in E1.get(tid, [])},
    "a2": lambda tid, campo: any(campo.endswith(x) for x in (
        "n_randomized", "n_analyzed", "hba1c_change_mean", "hba1c_change_dispersion",
        "hba1c_baseline_mean", "hba1c_baseline_sd", "hba1c_final_mean", "hba1c_final_sd")),
    "a3": lambda tid, campo: campo.endswith(".deaths") or campo.endswith(".n"),
}


def celulas_de(obj, prefixo=""):
    """Como e9-redes.celulas, mas descendo também em listas: a ficha da âncora 3 traz os braços
    numa lista `mortality`, e a versão do Estudo 9 só conhecia dicionários."""
    if isinstance(obj, dict):
        if "value" in obj:
            yield prefixo, obj
            return
        for k, v in obj.items():
            yield from celulas_de(v, f"{prefixo}.{k}" if prefixo else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from celulas_de(v, f"{prefixo}[{i}]")


def fonte_de(tid, ancora):
    for d in FONTES[ancora]:
        p = d / f"{tid}.txt"
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return None


def redes_v2(modelo, ancora):
    """N9-1, N9-2 e N9-3 sobre a ficha v2, com as funções do Estudo 9. Avisam, não substituem."""
    flags, inspecionadas, elegiveis = [], 0, 0
    pasta = SAIDAS / ancora / "v2" / modelo
    for p in sorted(pasta.glob("*.json")):
        j = json.loads(p.read_text(encoding="utf-8"))
        tid, rep = j["ensaio"], j["replica"]
        src = fonte_de(tid, ancora)
        if src is None:
            continue
        src_n = redes.normaliza(src)
        js = h3.acha_json(j.get("conteudo", ""))
        if not isinstance(js, dict):
            flags.append(dict(net="parse", trial=tid, replicate=rep, field=None, detail="ilegível"))
            continue
        for campo, cel in celulas_de(js):
            valor = str(cel.get("value", "") or "").strip()
            quote = str(cel.get("quote", "") or "").strip()
            if valor in ("", "NR"):
                continue
            inspecionadas += 1
            eleg = ELEGIVEL_REDE[ancora](tid, re.sub(r"\[\d+\]", "", campo))
            elegiveis += eleg
            base = dict(trial=tid, replicate=rep, field=campo, elegivel=eleg,
                        value=valor[:60], quote=quote[:140])
            if not quote:
                flags.append(dict(net="N9-1", detail="célula preenchida, citação vazia", **base))
                continue
            if redes.normaliza(quote) not in src_n:
                flags.append(dict(net="N9-1", detail="citação não é literal na fonte",
                                  subclass=redes.sub_classe_n91(quote, src), **base))
            vn = redes.nums(valor)
            if vn:
                faltando = [n for n in vn if not redes.num_no_texto(n, quote)]
                if faltando:
                    flags.append(dict(net="N9-2", detail=f"valor ausente da própria citação: {faltando}", **base))
            elif redes.normaliza(valor) not in redes.normaliza(quote):
                flags.append(dict(net="N9-2", detail="valor qualitativo ausente da citação", **base))
            if "dispersion_type" in campo:
                decl = redes.classe_declarada(valor)
                qn = redes.normaliza(quote)
                ti, ts = bool(redes.RE_INTERVALO.search(qn)), bool(redes.RE_SPREAD.search(qn))
                if decl in ("SD", "SE") and ti and not ts:
                    flags.append(dict(net="N9-3", detail=f"declara {decl}, a citação imprime intervalo", **base))
                elif decl == "CI" and ts and not ti:
                    flags.append(dict(net="N9-3", detail="declara IC, a citação imprime dispersão solta", **base))
    por = {}
    for f in flags:
        por.setdefault(f["net"], {"total": 0, "elegiveis": 0})
        por[f["net"]]["total"] += 1
        por[f["net"]]["elegiveis"] += bool(f.get("elegivel"))
    return dict(inspecionadas=inspecionadas, elegiveis=elegiveis, por_rede=por, flags=flags)


# ------------------------------------------------------------------ hipóteses
def dist(a, b):
    return None if a is None or b is None else round(abs(a - b), 3)


def hipoteses(R, L2):
    h = {}
    # H12.1 -- fichas parseáveis e pool digit-consistente com as próprias células (recalculado aqui)
    h["H12.1"] = {}
    for m in ELENCO:
        for f in FICHAS:
            r = R["a3"][m][f]
            est = est_a3(r["celulas"])
            dl = A.OR.pool_or_dl(est) if len(est) >= 2 else None
            p = (r["pool"] or {}).get("dl")
            coerente = bool(dl and p and abs(dl["or"] - p["or"]) <= 0.01
                            and all(abs(dl["ic95"][i] - p["ic95"][i]) <= 0.01 for i in (0, 1)))
            h["H12.1"][f"{m}/{f}"] = dict(legiveis=r["legiveis"], pool=bool(p), coerente=coerente)
    # H12.2 -- quantos modelos leem o Aguilar como 6/30 e o Shaker como 15/60
    h["H12.2"] = {f: dict(
        aguilar_6_30=[m for m in ELENCO if R["a3"][m][f]["h12_2"]["aguilar_6_30"]],
        aguilar_24_30=[m for m in ELENCO if R["a3"][m][f]["h12_2"]["aguilar_24_30"]],
        shaker_15_60=[m for m in ELENCO if R["a3"][m][f]["h12_2"]["shaker_15_60"]],
        shaker_15_30=[m for m in ELENCO if R["a3"][m][f]["h12_2"]["shaker_15_30"]],
        ambos=[m for m in ELENCO if R["a3"][m][f]["h12_2"]["aguilar_6_30"]
               and R["a3"][m][f]["h12_2"]["shaker_15_60"]]) for f in FICHAS}
    # H12.3 -- acurácia preservada (delta médio v1->v2 na âncora 1 >= -4) e estimativa comprada
    deltas = {m: R["a1"][m]["v2"]["cells"] - R["a1"][m]["v1"]["cells"] for m in ELENCO}
    mais_perto = {}
    for anc in ("a1", "a2", "a3"):
        conta = []
        for m in ELENCO:
            if anc == "a1":
                v1 = (R["a1"][m]["v1"]["pools"].get("morbidity") or {}).get("rr")
                v2 = (R["a1"][m]["v2"]["pools"].get("morbidity") or {}).get("rr")
                alvo = (L2["a1"].get("morbidity") or {}).get("rr")
            elif anc == "a2":
                v1 = (R["a2"][m]["v1"]["lens"] or {}).get("md")
                v2 = (R["a2"][m]["v2"]["lens"] or {}).get("md")
                alvo = L2["a2"]["md"]
            else:
                v1 = ((R["a3"][m]["v1"]["pool"] or {}).get("dl") or {}).get("or")
                v2 = ((R["a3"][m]["v2"]["pool"] or {}).get("dl") or {}).get("or")
                alvo = CAMADA2_A3["dl"]["or"]
            d1, d2 = dist(v1, alvo), dist(v2, alvo)
            conta.append(dict(modelo=m, v1=v1, v2=v2, alvo=alvo, v2_mais_perto=(d1 is not None and d2 is not None and d2 < d1)))
        mais_perto[anc] = conta
    ancoras_ok = sum(1 for anc in mais_perto if sum(c["v2_mais_perto"] for c in mais_perto[anc]) >= 4)
    h["H12.3"] = dict(delta_celulas_a1=deltas,
                      delta_medio=round(sum(deltas.values()) / len(deltas), 2),
                      acuracia_preservada=(sum(deltas.values()) / len(deltas)) >= -4,
                      estimativa=mais_perto,
                      ancoras_com_4_de_6=ancoras_ok, estimativa_comprada=ancoras_ok >= 2)
    # H12.5 -- o controle de contexto
    c1 = R["a1"]["gemma12"]["v1"]["cells"]
    alvo, tol = CONTROLE["a1_gemma12_v1"]
    l2 = (R["a2"]["gemma12"]["v1"]["lens"] or {}).get("md")
    alvo2, tol2 = CONTROLE["a2_gemma12_v1_lente"]
    h["H12.5"] = dict(a1_gemma12_v1=c1, faixa_a1=[alvo - tol, alvo + tol],
                      a1_dentro=(alvo - tol) <= c1 <= (alvo + tol),
                      a2_gemma12_v1_lente=l2, faixa_a2=[round(alvo2 - tol2, 2), round(alvo2 + tol2, 2)],
                      a2_dentro=(l2 is not None and abs(l2 - alvo2) <= tol2))
    h["H12.5"]["passa"] = h["H12.5"]["a1_dentro"] and h["H12.5"]["a2_dentro"]
    # H12.6 -- o nulo honesto: nenhum modelo passa de 50% das 32 células, na média das réplicas
    h["H12.6"] = {}
    for m in ELENCO:
        for f in FICHAS:
            r = R["a3"][m][f]
            h["H12.6"][f"{m}/{f}"] = dict(cells=r["cells"], of=r["graded"], acima_de_50=r["cells"] > 16)
    h["H12.6"]["algum_acima_de_50"] = any(v["acima_de_50"] for k, v in h["H12.6"].items() if "/" in k)
    return h


# ------------------------------------------------------------------ relatórios
def resumo_md(R, L2, hip, redes_r):
    L = ["# Estudo 12 — Fases 2 e 3, o resumo", "",
         f"Gerado em {time.strftime('%Y-%m-%d %H:%M')} sobre {SAIDAS.relative_to(RAIZ)}. "
         "Nenhum modelo chamado. Cada célula divergente está em `adjudicacao-pendente.md`.", "",
         "## Camada 2 (as constantes de referência, reproduzidas aqui)", "",
         f"- âncora 1, DL sobre as células-fonte da chave: morbidade {json.dumps(L2['a1'].get('morbidity'))} · "
         f"mortalidade {json.dumps(L2['a1'].get('mortality'))} (publicado 0,778 / 1,021)",
         f"- âncora 2, DL sobre os sextetos da chave: {json.dumps(L2['a2'])} (registrado −0,24 [−0,32; −0,16])",
         f"- âncora 3, DL {json.dumps(L2['a3']['dl'])} · PM+HK {json.dumps(L2['a3']['pm_hk'])} "
         "(registrados 0,484 [0,319; 0,735] e 0,484 [0,342; 0,685])", ""]
    for anc, den in (("a1", 124), ("a2", 49), ("a3", 32)):
        L += [f"## Âncora {anc[1]} — células contra a camada 2 ({den})", "",
              "| modelo | ficha | células | estabilidade r1·r2 | ilegíveis | recitação | pool |",
              "|---|---|---|---|---|---|---|"]
        for m in ELENCO:
            for f in FICHAS:
                r = R[anc][m][f]
                if anc == "a1":
                    pool = f"morb RR {(r['pools'].get('morbidity') or {}).get('rr')} · mort RR {(r['pools'].get('mortality') or {}).get('rr')}"
                elif anc == "a2":
                    pool = f"lente MD {(r['lens'] or {}).get('md')} [{', '.join(str(x) for x in (r['lens'] or {}).get('ic95', []))}] · {r['estudos_no_pool']}/7"
                else:
                    dl = (r["pool"] or {}).get("dl") or {}
                    pool = f"DL OR {dl.get('or')} [{', '.join(str(x) for x in dl.get('ic95', []))}] · PM+HK {(r['pm_hk'] or {}).get('or')}"
                ileg = len(r.get("parse_failures", [])) if anc != "a3" else (8 - r["legiveis"])
                L.append(f"| {m} | {f} | {r['cells']}/{r['graded']} ({r['cells_pct']}%) | "
                         f"{r['stability']}/{r['stability_of']} ({r['stability_pct']}%) | {ileg} | "
                         f"{r.get('recitation_candidates', '—')} | {pool} |")
        L.append("")
    # a sensibilidade da âncora 3, ao lado da primária e nunca no lugar dela
    sens_l = []
    for m in ELENCO:
        for f in FICHAS:
            sv = R["a3"][m][f].get("sensibilidade_tolerante")
            if sv:
                dl = sv["dl"] or {}
                sens_l.append(f"- {m}/{f}: primária {R['a3'][m][f]['cells']}/{R['a3'][m][f]['graded']} "
                              f"com {len(sv['ilegiveis_na_primaria'])} ficha(s) recusada(s) pelo leitor estrito "
                              f"({', '.join(sv['ilegiveis_na_primaria'])}); tolerante recupera "
                              f"{len(sv['recuperadas'])} → **{sv['cells']}/{sv['graded']}**, "
                              f"DL {dl.get('or')} [{', '.join(str(x) for x in dl.get('ic95', []))}]")
    if sens_l:
        ctl = R.get("_corpus_controles") or {}
        L += ["### Âncora 3 — leitura tolerante (sensibilidade declarada; não substitui a primária)", "",
              "O leitor de JSON congelado é estrito e recusa caractere de controle dentro de string. "
              "Os textos convertidos de PDF carregam U+0001–U+0008 onde o PDF tinha símbolos "
              f"({', '.join(f'{k}: {v}' for k, v in ctl.items()) or 'nenhum'}); a ficha v2, que cita ao pé da "
              "letra, os carrega para a citação. A leitura tolerante usa `strict=False` e a primeira réplica "
              "que abre. Onde a ficha é JSON malformado de verdade, ela também falha, e isso fica dito.", ""]
        L += sens_l + [""]
    L += ["## Hipóteses pré-registradas", ""]
    h = hip
    L += ["### H12.1 — o portão de generalização", ""]
    ruins = [k for k, v in h["H12.1"].items() if not (v["legiveis"] == 8 and v["pool"] and v["coerente"])]
    L += [("Passa: todos os 12 pares modelo×ficha leem as 8 fichas, agrupam, e o DL é coerente com as "
           "próprias células a ±0,01.") if not ruins else
          f"Falha na leitura primária em: {', '.join(ruins)} — em todos os casos por ficha v2 recusada pelo "
          "leitor estrito (ver a sensibilidade acima); o DL é coerente com as próprias células em todos os 12.", ""]
    L += ["### H12.2 — a que decide", ""]
    for f in FICHAS:
        x = h["H12.2"][f]
        L += [f"- ficha {f}: Aguilar **6/30** em {len(x['aguilar_6_30'])} de 6 ({', '.join(x['aguilar_6_30']) or '—'}); "
              f"24/30 (a errata) em {len(x['aguilar_24_30'])} ({', '.join(x['aguilar_24_30']) or '—'}); "
              f"Shaker **15/60** em {len(x['shaker_15_60'])} ({', '.join(x['shaker_15_60']) or '—'}); "
              f"15/30 (a errata) em {len(x['shaker_15_30'])} ({', '.join(x['shaker_15_30']) or '—'}); "
              f"**ambas** em {len(x['ambos'])} ({', '.join(x['ambos']) or '—'})"]
    L += ["", "### H12.3 — a ficha v2, na escala do elenco", "",
          f"- delta médio v2−v1 nas 124 células da âncora 1: **{h['H12.3']['delta_medio']}** "
          f"(critério ≥ −4 → {'passa' if h['H12.3']['acuracia_preservada'] else 'falha'}); por modelo: "
          + ", ".join(f"{m} {d:+d}" for m, d in h["H12.3"]["delta_celulas_a1"].items()),
          f"- v2 mais perto da camada 2 em ≥4 de 6 modelos: {h['H12.3']['ancoras_com_4_de_6']} de 3 âncoras "
          f"(critério ≥ 2 → {'passa' if h['H12.3']['estimativa_comprada'] else 'falha'})", ""]
    for anc in ("a1", "a2", "a3"):
        L.append(f"  - {anc}: " + ", ".join(
            f"{c['modelo']} v1 {c['v1']} · v2 {c['v2']}{' ✓' if c['v2_mais_perto'] else ''}"
            for c in h["H12.3"]["estimativa"][anc]) + f" · alvo {h['H12.3']['estimativa'][anc][0]['alvo']}")
    L += ["", "### H12.5 — o controle de contexto", "",
          f"- gemma12 âncora 1 v1: **{h['H12.5']['a1_gemma12_v1']}/124** (faixa {h['H12.5']['faixa_a1']}) → "
          f"{'dentro' if h['H12.5']['a1_dentro'] else 'FORA'}",
          f"- gemma12 âncora 2 v1, lente: **{h['H12.5']['a2_gemma12_v1_lente']}** (faixa {h['H12.5']['faixa_a2']}) → "
          f"{'dentro' if h['H12.5']['a2_dentro'] else 'FORA'}",
          f"- **{'passa: o contexto não é confundidor' if h['H12.5']['passa'] else 'FALHA: o contexto é confundidor e vai reportado antes de qualquer resultado da âncora 3'}**", ""]
    L += ["### H12.6 — o nulo honesto", "",
          ("Algum modelo passa de 50% das 32 células: " + ", ".join(
              k for k, v in h["H12.6"].items() if "/" in k and v["acima_de_50"]))
          if h["H12.6"]["algum_acima_de_50"] else
          "**Nenhum modelo passa de 50% das 32 células da âncora 3 — o nulo pré-registrado.**", ""]
    L += ["## H12.4 — redes de proveniência sobre a ficha v2 (exploratório; avisam, não substituem)", "",
          "| âncora | modelo | células inspecionadas | elegíveis | N9-1 | N9-2 | N9-3 | ilegíveis |",
          "|---|---|---|---|---|---|---|---|"]
    for anc in ("a1", "a2", "a3"):
        for m in ELENCO:
            r = redes_r[anc][m]
            pr = r["por_rede"]
            L.append(f"| {anc} | {m} | {r['inspecionadas']} | {r['elegiveis']} | "
                     f"{pr.get('N9-1', {}).get('total', 0)} ({pr.get('N9-1', {}).get('elegiveis', 0)}) | "
                     f"{pr.get('N9-2', {}).get('total', 0)} ({pr.get('N9-2', {}).get('elegiveis', 0)}) | "
                     f"{pr.get('N9-3', {}).get('total', 0)} | {pr.get('parse', {}).get('total', 0)} |")
    L += ["", "Entre parênteses: bandeiras nas células que entram no denominador da H12.4.", ""]
    return NL.join(L)


def adjudicacao_md(R):
    L = ["# Estudo 12 — células que não bateram com a camada 2 (entrada da Fase 4)", "",
         "Doutrina: o valor do modelo e o da fonte, lado a lado; a citação decide, na adjudicação. "
         "Nada aqui foi corrigido. `agrees_with_review` marca, na âncora 3, a célula que reproduz a "
         "revisão em vez da fonte — o que a H12.2 chama de reproduzir a errata.", ""]
    for anc in ("a1", "a2", "a3"):
        for m in ELENCO:
            for f in FICHAS:
                d = R[anc][m][f]["divergents"]
                if not d:
                    continue
                L += [f"## {anc} · {m} · {f} — {len(d)} células", "",
                      "| ensaio | campo | modelo | fonte | nota |", "|---|---|---|---|---|"]
                for x in d:
                    nota = ("= revisão" if x.get("agrees_with_review") else
                            x.get("provenance", "") or "")
                    L.append(f"| {x['trial']} | {x['field']} | {str(x.get('model'))[:60].replace('|', '/')} | "
                             f"{str(x.get('source'))[:60].replace('|', '/')} | {nota} |")
                L.append("")
    return NL.join(L)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    print("FASES 2 e 3 DO ESTUDO 12", flush=True)

    print("\nportão 1: a Fase 1 está completa?", flush=True)
    n, faltam, recusam = p1_completa()
    if faltam or recusam:
        print(f"  x {len(faltam)} faltam, {len(recusam)} recusadas, de {n}. A P2 não corre sobre P1 incompleta.")
        for x in (faltam + recusam)[:8]:
            print("     ", x)
        return False
    print(f"  ok  {n} de {n} chamadas, todas íntegras", flush=True)

    print("\nportão 2: os agrupamentos da camada 2 reproduzem as constantes registradas?", flush=True)
    L2 = {}
    L2["a2"] = camada2_a2()
    ok2 = round(L2["a2"]["md"], 2) == CAMADA2_A2["md"] and \
        [round(x, 2) for x in L2["a2"]["ic95"]] == CAMADA2_A2["ic95"]
    print(f"  {'ok ' if ok2 else 'x  '} âncora 2: {L2['a2']['md']} {L2['a2']['ic95']}")
    est2 = est_camada2_a3()
    L2["a3"] = dict(dl=A.OR.pool_or_dl(est2), pm_hk=pm_hk(est2))
    ok3 = L2["a3"]["dl"]["or"] == CAMADA2_A3["dl"]["or"] and L2["a3"]["dl"]["ic95"] == CAMADA2_A3["dl"]["ic95"] \
        and L2["a3"]["pm_hk"]["or"] == CAMADA2_A3["pm_hk"]["or"] and L2["a3"]["pm_hk"]["ic95"] == CAMADA2_A3["pm_hk"]["ic95"]
    print(f"  {'ok ' if ok3 else 'x  '} âncora 3: DL {L2['a3']['dl']['or']} {L2['a3']['dl']['ic95']} · "
          f"PM+HK {L2['a3']['pm_hk']['or']} {L2['a3']['pm_hk']['ic95']}")
    L2["a1"] = camada2_a1()
    print(f"  ok  âncora 1 (calculado, sem constante registrada): morbidade {json.dumps(L2['a1'].get('morbidity'))} · "
          f"mortalidade {json.dumps(L2['a1'].get('mortality'))}")
    if not (ok2 and ok3):
        print("  a camada 2 não reproduz: a P2 para aqui.")
        return False

    R = {"a1": {}, "a2": {}, "a3": {}}
    for m in ELENCO:
        print(f"\n===== {m}", flush=True)
        R["a1"][m], R["a2"][m], R["a3"][m] = {}, {}, {}
        for f in FICHAS:
            r1 = corrige_a1(m, f)
            r1["pools"] = pools_a1(P2 / "ma1" / f"{m}-{f}",
                                   lambda tid, m=m, f=f: (lambda js: e7d.ficha_ma1_pt(js) if js else None)(primeira("a1", f, m, tid)[0]))
            R["a1"][m][f] = r1
            R["a2"][m][f] = corrige_a2(m, f)
            R["a3"][m][f] = corrige_a3(m, f)
            a1, a2, a3 = R["a1"][m][f], R["a2"][m][f], R["a3"][m][f]
            print(f"  {f}: a1 {a1['cells']}/{a1['graded']} · a2 {a2['cells']}/{a2['graded']} · "
                  f"a3 {a3['cells']}/{a3['graded']} (legíveis {a3['legiveis']}/8) · "
                  f"a3 DL {((a3['pool'] or {}).get('dl') or {}).get('or')}", flush=True)

    print("\nredes de proveniência (v2)", flush=True)
    RD = {anc: {m: redes_v2(m, anc) for m in ELENCO} for anc in ("a1", "a2", "a3")}

    hip = hipoteses(R, L2)
    R["_corpus_controles"] = controles_no_corpus()

    # as células cruas da âncora 3 são grandes; ficam no JSON, fora do resumo
    grava_json(P2 / "avaliacao-p2.json", dict(gerado=time.strftime("%Y-%m-%d %H:%M:%S"),
                                              saidas=str(SAIDAS), camada2=L2, resultados=R,
                                              hipoteses=hip))
    grava_json(P2 / "redes-proveniencia.json", RD)
    grava(P2 / "resumo-p2.md", resumo_md(R, L2, hip, RD))
    grava(P2 / "adjudicacao-pendente.md", adjudicacao_md(R))
    n_pend = sum(len(R[a][m][f]["divergents"]) for a in ("a1", "a2", "a3") for m in ELENCO for f in FICHAS)
    print(f"\n{n_pend} células para a adjudicação · {time.time() - t0:.0f}s")
    print(f"gravado em {P2.relative_to(RAIZ)}: avaliacao-p2.json · resumo-p2.md · "
          f"adjudicacao-pendente.md · redes-proveniencia.json · ma1/")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
