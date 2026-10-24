import hashlib
import json
from datetime import datetime, timezone
from statistics import mean, median
from time import perf_counter

from openbench.metrics import exact_match, token_f1


def _percentile(values: list[float], percentile: float) -> float:
    """Return a linearly interpolated percentile for a non-empty list."""
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def evaluate(dataset: list[dict[str, str]], adapter) -> dict:
    if not dataset:
        raise ValueError("Dataset must contain at least one example.")

    canonical_dataset = json.dumps(
        dataset,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    dataset_sha256 = hashlib.sha256(canonical_dataset).hexdigest()

    results = []
    run_start = perf_counter()
    for example in dataset:
        start = perf_counter()
        error = None
        try:
            prediction = adapter.generate(example["question"])
            if not isinstance(prediction, str):
                raise TypeError("Adapter output must be a string")
        except Exception as exc:
            prediction = ""
            error = f"{type(exc).__name__}: {exc}"
        latency_ms = (perf_counter() - start) * 1000
        results.append(
            {
                "id": example["id"],
                "question": example["question"],
                "expected_answer": example["expected_answer"],
                "prediction": prediction,
                "exact_match": exact_match(prediction, example["expected_answer"]),
                "token_f1": token_f1(prediction, example["expected_answer"]),
                "latency_ms": round(latency_ms, 3),
                "error": error,
            }
        )

    total_seconds = max(perf_counter() - run_start, 1e-9)
    latencies = [row["latency_ms"] for row in results]
    return {
        "project": "OpenBench AI",
        "schema_version": "1.2",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "adapter": adapter.name,
        "dataset_size": len(results),
        "dataset_sha256": dataset_sha256,
        "run_duration_seconds": round(total_seconds, 6),
        "summary": {
            "exact_match": round(mean(row["exact_match"] for row in results), 4),
            "token_f1": round(mean(row["token_f1"] for row in results), 4),
            "mean_latency_ms": round(mean(latencies), 3),
            "p50_latency_ms": round(median(latencies), 3),
            "p95_latency_ms": round(_percentile(latencies, 0.95), 3),
            "examples_per_second": round(len(results) / total_seconds, 3),
            "error_count": sum(row["error"] is not None for row in results),
        },
        "results": results,
    }
