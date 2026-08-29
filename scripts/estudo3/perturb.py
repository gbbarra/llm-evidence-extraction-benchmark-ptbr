# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — perturbation of the 7 primary texts (reading proof).

Study-1 operator (corrected boundaries, semantic windows, leak checks) over a
HAND-CURATED target list: the reconnaissance (verify-source.py + gabarito-fonte)
already identified each trial's arithmetic-critical facts AND the numeric
collisions to avoid (Thomsen's 0.83 doubles as a p-value; Dorans's 0.31 as a
baseline SD; Goday's 89 lives inside the '32–89 g' range; Saslow 2017's 0.8/0.3
double as unrelated SDs), so automatic candidate mining is replaced by curation.

Every occurrence of a chosen fact is replaced (multi-site facts stay coherent);
a target is DROPPED (loudly) if any of its occurrence windows fails the semantic
anchor — no silent partial perturbation.

Output (out of repo): corpus/estudo3/perturbados/<ID>.txt +
dados/estudo3/perturbacoes-estudo3.json (sealed until grading is published).
"""
import json
import random
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
TXT = ROOT / "corpus" / "estudo3" / "primarios-texto"
OUT = ROOT / "corpus" / "estudo3" / "perturbados"
SEAL = ROOT / "dados" / "estudo3" / "perturbacoes-estudo3.json"

HBA = r"HbA\s?1c|hemoglobin|glycated|glyc[ae]mic"
NRAND = r"randomi|allocated|assigned|enrolled|recruited|participants|patients|subjects|group"

# (field-in-key, value-as-in-text, anchor regex, max occurrences[, veto_apos])
# veto_apos: occurrences immediately followed by this regex are a DIFFERENT fact
# — they are excluded from replacement and recorded as a residual leak (E1
# Amendment-3 treatment: recitation unattributable for that value, symmetric).
TARGETS = {
    "PMC5329646": [  # Saslow 2017 — EMM/CI strings collide across rows; perturb the
        # baseline table cells and VETO the weight-CI twins by what follows the
        # number ("-7.1, -0.1" and "7.2 (-9.0, 23.4)" are different facts; their
        # leftovers are recorded as residual leaks, E1 Amendment-3 treatment)
        ("exp_basal_media", "7.1", HBA, 2, r","),
        ("ctl_basal_media", "7.2", HBA, 2, r"\s?\((–|-)"),
    ],
    "REF9": [        # Saslow 2023
        ("exp_media", "0.35", HBA, 3),
        ("n_randomizado_total", "94", NRAND, 6, r"%"),
    ],
    "PMC9606840": [  # Dorans 2022
        ("exp_media", "0.26", HBA, 3),
        ("n_randomizado_total", "150", NRAND, 6),
    ],
    "PMC7535044": [  # Chen 2020
        ("exp_media", "1.63", HBA, 3),
        ("exp_basal_media", "8.47", HBA, 2),
        ("exp_n", "43", NRAND + r"|LCD", 4),
    ],
    "REF12": [       # Thomsen 2022
        ("exp_basal_media", "7.42", HBA, 2),
        ("ctl_media", "0.66", HBA, 3),
        ("n_randomizado_total", "72", NRAND, 3),
    ],
    "PMC6024764": [  # Wang 2018
        ("exp_media", "0.54", HBA + r"|MD", 2),
        ("exp_dp", "1.12", HBA + r"|MD", 2),
        ("n_randomizado_total", "56", NRAND, 3),
    ],
    "PMC5048014": [  # Goday 2016 — 89 and 45 excluded (range/multi-fact collisions)
        ("exp_final_media", "6.0", HBA, 3),
        ("ctl_final_media", "6.4", HBA, 3),
    ],
}


def ocorre(texto, valor):
    """Occurrence spans with the corrected E1 boundaries."""
    spans = []
    for m in re.finditer(r"(?<![\d.,])" + re.escape(valor) + r"(?!\d|\.\d)", texto):
        i = m.start()
        antes = texto[i - 1] if i else ""
        if antes.isalpha() or antes == "_":
            continue
        if antes in "-–—−":
            antes2 = texto[i - 2] if i >= 2 else ""
            if antes2.isalpha():
                continue  # word-hyphen glue stays out; minus signs and ranges are in
        spans.append((m.start(), m.end()))
    return spans


def substitui(texto, valor, novo):
    spans = ocorre(texto, valor)
    out, ultimo = [], 0
    for a, b in spans:
        out.append(texto[ultimo:a])
        out.append(novo)
        ultimo = b
    out.append(texto[ultimo:])
    return "".join(out), len(spans)


def perturba(valor, rng, texto):
    casas = len(valor.split(".")[1]) if "." in valor else 0
    v = float(valor)
    for _ in range(60):
        fator = rng.uniform(0.05, 0.18) * rng.choice((1, -1))
        novo = round(v * (1 + fator), casas)
        if casas == 0:
            novo = int(novo)
        s = f"{novo:.{casas}f}" if casas else str(novo)
        if s != valor and float(s) > 0 and not ocorre(texto, s):
            return s
    return None


def substitui_spans(texto, spans, novo, tam):
    out, ultimo = [], 0
    for a, b in spans:
        out.append(texto[ultimo:a])
        out.append(novo)
        ultimo = b
    out.append(texto[ultimo:])
    return "".join(out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    selo = {}
    for tid, alvos in TARGETS.items():
        texto = (TXT / f"{tid}.txt").read_text(encoding="utf-8")
        rng = random.Random(f"EXTRAI-E3-{tid}")
        pert, registros = texto, []
        print(f"\n===== {tid}")
        for alvo in alvos:
            campo, valor, ancora, max_occ = alvo[:4]
            veto_apos = alvo[4] if len(alvo) > 4 else None
            spans = ocorre(texto, valor)
            vetados = []
            if veto_apos:
                mantidos = []
                for a, b in spans:
                    if re.match(veto_apos, texto[b:b + 4]):
                        vetados.append((a, b))
                    else:
                        mantidos.append((a, b))
                spans = mantidos
            janelas = [texto[max(0, a - 120):b + 120] for a, b in spans]
            problema = None
            if not spans:
                problema = "0 ocorrências"
            elif len(spans) > max_occ:
                problema = f"{len(spans)} ocorrências > máx {max_occ}"
            elif not all(re.search(ancora, j, re.I) for j in janelas):
                ruins = sum(1 for j in janelas if not re.search(ancora, j, re.I))
                problema = f"{ruins}/{len(janelas)} janelas sem âncora"
            if problema:
                print(f"  DROP {campo} ({valor}): {problema}")
                for a, b in spans[:6]:
                    print(f"      …{re.sub(chr(92)+'s+', ' ', texto[max(0, a-60):b+60])}…")
                continue
            novo = perturba(valor, rng, texto)
            if novo is None:
                print(f"  DROP {campo} ({valor}): sem substituto sem vazamento")
                continue
            # scoped replacement: recompute spans against the CURRENT perturbed
            # text (positions shift only if an earlier target overlapped, which
            # curation forbids), then replace only non-vetoed spans
            spans_pert = ocorre(pert, valor)
            if veto_apos:
                spans_pert = [(a, b) for a, b in spans_pert
                              if not re.match(veto_apos, pert[b:b + 4])]
            pert = substitui_spans(pert, spans_pert, novo, len(valor))
            ctxs = [re.sub(r"\s+", " ", texto[max(0, a - 45):b + 45]) for a, b in spans]
            reg = dict(campo=campo, original=valor, perturbado=novo,
                       ocorrencias=len(spans_pert), contextos=ctxs)
            if vetados:
                reg["vazamento_residual"] = [re.sub(r"\s+", " ", texto[max(0, a - 45):b + 45])
                                             for a, b in vetados]
            registros.append(reg)
            print(f"  OK  {campo}: {valor} -> {novo} (×{len(spans_pert)}"
                  + (f", {len(vetados)} vetada(s) como fato distinto" if vetados else "") + ")")
            for c in ctxs:
                print(f"      …{c}…")
            for a, b in vetados:
                print(f"      VETO: …{re.sub(chr(92)+'s+', ' ', texto[max(0, a-45):b+45])}…")
        (OUT / f"{tid}.txt").write_text(pert, encoding="utf-8")
        selo[tid] = registros
    SEAL.write_text(json.dumps(selo, ensure_ascii=False, indent=2), encoding="utf-8")
    tot = sum(len(v) for v in selo.values())
    print(f"\n{tot} perturbações seladas -> {SEAL.relative_to(ROOT)} (fora do repo)")


if __name__ == "__main__":
    main()
