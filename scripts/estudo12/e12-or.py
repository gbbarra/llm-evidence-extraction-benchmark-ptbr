# -*- coding: utf-8 -*-
"""EXTRAI — instrument work for the three-anchor campaign: the odds-ratio half of the engine.

WHY THIS EXISTS. Anchors 1 and 2 are risk-ratio and mean-difference anchors, and the frozen engine
(`scripts/estudo2/e2-harness.py`) pools those two and only those two. Anchor 3 — methylene blue in
adult shock, PMC13302755 — publishes its primary outcome as an **odds ratio**: OR 0.73 (95% CI
0.40-1.36) for 28-30-day mortality over 8 studies. Reproducing that estimand needs log-odds-ratio
pooling, which the engine does not contain.

WHAT IS AND IS NOT TOUCHED. `e2-harness.py` is imported, never edited: this module reuses its
continuity rule (`_cont`) verbatim, so a zero cell is handled identically on both estimands, and its
`rr` / `pool_dl` are used as independent references in the self-test below. Every function here is
new. The campaign reports BOTH estimands on anchor 3: the odds ratio, to compare with the published
diamond, and the risk ratio, from the untouched function.

VALIDATION. Running this file executes the battery in `validar()`, which checks each function against
an independently computed path rather than against a stored expected value:
  1. algebraic identity  OR = RR x (1 - p_control) / (1 - p_experimental), against the frozen `rr`
  2. Woolf standard error by the explicit 1/a + 1/b + 1/c + 1/d form
  3. Mantel-Haenszel OR by the textbook sum-of-products form, computed inline
  4. Robins-Breslow-Greenland variance by its explicit three-term form
  5. rare-event convergence: as event rates fall, the pooled OR approaches the frozen pooled RR
  6. arm symmetry: swapping arms inverts the odds ratio
  7. continuity: a zero cell is corrected by the frozen rule and the correction is reported
  8. degenerate heterogeneity: with tau-squared at zero, DL collapses to inverse-variance fixed effect
The anchor's published OR 0.73 [0.40, 1.36] is NOT used here as an expected value: it becomes the
standing published test case only once the answer key is complete, and reproducing it will then be a
result of the campaign, not a precondition of the instrument.

Run: python scripts/estudo12/e12-or.py
"""
import importlib.util
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]

_sp = importlib.util.spec_from_file_location("e2", ROOT / "scripts" / "estudo2" / "e2-harness.py")
e2 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(e2)


def _cells(a, n1, c, n2):
    """(a, b, c, d) after the frozen continuity rule; b and d are the non-event counts."""
    a, n1, c, n2, cc = e2._cont(float(a), float(n1), float(c), float(n2))
    return a, n1 - a, c, n2 - c, cc


# ---------------------------------------------------------------- per study
def odds_ratio(a, n1, c, n2):
    """Odds ratio of the event, experimental arm over control arm."""
    a, b, c, d, _ = _cells(a, n1, c, n2)
    return round((a * d) / (b * c), 3)


def ci95_or(a, n1, c, n2):
    """Woolf (log-odds) 95% interval."""
    a, b, c, d, _ = _cells(a, n1, c, n2)
    o = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return [round(math.exp(math.log(o) - 1.96 * se), 3), round(math.exp(math.log(o) + 1.96 * se), 3)]


# ---------------------------------------------------------------- pooling
def pool_or_mh(estudos):
    """Mantel-Haenszel fixed-effect odds ratio, Robins-Breslow-Greenland interval.

    estudos: sequence of (a, n1, c, n2)."""
    R = S = 0.0
    PR = PSQR = QS = 0.0
    for e in estudos:
        a, b, c, d, _ = _cells(*[float(x) for x in e])
        N = a + b + c + d
        Ri, Si = a * d / N, b * c / N
        P, Q = (a + d) / N, (b + c) / N
        R += Ri
        S += Si
        PR += P * Ri
        PSQR += P * Si + Q * Ri
        QS += Q * Si
    o = R / S
    var = PR / (2 * R * R) + PSQR / (2 * R * S) + QS / (2 * S * S)
    se = math.sqrt(var)
    return dict(**{"or": round(o, 3)},
                ic95=[round(math.exp(math.log(o) - 1.96 * se), 3),
                      round(math.exp(math.log(o) + 1.96 * se), 3)])


