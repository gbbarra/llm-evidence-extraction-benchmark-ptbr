# Estudo 4 · rodada 2 — as contas e os códigos

As fichas (documento-irmão `fichas-comparadas.md`) são a parte dos MODELOS. Tudo daqui para baixo é a parte do CÓDIGO: nenhum modelo — e nenhum humano — digita um número. Este documento mostra as fórmulas, o código exato que roda, um exemplo feito à mão, e, para cada modelo, a rota que levou cada ficha ao resultado. O gerador deste arquivo recomputa tudo e só grava se bater com o registrado (gate).

## 1. O seletor de rota (que campos da ficha viram média, desvio e n)

Para cada braço: usa `n_analisado` (senão `n_randomizado`); usa a mudança lida (senão deriva final−basal, com desvio combinado pela regra r=0,5 do Cochrane); converte o desvio conforme o TIPO que a ficha declara — intervalo de confiança vira DP pela largura, erro-padrão vira DP multiplicando por √n.

```python
def bounds_ic(braco):
    """CI bounds = the LAST TWO numbers across tipo+dispersao (the '95' of
    'IC95' must never be a bound — the judges' lesson)."""
    fonte = str(braco.get("hba1c_mudanca_tipo_dispersao", "")) + " " + str(braco.get("hba1c_mudanca_dispersao", ""))
    ms = re.findall(r"-?\d+(?:\.\d+)?", fonte)
    return (float(ms[-2]), float(ms[-1])) if len(ms) >= 2 else None


def braco_deterministico(braco, julgamentos, chave_braco):
    """(mean, sd, n) for one arm, deterministic; sign questions may override."""
    n = num(braco.get("n_analisado"))
    if n is None:
        n = num(braco.get("n_randomizado"))
    m = num(braco.get("hba1c_mudanca_media"))
    tipo = str(braco.get("hba1c_mudanca_tipo_dispersao", "")).upper()
    dp = num(braco.get("hba1c_mudanca_dispersao"))
    if m is None:
        b0, b1 = num(braco.get("hba1c_basal_media")), num(braco.get("hba1c_final_media"))
        if b0 is not None and b1 is not None:
            m = round(b1 - b0, 2)
            d0, d1 = num(braco.get("hba1c_basal_dp")), num(braco.get("hba1c_final_dp"))
            if d0 is not None and d1 is not None:
                dp = h3.dp_mudanca_r05(d0, d1)
                tipo = "DP"
    if tipo.startswith("IC"):
        bb = bounds_ic(braco)
        if bb and n:
            dp = h3.dp_de_ic(bb[0], bb[1], n)
    elif tipo in ("EP", "SE") and dp is not None and n:
        dp = h3.dp_de_se(dp, n)
    # judgment override: as-reported positive change
    if chave_braco in julgamentos:
        m = julgamentos[chave_braco]
    return m, dp, n
```

## 2. As cinco fórmulas (código verbatim do harness)

- `md`: diferença de médias entre braços (m1 − m2).
- `ic95_md`: intervalo de 95% = diferença ± 1,96 × erro-padrão combinado.
- `dp_de_ic`: DP a partir de um IC95 = (largura ÷ 2 ÷ 1,96) × √n.
- `dp_de_se`: DP a partir de um erro-padrão = EP × √n.
- `dp_mudanca_r05`: DP da mudança a partir dos DPs basal/final (correlação 0,5).
- `pool_dl_md`: síntese DerSimonian–Laird (pesos 1/variância; heterogeneidade τ²; I²).

