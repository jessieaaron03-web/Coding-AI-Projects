import json
from io import BytesIO
from urllib.error import URLError

import pytest

from openbench.adapters.ollama import OllamaAdapter


class FakeResponse:
    def __init__(self, payload: dict):
        self.body = BytesIO(json.dumps(payload).encode("utf-8"))

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body.read()


def test_ollama_adapter_posts_chat_request(monkeypatch):
    seen = {}

    def fake_urlopen(request, timeout):
        seen["url"] = request.full_url
        seen["timeout"] = timeout
        seen["payload"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse({"message": {"content": "  Paris  "}})

    monkeypatch.setattr("openbench.adapters.ollama.urlopen", fake_urlopen)
    adapter = OllamaAdapter(model="tiny-model", base_url="http://localhost:11434/")

    assert adapter.generate("Capital of France?") == "Paris"
    assert adapter.name == "ollama:tiny-model"
    assert seen["url"] == "http://localhost:11434/api/chat"
    assert seen["payload"]["model"] == "tiny-model"
    assert seen["payload"]["stream"] is False
    assert seen["payload"]["messages"][0]["content"] == "Capital of France?"


def test_ollama_adapter_explains_connection_failure(monkeypatch):
    def fail_urlopen(_request, timeout):
        raise URLError("connection refused")

    monkeypatch.setattr("openbench.adapters.ollama.urlopen", fail_urlopen)
    adapter = OllamaAdapter()

    with pytest.raises(RuntimeError, match="Is Ollama installed and running"):
        adapter.generate("hello")


def test_ollama_adapter_rejects_unexpected_response(monkeypatch):
    monkeypatch.setattr(
        "openbench.adapters.ollama.urlopen",
        lambda _request, timeout: FakeResponse({"unexpected": "shape"}),
    )
    with pytest.raises(RuntimeError, match="did not contain"):
        OllamaAdapter().generate("hello")
