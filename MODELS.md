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
