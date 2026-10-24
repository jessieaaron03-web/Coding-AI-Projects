# OpenBench AI

A reproducible evaluation lab for language models. OpenBench AI runs consistent tests, scores model outputs, measures latency, and exports results. This is an early MVP with a deterministic demo adapter; demo results are not evidence of real-world model quality.

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
openbench run --dataset data/sample_qa.jsonl --output results/demo.json --csv results/demo.csv
pytest
```

## Features

- Exact-match and token F1 baselines
- Per-example latency measurements
- JSON and CSV exports
- FastAPI evaluation endpoint
- Optional Streamlit dashboard
- Tests and GitHub Actions CI

## Important limitations

The included `demo` adapter makes no network calls. Exact match and token F1 are simple baselines, not semantic correctness metrics. Cost is not measured until a real provider adapter reports token usage and pricing. Do not treat demo results as model benchmarks.

## Roadmap

- [ ] Hosted model adapters
- [ ] Token usage and cost accounting
- [ ] Confidence intervals
- [ ] Validated rubric-based scoring
- [ ] Side-by-side run comparisons
- [ ] Dataset versioning and safety test suites

See `CONTRIBUTING.md` for contribution guidance. Licensed under MIT.