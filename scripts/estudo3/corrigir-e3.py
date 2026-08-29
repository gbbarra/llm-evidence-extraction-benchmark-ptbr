# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — mechanical grader (no language judge; ties go to adjudication).

Grades the four stages against the PERTURBED-source expectation:

E  extraction : each sheet cell vs the perturbed text's value.
               Labels: exata / derivavel / nr-correta (1.0) · omissa / errada (0)
               · recitou (returned the ORIGINAL value where a perturbed one was
               expected; cells with a recorded residual leak grade as
               recitacao-inatribuivel, symmetric) · adjudicar · fora.
A  audit      : per lane. Seeds -> sensitivity, correction accuracy; clean
               fields -> false-alarm rate; plus catches of genuine E errors.
S  (arm)       The expected key below is BUILT from gabarito-fonte.json plus the
               sealed perturbation map, then frozen here explicitly so the
               reader can audit the ruler itself.
C  arithmetic : model's per-study MD/CI and pooled DL vs mechanical recomputation
               over the SAME audited sheets (tolerance ±0.01; pooled also vs the
               anchor's published diamond, rounding allowance §8).
S  synthesis  : word count 250–400; orphan-number check (every number in the
               text must exist in the stage's input).

Run after the queue: python scripts/estudo3/corrigir-e3.py
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D3 = ROOT / "dados" / "estudo3"
SAIDAS = D3 / "saidas"

_spec = importlib.util.spec_from_file_location("h3", ROOT / "scripts" / "estudo3" / "e3-harness.py")
h3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h3)

TRIALS = h3.TRIALS
ROT = h3.ROT

# ---------------------------------------------------------------------------
# Expected sheet key (perturbed-source layer). Built from gabarito-fonte.json +
# the sealed perturbation map (2026-08-29, SHA a8bc6e1a…) and frozen explicitly.
# Per field: aceitos = acceptable strings/numbers (canonical first; matching is
# numeric when both sides parse); original = unperturbed value (returning it
# scores 'recitou' unless vazamento=True -> 'recitacao-inatribuivel').
# 'NR' in aceitos means the text genuinely does not state the field.
# ---------------------------------------------------------------------------
E = "braco_experimental."
C = "braco_controle."


def cel(aceitos, original=None, vazamento=False):
    return dict(aceitos=aceitos if isinstance(aceitos, list) else [aceitos],
                original=original, vazamento=vazamento)


EXPECTED = {
 "PMC5329646": {  # Saslow 2017 — change reported as EMM with CI; baselines perturbed
  E+"n_randomizado": cel([12]), C+"n_randomizado": cel([13]),
  E+"n_analisado": cel(["NR", 12, 11]), C+"n_analisado": cel(["NR", 13, 7]),
  E+"hba1c_mudanca_media": cel([-0.8]), C+"hba1c_mudanca_media": cel([-0.3]),
  E+"hba1c_mudanca_tipo_dispersao": cel(["IC95: -1.1 a -0.6", "IC95"]),
  C+"hba1c_mudanca_tipo_dispersao": cel(["IC95: -0.6 a 0.0", "IC95"]),
  E+"hba1c_basal_media": cel([5.8], original=7.1, vazamento=True),
  C+"hba1c_basal_media": cel([7.6], original=7.2, vazamento=True),
  E+"hba1c_basal_dp": cel([0.4]), C+"hba1c_basal_dp": cel([0.3]),
  E+"hba1c_final_media": cel(["NR"]), C+"hba1c_final_media": cel(["NR"]),
  "n_randomizado_total": cel([25, "NR"]),
 },
 "REF9": {  # Saslow 2023 — factorial margins; SE dispersion; mean and total n perturbed
  E+"n_randomizado": cel(["NR", 45]), C+"n_randomizado": cel(["NR", 49]),
  E+"n_analisado": cel(["NR", 45, 39]), C+"n_analisado": cel(["NR", 49, 42]),
  E+"hba1c_mudanca_media": cel([-0.32], original=-0.35),
  C+"hba1c_mudanca_media": cel([-0.14]),
  E+"hba1c_mudanca_dispersao": cel([0.07]), C+"hba1c_mudanca_dispersao": cel([0.07]),
  E+"hba1c_mudanca_tipo_dispersao": cel(["EP", "SE"]), C+"hba1c_mudanca_tipo_dispersao": cel(["EP", "SE"]),
  E+"hba1c_basal_media": cel([6.09, "NR"]), C+"hba1c_basal_media": cel([6.10, 6.1, "NR"]),
  "n_randomizado_total": cel([83], original=94, vazamento=True),
 },
 "PMC9606840": {  # Dorans 2022 — CI dispersion; mean and total n perturbed
  E+"n_randomizado": cel([75]), C+"n_randomizado": cel([75]),
  E+"n_analisado": cel(["NR", 75]), C+"n_analisado": cel(["NR", 75]),
  E+"hba1c_mudanca_media": cel([-0.24], original=-0.26),
  C+"hba1c_mudanca_media": cel([-0.04]),
  E+"hba1c_mudanca_tipo_dispersao": cel(["IC95: -0.33 a -0.19", "IC95"]),
  C+"hba1c_mudanca_tipo_dispersao": cel(["IC95: -0.10 a 0.02", "IC95"]),
  E+"hba1c_basal_media": cel([6.17, "NR"]), C+"hba1c_basal_media": cel([6.14, "NR"]),
  E+"hba1c_basal_dp": cel([0.31, "NR"]), C+"hba1c_basal_dp": cel([0.30, 0.3, "NR"]),
  "n_randomizado_total": cel([141], original=150),
 },
 "PMC7535044": {  # Chen 2020 — CI dispersion; change, baseline and arm n perturbed
  E+"n_randomizado": cel(["NR", 46]), C+"n_randomizado": cel(["NR", 46]),
  E+"n_analisado": cel([41], original=43), C+"n_analisado": cel([42]),
  E+"hba1c_mudanca_media": cel([-1.44], original=-1.63),
  C+"hba1c_mudanca_media": cel([-1.01]),
  E+"hba1c_mudanca_tipo_dispersao": cel(["IC95: -1.96 a -1.30", "IC95"]),
  C+"hba1c_mudanca_tipo_dispersao": cel(["IC95: -1.40 a -0.63", "IC95"]),
  E+"hba1c_basal_media": cel([9.95], original=8.47),
  C+"hba1c_basal_media": cel([8.70, 8.7]),
  E+"hba1c_basal_dp": cel([1.04]), C+"hba1c_basal_dp": cel([1.01]),
  E+"hba1c_final_media": cel([6.84]), C+"hba1c_final_media": cel([7.69]),
  E+"hba1c_final_dp": cel([0.59]), C+"hba1c_final_dp": cel([1.06]),
  "n_randomizado_total": cel([92]),
 },
 "REF12": {  # Thomsen 2022 — the one literal-SD trial; ctl change, exp baseline, total n perturbed
  E+"n_randomizado": cel(["NR", 34]), C+"n_randomizado": cel(["NR", 33]),
  E+"n_analisado": cel([34]), C+"n_analisado": cel([33]),
  E+"hba1c_mudanca_media": cel([-0.83]),
  C+"hba1c_mudanca_media": cel([-0.56], original=-0.66),
  E+"hba1c_mudanca_dispersao": cel([0.38]), C+"hba1c_mudanca_dispersao": cel([0.37]),
  E+"hba1c_mudanca_tipo_dispersao": cel(["DP", "SD"]), C+"hba1c_mudanca_tipo_dispersao": cel(["DP", "SD"]),
  E+"hba1c_basal_media": cel([8.09], original=7.42),
  C+"hba1c_basal_media": cel([7.40, 7.4]),
  E+"hba1c_basal_dp": cel([0.77]), C+"hba1c_basal_dp": cel([0.70, 0.7]),
  "n_randomizado_total": cel([63], original=72),
 },
 "PMC6024764": {  # Wang 2018 — drop printed positive; change, its SD and total n perturbed
  E+"n_randomizado": cel([28]), C+"n_randomizado": cel([28]),
  E+"n_analisado": cel(["NR", 24, 25, 28]), C+"n_analisado": cel(["NR", 24, 25, 28]),
  E+"hba1c_mudanca_media": cel([0.48, -0.48], original=0.54),
  C+"hba1c_mudanca_media": cel([0.28, -0.28]),
  E+"hba1c_mudanca_dispersao": cel([0.94], original=1.12),
  C+"hba1c_mudanca_dispersao": cel([0.67]),
  E+"hba1c_mudanca_tipo_dispersao": cel(["DP", "SD"]), C+"hba1c_mudanca_tipo_dispersao": cel(["DP", "SD"]),
  "n_randomizado_total": cel([49], original=56),
 },
 "PMC5048014": {  # Goday 2016 — no change reported; finals perturbed
  E+"n_randomizado": cel(["NR", 45]), C+"n_randomizado": cel(["NR", 44, 40]),
  E+"n_analisado": cel([45]), C+"n_analisado": cel([40]),
  E+"hba1c_mudanca_media": cel(["NR"]), C+"hba1c_mudanca_media": cel(["NR"]),
  E+"hba1c_mudanca_tipo_dispersao": cel(["NR"]), C+"hba1c_mudanca_tipo_dispersao": cel(["NR"]),
  E+"hba1c_basal_media": cel([6.9]), C+"hba1c_basal_media": cel([6.8]),
  E+"hba1c_basal_dp": cel([1.1]), C+"hba1c_basal_dp": cel([1.0, 1]),
  E+"hba1c_final_media": cel([5.3], original=6.0),
  C+"hba1c_final_media": cel([7.1], original=6.4),
  E+"hba1c_final_dp": cel([0.7]), C+"hba1c_final_dp": cel([0.8]),
  "n_randomizado_total": cel([89]),
 },
}


def num(x):
    try:
        return float(str(x).replace(",", ".").replace("−", "-").replace("–", "-").strip().rstrip("%"))
    except (TypeError, ValueError):
        return None


def eh_nr(x):
    return str(x).strip().upper() in ("NR", "NA", "N/A", "", "NONE", "NOT REPORTED")


def pega(d, caminho):
    cur = d
    for p in caminho.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def rotula_cel(valor_modelo, esperado):
    aceitos = esperado["aceitos"]
    vm_num = num(valor_modelo)
    if valor_modelo is None:
        return "omissa" if "NR" not in aceitos else "nr-correta"
    if eh_nr(valor_modelo):
        return "nr-correta" if "NR" in aceitos else "omissa"
    for a in aceitos:
        if eh_nr(a):
            continue
        a_num = num(a)
        if a_num is not None and vm_num is not None and abs(a_num - vm_num) <= 0.005:
            return "exata"
        if isinstance(a, str) and a_num is None:
            # type strings (DP/EP/IC95…): substring match either way
            va, vb = str(valor_modelo).upper(), a.upper()
            if vb.split(":")[0].strip() in va or va in vb:
                return "exata"
    org = esperado.get("original")
    if org is not None and vm_num is not None and abs(num(org) - vm_num) <= 0.005:
        return "recitacao-inatribuivel" if esperado.get("vazamento") else "recitou"
    return "adjudicar"


# ---------------- stage E ----------------
def corrige_extracao():
    placar = {}
    detalhes = []
    for tid in TRIALS:
        for rep in (1, 2):
            f = SAIDAS / "extracao" / f"{tid}-r{rep}.json"
            if not f.exists():
                continue
            js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            chave = f"{tid}-r{rep}"
            if not js:
                placar[chave] = dict(parse=False)
                continue
            contas = {}
            for caminho, esperado in EXPECTED[tid].items():
                r = rotula_cel(pega(js, caminho), esperado)
                contas[r] = contas.get(r, 0) + 1
                detalhes.append(dict(trial=tid, rep=rep, campo=caminho,
                                     modelo=pega(js, caminho),
                                     aceitos=esperado["aceitos"], rotulo=r))
            placar[chave] = dict(parse=True, **contas)
    (D3 / "correcao").mkdir(exist_ok=True)
    (D3 / "correcao" / "extracao.json").write_text(
        json.dumps(dict(placar=placar, detalhes=detalhes), ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n== Etapa E (extração, gemma12) — células vs fonte perturbada")
    for chave, c in placar.items():
        if not c.get("parse"):
            print(f"  {chave}: JSON INVÁLIDO")
            continue
        boas = c.get("exata", 0) + c.get("nr-correta", 0) + c.get("derivavel", 0)
        tot = sum(v for k, v in c.items() if k != "parse")
        print(f"  {chave}: {boas}/{tot} " +
              " ".join(f"{k}={v}" for k, v in sorted(c.items()) if k != "parse"))
    return placar


# ---------------- stage A ----------------
def corrige_auditoria():
    sementes = json.loads((D3 / "sementes-auditoria.json").read_text(encoding="utf-8"))["sementes"]
    seeded = {}
    for s in sementes:
        if s["classe"] == "troca-de-braco":
            seeded.setdefault(s["estudo"], []).append(("braco_experimental." + s["campo"], s))
            seeded.setdefault(s["estudo"], []).append(("braco_controle." + s["campo"], s))
        else:
            seeded.setdefault(s["estudo"], []).append((s["campo"], s))
    resultado = {}
    for lane in ("L", "S"):
        entrada_f = SAIDAS / "auditoria" / f"fichas-entrada-{lane}.json"
        if not entrada_f.exists():
            continue
        entrada = json.loads(entrada_f.read_text(encoding="utf-8"))
        linhas = []
        for tid in TRIALS:
            f = SAIDAS / "auditoria" / f"{tid}-{lane}.json"
            if not f.exists():
                continue
            aud = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            vereditos = (aud or {}).get("vereditos", {}) or {}
            ficha = entrada["fichas"][tid]
            for caminho, esperado in EXPECTED[tid].items():
                v_ficha = pega(ficha, caminho)
                r_ficha = rotula_cel(v_ficha, esperado)
                semeada = None
                if lane == "S":
                    for cam, s in seeded.get(tid, []):
                        if cam == caminho:
                            semeada = s
                ver = None
                for k, vv in vereditos.items():
                    if k.strip() == caminho or k.strip().endswith(caminho.split(".")[-1]) and caminho.split(".")[0] in k:
                        ver = vv if isinstance(vv, dict) else {"veredito": str(vv)}
                        break
                veredito = (ver or {}).get("veredito", "sem-veredito")
                corr = (ver or {}).get("valor_corrigido")
                certa = r_ficha in ("exata", "nr-correta")
                linhas.append(dict(lane=lane, trial=tid, campo=caminho,
                                   valor_na_ficha=v_ficha, ficha_estava=r_ficha,
                                   semeada=bool(semeada), classe=(semeada or {}).get("classe"),
                                   veredito=veredito, valor_corrigido=corr,
                                   correcao_bate=(rotula_cel(corr, esperado) in ("exata", "nr-correta")
                                                  if corr is not None else None)))
        resultado[lane] = linhas
    (D3 / "correcao" / "auditoria.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n== Etapa A (auditoria, qwen38)")
    for lane, linhas in resultado.items():
        sem = [l for l in linhas if l["semeada"]]
        pegou = [l for l in sem if l["veredito"] == "corrige"]
        corr_ok = [l for l in pegou if l["correcao_bate"]]
        limpas = [l for l in linhas if not l["semeada"] and l["ficha_estava"] in ("exata", "nr-correta")]
        fa = [l for l in limpas if l["veredito"] == "corrige"]
        print(f"  lane {lane}: campos={len(linhas)}"
              + (f" · sementes {len(pegou)}/{len(sem)} pegas, correção exata {len(corr_ok)}/{len(pegou)}"
                 if lane == "S" else "")
              + f" · falso-alarme {len(fa)}/{len(limpas)}")
        for l in sem:
            print(f"      semente {l['classe']:<14} {l['trial']:<11} {l['campo'].split('.')[-1]:<24}"
                  f" -> {l['veredito']}" + (f" (corrigiu p/ {l['valor_corrigido']})" if l["veredito"] == "corrige" else ""))
    return resultado


# ---------------- stage C ----------------
def sexteto(ficha):
    """Build (m,dp,n) per arm from an audited sheet, mirroring the prompt's rules."""
    out = []
    for br in ("braco_experimental", "braco_controle"):
        b = ficha.get(br, {})
        n = num(b.get("n_analisado"))
        if n is None:
            n = num(b.get("n_randomizado"))
        m = num(b.get("hba1c_mudanca_media"))
        dp = num(b.get("hba1c_mudanca_dispersao"))
        tipo = str(b.get("hba1c_mudanca_tipo_dispersao", "")).upper()
        if m is None:
            b0, b1 = num(b.get("hba1c_basal_media")), num(b.get("hba1c_final_media"))
            if b0 is not None and b1 is not None:
                m = round(b1 - b0, 2)
                d0, d1 = num(b.get("hba1c_basal_dp")), num(b.get("hba1c_final_dp"))
                if d0 is not None and d1 is not None:
                    dp = h3.dp_mudanca_r05(d0, d1)
                    tipo = "DP"
        if tipo.startswith("IC"):
            ms = re.findall(r"-?\d+(?:\.\d+)?", str(b.get("hba1c_mudanca_tipo_dispersao")))
            if len(ms) >= 2 and n:
                dp = h3.dp_de_ic(float(ms[0]), float(ms[1]), n)
        elif tipo in ("EP", "SE") and dp is not None and n:
            dp = h3.dp_de_se(dp, n)
        if m is not None and m > 0 and str(b.get("hba1c_mudanca_media", "")).strip()[0].isdigit():
            m = -m  # drop printed positive (Wang convention)
        out += [m, dp, n]
    return out if all(x is not None for x in out) else None


def corrige_calc():
    print("\n== Etapa C (aritmética, qwen38)")
    resultado = {}
    for lane in ("L", "S"):
        f = SAIDAS / "calc" / f"calc-{lane}.json"
        if not f.exists():
            continue
        cj = json.loads(f.read_text(encoding="utf-8"))
        final = cj.get("json_final") or {}
        sext, usaveis = {}, []
        for tid in TRIALS:
            fs, _ = h3.ficha_auditada(tid, lane)
            s = sexteto(fs)
            sext[ROT[tid]] = s
            if s:
                usaveis.append(s)
        verdade_pool = h3.pool_dl_md(usaveis) if usaveis else None
        linhas = []
        for est in final.get("por_estudo", []):
            nome = est.get("estudo", "")
            chave = next((r for r in sext if r.split()[0].lower() in nome.lower()), None)
            s = sext.get(chave)
            if not s:
                linhas.append(dict(estudo=nome, rotulo="sem-verdade"))
                continue
            vmd = h3.md(*s)
            vic = h3.ic95_md(*s)
            emd, eic = num(est.get("md")), est.get("ic95") or [None, None]
            ok_md = emd is not None and abs(emd - vmd) <= 0.011
            ok_ic = (num(eic[0]) is not None and abs(num(eic[0]) - vic[0]) <= 0.011
                     and abs(num(eic[1]) - vic[1]) <= 0.011)
            linhas.append(dict(estudo=nome, modelo_md=emd, verdade_md=vmd,
                               modelo_ic=eic, verdade_ic=vic,
                               rotulo=("exata" if ok_md and ok_ic else
                                       "md-exata-ic-errada" if ok_md else "errada")))
        ag = final.get("agregado") or {}
        resultado[lane] = dict(fechou=cj.get("fechou"), chamadas=cj.get("chamadas"),
                               fechamentos_forcados=cj.get("fechamentos_forcados"),
                               por_estudo=linhas, agregado_modelo=ag, agregado_verdade=verdade_pool)
        print(f"  lane {lane}: fechou={cj.get('fechou')} chamadas={cj.get('chamadas')} "
              f"fechamentos_forcados={cj.get('fechamentos_forcados')}")
        for l in linhas:
            print(f"      {l.get('estudo', '?'):<22} {l['rotulo']}"
                  + (f"  md {l.get('modelo_md')} vs {l.get('verdade_md')}" if "verdade_md" in l else ""))
        if verdade_pool:
            print(f"      AGREGADO modelo: {json.dumps(ag, ensure_ascii=False)}")
            print(f"      AGREGADO verdade (mesmas fichas): {json.dumps(verdade_pool, ensure_ascii=False)}")
    (D3 / "correcao" / "calc.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    return resultado


# ---------------- stage S ----------------
def corrige_sintese():
    print("\n== Etapa S (síntese, gemma26)")
    resultado = {}
    for lane in ("L", "S"):
        f = SAIDAS / "sintese" / f"sintese-{lane}.json"
        if not f.exists():
            continue
        sj = json.loads(f.read_text(encoding="utf-8"))
        texto = sj["content"]
        palavras = len(texto.split())
        calc = json.loads((SAIDAS / "calc" / f"calc-{lane}.json").read_text(encoding="utf-8"))
        insumo = json.dumps(calc.get("json_final"), ensure_ascii=False)
        for tid in TRIALS:
            fs, _ = h3.ficha_auditada(tid, lane)
            insumo += json.dumps(fs, ensure_ascii=False)
        nums_insumo = set(re.findall(r"\d+(?:\.\d+)?", insumo.replace(",", ".")))
        orfaos = []
        for m in re.findall(r"\d+(?:[.,]\d+)?", texto):
            mn = m.replace(",", ".")
            if mn in nums_insumo or float(mn) < 10 and mn in {str(i) for i in range(10)}:
                continue
            if mn.rstrip("0").rstrip(".") in {x.rstrip("0").rstrip(".") for x in nums_insumo}:
                continue
            orfaos.append(m)
        resultado[lane] = dict(palavras=palavras, na_faixa=250 <= palavras <= 400,
                               numeros_orfaos=orfaos)
        print(f"  lane {lane}: {palavras} palavras ({'na faixa' if 250 <= palavras <= 400 else 'FORA'}) "
              f"· órfãos: {orfaos if orfaos else 'zero'}")
    (D3 / "correcao" / "sintese.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    return resultado


def main():
    corrige_extracao()
    corrige_auditoria()
    corrige_calc()
    corrige_sintese()
    print("\ncorreção mecânica salva em dados/estudo3/correcao/")


if __name__ == "__main__":
    main()
