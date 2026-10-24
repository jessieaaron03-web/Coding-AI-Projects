import argparse
import json
from openbench.adapters.demo import DemoAdapter
from openbench.dataset import load_jsonl
from openbench.report import save_csv, save_json
from openbench.runner import evaluate

def main() -> None:
    parser = argparse.ArgumentParser(prog="openbench", description="Run an OpenBench AI evaluation.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run an evaluation")
    run_parser.add_argument("--dataset", required=True, help="Path to a JSONL dataset")
    run_parser.add_argument("--output", default="results/latest.json", help="JSON report path")
    run_parser.add_argument("--csv", default=None, help="Optional per-example CSV output")
    run_parser.add_argument("--adapter", choices=["demo"], default="demo", help="Model adapter")
    args = parser.parse_args()
    report = evaluate(load_jsonl(args.dataset), DemoAdapter())
    save_json(report, args.output)
    if args.csv:
        save_csv(report, args.csv)
    print(json.dumps({"output": args.output, "adapter": report["adapter"], **report["summary"]}, indent=2))

if __name__ == "__main__":
    main()
