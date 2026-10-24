# Architecture

OpenBench AI keeps the evaluation pipeline deliberately small so the pieces are easy to inspect and replace.

```text
JSONL dataset
    |
    v
Dataset loader and validation
    |
    v
Adapter.generate(question) ---- DemoAdapter (offline, deterministic)
    |                           OllamaAdapter (local HTTP API)
    v
Prediction + latency + error capture
    |
    v
Exact match / token F1 + run summary
    |
    +--> JSON report
    +--> CSV per-example report
    +--> Streamlit report viewer
    +--> FastAPI demo endpoint
```

## Extension points

Implement the `ModelAdapter` protocol with a stable `name` and a `generate(question: str) -> str` method. Keep provider-specific network code in the adapter; the runner handles timing, errors, and metrics.

## Data flow and privacy

The demo adapter does not make network calls. The Ollama adapter sends prompts to the configured Ollama server, normally on the same computer. If you change the server URL, prompts will be sent to that endpoint. Avoid uploading sensitive datasets to services you do not control.

The project currently stores reports as local JSON and CSV files. It does not include authentication, multi-user isolation, or access control for a publicly exposed API. Keep the API on localhost or behind appropriate access controls; do not expose it directly to the public internet without hardening it.
