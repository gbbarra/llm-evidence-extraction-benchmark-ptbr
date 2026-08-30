# Estudo 5 · G1 — transcrição turno a turno

O que o modelo emitiu (MODELO), o que o harness devolveu (HARNESS: resultado ou aviso). Não há canal de pensamento: `think=false` — isto é tudo que o modelo produz. Fichas de entrada: as extrações da rodada 2 do próprio gemma12.

## Goday 2016

```
MODELO : CALC: dp_mudanca_r05(1.1, 0.7)
HARNESS: RESULTADO: 0.96
MODELO : CALC: dp_mudanca_r05(1.0, 0.8)
HARNESS: RESULTADO: 0.92
MODELO : CALC: md(5.3, 0.7, 45, 7.1, 0.8, 40)
HARNESS: RESULTADO: -1.8
MODELO : CALC: ic95_md(5.3, 0.7, 45, 7.1, 0.8, 40)
HARNESS: RESULTADO: [-2.12, -1.48]
MODELO : FIM
FINAL  : {"md": -1.8, "ic95": [-2.12, -1.48]}
```

## Saslow 2017

```
MODELO : CALC: dp_de_ic(-1.1, -0.6, 11)
HARNESS: RESULTADO: 0.42
MODELO : CALC: dp_de_ic(-0.6, 0.0, 8)
HARNESS: RESULTADO: 0.43
MODELO : CALC: md(-0.8, 0.42, 11, -0.3, 0.43, 8)
HARNESS: RESULTADO: -0.5
MODELO : CALC: ic95_md(-0.8, 0.42, 11, -0.3, 0.43, 8)
HARNESS: RESULTADO: [-0.89, -0.11]
MODELO : FIM
FINAL  : {"md": -0.5, "ic95": [-0.89, -0.11]}
```

## Wang 2018

```
MODELO : CALC: md(-0.63, 1.18, 24, -0.31, 0.70, 25)
HARNESS: RESULTADO: -0.32
MODELO : CALC: ic95_md(-0.63, 1.18, 24, -0.31, 0.70, 25)
HARNESS: RESULTADO: [-0.87, 0.23]
MODELO : FIM
FINAL  : {"md": -0.32, "ic95": [-0.87, 0.23]}
```

## Chen 2020

```
MODELO : CALC: md(-1.44, 0.59, 41, -1.01, 1.06, 42)
HARNESS: RESULTADO: -0.43
MODELO : CALC: ic95_md(-1.44, 0.59, 41, -1.01, 1.06, 42)
HARNESS: RESULTADO: [-0.8, -0.06]
MODELO : FIM
FINAL  : {"md": -0.43, "ic95": [-0.8, -0.06]}
```

## Dorans 2022

```
MODELO : CALC: dp_de_ic(-0.19, -0.33, 73)
HARNESS: RESULTADO: -0.31
MODELO : CALC: dp_de_ic(0.02, -0.10, 69)
HARNESS: RESULTADO: -0.25
MODELO : CALC: md(-0.24, -0.31, 73, -0.04, -0.25, 69)
HARNESS: AVISO: o argumento -0.31 tem a mesma magnitude do campo 'braco_experimental.hba1c_basal_dp' da ficha, mas com o SINAL oposto — e nenhum número da ficha vale -0.31. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : CALC: dp_de_ic(-0.19, -0.33, 73)
HARNESS: RESULTADO: -0.31
MODELO : CALC: dp_de_ic(0.02, -0.10, 69)
HARNESS: RESULTADO: -0.25
MODELO : CALC: md(-0.24, -0.31, 73, -0.04, -0.25, 69)
HARNESS: AVISO: o argumento -0.31 tem a mesma magnitude do campo 'braco_experimental.hba1c_basal_dp' da ficha, mas com o SINAL oposto — e nenhum número da ficha vale -0.31. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : CALC: md(-0.24, 0.31, 73, -0.04, 0.25, 69)
HARNESS: RESULTADO: -0.2
MODELO : CALC: ic95_md(-0.24, 0.31, 73, -0.04, 0.25, 69)
HARNESS: RESULTADO: [-0.29, -0.11]
MODELO : FIM
FINAL  : {"md": -0.2, "ic95": [-0.29, -0.11]}
```

## Thomsen 2022

```
MODELO : CALC: md(-0.83, 0.38, 34, -0.56, 0.37, 33)
HARNESS: RESULTADO: -0.27
MODELO : CALC: ic95_md(-0.83, 0.38, 34, -0.56, 0.37, 33)
HARNESS: RESULTADO: [-0.45, -0.09]
MODELO : FIM
FINAL  : {"md": -0.27, "ic95": [-0.45, -0.09]}
```

## Saslow 2023

```
MODELO : CALC: md(-0.32, 0.07, 23, -0.14, 0.07, 25)
HARNESS: RESULTADO: -0.18
MODELO : CALC: ic95_md(-0.32, 0.07, 23, -0.14, 0.07, 25)
HARNESS: RESULTADO: [-0.22, -0.14]
MODELO : FIM
FINAL  : {"md": -0.18, "ic95": [-0.22, -0.14]}
```
