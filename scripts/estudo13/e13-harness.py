# -*- coding: utf-8 -*-
"""EXTRAI Study 13 — the v3 campaign harness: the Study 12 harness (transport, atomic writes, resume gate,
single-instance lock, per-call record) with the v3 sheets, text hygiene at read time and the study's own output
tree. It REFUSES to call a model until the protocol carries its registration line; a dry run never calls anything.

  python scripts/estudo13/e13-harness.py --etapa P1-A --seco      # anchor 2 only: the plan, no call
  python scripts/estudo13/e13-harness.py --etapa P1-A             # after registration
  python scripts/estudo13/e13-harness.py --etapa P1-B [--modelo gemma12]   # anchors 1 and 3, conditional on H13.1
"""
import argparse
import importlib.util
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D13 = RAIZ / "dados" / "estudo13"


def _carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, RAIZ / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


H = _carrega("h12", "scripts/estudo12/e12-harness.py")
HIG = _carrega("hig13", "scripts/estudo13/e13-higiene.py")

ETAPAS = {"P1-A": ("a2",), "P1-B": ("a1", "a3")}
_ativas = ["a2"]
_ultima_higiene = [0]

# the Study 12 harness, re-pointed: v3 sheet per anchor, output allowance 8,000 (as v2), own output tree
H.SAIDA["v3"] = 8000
H.SAIDAS = D13 / "saidas"
H.RECUSADOS = D13 / "recusados"
for anc in ("a1", "a2", "a3"):
    H.ANCORAS[anc]["fichas"]["v3"] = D13 / "prompts" / f"{anc}-extraction-v3.txt"


def plano_v3():
    for modelo in H.ELENCO:
        for ancora in _ativas:
            for tid, caminho in H.ensaios(ancora):
                for rep in range(1, H.REPLICAS + 1):
                    yield dict(modelo=modelo, ancora=ancora, ficha="v3", ensaio=tid, replica=rep, caminho=caminho)


def confere_fichas_v3():
    p = D13 / "fichas.sha256"
    if not p.exists():
        raise SystemExit("dados/estudo13/fichas.sha256 não existe: rode e13-sela-fichas.py antes.")
    reg = {}
    for linha in io.open(p, encoding="utf-8").read().splitlines():
        if linha.startswith("#") or not linha.strip():
            continue
        sha, rot, rel = linha.split(None, 2)
        reg[rot] = (sha, rel.strip())
    import hashlib
    ruins = [f"{rot} ({rel})" for rot, (sha, rel) in reg.items()
             if hashlib.sha256(io.open(RAIZ / rel, "rb").read()).hexdigest() != sha]
    if ruins:
        raise SystemExit("fichas v3 não batem com os selos: " + ", ".join(ruins))
    return len(reg)


_monta = H.monta
_chama = H.chama


def monta_v3(tpl, texto):
    limpo, n = HIG.limpa(texto)
    _ultima_higiene[0] = n
    return _monta(tpl, limpo)


def chama_v3(c, prompt):
    r = _chama(c, prompt)
    r["estudo"] = 13
    r["higiene_removidos"] = _ultima_higiene[0]
    return r


H.plano = plano_v3
H.confere_fichas = confere_fichas_v3
H.monta = monta_v3
H.chama = chama_v3


def registrado():
    """The protocol carries a registration line only once the author fixes the freeze commit and the date."""
    t = io.open(D13 / "protocolo-estudo13.md", encoding="utf-8").read()
    return re.search(r"\*\*Registered \d{4}-\d{2}-\d{2}", t) is not None and "NOT REGISTERED" not in t.split("\n", 4)[2]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="harness da campanha do Estudo 13 (ficha v3)")
    ap.add_argument("--etapa", choices=sorted(ETAPAS), required=True)
    ap.add_argument("--modelo", choices=H.ELENCO)
    ap.add_argument("--seco", action="store_true", help="não chama modelo nenhum; só mostra o plano")
    a = ap.parse_args()
    _ativas[:] = ETAPAS[a.etapa]
    if not a.seco and not registrado():
        raise SystemExit("O protocolo do Estudo 13 não está registrado (sem linha '**Registered AAAA-MM-DD' no "
                         "cabeçalho). Registrar é ato do autor; até lá só a corrida seca (--seco) roda.")
    H.roda(a.modelo, None, "v3", a.seco)
