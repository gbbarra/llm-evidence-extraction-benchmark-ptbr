# Pinned model builds (Ollama)

The exact quantized builds behind every EXTRAI run, recorded 2026-08-30 on the benchmark machine (Ollama 0.32.15, `ollama list` / `ollama show`). The ID column is Ollama's manifest-digest prefix as printed by `ollama list`; re-pulling a tag later may fetch a different build, so exact reproduction should verify these IDs.

| Paper name | Ollama tag (in the harnesses) | ID (digest prefix) | Params | Quant | Architecture |
|---|---|---|---|---|---|
| gemma4:12b | `gemma4:12b` | `4eb23ef187e2` | 11.9B | Q4_K_M | gemma4 |
| qwen3:14b | `qwen3:14b` | `bdbd181c33f2` | 14.8B | Q4_K_M | qwen3 |
| gemma4:26b | `gemma4:26b` | `5571076f3d70` | 25.8B | Q4_K_M | gemma4 (MoE) |
| qwen3.8:27b | `qwen3.8:27b-texto` | `7754b7d139c8` | 27.3B | Q4_K_M | qwen35 |

Study-4 Amendment-1 extension arm (recorded 2026-08-30, same machine):

| Paper name | Ollama tag | ID (digest prefix) | Params | Quant | Architecture |
|---|---|---|---|---|---|
| llama3.1:8b | `llama3.1:8b` | `46e0c10c039e` | 8.0B | Q4_K_M | llama |
| qwen3.5:9b | `qwen3.5:9b` | `6488c96fa5fa` | 9.7B | Q4_K_M | qwen35 |
| deepseek-r1:14b | `deepseek-r1:14b` | `c333b7232bdb` | 14.8B | Q4_K_M | qwen2 (distill) |

Study-5 Amendment-7 orchestrator arm (recorded 2026-08-30):

| Role | Ollama tag | ID (digest prefix) | Size | Notes |
|---|---|---|---|---|
| orchestrator under test | `codegemma:latest` | `0c96700aaada` | 5.0 GB | earlier-generation code model |
| orchestrator under test | `xentriom/gemma-4-12B-coder-fable5-composer2.5-v1:latest` | `9d01307b99a8` | 7.4 GB | community GGUF fine-tune of gemma-4-12B (Python/code); Ollama mirror namespace differs from the Hugging Face author (yuxinlu1) — unofficial, hobbyist provenance |

**Note on the 27B tag.** All three studies call the 27B through the local tag `qwen3.8:27b-texto`: the same base-weights blob as the stock `qwen3.8:27b` (`sha256-f5f1dd8920d417aac2718b0bda3403da274301efdd6760b4f0f4b864ff2ad57d`, verified identical `FROM` on both tags) rebuilt with a raw-prompt template (`TEMPLATE {{ .Prompt }}`), so the frozen Portuguese instruments pass through verbatim with no chat wrapper. Each study's `MODELS` dict in `scripts/estudo*/e*-harness.py` records the tag it ran.

Study-8 Amendment-1 extension arm (recorded 2026-09-07, same machine):

| Paper name | Ollama tag | ID (digest prefix) | Params | Quantization | Architecture |
|---|---|---|---|---|---|
| qwen3.8:27b (ext.) | `smtek/Qwen3.8-27B:Q2_K_XL` | `d67a36b99f60` | 27.32B | mixed precision, **3.13 bits per weight** (10.68 GB) | qwen35 |

**Note on this build's quantization.** Three sources disagree, and only one of them describes the weights:

- the **Ollama tag** says `Q2_K_XL` — Unsloth's "dynamic" naming, not a uniform ggml type;
- the **GGUF header** field `general.file_type` says `14` = `MOSTLY_Q4_K_S`, which is what `ollama show` prints; the field holds a single enum and cannot express a mixed quantization;
- the **tensors themselves** are mixed: IQ3_XXS on 77.4% of parameters, IQ3_S on 11.7%, Q3_K and Q2_K on 4.7% each, IQ4_XS on 1.5%, IQ1_M on 0.1%, the rest F32.

Measured by reading the GGUF header of the weight blob with `scripts/estudo8/gguf-inspect.py` (full output in `dados/estudo8/gguf-qwen27q2.json`): 866 tensors, 27.32 B parameters, 10.68 GB, **3.13 bits per weight** from the file size and 3.12 from the tensor types — against ~4.5 bits per weight for the cast's Q4_K_M builds. `general.repo_url` names `huggingface.co/unsloth`, so this is an Ollama mirror (namespace `smtek`) of an Unsloth dynamic quantization; the mirror namespace is not the quantizer. Both published tags of this build (`Q2_K_XL` and `Q2_K_XL-16gb`) point to the same weight blob and carry `TEMPLATE {{ .Prompt }}`, the raw-prompt template — the same one the 27B of the instrument-development phase used, so the template is not a confounder against that record; the quantization is (Q4_K_M there, 3.13 bits per weight here). The two tags differ only in `num_ctx` (262144 against 131072, both overridden to 16384 by the harness) and in `draft_num_predict` (4 against 0), so under this campaign's fixed context they are the same model. Measured 2026-09-08 with `ollama show --modelfile`.
