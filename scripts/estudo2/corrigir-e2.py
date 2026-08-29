# -*- coding: utf-8 -*-
"""EXTRAI E2 — corretor mecânico das contas (100% sem juiz de linguagem).

Verdade por célula = recomputação (funções validadas do harness) sobre o INSUMO que o
modelo recebeu — as suas próprias extrações do E1, interpretadas por regras fixas:
  eventos: primeiro inteiro fora de percentual ("19 (32.8%)"→19; "28/39 [..]"→28);
           se só houver percentual e n ("8.6%", n=224) → eventos = pct/100×n;
  n: primeiro inteiro do campo n_randomizados;
  médias: "m ± dp" exigido; mediana(IQR) → verdade indisponível (NC é a resposta certa).

Rótulos por quantidade: exata (|Δ|≤0,01 em RR/IC; ≤0,1 em MD) · direcao-certa ·
errada · nc-correta (NAO-CALCULAVEL onde a verdade é indisponível) · nc-recusa
(NAO-CALCULAVEL onde dava para calcular) · fabricada (número sem insumo) · sem-verdade.

Braço B, adicionalmente: chamadas CALC com argumentos corretos vs errados.

Uso: python corrigir-e2.py   → resumo por modelo×braço + dados/estudo2/correcao/
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D2 = RAIZ / "dados" / "estudo2"
spec = importlib.util.spec_from_file_location("h", RAIZ / "scripts" / "estudo2" / "e2-harness.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def parse_eventos(valor, n=None):
    v = str(valor or "").strip()
    if not v or v.upper().startswith(("NR", "NAO", "NÃO")):
        return None
    m = re.match(r"^\s*(\d+)\s*(?:/\s*\d+)?\s*[\(\[]", v) or re.match(r"^\s*(\d+)\s*$", v) \
        or re.match(r"^\s*(\d+)\s*/", v) or re.match(r"^\s*(\d+)\b(?!\s*%)", v)
    if m:
        return float(m.group(1))
    pm = re.match(r"^\s*(\d+(?:\.\d+)?)\s*%", v)
    if pm and n:
        return round(float(pm.group(1)) / 100 * n, 1)
    return None


def parse_n(valor):
    m = re.search(r"\d+", str(valor or ""))
    return float(m.group(0)) if m else None


def parse_media(valor):
    v = str(valor or "").replace(",", ".")
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:±|\+/-|\+-)\s*(\d+(?:\.\d+)?)", v)
    return (float(m.group(1)), float(m.group(2))) if m else None


def insumo_parseado(mod):
    por = h.estudos_por_desfecho()
    dados = {}
    for desfecho, c_g, c_c in h.CAMPOS_FAM["rr"]:
        for pm in por[desfecho]:
            j = h.extracao(mod, pm)
            ng, nc = parse_n(j.get("n_randomizados_gdft", {}).get("valor")), parse_n(j.get("n_randomizados_controle", {}).get("valor"))
            a = parse_eventos(j.get(c_g, {}).get("valor"), ng)
            c = parse_eventos(j.get(c_c, {}).get("valor"), nc)
            dados[(desfecho, h.ROT[pm])] = (a, ng, c, nc) if None not in (a, ng, c, nc) else None
    for desfecho, c_g, c_c in h.CAMPOS_FAM["md"]:
        for pm in por[desfecho]:
            j = h.extracao(mod, pm)
            mg, mc = parse_media(j.get(c_g, {}).get("valor")), parse_media(j.get(c_c, {}).get("valor"))
            ng, nc = parse_n(j.get("n_randomizados_gdft", {}).get("valor")), parse_n(j.get("n_randomizados_controle", {}).get("valor"))
            dados[(desfecho, h.ROT[pm])] = (mg[0], mg[1], ng, mc[0], mc[1], nc) if mg and mc and ng and nc else None
    return dados


def acha_json(texto):
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto.strip())
    try:
        return json.loads(t)
    except Exception:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


def eh_nc(x):
    return isinstance(x, str) and "CALCULAVEL" in x.upper().replace("Á", "A")


def rotula(par, verdade, tol):
    """par=(valor_modelo, verdade_float)"""
    v, t = par, verdade
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if abs(v - t) <= tol:
        return "exata"
    if (v < 1) == (t < 1) if tol == 0.01 else (v < 0) == (t < 0):
        return "direcao-certa"
    return "errada"


def nome_estudo(chave, rotulos):
    for r in rotulos:
        if r.split()[0].lower() in chave.lower():
            return r
    return None


def corrige(mod, braco, rep, insumo, think=False):
    suf = "-think" if think else ""
    contas = {}
    detalhes = []
    for familia in ("rr", "md", "pool"):
        f = D2 / "saidas" / mod / f"{familia}-{braco}{suf}-r{rep}.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        js = acha_json(d["transcricao"][-1]["saida"])
        if js is None:
            contas["json-invalido"] = contas.get("json-invalido", 0) + 1
            continue
        if familia in ("rr", "md"):
            for desfecho, bloco in js.items():
                if not isinstance(bloco, dict):
                    continue
                for est, val in bloco.items():
                    rot = nome_estudo(est, [r for (dfx, r) in insumo if dfx == desfecho.strip().lower().replace("í", "i")])
                    chave = (desfecho.strip().lower().replace("í", "i"), rot)
                    ins = insumo.get(chave)
                    ponto = val.get("rr") if isinstance(val, dict) else val
                    ponto_md = val.get("md") if isinstance(val, dict) else None
                    ponto = ponto if ponto is not None else ponto_md
                    if ins is None:
                        r = "nc-correta" if (eh_nc(ponto) or ponto is None) else "sem-verdade"
                    elif eh_nc(ponto) or ponto is None:
                        r = "nc-recusa"
                    else:
                        if familia == "rr":
                            t = h.rr(*ins)
                            r = rotula(ponto, t, 0.01)
                        else:
                            t = h.md(*ins)
                            r = rotula(ponto, t, 0.1) if abs(t) > 0.001 else ("exata" if abs(float(ponto)) <= 0.1 else "errada")
                        # IC como quantidade separada
                        ic = val.get("ic95") if isinstance(val, dict) else None
                        if isinstance(ic, list) and len(ic) == 2 and not eh_nc(ic[0]):
                            tic = h.ic95_rr(*ins) if familia == "rr" else h.ic95_md(*ins)
                            try:
                                ric = "exata" if (abs(float(ic[0]) - tic[0]) <= (0.01 if familia == "rr" else 0.1)
                                                  and abs(float(ic[1]) - tic[1]) <= (0.01 if familia == "rr" else 0.1)) else "errada"
                            except (TypeError, ValueError):
                                ric = "errada"
                            contas[f"ic-{ric}"] = contas.get(f"ic-{ric}", 0) + 1
                    if r:
                        contas[r] = contas.get(r, 0) + 1
                        detalhes.append(dict(familia=familia, desfecho=desfecho, estudo=est,
                                             valor=ponto, rotulo=r))
        else:  # pool
            for desfecho, bloco in js.items():
                if not isinstance(bloco, dict):
                    continue
                dnorm = desfecho.strip().lower().replace("í", "i")
                ests = [ins for (dfx, r), ins in insumo.items() if dfx == dnorm and ins]
                if len(ests) < 2:
                    continue
                for metodo, alvo_fn in (("mh", h.pool_rr_mh), ("dl", h.pool_dl), ("iv", h.pool_md_iv)):
                    mv = bloco.get(metodo)
                    if mv is None:
                        continue
                    ponto = mv.get("rr") or mv.get("md") if isinstance(mv, dict) else mv
                    if eh_nc(ponto) or ponto is None:
                        contas["pool-nc"] = contas.get("pool-nc", 0) + 1
                        continue
                    try:
                        t = alvo_fn(ests)
                        tv = t.get("rr") or t.get("md")
                        r = rotula(ponto, tv, 0.01 if metodo != "iv" else 0.1)
                    except Exception:
                        r = "sem-verdade"
                    contas[f"pool-{r}"] = contas.get(f"pool-{r}", 0) + 1
                    detalhes.append(dict(familia="pool", desfecho=desfecho, metodo=metodo,
                                         valor=ponto, rotulo=r))
    return contas, detalhes


def main():
    (D2 / "correcao").mkdir(exist_ok=True)
    print(f"{'modelo':<9} {'braço':<8} {'pontos':>6} {'exatas':>7} {'direção':>8} {'erradas':>8} {'NC-rec':>7} | IC exatas | pool exatas")
    for mod in ("gemma12", "qwen14", "gemma26", "qwen38"):
        insumo = insumo_parseado(mod)
        for braco, think in (("A", False), ("B", False)) + ((("A", True),) if mod == "qwen14" else ()):
            c, det = corrige(mod, braco, 1, insumo, think)
            if not c and not det:
                continue
            ex, di, er = c.get("exata", 0), c.get("direcao-certa", 0), c.get("errada", 0)
            tot = ex + di + er
            icx, ice = c.get("ic-exata", 0), c.get("ic-errada", 0)
            px = c.get("pool-exata", 0)
            ptot = px + c.get("pool-direcao-certa", 0) + c.get("pool-errada", 0)
            rot = braco + ("*" if think else "")
            print(f"{mod:<9} {rot:<8} {tot:>6} {ex:>7} {di:>8} {er:>8} {c.get('nc-recusa',0):>7} | "
                  f"{icx}/{icx+ice:>4}    | {px}/{ptot}")
            (D2 / "correcao" / f"{mod}-{braco}{'-think' if think else ''}.json").write_text(
                json.dumps(dict(contas=c, detalhes=det), ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n(r1; verdade = recomputação sobre o insumo do próprio modelo; detalhes em dados/estudo2/correcao/)")


if __name__ == "__main__":
    main()
