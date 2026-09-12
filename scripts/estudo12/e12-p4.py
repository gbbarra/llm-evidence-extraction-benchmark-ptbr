# -*- coding: utf-8 -*-
"""Estudo 12 — Fase 4: adjudicação das células que não bateram com a camada 2, e erratas.

Doutrina (protocolo §7, P4): a citação antes do veredito; nada é apagado; toda saída recusada fica
registrada com o motivo. Esta fase NÃO chama modelo e NÃO reescreve a Fase 2: lê `p2/avaliacao-p2.json`
(as 633 células divergentes), põe cada uma ao lado da chave (valor da fonte, camada publicada, citação)
e do texto que o modelo leu, e classifica por MECANISMO, nas mesmas classes do registro do Estudo 8
(Tabelas S1–S7 do artigo), estendidas às âncoras 2 e 3:

  passes mecânicos (regras nomeadas, cada uma imprime a evidência):
    omission           NR onde a chave tem valor
    lookup-collision   o valor cru já bate com a fonte; a lente de desperturbação o corrompeu
                       (artefato do avaliador -> adjudicado A FAVOR do modelo, regra de 01/09/2026)
    summary            campo qualitativo resumido em vez da enumeração da chave
    re-encoding        os mesmos números em outra codificação (percentual x contagem, a/b, unidade)
    rounding           o mesmo número com menos casas
    layer-choice       outra camada populacional citada pela fonte (alocados x analisados)
    dispersion-type    EP, meia-largura do IC ou DP de outra visita no lugar do DP da mudança
    derived-own-n      o DP derivado pela regra da chave, mas com o n que o próprio modelo leu
    sign-as-printed    sinal como impresso na fonte, que a chave inverteu pela convenção da MA
    self-contradiction a chave já registra que o primário se contradiz nessa célula
    arm-swap · polarity · field-mix · row-slip · unmatched
                       deslizes de leitura: braço trocado; sobreviventes como mortos; percentual na
                       casa do denominador; número de outra linha; número ausente do texto lido
  resíduo: o que nenhuma regra decide vai para o leitor, com o texto aberto, e entra por um
  arquivo de vereditos (`p4/vereditos-leitor.json`), cada um com a citação que decide.

Pontuação: a mecânica (comparador congelado) fica como está; a "adjudicada" soma só as células em
que o modelo estava certo e o avaliador errado (lookup-collision), exatamente como em 01/09/2026.
Nenhuma chave é alterada aqui: itens em que a chave fica sob julgamento são listados para o autor.

Saídas: dados/estudo12/p4/  (adjudicacao-p4.json · adjudicacao-p4.md · residuos.md)
Roda:   python scripts/estudo12/e12-p4.py            (imprime o resumo e os resíduos)
"""
import importlib.util
import io
import json
import math
import os
import re
import sys
import time
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
D12 = RAIZ / "dados" / "estudo12"
P2 = Path(os.environ.get("E12_P2") or (D12 / "p2"))
P4 = Path(os.environ.get("E12_P4") or (D12 / "p4"))
NL = chr(10)
QUEM_LEITOR = "reader (the assistant), under the author's delegation of 2026-09-11; reversible"


def _carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, RAIZ / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


M2 = _carrega("p2m", "scripts/estudo12/e12-p2.py")      # folha, E1, GAB1, GAB2, A, e9, compat, celulas_a2
A3 = M2.A
GAB1, GAB2, GAB3 = M2.GAB1, M2.GAB2, A3.GAB["celulas"]
BRACOS3 = A3.GAB["bracos_da_fonte"]
ELENCO, FICHAS = list(M2.ELENCO), ("v1", "v2")
compat = M2.compat

# ------------------------------------------------------------------ textos: o que o modelo leu, e o original
CORPUS = {
    "a1": ([RAIZ / "corpus" / "perturbados", RAIZ / "corpus" / "perturbados-fechados"],
           [RAIZ / "corpus" / "primarios-texto", RAIZ / "corpus" / "fechados-texto"]),
    "a2": ([RAIZ / "corpus" / "estudo3" / "perturbados"], [RAIZ / "corpus" / "estudo3" / "primarios-texto"]),
    "a3": ([RAIZ / "corpus" / "estudo12" / "perturbados"], [RAIZ / "corpus" / "estudo12" / "original"]),
}
_TXT = {}


def texto(anc, tid, perturbado=True):
    k = (anc, tid, perturbado)
    if k not in _TXT:
        _TXT[k] = ""
        for d in CORPUS[anc][0 if perturbado else 1]:
            f = d / f"{tid}.txt"
            if f.exists():
                _TXT[k] = f.read_text(encoding="utf-8", errors="replace")
                break
    return _TXT[k]


# ------------------------------------------------------------------ números
_NUM = re.compile(r"(?<![\d.])-?\d+(?:\.\d+)?")


def nums(s):
    return [float(x) for x in _NUM.findall(str(s or "").replace("−", "-").replace("–", "-").replace(",", ""))]


def eh_nr(v):
    return str(v or "").strip().upper() in ("NR", "NA", "N/A", "", "NONE", "NOT REPORTED", "NULL", "NAN")


def f(x):
    try:
        return float(str(x).replace("−", "-").replace(",", ""))
    except Exception:
        return None


def eq(a, b, tol=0.0051):
    return a is not None and b is not None and abs(a - b) <= tol


def decimais(s):
    m = re.search(r"\.(\d+)", str(s))
    return len(m.group(1)) if m else 0


def fmt_num(x):
    return str(int(x)) if float(x).is_integer() else (f"{x:.4f}".rstrip("0").rstrip("."))


def no_texto(x, txt):
    """O número aparece, como token, no texto: na forma em que o modelo o escreveu, ou com zeros
    à direita a mais (0.7 casa com 0.70), nunca com MENOS casas (0.43 não casa com 0.4)."""
    if x is None or not txt:
        return False
    base = fmt_num(x).lstrip("-")
    cands = {base}
    if "." in base:
        cands |= {base + "0", base + "00"}
    else:
        cands |= {base + ".0", base + ".00"}
    for c in cands:
        if re.search(r"(?<![\d.])" + re.escape(c) + r"(?![\d])", txt):
            return True
    return False


def imagem_no_selo(anc, tid, valor):
    """Se `valor` (original) foi deslocado pelo selo desse ensaio, devolve a imagem perturbada."""
    if anc == "a2":
        for r in M2.SELO3.get(tid, []):
            if eq(f(r["original"]), valor, 1e-9):
                return f(r["perturbado"])
    return None