```python
def md(m1, dp1, n1, m2, dp2, n2):
    return round(m1 - m2, 2)


def ic95_md(m1, dp1, n1, m2, dp2, n2):
    se = math.sqrt(dp1 ** 2 / n1 + dp2 ** 2 / n2)
    d = m1 - m2
    return [round(d - 1.96 * se, 2), round(d + 1.96 * se, 2)]


def dp_de_ic(lo, hi, n):
    return round((hi - lo) / 2 / 1.96 * math.sqrt(n), 2)


def dp_de_se(se, n):
    return round(se * math.sqrt(n), 2)


def dp_mudanca_r05(dp1, dp2):
    return round(math.sqrt(dp1 ** 2 + dp2 ** 2 - 2 * 0.5 * dp1 * dp2), 2)


def pool_dl_md(estudos):
    ys, vs = [], []
    for e in estudos:
        m1, dp1, n1, m2, dp2, n2 = [float(x) for x in e]
        ys.append(m1 - m2)
        vs.append(dp1 ** 2 / n1 + dp2 ** 2 / n2)
    w = [1 / v for v in vs]
    yf = sum(wi * yi for wi, yi in zip(w, ys)) / sum(w)
    q = sum(wi * (yi - yf) ** 2 for wi, yi in zip(w, ys))
    df = len(ys) - 1
    cden = sum(w) - sum(wi ** 2 for wi in w) / sum(w)
    tau2 = max(0.0, (q - df) / cden) if df > 0 and cden > 0 else 0.0
    ws = [1 / (v + tau2) for v in vs]
    yr = sum(wi * yi for wi, yi in zip(ws, ys)) / sum(ws)
    se = math.sqrt(1 / sum(ws))
    i2 = max(0.0, (q - df) / q) * 100 if q > 0 and df > 0 else 0.0
    return dict(md=round(yr, 2), ic95=[round(yr - 1.96 * se, 2), round(yr + 1.96 * se, 2)],
                tau2=round(tau2, 4), i2_pct=round(i2, 1))


FUNCOES = dict(md=md, ic95_md=ic95_md, dp_de_ic=dp_de_ic, dp_de_se=dp_de_se,
               dp_mudanca_r05=dp_mudanca_r05, pool_dl_md=pool_dl_md)
```

## 3. Exemplo feito à mão — gemma12 × Saslow 2017

Ficha: exp mudança −0.8, tipo `IC95: -1.1 a -0.6`, n analisado 11; ctl mudança −0.3, tipo `IC95: -0.6 a 0.0`, n 8.

```
DP exp = (−0.6 − (−1.1)) / 2 / 1.96 × √11 = 0.1276 × 3.3166 = 0.42
DP ctl = ( 0.0 − (−0.6)) / 2 / 1.96 × √8  = 0.1531 × 2.8284 = 0.43
MD     = −0.8 − (−0.3) = −0.50
EP     = √(0.42²/11 + 0.43²/8) = √(0.01604 + 0.02311) = 0.1979
IC95   = −0.50 ± 1.96 × 0.1979 = [−0.89, −0.11]
```

Confere com a linha registrada do gemma12: `-0.5 [-0.89, -0.11]`.

## 4.1 gemma12 — conta por estudo

