# Estudo 5 · G2 — transcrição turno a turno

O que o modelo emitiu (MODELO), o que o harness devolveu (HARNESS: resultado ou aviso). Não há canal de pensamento: `think=false` — isto é tudo que o modelo produz. Fichas de entrada: as extrações da rodada 2 do próprio gemma12.

## Goday 2016

```
MODELO : {"funcao": "dp_mudanca_r05", "argumentos": [1.1, 0.7], "fonte": ["hba1c_basal_dp", "hba1c_final_dp"]}
HARNESS: RESULTADO: 0.96
MODELO : {"funcao": "dp_de_se", "argumentos": [0.96, 45], "fonte": ["resultado-anterior", "n_analisado"]}
HARNESS: RESULTADO: 6.44
MODELO : {"funcao": "dp_de_se", "argumentos": [0.8, 40], "fonte": ["hba1c_final_dp", "n_analisado"]}
HARNESS: AVISO: o argumento 0.8 declara vir do campo 'braco_experimental.hba1c_final_dp', mas a ficha registra 0.7 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_se", "argumentos": [0.7, 40], "fonte": ["hba1c_final_dp", "n_analisado"]}
HARNESS: AVISO: o argumento 40.0 declara vir do campo 'braco_experimental.n_analisado', mas a ficha registra 45.0 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_se", "argumentos": [0.7, 45], "fonte": ["hba1c_final_dp", "n_analisado"]}
HARNESS: RESULTADO: 4.7
MODELO : {"funcao": "dp_de_se", "argumentos": [1.0, 40], "fonte": ["hba1c_basal_dp", "n_analisado"]}
HARNESS: AVISO: o argumento 1.0 declara vir do campo 'braco_experimental.hba1c_basal_dp', mas a ficha registra 1.1 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_se", "argumentos": [1.1, 40], "fonte": ["hba1c_basal_dp", "n_analisado"]}
HARNESS: AVISO: o argumento 40.0 declara vir do campo 'braco_experimental.n_analisado', mas a ficha registra 45.0 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_se", "argumentos": [1.1, 45], "fonte": ["hba1c_basal_dp", "n_analisado"]}
HARNESS: RESULTADO: 7.38
MODELO : {"funcao": "dp_de_se", "argumentos": [0.8, 40], "fonte": ["hba1c_final_dp", "n_analisado"]}
HARNESS: AVISO: o argumento 0.8 declara vir do campo 'braco_experimental.hba1c_final_dp', mas a ficha registra 0.7 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_se", "argumentos": [0.7, 40], "fonte": ["hba1c_final_dp", "n_analisado"]}
HARNESS: AVISO: o argumento 40.0 declara vir do campo 'braco_experimental.n_analisado', mas a ficha registra 45.0 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_se", "argumentos": [0.7, 40], "fonte": ["braco_controle.hba1c_final_dp", "braco_controle.n_analisado"]}
HARNESS: RESULTADO: 4.43
MODELO : {"funcao": "md", "argumentos": [5.3, 6.44, 45, 7.1, 4.43, 40], "fonte": ["hba1c_final_media", "resultado-anterior", "n_analisado", "hba1c_final_media", "resultado-anterior", "n_analisado"]}
HARNESS: AVISO: o argumento 7.1 declara vir do campo 'braco_experimental.hba1c_final_media', mas a ficha registra 5.3 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "md", "argumentos": [5.3, 6.44, 45, 7.1, 4.43, 40], "fonte": ["braco_experimental.hba1c_final_media", "resultado-anterior", "braco_experimental.n_analisado", "braco_controle.hba1c_final_media", "resultado-anterior", "braco_controle.n_analisado"]}
HARNESS: RESULTADO: -1.8
MODELO : {"funcao": "ic95_md", "argumentos": [5.3, 6.44, 45, 7.1, 4.43, 40], "fonte": ["braco_experimental.hba1c_final_media", "resultado-anterior", "braco_experimental.n_analisado", "braco_controle.hba1c_final_media", "resultado-anterior", "braco_controle.n_analisado"]}
HARNESS: RESULTADO: [-4.13, 0.53]
MODELO : {"funcao": "fim", "argumentos": [-1.8, -4.13, 0.53], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -1.8, "ic95": [-4.13, 0.53]}
```

