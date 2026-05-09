"""Lab 7 starter: DataOps / IoT portal (Streamlit)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "iot_device_metrics.json"


@st.cache_data
def load_devices() -> pd.DataFrame:
    with open(DATA_PATH, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))


def main() -> None:
    st.set_page_config(page_title="DataOps Portal", layout="wide")
    st.title("Manufacturing DataOps portal")

    df = load_devices()

    line = st.sidebar.selectbox("Production line", sorted(df["line"].unique()))
    filtered = df[df["line"] == line]

    st.subheader("Device metrics")
    st.dataframe(filtered, use_container_width=True)

    st.subheader("Uptime by device")
    fig = px.bar(filtered, x="device_id", y="uptime_pct", title="Uptime %")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Alerts")
    alerts = df[df["alert_level"] != "none"]
    if alerts.empty:
        st.success("No active device alerts in sample data.")
    else:
        st.warning("Devices with alerts")
        st.dataframe(alerts, use_container_width=True)


if __name__ == "__main__":
    main()
