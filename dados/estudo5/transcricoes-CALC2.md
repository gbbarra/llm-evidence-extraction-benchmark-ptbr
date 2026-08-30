# Estudo 5 · CALC2 — transcrição turno a turno

O que o modelo emitiu (MODELO), o que o harness devolveu (HARNESS: resultado ou aviso). Não há canal de pensamento: `think=false` — isto é tudo que o modelo produz. Fichas de entrada: as extrações da rodada 2 do próprio gemma12.

## Goday 2016

```
MODELO : {"funcao": "dp_mudanca_r05", "argumentos": [1.1, 0.7], "fonte": ["hba1c_basal_dp", "hba1c_final_dp"]}
HARNESS: RESULTADO: 0.96
MODELO : {"funcao": "dp_mudanca_r05", "argumentos": [1.0, 0.8], "fonte": ["hba1c_basal_dp", "hba1c_final_dp"]}
HARNESS: RESULTADO: 0.92
MODELO : {"funcao": "md", "argumentos": [5.3, 0.7, 45, 7.1, 0.8, 40], "fonte": ["hba1c_final_media", "hba1c_final_dp", "n_analisado", "hba1c_final_media", "hba1c_final_dp", "n_analisado"]}
HARNESS: RESULTADO: -1.8
MODELO : {"funcao": "ic95_md", "argumentos": [-1.8, 0.7, 45, 7.1, 0.8, 40], "fonte": ["resultado-anterior", "hba1c_final_dp", "n_analisado", "hba1c_final_media", "hba1c_final_dp", "n_analisado"]}
HARNESS: RESULTADO: [-9.22, -8.58]
MODELO : {"funcao": "fim", "argumentos": [-1.8, -9.22, -8.58], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -1.8, "ic95": [-9.22, -8.58]}
```

## Saslow 2017

```
MODELO : {"funcao": "dp_de_ic", "argumentos": [-1.1, -0.6, 11], "fonte": ["hba1c_mudanca_dispersao", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: 0.42
MODELO : {"funcao": "dp_de_ic", "argumentos": [-0.6, 0.0, 8], "fonte": ["hba1c_mudanca_dispersao", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: 0.43
MODELO : {"funcao": "md", "argumentos": [-0.8, 0.42, 11, -0.3, 0.43, 8], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: RESULTADO: -0.5
MODELO : {"funcao": "ic95_md", "argumentos": [-0.8, 0.42, 11, -0.3, 0.43, 8], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: RESULTADO: [-0.89, -0.11]
MODELO : {"funcao": "fim", "argumentos": [-0.5, -0.89, -0.11], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.5, "ic95": [-0.89, -0.11]}
```

## Wang 2018

```
MODELO : {"funcao": "md", "argumentos": [-0.63, 1.18, 24, -0.31, 0.70, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: -0.32
MODELO : {"funcao": "ic95_md", "argumentos": [-0.63, 1.18, 24, -0.31, 0.70, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: [-0.87, 0.23]
MODELO : {"funcao": "fim", "argumentos": [-0.32, -0.87, 0.23], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.32, "ic95": [-0.87, 0.23]}
```

## Chen 2020

