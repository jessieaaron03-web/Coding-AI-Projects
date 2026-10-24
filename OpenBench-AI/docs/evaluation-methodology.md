# Evaluation methodology

## Purpose

OpenBench AI is a small, inspectable starting point for evaluating question-answering systems. It is not a leaderboard and it does not claim that one model is universally better than another.

## Reproducible runs

For comparisons, keep the dataset, prompt, model identifier, decoding settings, hardware, software versions, and run conditions fixed where possible. The Ollama adapter requests temperature 0 and seed 42, but model/runtime changes can still affect output. Warm-up and model loading can affect observed latency. Run multiple trials for serious comparisons and report variation rather than relying on a single run.

The current report records the adapter name, UTC timestamp, dataset size, a SHA-256 fingerprint of the canonicalized dataset records, run duration, per-example predictions, baseline scores, latency, and generation errors. The fingerprint helps identify whether the dataset records changed, but it is not a substitute for archiving the dataset and settings.

## Metrics

- **Exact match:** Case- and whitespace-normalized string equality. Useful for exact-answer tasks, but overly strict when multiple answers are valid.
- **Token F1:** Overlap-based F1 over whitespace-separated normalized tokens. This is a lexical baseline and does not measure semantic equivalence.
- **P50/P95 latency:** Median and linearly interpolated 95th percentile of per-example wall-clock timings observed during a sequential run.
- **Examples per second:** Number of dataset examples divided by total run wall-clock time.
- **Error count:** Number of examples whose adapter raised an exception or returned a non-string value.

A failed generation receives an empty prediction and an error string in the row. Review failures separately; do not silently discard them from reports.

## Recommended comparison protocol

1. Define the task and success criteria before running models.
2. Use a held-out dataset representative of the intended workload.
3. Run the same examples with the same prompt and generation settings.
4. Record exact model versions and environment details.
5. Repeat runs when latency or sampling variability matters.
6. Inspect a sample of successes and failures manually.
7. Report limitations, missing examples, errors, and uncertainty.
8. Do not infer broad capability from the tiny bundled sample dataset.

## Known limitations

The current implementation does not calculate confidence intervals, semantic similarity, a validated model-judge score, per-token hosted API cost, or parallel throughput. It does not automatically capture all hardware and generation settings or version datasets. Add these before using the tool for high-stakes decisions or publishing a comparative leaderboard.