def trecho(txt, alvo, larg=80):
    """Um recorte do texto em volta da primeira ocorrência de `alvo` (número ou frase)."""
    if not txt or alvo is None:
        return ""
    if isinstance(alvo, (int, float)):
        cands = [fmt_num(alvo)] + ([f"{alvo:.{d}f}" for d in (1, 2, 3)] if not float(alvo).is_integer() else [])
        pos = -1
        for c in cands:
            m = re.search(r"(?<![\d.])" + re.escape(c.lstrip("-")) + r"(?![\d])", txt)
            if m:
                pos = m.start()
                break
    else:
        pos = txt.find(str(alvo))
    if pos < 0:
        return ""
    a, b = max(0, pos - larg), min(len(txt), pos + larg)
    return ("…" if a > 0 else "") + txt[a:b].replace(NL, " ") + ("…" if b < len(txt) else "")


# ------------------------------------------------------------------ o registro de uma célula
def celula(anc, modelo, ficha, tid, campo, model_val, source, extra=None):
    c = OrderedDict(anchor=anc, model=modelo, sheet=ficha, trial=tid, field=campo,
                    model_value=model_val, source_value=source)
    if extra:
        c.update(extra)
    c.update({"class": None, "verdict": None, "evidence": "", "quote": "", "decided_by": None, "key_on_trial": False})
    return c


def decide(c, classe, veredito, evidencia="", citacao="", por="mechanical rule", chave_sob_julgamento=False):
    c["class"], c["verdict"], c["evidence"], c["quote"] = classe, veredito, evidencia, citacao
    c["decided_by"], c["key_on_trial"] = por, chave_sob_julgamento
    return c


FIEL, ERRO, OMIT, CERTO, RESID = "faithful-different-encoding", "reading-slip", "omission", "model-correct", "residue"


# ------------------------------------------------------------------ âncora 1
_FOLHA = {}


def folha_a1(modelo, ficha, tid):
    k = ("a1", modelo, ficha, tid)
    if k not in _FOLHA:
        r1, _ = M2.folha("a1", ficha, modelo, tid, 1)
        r2, _ = M2.folha("a1", ficha, modelo, tid, 2)
        _FOLHA[k] = r1 or r2
    return _FOLHA[k]


def rev_a1(modelo, ficha, tid, campo):
    js = folha_a1(modelo, ficha, tid)
    if js is None:
        return None
    rev = M2.e9.d6.desperturba(tid, M2.e9.pt_form(js))
    return (rev.get(campo) or {}).get("valor")


def asa_counts(s):
    m = re.fullmatch(r"\s*(\d+):(\d+):(\d+):(\d+)\s*", str(s or ""))
    return [int(x) for x in m.groups()] if m else None


