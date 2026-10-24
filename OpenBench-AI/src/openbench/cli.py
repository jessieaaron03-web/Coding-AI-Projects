import argparse
import json
import os

from openbench.adapters.demo import DemoAdapter
from openbench.adapters.ollama import OllamaAdapter
from openbench.dataset import load_jsonl
from openbench.report import save_csv, save_json
from openbench.runner import evaluate


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="openbench",
        description="Run a reproducible OpenBench AI evaluation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run an evaluation")
    run_parser.add_argument("--dataset", required=True, help="Path to a JSONL dataset")
    run_parser.add_argument("--output", default="results/latest.json", help="JSON report path")
    run_parser.add_argument("--csv", default=None, help="Optional per-example CSV output")
    run_parser.add_argument(
        "--adapter",
        choices=["demo", "ollama"],
        default="demo",
        help="Use deterministic demo answers or a local Ollama model",
    )
    run_parser.add_argument(
        "--model",
        default=os.getenv("OPENBENCH_OLLAMA_MODEL", "llama3.2:3b"),
        help="Ollama model name (used only with --adapter ollama)",
    )
    run_parser.add_argument(
        "--base-url",
        default=os.getenv("OPENBENCH_OLLAMA_URL", "http://localhost:11434"),
        help="Ollama server URL (used only with --adapter ollama)",
    )
    args = parser.parse_args()

    dataset = load_jsonl(args.dataset)
    adapter = DemoAdapter() if args.adapter == "demo" else OllamaAdapter(
        model=args.model,
        base_url=args.base_url,
    )
    report = evaluate(dataset, adapter)
    save_json(report, args.output)
    if args.csv:
        save_csv(report, args.csv)
    print(
        json.dumps(
            {"output": args.output, "adapter": report["adapter"], **report["summary"]},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
