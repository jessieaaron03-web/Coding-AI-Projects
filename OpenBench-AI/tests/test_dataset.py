import json
import pytest
from openbench.dataset import load_jsonl

def test_load_jsonl(tmp_path):
    path = tmp_path / "data.jsonl"
    path.write_text(json.dumps({"id":"1","question":"Q?","expected_answer":"A"}) + "\n")
    assert load_jsonl(path)[0]["id"] == "1"

def test_invalid_row_fails(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text('{"id":"1"}\n')
    with pytest.raises(ValueError, match="missing"):
        load_jsonl(path)
