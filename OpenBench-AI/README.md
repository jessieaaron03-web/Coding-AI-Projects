# OpenBench AI 🧪

**A free, open-source evaluation lab for language models.** Run repeatable question-answering evaluations, inspect individual failures, and compare quality and latency without paying for hosted model APIs.

> **Honest-results policy:** The built-in demo adapter is deterministic test data, not an LLM benchmark. The Ollama adapter can run local models on your own computer at no API cost. Scores depend on your dataset and settings; do not compare results from materially different environments as if they were controlled experiments.

## Features

- JSONL datasets with input validation
- Exact-match and token F1 baseline metrics
- Per-example latency, P50/P95 latency, throughput, and error counts
- JSON and CSV result exports
- Pluggable adapter interface
- Local model evaluation through [Ollama](https://ollama.com/)
- FastAPI endpoint and optional Streamlit report viewer
- Unit tests and GitHub Actions across Python 3.10–3.12
- Docker support for the API

## Quick start: free demo

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
openbench run --dataset data/sample_qa.jsonl --output results/demo.json --csv results/demo.csv
pytest
```

The demo adapter makes no network calls and is useful for checking the pipeline, reports, and dashboard. Its scores should not be interpreted as model quality.

## Evaluate a real local model for free

1. Install Ollama from its official website and start the Ollama service.
2. Download a model that fits your computer, for example:

   ```bash
   ollama pull llama3.2:3b
   ```

3. Run an evaluation:

   ```bash
   openbench run --adapter ollama --model llama3.2:3b --dataset data/sample_qa.jsonl --output results/ollama.json --csv results/ollama.csv
   ```

No hosted API key is required. Local model downloads require disk space and local compute. You can configure the server with `--base-url` or `OPENBENCH_OLLAMA_URL`, and choose a default model with `OPENBENCH_OLLAMA_MODEL`.

## Explore results

Install dashboard dependencies:

```bash
python -m pip install -e ".[dashboard]"
streamlit run dashboard/app.py
```

Upload a generated JSON report in the dashboard to inspect metrics and individual predictions.

## API

Start the local API from the project root:

```bash
uvicorn openbench.api:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the interactive API documentation. The API currently uses the demo adapter.

## Dataset format

Each non-empty line in a dataset is one JSON object:

```json
{"id":"capital-france","question":"What is the capital of France?","expected_answer":"Paris"}
```

Every row needs non-empty string fields `id`, `question`, and `expected_answer`. Use your own task-specific dataset to get meaningful results.

## Metrics and limitations

- **Exact match** normalizes case and whitespace only. It does not account for equivalent meanings.
- **Token F1** measures overlap between whitespace-separated tokens. It is a basic lexical baseline, not a semantic correctness score.
- **P50/P95 latency** summarize observed per-example wall-clock latency. Results depend on model warm-up, hardware, concurrency, and network conditions.
- **Throughput** is examples processed per second for the complete sequential run.
- **Error count** counts failed generations. A failed generation receives an empty prediction; review the per-example error field.
- **Cost is not currently measured.** Local Ollama inference has no per-token API bill, but does use your computer's resources and electricity.
- This is an early-stage project. It does not yet provide confidence intervals, a validated LLM-as-judge metric, parallel load testing, or dataset versioning.

See [the evaluation methodology](docs/evaluation-methodology.md), [architecture notes](docs/architecture.md), [contributing guide](CONTRIBUTING.md), and [security policy](SECURITY.md).

## Roadmap

- [x] Deterministic demo adapter
- [x] Local Ollama adapter
- [x] JSON/CSV reports and baseline metrics
- [x] P50/P95 latency, throughput, and error reporting
- [ ] Multiple-run comparison and confidence intervals
- [ ] Additional provider adapters
- [ ] Dataset versioning and rubric-based evaluation
- [ ] Cost accounting for hosted providers

## License

MIT. See [LICENSE](LICENSE).
