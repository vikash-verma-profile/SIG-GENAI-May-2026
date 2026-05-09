"""Lab 4 starter: telecom pipeline monitor (mirrors what you might build in Replit)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "telecom_pipelines.json"


@st.cache_data
def load_data() -> pd.DataFrame:
    with open(DATA_PATH, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))


def main() -> None:
    st.set_page_config(page_title="Telecom Pipeline Monitor", layout="wide")
    st.title("Telecom pipeline monitoring")

    df = load_data()

    q = st.text_input("Search pipeline or region", "")
    if q:
        mask = (
            df["pipeline"].str.contains(q, case=False, na=False)
            | df["region"].str.contains(q, case=False, na=False)
        )
        df = df[mask]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total alerts", int(df["alert_count"].sum()))
    failed = (df["status"].str.lower() == "failed").sum()
    c2.metric("Failed runs", int(failed))
    c3.metric("Pipelines", len(df))

    st.subheader("Status")
    st.dataframe(df, use_container_width=True)

    st.bar_chart(df.set_index("pipeline")["duration_sec"])


if __name__ == "__main__":
    main()
