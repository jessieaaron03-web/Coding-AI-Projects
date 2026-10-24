import pytest

from openbench.runner import evaluate


class GoodAdapter:
    name = "test"

    def generate(self, question):
        return "Paris"


class BadAdapter:
    name = "bad"

    def generate(self, question):
        raise RuntimeError("example failure")


def test_evaluate_returns_summary():
    dataset = [{"id": "1", "question": "Capital?", "expected_answer": "Paris"}]
    report = evaluate(dataset, GoodAdapter())

    assert report["summary"]["exact_match"] == 1.0
    assert report["dataset_size"] == 1
    assert report["results"][0]["error"] is None
    assert report["summary"]["p50_latency_ms"] >= 0
    assert report["summary"]["p95_latency_ms"] >= 0
    assert report["summary"]["examples_per_second"] > 0
    assert len(report["dataset_sha256"]) == 64
    assert report["run_duration_seconds"] > 0


def test_adapter_failure_is_recorded():
    dataset = [{"id": "1", "question": "Capital?", "expected_answer": "Paris"}]
    report = evaluate(dataset, BadAdapter())

    assert report["summary"]["error_count"] == 1
    assert report["results"][0]["prediction"] == ""
    assert "example failure" in report["results"][0]["error"]


def test_empty_dataset_is_rejected():
    with pytest.raises(ValueError, match="at least one example"):
        evaluate([], GoodAdapter())
