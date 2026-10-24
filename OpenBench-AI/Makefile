.PHONY: install test lint demo dashboard api

install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

demo:
	openbench run --dataset data/sample_qa.jsonl --output results/demo.json --csv results/demo.csv

dashboard:
	python -m pip install -e ".[dashboard]"
	streamlit run dashboard/app.py

api:
	uvicorn openbench.api:app --reload