## Saslow 2017

```
MODELO : {"funcao": "dp_de_ic", "argumentos": [-1.1, -0.6, 11], "fonte": ["hba1c_mudanca_dispersao_inferior", "hba1c_mudanca_dispersao_superior", "n_analisado"]}
HARNESS: RESULTADO: 0.42
MODELO : {"funcao": "dp_de_ic", "argumentos": [-0.6, 0.0, 8], "fonte": ["hba1c_mudanca_dispersao_inferior", "hba1c_mudanca_dispersao_superior", "n_analisado"]}
HARNESS: AVISO: o argumento 8.0 declara vir do campo 'braco_experimental.n_analisado', mas a ficha registra 11.0 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "dp_de_ic", "argumentos": [-0.6, 0.0, 8], "fonte": ["hba1c_mudanca_dispersao_inferior", "hba1c_mudanca_dispersao_superior", "n_analisado"]}
HARNESS: RESULTADO: 0.43
MODELO : {"funcao": "md", "argumentos": [-0.8, 0.42, 11, -0.3, 0.43, 8], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: AVISO: o argumento -0.3 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.8 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "md", "argumentos": [-0.8, 0.42, 11, -0.3, 0.43, 8], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: RESULTADO: -0.5
MODELO : {"funcao": "ic95_md", "argumentos": [-0.8, 0.42, 11, -0.3, 0.43, 8], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: AVISO: o argumento -0.3 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.8 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "md", "argumentos": [-0.8, 0.42, 11, -0.3, 0.43, 8], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: RESULTADO: -0.5
MODELO : {"funcao": "ic95_md", "argumentos": [-0.8, 0.42, 11, -0.3, 0.43, 8], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: AVISO: o argumento -0.3 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.8 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "ic95_md", "argumentos": [-0.8, 0.42, 11, -0.3, 0.43, 8], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "n_analisado", "hba1c_mudanca_media", "resultado-anterior", "n_analisado"]}
HARNESS: RESULTADO: [-0.89, -0.11]
MODELO : {"funcao": "fim", "argumentos": [-0.5, -0.89, -0.11], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.5, "ic95": [-0.89, -0.11]}
```

## Wang 2018

```
MODELO : {"funcao": "md", "argumentos": [-0.63, 1.18, 24, -0.31, 0.70, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: AVISO: o argumento -0.31 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.63 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "md", "argumentos": [-0.63, 1.18, 24, -0.31, 0.70, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: -0.32
MODELO : {"funcao": "ic95_md", "argumentos": [-0.63, 1.18, 24, -0.31, 0.70, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: AVISO: o argumento -0.31 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.63 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "ic95_md", "argumentos": [-0.63, 1.18, 24, -0.31, 0.70, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: [-0.87, 0.23]
MODELO : {"funcao": "fim", "argumentos": [-0.32, -0.87, 0.23], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.32, "ic95": [-0.87, 0.23]}
```

## Chen 2020

```
MODELO : {"funcao": "md", "argumentos": [-1.44, 0.59, 41, -1.01, 1.06, 42], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: AVISO: o argumento -1.01 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -1.44 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "md", "argumentos": [-1.44, 0.59, 41, -1.01, 1.06, 42], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: -0.43
MODELO : {"funcao": "ic95_md", "argumentos": [-1.44, 0.59, 41, -1.01, 1.06, 42], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: AVISO: o argumento -1.01 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -1.44 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "ic95_md", "argumentos": [-1.44, 0.59, 41, -1.01, 1.06, 42], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: [-0.8, -0.06]
MODELO : {"funcao": "fim", "argumentos": [-0.43, -0.8, -0.06], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.43, "ic95": [-0.8, -0.06]}
```

