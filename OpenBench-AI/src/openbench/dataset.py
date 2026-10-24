import json
from pathlib import Path

def load_jsonl(path: str | Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            required = ("id", "question", "expected_answer")
            missing = [key for key in required if not isinstance(row.get(key), str) or not row[key].strip()]
            if missing:
                raise ValueError(f"Line {line_number} is missing non-empty fields: {', '.join(missing)}")
            rows.append({key: row[key] for key in required})
    if not rows:
        raise ValueError("Dataset is empty.")
    return rows
