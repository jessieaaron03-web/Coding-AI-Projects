from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openbench.adapters.demo import DemoAdapter
from openbench.dataset import load_jsonl
from openbench.runner import evaluate

app = FastAPI(title="OpenBench AI", version="0.1.0",
              description="Minimal API for reproducible LLM evaluation.")

class EvaluationRequest(BaseModel):
    dataset_path: str = Field(default="data/sample_qa.jsonl", description="Local JSONL dataset path")

@app.get("/health")
def health():
    return {"status": "ok", "project": "OpenBench AI"}

@app.post("/evaluate")
def run_evaluation(request: EvaluationRequest):
    path = Path(request.dataset_path)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Dataset file not found")
    try:
        return evaluate(load_jsonl(path), DemoAdapter())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