```
MODELO : {"funcao": "dp_de_ic", "argumentos": [-1.96, -1.30, 41], "fonte": ["hba1c_mudanca_dispersao", "hba1c_mudanca_dispersao", "braco_experimental_n_analisado"]}
HARNESS: AVISO: o argumento -1.96 declara vir de 'hba1c_mudanca_dispersao', mas a ficha registra: 'braco_experimental.hba1c_mudanca_dispersao' = 1.96; 'braco_experimental.hba1c_mudanca_dispersao' = 1.3; 'braco_controle.hba1c_mudanca_dispersao' = 1.4. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_ic", "argumentos": [-1.96, -1.30, 41], "fonte": ["hba1c_mudanca_dispersao", "hba1c_mudanca_dispersao", "braco_experimental_n_analisado"]}
HARNESS: RESULTADO: 1.08
MODELO : {"funcao": "dp_de_ic", "argumentos": [-1.40, -0.63, 42], "fonte": ["hba1c_mudanca_dispersao", "hba1c_mudanca_dispersao", "braco_controle_n_analisado"]}
HARNESS: AVISO: o argumento -1.4 declara vir de 'hba1c_mudanca_dispersao', mas a ficha registra: 'braco_experimental.hba1c_mudanca_dispersao' = 1.96; 'braco_experimental.hba1c_mudanca_dispersao' = 1.3; 'braco_controle.hba1c_mudanca_dispersao' = 1.4. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_ic", "argumentos": [-1.40, -0.63, 42], "fonte": ["hba1c_mudanca_dispersao", "hba1c_mudanca_dispersao", "braco_controle_n_analisado"]}
HARNESS: RESULTADO: 1.27
MODELO : {"funcao": "md", "argumentos": [-1.44, 1.08, 41, -1.01, 1.27, 42], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "braco_experimental_n_analisado", "hba1c_mudanca_media", "resultado-anterior", "braco_controle_n_analisado"]}
HARNESS: RESULTADO: -0.43
MODELO : {"funcao": "ic95_md", "argumentos": [-1.44, 1.08, 41, -1.01, 1.27, 42], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "braco_experimental_n_analisado", "hba1c_mudanca_media", "resultado-anterior", "braco_controle_n_analisado"]}
HARNESS: RESULTADO: [-0.94, 0.08]
MODELO : {"funcao": "fim", "argumentos": [-0.43, -0.94, 0.08], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.43, "ic95": [-0.94, 0.08]}
```

## Dorans 2022

```
MODELO : {"funcao": "dp_de_ic", "argumentos": [-0.33, -0.19], "fonte": ["hba1c_mudanca_dispersao (inferior)", "hba1c_mudanca_dispersao (superior)"]}
HARNESS: AVISO: a função dp_de_ic exige 3 argumentos — dp_de_ic(inferior, superior, n) — e você enviou 2. Reemita a chamada completa.
MODELO : {"funcao": "dp_de_ic", "argumentos": [-0.33, -0.19, 73], "fonte": ["hba1c_mudanca_dispersao (inferior)", "hba1c_mudanca_dispersao (superior)", "n_analisado"]}
HARNESS: RESULTADO: 0.31
MODELO : {"funcao": "dp_de_ic", "argumentos": [-0.1, 0.02, 69], "fonte": ["hba1c_mudanca_dispersao (inferior)", "hba1c_mudanca_dispersao (superior)", "n_analisado"]}
HARNESS: RESULTADO: 0.25
MODELO : {"funcao": "md", "argumentos": [-0.24, 0.31, 73, -0.04, 0.25, 69], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: RESULTADO: -0.2
MODELO : {"funcao": "ic95_md", "argumentos": [-0.24, 0.31, 73, -0.04, 0.25, 69], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: RESULTADO: [-0.29, -0.11]
MODELO : {"funcao": "fim", "argumentos": [-0.2, -0.29, -0.11], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.2, "ic95": [-0.29, -0.11]}
```

## Thomsen 2022

```
MODELO : {"funcao": "md", "argumentos": [-0.83, 0.38, 34, -0.56, 0.37, 33], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: -0.27
MODELO : {"funcao": "ic95_md", "argumentos": [-0.83, 0.38, 34, -0.56, 0.37, 33], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: [-0.45, -0.09]
MODELO : {"funcao": "fim", "argumentos": [-0.27, -0.45, -0.09], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.27, "ic95": [-0.45, -0.09]}
```

## Saslow 2023

```
MODELO : {"funcao": "md", "argumentos": [-0.32, 0.07, 23, -0.14, 0.07, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: -0.18
MODELO : {"funcao": "ic95_md", "argumentos": [-0.32, 0.07, 23, -0.14, 0.07, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: [-0.22, -0.14]
MODELO : {"funcao": "fim", "argumentos": [-0.18, -0.22, -0.14], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.18, "ic95": [-0.22, -0.14]}
```
