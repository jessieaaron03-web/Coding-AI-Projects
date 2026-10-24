from datetime import datetime, timezone
from statistics import mean
from time import perf_counter
from openbench.metrics import exact_match, token_f1

def evaluate(dataset: list[dict[str, str]], adapter) -> dict:
    results = []
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
        results.append({
            "id": example["id"], "question": example["question"],
            "expected_answer": example["expected_answer"], "prediction": prediction,
            "exact_match": exact_match(prediction, example["expected_answer"]),
            "token_f1": token_f1(prediction, example["expected_answer"]),
            "latency_ms": round(latency_ms, 3), "error": error,
        })
    return {
        "project": "OpenBench AI", "schema_version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "adapter": adapter.name, "dataset_size": len(results),
        "summary": {
            "exact_match": round(mean(r["exact_match"] for r in results), 4),
            "token_f1": round(mean(r["token_f1"] for r in results), 4),
            "mean_latency_ms": round(mean(r["latency_ms"] for r in results), 3),
            "error_count": sum(r["error"] is not None for r in results),
        },
        "results": results,
    }
