import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="OpenBench AI", page_icon="🧪", layout="wide")
st.title("🧪 OpenBench AI")
st.caption(
    "Compare saved evaluation runs. Demo results validate the pipeline only; "
    "they are not evidence of real model quality."
)

uploads = st.file_uploader(
    "Upload one or more OpenBench JSON reports",
    type=["json"],
    accept_multiple_files=True,
)
reports = []
for upload in uploads:
    try:
        report = json.load(upload)
        if not isinstance(report, dict) or not isinstance(report.get("summary"), dict):
            st.warning(f"Skipped {upload.name}: not a recognized OpenBench report.")
            continue
        report["_filename"] = upload.name
        reports.append(report)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        st.warning(f"Could not read {upload.name}: {exc}")

if not reports:
    default_path = Path("results/demo.json")
    if default_path.exists():
        try:
            report = json.loads(default_path.read_text(encoding="utf-8"))
            if isinstance(report, dict) and isinstance(report.get("summary"), dict):
                report["_filename"] = default_path.name
                reports.append(report)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            st.warning(f"Could not read {default_path}: {exc}")

if not reports:
    st.info(
        "Run an evaluation with the CLI, then upload the resulting JSON file. "
        "For a free real-model run, use the local Ollama adapter."
    )
    st.stop()

comparison_rows = []
for report in reports:
    summary = report["summary"]
    comparison_rows.append(
        {
            "Report": report.get("_filename", "uploaded report"),
            "Adapter": report.get("adapter", "unknown"),
            "Examples": report.get("dataset_size", 0),
            "Exact match": summary.get("exact_match"),
            "Token F1": summary.get("token_f1"),
            "Mean latency (ms)": summary.get("mean_latency_ms"),
            "P50 latency (ms)": summary.get("p50_latency_ms"),
            "P95 latency (ms)": summary.get("p95_latency_ms"),
            "Examples/sec": summary.get("examples_per_second"),
            "Errors": summary.get("error_count"),
            "Created": report.get("created_at", "unknown"),
        }
    )

st.subheader("Run comparison")
st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True, hide_index=True)

selected_label = st.selectbox(
    "Inspect run",
    options=[
        f"{report.get('_filename', 'report')} — {report.get('adapter', 'unknown')}"
        for report in reports
    ],
)
selected_index = next(
    index
    for index, report in enumerate(reports)
    if f"{report.get('_filename', 'report')} — {report.get('adapter', 'unknown')}"
    == selected_label
)
selected = reports[selected_index]
summary = selected["summary"]

st.subheader(f"Run details — {selected.get('adapter', 'unknown adapter')}")
st.write(
    f"Created: {selected.get('created_at', 'unknown')} · "
    f"Dataset size: {selected.get('dataset_size', 0)} · "
    f"Schema: {selected.get('schema_version', 'unknown')} · "
    f"Dataset SHA-256: {selected.get('dataset_sha256', 'not recorded')}"
)

metrics = [
    ("Exact match", f"{summary.get('exact_match', 0):.1%}"),
    ("Token F1", f"{summary.get('token_f1', 0):.1%}"),
    ("Mean latency", f"{summary.get('mean_latency_ms', 0):.2f} ms"),
    ("P50 latency", f"{summary.get('p50_latency_ms', 0):.2f} ms"),
    ("P95 latency", f"{summary.get('p95_latency_ms', 0):.2f} ms"),
    ("Examples/sec", f"{summary.get('examples_per_second', 0):.2f}"),
    ("Errors", str(summary.get("error_count", 0))),
]
columns = st.columns(len(metrics))
for column, (label, value) in zip(columns, metrics):
    column.metric(label, value)

frame = pd.DataFrame(selected.get("results", []))
if not frame.empty:
    st.subheader("Per-example results")
    st.dataframe(frame, use_container_width=True, hide_index=True)
    st.download_button(
        "Download selected run as CSV",
        frame.to_csv(index=False).encode("utf-8"),
        "openbench-results.csv",
        "text/csv",
    )