| estudo | sexteto (m,dp,n × 2 braços) | rota experimental | rota controle | MD [IC95] |
|---|---|---|---|---|
| Saslow 2017 | [-0.8, 0.42, 11.0, -0.3, 0.43, 8.0] | mudança lida da ficha; IC (-1.1, -0.6) → DP (n=11); n_analisado | mudança lida da ficha; IC (-0.6, 0.0) → DP (n=8); n_analisado | -0.5 [-0.89, -0.11] |
| Saslow 2023 | [-0.32, 0.34, 23.0, -0.14, 0.35, 25.0] | mudança lida da ficha; EP 0.07 → DP (×√23); n_analisado | mudança lida da ficha; EP 0.07 → DP (×√25); n_analisado | -0.18 [-0.38, 0.02] |
| Dorans 2022 | [-0.24, 0.31, 73.0, -0.04, 0.25, 69.0] | mudança lida da ficha; IC (-0.33, -0.19) → DP (n=73); n_analisado | mudança lida da ficha; IC (-0.1, 0.02) → DP (n=69); n_analisado | -0.2 [-0.29, -0.11] |
| Chen 2020 | [-1.44, 0.59, 41.0, -1.01, 1.06, 42.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.43 [-0.8, -0.06] |
| Thomsen 2022 | [-0.83, 0.38, 34.0, -0.56, 0.37, 33.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.27 [-0.45, -0.09] |
| Wang 2018 | [-0.63, 1.18, 24.0, -0.31, 0.7, 25.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.32 [-0.87, 0.23] |
| Goday 2016 | [-1.6, 0.96, 45.0, 0.3, 0.92, 40.0] | derivada: final−basal = 5.3−6.9; r=0,5 sobre DPs 1.1/0.7; n_analisado | derivada: final−basal = 7.1−6.8; r=0,5 sobre DPs 1.0/0.8; n_analisado | -1.9 [-2.3, -1.5] |

**Pool DerSimonian–Laird**: -0.52 [-0.82, -0.22] (τ²=0.1367, I²=91.3%) — recomputado pelo gerador: idêntico ✓

## 4.2 qwen14 — conta por estudo

| estudo | sexteto (m,dp,n × 2 braços) | rota experimental | rota controle | MD [IC95] |
|---|---|---|---|---|
| Saslow 2017 | [-0.8, -0.42, 11.0, -0.3, -0.43, 8.0] | mudança lida da ficha; IC (1.1, 0.6) → DP (n=11); n_analisado | mudança lida da ficha; IC (0.6, 0.0) → DP (n=8); n_analisado | -0.5 [-0.89, -0.11] |
| Saslow 2023 | [-0.32, 0.07, 22.0, -0.14, 0.07, 22.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.18 [-0.22, -0.14] |
| Dorans 2022 | [-0.24, 0.57, 73.0, -0.04, 0.04, 69.0] | mudança lida da ficha; IC (-0.19, 0.07) → DP (n=73); n_analisado | mudança lida da ficha; IC (0.02, 0.04) → DP (n=69); n_analisado | -0.2 [-0.33, -0.07] |
| Chen 2020 | [-1.44, 0.59, 41.0, -1.01, 1.06, 42.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.43 [-0.8, -0.06] |
| Thomsen 2022 | [-9.1, 4.2, 34.0, -7.2, 4.0, 33.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -1.9 [-3.86, 0.06] |
| Wang 2018 | [-0.63, 1.18, 24.0, -0.31, 0.7, 25.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.32 [-0.87, 0.23] |
| Goday 2016 | [-1.6, 0.7, 45.0, 0.3, 0.8, 44.0] | mudança lida da ficha; DP direto da ficha; n_randomizado | mudança lida da ficha · GATILHO respondeu 0.3; DP direto da ficha; n_randomizado | -1.9 [-2.21, -1.59] |

**Pool DerSimonian–Laird**: -0.62 [-0.99, -0.25] (τ²=0.1919, I²=95.0%) — recomputado pelo gerador: idêntico ✓

## 4.3 llama8 — conta por estudo

| estudo | sexteto (m,dp,n × 2 braços) | rota experimental | rota controle | MD [IC95] |
|---|---|---|---|---|
| Saslow 2017 | [-0.8, 0.42, 11.0, -0.3, 0.43, 8.0] | mudança lida da ficha; IC (-1.1, -0.6) → DP (n=11); n_analisado | mudança lida da ficha; IC (-0.6, 0.0) → DP (n=8); n_analisado | -0.5 [-0.89, -0.11] |
| Saslow 2023 | — | FORA DO POOL: faltou [-0.32, 0.4, 25.0]/[-0.14, None, 25.0] | | |
| Dorans 2022 | — | FORA DO POOL: faltou [-0.24, 0.3, 73.0]/[-0.04, None, 69.0] | | |
| Chen 2020 | [-1.44, 5.33, 41.0, -1.01, 3.36, 42.0] | mudança lida da ficha; IC (-1.3, 1.96) → DP (n=41); n_analisado | mudança lida da ficha; IC (-0.63, 1.4) → DP (n=42); n_analisado | -0.43 [-2.35, 1.49] |
| Thomsen 2022 | [-9.1, 4.2, 34.0, -7.2, 4.0, 33.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -1.9 [-3.86, 0.06] |
| Wang 2018 | [-0.63, 1.18, 24.0, -0.31, 0.7, 25.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.32 [-0.87, 0.23] |
| Goday 2016 | [-0.36, 0.11, 45.0, -0.15, 0.15, 44.0] | mudança lida da ficha; DP direto da ficha; n_randomizado | mudança lida da ficha; DP direto da ficha; n_randomizado · GATILHO NR preencheu {'dp': 0.15} | -0.21 [-0.26, -0.16] |

**Pool DerSimonian–Laird**: -0.3 [-0.49, -0.1] (τ²=0.0141, I²=21.8%) — recomputado pelo gerador: idêntico ✓

## 4.4 qwen35 — conta por estudo

| estudo | sexteto (m,dp,n × 2 braços) | rota experimental | rota controle | MD [IC95] |
|---|---|---|---|---|
| Saslow 2017 | [-0.8, -0.44, 12.0, -0.3, -0.55, 13.0] | mudança lida da ficha; IC (1.1, 0.6) → DP (n=12); n_randomizado | mudança lida da ficha; IC (0.6, 0.0) → DP (n=13); n_randomizado | -0.5 [-0.89, -0.11] |
| Saslow 2023 | [-0.32, 0.07, 39.0, -0.14, 0.07, 42.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.18 [-0.21, -0.15] |
| Dorans 2022 | [-0.24, -0.31, 75.0, -0.04, -0.18, 75.0] | mudança lida da ficha; IC (0.33, 0.19) → DP (n=75); n_analisado | mudança lida da ficha; IC (0.1, 0.02) → DP (n=75); n_analisado | -0.2 [-0.28, -0.12] |
| Chen 2020 | [-1.44, 2.71, 41.0, -1.01, 1.65, 42.0] | mudança lida da ficha; IC (-1.3, 0.36) → DP (n=41); n_randomizado | mudança lida da ficha; IC (-0.63, 0.37) → DP (n=42); n_randomizado | -0.43 [-1.4, 0.54] |
| Thomsen 2022 | — | FORA DO POOL: faltou [-0.18, -0.43, 34.0]/[-0.56, None, 33.0] | | |
| Wang 2018 | [-0.63, 1.18, 24.0, -0.31, 0.7, 25.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.32 [-0.87, 0.23] |
| Goday 2016 | [-1.6, 0.7, 45.0, 0.3, 0.92, 40.0] | mudança lida da ficha; DP direto da ficha; n_analisado | derivada: final−basal = 7.1−6.8; r=0,5 sobre DPs 1.0/0.8; n_analisado | -1.9 [-2.25, -1.55] |

**Pool DerSimonian–Laird**: -0.57 [-0.84, -0.3] (τ²=0.0776, I²=94.7%) — recomputado pelo gerador: idêntico ✓

## 4.5 deepseek14 — conta por estudo

| estudo | sexteto (m,dp,n × 2 braços) | rota experimental | rota controle | MD [IC95] |
|---|---|---|---|---|
| Saslow 2017 | [-0.8, 0.44, 12.0, -0.3, 0.55, 13.0] | mudança lida da ficha; IC (-1.1, -0.6) → DP (n=12); n_analisado | mudança lida da ficha; IC (-0.6, 0.0) → DP (n=13); n_analisado | -0.5 [-0.89, -0.11] |
| Saslow 2023 | — | FORA DO POOL: faltou [-0.32, 0.07, None]/[-0.14, 0.07, None] | | |
| Dorans 2022 | [-0.23, -209.77, 75.0, -0.04, -209.75, 75.0] | mudança lida da ficha; IC (95.0, 0.05) → DP (n=75); n_analisado | mudança lida da ficha; IC (95.0, 0.06) → DP (n=75); n_analisado | -0.19 [-67.33, 66.95] |
| Chen 2020 | [-1.44, 0.59, 40.0, -1.01, 0.7, 41.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.43 [-0.71, -0.15] |
| Thomsen 2022 | — | FORA DO POOL: faltou [None, None, 34.0]/[None, None, 33.0] | | |
| Wang 2018 | [-0.63, 1.18, 24.0, -0.31, 0.7, 25.0] | mudança lida da ficha; DP direto da ficha; n_analisado | mudança lida da ficha; DP direto da ficha; n_analisado | -0.32 [-0.87, 0.23] |
| Goday 2016 | — | FORA DO POOL: faltou [-1.6, 0.7, 45.0]/[None, None, 44.0] | | |

**Pool DerSimonian–Laird**: -0.43 [-0.64, -0.22] (τ²=0.0, I²=0.0%) — recomputado pelo gerador: idêntico ✓

---
*Todas as linhas acima foram recomputadas por este gerador a partir das fichas e conferidas contra os resultados registrados antes de gravar. Fontes: `scripts/estudo3/e3-harness.py` (fórmulas), `scripts/estudo3/dirigida.py` (rotas), `scripts/estudo4/e4-rodada2.py` (fila), `resultados/<modelo>.json` (registro).*