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
    dataset = [{"id":"1","question":"Capital?","expected_answer":"Paris"}]
    report = evaluate(dataset, GoodAdapter())
    assert report["summary"]["exact_match"] == 1.0
    assert report["dataset_size"] == 1
    assert report["results"][0]["error"] is None

def test_adapter_failure_is_recorded():
    dataset = [{"id":"1","question":"Capital?","expected_answer":"Paris"}]
    report = evaluate(dataset, BadAdapter())
    assert report["summary"]["error_count"] == 1
    assert report["results"][0]["prediction"] == ""
