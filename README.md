# AI & Software Engineering Projects

A portfolio of practical software and AI engineering projects.

## Featured project: OpenBench AI

[**OpenBench AI — open-source LLM evaluation lab**](OpenBench-AI/)

OpenBench AI is a Python evaluation toolkit for question-answering systems. It includes a reproducible evaluation pipeline, exact-match and token-F1 baseline metrics, latency and throughput reporting, JSON/CSV exports, a FastAPI demo endpoint, and a Streamlit dashboard for comparing saved runs.

### Try it

```bash
cd OpenBench-AI
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
openbench run --dataset data/sample_qa.jsonl --output results/demo.json
pytest
```

For a real model without a paid API, install [Ollama](https://ollama.com/) and follow the [OpenBench AI README](OpenBench-AI/README.md).

**Transparency:** the demo adapter is deterministic and does not measure real model quality. Real local-model evaluations use the Ollama adapter. The project documents metric limitations and reproducibility recommendations in its evaluation methodology.

## Project principles

- Prefer reproducible, inspectable results over unsupported claims.
- Keep projects runnable with free tools wherever practical.
- Document limitations, setup instructions, and next steps.