def classifica_a1(c, recit):
    tid, campo, raw = c["trial"], c["field"], c["model_value"]
    g = GAB1[tid][campo]
    fonte, ma, cit, ver = str(g.get("valor_fonte")), str(g.get("ma")), str(g.get("cit") or ""), str(g.get("veredito"))
    c["published_value"], c["key_verdict"], c["key_quote"] = ma, ver, cit[:240]
    orig, pert = texto("a1", tid, False), texto("a1", tid, True)
    rev = rev_a1(c["model"], c["sheet"], tid, campo)
    c["reversed_value"] = rev
    if eh_nr(raw):
        return decide(c, "omission", OMIT, "NR where the source-verified key holds a value",
                      trecho(orig, cit[:40]) or cit[:160])
    if (tid, campo) in recit:
        return decide(c, "recitation-candidate", RESID, "listed by P2's recitation net; adjudicated with the perturbed text",
                      trecho(pert, nums(raw)[0] if nums(raw) else None))
    raw_su = re.sub(r"\s*(mL|ml|min|kg|%)\s*$", "", str(raw)).strip()
    if compat(raw_su, fonte) and not compat(str(rev), fonte):
        return decide(c, "lookup-collision", CERTO,
                      f"raw cell {raw!r} is magnitude-compatible with the key's source value {fonte!r}; the seal "
                      f"reversal produced {rev!r} (a seal pair applied inside the number) — grader-side artifact, "
                      f"2026-09-01 rule", trecho(pert, nums(raw_su)[0]))
    nm, nf = nums(rev), nums(fonte)
    if campo == "tipo_cirurgia":
        if len(nm) < 2:
            return decide(c, "summary", FIEL, "category-level description where the key holds the enumerated case mix",
                          trecho(orig, cit[:40]) or cit[:160])
        return decide(c, "re-encoding-partial", RESID, "enumeration with numbers; compare with the key's case mix", cit[:200])
    if campo.startswith("asa_"):
        K = asa_counts(fonte)
        if K is None:
            return decide(c, "row-slip", RESID, "key ASA value is not a:b:c:d", cit[:200])
        if not nm:
            return decide(c, "labels-only", OMIT, f"no numbers in the cell ({rev!r}); the key holds {fonte}",
                          trecho(orig, "ASA") or cit[:160])
        tot = sum(K)
        n_arm = f(GAB1[tid].get("n_randomizados_" + campo.split("_")[1], {}).get("valor_fonte"))
        alvos = set(K)
        for t in ({tot} | ({n_arm} if n_arm else set())):
            if t:
                alvos |= {round(100 * k / t, 1) for k in K}
                alvos |= {round(100 * (K[i] + K[i + 1]) / t, 1) for i in range(3)}  # categorias agrupadas
                alvos |= {round(100 * (K[i] + K[i + 1] + K[i + 2]) / t, 1) for i in range(2)}
        romanos = {1, 2, 3, 4}
        ruins = [x for x in nm if not any(abs(x - a) <= 1.0 for a in alvos) and x not in romanos]
        if not ruins:
            return decide(c, "re-encoding", FIEL, f"every number in the cell is a count or a percentage of {fonte} "
                          f"(over {tot}{' or n=' + fmt_num(n_arm) if n_arm else ''}); arithmetic verified",
                          trecho(orig, "ASA") or cit[:160])
        return decide(c, "re-encoding-partial", RESID,
                      f"numbers not reconstructible from {fonte}: {', '.join(fmt_num(x) for x in ruins)}",
                      trecho(orig, "ASA") or cit[:160])
    if campo.startswith("n_randomizados"):
        m0 = nm[0] if nm else None
        if m0 is None:
            return decide(c, "row-slip", RESID, f"no number in {rev!r}", cit[:200])
        if ver == "primario-contraditorio":
            return decide(c, "self-contradiction", FIEL,
                          f"the key records that the primary contradicts itself on this cell (verdict "
                          f"'primario-contraditorio'); the model's {fmt_num(m0)} is one of the printed figures",
                          trecho(orig, m0) or cit[:200])
        if eq(m0, f(ma)):
            return decide(c, "layer-choice", FIEL, f"matches the review's analysed layer ({ma}); the key's source "
                          f"layer is the randomized count {fonte}", trecho(orig, m0) or cit[:200])
        if any(eq(m0, x) for x in nums(cit)):
            kot = tid == "REF33" and fmt_num(m0) in ("224", "226")
            return decide(c, "layer-choice", FIEL,
                          f"{fmt_num(m0)} is another population layer quoted in the trial's flow text (key: {fonte})"
                          + ("; Study 1 adjudicated 224/226 'exata' (literal allocation) — key on trial" if kot else ""),
                          trecho(orig, m0) or cit[:200], chave_sob_julgamento=kot)
        if no_texto(m0, orig) or no_texto(nums(raw)[0] if nums(raw) else None, pert):
            return decide(c, "row-slip", RESID, f"{fmt_num(m0)} is printed in the source, not in the flow text",
                          trecho(orig, m0) or trecho(pert, nums(raw)[0]))
        return decide(c, "unmatched", RESID, f"{fmt_num(m0)} is absent from the text the model read", "")
    # campos "a (b%)", contagens, fluidos
    if campo.startswith("laparoscopia") and nm and any(abs(x) > 0 for x in nm):
        k0 = f(fonte)
        for lay in ("valor_fonte", "ma"):
            n_arm = f(GAB1[tid].get("n_randomizados_" + campo.split("_")[1], {}).get(lay))
            if k0 is not None and n_arm and any(abs(x - 100 * k0 / n_arm) <= 0.15 for x in nm):
                return decide(c, "re-encoding", FIEL, f"{fmt_num(nm[0])}% = {fonte}/{fmt_num(n_arm)} × 100 (the "
                              f"{'analysed' if lay == 'ma' else 'randomized'} arm)", trecho(orig, k0) or cit[:160])
    if ver == "ma-inferiu" and not nm:
        return decide(c, "summary", FIEL, f"the key itself records the value as inferred by the review "
                      f"('ma-inferiu': {fonte}); the model wrote {rev!r}", cit[:200] or "(no quotation in the key)")
    nf_nz = [x for x in nf if x != 0]
    pct_src = {x for x in nf if re.search(r"(?<![\d.])" + re.escape(fmt_num(x)) + r"\s*%", fonte.replace(",", ""))}
    n_layers = {f(GAB1[tid].get("n_randomizados_" + campo.split("_")[-1], {}).get(k)) for k in ("valor_fonte", "ma")}
    n_layers.discard(None)

    def bate(x):
        return any(abs(x - y) <= 0.01 or (y in pct_src and abs(x - y) <= 1.0) for y in nf_nz)
    cobre = all(any(abs(y - x) <= 0.01 or (y in pct_src and abs(y - x) <= 1.0) for x in nm) for y in nf_nz)
    extras = [x for x in nm if x != 0 and not bate(x) and not any(abs(x - n) <= 0.01 for n in n_layers)]
    if nf_nz and cobre and not extras:
        return decide(c, "re-encoding", FIEL, f"the cell carries every number of the key ({fonte}) in another format",
                      trecho(orig, nf_nz[0]) or cit[:160])
    if nf_nz and nm and not extras and any(bate(x) for x in nm):
        return decide(c, "re-encoding-partial", FIEL,
                      f"part of the key's numbers ({fonte}) in another format, nothing foreign added",
                      trecho(orig, nf_nz[0]) or cit[:160])
    # o valor do outro braço?
    outro = None
    if campo.endswith("_gdft"):
        outro = campo[:-5] + "_controle"
    elif campo.endswith("_controle"):
        outro = campo[:-9] + "_gdft"
    if outro and outro in GAB1[tid] and nm and compat(str(rev), str(GAB1[tid][outro].get("valor_fonte"))):
        return decide(c, "arm-swap", ERRO, f"the cell equals the other arm's key value "
                      f"({GAB1[tid][outro].get('valor_fonte')})", trecho(orig, nm[0]))
    presentes = [x for x in nums(raw) if no_texto(x, pert)]
    if nm and presentes:
        return decide(c, "row-slip", RESID, f"numbers present in the text read ({', '.join(fmt_num(x) for x in presentes)}) "
                      f"but matching neither the key ({fonte}) nor the other arm", trecho(pert, presentes[0]))
    if nm:
        return decide(c, "unmatched", RESID, "no number of the cell is printed in the text the model read", "")
    return decide(c, "row-slip", RESID, f"non-numeric cell {rev!r}", cit[:160])


# ------------------------------------------------------------------ âncora 2
def folha_a2(modelo, ficha, tid):
    k = ("a2", modelo, ficha, tid)
    if k not in _FOLHA:
        r1, _ = M2.folha("a2", ficha, modelo, tid, 1)
        r2, _ = M2.folha("a2", ficha, modelo, tid, 2)
        _FOLHA[k] = r1 or r2
    return _FOLHA[k]


def celulas_modelo_a2(modelo, ficha, tid):
    js = folha_a2(modelo, ficha, tid)
    if js is None:
        return {}
    try:
        return M2.celulas_a2(js, tid, True)
    except Exception:
        return {}


_HBA1C = 10.929   # % -> mmol/mol (IFCC): 10.929 × % − 23.5 para níveis; diferenças escalam por 10.929