## Dorans 2022

```
MODELO : {"funcao": "dp_de_ic", "argumentos": [-0.33, -0.19, 73], "fonte": ["hba1c_mudanca_dispersao_inferior", "hba1c_mudanca_dispersao_superior", "braco_experimental_n_analisado"]}
HARNESS: RESULTADO: 0.31
MODELO : {"funcao": "dp_de_ic", "argumentos": [-0.10, 0.02, 69], "fonte": ["hba1c_mudanca_dispersao_inferior", "hba1c_mudanca_dispersao_superior", "braco_controle_n_analisado"]}
HARNESS: RESULTADO: 0.25
MODELO : {"funcao": "md", "argumentos": [-0.24, 0.31, 73, -0.04, 0.25, 69], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "braco_experimental_n_analisado", "hba1c_mudanca_media", "resultado-anterior", "braco_controle_n_analisado"]}
HARNESS: AVISO: o argumento -0.04 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.24 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "md", "argumentos": [-0.24, 0.31, 73, -0.04, 0.25, 69], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "braco_experimental_n_analisado", "hba1c_mudanca_media", "resultado-anterior", "braco_controle_n_analisado"]}
HARNESS: RESULTADO: -0.2
MODELO : {"funcao": "ic95_md", "argumentos": [-0.24, 0.31, 73, -0.04, 0.25, 69], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "braco_experimental_n_analisado", "hba1c_mudanca_media", "resultado-anterior", "braco_controle_n_analisado"]}
HARNESS: AVISO: o argumento -0.04 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.24 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "ic95_md", "argumentos": [-0.24, 0.31, 73, -0.04, 0.25, 69], "fonte": ["hba1c_mudanca_media", "resultado-anterior", "braco_experimental_n_analisado", "hba1c_mudanca_media", "resultado-anterior", "braco_controle_n_analisado"]}
HARNESS: RESULTADO: [-0.29, -0.11]
MODELO : {"funcao": "fim", "argumentos": [-0.2, -0.29, -0.11], "fonte": ["resultado-anterior", "resultado-anterior", "resultado-anterior"]}
FINAL  : {"md": -0.2, "ic95": [-0.29, -0.11]}
```

## Thomsen 2022

```
MODELO : {"funcao": "md", "argumentos": [-0.83, 0.38, 34, -0.56, 0.37, 33], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: AVISO: o argumento -0.56 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.83 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "md", "argumentos": [-0.83, 0.38, 34, -0.56, 0.37, 33], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: -0.27
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: AVISO: o argumento 0.37 declara vir do campo 'braco_experimental.hba1c_mudanca_dispersao', mas a ficha registra 0.38 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.27, 0.38, 34, 0.37, 33], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
FINAL  : null
```

## Saslow 2023

```
MODELO : {"funcao": "md", "argumentos": [-0.32, 0.07, 23, -0.14, 0.07, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: AVISO: o argumento -0.14 declara vir do campo 'braco_experimental.hba1c_mudanca_media', mas a ficha registra -0.32 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "md", "argumentos": [-0.32, 0.07, 23, -0.14, 0.07, 25], "fonte": ["hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: -0.18
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: AVISO: o argumento 25.0 declara vir do campo 'braco_experimental.n_analisado', mas a ficha registra 23.0 nesse campo. Confira e reemita a chamada (corrigida, ou idêntica se você confirma).
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
MODELO : {"funcao": "ic95_md", "argumentos": [-0.18, 0.07, 23, 0.07, 25], "fonte": ["resultado-anterior", "hba1c_mudanca_dispersao", "n_analisado", "hba1c_mudanca_dispersao", "n_analisado"]}
HARNESS: RESULTADO: erro — ic95_md() missing 1 required positional argument: 'n2'
FINAL  : null
```