def pool_or_dl(estudos):
    """DerSimonian-Laird random-effects pooling on the log odds ratio, with tau-squared and I-squared.

    Same machinery as the frozen `pool_dl`, applied to the log-odds effect and its Woolf variance."""
    ys, vs = [], []
    for e in estudos:
        a, b, c, d, _ = _cells(*[float(x) for x in e])
        ys.append(math.log((a * d) / (b * c)))
        vs.append(1 / a + 1 / b + 1 / c + 1 / d)
    w = [1 / v for v in vs]
    yf = sum(wi * yi for wi, yi in zip(w, ys)) / sum(w)
    q = sum(wi * (yi - yf) ** 2 for wi, yi in zip(w, ys))
    df = len(ys) - 1
    cdenom = sum(w) - sum(wi ** 2 for wi in w) / sum(w)
    tau2 = max(0.0, (q - df) / cdenom) if df > 0 and cdenom > 0 else 0.0
    ws = [1 / (v + tau2) for v in vs]
    yr = sum(wi * yi for wi, yi in zip(ws, ys)) / sum(ws)
    se = math.sqrt(1 / sum(ws))
    i2 = max(0.0, (q - df) / q) * 100 if q > 0 and df > 0 else 0.0
    return dict(**{"or": round(math.exp(yr), 3)},
                ic95=[round(math.exp(yr - 1.96 * se), 3), round(math.exp(yr + 1.96 * se), 3)],
                tau2=round(tau2, 4), i2=round(i2, 1))


# ---------------------------------------------------------------- validação
def _quase(x, y, tol=1e-9, nome=""):
    if abs(x - y) > tol:
        raise AssertionError(f"{nome}: {x!r} != {y!r} (delta {abs(x-y):.3e})")