def classifica_a2(c):
    tid, campo, mv = c["trial"], c["field"], c["model_value"]
    g = GAB2[tid]["celulas"][campo]
    k, prov, regra, conta, cit = f(g.get("valor")), str(g.get("proveniencia")), str(g.get("regra") or ""), str(g.get("conta") or ""), str(g.get("cit") or "")
    c["key_provenance"], c["key_rule"], c["key_quote"] = prov, regra, cit[:240]
    orig, pert = texto("a2", tid, False), texto("a2", tid, True)
    braco = campo.split("_")[0]
    if eh_nr(mv):
        return decide(c, "omission", OMIT, "NR where the key holds a value"
                      + (f" (derived: {regra})" if prov == "derivada" else ""), cit[:200] or f"(derived: {conta})")
    m = f(mv)
    if m is None:
        return decide(c, "row-slip", RESID, f"non-numeric cell {mv!r}", cit[:200])
    cel = celulas_modelo_a2(c["model"], c["sheet"], tid)
    n_own = f(cel.get(braco + "_n")) if cel else None
    c["model_own_n"] = n_own
    # 1. a lente falhou: o modelo escreveu exatamente a imagem perturbada da célula da chave
    img = imagem_no_selo("a2", tid, k) if k is not None else None
    if img is not None and (eq(m, img) or eq(m, -img)):
        return decide(c, "lookup-collision", CERTO,
                      f"{fmt_num(m)} is the seal's displaced image of the key's {fmt_num(k)} — the value the model actually "
                      f"read; the reversal lens missed it (sign or format outside the lens's patterns) — grader-side artifact",
                      trecho(pert, img) or cit[:200])
    # 2. a chave deriva a célula (média = final − basal) e o selo deslocou um dos termos: o modelo que
    #    aplica a regra da chave ao texto que leu chega a OUTRO número, que a lente não sabe reverter
    if regra == "media_de_basal_final" and conta:
        termos = nums(conta)[:2]
        if len(termos) == 2:
            fin, bas = termos[0], termos[1]
            if not eq(fin - bas, k, 0.051):          # a ordem em `conta` pode ser basal, final
                fin, bas = bas, fin
            fin_p = imagem_no_selo("a2", tid, fin)
            bas_p = imagem_no_selo("a2", tid, bas)
            if fin_p is not None or bas_p is not None:
                alvo = (fin_p if fin_p is not None else fin) - (bas_p if bas_p is not None else bas)
                if eq(m, alvo, 0.051):
                    return decide(c, "derived-through-seal", CERTO,
                                  f"{fmt_num(m)} = {fmt_num(fin_p if fin_p is not None else fin)} − "
                                  f"{fmt_num(bas_p if bas_p is not None else bas)}: the key's own rule ({regra}) applied to the "
                                  f"perturbed text the model read (final mean displaced by the seal); the lens cannot reverse a "
                                  f"derived quantity — grader-side limit, the model is right",
                                  trecho(pert, fin_p if fin_p is not None else fin) or cit[:200])
    tol_r = max(0.5 * 10 ** (-decimais(mv)), 0.5 * 10 ** (-decimais(g.get("valor")))) + 1e-9
    if k is not None and abs(m - k) <= tol_r and m != k:
        return decide(c, "rounding", FIEL, f"{fmt_num(m)} is {fmt_num(k)} at fewer decimals", cit[:200] or f"(derived: {conta})")
    if k is not None and eq(m, -k):
        if prov.startswith("literal-com-sinal"):
            return decide(c, "sign-as-printed", FIEL, f"the source prints the reduction as {fmt_num(-k)}; the key "
                          f"inverted the sign to the meta-analysis convention", cit[:200])
        return decide(c, "sign", ERRO, f"sign inverted relative to the key ({fmt_num(k)})", cit[:200])
    outro = ("ctl" if braco == "exp" else "exp") + campo[len(braco):]
    if outro in GAB2[tid]["celulas"] and eq(m, f(GAB2[tid]["celulas"][outro].get("valor")), 0.0051):
        return decide(c, "arm-swap", ERRO, f"equals the other arm's key value ({GAB2[tid]['celulas'][outro].get('valor')})",
                      str(GAB2[tid]["celulas"][outro].get("cit") or cit)[:200])
    if campo.endswith("_dispersao"):
        media = GAB2[tid]["celulas"].get(braco + "_media", {})
        cit_m = str(media.get("cit") or "")
        se = n_key = None
        mm = re.search(r"(-?[\d.]+)\s*[×x\*]\s*sqrt\((\d+)\)", conta)
        if mm:
            se, n_key = f(mm.group(1)), f(mm.group(2))
        ci = re.search(r"\(\s*(-?[\d.]+)\s*(?:,|to|a|;)\s*(-?[\d.]+)\s*\)", (cit or cit_m).replace("–", "-").replace("−", "-"))
        hw = se_ci = None
        if ci:
            lo, hi = f(ci.group(1)), f(ci.group(2))
            if lo is not None and hi is not None and hi > lo:
                hw = (hi - lo) / 2
                se_ci = hw / 1.96
        if se is not None and eq(m, se, 0.0051):
            return decide(c, "dispersion-type", FIEL if False else ERRO,
                          f"the standard error printed by the source ({fmt_num(se)}) transcribed as the SD; the key's SD "
                          f"is {conta}", cit[:200] or cit_m[:200])
        if hw is not None and eq(m, hw, 0.0051):
            return decide(c, "dispersion-type", ERRO, f"the CI half-width ({fmt_num(hw)}) written as the SD; key {conta}",
                          (cit or cit_m)[:200])
        if se_ci is not None and eq(m, se_ci, 0.006):
            return decide(c, "dispersion-type", ERRO, f"the SE derived from the CI ({se_ci:.3f}) not scaled by √n; key {conta}",
                          (cit or cit_m)[:200])
        for base, rot in ((se, "SE"), (se_ci, "SE from CI")):
            if base is not None and n_own and eq(m, base * math.sqrt(n_own), 0.011):
                return decide(c, "derived-own-n", FIEL, f"{fmt_num(m)} = {rot} {base:.4g} × √{fmt_num(n_own)}: the key's "
                              f"rule applied with the n the model itself read (key uses n={fmt_num(n_key) if n_key else '?'})",
                              (cit or cit_m)[:200])
        lit = [x for x in nums(conta) if x is not None]
        if any(eq(m, x, 0.0051) for x in lit):
            return decide(c, "dispersion-type", ERRO, f"a literal SD from the quotation (baseline or final visit) instead "
                          f"of the change SD; key {conta}", (cit or cit_m)[:200])
        if any(eq(m, x, 0.0051) for x in nums(cit_m)):
            return decide(c, "row-slip", ERRO, f"{fmt_num(m)} is another figure in the quoted row: {cit_m[:120]}", cit_m[:200])
        if k is not None and eq(m, k * _HBA1C, 0.2):
            return decide(c, "unit", FIEL, f"{fmt_num(m)} ≈ {fmt_num(k)} × 10.929: the same dispersion in mmol/mol", cit[:200])
        if k is not None and n_own and eq(m, k * _HBA1C * math.sqrt(n_own), 0.2):
            return decide(c, "dispersion-type", ERRO, f"{fmt_num(m)} ≈ ({fmt_num(k)} × 10.929) × √{fmt_num(n_own)}: the mmol/mol "
                          f"SD treated as an SE and scaled", cit[:200])
    if campo.endswith("_media"):
        if k is not None and eq(m, k * _HBA1C, 0.15):
            return decide(c, "unit", FIEL, f"{fmt_num(m)} ≈ {fmt_num(k)} × 10.929: the same change in mmol/mol", cit[:200])
        if any(eq(m, x, 0.0051) for x in nums(cit)):
            return decide(c, "row-slip", ERRO, f"{fmt_num(m)} is another figure in the quoted row (a visit mean, not the change)",
                          cit[:200])
        if any(eq(abs(m), abs(x), 0.0051) for x in nums(cit)):
            return decide(c, "row-slip", ERRO, f"{fmt_num(m)} is another figure in the quoted row, with the sign changed", cit[:200])
    if campo.endswith("_n") and campo != "n_randomizado_total":
        tot = f(GAB2[tid]["celulas"].get("n_randomizado_total", {}).get("valor"))
        tot_p = imagem_no_selo("a2", tid, tot) if tot else None
        if tot and (eq(m, tot) or (tot_p is not None and eq(m, tot_p))):
            return decide(c, "row-slip", ERRO, f"{fmt_num(m)} is the trial's total randomized n, written as the arm's n "
                          f"(key: {fmt_num(k)})", trecho(orig, tot) or cit[:200])
    if campo.endswith("_n") or campo == "n_randomizado_total":
        if any(eq(m, x) for x in nums(cit)):
            return decide(c, "layer-choice", FIEL, f"{fmt_num(m)} is another population figure quoted beside the key's "
                          f"({fmt_num(k)})", cit[:200])
        if no_texto(m, orig):
            ctx = trecho(orig, m, 70)
            if re.search(r"complet|analy|per[- ]protocol|withdr|dropout|finish|attend|evaluab", ctx, re.I):
                return decide(c, "layer-choice", FIEL, f"{fmt_num(m)} is printed in a participant-flow context (completers/"
                              f"analysed) where the key holds the randomized {fmt_num(k)}", ctx)
            return decide(c, "row-slip", RESID, f"{fmt_num(m)} is printed in the source, context unclear", ctx)
        return decide(c, "unmatched", RESID, f"{fmt_num(m)} is not printed in the source", "")
    presentes = no_texto(m, pert) or no_texto(m, orig)
    if presentes:
        return decide(c, "row-slip", RESID, f"{fmt_num(m)} is printed in the text; row not identified mechanically",
                      trecho(orig, m) or trecho(pert, m))
    return decide(c, "unmatched", RESID, f"{fmt_num(m)} is not printed in the text the model read", "")


