"""Tests for retail pipeline."""
from pathlib import Path

import pandas as pd

import main as pipeline_main

LAB_ROOT = Path(__file__).resolve().parent.parent


def test_orders_not_empty():
    df = pd.read_csv(LAB_ROOT / "data" / "orders.csv")
    assert df.shape[0] > 0


def test_pipeline_outputs_after_run(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline_main, "OUT_DIR", tmp_path)
    monkeypatch.setattr(pipeline_main, "DATA_PATH", LAB_ROOT / "data" / "orders.csv")
    pipeline_main.run_pipeline()
    assert (tmp_path / "revenue.csv").is_file()
    assert (tmp_path / "daily_sales.csv").is_file()
