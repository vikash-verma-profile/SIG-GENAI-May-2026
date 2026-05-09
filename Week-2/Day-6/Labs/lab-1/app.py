"""Lab 1 starter: Streamlit pipeline health dashboard (extend with AI)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
METADATA_PATH = ROOT / "metadata.json"


@st.cache_data
def load_metadata() -> pd.DataFrame:
    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"Missing {METADATA_PATH.name} next to app.py.")
    with open(METADATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)


def main() -> None:
    st.set_page_config(page_title="Pipeline Health", layout="wide")
    st.title("Pipeline Health Dashboard")

    try:
        df = load_metadata()
    except FileNotFoundError as e:
        st.error(str(e))
        return

    ok = (df["status"].str.lower() == "success").sum()
    failed = (df["status"].str.lower() == "failed").sum()
    rows = int(df["row_count"].sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Successful pipelines", ok)
    c2.metric("Failed pipelines", failed)
    c3.metric("Total rows processed", f"{rows:,}")
    c4.metric("Pipelines tracked", len(df))

    st.subheader("Alerts")
    bad = df[df["status"].str.lower() != "success"]
    if bad.empty:
        st.success("No failing pipelines in metadata.")
    else:
        st.warning("Failure or non-success status detected.")
        st.dataframe(bad, use_container_width=True)

    st.subheader("All pipelines")
    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
