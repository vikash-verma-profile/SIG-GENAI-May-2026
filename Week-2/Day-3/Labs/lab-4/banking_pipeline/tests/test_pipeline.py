"""Smoke test for banking pipeline."""
import sys
from pathlib import Path

import pandas as pd

LAB_ROOT = Path(__file__).resolve().parent.parent.parent

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import main as banking_main  # noqa: E402


def test_data_loaded():
    df = pd.read_csv(LAB_ROOT / "data" / "transactions.csv")
    assert df.shape[0] > 0


def test_pipeline_writes_outputs(tmp_path, monkeypatch):
    monkeypatch.setattr(banking_main, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(banking_main, "DATA_PATH", LAB_ROOT / "data" / "transactions.csv")

    banking_main.run_pipeline()

    clean_df = pd.read_csv(tmp_path / "clean.csv")
    agg_df = pd.read_csv(tmp_path / "agg.csv")

    assert "is_fraud" in clean_df.columns
    assert clean_df.duplicated().sum() == 0

    totals = dict(zip(agg_df["account_id"], agg_df["amount"]))
    assert totals[1001] == 500
    assert totals[1002] == 200
    assert totals[1003] == 1000
