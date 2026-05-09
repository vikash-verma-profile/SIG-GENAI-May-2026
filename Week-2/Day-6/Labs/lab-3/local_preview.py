"""
Optional local preview (Lab 3): loads sample JSON — primary path is Lovable.dev.

Run: streamlit run local_preview.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "sample_healthcare_etl.json"


def main() -> None:
    st.set_page_config(page_title="Healthcare ETL — Local Preview", layout="wide")
    st.title("Healthcare ETL status (local preview)")
    st.caption("Build the richer UI in Lovable.dev; this file is optional.")

    with open(DATA, encoding="utf-8") as f:
        rows = json.load(f)
    df = pd.DataFrame(rows)

    failed = df[df["status"].str.lower() == "failed"]
    st.metric("Failed pipelines", len(failed))
    if not failed.empty:
        st.error("Failed pipeline alerts")
        st.dataframe(failed, use_container_width=True)

    dept = st.sidebar.selectbox("Department", sorted(df["department"].unique()))
    st.dataframe(df[df["department"] == dept], use_container_width=True)


if __name__ == "__main__":
    main()