# ------------------------------------------------------------------ âncora 3
def classifica_a3(c, motivo):
    tid, campo, mv = c["trial"], c["field"], c["model_value"]
    g = GAB3[tid][campo]
    fonte, ma, cit, ver = str(g.get("valor_fonte")), str(g.get("ma")), str(g.get("cit") or ""), str(g.get("veredito"))
    c["published_value"], c["key_verdict"], c["key_quote"] = ma, ver, cit[:240]
    orig, pert = texto("a3", tid, False), texto("a3", tid, True)
    braco = "mb" if campo.endswith("_mb") else "ct"
    arms = [b for b in BRACOS3[tid]["bracos"] if (b["papel_norm"] == ("azul" if braco == "mb" else "controle"))]
    if eh_nr(mv):
        return decide(c, "omission", OMIT, "NR where the key holds a value" + (f"; sheet reason: {motivo}" if motivo else ""),
                      cit[:200])
    m = f(mv)
    if c.get("agrees_with_review"):
        return decide(c, "reproduces-review", ERRO, f"equals the review's published cell ({ma}) that the source contradicts "
                      f"({fonte}) — the erratum reproduced", cit[:200])
    if campo.startswith("eventos"):
        for b in arms:
            if eq(m, b["n"] - b["eventos"]):
                return decide(c, "polarity", ERRO, f"{fmt_num(m)} = survivors ({b['n']} − {b['eventos']} deaths): the source "
                              f"publishes survivors and the model reported them as deaths", cit[:200])
        for b in BRACOS3[tid]["bracos"]:
            if eq(m, b["eventos"]) and b["papel_norm"] != ("azul" if braco == "mb" else "controle"):
                return decide(c, "arm-swap", ERRO, f"{fmt_num(m)} is the other arm's death count", cit[:200])
    if campo.startswith("n_"):
        for b in arms:
            if b.get("pct") and eq(m, f(b["pct"]), 0.51):
                return decide(c, "field-mix", ERRO, f"{fmt_num(m)} is the arm's reported percentage ({b['pct']}%), written in "
                              f"the denominator slot", cit[:200])
        for b in BRACOS3[tid]["bracos"]:
            if eq(m, b["n"]) and b["papel_norm"] != ("azul" if braco == "mb" else "controle"):
                return decide(c, "arm-swap", ERRO, f"{fmt_num(m)} is the other arm's denominator", cit[:200])
    if no_texto(m, orig) or no_texto(m, pert):
        return decide(c, "row-slip", RESID, f"{fmt_num(m)} is printed in the text; row not identified mechanically",
                      trecho(orig, m) or trecho(pert, m))
    return decide(c, "unmatched", RESID, f"{fmt_num(m)} is not printed in the text the model read", "")


# ------------------------------------------------------------------ vereditos do leitor (overlay)
def carrega_vereditos():
    p = P4 / "vereditos-leitor.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def _norm(v):
    return re.sub(r"\s+", " ", str(v or "").strip().lower())


def aplica_vereditos(cels, vers):
    usados = Counter()
    for v in vers:
        alvo = (v["anchor"], v["trial"], v["field"], _norm(v.get("model_value")))
        for c in cels:
            if (c["anchor"], c["trial"], c["field"], _norm(c["model_value"])) != alvo:
                continue
            if v.get("models") and c["model"] not in v["models"]:
                continue
            if c["verdict"] != RESID and not v.get("override"):
                continue
            decide(c, v["class"], v["verdict"], v.get("evidence", ""), v.get("quote", ""), QUEM_LEITOR,
                   bool(v.get("key_on_trial")))
            if v.get("note"):
                c["note"] = v["note"]
            usados[json.dumps(alvo, ensure_ascii=False)] += 1
    return usados