def validar(verboso=True):
    falhas = []
    passou = 0

    def ok(nome):
        nonlocal passou
        passou += 1
        if verboso:
            print(f"  ok  {nome}")

    def falha(nome, e):
        falhas.append((nome, str(e)))
        print(f"  FALHA  {nome}: {e}")

    # conjuntos de células determinísticos, incluindo célula zero e desbalanceio de braços
    CASOS = [(10, 50, 20, 50), (5, 30, 9, 31), (1, 20, 4, 20), (25, 100, 30, 100),
             (0, 28, 6, 28), (3, 14, 3, 15), (40, 60, 20, 60), (2, 200, 8, 200)]

    # 1. identidade OR = RR x (1 - pc) / (1 - pe), contra o rr congelado
    try:
        for a, n1, c, n2 in CASOS:
            aa, bb, cc_, dd, _ = _cells(a, n1, c, n2)
            pe, pc = aa / (aa + bb), cc_ / (cc_ + dd)
            esperado = e2.rr(a, n1, c, n2) * (1 - pc) / (1 - pe)
            # rr() arredonda a 3 casas; compara na mesma resolução
            _quase(odds_ratio(a, n1, c, n2), round(esperado, 3), 2e-3, f"identidade {a}/{n1} vs {c}/{n2}")
        ok("1. identidade OR = RR x (1-pc)/(1-pe), contra o rr congelado")
    except AssertionError as e:
        falha("1. identidade com o rr congelado", e)

    # 2. erro padrão de Woolf por caminho explícito
    try:
        for a, n1, c, n2 in CASOS:
            aa, bb, cc_, dd, _ = _cells(a, n1, c, n2)
            se = math.sqrt(1 / aa + 1 / bb + 1 / cc_ + 1 / dd)
            o = (aa * dd) / (bb * cc_)
            alvo = [round(math.exp(math.log(o) - 1.96 * se), 3), round(math.exp(math.log(o) + 1.96 * se), 3)]
            assert ci95_or(a, n1, c, n2) == alvo, f"{ci95_or(a, n1, c, n2)} != {alvo}"
        ok("2. intervalo de Woolf por caminho independente")
    except AssertionError as e:
        falha("2. intervalo de Woolf", e)

    # 3. MH pelo somatório de produtos, calculado aqui
    try:
        R = S = 0.0
        for a, n1, c, n2 in CASOS:
            aa, bb, cc_, dd, _ = _cells(a, n1, c, n2)
            N = aa + bb + cc_ + dd
            R += aa * dd / N
            S += bb * cc_ / N
        _quase(pool_or_mh(CASOS)["or"], round(R / S, 3), 1e-9, "MH")
        ok("3. Mantel-Haenszel pelo somatório de produtos")
    except AssertionError as e:
        falha("3. Mantel-Haenszel", e)

    # 4. variância de Robins-Breslow-Greenland pelos três termos explícitos
    try:
        R = S = t1 = t2 = t3 = 0.0
        for a, n1, c, n2 in CASOS:
            aa, bb, cc_, dd, _ = _cells(a, n1, c, n2)
            N = aa + bb + cc_ + dd
            R += aa * dd / N
            S += bb * cc_ / N
        for a, n1, c, n2 in CASOS:
            aa, bb, cc_, dd, _ = _cells(a, n1, c, n2)
            N = aa + bb + cc_ + dd
            Ri, Si = aa * dd / N, bb * cc_ / N
            P, Q = (aa + dd) / N, (bb + cc_) / N
            t1 += P * Ri
            t2 += P * Si + Q * Ri
            t3 += Q * Si
        var = t1 / (2 * R * R) + t2 / (2 * R * S) + t3 / (2 * S * S)
        se = math.sqrt(var)
        o = R / S
        alvo = [round(math.exp(math.log(o) - 1.96 * se), 3), round(math.exp(math.log(o) + 1.96 * se), 3)]
        assert pool_or_mh(CASOS)["ic95"] == alvo, f"{pool_or_mh(CASOS)['ic95']} != {alvo}"
        ok("4. variância de Robins-Breslow-Greenland pelos três termos")
    except AssertionError as e:
        falha("4. variância RBG", e)

    # 5. convergência em evento raro: OR -> RR quando as taxas caem
    try:
        anteriores = None
        for escala in (1, 10, 100, 1000):
            raros = [(2, 100 * escala, 4, 100 * escala), (1, 50 * escala, 3, 50 * escala),
                     (3, 200 * escala, 5, 200 * escala)]
            d = abs(pool_or_dl(raros)["or"] - e2.pool_dl(raros)["rr"])
            if anteriores is not None:
                assert d <= anteriores + 1e-9, f"não convergiu na escala {escala}: {d} > {anteriores}"
            anteriores = d
        assert anteriores < 0.01, f"limite raro afastado do RR: delta {anteriores}"
        ok(f"5. convergência para o RR congelado em evento raro (delta final {anteriores:.5f})")
    except AssertionError as e:
        falha("5. convergência em evento raro", e)

    # 6. simetria: trocar os braços inverte a razão de chances
    try:
        for a, n1, c, n2 in CASOS:
            direto = odds_ratio(a, n1, c, n2)
            invertido = odds_ratio(c, n2, a, n1)
            _quase(direto * invertido, 1.0, 5e-3, f"simetria {a}/{n1} vs {c}/{n2}")
        ok("6. simetria dos braços")
    except AssertionError as e:
        falha("6. simetria dos braços", e)

    # 7. correção de continuidade: célula zero tratada pela regra congelada
    try:
        # Levin 2004 como a própria revisão o imprime na Tabela 1: 0/28 contra 6/28.
        # A regra congelada soma 0,5 às QUATRO células, ou seja, +0,5 no evento e +1 no n,
        # o que também soma 0,5 ao não evento: 28 -> 28,5 e 22 -> 22,5.
        a, b, c, d, cc = _cells(0, 28, 6, 28)
        assert cc, "a regra congelada não sinalizou a correção na célula zero"
        assert (a, b, c, d) == (0.5, 28.5, 6.5, 22.5), f"células corrigidas inesperadas: {(a, b, c, d)}"
        assert (b, d) == (28 - 0 + 0.5, 28 - 6 + 0.5), "o não evento não recebeu a mesma correção"
        assert math.isfinite(odds_ratio(0, 28, 6, 28)), "OR não finito com célula zero"
        ok("7. correção de continuidade na célula zero, pela regra congelada")
    except AssertionError as e:
        falha("7. correção de continuidade", e)

    # 8. sem heterogeneidade, DL colapsa no efeito fixo de variância inversa
    try:
        iguais = [(10, 100, 20, 100), (20, 200, 40, 200), (5, 50, 10, 50)]
        r = pool_or_dl(iguais)
        assert r["tau2"] == 0.0, f"tau2 deveria ser zero: {r['tau2']}"
        ys, vs = [], []
        for a, n1, c, n2 in iguais:
            aa, bb, cc_, dd, _ = _cells(a, n1, c, n2)
            ys.append(math.log(aa * dd / (bb * cc_)))
            vs.append(1 / aa + 1 / bb + 1 / cc_ + 1 / dd)
        w = [1 / v for v in vs]
        fixo = math.exp(sum(wi * yi for wi, yi in zip(w, ys)) / sum(w))
        _quase(r["or"], round(fixo, 3), 1e-9, "DL == efeito fixo com tau2 zero")
        ok("8. DL colapsa no efeito fixo quando tau-quadrado é zero")
    except AssertionError as e:
        falha("8. DL sem heterogeneidade", e)

    print(f"\n{passou} de {passou + len(falhas)} verificações passaram")
    if falhas:
        print("FALHAS:")
        for nome, e in falhas:
            print(f"  - {nome}: {e}")
    return not falhas


if __name__ == "__main__":
    print("Validação do agrupador de razão de chances (instrumento novo; motor congelado intocado)\n")
    ok = validar()
    print("\nPUBLICADO, ainda NÃO usado como valor esperado: a âncora 3 imprime uma única estimativa em texto,")
    print("OR 0,73 (IC 95% 0,40 a 1,36) para mortalidade em 28 a 30 dias, 8 estudos. Ela vira o caso de teste")
    print("publicado desta metade do motor quando a chave estiver completa; reproduzi-la será resultado da")
    print("campanha, não pré-condição do instrumento.")
    sys.exit(0 if ok else 1)
