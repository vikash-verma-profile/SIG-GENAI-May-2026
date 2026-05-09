"""Lab 9 starter: Smart city traffic dashboard (Streamlit)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "traffic_sensors.json"


@st.cache_data
def load_traffic() -> pd.DataFrame:
    with open(DATA_PATH, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))


def main() -> None:
    st.set_page_config(page_title="Smart City Traffic", layout="wide")
    st.title("Smart city traffic analytics")

    df = load_traffic()

    c1, c2, c3 = st.columns(3)
    c1.metric("Avg congestion index", f"{df['congestion_index'].mean():.2f}")
    c2.metric("Total incidents", int(df["incidents"].sum()))
    c3.metric("Corridors monitored", len(df))

    high = df[df["congestion_index"] >= 0.8]
    st.subheader("Sensor alerts (high congestion)")
    if high.empty:
        st.info("No corridors above 0.8 in sample data.")
    else:
        st.dataframe(high, use_container_width=True)

    st.subheader("All corridors")
    st.dataframe(df, use_container_width=True)

    st.subheader("Congestion by corridor")
    st.bar_chart(df.set_index("corridor")["congestion_index"])


if __name__ == "__main__":
    main()