# ------------------------------------------------------------------ sensibilidade: os pools da âncora 2 com as células adjudicadas
def pools_adjudicados_a2(cels, R):
    """P3 recomputado com as células em que o modelo estava certo e a lente errada (model-correct) postas
    no valor que a lente devia ter devolvido: o da chave. Sensibilidade, ao lado da primária, nunca no lugar."""
    h3 = M2.h3
    out = OrderedDict()
    certos = {(c["model"], c["sheet"], c["trial"], c["field"]) for c in cels
              if c["anchor"] == "a2" and c["verdict"] == CERTO}
    for m in ELENCO:
        for fch in FICHAS:
            sx, trocas = [], 0
            for tid in h3.TRIALS:
                js = folha_a2(m, fch, tid)
                if js is None:
                    continue
                try:
                    cel = M2.celulas_a2(js, tid, True)
                except Exception:
                    continue
                for k in M2.SEXTETO_A2:
                    if (m, fch, tid, k) in certos:
                        cel[k] = GAB2[tid]["celulas"][k]["valor"]
                        trocas += 1
                v = [cel.get(k) for k in M2.SEXTETO_A2]
                if all(x not in (None, "") for x in v):
                    try:
                        sx.append([float(x) for x in v])
                    except Exception:
                        pass
            adj = h3.pool_dl_md(sx) if len(sx) >= 2 else None
            out[(m, fch)] = dict(p3=R["a2"][m][fch].get("lens"), adjudicado=adj, celulas_trocadas=trocas, estudos=len(sx))
    return out


def releitura_hipoteses(placar, pools_adj):
    """As hipóteses lidas de novo com a pontuação adjudicada. A leitura primária é a da Fase 2."""
    L = []
    g = placar[("a1", "gemma12", "v1")]
    dentro = 99 <= g["adjudicated"] <= 107
    L.append(f"- **H12.5** (context control): gemma12 anchor-1 v1 = {g['mechanical']}/124 mechanical, "
             f"{g['adjudicated']}/124 adjudicated, against the band 103 ± 4 → {'inside' if dentro else 'still outside (above)'}; "
             f"the Phase-2 reading stands: the context is declared a confounder.")
    deltas = []
    for m in ELENCO:
        d = placar[("a1", m, "v2")]["adjudicated"] - placar[("a1", m, "v1")]["adjudicated"]
        deltas.append((m, d))
    med = sum(d for _, d in deltas) / len(deltas)
    L.append(f"- **H12.3**, accuracy criterion under adjudicated scores: mean v2 − v1 on anchor 1 = **{med:+.1f}** cells "
             f"(criterion ≥ −4): " + ", ".join(f"{m} {d:+d}" for m, d in deltas) + f" → {'met' if med >= -4 else 'fails, as in Phase 2'}.")
    alvo = -0.24
    perto = 0
    linhas = []
    for m in ELENCO:
        p1, p2 = pools_adj[(m, "v1")]["adjudicado"], pools_adj[(m, "v2")]["adjudicado"]
        d1 = abs(p1["md"] - alvo) if p1 else None
        d2 = abs(p2["md"] - alvo) if p2 else None
        ok = d1 is not None and d2 is not None and d2 < d1
        perto += ok
        linhas.append(f"{m} v1 {p1['md'] if p1 else '—'} · v2 {p2['md'] if p2 else '—'}{' ✓' if ok else ''}")
    L.append(f"- **H12.3**, estimate criterion on anchor 2 under adjudicated pools (v2 closer to −0.24 than v1): "
             f"{perto} of 6 models ({'; '.join(linhas)}); the criterion needs ≥ 4 on ≥ 2 anchors, and anchors 1 and 3 "
             f"are unchanged by adjudication → fails, as in Phase 2.")
    L.append("- **H12.1, H12.2, H12.4, H12.6**: no adjudicated cell touches anchor 3 or the parse gate; the Phase-2 readings stand "
             "(H12.2: no model reproduced an erratum; 4 of 6 read Aguilar 6/30 and 6 of 6 reduced Shaker to 15/60 on the v1 sheet).")
    return L


# ------------------------------------------------------------------ montagem
def main():
    t0 = time.time()
    av = json.loads((P2 / "avaliacao-p2.json").read_text(encoding="utf-8"))
    R = av["resultados"]
    cels = []
    for anc in ("a1", "a2", "a3"):
        for m in ELENCO:
            for fch in FICHAS:
                r = R[anc][m][fch]
                recit = {(x["trial"], x["field"]) for x in (r.get("recitations") or [])}
                for x in r["divergents"]:
                    extra = {}
                    if anc == "a2":
                        extra["key_provenance"] = x.get("provenance")
                    if anc == "a3":
                        extra["published_value"] = x.get("review")
                        extra["agrees_with_review"] = bool(x.get("agrees_with_review"))
                    c = celula(anc, m, fch, x["trial"], x["field"], x.get("model"), x.get("source"), extra)
                    if anc == "a1":
                        classifica_a1(c, recit)
                    elif anc == "a2":
                        classifica_a2(c)
                    else:
                        motivo = ((r.get("celulas") or {}).get(x["trial"]) or {}).get("motivo") or ""
                        classifica_a3(c, motivo)
                    cels.append(c)
    vers = carrega_vereditos()
    usados = aplica_vereditos(cels, vers)
    nao_usados = [v for v in vers if json.dumps((v["anchor"], v["trial"], v["field"], _norm(v.get("model_value"))),
                                                 ensure_ascii=False) not in usados]

    # pontuação adjudicada por modelo × ficha
    placar = OrderedDict()
    for anc in ("a1", "a2", "a3"):
        for m in ELENCO:
            for fch in FICHAS:
                r = R[anc][m][fch]
                mine = [c for c in cels if (c["anchor"], c["model"], c["sheet"]) == (anc, m, fch)]
                flips = sum(1 for c in mine if c["verdict"] == CERTO)
                placar[(anc, m, fch)] = OrderedDict(
                    mechanical=r["cells"], graded=r["graded"], adjudicated=r["cells"] + flips, flips=flips,
                    divergents=len(mine), omissions=sum(1 for c in mine if c["verdict"] == OMIT),
                    faithful=sum(1 for c in mine if c["verdict"] == FIEL),
                    slips=sum(1 for c in mine if c["verdict"] == ERRO),
                    residue=sum(1 for c in mine if c["verdict"] == RESID),
                    classes=dict(Counter(c["class"] for c in mine)))
    residuos = [c for c in cels if c["verdict"] == RESID]
    kot = [c for c in cels if c["key_on_trial"]]
    pools_adj = pools_adjudicados_a2(cels, R)
    hip = releitura_hipoteses(placar, pools_adj)

    P4.mkdir(parents=True, exist_ok=True)
    reg = OrderedDict(gerado=time.strftime("%Y-%m-%d %H:%M:%S"), fase="P4", fonte_p2=str(P2 / "avaliacao-p2.json"),
                      leitor=QUEM_LEITOR if vers else None, vereditos_do_leitor=len(vers),
                      vereditos_nao_usados=[v for v in nao_usados],
                      placar={f"{a}·{m}·{f_}": v for (a, m, f_), v in placar.items()},
                      pools_a2_adjudicados={f"{m}·{f_}": v for (m, f_), v in pools_adj.items()},
                      hipoteses_releitura=hip,
                      totais=dict(celulas=len(cels), residuos=len(residuos), chave_sob_julgamento=len(kot),
                                  por_veredito=dict(Counter(c["verdict"] for c in cels)),
                                  por_classe=dict(Counter(c["class"] for c in cels))),
                      celulas=cels)
    M2.grava_json(P4 / "adjudicacao-p4.json", reg)
    M2.grava(P4 / "adjudicacao-p4.md", registro_md(reg, placar, cels, kot, residuos, R, pools_adj, hip))
    M2.grava(P4 / "residuos.md", residuos_md(residuos))

    # console
    print(f"P4 · {len(cels)} divergent cells · residue {len(residuos)} · key-on-trial {len(kot)} · "
          f"reader verdicts {len(vers)} ({len(nao_usados)} unused) · {time.time() - t0:.0f} s")
    for anc in ("a1", "a2", "a3"):
        sub = [c for c in cels if c["anchor"] == anc]
        print(f"  {anc}: {len(sub)} · " + " · ".join(f"{k} {v}" for k, v in sorted(Counter(c['verdict'] for c in sub).items())))
        print("      " + " · ".join(f"{k} {v}" for k, v in sorted(Counter(c["class"] for c in sub).items())))
    if residuos:
        print(f"residue by group in {P4 / 'residuos.md'}")
    return True


