import json
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="OpenBench AI", page_icon="🧪", layout="wide")
st.title("🧪 OpenBench AI")
st.caption("Demo metrics are not claims about real model quality.")
uploaded = st.file_uploader("Upload an OpenBench JSON report", type=["json"])
default_path = Path("results/demo.json")
report = None
if uploaded is not None:
    report = json.load(uploaded)
elif default_path.exists():
    report = json.loads(default_path.read_text(encoding="utf-8"))
if report is None:
    st.info("Run an evaluation and upload its JSON report to explore results.")
    st.stop()
summary = report.get("summary", {})
c1, c2, c3, c4 = st.columns(4)
c1.metric("Exact match", f"{summary.get('exact_match', 0):.1%}")
c2.metric("Token F1", f"{summary.get('token_f1', 0):.1%}")
c3.metric("Mean latency", f"{summary.get('mean_latency_ms', 0):.2f} ms")
c4.metric("Errors", summary.get("error_count", 0))
st.subheader(f"Run details — {report.get('adapter', 'unknown adapter')}")
st.write(f"Created: {report.get('created_at', 'unknown')} · Dataset size: {report.get('dataset_size', 0)}")
frame = pd.DataFrame(report.get("results", []))
if not frame.empty:
    st.dataframe(frame, use_container_width=True)
    st.download_button("Download result rows as CSV", frame.to_csv(index=False).encode("utf-8"),
                       "openbench-results.csv", "text/csv")