def registro_md(reg, placar, cels, kot, residuos, R, pools_adj, hip):
    L = ["# Study 12 — Phase 4: adjudication of the cells that failed the layer-2 comparison, and errata", "",
         f"Generated {reg['gerado']} by `scripts/estudo12/e12-p4.py` over `p2/avaliacao-p2.json` "
         f"({reg['totais']['celulas']} cells). No model was called; no key was edited; nothing from Phase 2 was rewritten.", "",
         "**Doctrine.** The quotation before the verdict. Every cell below sits beside the key's source-verified value, "
         "the review's published value where the anchor has one, and the quotation that decides; each verdict names "
         "the rule that produced it. Mechanical rules are the classes of Study 8's Supplementary Tables S1–S7, "
         "extended to anchors 2 and 3; whatever no rule decides is a *residue*, adjudicated by the reader with the "
         "source open and recorded in `vereditos-leitor.json` with its quotation. "
         f"Reader: {QUEM_LEITOR}. The adjudication is reversible: every verdict is a row the author can overturn.", "",
         "**Scores.** The *mechanical* score is the frozen comparator's (Phase 2). The *adjudicated* score adds only the "
         "cells in which the model was right and the grader wrong — the seal-pair lookup collision adjudicated in the "
         "models' favor on 2026-09-01 — and nothing else: faithful re-encodings, population-layer choices and "
         "summaries stay divergent, as in the published record. Cells that put the key on trial are listed for the "
         "author and not flipped.", ""]
    ver_ord = [OMIT, FIEL, ERRO, CERTO, RESID]
    L += ["## Scores per model and sheet", ""]
    for anc, nome in (("a1", "Anchor 1 — 124 cells"), ("a2", "Anchor 2 — 49 cells"), ("a3", "Anchor 3 — 32 cells")):
        L += [f"### {nome}", "", "| model | sheet | mechanical | adjudicated | flips | divergent | omissions | faithful (other encoding/layer) | reading slips | residue |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for (a, m, fch), v in placar.items():
            if a != anc:
                continue
            L.append(f"| {m} | {fch} | {v['mechanical']}/{v['graded']} | **{v['adjudicated']}/{v['graded']}** | {v['flips']} | "
                     f"{v['divergents']} | {v['omissions']} | {v['faithful']} | {v['slips']} | {v['residue']} |")
        L.append("")
    L += ["## Class totals", ""]
    for anc in ("a1", "a2", "a3"):
        sub = [c for c in cels if c["anchor"] == anc]
        cnt = Counter(c["class"] for c in sub)
        L.append(f"- **{anc}** ({len(sub)} cells): " + " · ".join(f"{k} {v}" for k, v in sorted(cnt.items(), key=lambda kv: -kv[1])))
    L.append("")
    flips = [c for c in cels if c["verdict"] == CERTO]
    L += ["## Adjudicated in the models' favor (grader-side artifacts)", ""]
    if flips:
        L += ["| anchor | model | sheet | trial | field | raw cell | after the lens | key | evidence |", "|---|---|---|---|---|---|---|---|---|"]
        for c in flips:
            L.append(f"| {c['anchor']} | {c['model']} | {c['sheet']} | {c['trial']} | {c['field']} | {md(c['model_value'])} | "
                     f"{md(c.get('reversed_value'))} | {md(c['source_value'])} | {md(c['evidence'])} |")
        L.append("")
        L.append(f"Quotation (the text the models read): *{md(flips[0]['quote'])}*")
        L.append("")
    else:
        L += ["None.", ""]
    L += ["## The key on trial (listed for the author; not flipped)", ""]
    if kot:
        vistos = set()
        for c in kot:
            k = (c["anchor"], c["trial"], c["field"], _norm(c["model_value"]))
            if k in vistos:
                continue
            vistos.add(k)
            n = sum(1 for x in kot if (x["anchor"], x["trial"], x["field"], _norm(x["model_value"])) == k)
            L.append(f"- **{c['anchor']} · {c['trial']} · {c['field']}** — model {md(c['model_value'])} ({n} sheets) vs key "
                     f"{md(c['source_value'])}: {md(c['evidence'])}. Quote: *{md(c['quote'])}*")
        L.append("")
    else:
        L += ["None.", ""]
    L += ["## Errata check (anchor 3, H12.2)", ""]
    repro = [c for c in cels if c["anchor"] == "a3" and c["class"] == "reproduces-review"]
    L.append(f"Cells that reproduce the review's erroneous published value instead of the source: **{len(repro)}** "
             f"(Aguilar 24/30 and Shaker 15/30 are the errata; the source values are 6/30 and 15/60). "
             + ("None of the 63 anchor-3 divergences is a reproduced erratum." if not repro else ""))
    L.append("")
    L += ["## Anchor 2 pools under adjudication (sensitivity beside the Phase-3 primary)", "",
          "Phase 3 pooled each model's lens-reversed sextets. Eleven anchor-2 cells were adjudicated in the models' favor "
          "because the lens could not reverse what the model correctly read (a Unicode minus; a change mean derived from a "
          "displaced final mean). Here those cells take the value the lens should have returned — the key's — and the frozen "
          "engine runs again. The Phase-3 pool stays the primary; this column says how much the artifact cost.", "",
          "| model | sheet | Phase-3 lens pool (MD [95% CI]) | adjudicated pool | cells replaced | trials pooled |",
          "|---|---|---|---|---|---|"]
    for (m, fch), v in pools_adj.items():
        p3, ad = v["p3"], v["adjudicado"]
        f3 = f"{p3['md']} [{p3['ic95'][0]}, {p3['ic95'][1]}]" if p3 else "—"
        fa = f"{ad['md']} [{ad['ic95'][0]}, {ad['ic95'][1]}]" if ad else "—"
        L.append(f"| {m} | {fch} | {f3} | {fa} | {v['celulas_trocadas']} | {v['estudos']} |")
    L += ["", "Layer 2: MD −0.24 [−0.32; −0.16].", ""]
    L += ["## The hypotheses, re-read under the adjudicated scores", ""] + hip + [""]
    L += ["## Instrument notes (backlog; never retroactive)", "",
          "- **The reversal lens misses a Unicode minus.** `lente_a2` matches `\"-p\"` and ` p`; a sheet that writes U+2212 "
          "before the displaced image passes through unreversed (deepseek14 v2, REF12). One cell here; the fix is a "
          "normalization step before the lens, for a future ruler.",
          "- **The lens cannot reverse a derived quantity.** When the key derives a cell (change = final − baseline) and the seal "
          "displaces a term, a model that applies the same rule to the text it read lands on a number the lens has never seen "
          "(Goday: 5.3 − 6.9 = −1.6; 7.1 − 6.8 = +0.3). Ten cells, four models, both sheets. The instrument charged the most "
          "careful reading; the anchor-3 seal already recomputes dependent percentages for exactly this reason, and the "
          "anchor-2 seal did not.",
          "- **The eligible set counts an NR cell that carries digits.** Anchor 1's `asa_gdft` for PMC4782303 holds "
          "`NR (elegibilidade ASA 1-3; …)`; the eligibility rule keeps any source value with a digit, so the cell is graded and "
          "only an NR answer can pass it. Three sheets failed it with invented distributions — reading slips in their own "
          "right — but the cell measures nothing about extraction.",
          "- **The comparator's NR and zero rules are literal.** `I:II:III:IV ratio not reported` fails against `NR`; `0 (0)` "
          "fails against `0 (0%)`. Both stay divergent here, as in the published record, and are named in the record.",
          "- **The seal-pair substring collision** (Castro, 31 → 28 inside 1283.2) recurred on all ten sheets that transcribed "
          "the cell; the 2026-09-01 rule flips them. The boundary-aware reversal remains backlog.", ""]
    # célula a célula, por âncora, agrupado por (ensaio, campo, valor)
    L += ["## Cell-by-cell record", "",
          "Grouped by trial, field and model value; the *sheets* column lists model·sheet pairs that wrote that value. "
          "Verdict vocabulary: omission · faithful-different-encoding · reading-slip · model-correct · residue.", ""]
    for anc, nome in (("a1", "Anchor 1 (goal-directed fluid therapy)"), ("a2", "Anchor 2 (low-carbohydrate diet)"),
                      ("a3", "Anchor 3 (methylene blue)")):
        L += [f"### {nome}", "", "| trial | field | model value | sheets | key (source) | published | class | verdict | evidence | quotation | decided by |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        grupos = OrderedDict()
        for c in cels:
            if c["anchor"] != anc:
                continue
            k = (c["trial"], c["field"], _norm(c["model_value"]))
            grupos.setdefault(k, []).append(c)
        for k, lst in sorted(grupos.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
            c = lst[0]
            fichas = ", ".join(f"{x['model']}·{x['sheet']}" for x in lst)
            L.append(f"| {c['trial']} | {c['field']} | {md(c['model_value'])} | {fichas} | {md(c['source_value'])} | "
                     f"{md(c.get('published_value', ''))} | {c['class']} | {c['verdict']} | {md(c['evidence'])} | "
                     f"{md(c['quote'])} | {md(c['decided_by'])} |")
        L.append("")
    if residuos:
        L += ["## Residue still open", "", f"{len(residuos)} cells await the reader; see `residuos.md`.", ""]
    else:
        L += ["## Residue", "", "None: every divergent cell carries a verdict and its quotation.", ""]
    return NL.join(L)


def md(x):
    return str(x if x is not None else "").replace("|", "/").replace(NL, " ")[:220]


def residuos_md(residuos):
    L = ["# Study 12 — Phase 4 residue (cells no mechanical rule decides)", "",
         "Grouped by anchor, trial, field and model value. For each group: the key, the quotation and a snippet of the "
         "text the model read around the model's number. The reader's verdicts go to `vereditos-leitor.json`.", ""]
    grupos = OrderedDict()
    for c in residuos:
        grupos.setdefault((c["anchor"], c["trial"], c["field"], _norm(c["model_value"])), []).append(c)
    for (anc, tid, campo, _), lst in grupos.items():
        c = lst[0]
        L.append(f"## {anc} · {tid} · {campo} · model value `{c['model_value']}` · {len(lst)} sheet(s): "
                 + ", ".join(f"{x['model']}·{x['sheet']}" for x in lst))
        L.append(f"- key: `{c['source_value']}` · published: `{c.get('published_value', '')}` · key verdict/provenance: "
                 f"{c.get('key_verdict', c.get('key_provenance', ''))}")
        L.append(f"- key quote: {c.get('key_quote', '')}")
        L.append(f"- mechanical note: {c['class']} — {c['evidence']}")
        if c.get("reversed_value") not in (None, c["model_value"]):
            L.append(f"- after the lens: `{c.get('reversed_value')}`")
        if c.get("model_own_n") is not None:
            L.append(f"- the model's own n for this arm: {c.get('model_own_n')}")
        if c["quote"]:
            L.append(f"- snippet: {c['quote']}")
        L.append("")
    return NL.join(L)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
